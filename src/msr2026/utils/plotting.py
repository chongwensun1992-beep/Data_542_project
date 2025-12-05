# src/utils/plotting.py
import os
import matplotlib.pyplot as plt


def ensure_dir(path: str):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def save_fig(fig_dir: str, name: str):
    """
    Save a figure to PNG and PDF formats (ACM-ready).
    Automatically creates the directory if needed.
    """
    ensure_dir(fig_dir)

    png_path = os.path.join(fig_dir, f"{name}.png")
    pdf_path = os.path.join(fig_dir, f"{name}.pdf")

    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.savefig(pdf_path, bbox_inches="tight")
    plt.close()
