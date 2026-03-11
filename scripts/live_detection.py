import cv2
import torch
import torch.nn as nn
import time
import serial
from collections import deque
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Serial communication with Arduino
ser = serial.Serial("COM3",115200,timeout=0.1)
time.sleep(2)

# Human detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Load model
CHECKPOINT="models/garbage_model.pth"
device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint=torch.load(CHECKPOINT,map_location=device)
classes=checkpoint["classes"]

model=models.mobilenet_v3_small(weights=None)
model.classifier[3]=nn.Linear(model.classifier[3].in_features,len(classes))
model.load_state_dict(checkpoint["model_state"])
model.to(device)
model.eval()

transform=transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485,0.456,0.406),
                         (0.229,0.224,0.225))
])

def preprocess(frame):
    img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img=Image.fromarray(img)
    img=transform(img)
    return img.unsqueeze(0).to(device)

prediction_buffer=deque(maxlen=10)
last_sent=0

CONF_THRESH=0.80
COOLDOWN=4
EDGE_THRESH=0.015

cap=cv2.VideoCapture(0)

while True:

    ret,frame=cap.read()
    if not ret:
        break

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    humans,_=hog.detectMultiScale(gray,
                                  winStride=(8,8),
                                  padding=(8,8),
                                  scale=1.05)

    if len(humans)>0:
        prediction_buffer.clear()
        cv2.putText(frame,"Human detected - paused",
                    (10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.imshow("Garbage Classifier",frame)
        if cv2.waitKey(1)&0xFF==27:
            break
        continue

    h,w,_=frame.shape
    box=350
    x1,y1=w//2-box//2,h//2-box//2
    x2,y2=x1+box,y1+box

    roi=frame[y1:y2,x1:x2]

    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

    roi_gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(roi_gray,50,150)
    edge_density=np.sum(edges>0)/edges.size

    if edge_density<EDGE_THRESH:
        prediction_buffer.clear()
        cv2.putText(frame,"No object present",
                    (10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.imshow("Garbage Classifier",frame)
        if cv2.waitKey(1)&0xFF==27:
            break
        continue

    inp=preprocess(roi)

    with torch.no_grad():
        out=model(inp)
        probs=torch.softmax(out,dim=1)
        conf,pred=torch.max(probs,1)

    label=classes[pred.item()]
    confidence=conf.item()

    if confidence>=CONF_THRESH:
        prediction_buffer.append(label)
    else:
        prediction_buffer.clear()

    if len(prediction_buffer)==prediction_buffer.maxlen:

        stable=max(set(prediction_buffer),
                   key=prediction_buffer.count)

        now=time.time()

        if now-last_sent>COOLDOWN:

            if stable=="Dry":
                ser.write(b'D')

            elif stable=="Wet":
                ser.write(b'W')

            elif stable=="Metal":
                ser.write(b'M')

            print(stable,"bin opened")

            last_sent=now
            prediction_buffer.clear()

    text=f"{label} ({confidence*100:.1f}%)"

    cv2.putText(frame,text,(10,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,0),2)

    cv2.imshow("Garbage Classifier",frame)

    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
