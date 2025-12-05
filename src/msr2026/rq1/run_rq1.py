# ============================================================
# RQ1 — Testing Behavior of AI Coding Agents
# MSR 2026 Challenge Track Artifact Version (Network-based)
# ============================================================

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.msr2026.utils.plotting import save_fig


# ============================
# Global Constants
# ============================
DATA_ROOT = "hf://datasets/hao-li/AIDev/"
FIG_DIR = "../output/figures/RQ1"
TABLE_DIR = "../output/tables/RQ1"

TEST_PATTERN = r"(?i)(?:^|/)(?:tests?/|test_|_test|__tests__/)"


# Ensure output directories exist
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)


# ============================
# Data Loading
# ============================
def load_data():
    """Load RQ1 datasets directly from HuggingFace (hf://)."""
    print("Loading RQ1 data from HuggingFace...")

    all_pr = pd.read_parquet(f"{DATA_ROOT}all_pull_request.parquet")
    commit = pd.read_parquet(f"{DATA_ROOT}pr_commit_details.parquet")
    task_type = pd.read_parquet(f"{DATA_ROOT}pr_task_type.parquet")

    return all_pr, commit, task_type


# ============================
# Data Processing
# ============================
def extract_test_files(commit):
    """Mark test files and aggregate PR-level test indicators."""
    print("Extracting test file indicators...")

    commit["is_test_file"] = commit["filename"].str.contains(TEST_PATTERN, regex=True, na=False)
    commit["test_file_count"] = commit["is_test_file"].astype(int)

    pr_test_agg = (
        commit.groupby("pr_id")
        .agg(
            contains_test=("is_test_file", "any"),
            test_file_count=("test_file_count", "sum"),
        )
        .reset_index()
    )
    return pr_test_agg


def merge_pr_info(all_pr, pr_test_agg, task_type):
    """Merge PR metadata with test indicators and task types."""
    print("Merging PR-level data...")

    pr = all_pr.merge(pr_test_agg, left_on="id", right_on="pr_id", how="left")

    pr["contains_test"] = pr["contains_test"].fillna(False)
    pr["test_file_count"] = pr["test_file_count"].fillna(0).astype(int)

    task_type = task_type.rename(columns={"id": "pr_id", "type": "task_type"})
    pr = pr.merge(task_type[["pr_id", "task_type"]], on="pr_id", how="left")
    pr["task_type"] = pr["task_type"].fillna("Unknown")

    return pr[["id", "agent", "contains_test", "test_file_count", "task_type", "created_at"]]


# ============================
# Plotting Helpers
# ============================
def plot_bar(df, x, y, title, xlabel, ylabel, fname):
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x=x, y=y)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    save_fig(FIG_DIR, fname)


def plot_heatmap(df, title, fname, cmap_color="blue", cbar_label="Value"):
    """ACM low-saturation heatmap."""
    plt.figure(figsize=(8, 4.2))

    cmap = sns.light_palette("#4C72B0" if cmap_color == "blue" else "#2C7A7B",
                             n_colors=6, as_cmap=True)

    ax = sns.heatmap(
        df,
        annot=True,
        fmt=".2f",
        cmap=cmap,
        linewidths=0.4,
        linecolor="#FFFFFF",
        cbar_kws={"shrink": 0.55, "label": cbar_label},
        annot_kws={"fontsize": 10},
    )

    if title:
        plt.title(title, fontsize=14)

    plt.xticks(rotation=25, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    save_fig(FIG_DIR, fname)


def plot_rq1_three_panel(inc, avg, cond, fname):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    plt.subplots_adjust(wspace=0.3)

    plots = [
        ("test_inclusion_rate", "Test Inclusion Rate", inc),
        ("avg_test_file_count", "Average Test File Count", avg),
        ("conditional_avg_test_file_count", "Conditional Test Contribution", cond),
    ]

    for ax, (col, title, df) in zip(axes, plots):
        sns.barplot(data=df, x=col, y="agent", ax=ax)
        ax.set_title(title, fontsize=13)
        ax.set_xlabel(col.replace("_", " ").title())
        ax.set_ylabel("Agent")

    plt.tight_layout()
    save_fig(FIG_DIR, fname)


# ============================
# Metrics
# ============================
def compute_agent_metrics(pr_df):
    print("Computing agent-level metrics...")

    inclusion = (
        pr_df.groupby("agent")["contains_test"]
        .mean()
        .rename("test_inclusion_rate")
        .reset_index()
    )

    avg_test = (
        pr_df.groupby("agent")["test_file_count"]
        .mean()
        .rename("avg_test_file_count")
        .reset_index()
    )

    conditional = (
        pr_df[pr_df["test_file_count"] > 0]
        .groupby("agent")["test_file_count"]
        .mean()
        .rename("conditional_avg_test_file_count")
        .reset_index()
    )

    return inclusion, avg_test, conditional


# ============================
# MAIN ENTRYPOINT
# ============================
def run_rq1():
    print("\n===================== Running RQ1 =====================")

    # Load data
    all_pr, commit, task_type = load_data()

    # Extract test indicators
    pr_test = extract_test_files(commit)

    # Merge PR-level metadata
    pr_df = merge_pr_info(all_pr, pr_test, task_type)

    # Compute metrics
    inclusion, avg_test, conditional = compute_agent_metrics(pr_df)

    # ============================
    # Save table outputs (CSV)
    # ============================
    print("Saving CSV outputs...")
    inclusion.to_csv(f"{TABLE_DIR}/rq1_test_inclusion.csv", index=False)
    avg_test.to_csv(f"{TABLE_DIR}/rq1_average_test_files.csv", index=False)
    conditional.to_csv(f"{TABLE_DIR}/rq1_conditional_test_files.csv", index=False)

    print("✔ CSV tables saved to:", TABLE_DIR)

    # ============================
    # Plotting
    # ============================
    plot_bar(inclusion, "test_inclusion_rate", "agent",
             "Test Inclusion Across AI Agents",
             "Inclusion Rate", "Agent",
             "rq1_test_inclusion")

    plot_bar(avg_test, "avg_test_file_count", "agent",
             "Average Test File Count",
             "Avg Test Files", "Agent",
             "rq1_avg_test_files")

    plot_bar(conditional, "conditional_avg_test_file_count", "agent",
             "Conditional Test Contribution",
             "Avg Test Files (Only PRs With Tests)", "Agent",
             "rq1_conditional")

    # Combined 3-panel
    plot_rq1_three_panel(inclusion, avg_test, conditional, "rq1_three_panel")

    # Heatmaps
    behavior_matrix = (
        inclusion.set_index("agent")
        .join(avg_test.set_index("agent"))
        .join(conditional.set_index("agent"))
    )

    behavior_matrix.to_csv(f"{TABLE_DIR}/rq1_behavior_matrix.csv")
    print("✔ Behavior matrix saved.")

    plot_heatmap(behavior_matrix, title=None,
                 fname="rq1_behavior_heatmap",
                 cmap_color="teal",
                 cbar_label="Value")

    # Top-4 task-type heatmap
    type_inclusion = (
        pr_df.groupby(["agent", "task_type"])["contains_test"]
        .mean()
        .rename("test_inclusion_rate")
        .reset_index()
    )

    top4 = (
        type_inclusion[type_inclusion["task_type"] != "Unknown"]["task_type"]
        .value_counts()
        .head(4)
        .index.tolist()
    )

    filtered = type_inclusion[type_inclusion["task_type"].isin(top4)]
    pivot = filtered.pivot(index="agent", columns="task_type", values="test_inclusion_rate")
    pivot = pivot[pivot.mean().sort_values(ascending=False).index]

    pivot.to_csv(f"{TABLE_DIR}/rq1_task_type_matrix.csv")
    print("✔ Task-type matrix saved.")

    plot_heatmap(
        pivot,
        title=None,
        fname="rq1_task_type_heatmap",
        cmap_color="blue",
        cbar_label="Test Inclusion Rate"
    )

    print("✔ RQ1 completed — Figures saved to:", FIG_DIR)
