import random
import hashlib
from GoldFishTrackerHSV import random_sequence
movement_data = random_sequence  # Assuming 'final' is defined somewhere in your code

hashed_seed = hashlib.sha256(movement_data.encode()).hexdigest()
random.seed(hashed_seed)

print(hashed_seed)
def generate_password(length, num_special, num_digits):
    password_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    special_characters = "!@#$%^&*()"
    digits = "0123456789"

    if num_special + num_digits > length:
        raise ValueError("Number of special characters and digits exceeds password length")

    random.seed(hashed_seed)  # This ensures that the same seed generates the result

    password = (
        [random.choice(special_characters) for _ in range(num_special)] +
        [random.choice(digits) for _ in range(num_digits)]
    )

    remaining_length = length - num_special - num_digits
    password += [random.choice(password_characters) for _ in range(remaining_length)]

    random.shuffle(password)

    return ''.join(password)


def main():
    try:
        length = int(input("Enter Password Length: "))
        num_special = int(input("Enter Number of Special Characters: "))
        num_digits = int(input("Enter Number of Digits: "))

        password = generate_password(length, num_special, num_digits)

        print(f"Generated Password: {password}")

        # Optionally, you can add functionality to copy to clipboard here if needed
        # However, this would require additional libraries like pyperclip

    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print("Error: Invalid input")


if __name__ == "__main__":
    main()