from __future__ import annotations

import argparse
import random
from pathlib import Path


def generate_random_binary_sequence(length: int, seed: int | None = None) -> str:
    rng = random.Random(seed)
    return "".join(rng.choice("01") for _ in range(length))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a random binary sequence.",
    )
    parser.add_argument("--length", type=int, default=264)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", default=None, help="Optional output file path.")
    args = parser.parse_args()

    binary_sequence = generate_random_binary_sequence(args.length, seed=args.seed)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(binary_sequence)
    else:
        print(binary_sequence)


if __name__ == "__main__":
    main()
