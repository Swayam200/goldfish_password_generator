from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np

from .entropy_utils import binary_to_ints, ints_to_two_digit_chunks, save_binary_sequence


@dataclass
class EntropyArtifacts:
    raw_fish1: str
    raw_fish2: str
    combined: str
    scrambled: str
    integer_array: list[int]
    two_digit_chunks: list[int]


def calculate_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    return float(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def calculate_angle(x1: int, y1: int, x2: int, y2: int) -> float:
    return float(np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi))


def lfsr_scramble(binary_sequence: str, seed: int = 0b1100101) -> str:
    lfsr = seed & 0b1111111
    scrambled_bits = []
    for bit in binary_sequence:
        new_bit = ((lfsr >> 2) & 1) ^ ((lfsr >> 1) & 1)
        lfsr = ((lfsr << 1) | new_bit) & 0b1111111
        scrambled_bits.append(str(int(bit) ^ new_bit))
    return "".join(scrambled_bits)


def extract_entropy_from_video(
    video_path: str | Path,
    *,
    output_path: str | Path | None = None,
    show_preview: bool = False,
    max_frames: int | None = None,
    sampling_interval_range: Tuple[int, int] = (5, 40),
) -> EntropyArtifacts:
    video_path = Path(video_path)
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    frame_count = 0
    binary_sequence_fish1 = ""
    binary_sequence_fish2 = ""
    prev_positions: dict[int, Tuple[int, int]] = {}
    rng = np.random.default_rng()

    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([25, 255, 255])

    try:
        while True:
            if max_frames is not None and frame_count >= max_frames:
                break

            ret, frame = capture.read()
            if not ret:
                break

            height, width, _ = frame.shape
            ref_x, ref_y = width // 2, height // 2
            diagonal = np.sqrt(width ** 2 + height ** 2)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_orange, upper_orange)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) >= 2:
                sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
                entity_data = []
                pixel_variation = int(np.sum(mask) % 256)

                for idx, contour in enumerate(sorted_contours):
                    moments = cv2.moments(contour)
                    if moments["m00"] == 0:
                        continue

                    fish_x = int(moments["m10"] / moments["m00"])
                    fish_y = int(moments["m01"] / moments["m00"])

                    distance = calculate_distance(ref_x, ref_y, fish_x, fish_y)
                    angle = calculate_angle(ref_x, ref_y, fish_x, fish_y)
                    normalized_distance = int((distance / diagonal) * 255)

                    if idx in prev_positions:
                        prev_x, prev_y = prev_positions[idx]
                        velocity = calculate_distance(prev_x, prev_y, fish_x, fish_y)
                        velocity_norm = int((velocity / diagonal) * 255) % 256
                    else:
                        velocity_norm = 0
                    prev_positions[idx] = (fish_x, fish_y)

                    processed_value = (normalized_distance + int(angle) % 360) % 256
                    processed_value = (processed_value ^ velocity_norm ^ pixel_variation) % 256
                    entity_data.append(f"{processed_value:08b}")

                    if show_preview:
                        cv2.circle(frame, (fish_x, fish_y), 5, (0, 255, 0), -1)
                        cv2.line(frame, (ref_x, ref_y), (fish_x, fish_y), (0, 255, 255), 2)

                if len(entity_data) == 2:
                    sample_interval = rng.integers(
                        sampling_interval_range[0], sampling_interval_range[1] + 1
                    )
                    if frame_count % sample_interval == 0:
                        binary_sequence_fish1 += entity_data[0]
                        binary_sequence_fish2 += entity_data[1]

            frame_count += 1

            if show_preview:
                cv2.imshow("Goldfish Tracking", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        capture.release()
        if show_preview:
            cv2.destroyAllWindows()

    combined_sequence = "".join(
        a + b if rng.integers(0, 2) else b + a
        for a, b in zip(binary_sequence_fish1, binary_sequence_fish2)
    )
    scrambled_sequence = lfsr_scramble(combined_sequence)

    if output_path is not None:
        save_binary_sequence(scrambled_sequence, output_path)

    integer_array = binary_to_ints(scrambled_sequence)
    two_digit_chunks = ints_to_two_digit_chunks(integer_array)

    if not scrambled_sequence:
        raise ValueError("No entropy extracted; check video input or parameters.")

    return EntropyArtifacts(
        raw_fish1=binary_sequence_fish1,
        raw_fish2=binary_sequence_fish2,
        combined=combined_sequence,
        scrambled=scrambled_sequence,
        integer_array=integer_array,
        two_digit_chunks=two_digit_chunks,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract a binary sequence from goldfish movement video.",
    )
    parser.add_argument("--video", required=True, help="Path to the input video file.")
    parser.add_argument(
        "--output",
        default="results/outputs/goldfish_binary.txt",
        help="Path to save the generated binary sequence.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show live tracking preview while processing.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Optional frame limit for quicker runs.",
    )
    args = parser.parse_args()

    extract_entropy_from_video(
        args.video,
        output_path=args.output,
        show_preview=args.preview,
        max_frames=args.max_frames,
    )


if __name__ == "__main__":
    main()
