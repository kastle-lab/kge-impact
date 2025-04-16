#!/bin/bash

# Set up log file
LOGFILE="drift_analysis_log.txt"
echo "=== Drift Analysis Log ===" > "$LOGFILE"

# Ensure output folders exist
mkdir -p gen_data img

# Step 1: Generate drift data with 100 and 5 epochs
#echo "Generating drift data (100 epochs)..." | tee -a "$LOGFILE"
#python3 save_drift_data.py --epochs 100 --filename ./drift_outputs/drift_data_100epochs.json >> "$LOGFILE" 2>&1

echo "Generating drift data (5 epochs)..." | tee -a "$LOGFILE"
python3 save_drift_data.py --epochs 5 --filename ./drift_outputs/drift_data_5epochs.json >> "$LOGFILE" 2>&1

# Step 2: Define datasets and SPO elements "drift_outputs/drift_data_100epochs.json"
datasets=("gen_data/drift_data_5epochs.json")
spo_elements=("head" "relation" "tail")

# Step 3: Loop through datasets and SPO terms
for dataset in "${datasets[@]}"; do
    for spo in "${spo_elements[@]}"; do
        base_name=$(basename "$dataset" .json)
        output_file="img/${base_name}_${spo}.png"
        
        echo "Generating drift histogram for $spo from $dataset..." | tee -a "$LOGFILE"
        python3 calc_drift.py --filepath "$dataset" --spo "$spo" --filename "$output_file" >> "$LOGFILE" 2>&1
    done
done

echo "✅ All drift analysis completed." | tee -a "$LOGFILE"
