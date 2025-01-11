import random

def generate_limited_random_numbers(seed, length, period):
    random.seed(seed)
    numbers = []
    for _ in range(length):
        numbers.append(random.randint(0, 100))  # Example range: 0 to 100
        if len(numbers) % period == 0:
            random.seed(seed)  # Re-seed to start a new period
    return numbers

# Example: Generate 100 numbers with a seed and reduced period of 20
numbers = generate_limited_random_numbers(seed=42, length=38, period=10000000)
print(numbers)
