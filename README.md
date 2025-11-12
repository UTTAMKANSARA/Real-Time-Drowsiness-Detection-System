# Real-Time Drowsiness Detection System

This is an advanced, multi-metric drowsiness detection system built in Python.
It uses a webcam and AI-powered facial analysis to monitor a driver for a *pattern* of fatigue, not just a single symptom.

The system intelligently tracks four key biometric indicators in real-time:

1.  **Micro-Sleeps** (Eyes closed for too long, using Eye Aspect Ratio - EAR)
2.  **Yawning** (Mouth open wide, using Mouth Aspect Ratio - MAR)
3.  **Head Nods** (Sudden head drop, using 3D Head Pose Estimation)
4.  **Fatigue/Staring** (A low blink-rate, using Blinks Per Minute - BPM)

When a dangerous pattern is detected, the system triggers a multi-stage alert, including a loud audio alarm,
an on-screen visual warning, and an emergency SMS alert via the Twilio API.

This repository contains two versions of the application:

1.  **Desktop GUI App:** A standalone application built with Tkinter that runs in a desktop window.
2.  **Web App:** A browser-based version powered by a Django web server.
-----

## 🚀 Core Features

  * **Multi-Metric Analysis:** Tracks eyes, mouth, head, and blink rate simultaneously for high accuracy.
  * **AI-Powered:** Uses Google's **MediaPipe** for a fast, lightweight, and accurate 468-point facial landmark detection.
  * **Dual Version:** Includes both a **Tkinter** desktop app and a **Django** web app.
  * **Multi-Stage Alert:** Provides a visual (on-screen text), audio (Pygame sound), and remote (Twilio SMS) alert.

-----

## 🔧 Technology Stack

| Category | Technology | Purpose |

**Language** | **Python 3.11+** | The core language for the entire project. 
**AI / Computer Vision** | **MediaPipe** | The AI "engine" for real-time facial landmark detection. 
**OpenCV** | For capturing the webcam feed, image processing, and 3D pose math. 
**Desktop GUI**| **Tkinter** | Python's built-in library for the standalone desktop GUI. 
**Pillow (PIL)** | A bridge library to convert OpenCV images into a format Tkinter can display. 
**Web GUI** | **Django** | A high-level Python framework used to build the web-server version. 
**Alerting** | **Pygame** | Used to load and play the `.wav` audio alarm. 
**Twilio** | Cloud communication platform used to send SMS alerts. 
**Data Handling** | **NumPy & SciPy**| For high-performance numerical calculations (EAR, MAR, etc.). 


-----

## 🛠️ Setup and Installation (For a New PC)

Follow these steps to get the project running on a new Windows machine.

### 1\. Prerequisites

  * **Python 3.11** or **Python 3.12** (must be the **64-bit** version).
  * **Git** for cloning the repository.

### 2\. Clone the Repository

```bash
git clone https://github.com/UTTAMKANSARA/Real-Time-Drowsiness-Detection-System.git
cd Real-Time-Drowsiness-Detection-System
```

### 3\. Create the Virtual Environment

This creates an isolated "bubble" for your project's packages.

```bash
# Create the virtual environment
py -3.11 -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

> **PowerShell Note:** If you get an error, you may need to run this command once (as Administrator) to allow scripts:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4\. Install Dependencies

All required packages are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5\. Add Alert Sound

The project needs an alarm sound to play.

1.  Create a new folder in the main project directory named `static`.
2.  Place an alarm sound file inside this folder and name it **`alarm.wav`**.

### 6\. Configure Secret Keys (for SMS)

The `.gitignore` file correctly blocks your secret API keys. A new user must create their own.

1.  In the main project folder, create a new file named **`config.py`**.

2.  Open it and add your Twilio credentials (you can get these from your Twilio account):

    ```python
    # config.py

    # --- TWILIO SMS CONFIGURATION ---
    TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID_HERE"
    TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"
    TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio Phone Number
    MY_PHONE_NUMBER = "+919876543210" # Your personal phone number
    ```

-----



For the Web App (settings.py)

Navigate to the drowsy_project folder.

Open the file settings.py.

Scroll to the very bottom of the file.

Add your Twilio credentials (you can copy/paste from config.py):

```Python

  # drowsy_project/settings.py

  # --- TWILIO SMS CONFIGURATION ---
  TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID_HERE"
  TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"
  TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio Phone Number
  MY_PHONE_NUMBER = "+919876543210" # Your personal phone number
````
-----


## 💻 How to Run

You can run either the Desktop or the Web version.

### Option 1: Desktop GUI App (Recommended)

This is the standalone application with all features.

1.  Make sure your virtual environment is active (you see `(venv)`).

2.  Run the `app_desktop.py` script:

    ```bash
    python app_desktop.py
    ```

A Tkinter window will open, your webcam will activate, and the system will be live.

### Option 2: Web Browser Version

This version uses Django to serve the video feed to your browser.

1.  Make sure your virtual environment is active.
2.  Initialize the Django database:
    ```bash
    python manage.py migrate
    ```
3.  Start the Django web server:
    ```bash
    python manage.py runserver
    ```
4.  Open your web browser and go to: **`http://127.0.0.1:8000/`**

-----
      * Replace the `if/else` logic block with a single line:
        `prediction = my_model.predict([features])`
      * This replaces all the manual thresholds with a single, intelligent prediction from your custom-trained AI.
