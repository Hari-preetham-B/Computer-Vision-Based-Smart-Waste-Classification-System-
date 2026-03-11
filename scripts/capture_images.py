import cv2
import os

category = "Dry"  # Change to Wet or Metal when needed

save_dir = f"data/train/{category}"
os.makedirs(save_dir, exist_ok=True)

cap = cv2.VideoCapture(0)

print("Press SPACE to capture image")
print("Press ESC to exit")

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture", frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break

    elif key == 32:  # SPACE
        filename = os.path.join(save_dir, f"{category}_{count}.jpg")
        cv2.imwrite(filename, frame)
        print("Saved:", filename)
        count += 1

cap.release()
cv2.destroyAllWindows()
