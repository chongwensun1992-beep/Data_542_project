# ============================================================
# Run All RQs — MSR 2026 Challenge Track Artifact
# ============================================================

import sys
import os

# Ensure src/ is on the Python path
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(ROOT, "src")
sys.path.append(SRC_PATH)

# Import RQ pipelines
from src.msr2026.rq1.run_rq1 import run_rq1
from src.msr2026.rq2.run_rq2 import run_rq2
from src.msr2026.rq3.run_rq3 import run_rq3


if __name__ == "__main__":

    print("\n================= MSR 2026 — Running All RQs =================\n")

    run_rq1()
    print("\n----------------- RQ1 Completed -----------------\n")

    run_rq2()
    print("\n----------------- RQ2 Completed -----------------\n")

    run_rq3()
    print("\n----------------- RQ3 Completed -----------------\n")

    print("\n✔ All RQs Completed — Figures and Tables saved to /output\n")
