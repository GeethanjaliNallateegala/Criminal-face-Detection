# Criminal Face Detection System

## Overview

This is a hybrid desktop application that performs real-time criminal face detection using:

- Java (OpenCV) for camera handling and UI
- Python (`face_recognition`) for face matching

The system captures faces from a live webcam feed and compares them against a dataset of known criminals.

---

## How It Works

### Concept

- Java acts as the controller (camera + UI)
- Python acts as the recognizer (face matching)

Think of it as:
- Java = Security Guard
- Python = Detective

---

## Execution Flow

### Step 1: Start Application

- Run `run.bat`
- Java and Python processes start
- Webcam initializes
- Java waits for Python to return `"READY"`

---

### Step 2: Load Dataset (Python)

- Python scans the `dataset/` folder
- Converts each face into a 128-dimensional encoding
- Stores all encodings in memory
- Sends `"READY"` signal

---

### Step 3: Face Detection (Java)

- Captures frames continuously from webcam
- Uses Haar Cascade classifier to detect faces
- Identifies face regions as rectangles

---

### Step 4: Face Cropping

- Draws bounding box on detected face
- Every 5th frame:
  - Crops face region
  - Saves as `temp_face.jpg`

---

### Step 5: Communication

- Java sends `temp_face.jpg` path to Python via stdin

---

### Step 6: Face Recognition (Python)

- Converts face into encoding
- Compares with dataset encodings
- If match (threshold < 0.55):
  - Returns name
- Else:
  - Returns `"Unknown"`

---

### Step 7: Display Result

- Java displays result on screen:
  - Red: Criminal detected
  - Green: No match

---

### Step 8: Continuous Loop

- Steps repeat in real-time
- Press `Q` or `Esc` to exit
- Cleans temporary files and shuts down processes

---

## Project Structure

| File | Description |
|------|------------|
| `run.bat` | Starts the application |
| `Main.java` | Controls application flow |
| `FaceDetector.java` | Detects faces in frames |
| `haarcascade_frontalface_default.xml` | Pre-trained face detection model |
| `FaceRecognizer.java` | Handles Java–Python communication |
| `recognize_server.py` | Performs face recognition |
| `dataset/` | Stores criminal images |
| `temp_face.jpg` | Temporary cropped face image |
| `pom.xml` | Maven configuration file |

---

## Key Components

### Face Detection

- Uses Haar Cascade classifier
- Converts image to grayscale
- Applies histogram equalization
- Detects faces with:
  - Scale factor: 1.1
  - Min neighbors: 8

---

### Face Recognition

- Uses `face_recognition` (dlib-based)
- Converts faces into 128D vectors
- Matching based on distance threshold = 0.55

---

### Java–Python Integration

- Python runs as a persistent background process
- Communication via stdin/stdout
- Avoids delay from repeated initialization

---

## Dataset

- Located in `dataset/`
- Each image represents one person
- Filename = Person name

### Example

```
Praneeth.jpg → "Praneeth"
john_doe.jpg → "John Doe"
```

---

## Adding a New Criminal

1. Take a clear front-facing image
2. Rename file as desired display name
3. Place in `dataset/`
4. Restart the application

---

## Requirements

- Java 11
- Maven
- Python 3
- OpenCV (via Maven dependency)
- Python libraries:
  - face_recognition
  - dlib
  - numpy

---

## Build and Run

```bash
mvn compile
```

Run using:

```bash
run.bat
```

---

## System Summary

Java captures webcam frames, detects faces, and sends cropped images to Python.  
Python compares them with stored encodings and returns a name or "Unknown".

---

## Architecture

Java (OpenCV) → Face Detection → Image Crop → Python (face_recognition) → Match Result → Display

---

## Notes

- Recognition runs every 5th frame for performance
- Python process runs continuously to avoid delays
- System works best with clear, front-facing images
