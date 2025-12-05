# ================================================================
# RQ2 — Review Comments & Resolution Dynamics
# MSR 2026 Challenge Track Artifact Version (Network-based)
# ================================================================

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from src.msr2026.utils.plotting import save_fig



# ============================
# Constants
# ============================
DATA_ROOT = "hf://datasets/hao-li/AIDev/"
FIG_DIR = "../output/figures/RQ2"
TABLE_DIR = "../output/tables/RQ2"

ACM_STACK_COLORS = [
    "#e8eef7",
    "#d5e0f2",
    "#b7c9e4",
    "#9ab2d6",
    "#7c9bc8",
    "#5c80b1",
]

HEATMAP_CMAP = sns.blend_palette(
    ["#f1f4fb", "#d6e0f3", "#b0c4e4", "#4c72b0"],
    as_cmap=True
)

# Ensure directories exist
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)


# ============================
# Helper Functions
# ============================
def load_rq2_data():
    print("Loading RQ2 data from HuggingFace...")

    pr_review_comments_v2 = pd.read_parquet(f"{DATA_ROOT}pr_review_comments_v2.parquet")
    all_pull_request = pd.read_parquet(f"{DATA_ROOT}all_pull_request.parquet")[["id", "number", "agent"]]
    pr_reviews = pd.read_parquet(f"{DATA_ROOT}pr_reviews.parquet")[["id", "pr_id"]]
    pr_commits = pd.read_parquet(f"{DATA_ROOT}pr_commits.parquet")[["pr_id", "sha"]]

    # Type conversions
    all_pull_request["id"] = all_pull_request["id"].astype("Int64")
    pr_reviews["pr_id"] = pr_reviews["pr_id"].astype("Int64")
    pr_commits["pr_id"] = pr_commits["pr_id"].astype("Int64")

    return pr_review_comments_v2, all_pull_request, pr_reviews, pr_commits


# ============================
# Comment Cleaning Pipeline
# ============================
def clean_comments(df):
    print("\n=== Cleaning Stage 1 ===")
    df["comment_body"] = df["body"].fillna("").astype(str)
    df["comment_time"] = pd.to_datetime(df["created_at"], errors="coerce")

    text = df["comment_body"]

    # Stage 1 Filter
    mask1 = (
        text.str.contains(r"[A-Za-z]{3,}", na=False)
        & (text.str.len() < 3000)
        & (~text.str.startswith(("+", "-"), na=False))
        & (~text.str.contains(r"^@@", regex=True, na=False))
        & (~text.str.contains(r"[{}<>]", na=False))
    )
    filtered = df[mask1].copy()
    print(f"After Stage 1: {len(filtered):,} comments")

    # Stage 2 Filter
    print("\n=== Cleaning Stage 2 ===")
    text = filtered["comment_body"]

    mask2 = (
        ~text.str.contains("dependabot|github-actions|renovate|codecov", case=False, na=False)
        & ~text.str.contains(r"http[s]?://", na=False)
        & ~text.str.contains(r"traceback|exception|error:|failed|stack trace", case=False, na=False)
        & (text.str.len() >= 5)
        & (text.str.len() <= 2000)
        & text.str.contains(r"[A-Za-z]{3,}\s+[A-Za-z]{3,}", na=False)
    )

    filtered2 = filtered[mask2].copy()
    print(f"After Stage 2: {len(filtered2):,} comments")

    filtered2["first_line"] = filtered2["comment_body"].str.split("\n").str[0]
    filtered2["short_body"] = filtered2["first_line"].str.slice(0, 300)

    return filtered2


# ============================
# Rule-based Classification
# ============================
def apply_comment_rules(df):
    print("\n=== Classifying comments ===")

    rules = {
        "correctness": r"\b(fix|bug|issue|error|wrong|incorrect|null|edge case)\b",
        "style": r"\b(style|format|indent|pep8|naming)\b",
        "documentation": r"\b(doc|readme|comment|description|explain)\b",
        "testing": r"\b(test|coverage|unit test)\b",
        "security": r"\b(security|vulnerable|sanitize|injection|escape)\b",
    }

    df["comment_type"] = "other"

    for label, pattern in rules.items():
        df.loc[
            df["short_body"].str.contains(pattern, case=False, regex=True, na=False),
            "comment_type",
        ] = label

    return df


# ============================
# Stacked Bar Plot
# ============================
def plot_stacked_type_distribution(type_counts_pct):
    print("\n=== Generating Figure 1b — Normalized Comment Distribution ===")

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(type_counts_pct))

    for idx, col in enumerate(type_counts_pct.columns):
        ax.barh(
            type_counts_pct.index,
            type_counts_pct[col],
            left=bottom,
            color=ACM_STACK_COLORS[idx],
            edgecolor="white",
            label=col,
        )
        bottom += type_counts_pct[col].values

    ax.set_xlabel("Percentage of Review Comments", fontsize=13)
    ax.set_xlim(0, 1.0)
    ax.set_xticks(np.linspace(0, 1, 6))
    ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.legend(
        title="Comment Type",
        fontsize=11,
        title_fontsize=12,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=len(type_counts_pct.columns),
        frameon=False,
    )

    plt.tight_layout()
    save_fig(FIG_DIR, "rq2_comment_distribution")


# ============================
# Resolution Heatmap
# ============================
def plot_resolution_heatmap(correction_stats):
    print("\n=== Generating Figure 2 — Resolution Heatmap ===")

    plt.figure(figsize=(9, 5))
    sns.heatmap(
        correction_stats,
        annot=True,
        fmt=".2f",
        cmap=HEATMAP_CMAP,
        linewidths=0.5,
        linecolor="#ffffff",
        annot_kws={"fontsize": 11},
        cbar_kws={"shrink": 0.65, "label": "Resolution Rate"},
    )

    plt.xlabel("Comment Type", fontsize=13)
    plt.ylabel("Agent", fontsize=13)
    plt.xticks(rotation=25)
    plt.yticks(rotation=0)

    plt.tight_layout()
    save_fig(FIG_DIR, "rq2_resolution_heatmap")


# ============================
# MAIN ENTRYPOINT
# ============================
def run_rq2():
    print("\n===================== Running RQ2 =====================")

    # 1. Load data
    pr_review_comments_v2, all_pr, pr_reviews, pr_commits = load_rq2_data()

    # 2. Map comments → PR ID
    reviews = pr_review_comments_v2.merge(
        pr_reviews.rename(columns={"id": "pull_request_review_id"}),
        on="pull_request_review_id",
        how="left",
    )

    # 3. Merge PR metadata
    reviews = reviews.merge(
        all_pr.rename(columns={"id": "pr_id"}),
        on="pr_id",
        how="left",
    )
    reviews["agent"] = reviews["agent"].fillna("Unknown")

    # 4. Clean comments
    cleaned = clean_comments(reviews)

    # 5. Apply rules
    classified = apply_comment_rules(cleaned)

    # 6. Count by agent × comment type
    type_counts = (
        classified.groupby("agent")["comment_type"]
        .value_counts()
        .unstack(fill_value=0)
    )

    # Exclude "other"
    plot_type_counts = type_counts.drop(columns=["other"], errors="ignore")
    type_counts_pct = plot_type_counts.div(plot_type_counts.sum(axis=1), axis=0)

    # ---- Save CSV files ----
    print("\nSaving CSV outputs...")

    type_counts.to_csv(f"{TABLE_DIR}/rq2_type_counts_raw.csv")
    plot_type_counts.to_csv(f"{TABLE_DIR}/rq2_type_counts_filtered.csv")
    type_counts_pct.to_csv(f"{TABLE_DIR}/rq2_type_distribution_pct.csv")

    print("✔ Comment distribution tables saved.")

    # 7. Plot normalized distribution
    plot_stacked_type_distribution(type_counts_pct)

    # 8. Compute resolution signal
    commit_count = (
        pr_commits.groupby("pr_id")["sha"]
        .count()
        .reset_index()
        .rename(columns={"sha": "commit_count"})
    )

    classified = classified.merge(commit_count, on="pr_id", how="left")
    classified["commit_count"] = classified["commit_count"].fillna(0)
    classified["resolved"] = classified["commit_count"] > 1

    correction_stats = (
        classified.groupby(["agent", "comment_type"])["resolved"]
        .mean()
        .unstack(fill_value=0)
    )

    correction_stats.to_csv(f"{TABLE_DIR}/rq2_resolution_matrix.csv")
    print("✔ Resolution matrix saved.")

    # 9. Plot heatmap
    plot_resolution_heatmap(correction_stats)

    print("\n✔ RQ2 completed — Figures saved to:", FIG_DIR)
    print("✔ RQ2 CSV tables saved to:", TABLE_DIR)
