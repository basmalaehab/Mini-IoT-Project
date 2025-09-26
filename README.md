# Mini-IoT-Project: Smart Attendance System


## 1. Project Overview

The Smart Attendance System is designed for universities and schools to solve common issues with manual attendance. Manual attendance is often time-consuming, prone to human errors, and makes data analysis difficult. This system automates attendance tracking, ensuring accurate records and easier analysis.

![Smart Attendance](https://miro.medium.com/v2/resize:fit:720/format:webp/1*REkyBlBoacF-qn65zhIzVg.jpeg)

---

## 2. How It Works

1. **Detection**: An ultrasonic sensor detects when a person is standing in front of the system.
2. **Activation**: Upon detection, the camera activates and initiates the face recognition process.
3. **Recognition**: The system compares the captured face against a database of enrolled students:
   - If recognized, the student's name and timestamp are displayed, indicating successful attendance.
   - If not recognized, the system displays "Unknown".
4. **Data Transmission**: Attendance data is transmitted via the MQTT protocol to the university server.
5. **Record Keeping**: The system records the student's name and time of entry in a CSV file for record-keeping.

---

## 3. Installation

For Raspberry Pi: Follow the guide: [Face Identification on Raspberry Pi](https://core-electronics.com.au/guides/face-identify-raspberry-pi/)

For Ubuntu:
```bash
sudo apt update
sudo apt install -y build-essential cmake python3 python3-dev python3-pip \
                    libgtk-3-dev libboost-all-dev git
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake ..
cmake --build .
cd ..
sudo python3 setup.py install
sudo pip3 install face_recognition opencv-python numpy
```
## Verify Installation:
```bash

python3
```
Then in the Python shell:

```bash

import dlib
import face_recognition
import cv2
import numpy as np

print(dlib.__version__)
print(face_recognition.__version__)
print(cv2.__version__)
print(np.__version__)
```
