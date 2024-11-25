# trans2vec
This repository provides a new implementation of the trans2vec algorithm, 
inspired by the paper "[Who Are the Phishers? Phishing Scam Detection on Ethereum via Network Embedding](https://ieeexplore.ieee.org/document/9184813)". 
Note that this version not fully replicate the performance of the original paper due to the absence of the original implementation and dataset.

# Requirements:
- argparse
- scipy
- numpy
- pandas
- gensim
- sklearn
- numba

# Run the demo
```
python trans2vec.py
```

# Feature
Graph-based Network Embedding:
(1)Loads Ethereum transaction data from .npz files.
(2)Performs biased random walks on the graph to capture structural and temporal information.
(3)Generates low-dimensional node embeddings using Word2Vec.

Classification:
(1)Splits the data into training and test sets.
(2)Uses LightGBM as the classifier to distinguish phishing accounts from normal accounts.

Export Embeddings:
Outputs the generated embedding vectors into a text file (embeddings.txt), where each line represents the vector for one node.

# Dataset
The example implementation uses a dataset provided in the dataset/tedge.npz file. This dataset includes:

- Adjacency matrix of the Ethereum transaction graph.
- Transaction amount data.
- Timestamp data.
- Node labels indicating phishing or normal accounts.
If you want to learn more about the dataset, refer to the paper "T-EDGE: Temporal WEighted MultiDiGraph Embedding for Ethereum Transaction Network Analysis".

# output
(1) A text file named embeddings.txt is generated. Each line contains the embedding of a single node in the following format: node_id dimension1 dimension2 ... dimensionN
(2) Classification Report: The performance of the LightGBM model is displayed in the terminal, including metrics such as precision, recall, F1-score, and accuracy.

# Cite
Please cite our paper if you use this dataset in your own work:
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

Please cite our paper if you use this code in your own work:
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