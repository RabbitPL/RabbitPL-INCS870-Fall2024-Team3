```markdown
# trans2vec: Ethereum Network Embedding and Node Classification

This repository implements the **trans2vec** algorithm, as described in the paper "[Who Are the Phishers? Phishing Scam Detection on Ethereum via Network Embedding](https://ieeexplore.ieee.org/document/9184813)."  
The trans2vec algorithm embeds Ethereum transaction networks into low-dimensional vector spaces and performs node classification using machine learning. 

---

## Features

1. **Network Embedding:**
   - Implements the **trans2vec** algorithm to generate embeddings for Ethereum accounts based on their transaction history.
   - Balances the influence of transaction amounts and timestamps using a tunable alpha parameter.

2. **Biased Random Walk:**
   - Generates random walk paths from the Ethereum transaction network using a biased random walker.

3. **Node Classification:**
   - Classifies nodes (e.g., phishing vs. non-phishing accounts) using **LightGBM** with the generated embeddings.
   - Outputs performance metrics, including precision, recall, F1-score, and accuracy.

---

## Requirements

The following Python libraries are required:
- `argparse`
- `numpy`
- `scipy`
- `gensim`
- `sklearn`
- `lightgbm`
- `random`
- `numba`

You can install the required libraries using pip:
```bash
pip install numpy scipy gensim lightgbm scikit-learn numba
```

---

## How to Use

1. **Prepare the Dataset:**
   - Ensure you have the dataset `tedge.npz` and `label.txt` in the `dataset/` folder. 
   - The dataset should include:
     - `adj_matrix`: Adjacency matrix of the Ethereum network.
     - `amount_data`: Transaction amounts.
     - `timestamp_data`: Transaction timestamps.
     - `node_label`: Labels for nodes (e.g., phishing = 1, non-phishing = 0).

2. **Run the Script:**
   - Execute the script using the following command:
     ```bash
     python trans2vec.py
     ```

3. **Command-Line Parameters:**
   - Customize parameters like embedding dimensions, random walk length, and alpha:
     ```bash
     python trans2vec.py --dimensions 128 --num_walks 20 --walk_length 10 --alpha 0.5
     ```

4. **Output:**
   - The script generates the embeddings and trains a classifier (LightGBM).
   - Outputs a detailed classification report, including precision, recall, F1-score, and accuracy.

---

## Key Parameters

| Parameter       | Default Value | Description                                           |
|------------------|---------------|-------------------------------------------------------|
| `--dimensions`   | 128           | The number of dimensions for the node embeddings.    |
| `--num_walks`    | 10            | The number of random walks per node.                 |
| `--walk_length`  | 5             | The length of each random walk.                      |
| `--window_size`  | 5             | The context window size for the Word2Vec model.      |
| `--train_size`   | 0.8           | The proportion of data used for training.            |
| `--alpha`        | 0.3           | Balances the influence of transaction amount and time.|

---

## Output

### Classification Report:
The script outputs a detailed classification report after training the LightGBM model. Metrics include:
- Precision
- Recall
- F1-score
- Accuracy

---

## Dataset Information

The required dataset (`tedge.npz`) includes pre-processed Ethereum transaction data, with the following keys:
- `adj_matrix`: The adjacency matrix representing the Ethereum transaction network.
- `amount_data`: Data representing transaction amounts.
- `timestamp_data`: Data representing transaction timestamps.
- `node_label`: Labels for nodes (e.g., phishing = 1, non-phishing = 0).

Refer to the paper "[T-EDGE: Temporal WEighted MultiDiGraph Embedding for Ethereum Transaction Network Analysis](https://arxiv.org/abs/1905.08038)" for details on the dataset's structure.

---

## Notes

1. **Customization:**
   - You can modify parameters like random walk length, dimensions, or alpha to suit your dataset or objectives.

2. **Data Preparation:**
   - Ensure the input dataset is formatted correctly before running the script.

3. **System Requirements:**
   - Ensure sufficient memory for large graphs, as processing large Ethereum networks can be resource-intensive.

---

## Cite

If you use this code or dataset, please cite the following papers:

### T-EDGE Dataset:
```
@ARTICLE{wu2019t,
  TITLE={T-EDGE: Temporal WEighted MultiDiGraph Embedding for Ethereum Transaction Network Analysis},
  AUTHOR={Lin, Dan and Wu, Jiajing and Yuan, Qi and Zheng, Zibin},   
  JOURNAL={Frontiers in Physics},      
  VOLUME={8},      
  number={},      
  PAGES={204},     
  YEAR={2020}
}
```

### Who Are the Phishers Paper:
```
@ARTICLE{wu2019who,
  author={Wu, Jiajing and Yuan, Qi and Lin, Dan and You, Wei and Chen, Weili and Chen, Chuan and Zheng, Zibin},
  journal={IEEE Transactions on Systems, Man, and Cybernetics: Systems}, 
  title={Who Are the Phishers? Phishing Scam Detection on Ethereum via Network Embedding}, 
  year={2022},
  volume={52},
  number={2},
  pages={1156-1166},
}
```
```