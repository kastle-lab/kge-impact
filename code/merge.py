import os

# Define the path to the datasets and datasets to merge
base_path = "/home/w535axc/experiment/code"
datasets = ["output-4b","output-5b","output-6b"]

# Loop through each dataset and merge train, valid, and test files
for dataset in datasets:
    dataset_path = os.path.join(base_path, dataset)
    merged_file_path = os.path.join(dataset_path, "merged.txt")
    
    with open(merged_file_path, "w") as outfile:
        for split in ["train.tsv", "valid.tsv", "test.tsv"]:
            file_path = os.path.join(dataset_path, split)
            if os.path.exists(file_path):
                with open(file_path, "r") as infile:
                    outfile.write(infile.read())
    print(f"Merged files for {dataset} into {merged_file_path}")
