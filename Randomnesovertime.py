import matplotlib.pyplot as plt
import random
from GoldFishTrackerHSV import two_digit_chunks as tdc
from shorterseedrand import numbers

# Example random numbers
# Using the two-digit chunks from GoldFishTrackerHSV
random_numbers_1 = tdc

# Generate a second dataset of 101 two-digit random numbers
random_numbers_2 = numbers

# Adjust the graph scale: select every 2nd or 3rd value for plotting to reduce clutter
x_indices_1 = range(len(random_numbers_1))[::3]  # Every 3rd index for dataset 1
x_indices_2 = range(len(random_numbers_2))[::3]  # Every 3rd index for dataset 2

reduced_numbers_1 = [random_numbers_1[i] for i in x_indices_1]
reduced_numbers_2 = [random_numbers_2[i] for i in x_indices_2]

# Create a larger figure for better scaling
plt.figure(figsize=(14, 8))

# Plot the reduced dataset
plt.plot(x_indices_1, reduced_numbers_1, marker='o', linestyle='-', label='GoldFish (Blue)', color='blue')
plt.plot(x_indices_2, reduced_numbers_2, marker='s', linestyle='--', label='Normal pRNG (Orange)', color='orange')

# Add labels, title, legend, and grid
plt.xlabel('Index (Reduced Sampling)')
plt.ylabel('Random Number')
plt.title('Comparison of Two Random Number Datasets (Reduced Clutter)')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()
