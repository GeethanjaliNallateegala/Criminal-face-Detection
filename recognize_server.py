# ============================================================
#   recognize_server.py — Persistent Python Server
#   Starts ONCE, stays running, processes requests instantly
# ============================================================
#
#  How it works:
#  1. Loads face_recognition library ONCE at startup
#  2. Loads all dataset photos ONCE at startup
#  3. Waits for Java to send image paths (one per line)
#  4. Compares face and prints result back to Java
#  5. Repeats steps 3-4 forever until Java sends "EXIT"
#
#  This way face_recognition loads only once = no freezing!

import sys
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
from PIL import Image
import face_recognition

def load_dataset(dataset_path="dataset/"):
    known_encodings = []
    known_names     = []

    if not os.path.exists(dataset_path):
        return known_encodings, known_names

    for filename in os.listdir(dataset_path):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        filepath = os.path.join(dataset_path, filename)
        try:
            pil_img   = Image.open(filepath).convert("RGB")
            img_array = np.array(pil_img, dtype=np.uint8)
            encodings = face_recognition.face_encodings(img_array)
            if len(encodings) == 0:
                continue
            known_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0]
            name = name.replace("_", " ").title()
            known_names.append(name)
        except Exception:
            continue

    return known_encodings, known_names


def recognize(image_path, known_encodings, known_names):
    if not os.path.exists(image_path):
        return "Unknown"

    try:
        pil_img    = Image.open(image_path).convert("RGB")
        webcam_img = np.array(pil_img, dtype=np.uint8)

        # Upscale if too small
        h, w = webcam_img.shape[:2]
        if h < 100 or w < 100:
            pil_img    = pil_img.resize((200, 200), Image.LANCZOS)
            webcam_img = np.array(pil_img, dtype=np.uint8)

        # Try to encode face
        encodings = face_recognition.face_encodings(webcam_img)

        if len(encodings) == 0:
            # Force encode the whole crop
            face_locs = [(0, webcam_img.shape[1],
                          webcam_img.shape[0], 0)]
            encodings = face_recognition.face_encodings(
                webcam_img, known_face_locations=face_locs
            )

        if len(encodings) == 0:
            return "Unknown"

        webcam_encoding = encodings[0]

        matches   = face_recognition.compare_faces(
            known_encodings, webcam_encoding, tolerance=0.55
        )
        distances = face_recognition.face_distance(
            known_encodings, webcam_encoding
        )

        if len(distances) == 0:
            return "Unknown"

        best_index = np.argmin(distances)
        best_score = distances[best_index]

        if matches[best_index] and best_score < 0.55:
            return known_names[best_index]
        else:
            return "Unknown"

    except Exception:
        return "Unknown"


# ── MAIN SERVER LOOP ─────────────────────────────────────────
if __name__ == "__main__":

    # Load dataset ONCE at startup
    known_encodings, known_names = load_dataset("dataset/")

    # Tell Java we are ready
    print("READY", flush=True)

    # Keep reading image paths from Java forever
    for line in sys.stdin:
        line = line.strip()

        # Exit command from Java
        if line == "EXIT":
            break

        if not line:
            continue

        # Recognize the face and send result back to Java
        result = recognize(line, known_encodings, known_names)
        print(result, flush=True)  # Java reads this!