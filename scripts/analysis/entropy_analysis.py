from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import entropy

from scripts.core.entropy_utils import binary_to_ints, load_binary_sequence
from scripts.core.periodic_prng import generate_periodic_prng


def calculate_entropy(segment: list[int]) -> float:
    hist, _ = np.histogram(segment, bins="auto")
    return float(entropy(hist))


def compute_entropy_over_time(values: list[int], window_size: int) -> list[float]:
    return [
        calculate_entropy(values[i : i + window_size])
        for i in range(len(values) - window_size + 1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot entropy over time for goldfish vs baseline PRNG.",
    )
    parser.add_argument(
        "--binary",
        default="results/outputs/goldfish_binary_sample.txt",
        help="Binary sequence generated from goldfish movement.",
    )
    parser.add_argument("--window-size", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--period", type=int, default=10000000)
    parser.add_argument("--low", type=int, default=0)
    parser.add_argument("--high", type=int, default=255)
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save the figure.",
    )
    args = parser.parse_args()

    binary_sequence = load_binary_sequence(args.binary)
    goldfish_values = binary_to_ints(binary_sequence)

    if len(goldfish_values) < args.window_size:
        raise ValueError("Window size is larger than the available sequence.")

    baseline_values = generate_periodic_prng(
        seed=args.seed,
        length=len(goldfish_values),
        period=args.period,
        low=args.low,
        high=args.high,
    )

    goldfish_entropy = compute_entropy_over_time(goldfish_values, args.window_size)
    baseline_entropy = compute_entropy_over_time(baseline_values, args.window_size)

    plt.figure(figsize=(10, 6))
    plt.plot(
        range(len(goldfish_entropy)),
        goldfish_entropy,
        label="Entropy (Goldfish)",
        color="blue",
    )
    plt.plot(
        range(len(baseline_entropy)),
        baseline_entropy,
        label="Entropy (Baseline PRNG)",
        color="orange",
    )
    plt.xlabel("Time")
    plt.ylabel("Entropy")
    plt.title("Entropy Over Time (Goldfish vs Baseline)")
    plt.legend()
    plt.grid(True)

    if args.output:
        plt.savefig(args.output, dpi=200, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
