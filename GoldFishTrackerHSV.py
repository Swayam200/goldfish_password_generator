import cv2
import numpy as np

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_angle(x1, y1, x2, y2):
    return np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi)

def lfsr_scramble(binary_sequence, seed=0b1100101, tap=0b101):
    lfsr = seed
    scrambled_sequence = ""
    for bit in binary_sequence:
        new_bit = (lfsr >> 2) & 1 ^ (lfsr >> 1) & 1  # XOR taps
        lfsr = ((lfsr << 1) | new_bit) & 0b1111111  # Keep LFSR within 7 bits
        scrambled_sequence += str(int(bit) ^ new_bit)  # XOR with input bit
    return scrambled_sequence

video = cv2.VideoCapture('GoldFishRandom.mp4')

frame_count = 0
binary_sequence_fish1 = ""
binary_sequence_fish2 = ""
prev_positions = {}

while True:
    ret, frame = video.read()
    if not ret:
        break

    height, width, _ = frame.shape
    ref_x, ref_y = width // 2, height // 2

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([25, 255, 255])
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) >= 2:
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        entity_data = []

        for idx, contour in enumerate(sorted_contours):
            M = cv2.moments(contour)
            if M['m00'] != 0:
                fish_x = int(M['m10'] / M['m00'])
                fish_y = int(M['m01'] / M['m00'])

                distance = calculate_distance(ref_x, ref_y, fish_x, fish_y)
                angle = calculate_angle(ref_x, ref_y, fish_x, fish_y)
                normalized_distance = int((distance / np.sqrt(width ** 2 + height ** 2)) * 255)

                if idx in prev_positions:
                    prev_x, prev_y = prev_positions[idx]
                    velocity = calculate_distance(prev_x, prev_y, fish_x, fish_y)
                    velocity_norm = int((velocity / np.sqrt(width ** 2 + height ** 2)) * 255) % 256
                else:
                    velocity_norm = 0
                prev_positions[idx] = (fish_x, fish_y)

                pixel_variation = int(np.sum(mask) % 256)  # 🔹 Convert NumPy type to Python int

                processed_value = int((normalized_distance + int(angle) % 360) % 256)  # 🔹 Convert to int
                processed_value = int((processed_value ^ velocity_norm ^ pixel_variation) % 256)  # 🔹 Ensure XOR works

                entity_data.append(f"{processed_value:08b}")

                cv2.circle(frame, (fish_x, fish_y), 5, (0, 255, 0), -1)
                cv2.line(frame, (ref_x, ref_y), (fish_x, fish_y), (0, 255, 255), 2)

        if len(entity_data) == 2:
            if frame_count % np.random.randint(5, 40) == 0:
                binary_sequence_fish1 += entity_data[0]
                binary_sequence_fish2 += entity_data[1]

    frame_count += 1
    cv2.imshow('Goldfish Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

final_binary_sequence = ''.join(
    a + b if np.random.randint(0, 2) else b + a for a, b in zip(binary_sequence_fish1, binary_sequence_fish2))

# Apply LFSR scrambling
scrambled_sequence = lfsr_scramble(final_binary_sequence)

with open("output2.txt", "w") as f:
    f.write(scrambled_sequence)
