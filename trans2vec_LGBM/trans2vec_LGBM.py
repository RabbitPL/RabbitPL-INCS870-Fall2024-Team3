import argparse                    # Used for parsing command-line arguments.
import scipy.sparse as sp          # Used for handling sparse matrices, especially adjacency matrices in the Ethereum network.
from gensim.models import Word2Vec  # Used for implementing the Word2Vec model to generate node embeddings.
from lightgbm import LGBMClassifier  # Used for training and predicting with the LightGBM classifier.
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split  # Used for splitting the dataset into training and testing sets.
from walker import BiasedRandomWalker   # Custom library for biased random walk algorithms and related utilities.
import numpy as np
import random
from utils import *

# Define the random_seed function to ensure reproducibility
def random_seed(seed_value):
    random.seed(seed_value)  # Set the random seed for Python's built-in random module
    np.random.seed(seed_value)  # Set the random seed for the numpy module

# trans2vec class: Implements the network embedding algorithm, with steps including loading data, performing random walks, and generating embeddings.
class trans2vec(object):

    def __init__(self, alpha=0.5, dimensions=64, num_walks=20, walk_length=5, window_size=10, workers=1, seed=2022):
        self.alpha = alpha  # A parameter to balance the weight between transaction amount and timestamps.
        self.dimensions = dimensions  # The dimensionality of the embeddings.
        self.window_size = window_size  # The window size for the Word2Vec model, defining the context range.
        self.workers = workers  # Number of parallel threads for training Word2Vec.
        self.seed = seed  # Random seed to ensure reproducibility.
        self.walk_length = walk_length  # The length of each random walk.
        self.num_walks = num_walks  # The number of random walks per node.

        self.walks = None    # Stores the paths generated by random walks.
        self.word2vec_model = None  # Stores the Word2Vec model.
        self.embeddings = None  # Stores the final node embeddings.
        self.do()

    # Execute the workflow: Load data and perform random walks.
    def do(self):
        self.load_data()
        self.walk()


    # Load adjacency matrix, transaction amounts, and timestamps from file and preprocess the data.
    # The input is a .npz file containing sparse matrices.
    def load_data(self):
        """load data from the npz processed by Lin
            refer to <https://arxiv.org/abs/1905.08038>
        """
        data = np.load('dataset/tedge.npz', allow_pickle=True)
        self.adj_matrix = data['adj_matrix'].item()
        self.amount_data = data['amount_data'].item()
        self.timestamp_data = data['timestamp_data'].item()
        self.node_label = data['node_label']
        self.adj_matrix.data = self.get_amount_timestamp_data()

    # Compute the edge weights (based on transaction amount and timestamp probabilities).
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

    # Perform biased random walks using BiasedRandomWalker and convert the paths into low-dimensional embeddings using Word2Vec.
    def walk(self):
        walks = BiasedRandomWalker(walk_length=self.walk_length, walk_number=self.num_walks).walk(self.adj_matrix)
        word2vec_model = Word2Vec(sentences=walks, vector_size=self.dimensions, window=self.window_size,
                                  min_count=0, sg=1, hs=1, workers=self.workers, seed=self.seed)

        embeddings = word2vec_model.wv.vectors[np.fromiter(map(int, word2vec_model.wv.index_to_key), np.int32).argsort()]
        self.walks = walks
        self.word2vec_model = word2vec_model
        self.embeddings = embeddings

# Load the label file (label.txt), split the embeddings and labels into training and testing sets,
# and classify the nodes using the LightGBM classifier. Finally, output a detailed classification report.
def node_classification(args, embeddings):
    labels_dict = load_labels('dataset/label.txt')
    nodes = list([int(node) for node in labels_dict.keys()])
    nodes_labels = list(labels_dict.values())
    nodes_embeddings = embeddings[nodes]

    X_train, X_test, y_train, y_test = train_test_split(nodes_embeddings, nodes_labels, train_size=args.train_size, random_state=args.seed)

    # Train a LightGBM classifier
    model = LGBMClassifier(boosting_type='gbdt', num_leaves=20, learning_rate=0.25, n_estimators=100, max_depth=20, random_state=args.seed)

    # Train the LightGBM model
    model.fit(X_train, y_train)

    # Predict the labels of the testing set
    y_pred = model.predict(X_test)

    # Calculate performance metrics such as precision, recall, and F1-score
    cr = classification_report(y_pred, y_test)
    print('classification_report:\n{}'.format(cr))

# Parse command-line arguments, execute the trans2vec workflow to generate embeddings,
# and perform node classification on the graph.
def run_trans2vec(args):
    t2v = trans2vec(alpha=args.alpha, dimensions=args.dimensions, num_walks=args.num_walks,
                    walk_length=args.walk_length, window_size=args.window_size, workers=args.workers, seed=args.seed)
    embeddings = t2v.embeddings
    node_classification(args, embeddings)

# Command-line argument section
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
