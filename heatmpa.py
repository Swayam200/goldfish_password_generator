import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from GoldFishTrackerHSV import two_digit_chunks as tdc
from shorterseedrand import numbers

# Example function to simulate GoldFish and PRNG datasets
def generate_data(length, prng_period=50, goldfish_seed=42):
    np.random.seed(goldfish_seed)  # GoldFish is a random dataset
    goldfish_data = tdc[:length]  # Slice GoldFish data to match the required length
    
    # PRNG with a smaller period
    prng_data = numbers  # Ensure PRNG matches the same length
    
    return goldfish_data, prng_data

# Generate random data
length = 100
goldfish_data, prng_data = generate_data(length)

# Create a heatmap for both GoldFish and PRNG
# We will stack both datasets vertically for comparison
data = np.vstack([goldfish_data, prng_data])

# Plotting
plt.figure(figsize=(10, 6))
sns.heatmap(data, cmap='YlGnBu', cbar=True, xticklabels=10, yticklabels=['GoldFish', 'PRNG'])
plt.title('Heatmap of Randomness for GoldFish and PRNG')
plt.xlabel('Index (Reduced Sampling)')
plt.ylabel('Dataset')
plt.show()
