# 👁️ Third Eye – Real-Time Violence Detection using Pose Estimation

A lightweight Python system that uses **MediaPipe Pose** and **OpenCV** to
detect violent behaviour in real time from a webcam or video file.  No GPU or
deep-learning training data required — the classifier uses interpretable,
geometry-based rules derived from body-pose landmarks.

---

## 🗂️ Project Structure

```
third-eye-violence-detection/
├── violence_detector.py    # Main entry point (CLI + run loop)
├── pose_analyzer.py        # MediaPipe wrapper — extracts joint angles & velocities
├── violence_classifier.py  # Rule-based classifier: PUNCH, KICK, CHOKE, AGGRESSIVE POSE
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ How It Works

```
Camera / Video
     │
     ▼
┌─────────────────────────┐
│   OpenCV VideoCapture   │  reads frames
└────────────┬────────────┘
             │ BGR frame
             ▼
┌─────────────────────────┐
│     PoseAnalyzer        │  MediaPipe Pose
│  (pose_analyzer.py)     │  33 body landmarks
└────────────┬────────────┘
             │ PoseFeatures
             │  • joint angles  (elbow, shoulder, knee)
             │  • wrist / ankle velocities
             │  • wrist elevation relative to shoulder
             │  • wrist-to-wrist distance
             ▼
┌─────────────────────────┐
│  ViolenceClassifier     │  Rule-based detector
│ (violence_classifier.py)│  PUNCH | KICK | CHOKE | AGGRESSIVE_POSE
└────────────┬────────────┘
             │ ViolenceResult  (confidence, detected actions)
             ▼
┌─────────────────────────┐
│   Smoothing window (8 f)│  majority vote to reduce false positives
└────────────┬────────────┘
             │
             ▼
    Annotated display + optional MP4 output
```

### Detected Actions

| Action | Triggers |
|---|---|
| **PUNCH** | High wrist speed + arm extended + wrist above hip |
| **KICK** | High ankle speed + knee extended |
| **CHOKE** | Both wrists close together + elevated near face/neck |
| **AGGRESSIVE\_POSE** | Both arms raised above shoulder height |

An overall **confidence score** (0–1) is computed as the maximum individual
action score.  A frame is flagged as violent when confidence ≥ 0.55 (tunable).
To reduce flicker, a rolling 8-frame majority vote is applied before raising
an alert.

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> Requires **Python 3.8+** and **mediapipe ≥ 0.10**.
>
> On first run, the pose landmarker model (~3 MB) is downloaded automatically
> from the official MediaPipe model repository and saved alongside the scripts.

### 2. Run with webcam (default)

```bash
python violence_detector.py
```

Press **Q** or **Esc** to quit.

### 3. Run on a video file

```bash
python violence_detector.py --source path/to/video.mp4
```

### 4. Save annotated output

```bash
python violence_detector.py --source video.mp4 --output annotated.mp4
```

### 5. Headless / server mode (no display window)

```bash
python violence_detector.py --source video.mp4 --output out.mp4 --no-display
```

---

## 🖥️ Display Overlay

When a display window is open you will see:

| Element | Description |
|---|---|
| **Skeleton overlay** | MediaPipe 33-landmark skeleton drawn on the body |
| **Top banner** | Red semi-transparent banner when violence is detected |
| **Status text** | "! VIOLENCE DETECTED" (red) or "* Monitoring..." (green) |
| **Confidence bar** | Horizontal bar showing the current confidence level |
| **Action labels** | Names of detected violent actions (PUNCH, KICK, etc.) |
| **FPS counter** | Live frames-per-second (top-right corner) |

---

## 🛠️ Configuration

All detection thresholds are defined as module-level constants in
`violence_classifier.py` and can be adjusted without changing the logic:

| Constant | Default | Meaning |
|---|---|---|
| `VIOLENCE_THRESHOLD` | `0.55` | Minimum confidence to flag a frame as violent |
| `_PUNCH_MIN_WRIST_VEL` | `18.0` | Minimum wrist speed (pixels/frame) for punch |
| `_PUNCH_MIN_ELBOW_ANGLE` | `90°` | Minimum elbow extension angle |
| `_KICK_MIN_ANKLE_VEL` | `20.0` | Minimum ankle speed (pixels/frame) for kick |
| `_KICK_MIN_KNEE_ANGLE` | `100°` | Minimum knee extension angle |
| `_CHOKE_MAX_WRIST_DIST` | `0.6` | Max normalised wrist-to-wrist distance |
| `_CHOKE_MIN_ELEV` | `0.15` | Min wrist elevation above shoulder |
| `_AGG_MIN_SHOULDER_ANGLE` | `70°` | Shoulder angle for aggressive pose |

The smoothing window and majority-vote fraction are in `violence_detector.py`:

| Constant | Default | Meaning |
|---|---|---|
| `_SMOOTHING_WINDOW` | `8` | Number of recent frames used for voting |
| `_ALERT_MAJORITY` | `0.60` | Fraction of window that must be violent to alert |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `opencv-python` | Video capture, frame manipulation, display |
| `mediapipe` | Pose estimation (33 body landmarks at ~30 fps on CPU) |
| `numpy` | Numerical computations (angles, distances, velocities) |

---

## 📋 System Requirements

| Requirement | Minimum |
|---|---|
| Python | 3.8+ |
| RAM | 2 GB |
| CPU | Any modern x86-64 / ARM64 (GPU not required) |
| OS | Windows 10+, macOS 11+, Ubuntu 20.04+ |
| Camera | Any USB/built-in webcam at 720p+ |

---

## 🔮 Extending the System

* **Add a trained classifier** — replace `ViolenceClassifier.classify` with a
  scikit-learn or ONNX model that takes the same `PoseFeatures` fields as
  input.  The rest of the pipeline stays the same.
* **Multi-person detection** — switch MediaPipe to `Holistic` or use the
  multi-person model and run `PoseAnalyzer` per detected person.
* **Alert integration** — hook into the `if smoothed_violent:` block in
  `violence_detector.py` to send emails, MQTT messages, or database logs.
* **Recording on alert** — start a `VideoWriter` only when violence is
  detected to save evidence clips automatically.

---

## 📄 License

This project is provided under the same license as the parent repository.
See [LICENSE](../../LICENSE) for details.
