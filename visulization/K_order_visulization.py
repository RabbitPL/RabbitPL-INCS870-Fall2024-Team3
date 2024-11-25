import pandas as pd
import networkx as nx
from decimal import Decimal
from pyvis.network import Network
import urllib.request as urlrequest
import json

apikey = "93C5MJFXC6RVB4J4JETKK4I85UQA5KY65I"  # 这个换成自己账户的apikey

# 将 Wei 转换为 Ether
def wei2ether(s):
    length = len(s)
    t = length - 18
    if t > 0:
        s1 = s[:t] + "." + s[t:]
    else:
        x = 18 - length
        s1 = "0." + "0" * x + s
    return Decimal(s1)


# 加载交易数据并过滤
def load_Tx(list_result):
    df_out = pd.DataFrame(
        columns=['TxHash', 'BlockHeight', 'TimeStamp', 'From', 'To', 'Value', 'ContractAddress', 'Input', 'isError'])

    for dic_txs in list_result:
        # 检查交易是否为错误的或者金额为 0
        if dic_txs["isError"] == '1' or dic_txs["value"] == "0":
            continue  # 如果交易失败或者金额为 0 则跳过

        value_in_ether = float(wei2ether(dic_txs["value"]))  # 确保转换为 float
        t1 = (dic_txs['hash'], dic_txs['blockNumber'], dic_txs['timeStamp'], dic_txs["from"], dic_txs["to"],
              value_in_ether, dic_txs["contractAddress"], dic_txs["input"], dic_txs["isError"])
        t = [x if x != "" else 'NULL' for x in t1]
        s = pd.Series({'TxHash': t[0], 'BlockHeight': t[1], 'TimeStamp': t[2], 'From': t[3], 'To': t[4],
                       'Value': t[5], 'ContractAddress': t[6], 'Input': t[7], 'isError': t[8]})
        df_out = pd.concat([df_out, s.to_frame().T], ignore_index=True)

    # 打印交易记录中的 'Value' 列，确保金额不为 0
    print("transaction record:", df_out[['From', 'To', 'Value']])

    return df_out

# 加载以太坊地址的交易数据
def load_url(address):
    url_outer = f'http://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={apikey}'
    crawl_outer = urlrequest.urlopen(url_outer).read()
    json_outer = json.loads(crawl_outer.decode('utf8'))

    if json_outer["status"] == "1":
        result_outer = json_outer['result']
    else:
        result_outer = []

    df_outer = load_Tx(result_outer)

    url_inter = f'http://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={apikey}'
    crawl_inter = urlrequest.urlopen(url_inter).read()
    json_inter = json.loads(crawl_inter.decode('utf8'))

    if json_inter["status"] == "1":
        result_inter = json_inter['result']
    else:
        result_inter = []

    df_inter = load_Tx(result_inter)

    df_outer = pd.concat([df_outer, df_inter], ignore_index=True)  # 使用 pd.concat 替换 append
    df_outer = df_outer.sort_values(by="TimeStamp")
    return df_outer


# 获取邻居账户列表
def get_neighbor_list(df_address, address):
    set_neighbor = set()
    for i in df_address.index:
        # 过滤金额为 0 的交易
        if df_address.Value.iloc[i] == 0:
            continue  # 跳过金额为 0 的交易
        if str.lower(df_address.From.iloc[i]) != str.lower(address):
            # 打印调试信息，查看金额
            print(f"Adding neighbor from {df_address.From.iloc[i]} to {df_address.To.iloc[i]} with value: {df_address.Value.iloc[i]}")
            set_neighbor.add((str.lower(df_address.From.iloc[i]), float(df_address.Value.iloc[i])))  # 转为 float
        elif str.lower(df_address.To.iloc[i]) != str.lower(address):
            # 打印调试信息，查看金额
            print(f"Adding neighbor from {df_address.From.iloc[i]} to {df_address.To.iloc[i]} with value: {df_address.Value.iloc[i]}")
            set_neighbor.add((str.lower(df_address.To.iloc[i]), float(df_address.Value.iloc[i])))  # 转为 float

    # 打印获取到的邻居账户和交易金额
    print(f"Neighbors for {address}: {set_neighbor}")  # 打印邻居账户和交易金额
    return list(set_neighbor)

# 递归获取K阶邻居账户
def get_k_order_neighbors(k, i, address, neighbors_dict):
    if i >= k:  # 当递归深度等于或超过k时停止递归
        return

    # 加载交易记录
    df_address = load_url(address)

    # 获取当前地址的直接邻居（1阶邻居）
    list_neighbor = get_neighbor_list(df_address, address)
    neighbors_dict[address] = list_neighbor  # 将邻居列表存入字典

    # 递归调用以获取更高阶的邻居
    for neighbor, value in list_neighbor:
        if neighbor not in neighbors_dict:
            get_k_order_neighbors(k, i + 1, neighbor, neighbors_dict)  # 递归获取下一阶邻居


# 可视化交易图
def visualize_graph(address, neighbors_dict):
    G = nx.Graph()

    # 添加节点和边
    for node, neighbors in neighbors_dict.items():
        G.add_node(node)  # 确保节点添加正确
        for neighbor, value in neighbors:
            print(f"Adding edge from {node} to {neighbor} with value: {value}")  # 调试输出
            # 明确在 networkx 中为边设置 weight 属性
            G.add_edge(node, neighbor, weight=float(value))  # 将交易金额转换为浮点数

    # 用 pyvis 进行可视化
    net = Network(notebook=False, height="750px", width="100%", directed=False)

    # 不使用 from_nx，手动添加节点和边以确保正确的 value 和 title 被传递
    for node in G.nodes:
        net.add_node(node, label=node, title=node, color='red' if node == address else 'blue',
                     size=25 if node == address else 15)

    # 手动为每条边添加 title 和 value
    for from_node, to_node, edge_data in G.edges(data=True):
        weight = edge_data.get('weight', 0)  # 获取 'weight'，如果不存在，默认为 0
        print(f"Edge from {from_node} to {to_node} with weight: {weight}")  # 调试输出
        # 直接使用 pyvis 添加边
        net.add_edge(from_node, to_node, title=f"Value: {weight:.18f} ETH", value=weight)  # 设置边的 title 和 value

    # 保存并展示图
    net.save_graph(f"{address}_k_order_graph.html")


# 主函数：用户输入地址并显示K阶交易图
def main():
    address = input("请输入以太坊账户地址（例：0x002f0c8119c16d310342d869ca8bf6ace34d9c39）: ")
    k = int(input("请输入你要查看的K阶邻居数: "))

    neighbors_dict = {}
    get_k_order_neighbors(k, 0, address, neighbors_dict)

    visualize_graph(address, neighbors_dict)


if __name__ == "__main__":
    main()
