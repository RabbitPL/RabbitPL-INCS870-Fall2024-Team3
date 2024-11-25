import argparse
import scipy.sparse as sp
from gensim.models import Word2Vec
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from walker import BiasedRandomWalker
import numpy as np
import random
from utils import *

# Define the random_seed function to ensure consistent results
def random_seed(seed_value):
    random.seed(seed_value)  # Set random seed for Python's random module
    np.random.seed(seed_value)  # Set random seed for NumPy

# The trans2vec class implements the network embedding algorithm,
# including data loading, random walk execution, and embedding generation.
class trans2vec(object):

    def __init__(self, alpha=0.5, dimensions=64, num_walks=20, walk_length=5, window_size=10, workers=1, seed=2022):
        self.alpha = alpha  # Parameter to balance weights between transaction amount and timestamp
        self.dimensions = dimensions  # The dimensionality of the embedding vectors
        self.window_size = window_size  # Context window size for the Word2Vec model
        self.workers = workers  # Number of threads for training the Word2Vec model
        self.seed = seed  # Random seed for reproducibility
        self.walk_length = walk_length  # Length of each random walk
        self.num_walks = num_walks  # Number of random walks per node

        self.walks = None    # Stores the generated random walks
        self.word2vec_model = None  # Stores the trained Word2Vec model
        self.embeddings = None  # Stores the final node embeddings
        self.do()

    # Execute the main workflow: data loading and random walk execution
    def do(self):
        self.load_data()
        self.walk()

    # Load adjacency matrix, transaction amounts, and timestamps from .npz file
    def load_data(self):
        """Load data from the .npz file"""
        data = np.load('dataset/tedge.npz', allow_pickle=True)
        self.adj_matrix = data['adj_matrix'].item()
        self.amount_data = data['amount_data'].item()
        self.timestamp_data = data['timestamp_data'].item()
        self.node_label = data['node_label']
        self.adj_matrix.data = self.get_amount_timestamp_data()

    # Compute edge weights based on transaction amounts and timestamps
    def get_amount_timestamp_data(self):
        N = self.adj_matrix.shape[0]
        amount_timestamp_data = sp.lil_matrix((N, N), dtype=np.float64)

        nodes = np.arange(N, dtype=np.int32)
        indices = self.adj_matrix.indices
        indptr = self.adj_matrix.indptr
        amount_data = self.amount_data.data
        timestamp_data = self.timestamp_data.data

        for node in nodes:
            nbrs = indices[indptr[node]: indptr[node + 1]]
            nbrs_amount_probs = amount_data[indptr[node]: indptr[node + 1]].copy()
            nbrs_timestamp_probs = timestamp_data[indptr[node]: indptr[node + 1]].copy()
            nbrs_unnormalized_probs = combine_probs(nbrs_amount_probs, nbrs_timestamp_probs, self.alpha)

            for i, nbr in enumerate(nbrs):
                amount_timestamp_data[node, nbr] = nbrs_unnormalized_probs[i]

        return amount_timestamp_data.tocsr().data

    # Execute biased random walk and generate network embeddings using Word2Vec
    def walk(self):
        # Perform random walks on the graph
        walks = BiasedRandomWalker(walk_length=self.walk_length, walk_number=self.num_walks).walk(self.adj_matrix)

        # Train Word2Vec to generate embeddings
        word2vec_model = Word2Vec(sentences=walks, vector_size=self.dimensions, window=self.window_size,
                                  min_count=0, sg=1, hs=1, workers=self.workers, seed=self.seed)

        # Extract embedding vectors
        embeddings = word2vec_model.wv.vectors[
            np.fromiter(map(int, word2vec_model.wv.index_to_key), np.int32).argsort()]
        self.walks = walks
        self.word2vec_model = word2vec_model
        self.embeddings = embeddings

        # Print the total number of nodes and dimensions of the embeddings
        print(f"\nTotal number of nodes: {len(embeddings)}")
        print(f"Embedding dimensions: {embeddings.shape[1]}")

        # Export embeddings to a text file
        with open('embeddings.txt', 'w') as f:
            for vector in embeddings:
                f.write(f"{' '.join(map(str, vector))}\n")
        print("All embeddings have been saved to 'embeddings.txt'")

# Load labels, split data into train and test sets, and classify using LightGBM
def node_classification(args, embeddings):
    labels_dict = load_labels('dataset/label.txt')
    nodes = list([int(node) for node in labels_dict.keys()])
    nodes_labels = list(labels_dict.values())
    nodes_embeddings = embeddings[nodes]

    X_train, X_test, y_train, y_test = train_test_split(nodes_embeddings, nodes_labels, train_size=args.train_size, random_state=args.seed)

    # Train a LightGBM classifier
    model = LGBMClassifier(boosting_type='gbdt', num_leaves=20, learning_rate=0.25, n_estimators=100, max_depth=20, random_state=args.seed)
    model.fit(X_train, y_train)

    # Evaluate the model and print classification metrics
    y_pred = model.predict(X_test)
    cr = classification_report(y_pred, y_test)
    print('classification_report:\n{}'.format(cr))

# Run trans2vec and perform node classification
def run_trans2vec(args):
    t2v = trans2vec(alpha=args.alpha, dimensions=args.dimensions, num_walks=args.num_walks,
                    walk_length=args.walk_length, window_size=args.window_size, workers=args.workers, seed=args.seed)
    embeddings = t2v.embeddings

    # Print embedding statistics
    print("\nTotal number of embeddings:", len(embeddings))
    print("\nEmbedding dimensions:", embeddings.shape[1])

    # Perform node classification
    node_classification(args, embeddings)

# Command-line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default=2022, type=int, help="random seed")
    parser.add_argument("-d", "--dimensions", default=128, type=int)
    parser.add_argument("--num_walks", default=10, type=int)
    parser.add_argument("--walk_length", default=5, type=int)
    parser.add_argument("--window_size", default=5, type=int)
    parser.add_argument("--workers", default=4, type=int)
    parser.add_argument("--train_size", default=0.8, type=float)
    parser.add_argument("--alpha", default=0.3, type=float, help="balance between TBS and WBS")
    args = parser.parse_args()

    random_seed(args.seed)
    run_trans2vec(args)
