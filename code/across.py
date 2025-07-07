from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
import pandas as pd
import os

def read_triples(path):
    # since we have both txt and tsv versions
    sep = '\t' if path.endswith('.tsv') else '\t'
    return TriplesFactory.from_path(path, sep=sep)

if __name__ == "__main__":
    train_dir = "fb15k-237" # to take the train set from this folder
    eval_dir = "fb15k-239"
    output_dir = "fb15k-237"

    os.makedirs(output_dir, exist_ok=True)

    models = ['TransD']

    train_file = os.path.join(train_dir, 'train.txt') 
    test_file = os.path.join(eval_dir, 'test.txt')     
    valid_file = os.path.join(eval_dir, 'valid.txt')   

 
    training = read_triples(train_file)
    testing = read_triples(test_file)
    validation = read_triples(valid_file)

    for model in models:
        model_output_dir = os.path.join(output_dir, model)
        os.makedirs(model_output_dir, exist_ok=True)

        result = pipeline(
            training=training,
            testing=testing,
            validation=validation,
            model=model,
            model_kwargs=dict(embedding_dim=300),
            epochs=100,
        )

        if result.metric_results:
            metrics_df = pd.DataFrame(result.metric_results.to_dict())
            metrics_df.to_csv(os.path.join(model_output_dir, "metrics.csv"), index=False)
            print(f"Evaluation results for {model} saved.")
        else:
            print(f"No evaluation results for {model}.")

        result.save_to_directory(model_output_dir)
