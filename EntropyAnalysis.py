import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
import random
from GoldFishTrackerHSV import integer_array as tdc
from shorterseedrand import numbers


# Original dataset (provided data)
random_numbers = tdc  # Replace with your original data
window_size = 50  # Size of the moving window for calculating entropy

# Generate random dataset
random_data = numbers

# Function to calculate entropy for a segment
def calculate_entropy(segment):
    hist, _ = np.histogram(segment, bins='auto')
    return entropy(hist)

# Compute entropy over time for original data
original_entropy_values = [
    calculate_entropy(random_numbers[i:i + window_size])
    for i in range(len(random_numbers) - window_size + 1)
]

# Compute entropy over time for random data
random_entropy_values = [
    calculate_entropy(random_data[i:i + window_size])
    for i in range(len(random_data) - window_size + 1)
]

# Plot entropy for both datasets
plt.figure(figsize=(10, 6))
plt.plot(
    range(len(original_entropy_values)),
    original_entropy_values,
    label='Entropy (Original Data)',
    color='blue',
)
plt.plot(
    range(len(random_entropy_values)),
    random_entropy_values,
    label='Entropy (Random Data)',
    color='orange',
)
plt.xlabel('Time')
plt.ylabel('Entropy')
plt.title('Entropy Over Time (Original vs Random Data)')
plt.legend()
plt.grid(True)
plt.show()
