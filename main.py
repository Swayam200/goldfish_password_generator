from __future__ import annotations

import argparse
import hashlib
import random

from scripts.core.entropy_utils import load_binary_sequence
from scripts.core.goldfish_tracker_hsv import extract_entropy_from_video


def generate_password(
    length: int,
    num_special: int,
    num_digits: int,
    seed_hex: str,
) -> str:
    password_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    special_characters = "!@#$%^&*()"
    digits = "0123456789"

    if num_special + num_digits > length:
        raise ValueError("Number of special characters and digits exceeds password length")

    rng = random.Random(seed_hex)
    password = [rng.choice(special_characters) for _ in range(num_special)]
    password += [rng.choice(digits) for _ in range(num_digits)]

    remaining_length = length - num_special - num_digits
    password += [rng.choice(password_characters) for _ in range(remaining_length)]
    rng.shuffle(password)

    return "".join(password)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a password from goldfish-derived entropy.",
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--video",
        help="Path to the goldfish movement video to process.",
    )
    source_group.add_argument(
        "--binary",
        help="Path to a pre-generated binary sequence.",
    )
    parser.add_argument("--length", type=int, default=16)
    parser.add_argument("--special", type=int, default=2)
    parser.add_argument("--digits", type=int, default=2)
    parser.add_argument(
        "--output-binary",
        default="results/outputs/goldfish_binary.txt",
        help="Where to save extracted binary when using --video.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show live tracking preview while processing video.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Optional frame limit for quicker runs.",
    )
    parser.add_argument(
        "--show-hash",
        action="store_true",
        help="Print the SHA-256 hash used as the password seed.",
    )
    args = parser.parse_args()

    if args.video:
        artifacts = extract_entropy_from_video(
            args.video,
            output_path=args.output_binary,
            show_preview=args.preview,
            max_frames=args.max_frames,
        )
        binary_sequence = artifacts.scrambled
    else:
        binary_sequence = load_binary_sequence(args.binary)

    if not binary_sequence:
        raise ValueError("Binary sequence is empty.")

    hashed_seed = hashlib.sha256(binary_sequence.encode()).hexdigest()
    if args.show_hash:
        print(f"SHA-256 seed: {hashed_seed}")

    password = generate_password(
        length=args.length,
        num_special=args.special,
        num_digits=args.digits,
        seed_hex=hashed_seed,
    )
    print(f"Generated Password: {password}")


if __name__ == "__main__":
    main()
