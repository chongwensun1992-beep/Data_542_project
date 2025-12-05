# ============================================================
# RQ3 — Early Acceptance Signals in AI-Generated Pull Requests
# MSR 2026 Challenge Track Artifact Version (Network-based)
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import mannwhitneyu
from src.msr2026.utils.plotting import save_fig



# ============================================================
# Global Settings & Config
# ============================================================
DATA_ROOT = "hf://datasets/hao-li/AIDev/"
FIG_DIR = "../output/figures/RQ3"
TABLE_DIR = "../output/tables/RQ3"

# ensure output folders exist
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)

COLOR_ACCEPT = "#4C72B0"  # blue
COLOR_REJECT = "#C44E52"  # red

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.linewidth": 1.2,
    "lines.linewidth": 1.4,
    "axes.grid": True,
    "grid.color": "0.85",
    "grid.linestyle": "--",
    "grid.linewidth": 0.7,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "figure.dpi": 200,
})


# ============================================================
# Data Loading
# ============================================================
def load_rq3_data():
    print("Loading RQ3 data from HuggingFace...")

    pull_request = pd.read_parquet(f"{DATA_ROOT}pull_request.parquet")
    pr_commit_details = pd.read_parquet(f"{DATA_ROOT}pr_commit_details.parquet")

    return pull_request, pr_commit_details


# ============================================================
# Feature Engineering
# ============================================================
def compute_features(pull_request, pr_commit_details):
    print("Computing RQ3 features...")

    ai_pr = pull_request[pull_request["agent"] != "Human"].copy()
    ai_pr["pr_id"] = ai_pr["id"]
    ai_pr["accepted"] = ai_pr["merged_at"].notna().astype(int)

    # Description length
    ai_pr["desc_length"] = ai_pr["body"].fillna("").astype(str).str.len()

    # Churn & file count
    stats = (
        pr_commit_details.groupby("pr_id")
        .agg(
            total_add=("additions", "sum"),
            total_del=("deletions", "sum"),
            files_changed=("filename", "nunique"),
        )
        .reset_index()
    )
    stats["total_add"] = stats["total_add"].fillna(0)
    stats["total_del"] = stats["total_del"].fillna(0)
    stats["churn"] = stats["total_add"] + stats["total_del"]

    # Test presence
    TEST_PATTERN = r"(?i)(?:^|/)(?:tests?/|test_|_test|__tests__/)"
    is_test = (
        pr_commit_details.assign(
            is_test=lambda df: df["filename"].str.contains(TEST_PATTERN, regex=True)
        )
        .groupby("pr_id")["is_test"]
        .any()
        .astype(int)
        .reset_index()
    )

    final = (
        ai_pr[["pr_id", "agent", "accepted", "desc_length"]]
        .merge(stats[["pr_id", "churn", "files_changed"]], on="pr_id", how="left")
        .merge(is_test, on="pr_id", how="left")
    )

    final = final.fillna({"churn": 0, "files_changed": 0, "is_test": 0})

    return final


# ============================================================
# Utility — Outlier clipping (for visualization only)
# ============================================================
def clip_feature(df, feature, p=0.99):
    limit = df[feature].quantile(p)
    df[feature] = np.where(df[feature] > limit, limit, df[feature])
    return df


# ============================================================
# Visualization — ACM 1×3 Log-Boxplots
# ============================================================
def log_box(ax, feature, title, final_clipped):
    groups = [
        final_clipped[final_clipped["accepted"] == 0][feature],
        final_clipped[final_clipped["accepted"] == 1][feature],
    ]

    bp = ax.boxplot(
        groups,
        patch_artist=True,
        labels=["Reject", "Accept"],
        showfliers=False,
        medianprops=dict(color="black", linewidth=1.4),
        boxprops=dict(color="black"),
        whiskerprops=dict(color="black"),
        capprops=dict(color="black"),
    )

    colors = [COLOR_REJECT + "33", COLOR_ACCEPT + "33"]
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(c)

    ax.set_yscale("log")
    ax.set_title(title, pad=10)


# ============================================================
# MAIN ENTRYPOINT
# ============================================================
def run_rq3():
    print("\n===================== Running RQ3 =====================")

    # 1. Load data
    pull_request, pr_commit_details = load_rq3_data()

    # 2. Compute features
    final = compute_features(pull_request, pr_commit_details)

    # ---- Save raw features to CSV ----
    final.to_csv(f"{TABLE_DIR}/rq3_features_raw.csv", index=False)

    # 3. Apply clipping for visualization
    final_clipped = final.copy()
    for f in ["desc_length", "churn", "files_changed"]:
        final_clipped = clip_feature(final_clipped, f)

    final_clipped.to_csv(f"{TABLE_DIR}/rq3_features_clipped.csv", index=False)

    # 4. Summary statistics
    summary = pd.DataFrame({
        f: {
            "Reject_median": final[final["accepted"] == 0][f].median(),
            "Reject_IQR": final[final["accepted"] == 0][f].quantile(0.75) - final[final["accepted"] == 0][f].quantile(0.25),
            "Accept_median": final[final["accepted"] == 1][f].median(),
            "Accept_IQR": final[final["accepted"] == 1][f].quantile(0.75) - final[final["accepted"] == 1][f].quantile(0.25),
        }
        for f in ["desc_length", "churn", "files_changed", "is_test"]
    }).T

    summary.to_csv(f"{TABLE_DIR}/rq3_summary_table.csv")

    print("\n=========== RQ3 Summary Table (Median & IQR) ===========")
    print(summary)
    print("========================================================\n")

    # 5. Log-boxplots
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    plot_features = [
        ("desc_length", "Description Length"),
        ("churn", "Churn"),
        ("files_changed", "Files Changed"),
    ]
    for ax, (f, title) in zip(axes, plot_features):
        log_box(ax, f, title, final_clipped)

    plt.tight_layout()
    save_fig(FIG_DIR, "rq3_features")

    # 6. Statistical significance tests
    print("\n===== Statistical Significance Tests (RQ3) =====")

    accepted = final[final["accepted"] == 1]
    rejected = final[final["accepted"] == 0]

    tests = []
    def mw_test(feature):
        stat, p = mannwhitneyu(
            rejected[feature],
            accepted[feature],
            alternative="two-sided"
        )
        tests.append([feature, stat, p])
        print(f"{feature:15s}: U={stat:.4e}, p={p:.4f}")

    mw_test("desc_length")
    mw_test("churn")
    mw_test("files_changed")
    mw_test("is_test")

    # save MW-U test results
    pd.DataFrame(tests, columns=["feature", "U_value", "p_value"]).to_csv(
        f"{TABLE_DIR}/rq3_mannwhitney_tests.csv",
        index=False
    )

    print("========================================================")
    print("✔ RQ3 completed — Figures saved to:", FIG_DIR)
    print("✔ CSV tables saved to:", TABLE_DIR)
