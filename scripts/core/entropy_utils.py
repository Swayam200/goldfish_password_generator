from __future__ import annotations

from pathlib import Path
from typing import Iterable


def load_binary_sequence(path: str | Path) -> str:
    raw = Path(path).read_text().strip()
    return "".join(ch for ch in raw if ch in "01")


def save_binary_sequence(binary_sequence: str, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(binary_sequence)


def binary_to_ints(binary_sequence: str, chunk_size: int = 8) -> list[int]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    usable_length = len(binary_sequence) - (len(binary_sequence) % chunk_size)
    return [
        int(binary_sequence[i : i + chunk_size], 2)
        for i in range(0, usable_length, chunk_size)
    ]


def ints_to_two_digit_chunks(values: Iterable[int]) -> list[int]:
    return [value % 100 for value in values]


def binary_to_two_digit_chunks(binary_sequence: str) -> list[int]:
    return ints_to_two_digit_chunks(binary_to_ints(binary_sequence))
