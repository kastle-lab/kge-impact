#!/bin/bash

# Configuration
DATASET_PATH="/path/to/dataset"
OUTPUT_DIR="/path/to/results"
MODEL="TransE"
EPOCHS=100

# Run PyKEEN in container
singularity exec pykeen.sif python3 run_pykeen.py \
    --dataset "$DATASET_PATH" \
    --model "$MODEL" \
    --epochs "$EPOCHS" \
    --output "$OUTPUT_DIR"
