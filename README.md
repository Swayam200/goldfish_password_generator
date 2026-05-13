# Random Number Generator Using Fish Movements
[Demo Video (Drive)](https://drive.google.com/file/d/1i2_A7jCL5BgJ4X8Ba78uF44QN4N8ooCP/view?usp=sharing)
![shuvrodeep-dutta-RwV0gDKXRLo-unsplash](https://github.com/user-attachments/assets/47971a19-0bff-4958-b272-f841132bc7ad)

## Overview
This repository implements the pipeline described in our accepted paper: using goldfish movement as a biological entropy source, extracting a binary sequence with computer vision, and hashing that sequence to seed password generation. The goal is a transparent, reproducible codebase that maps cleanly to the paper while keeping all claims accurate.

## Paper
- Title: [Add final paper title]
- Authors: [Add author list]
- Conference: [Add conference name]
- Year: 2026
- Link: [Add DOI or URL]

## Method (Paper-Aligned Summary)
1. Record goldfish movement in a controlled environment and capture a video stream.
2. Track fish centroids per frame (HSV color thresholding + contour selection).
3. Extract per-frame features (distance to center, angle, velocity, pixel variation).
4. Sample and interleave features from two fish, producing a raw binary sequence.
5. Scramble with a lightweight LFSR to reduce local bias.
6. Hash the final sequence (SHA-256) to seed password generation.

## Results and NIST Testing
- The paper reports passing 13/14 NIST tests on the full evaluation sequences at $\alpha = 0.01$.
- The included sample NIST logs in [results/nist](results/nist) are shorter runs for reproducibility. Several tests are reported as -1 in those logs due to sequence length or NIST configuration constraints. These logs are kept as-is for transparency.
- Sample binary sequences are stored in [results/outputs](results/outputs) for convenience and do not necessarily correspond to the NIST logs.

## Demo
- Local demo video: [Goldfish_Demo.mp4](Goldfish_Demo.mp4)
- Drive mirror: https://drive.google.com/file/d/1i2_A7jCL5BgJ4X8Ba78uF44QN4N8ooCP/view?usp=sharing

## Quickstart
1. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

2. Generate a password directly from a video:
  ```bash
  python main.py --video path/to/GoldFishRandom.mp4 --length 16 --special 2 --digits 2 --preview
  ```

3. Generate a password from an existing binary sequence:
  ```bash
  python main.py --binary results/outputs/goldfish_binary_sample.txt --length 16 --special 2 --digits 2
  ```

## Analysis Scripts
- Entropy over time:
  ```bash
  python -m scripts.analysis.entropy_analysis --binary results/outputs/goldfish_binary_sample.txt
  ```

- Randomness over time (goldfish vs baseline PRNG):
  ```bash
  python -m scripts.analysis.randomness_over_time --binary results/outputs/goldfish_binary_sample.txt
  ```

- Heatmap comparison:
  ```bash
  python -m scripts.analysis.heatmap --binary results/outputs/goldfish_binary_sample.txt
  ```

- NIST results plot:
  ```bash
  python -m scripts.analysis.nist_graph --goldfish results/nist/goldfish_nist.txt --prng results/nist/prng_nist_test.txt
  ```

## Project Structure
- main.py
- scripts/
  - core/
    - goldfish_tracker_hsv.py
    - entropy_utils.py
    - periodic_prng.py
    - random_binary.py
  - analysis/
    - entropy_analysis.py
    - randomness_over_time.py
    - heatmap.py
    - nist_graph.py
- results/
  - outputs/
  - nist/
  - figures/
- randomness_testsuite/

## Data
Raw video data is not included in this repository. Record your own or obtain data via the paper's data collection protocol, then supply the video path to the CLI.

## Limitations
- Requires stable lighting and consistent background conditions for reliable tracking.
- Short sequences can lead to NIST tests returning -1 (insufficient length).
- Current tracking thresholds are tuned for orange goldfish; other species may need re-tuning.

## License
This project is licensed under the MIT License. See LICENSE for details.
