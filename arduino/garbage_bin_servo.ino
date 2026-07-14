#include <Servo.h>

Servo dryServo;
Servo wetServo;
Servo metalServo;

const int CLOSED = 0;
const int OPEN = 90;
const unsigned long OPEN_TIME = 10000;

bool busy = false;
unsigned long startTime = 0;
Servo* activeServo = nullptr;

void setup() {

  Serial.begin(115200);

  dryServo.attach(9);
  wetServo.attach(10);
  metalServo.attach(11);

  dryServo.write(CLOSED);
  wetServo.write(CLOSED);
  metalServo.write(CLOSED);
}

void loop() {

  if (busy) {

    if (millis() - startTime >= OPEN_TIME) {

      activeServo->write(CLOSED);

      busy = false;
      activeServo = nullptr;

    }

    return;
  }

  if (Serial.available()) {

    char cmd = Serial.read();

    if (cmd == 'D') triggerServo(dryServo);
    else if (cmd == 'W') triggerServo(wetServo);
    else if (cmd == 'M') triggerServo(metalServo);
  }
}

void triggerServo(Servo &s) {

  s.write(OPEN);

  activeServo = &s;
  startTime = millis();

  busy = true;
}
