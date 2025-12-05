# ARTIFACT.md — MSR 2026 Challenge Track (Anonymous Submission)

## Title  
**Replication Package for MSR 2026 Challenge Track Submission (Anonymous)**

This artifact contains all code, scripts, and notebooks required to fully reproduce the results presented in our MSR 2026 Challenge Track paper. The package includes automated pipelines, engineered features, statistical tests, figures, and reproducible tables for all three research questions (RQ1–RQ3).

---

# 1. Artifact Overview

This replication package provides:

- ✔ Fully automated end-to-end pipelines for RQ1–RQ3  
- ✔ Clean and analysis-ready CSV tables  
- ✔ All figures used in the paper (generated programmatically)  
- ✔ Statistical analysis (Mann–Whitney U tests)  
- ✔ Interactive Jupyter notebooks  
- ✔ Conda and pip environments for full reproducibility  
- ✔ Deterministic workflows with no manual steps  

The only external dependency is the **AIDev dataset**, which is loaded automatically via HuggingFace using the `hf://` protocol.

---

# 2. System Requirements

- **OS:** Linux, macOS, or Windows  
- **Python:** 3.10  
- **RAM:** ≥ 8 GB (recommended: 16 GB)  
- **Internet Access:** Required to load dataset parquet files from HuggingFace  
- **Disk Space:** < 2 GB (only figures and tables are saved locally)

---

# 3. Installation Instructions

## Option A — Conda (recommended)

```bash
conda env create -f environment.yml
conda activate msr2026
```
## Option B — Pip Installation

If you prefer not to use conda, you can install dependencies directly:

```bash
pip install -r requirements.txt
```
The environment includes core scientific libraries required for all analyses, such as:

- **pandas** — data loading and cleaning  
- **numpy** — numerical computation  
- **pyarrow** — fast parquet access (required for HuggingFace `hf://` loading)  
- **matplotlib** — figure generation  
- **seaborn** — statistical visualization  
- **scipy** — significance testing (e.g., Mann–Whitney U)  
- **tqdm** — progress bars for long-running tasks  
- **statsmodels** — statistical utilities used during analysis  

These guarantee complete reproducibility across all Research Questions (RQ1–RQ3).

---

# 4. Dataset Access

All analyses rely on the **AIDev Dataset (2025 snapshot)**:

🔗 HuggingFace: https://huggingface.co/datasets/hao-li/AIDev

The dataset is accessed programmatically using the HuggingFace filesystem scheme: `hf://hao-li/AIDev/`


No manual download is required—scripts load parquet files directly over the network.

⚠ **Dataset files are NOT bundled in this artifact**, following MSR’s double-anonymity rules.

---

# 5. Reproducing All Results (Automated Pipeline)

To execute the full workflow for all research questions, run:

```bash
python src/main_run_all.py
```
This generates:

- All figures used across RQ1–RQ3  
- All processed and cleaned CSV tables  
- All statistical test outputs (Mann–Whitney U for RQ3)  
- Full reproducibility logs printed in the console  

Outputs are written into the structured directory:
```text
output/
├── figures/
│   ├── RQ1/
│   │   ├── rq1_test_inclusion.png
│   │   ├── rq1_avg_test_files.png
│   │   ├── rq1_three_panel.pdf
│   │   └── ...
│   ├── RQ2/
│   │   ├── rq2_comment_distribution.png
│   │   ├── rq2_resolution_heatmap.pdf
│   │   └── ...
│   └── RQ3/
│       ├── rq3_features.png
│       └── ...
```

Every figure and table corresponds directly to the results described in the paper.

---

# 6. Running Individual Research Questions

If you prefer executing one research question at a time, you may run:

### **RQ1 — Testing Behavior**
```bash
python src/msr2026/rq1/run_rq1.py
```

### **RQ2 — Review Dynamics and Resolution**
```bash
python src/msr2026/rq1/run_rq2.py
```

### **RQ3 — Early Acceptance Signals**
```bash
python src/msr2026/rq1/run_rq3.py
```
---

# 7. Jupyter Notebooks (Interactive Replication)

We provide four notebooks:
- 00_setup_environment.ipynb
- 01_rq1_testing_behavior.ipynb
- 02_rq2_review_dynamics.ipynb
- 03_rq3_early_acceptance.ipynb
- 04_full_pipeline.ipynb

### Recommended evaluation order:

1. Run `00_setup_environment` (sanity checks)
2. Explore RQ1–RQ3 step-by-step
3. Use `04_full_pipeline` for one-click execution
---

# 8. Reproducibility Claims

| Criterion | Status |
|----------|--------|
| Workflows fully automated | ✔ Yes |
| All outputs generated programmatically | ✔ Yes |
| No manual data editing | ✔ Yes |
| Open-source dependencies only | ✔ Yes |
| Deterministic code paths | ✔ Yes |

---

# 9. License

MIT License (anonymous).

---
# 10. Expected Runtime

Approximate end-to-end running time on a laptop (16GB RAM):

| Component | Runtime      |
|----------|--------------|
| RQ1 pipeline | 1–2 minutes  |
| RQ2 pipeline | 1–2 minutes  |
| RQ3 pipeline | 1–2 minutes  |
| Full pipeline (`main_run_all.py`) | ~3–6 minutes |
---
# 11. Repository Structure

```text
MSR-2026/
├── notebooks/                     # Jupyter notebooks (interactive reproduction)
│   ├── 00_setup_environment.ipynb
│   ├── 01_rq1_testing_behavior.ipynb
│   ├── 02_rq2_review_dynamics.ipynb
│   ├── 03_rq3_early_acceptance.ipynb
│   └── 04_full_pipeline.ipynb
│
├── output/
│   ├── figures/                   # All generated figures (RQ1–RQ3)
│   └── tables/                    # All generated CSV tables (RQ1–RQ3)
│
├── src/
│   ├── msr2026/                   # Main Python package
│   │   ├── rq1/
│   │   │   ├── __init__.py
│   │   │   └── run_rq1.py
│   │   │
│   │   ├── rq2/
│   │   │   ├── __init__.py
│   │   │   └── run_rq2.py
│   │   │
│   │   ├── rq3/
│   │   │   ├── __init__.py
│   │   │   └── run_rq3.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── plotting.py
│   │
│   └── main_run_all.py            # One-click full pipeline
│
├── CITATION.cff                   # Citation metadata
├── LICENSE.txt                    # MIT license (anonymous)
├── README.md                      # Documentation (artifact instructions)
├── environment.yml                # Conda environment definition
├── requirements.txt               # pip dependencies
├── run.sh                         # Shell script for Linux/macOS
└── run.bat                        # Batch script for Windows

```