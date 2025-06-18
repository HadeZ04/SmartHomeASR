
# 🏠 Smart Home Assistant

A Raspberry Pi-based voice-controlled smart home assistant with support for:
- Voice command recognition (via TFLite)
- GPIO control (lights, fans, PIR sensor, DHT11)
- Music playback (via VLC)
- GUI control panel (Tkinter)
## DEMO
[![Xem demo]([https://youtu.be/KYMTGdMLUcA)](https://youtu.be/KYMTGdMLUcA))
---

## 🚀 Features
- Voice recognition using TensorFlow Lite + Keras CTC
- Real-time GPIO hardware control: LED, Fan, PIR sensor, Servo
- Espeak TTS for voice feedback
- Smart GUI dashboard with button controls
- Media playback and volume control

---

## 📦 Project Structure
```
smart_home_assistant/
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── assets/                # Icons, mic image
├── model/                 # TFLite voice model
├── vocab/                 # Character vocabulary file
├── media/                 # Music or video playback files
├── smart_home/            # Main package
│   ├── __init__.py
│   ├── audio.py
│   ├── voice.py
│   ├── gpio_control.py
│   ├── utils.py
│   ├── gui.py
│   ├── config.py
│   └── command_map.py
```

---

## 🛠️ Installation
```bash
sudo apt update && sudo apt install python3-pip espeak libasound-dev -y
pip3 install -r requirements.txt
```

---

## 🧪 Run the Project
```bash
python3 main.py
```
Then type `main` to start voice mode or `test` to test via keyboard.

---

## 🎤 Hardware Used
- Raspberry Pi 3/4/5
- USB Microphone
- DHT11 Sensor
- PIR Motion Sensor
- Servo Motor
- Relays for Fan/Light
- I2C LCD (optional)

---

## 📋 Notes
- `mic.jpeg` should be placed inside `/assets`
- `fixed_model.tflite` and `vocab.txt` paths should match `config.py`
- Run with `sudo` if needed to access GPIO

---

## 🤖 Credits
Built using Python, TensorFlow, Keras, and Raspberry Pi GPIO. Speech processing powered by Espeak.

---

## 📜 License
MIT License © 2025
