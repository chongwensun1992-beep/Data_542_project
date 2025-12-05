#!/bin/bash
set -e

echo "========================================================"
echo " MSR 2026 Artifact — One-Click Reproduction Script"
echo "========================================================"
echo

# -------------------------------
# 1. Activate Conda Environment
# -------------------------------

ENV_NAME="msr2026"

echo "[1/4] Checking Conda environment..."

if conda info --envs | grep -q "${ENV_NAME}"; then
    echo "✔ Environment '${ENV_NAME}' already exists."
else
    echo "Environment '${ENV_NAME}' not found."
    echo "Creating it from environment.yml..."
    conda env create -f environment.yml
fi

echo "Activating environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ${ENV_NAME}

echo "✔ Conda environment ready."
echo

# -------------------------------
# 2. Ensure PYTHONPATH contains src/
# -------------------------------
echo "[2/4] Setting PYTHONPATH..."

export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
echo "✔ PYTHONPATH set to include src/"
echo

# -------------------------------
# 3. Run the full pipeline
# -------------------------------

echo "[3/4] Running all RQs..."
python main_run_all.py
echo "✔ All RQs executed successfully."
echo

# -------------------------------
# 4. Completion message
# -------------------------------

echo "[4/4] All results generated!"
echo "Figures saved to:  output/figures/"
echo "Tables saved to:   output/tables/"
echo
echo "========================================================"
echo " Artifact Reproduction Completed Successfully!"
echo "========================================================"
