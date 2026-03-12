# 👁️ Gaze Attention Tracker

A real-time eye gaze detection system built with Python and MediaPipe that tracks iris movement, detects when your attention drifts from the screen, and logs your focus stats live — all running on a standard webcam.

No eye-tracking hardware. No cloud. Just your camera and 128 lines of Python.

---

## ⚙️ How It Works

The system uses **MediaPipe Face Mesh** to map 468 facial landmarks per frame. From those, it extracts iris positions (landmarks 468–477) and eye corner coordinates to compute two independent gaze ratios:

### Horizontal Ratio (Left / Right)
```python
left_ratio = (left_eye_left_corner_x - iris_center_left_x) / 
             (left_eye_left_corner_x - left_eye_right_corner_x)
```

### Vertical Ratio (Up / Down)
```python
eye_corner_y = (left_eye_left_corner_y + left_eye_right_corner_y) / 2
eye_width    = abs(left_eye_right_corner_x - left_eye_left_corner_x)
vertical_ratio = (iris_center_left_y - eye_corner_y) / eye_width
```

> ⚠️ Eye **width** is used as the vertical normalizer — not eye height. This accounts for head tilt, where the iris barely shifts vertically relative to eye height when looking up or down.

### Gaze Classification
```python
if vertical_ratio < -0.10:   → "Looking Top"
elif vertical_ratio > 0.023: → "Looking Down"
elif left_ratio < 0.38:      → "Looking Left"
elif left_ratio > 0.55:      → "Looking Right"
else:                        → "Center"
```

### Attention Logic
- Gaze away for **> 0.3 seconds** → triggers **"Look At The Screen!"** warning
- Each new look-away event increments the **Look Away Counter**
- Consecutive centered gaze is timed and logged as a **Focus Streak**
- The longest streak is saved as **Max Focus Time**

---

## 📊 Live Overlay

| Position | Display |
|---|---|
| Top Left | Gaze direction label (e.g. `Looking Right`) |
| Center | `Look At The Screen!` alert in red |
| Bottom Left | `Look Away Count: N` |
| Bottom Right | `Max Focus: 4.12s` |
| Bottom Right | `Center Time: 0.00s` |

Iris centers are marked as **blue dots** on both eyes in real time.

---

## 🌍 Real-World Applications

The same problem this solves in a personal setting is being solved at scale across several industries:

- 🚗 **Driver Monitoring** — detecting fatigue and distraction before an incident, not after
- 🎓 **E-Learning** — measuring whether a student is watching a lecture or zoned out
- ♿ **Accessibility** — gaze-based control interfaces for users with limited motor function
- 🔬 **Behavioral Research** — passive attention measurement without lab equipment
- 💼 **Workplace Productivity** — tracking where attention actually goes, not just screen time

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 (64-bit)
- A working webcam

### Installation

```bash
git clone https://github.com/umang-agarwal-dev/gaze-attention-tracker.git
cd gaze-attention-tracker
pip install -r requirements.txt
```

### Dependencies

```
opencv-python==4.13.0.92
mediapipe==0.10.32
numpy==2.4.2
```

### Run

```bash
py -3.11 "project ap/project.py"
```

Press `Q` to quit.

---

## 📁 Project Structure

```
gaze-attention-tracker/
│
├── project ap/
│   └── project.py     # Full source — webcam loop, iris tracking, gaze logic, focus stats
├── README.md
└── requirements.txt
```

---

## 🔧 Calibration

All thresholds are in `project.py` and can be tuned to your webcam and environment:

```python
# Vertical gaze
LOOK_TOP_THRESHOLD   = -0.10
LOOK_DOWN_THRESHOLD  =  0.023

# Horizontal gaze
LOOK_LEFT_THRESHOLD  =  0.38
LOOK_RIGHT_THRESHOLD =  0.55

# Warning delay
LOOKAWAY_DELAY = 0.3  # seconds before alert fires
```

**Tip:** These were tuned from live debug output — not guesswork. If detection feels off, adjust based on what the ratios actually read in your setup.

---

## 🛠️ Built With

| Library | Version | Purpose |
|---|---|---|
| [Python](https://www.python.org/) | 3.11 (64-bit) | Core language |
| [OpenCV](https://opencv.org/) | 4.13.0.92 | Webcam capture & frame rendering |
| [MediaPipe](https://mediapipe.dev/) | 0.10.32 | Face Mesh + TF Lite XNNPACK |
| [NumPy](https://numpy.org/) | 2.4.2 | Numerical operations |

---

## 👤 Author

**Umang Agarwal**  
[GitHub](https://github.com/umang-agarwal-dev) · [LinkedIn](https://www.linkedin.com/in/umang-agarwal-dev)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

*Inspired by a friend who wasn't paying attention mid-conversation. She still doesn't know she's responsible for this.*
