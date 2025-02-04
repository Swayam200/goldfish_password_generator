import cv2
import numpy as np


def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_angle(x1, y1, x2, y2):
    return np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi)


video = cv2.VideoCapture('C:\\Users\\abhin\\Downloads\\Project\\Project\\1.mp4')

frame_count = 0
binary_sequence_fish1 = ""
binary_sequence_fish2 = ""
prev_positions = {}  # Store previous positions

while True:
    ret, frame = video.read()
    if not ret:
        break

    height, width, _ = frame.shape
    ref_x, ref_y = width // 2, height // 2  # Static reference

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

                # Calculate velocity as additional entropy
                if idx in prev_positions:
                    prev_x, prev_y = prev_positions[idx]
                    velocity = calculate_distance(prev_x, prev_y, fish_x, fish_y)
                    velocity_norm = int((velocity / np.sqrt(width ** 2 + height ** 2)) * 255) % 256
                else:
                    velocity_norm = 0
                prev_positions[idx] = (fish_x, fish_y)

                # Add pixel noise entropy
                pixel_variation = np.sum(mask) % 256

                # Combine values with velocity and pixel noise
                processed_value = (normalized_distance + int(angle) % 360) % 256
                processed_value = (processed_value ^ velocity_norm ^ pixel_variation) % 256
                entity_data.append(f"{processed_value:08b}")

                cv2.circle(frame, (fish_x, fish_y), 5, (0, 255, 0), -1)
                cv2.line(frame, (ref_x, ref_y), (fish_x, fish_y), (0, 255, 255), 2)

        if len(entity_data) == 2:
            if frame_count % np.random.randint(5, 40) == 0:  # Randomized sampling interval
                binary_sequence_fish1 += entity_data[0]
                binary_sequence_fish2 += entity_data[1]

    frame_count += 1
    cv2.imshow('Goldfish Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

# Splice the two binary sequences together with randomized order
final_binary_sequence = ''.join(
    a + b if np.random.randint(0, 2) else b + a for a, b in zip(binary_sequence_fish1, binary_sequence_fish2))

with open("output1.txt", "w") as f:
    f.write(final_binary_sequence)
