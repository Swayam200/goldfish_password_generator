import matplotlib.pyplot as plt
import numpy as np

# Data from the two files (manually parsed)
nist1_results = [
    0.9020346492544503, 0.6065306597126334, 0.7126025058889216, 0.9723849629374176,
    -1.0, 0.8212690882910506, 0.9999797681511727, -1.0, -1.0, 0.4989610874592239, 
    0.245841034721659, 1.0, 0.75832349293589, 0.8673736988386227
]

nist2_results = [
    0.21835469056590195, 0.0820849986238988, 0.47596984089148886, 0.27556009460449676,
    -1.0, 0.4291217069788855, 0.9999797681511727, -1.0, -1.0,
    0.833864766445661, 0.7529282103238129, 1.0, 0.24777481159120243, 0.2792800633384313
]

# Test names (shortened for clarity)
tests = [
    "Monobit", "BlockFreq", "Runs", "LongestRun",
    "MatrixRank", "FFT", "TemplateMatch", "Maurer",
    "LinearComplex", "Serial1", "Serial2", "ApproxEntropy",
    "CumSumF", "CumSumB"
]

# Plotting
x = np.arange(len(tests))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width/2, nist1_results, width, label='GoldfishRNG')
rects2 = ax.bar(x + width/2, nist2_results, width, label='pRNG')

# Add labels, title, and legend
ax.set_xlabel('Tests')
ax.set_ylabel('P-Values')
ax.set_title('NIST Test Results Comparison')
ax.set_xticks(x)
ax.set_xticklabels(tests, rotation=45, ha="right")
ax.legend()

# Add a horizontal line for significance threshold (e.g., 0.01)
significance_level = 0.01
ax.axhline(significance_level, color='red', linestyle='--', label='Significance Threshold')

# Annotate bars
def annotate_bars(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # offset
                    textcoords="offset points",
                    ha='center', va='bottom')

annotate_bars(rects1)
annotate_bars(rects2)

# Show plot
plt.tight_layout()
plt.show()
