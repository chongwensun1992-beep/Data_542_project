# Behavioral Analysis of AI Coding Agents Using the AIDev Dataset  
**DATA 542 — Data Wrangling | Final Project**  
University of British Columbia, Okanagan  
**Authors:** Chongwen Sun, Inaara Rajwani  

---

## 📘 Overview

This repository contains the full code, analysis pipeline, reproducibility files, and final paper for our DATA 542 project:

**“Behavioral Analysis of AI Coding Agents in Software Engineering:  
An Empirical Study Using the AIDev Dataset.”**

The project analyzes thousands of AI-generated pull requests (PRs) in open-source repositories, focusing on:

- **RQ1:** Do AI agents write tests, and how often?  
- **RQ2:** What review comments do they receive, and which are hardest to resolve?  
- **RQ3:** Can early PR features (churn, files changed, description length) predict acceptance?

All analyses follow the goals of the course — **data cleaning, feature engineering, structured processing**, and **reproducibility**, without machine-learning modeling.

---

## 📂 Repository Structure

```
Data_542_project/
│
├── notebooks/                     # Main analysis notebooks for each RQ
│   ├── RQ1_TestingBehavior_AI_Agents.ipynb
│   ├── RQ2_Review_Dynamics.ipynb
│   └── RQ3_Acceptance_Analysis.ipynb
│
├── paper/                         # Paper drafts and templates
│   ├── ACM_Journals_Primary_Article_Template_2_.zip
│   ├── Milestone_1_Research_Questions_and_Methodology_v2.pdf
│   ├── Milestone_2_Research_Paper1.pdf
│   └── Milestone_3_Research_Paper2.pdf
│
├── reproducibility/               # Reproduction notebooks + documentation
│   ├── requirements.txt
│   ├── RQ1_TestingBehavior_AI_Agents.ipynb
│   ├── RQ2_Review_Dynamics.ipynb
│   └── RQ3_Acceptance_Analysis.ipynb
│
├── results/                       # All exported figures for the paper
│   └── figures/
│       ├── fig1_comment_type_distribution.png
│       ├── fig4_radar_agents.png
│       ├── rq1_average_test_file_count.png
│       ├── rq1_conditional_test_contribution.png
│       ├── rq1_test_inclusion_rate.png
│       ├── rq1_test_inclusion_rate_by_task.png
│       ├── rq1_testing_behavior_profile.png
│       ├── rq1_three_panel_summary.png
│       ├── rq2_fig1_comment_type_distribution.png
│       ├── rq2_fig2_resolution_heatmap.png
│       ├── rq2_fig3_resolution_comparison.png
│       └── rq3_fig_summary_features.png
│
├── .gitignore
├── environment.yml                # Conda environment
├── LICENSE
└── README.md

```



---

## 🔍 Research Questions

### **RQ1 — Do AI agents generate tests?**
- Detect test files using directory and filename heuristics  
  (e.g., `tests/`, `__tests__/`, `*_test.py`, `.spec.ts`).
- Compute:
  - `contains_test`
  - `test_file_count`
  - test inclusion rate per agent
  - test inclusion rate per task type

**Key Finding:**  
Only **1–5%** of AI-generated PRs contain tests.  
When tests appear, they usually come in **large template batches** (8–17 files).

---

### **RQ2 — What types of review comments do agents receive, and how well do they resolve them?**

Processing steps:
1. Two-stage cleaning of review comments  
   (remove bots, CI noise, diffs, code dumps).
2. Rule-based classification into:
   - correctness  
   - style  
   - documentation  
   - security  
   - testing  
   - other
3. Infer whether a comment is resolved using commit sequences.

**Key Findings:**
- **Correctness** comments dominate across all agents.
- Correctness and style issues have the **lowest resolution rates**.
- Documentation and testing remarks are resolved more easily.

---

### **RQ3 — Do early PR features predict acceptance?**
Features used:
- PR description length  
- churn (additions + deletions)  
- number of changed files  
- presence/absence of tests  

**Key Findings:**
- Rejected PRs show significantly higher churn, longer descriptions, and more file modifications.
- Smaller and more focused PRs are more likely to be accepted.
- Test presence has no predictive power (because tests are extremely rare).

---

## ⚙️ Environment Setup

### **Option A — Conda (recommended)**

```bash
conda env create -f environment.yml
conda activate data542
```
### **Option B — pip**

```bash
pip install -r requirements.md
```

## 🚀 How to Reproduce the Results

- A full reproducibility guide is provided in:
## 📄 Paper

- The paper is written in LaTeX using a modified ACM acmsmall template.
- The final paper is 7 pages, as required by the DATA 542 project instructions.
## 🔒 Ethics & Privacy

- Only public GitHub PRs and comments are used.
- No personal, private, or sensitive information is included.
- All analyses focus on aggregate behavior of AI coding agents.
- This project fully complies with UBC research ethics expectations for coursework.

##  License

- This repository is released under the MIT License.
- See the LICENSE file for details.

## 🙏 Acknowledgements

- AIDev dataset by Hao Li et al. (2025):
- https://huggingface.co/datasets/hao-li/AIDev

