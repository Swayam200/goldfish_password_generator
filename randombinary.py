import random

def generate_random_binary_sequence(length):
    return ''.join(random.choice('01') for _ in range(length))

# Generate a binary sequence of 3000 bits
binary_sequence = generate_random_binary_sequence(264)
print(f"Random Binary Sequence of 3000 bits:\n{binary_sequence}")
