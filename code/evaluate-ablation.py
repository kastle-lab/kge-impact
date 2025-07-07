import os
from collections import defaultdict
import pandas as pd
import torch
from pykeen.triples import TriplesFactory
from pykeen.evaluation import RankBasedEvaluator


DATASET_BASE_PATH = "/home/w535axc"
RESULTS_FILE = "/home/w535axc/ablation_results.txt"
DIFF_TEST_DIR = "./diff_tests" # where the subsets are
SEED = 42

DATASET_DIRS = {
    "237": os.path.join(DATASET_BASE_PATH, "fb15k-237"),
    "238": os.path.join(DATASET_BASE_PATH, "fb15k-238"),
    "239": os.path.join(DATASET_BASE_PATH, "fb15k-239"),
}

TEST_DIFFS = {
    "T_238-237": ("238", "237"),
    "T_239-238": ("239", "238"),
    "T_239-237": ("239", "237"),
}

os.makedirs(DIFF_TEST_DIR, exist_ok=True)


def create_diff_file(test_a_dir: str, test_b_dir: str, output_path: str):
    print(f"Generating diff file: {os.path.basename(output_path)}")
    test_a_path = os.path.join(test_a_dir, "merged_triples_unique.tsv")
    test_b_path = os.path.join(test_b_dir, "merged_triples_unique.tsv")

    try:
        with open(test_a_path, "r") as fa:
            a_lines = set(fa.readlines())
    except FileNotFoundError:
        print(f"Error: {test_a_path} not found.")
        return
    
    try:
        with open(test_b_path, "r") as fb:
            b_lines = set(fb.readlines())
    except FileNotFoundError:
        print(f"Error: {test_b_path} not found.")
        return

    diff = sorted(list(a_lines - b_lines)) # creating those subsets
    with open(output_path, "w") as fout:
        fout.writelines(diff)
    print(f"Generated {len(diff)} unique triples in {output_path}")


def load_model_torch(model_dir: str):
    model_path = os.path.join(model_dir, "trained_model.pkl") # Loading trained models-> pickle files
    print(f"Loading model from: {model_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    model = torch.load(model_path, map_location="cpu", weights_only=False)
    model.eval()
    return model


def evaluate_model_on_subset(model_dir: str, subset_path: str) -> dict:
    print(f"Evaluating model in '{model_dir}' on subset '{os.path.basename(subset_path)}'...")

    if not os.path.exists(subset_path):
        print(f"Error: Subset file {subset_path} not found.")
        return {}

    if os.stat(subset_path).st_size == 0:
        print(f"Subset file {subset_path} is empty.")
        return {}

    try:
        model = load_model_torch(model_dir)
    except Exception as e:
        print(f"Error loading model from {model_dir}: {e}")
        return {}

    try:
        subset_factory = TriplesFactory.from_path(subset_path)
    except Exception as e:
        print(f"Error loading triples from {subset_path}: {e}")
        return {}

    evaluator = RankBasedEvaluator() # our metrics

    metrics = evaluator.evaluate(
        model=model, # our trained models
        mapped_triples=subset_factory.mapped_triples,
        additional_filter_triples=subset_factory.mapped_triples, # in order to predict you need to evaluate on unseen data
    )

    return metrics.to_dict()


def main():
    # Step 1: Generate difference subset files
    print("Generating difference subset files...")
    for diff_name, (a_key, b_key) in TEST_DIFFS.items():
        output_path = os.path.join(DIFF_TEST_DIR, f"{diff_name}.txt")
        create_diff_file(DATASET_DIRS[a_key], DATASET_DIRS[b_key], output_path)

    # Step 2: Evaluate models on subsets only
    results = defaultdict(dict)

    model_238_dir = os.path.normpath(os.path.join(DATASET_DIRS["238"], "TransD"))
    subset_238_237_path = os.path.join(DIFF_TEST_DIR, "T_238-237.txt")
    if os.path.exists(model_238_dir):
        results["M_238"]["T_238-237"] = evaluate_model_on_subset(model_238_dir, subset_238_237_path)
    else:
        print(f"Warning: Model directory {model_238_dir} not found.")

    model_239_dir = os.path.normpath(os.path.join(DATASET_DIRS["239"], "TransD"))
    if os.path.exists(model_239_dir):
        for subset_name in ["T_238-237", "T_239-238", "T_239-237"]:
            subset_path = os.path.join(DIFF_TEST_DIR, f"{subset_name}.txt")
            results["M_239"][subset_name] = evaluate_model_on_subset(model_239_dir, subset_path)
    else:
        print(f"Warning: Model directory {model_239_dir} not found.")

    # Step 3: Writing results to a text file
    print(f"\nWriting evaluation results to {RESULTS_FILE}...")
    with open(RESULTS_FILE, "w") as f:
        # Collect all metric keys found in results for header
        all_metric_keys = set()
        for model_data in results.values():
            for subset_metrics in model_data.values():
                all_metric_keys.update(subset_metrics.keys())

        sorted_metrics = sorted(list(all_metric_keys))
        header = "Model\tSubset\t" + "\t".join(sorted_metrics) + "\n"
        f.write(header)

        for model_key, subsets in results.items():
            for subset_name, metrics in subsets.items():
                row = [model_key, subset_name]
                for metric in sorted_metrics:
                    row.append(str(metrics.get(metric, "-")))
                f.write("\t".join(row) + "\n")

    print("Done.")


if __name__ == "__main__":
    main()
