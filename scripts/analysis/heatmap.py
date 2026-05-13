from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from scripts.core.entropy_utils import binary_to_two_digit_chunks, load_binary_sequence
from scripts.core.periodic_prng import generate_periodic_prng


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visualize goldfish vs baseline PRNG values as a heatmap.",
    )
    parser.add_argument(
        "--binary",
        default="results/outputs/goldfish_binary_sample.txt",
        help="Binary sequence generated from goldfish movement.",
    )
    parser.add_argument("--length", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--period", type=int, default=10000000)
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save the figure.",
    )
    args = parser.parse_args()

    goldfish_chunks = binary_to_two_digit_chunks(load_binary_sequence(args.binary))
    baseline_chunks = generate_periodic_prng(
        seed=args.seed,
        length=len(goldfish_chunks),
        period=args.period,
        low=0,
        high=99,
    )

    length = min(args.length, len(goldfish_chunks), len(baseline_chunks))
    goldfish_data = goldfish_chunks[:length]
    baseline_data = baseline_chunks[:length]

    data = np.vstack([goldfish_data, baseline_data])

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        data,
        cmap="YlGnBu",
        cbar=True,
        xticklabels=10,
        yticklabels=["Goldfish", "Baseline PRNG"],
    )
    plt.title("Heatmap of Randomness for Goldfish and Baseline PRNG")
    plt.xlabel("Index (Reduced Sampling)")
    plt.ylabel("Dataset")

    if args.output:
        plt.savefig(args.output, dpi=200, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
