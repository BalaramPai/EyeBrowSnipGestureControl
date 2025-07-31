# Eyebrow-Based Screenshot Capture with MediaPipe

This Python project uses MediaPipe FaceMesh to detect facial landmarks and captures a screenshot when the left eyebrow
 is raised. It’s a simple, hands-free screenshot system powered by webcam-based facial gesture detection.

## Features

* Real-time facial landmark tracking using MediaPipe
* Detects left eyebrow raise by measuring distance between specific facial landmarks
* Automatically captures a screenshot when the eyebrow raise gesture is recognized
* Displays FPS for performance monitoring
* Works with multiple faces (can be adapted for multi-user)

## How It Works

The script calculates the vertical distance between two face mesh landmarks:

* Landmark 23: Left eyebrow
* Landmark 66: Left eye

If the distance between them increases beyond a certain threshold (for example, 41 pixels), it's interpreted as an
eyebrow raise. When the eyebrow lowers again, a screenshot is captured.

The action is only triggered after the eyebrow is lowered back, to prevent repeated screenshots.

## Project Structure

```
eyebrow-screenshot/
├── FaceMeshModule.py      # Custom MediaPipe wrapper for face mesh
├── main.py                # Main script (your provided code)
├── README.md              # This file
```

## Requirements

Install the following Python libraries:

```
pip install opencv-python mediapipe pyautogui
```

If using a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate      # For macOS/Linux
venv\Scripts\activate         # For Windows
pip install -r requirements.txt
```

Ensure FaceMeshModule.py is present and correctly imported in your project.

## Screenshots

Saved screenshots will appear in the same directory as the script with names like:

```
snap_1722479250.png
snap_1722479302.png
```

## Testing

1. Run the script:

   ```
   python main.py
   ```

2. Look into your webcam.

3. Raise your left eyebrow (relative to your face on screen, this is typically on the right side of the image since
it's mirrored).

4. Lower it back — a screenshot should be saved, and "screenshot taken" printed in the terminal.

## Customization

To adjust sensitivity:

```
if length >= 41:
```

You can fine-tune this threshold to better suit your face or camera setup.

You can also add a cooldown timer if you want to avoid frequent screenshots. This logic can be added easily inside the
 existing loop.

## Author

Balaram Pai H

---
