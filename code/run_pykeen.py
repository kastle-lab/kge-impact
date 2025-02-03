import pykeen.pipeline as pipeline
import argparse
import os
import pandas as pd  # To save the metrics as CSV

def train_and_evaluate(dataset_path, model, epochs, output_path):
    result = pipeline.pipeline(
        training=f"{dataset_path}/train.tsv",
        testing=f"{dataset_path}/test.tsv",
        validation=f"{dataset_path}/valid.tsv",
        model=model,
        training_kwargs=dict(num_epochs=epochs),
    )

    # Save results to output directory that will be specified in the bash file
    result.save_to_directory(output_path)
    print(f"Results saved to {output_path}")

    # Save eval metrics in csv ( for link prediction )
    if result.evaluation_results:
        eval_metrics = result.evaluation_results.to_dict()
        metrics_df = pd.DataFrame(eval_metrics)  
        metrics_file = os.path.join(output_path, "metrics.csv")
        metrics_df.to_csv(metrics_file, index=False)  
        print(f"Evaluation results saved in {metrics_file}")
    else:
        print("No evaluation results available.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and evaluate PyKEEN models")
    parser.add_argument("--dataset", required=True, help="Path to dataset directory")
    parser.add_argument("--model", default="TransE", help="PyKEEN model to use")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--output", required=True, help="Directory to save results")

    args = parser.parse_args()
    train_and_evaluate(args.dataset, args.model, args.epochs, args.output)
