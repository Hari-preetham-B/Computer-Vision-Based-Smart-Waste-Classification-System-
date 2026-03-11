# Computer-Vision-Based-Smart-Waste-Classification-System-
This project is an automated waste segregation system using computer vision and machine learning.
The system detects garbage items using a webcam and classifies them into three categories:
- Dry Waste
- Wet Waste
- Metal Waste
Based on the prediction, a command is sent to an Arduino which opens the corresponding bin using a servo motor.
---
## Technologies Used
- Python
- PyTorch
- OpenCV
- Arduino
- Serial Communication
---
## Project Structure
```
scripts/
    capture_images.py
    train_model.py
    live_detection.py
data/
    train/
        Dry/
        Wet/
        Metal/
models/
    garbage_model.pth
arduino/
    garbage_bin_servo.ino
```
---
## How the System Works
1. The webcam captures the image.
2. The trained CNN model (MobileNetV3) classifies the waste item.
3. Python sends a command (`D`, `W`, or `M`) to the Arduino.
4. The Arduino opens the corresponding waste bin using a servo motor.
---
## Installation
Clone the repository:
```
git clone <your-repo-link>
cd <repo-name>
```
Install dependencies:

```
pip install -r requirements.txt
```
---
## Training the Model
```
python scripts/train_model.py
```
The trained model will be saved in:
```
models/garbage_model.pth
```
---
## Running Live Detection
```
python scripts/live_detection.py
```
---
## Hardware Used
- Arduino Uno
- Servo Motors
- Webcam
- Laptop
---
## Future Improvements
- Improve model accuracy with larger datasets
- Deploy on Raspberry Pi
- Add IoT monitoring for bin levels
