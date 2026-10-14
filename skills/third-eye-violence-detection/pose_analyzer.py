"""
pose_analyzer.py – Pose landmark extraction and feature computation.

Uses MediaPipe Pose Landmarker (Tasks API, mediapipe ≥ 0.10) to detect
33 body landmarks per frame and derives higher-level features (joint angles,
limb velocities, wrist elevation) that feed the violence classifier.

The pose landmarker model is downloaded automatically on first use from the
official MediaPipe model repository.
"""

from __future__ import annotations

import math
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import List, Optional

import mediapipe as mp
import numpy as np

# --------------------------------------------------------------------------- #
# Model download                                                               #
# --------------------------------------------------------------------------- #

_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
)
_MODEL_PATH = Path(__file__).parent / "pose_landmarker_lite.task"


def _ensure_model() -> str:
    """Download the pose landmarker model if it is not already present."""
    if not _MODEL_PATH.exists():
        print(f"Downloading pose landmarker model to {_MODEL_PATH} …")
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
        print("Download complete.")
    return str(_MODEL_PATH)


# --------------------------------------------------------------------------- #
# Landmark index aliases (same 33-point layout as the legacy solutions API)    #
# --------------------------------------------------------------------------- #

_LM = mp.tasks.vision.PoseLandmark


class PoseFeatures:
    """Container for per-frame pose-derived features."""

    def __init__(
        self,
        left_elbow_angle: float,
        right_elbow_angle: float,
        left_shoulder_angle: float,
        right_shoulder_angle: float,
        left_knee_angle: float,
        right_knee_angle: float,
        left_wrist_elevation: float,
        right_wrist_elevation: float,
        left_wrist_velocity: float,
        right_wrist_velocity: float,
        left_ankle_velocity: float,
        right_ankle_velocity: float,
        wrist_distance: float,
        landmarks: Optional[List] = None,
    ) -> None:
        self.left_elbow_angle = left_elbow_angle
        self.right_elbow_angle = right_elbow_angle
        self.left_shoulder_angle = left_shoulder_angle
        self.right_shoulder_angle = right_shoulder_angle
        self.left_knee_angle = left_knee_angle
        self.right_knee_angle = right_knee_angle
        # positive = wrist above shoulder (arms raised)
        self.left_wrist_elevation = left_wrist_elevation
        self.right_wrist_elevation = right_wrist_elevation
        # pixel-space velocity between frames
        self.left_wrist_velocity = left_wrist_velocity
        self.right_wrist_velocity = right_wrist_velocity
        self.left_ankle_velocity = left_ankle_velocity
        self.right_ankle_velocity = right_ankle_velocity
        # distance between both wrists (normalised to torso length)
        self.wrist_distance = wrist_distance
        # raw landmark list for drawing (list of NormalizedLandmark)
        self.landmarks = landmarks


def _angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Return the angle (degrees) at joint *b* formed by the three 2-D points."""
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-9)
    return math.degrees(math.acos(float(np.clip(cos_angle, -1.0, 1.0))))


def _lm_xy(landmarks: List, idx: int) -> np.ndarray:
    """Extract (x, y) as a numpy array from a landmark list."""
    lm = landmarks[idx]
    return np.array([lm.x, lm.y], dtype=np.float32)


class PoseAnalyzer:
    """
    Wraps MediaPipe PoseLandmarker (Tasks API) and computes per-frame
    violence-relevant features.

    Parameters
    ----------
    history_len : int
        Number of recent frames kept for velocity estimation.
    min_detection_confidence : float
        Minimum confidence for pose detection.
    min_tracking_confidence : float
        Minimum confidence for pose tracking between frames.
    """

    def __init__(
        self,
        history_len: int = 5,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        model_path = _ensure_model()
        options = mp.tasks.vision.PoseLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=model_path),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=min_detection_confidence,
            min_pose_presence_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self._landmarker = mp.tasks.vision.PoseLandmarker.create_from_options(options)
        self._history: deque[dict[str, np.ndarray]] = deque(maxlen=history_len)
        self._start_time_ms: int = int(time.time() * 1000)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def process(self, bgr_frame: np.ndarray) -> Optional[PoseFeatures]:
        """
        Run pose estimation on *bgr_frame* and return a :class:`PoseFeatures`
        instance, or ``None`` if no pose is detected.
        """
        # Build a MediaPipe Image from the BGR frame
        rgb = bgr_frame[:, :, ::-1].copy()  # BGR → RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        # Monotonically increasing timestamp required by VIDEO mode
        timestamp_ms = int(time.time() * 1000) - self._start_time_ms
        result = self._landmarker.detect_for_video(mp_image, timestamp_ms)

        if not result.pose_landmarks:
            return None

        # Use the first detected person's landmarks
        lms = result.pose_landmarks[0]
        h, w = bgr_frame.shape[:2]

        # ---------- joint angles ----------
        # Elbow: shoulder → elbow → wrist
        l_elbow = _angle(
            _lm_xy(lms, _LM.LEFT_SHOULDER),
            _lm_xy(lms, _LM.LEFT_ELBOW),
            _lm_xy(lms, _LM.LEFT_WRIST),
        )
        r_elbow = _angle(
            _lm_xy(lms, _LM.RIGHT_SHOULDER),
            _lm_xy(lms, _LM.RIGHT_ELBOW),
            _lm_xy(lms, _LM.RIGHT_WRIST),
        )

        # Shoulder: hip → shoulder → elbow
        l_shoulder = _angle(
            _lm_xy(lms, _LM.LEFT_HIP),
            _lm_xy(lms, _LM.LEFT_SHOULDER),
            _lm_xy(lms, _LM.LEFT_ELBOW),
        )
        r_shoulder = _angle(
            _lm_xy(lms, _LM.RIGHT_HIP),
            _lm_xy(lms, _LM.RIGHT_SHOULDER),
            _lm_xy(lms, _LM.RIGHT_ELBOW),
        )

        # Knee: hip → knee → ankle
        l_knee = _angle(
            _lm_xy(lms, _LM.LEFT_HIP),
            _lm_xy(lms, _LM.LEFT_KNEE),
            _lm_xy(lms, _LM.LEFT_ANKLE),
        )
        r_knee = _angle(
            _lm_xy(lms, _LM.RIGHT_HIP),
            _lm_xy(lms, _LM.RIGHT_KNEE),
            _lm_xy(lms, _LM.RIGHT_ANKLE),
        )

        # ---------- wrist elevation ----------
        # Positive value = wrist is *above* the shoulder in image coordinates
        # (y axis points downward in image space, so lower y = higher position)
        l_wrist_elev = lms[_LM.LEFT_SHOULDER].y - lms[_LM.LEFT_WRIST].y
        r_wrist_elev = lms[_LM.RIGHT_SHOULDER].y - lms[_LM.RIGHT_WRIST].y

        # ---------- torso length (for normalisation) ----------
        shoulder_mid_y = (lms[_LM.LEFT_SHOULDER].y + lms[_LM.RIGHT_SHOULDER].y) / 2.0
        hip_mid_y = (lms[_LM.LEFT_HIP].y + lms[_LM.RIGHT_HIP].y) / 2.0
        torso_len = abs(shoulder_mid_y - hip_mid_y) + 1e-6

        # ---------- wrist-to-wrist distance ----------
        l_wrist_xy = _lm_xy(lms, _LM.LEFT_WRIST)
        r_wrist_xy = _lm_xy(lms, _LM.RIGHT_WRIST)
        wrist_dist = float(np.linalg.norm(l_wrist_xy - r_wrist_xy)) / torso_len

        # ---------- velocity (pixel-space) ----------
        def to_px(lm_idx: int) -> np.ndarray:
            lm = lms[lm_idx]
            return np.array([lm.x * w, lm.y * h], dtype=np.float32)

        current = {
            "l_wrist": to_px(_LM.LEFT_WRIST),
            "r_wrist": to_px(_LM.RIGHT_WRIST),
            "l_ankle": to_px(_LM.LEFT_ANKLE),
            "r_ankle": to_px(_LM.RIGHT_ANKLE),
        }

        l_wrist_vel = r_wrist_vel = l_ankle_vel = r_ankle_vel = 0.0
        if self._history:
            prev = self._history[-1]
            l_wrist_vel = float(np.linalg.norm(current["l_wrist"] - prev["l_wrist"]))
            r_wrist_vel = float(np.linalg.norm(current["r_wrist"] - prev["r_wrist"]))
            l_ankle_vel = float(np.linalg.norm(current["l_ankle"] - prev["l_ankle"]))
            r_ankle_vel = float(np.linalg.norm(current["r_ankle"] - prev["r_ankle"]))

        self._history.append(current)

        return PoseFeatures(
            left_elbow_angle=l_elbow,
            right_elbow_angle=r_elbow,
            left_shoulder_angle=l_shoulder,
            right_shoulder_angle=r_shoulder,
            left_knee_angle=l_knee,
            right_knee_angle=r_knee,
            left_wrist_elevation=l_wrist_elev,
            right_wrist_elevation=r_wrist_elev,
            left_wrist_velocity=l_wrist_vel,
            right_wrist_velocity=r_wrist_vel,
            left_ankle_velocity=l_ankle_vel,
            right_ankle_velocity=r_ankle_vel,
            wrist_distance=wrist_dist,
            landmarks=lms,
        )

    def close(self) -> None:
        """Release MediaPipe resources."""
        self._landmarker.close()

    # Support use as a context manager
    def __enter__(self) -> "PoseAnalyzer":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
