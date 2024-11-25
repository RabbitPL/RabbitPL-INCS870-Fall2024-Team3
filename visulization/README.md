# Ethereum Transaction Network Visualization Tool

This Python script provides a tool to analyze and visualize Ethereum transaction networks. By retrieving Ethereum transaction data from [Etherscan](https://etherscan.io/), it allows users to explore multi-order neighbor relationships and visualize the financial interactions of a specified Ethereum address.

---

## Features

1. **Transaction Data Loading**:
   - Retrieves Ethereum transaction data using Etherscan's API.
   - Processes external (`txlist`) and internal (`txlistinternal`) transaction types.
   - Converts transaction values from Wei to Ether.

2. **Neighbor Exploration**:
   - Identifies direct neighbors (1st-order) and recursively finds K-order neighbors of a given Ethereum address.
   - Filters out transactions with zero values or errors.

3. **Network Visualization**:
   - Constructs a transaction graph using NetworkX.
   - Visualizes the graph with PyVis, including node and edge details such as transaction values.
   - Highlights the queried Ethereum address and its connections.

---

## Requirements

The following Python libraries are required:
- `pandas`
- `networkx`
- `decimal`
- `pyvis`
- `urllib`
- `json`

Install these dependencies using pip:
```bash
pip install pandas networkx pyvis
```

---

## How to Use

1. **Replace the Etherscan API Key**:
   - Update the `apikey` variable in the script with your own API key from [Etherscan](https://etherscan.io/apis).

2. **Run the Script**:
   - Execute the script using Python:
     ```bash
     python eth_visualization.py
     ```

3. **Provide Input**:
   - Enter an Ethereum address when prompted (e.g., `0x002f0c8119c16d310342d869ca8bf6ace34d9c39`).
   - Specify the order of neighbors (K) to explore.

4. **Output**:
   - A network graph will be saved as an HTML file (e.g., `0x002f0c8119c16d310342d869ca8bf6ace34d9c39_k_order_graph.html`).
   - Open the HTML file in a browser to interactively explore the network.

---

## Notes

1. **API Limitations**:
   - Ensure you use a valid API key with sufficient request limits.
   - Data accuracy depends on Etherscan's API.

2. **Customization**:
   - Adjust the visualization (e.g., node size, edge width) in the `visualize_graph()` function.
   - Add more filtering rules or metrics if needed.

3. **Graph Size**:
   - Large K values may result in a complex graph and extended processing times. Use smaller K values for quicker analysis.

---

## Graph

The script generates an interactive graph as an HTML file. When opened in a browser:

1. **Nodes**:
   - The queried Ethereum address is highlighted in **red**.
   - Neighboring addresses are displayed in **blue**.

2. **Edges**:
   - Represent transaction relationships between addresses.
   - Weighted by the transaction value.
   - Tooltips on edges show transaction value details in Ether.
```