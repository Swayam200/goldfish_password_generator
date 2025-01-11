import cv2
import numpy as np

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_angle(x1, y1, x2, y2):
    return np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi)

video = cv2.VideoCapture("GoldFishRandom.mp4")

frame_count = 0
random_sequence = ""

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

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M['m00'] != 0:
            fish_x = int(M['m10'] / M['m00'])
            fish_y = int(M['m01'] / M['m00'])

            # Calculate distance and angle
            distance = calculate_distance(ref_x, ref_y, fish_x, fish_y)
            angle = calculate_angle(ref_x, ref_y, fish_x, fish_y)

            # Normalize distance
            normalized_distance = int((distance / np.sqrt(width**2 + height**2)) * 255)
            processed_value = (normalized_distance + int(angle) % 360) % 256

            if frame_count % np.random.randint(10, 30) == 0:  # Randomize sampling
                random_sequence += f"{processed_value % 100:02}"  # Concatenate two-digit value

            cv2.circle(frame, (fish_x, fish_y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (ref_x, ref_y), 5, (255, 0, 0), -1)
            cv2.line(frame, (ref_x, ref_y), (fish_x, fish_y), (0, 255, 255), 2)

    frame_count += 1
    cv2.imshow('Goldfish Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

# Print the generated random sequence
print("Generated Random Sequence:")
print(random_sequence)
