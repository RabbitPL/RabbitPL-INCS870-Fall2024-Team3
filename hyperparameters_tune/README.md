
# LightGBM Learning Rate Tuning for Phishing Detection

This program optimizes the **learning rate** parameter for a LightGBM classifier used in phishing detection within the Ethereum transaction network. It uses the `trans2vec` algorithm to generate node embeddings, followed by classification and visualization of the effects of different learning rate values on model accuracy.

---

## Features
1. **Graph-based Network Embedding**:
   - Implements the `trans2vec` algorithm.
   - Performs biased random walks on Ethereum transaction graphs to generate node embeddings.
   - Incorporates transaction amounts and timestamps into embeddings.

2. **Hyperparameter Tuning**:
   - Tests the impact of various **learning rate** values on classification accuracy.
   - Automates parameter optimization with LightGBM.

3. **Visualization**:
   - Plots the relationship between the learning rate and model accuracy.
   - Provides insights into the optimal learning rate for phishing detection.

---

## Requirements

### Dependencies:
- Python Libraries:
  - `argparse`
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `gensim`
  - `lightgbm`
  - `sklearn`
  - `walker` (custom library for biased random walks)
  - `utils` (custom utility functions for graph processing)

### Installation:
To install the required Python libraries, run:
```bash
pip install numpy scipy matplotlib gensim lightgbm scikit-learn
```

---

## How to Use

1. **Prepare Dataset**:
   - Ensure the `tedge.npz` dataset and `label.txt` file are present in the `dataset/` directory.

2. **Run the Program**:
   - Execute the script with the following command:
   ```bash
   python script_name.py
   ```
   - Replace `script_name.py` with the name of the file containing this program.

3. **Output**:
   - The script will:
     1. Generate node embeddings using the `trans2vec` algorithm.
     2. Evaluate the LightGBM classifier for a range of learning rate values.
     3. Plot the accuracy for different learning rates.

---

## Parameters

### Command-Line Arguments:
- `--seed`: Random seed for reproducibility (default: `2022`).
- `--dimensions`: Embedding dimensions for `trans2vec` (default: `64`).
- `--num_walks`: Number of walks per node for random walks (default: `5`).
- `--walk_length`: Length of each random walk (default: `2`).
- `--window_size`: Context window size for Word2Vec (default: `2`).
- `--workers`: Number of worker threads for Word2Vec (default: `1`).
- `--train_size`: Training set size as a fraction of the total data (default: `0.8`).
- `--alpha`: Balances transaction amount and timestamp importance (default: `0.5`).

### Tuned Parameter:
- `learning_rate`: Range of values from `0.15` to `0.30` (increment: `0.01`).

---

## Example Output

- The program generates a plot showing the effect of learning rate on model accuracy.  
- Example visualization:

  ![Learning Rate vs Accuracy](example_plot.png)

---

## Notes

- **Performance**:
  - A balanced learning rate helps prevent overfitting while maintaining classification accuracy.
  - Hyperparameter tuning is essential for maximizing LightGBM's performance on imbalanced datasets.

- **Visualization**:
  - The accuracy plot guides the selection of an optimal learning rate for phishing detection.

---

## Future Work
- Extend this framework to tune additional hyperparameters such as `num_leaves` or `max_depth`.
- Integrate other graph-based machine learning techniques to improve model robustness.

