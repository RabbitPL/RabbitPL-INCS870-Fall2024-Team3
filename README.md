
# Phishing Scam Detection on Ethereum Using Graph-based Machine Learning Models

This repository includes multiple projects focused on phishing scam detection on the Ethereum blockchain, as well as parameter tuning and optimization for related algorithms.

## Directory Overview

1. **data_Collection**
   - **Purpose**: This project is implemented in Node.js to collect data from Ethereum blockchain. It includes scripts for web scraping and data gathering.
   - **Details**: 
     - `package.json` and `package-lock.json` contain information about the project's dependencies.
     - Configured scripts allow direct execution of commands, e.g., `npm run account`, from the root directory.
   - **Note**: Refer to the `README.md` within the `data_Collection` directory for detailed instructions on running this project.

2. **trans2vec_Param**
   - **Purpose**: This project focuses on **Parameter Optimization and Performance Comparison** for the Trans2Vec model. It is an enhancement based on the code from the paper [Who Are the Phishers? Phishing Scam Detection on Ethereum via Network Embedding](https://ieeexplore.ieee.org/abstract/document/9184813)
   - **Implementation**: The project is written in Python and includes scripts for parameter tuning and comparison between original and optimized settings.
   - **Note**: Refer to the `README.md` within the `trans2vec_Param` directory for specific details on running the code.

## How to Use

- Each project contains its own `README.md` file with instructions on installation, configuration, and execution.
- Make sure to install all necessary dependencies before running the respective projects.

For further questions or contributions, please reach out to the repository maintainers.
