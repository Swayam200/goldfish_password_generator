from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from scripts.core.entropy_utils import binary_to_two_digit_chunks, load_binary_sequence
from scripts.core.periodic_prng import generate_periodic_prng


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare goldfish vs baseline PRNG values over time.",
    )
    parser.add_argument(
        "--binary",
        default="results/outputs/goldfish_binary_sample.txt",
        help="Binary sequence generated from goldfish movement.",
    )
    parser.add_argument("--length", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--period", type=int, default=10000000)
    parser.add_argument("--stride", type=int, default=3)
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save the figure.",
    )
    args = parser.parse_args()

    goldfish_chunks = binary_to_two_digit_chunks(load_binary_sequence(args.binary))
    goldfish_chunks = goldfish_chunks[: args.length]

    baseline_chunks = generate_periodic_prng(
        seed=args.seed,
        length=len(goldfish_chunks),
        period=args.period,
        low=0,
        high=99,
    )

    stride = max(1, args.stride)
    x_indices = range(len(goldfish_chunks))[::stride]
    reduced_goldfish = [goldfish_chunks[i] for i in x_indices]
    reduced_baseline = [baseline_chunks[i] for i in x_indices]

    plt.figure(figsize=(14, 8))
    plt.plot(
        x_indices,
        reduced_goldfish,
        marker="o",
        linestyle="-",
        label="Goldfish",
        color="blue",
    )
    plt.plot(
        x_indices,
        reduced_baseline,
        marker="s",
        linestyle="--",
        label="Baseline PRNG",
        color="orange",
    )
    plt.xlabel("Index (Reduced Sampling)")
    plt.ylabel("Random Number")
    plt.title("Comparison of Two Random Number Datasets")
    plt.legend()
    plt.grid(True)

    if args.output:
        plt.savefig(args.output, dpi=200, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
