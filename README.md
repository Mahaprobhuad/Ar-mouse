# AR Mouse

AR Mouse is a Python webcam-based pointer control prototype created as a college mini project. It uses MediaPipe Face Mesh to detect the nose tip and maps its position to screen coordinates with PyAutoGUI.

> Note: Despite the original description in the source code, this project does not perform gaze tracking. It uses the face-mesh nose landmark as a head-position cursor input.

## Features

- Webcam face detection
- Nose landmark tracking
- On-screen calibration for screen-space mapping
- Real-time mouse pointer movement
- Mirror-flipped OpenCV preview

## Requirements

- Python 3.8 or later
- A webcam
- A desktop environment
- Python packages listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Mahaprobhuad/Ar-mouse.git
   cd Ar-mouse
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   **Windows:**

   ```bash
   .venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

## Usage

Run the script:

```bash
python main.py
```

The program first opens a calibration window and asks you to look at the:

1. Center of the screen
2. Top-left corner
3. Bottom-right corner

After calibration, the cursor window remains open and follows the position of the detected nose landmark. Press `Q` to close the program.

## How It Works

1. OpenCV captures frames from the default webcam.
2. MediaPipe Face Mesh finds face landmarks.
3. Landmark index `1` is used as the nose tip.
4. Calibration records nose-position minimum and maximum values.
5. Each nose position is normalized to the calibrated range.
6. The normalized coordinates are converted into screen coordinates.
7. PyAutoGUI moves the mouse pointer to those coordinates.

## Important Notes

- The script disables PyAutoGUI's fail-safe mode by setting `pyautogui.FAILSAFE = False`. Keep the terminal active and use `Q` to stop the program if needed.
- Camera access and mouse/automation permissions may be required on macOS, Linux, or Windows.
- Lighting, webcam quality, face distance, and calibration affect tracking accuracy.
- Use intentionally and with an easy way to regain control of your mouse.

## Troubleshooting

### Camera cannot be opened

- Check that a webcam is connected.
- Ensure another application is not exclusively using the camera.
- Allow terminal or Python camera access in system privacy settings.

### No face is detected

- Improve room lighting.
- Face the camera directly.
- Move closer to the camera without filling the frame completely.

### Cursor movement is difficult to control

- Run the calibration again while sitting in the same position where you plan to use the program.
- Keep the head and neck position natural during calibration and use small movements afterward.

### MediaPipe installation fails

- Upgrade pip:

  ```bash
  python -m pip install --upgrade pip
  ```

- If needed, create a virtual environment with a supported Python version.

## Project Structure

```text
.
├── main.py
├── requirements.txt
└── README.md
```

## License

No license is currently specified. A license should be added before using or distributing this project publicly, if applicable.
