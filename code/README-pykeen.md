# PyKEEN Model Training and Evaluation

This repository contains a Python script that trains and evaluates Knowledge Graph Embedding (KGE) models using the **PyKEEN** library. The script supports training and evaluating on a given dataset.

## Table of Contents
- [Overview](#overview)
- [What the Code Does](#what-the-code-does)
- [Parameters](#parameters)
- [Machine Learning Task](#machine-learning-task)
- [Results](#results)
- [How to Change Parameters and ML Tasks](#how-to-change-parameters-and-ml-tasks)


## Overview

This Python script uses the **PyKEEN** library to train and evaluate KGE models for **link prediction** tasks ( at this moment ). The models are trained on a dataset with **training**, **testing**, and **validation** splits, and the evaluation results are saved as **CSV** files.

The script can be customized to use different models and adjust hyperparameters like the number of epochs.

## What the Code Does

The Python script performs the following tasks:
1. **Loading the Dataset**: It loads the dataset from the specified directory that is adjusted in the batch file, which should include the following files:
    - `train.tsv`: Training data in tab-separated format.
    - `test.tsv`: Testing data in tab-separated format.
    - `valid.tsv`: Validation data in tab-separated format.
   
2. **Model Selection**: It allows the user to choose which KGE model to use (e.g., **TransE**, **DistMult**, etc.). If no model is specified, the script defaults to **TransE**.

3. **Training**: The model is trained for the specified number of epochs (default is 100).

4. **Evaluation**: After training, the model is evaluated on the test set, and evaluation metrics (e.g., Mean Rank, Hits@1, Hits@3, Hits@10) are computed.

5. **Saving Results**: The trained model and evaluation results are saved to the specified output directory. 

## Parameters

The script accepts the following command-line arguments:

- `--dataset` (required): The path to the dataset directory. This directory should contain the following files:
  - `train.tsv`
  - `test.tsv`
  - `valid.tsv`

- `--model` (optional): The KGE model to use for training. Available options:
  - **TransE** (default)
  - **DistMult**
  - **ComplEx**
  - **Other supported models in PyKEEN**.

  

## Machine Learning Task

The current implementation of this script is set up for **link prediction** as it is Pykeen's default task.

## How to Change Parameters and ML Tasks

### Adjusting for Different ML Tasks
If you wish to modify it for other types of machine learning tasks (e.g., **clustering** or **link completion**), you would need to:

1. **Change the Input Data Format**: For example, for entity classification or triple classification tasks, you will need to modify the dataset to include labels for entities or triples.
2. **Change the Model Type**: Depending on the task, you may want to choose a different KGE model. PyKEEN supports a variety of models for different types of tasks.

# Bash Script for Running PyKEEN in Singularity Container

The bash included in this repo allows the run of the **PyKEEN** model training and evaluation process within a **Singularity** container attached in the repository under ./containers.
## Overview
It passes the necessary parameters (dataset, model, epochs, output directory) to the Python script responsible for training the model. 
It allows the user to specify the following parameters:
   - Path to the dataset directory containing the training, validation, and test sets.
   - Path where the evaluation results and trained models will be saved.
   - Model type (default is **TransE**).
   - Number of training epochs (default is **100**).

The script runs the **PyKEEN** model training and evaluation inside the Singularity container using the `singularity exec` command. It invokes the Python script that trains and evaluates the model.

The following configuration parameters can be adjusted in the script:

- `DATASET_PATH`: The path to the directory containing the dataset files (`train.tsv`, `valid.tsv`, `test.tsv`).
- `OUTPUT_DIR`: The directory where the trained model and evaluation results will be saved.
- `MODEL`: The KGE model to use for training (default is **TransE**). You can change this to another supported model like **DistMult** or **ComplEx**.
- `EPOCHS`: The number of training epochs. The default is **100** but you can adjust it as needed.



