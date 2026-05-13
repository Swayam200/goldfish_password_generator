from __future__ import annotations

import argparse
import random


def generate_periodic_prng(
    seed: int,
    length: int,
    period: int,
    *,
    low: int = 0,
    high: int = 100,
) -> list[int]:
    rng = random.Random(seed)
    numbers: list[int] = []
    for index in range(length):
        numbers.append(rng.randint(low, high))
        if period > 0 and (index + 1) % period == 0:
            rng.seed(seed)
    return numbers


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a periodic baseline PRNG sequence for comparison.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--length", type=int, default=38)
    parser.add_argument("--period", type=int, default=10000000)
    parser.add_argument("--low", type=int, default=0)
    parser.add_argument("--high", type=int, default=100)
    args = parser.parse_args()

    numbers = generate_periodic_prng(
        seed=args.seed,
        length=args.length,
        period=args.period,
        low=args.low,
        high=args.high,
    )
    print(numbers)


if __name__ == "__main__":
    main()
