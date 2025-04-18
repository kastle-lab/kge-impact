import argparse
import os
import matplotlib.pyplot as plt
import ijson
from scipy.spatial.distance import euclidean


def calc_top10_drift(file_path, output_dir="./output"):
    os.makedirs(output_dir, exist_ok=True)

    for spo_term in ["head", "tail"]:
        print(f"Processing: {spo_term}s")

        drift_1 = []  # 237 vs 238
        drift_2 = []  # 237 vs 239
        drift_3 = []  # 238 vs 239

        with open(file_path, 'r', encoding='utf-8') as f:
            triples = ijson.kvitems(f, '')
            for triple_key, triple_data in triples:
                try:
                    h237 = triple_data['dataset_237'][spo_term]
                    h238 = triple_data['dataset_238'][spo_term]
                    h239 = triple_data['dataset_239'][spo_term]

                    parts = triple_key.split('\t')
                    if spo_term == 'head':
                        label = parts[0]
                    elif spo_term == 'tail':
                        label = parts[2]
                    else:
                        continue  # just in case

                    drift_1.append((label, euclidean(h237, h238)))
                    drift_2.append((label, euclidean(h237, h239)))
                    drift_3.append((label, euclidean(h238, h239)))
                except (KeyError, IndexError) as e:
                    print(f"Skipping {triple_key} due to missing key or bad format: {e}")

        for drift_set, name in [(drift_1, "237_vs_238"), (drift_2, "237_vs_239"), (drift_3, "238_vs_239")]:
            if not drift_set:
                continue

            drift_set.sort(key=lambda x: x[1])  # sort by drift value ascending

            # Carefully select lowest 10
            seen = set()
            lowest_10 = []
            for label, value in drift_set:
                if label not in seen:
                    lowest_10.append((label, value))
                    seen.add(label)
                if len(lowest_10) == 10:
                    break

            highest_10 = drift_set[-10:]  # highest 10 normally

            # --- Plotting Functions ---

            def plot_bar(data, title_suffix, filename_suffix):
                labels = [label for label, _ in data]
                values = [value for _, value in data]

                plt.figure(figsize=(12, 6))
                plt.bar(labels, values)
                plt.xticks(rotation=45, ha='right', fontsize=8)
                plt.ylabel('Drift Amount (Euclidean Distance)')
                plt.title(f"Top 10 {title_suffix} ({spo_term.capitalize()}s)")
                plt.tight_layout()

                save_path = os.path.join(output_dir, f"{spo_term}_{filename_suffix}.png")
                plt.savefig(save_path)
                plt.close()

                print(f"Saved plot: {save_path}")

            def plot_bar(data, title_suffix, filename_suffix):
                labels = [label for label, _ in data]
                values = [value for _, value in data]

                plt.figure(figsize=(12, 6))
                bars = plt.bar(labels, values)

                plt.xticks(rotation=45, ha='right', fontsize=8)
                plt.ylabel('Drift Amount (Euclidean Distance)')
                plt.title(f"Top 10 {title_suffix} ({spo_term.capitalize()}s)")
                plt.tight_layout()

                # Add drift value above each bar
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width() / 2, height, f"{value:.4f}", 
                            ha='center', va='bottom', fontsize=7, rotation=90)

                save_path = os.path.join(output_dir, f"{spo_term}_{filename_suffix}.png")
                plt.savefig(save_path)
                plt.close()

                print(f"Saved plot: {save_path}")


            # --- Actually plot now ---
            plot_bar(lowest_10, f"Lowest Drift {name}", f"{name}_lowest_{spo_term}")
            plot_bar(highest_10, f"Highest Drift {name}", f"{name}_highest_{spo_term}")
            plot_line(drift_set, name)  # plot full distribution too


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate and plot top 10 drifts for heads and tails.")
    parser.add_argument("--filepath", default="./drift_data.json", help="Path to the drift data JSON file.")
    parser.add_argument("--output", default="./output", help="Directory to save output plots.")
    args = parser.parse_args()

    calc_top10_drift(file_path=args.filepath, output_dir=args.output)
