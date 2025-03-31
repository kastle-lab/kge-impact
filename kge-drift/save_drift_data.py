from generate_drift_data import generate_drift_data
import pandas as pd
import json

def save_drift_data():

    format_choice = input("Save drift data as (1) CSV or (2) JSON? Enter 1 or 2: ").strip()

    if format_choice == "1":
        filename = input("Enter CSV filename (default: drift_data.csv): ").strip() or "drift_data.csv"
    elif format_choice == "2":
        filename = input("Enter JSON filename (default: drift_data.json): ").strip() or "drift_data.json"
    else:
        print("Invalid input. Please run the script again and enter 1 or 2.")
        return

    print("Generating drift data...")
    drift_data = generate_drift_data()
    print("Drift data obtained.")

    if format_choice == "1":
        print("Preparing data for CSV format...")

        rows = []
        for triple, dataset_embeddings in drift_data.items():
            for dataset, components in dataset_embeddings.items():
                row = {
                    "triple": triple,
                    "dataset": dataset
                }
                for component_name, embedding in components.items():
                    for i, val in enumerate(embedding):
                        row[f"{component_name}_{i}"] = val
                rows.append(row)

        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        print(f"Drift data saved as CSV to {filename}")

    else:  # JSON
        print("Preparing data for JSON format...")

        serializable_data = {
            triple: {
                dataset: {key: value.tolist() for key, value in embeddings.items()}
                for dataset, embeddings in dataset_data.items()
            }
            for triple, dataset_data in drift_data.items()
        }

        with open(filename, "w") as f:
            json.dump(serializable_data, f, indent=4)
        print(f"Drift data saved as JSON to {filename}")

# Run the function
save_drift_data()
