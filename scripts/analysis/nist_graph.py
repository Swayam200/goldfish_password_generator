from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

TESTS = [
    "Monobit",
    "BlockFreq",
    "Runs",
    "LongestRun",
    "MatrixRank",
    "FFT",
    "TemplateMatch",
    "Maurer",
    "LinearComplex",
    "Serial1",
    "Serial2",
    "ApproxEntropy",
    "CumSumF",
    "CumSumB",
]


def extract_last_float(line: str) -> float | None:
    matches = re.findall(r"-?\d+\.\d+", line)
    if not matches:
        return None
    return float(matches[-1])


def parse_nist_file(path: str | Path) -> list[float]:
    pvalues: dict[str, float] = {}
    serial_values: list[float] = []
    serial_mode = False

    for line in Path(path).read_text().splitlines():
        if "Frequency (Monobit) Test" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["Monobit"] = value
        elif "Frequency Test within a Block" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["BlockFreq"] = value
        elif "Runs Test" in line and "Serial" not in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["Runs"] = value
        elif "Test for the Longest Run of Ones in a Block" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["LongestRun"] = value
        elif "Binary Matrix Rank Test" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["MatrixRank"] = value
        elif "Discrete Fourier Transform" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["FFT"] = value
        elif "Non-overlapping Template Matching Test" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["TemplateMatch"] = value
        elif "Universal Statistical" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["Maurer"] = value
        elif "Linear Complexity Test" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["LinearComplex"] = value
        elif "Serial Test" in line:
            serial_mode = True
            serial_values = []
        elif serial_mode:
            value = extract_last_float(line)
            if value is not None:
                serial_values.append(value)
            if len(serial_values) == 2:
                pvalues["Serial1"] = serial_values[0]
                pvalues["Serial2"] = serial_values[1]
                serial_mode = False
        elif "Approximate Entropy Test" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["ApproxEntropy"] = value
        elif "Cumulative Sums Test (Forward)" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["CumSumF"] = value
        elif "Cumulative Sums Test (Backward)" in line:
            value = extract_last_float(line)
            if value is not None:
                pvalues["CumSumB"] = value

    return [pvalues.get(test, -1.0) for test in TESTS]


def annotate_bars(axis: plt.Axes, rects: list[plt.Rectangle]) -> None:
    for rect in rects:
        height = rect.get_height()
        axis.annotate(
            f"{height:.2f}",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot NIST test p-values from saved outputs.",
    )
    parser.add_argument(
        "--goldfish",
        default="results/nist/goldfish_nist.txt",
        help="NIST output file for goldfish RNG.",
    )
    parser.add_argument(
        "--prng",
        default="results/nist/prng_nist_test.txt",
        help="NIST output file for baseline PRNG.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save the figure.",
    )
    args = parser.parse_args()

    goldfish_results = parse_nist_file(args.goldfish)
    prng_results = parse_nist_file(args.prng)

    x = np.arange(len(TESTS))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width / 2, goldfish_results, width, label="Goldfish RNG")
    rects2 = ax.bar(x + width / 2, prng_results, width, label="Baseline PRNG")

    ax.set_xlabel("Tests")
    ax.set_ylabel("P-Values")
    ax.set_title("NIST Test Results Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(TESTS, rotation=45, ha="right")
    ax.legend()

    significance_level = 0.01
    ax.axhline(significance_level, color="red", linestyle="--")

    annotate_bars(ax, list(rects1))
    annotate_bars(ax, list(rects2))

    plt.tight_layout()
    if args.output:
        plt.savefig(args.output, dpi=200, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
