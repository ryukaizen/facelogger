<p align="center">
  <img src="https://i.imgur.com/8SHF1Eh.png" width="250" />
</p>

<h1 align="center">Facelogger</h1>

<p align="center">
  <strong>A face recognition check-in module based on AI-Thinker's ESP32-CAM</strong>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/ESP32-CAM-red.svg" alt="ESP32-CAM">
    <img src="https://img.shields.io/badge/Arduino-IDE-teal.svg" alt="Arduino IDE">
    <img src="https://img.shields.io/badge/face__recognition-1.3.0-blue.svg" alt="face_recognition">
    <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/OpenCV-4.5+-green.svg" alt="OpenCV">
    <img src="https://img.shields.io/badge/MongoDB-4.4+-green.svg" alt="MongoDB">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

This project combines the functionalities of ESP32-CAM with Python's face-recognition library for detecting and identifying faces in real time.

## 📚 Table of Contents

- [🛠 ESP32 Board Setup](#-esp32-board-setup)
- [🔌 Hardware Setup](#-hardware-setup)
- [💻 ESP32-CAM Programming](#-esp32-cam-programming)
- [📥 Installation](#-installation)
- [🚀 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🛠 ESP32 Board Setup

Before proceeding with the hardware connection, ensure your Arduino IDE is properly configured for ESP32 development:

1. Configure Additional Board Manager URL:
   - Navigate to "File" > "Preferences" (on macOS, "Arduino" > "Preferences").
   - Locate the "Additional Boards Manager URLs" field.
   - Click the icon next to the field to open the input window.
   - Add the following URL on a new line:
     ```
     https://dl.espressif.com/dl/package_esp32_index.json
     ```
   - Click "OK" to save the changes and close the Preferences window.

2. Install ESP32 Board Support:
   - Open the Boards Manager by selecting "Tools" > "Board" > "Boards Manager".
   - In the search bar, type "esp32".
   - Locate "esp32 by Espressif Systems" and click "Install".
   - After installation, close the Boards Manager.

3. Select ESP32 Board:
   - Go to "Tools" > "Board" and select your specific ESP32 board model from the list.

After completing these steps, your Arduino IDE will be ready for ESP32 development.

## 🔌 Hardware Setup

### ESP32-CAM and FTDI Programmer Connection

Before programming, connect your ESP32-CAM to an FTDI programmer as follows:

<p align="center">
  <img src="https://i.imgur.com/weNGvc8.png" alt="ESP32-CAM and FTDI Connection Diagram" width="500">
</p>

<div align="center">

| ESP32-CAM | FTDI Programmer |
|:---------:|:---------------:|
|    GND    |       GND       |
|    5V     |       VCC       |
|    U0R    |       TX        |
|    U0T    |       RX        |
|   GPIO0   |       GND       |

</div>

> ⚠️ **Important:** Short GPIO0 to GND to enter programming mode. Remove this connection after programming.

### OLED Display Connection

After programming:

1. Remove the GPIO0 to GND connection.
2. Connect OLED GND to ESP32-CAM GND.
3. Connect OLED VCC to ESP32-CAM 3V.
4. Press the reset button on ESP32-CAM.

The OLED should display "ESP32 Started!" 🎉

## 💻 ESP32-CAM Programming

1. Navigate to the `aithinker/src/` folder.
2. Open `esp32cam.ino` in Arduino IDE.
3. Add your Wi-Fi credentials:

```cpp
static const char* WIFI_SSID = "your_wifi_name";
static const char* WIFI_PASS = "your_wifi_password";
```

4. Upload the code to ESP32-CAM (ensure GPIO0 is connected to GND).
5. After uploading, disconnect GPIO0 from GND and reset the board.
6. Open the Serial Monitor to get the generated link.

## 📥 Installation

1. Clone this repository:

```bash
git clone https://github.com/ryukaizen/facelogger.git
cd facelogger
```

2. Set up the ESP32-CAM as described in the [Hardware Setup](#-hardware-setup) section.
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Before running the project, you need to set up some key variables in the `main.py` file:

```python
# In main.py

# Replace this with your own ESP32-CAM generated link (check aithinker folder)
ESP32_CAM_URL = 'http://192.168.52.160/640x480.jpg'

# Replace this with your own Google Form URL
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz/formResponse"

# Replace this with your own MongoDB URL
MONGODB_URL = 'mongodb://localhost:27017/'

# Inspect element on the Google Form and find the entry name ID and entry time ID
ENTRY_NAME_ID = 'entry.123456789' 
ENTRY_TIME_ID = 'entry.987654321'
```

Ensure you replace these placeholder values with your actual URLs and IDs:

1. `ESP32_CAM_URL`: The URL generated by your ESP32-CAM. You can find this in the Serial Monitor after uploading the code to your ESP32-CAM.

2. `GOOGLE_FORM_URL`: The URL of your Google Form where names and timestamps will be logged.

3. `MONGODB_URL`: The URL of your MongoDB instance.

4. `ENTRY_NAME_ID` and `ENTRY_TIME_ID`: These are specific to your Google Form. To find these:
   - Open your Google Form in a web browser
   - Right-click and select "Inspect" or "Inspect Element"
   - Look for input fields with names like "entry.123456789"
   - The number after "entry." is your ID

> ⚠️ **Note:** Keep your Google Form URL and entry IDs private to prevent unauthorized access to your logging data.

## 🚀 Usage

1. Program the ESP32-CAM and note the generated URL.
2. Run the Python script:

```bash
python3 main.py
```
3. The system will now detect and recognize faces using the ESP32-CAM feed.

>⚠️ Note: For the system to work properly, both the ESP32-CAM and the computer running the Python script must be on the same local network.

## 🤝 Contributing

As always, contributions are welcome! Feel free to submit a PR. You can reach out to me on [Telegram](https://telegram.me/ryukaizen).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ryukaizen">ryukaizen</a>
</p>
