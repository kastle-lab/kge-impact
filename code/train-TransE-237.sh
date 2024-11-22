#!/bin/bash
#SBATCH --output=/home/w535axc/experiment/code/output/TransE_training-237%A_%a.out  
#SBATCH --mem-per-cpu=2GB
#SBATCH --cpus-per-task=4
#SBATCH --partition=p100
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00


# Set environment variable for memory management
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128

# Define the common variables
DATA_PATH="/home/w535axc/experiment/code"
DATASET_BASE=“fb15k-237”
DATA_FILES="train.txt valid.txt test.txt"
FORMAT="raw_udd_hrt"

# TransE specific parameters
MODEL_NAME="TransE_l2"
BATCH_SIZE=10000
NEG_SAMPLE_SIZE=10000
HIDDEN_DIM=400
GAMMA=19.9
LR=0.25
MAX_STEP=500
LOG_INTERVAL=25
REGULARIZATION_COEF=1.00E-09
ADVERSARIAL_TEMPERATURE=1
REGULARIZATION_NORM=3



# Define the dataset and data directory
DATASET="${DATASET_BASE}"
DATA_DIR="${DATA_PATH}/${DATASET}"

# Train TransE model
singularity exec --nv dglke.sif dglke_train \
  --model_name ${MODEL_NAME} \
  --dataset ${DATASET} \
  --data_path ${DATA_DIR} \
  --data_files ${DATA_FILES} \
  --format ${FORMAT} \
  --batch_size ${BATCH_SIZE} \
  --neg_sample_size ${NEG_SAMPLE_SIZE} \
  --hidden_dim ${HIDDEN_DIM} \
  --gamma ${GAMMA} \
  --lr ${LR} \
  --max_step ${MAX_STEP} \
  --log_interval ${LOG_INTERVAL} \
  --regularization_coef ${REGULARIZATION_COEF} \
  --adversarial_temperature ${ADVERSARIAL_TEMPERATURE} \
  --regularization_norm ${REGULARIZATION_NORM}


