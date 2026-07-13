# 🗑️ Computer Vision-Based Smart Waste Classification System

An end-to-end automated waste segregation system using **MobileNetV3 deep learning** and **Arduino-based hardware actuation**. A webcam captures waste items in real time, a trained CNN classifies them into 3 categories, and servo motors physically sort them into the correct bin — no human involvement needed.

---

## 🎯 Model Performance

| Class | Accuracy |
|-------|----------|
| Dry Waste | ~85–90% |
| Wet Waste | ~85–90% |
| Metal Waste | ~85–90% |

- **Architecture:** MobileNetV3-Small (pretrained on ImageNet, fine-tuned)
- **Dataset:** 3,000 images across 3 classes (1,000 per class)
- **Inference:** Real-time on CPU, < 200ms latency per frame
- **Training:** PyTorch, 10 epochs, CrossEntropyLoss, Adam optimizer

---

## 🧠 How It Works

```
Webcam Feed → MobileNetV3 CNN → Classification (Dry / Wet / Metal)
                                        ↓
                          PySerial Command (D / W / M)
                                        ↓
                         Arduino Uno → Servo Motor → Correct Bin Opens
```

1. `live_detection.py` captures frames from the webcam
2. The trained model (`garbage_model.pth`) classifies each frame
3. Python sends a single character command over serial (`D`, `W`, or `M`)
4. Arduino reads the command and rotates the corresponding servo motor

---

## 🗂️ Project Structure

```
├── scripts/
│   ├── capture_images.py       # Webcam image capture for dataset building
│   ├── train_model.py          # MobileNetV3 training script
│   └── live_detection.py       # Real-time detection + Arduino serial control
├── data/
│   └── train/
│       ├── Dry/                # ~1000 images
│       ├── Wet/                # ~1000 images
│       └── Metal/              # ~1000 images
├── models/
│   └── garbage_model.pth       # Trained model weights (see below to download)
├── arduino/
│   └── garbage_bin_servo.ino   # Arduino sketch for servo control
├── requirements.txt
└── README.md
```

---

## 🔧 Hardware Requirements

| Component | Purpose |
|-----------|---------|
| Arduino Uno | Microcontroller for servo control |
| 3× Servo Motors | Opens each waste bin (Dry / Wet / Metal) |
| USB Webcam | Real-time waste capture |
| Laptop / PC | Runs Python inference |
| USB Cable | Arduino ↔ Python serial communication |

### Wiring

- Servo 1 (Dry) → Arduino Pin 9
- Servo 2 (Wet) → Arduino Pin 10
- Servo 3 (Metal) → Arduino Pin 11
- All servos: VCC → 5V, GND → GND

---

## ⚙️ Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/Hari-preetham-B/Computer-Vision-Based-Smart-Waste-Classification-System-.git
cd Computer-Vision-Based-Smart-Waste-Classification-System-
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the dataset

Dataset used: [Kaggle Garbage Classification Dataset](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)

Place images into:
```
data/train/Dry/
data/train/Wet/
data/train/Metal/
```

### 4. Train the model

```bash
python scripts/train_model.py
```

Model weights saved to `models/garbage_model.pth`

### 5. Upload Arduino sketch

- Open `arduino/garbage_bin_servo.ino` in Arduino IDE
- Select board: **Arduino Uno**
- Select correct COM port
- Upload

### 6. Run live detection

```bash
python scripts/live_detection.py
```

> ⚠️ Make sure Arduino is connected before running. Update the `serial_port` variable in `live_detection.py` to match your COM port (e.g., `COM3` on Windows, `/dev/ttyUSB0` on Linux).

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Deep Learning | PyTorch, MobileNetV3 |
| Computer Vision | OpenCV |
| Hardware Control | Arduino Uno, PySerial |
| Language | Python 3.x, C++ (Arduino) |

---

## 🚀 Future Improvements

- [ ] Expand dataset to 5+ waste categories
- [ ] Deploy model on Raspberry Pi for standalone operation
- [ ] Add IoT dashboard for bin fill-level monitoring
- [ ] Improve accuracy with data augmentation

---

## 👤 Author

**Bade Hari Preetham**
B.E. AI & ML — CMR Institute of Technology, Bengaluru
[GitHub](https://github.com/Hari-preetham-B) · [LinkedIn](https://linkedin.com/in/hari-preetham-b)
