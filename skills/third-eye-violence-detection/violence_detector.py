"""
violence_detector.py – Third Eye: Real-Time Violence Detection using Pose Estimation

Main entry point.  Captures video from a webcam (or a video file), runs
MediaPipe pose estimation on every frame, classifies the detected pose
as violent or non-violent, and overlays the result on the display.

Usage
-----
    # Webcam (default camera 0)
    python violence_detector.py

    # Video file
    python violence_detector.py --source path/to/video.mp4

    # Specific camera index
    python violence_detector.py --source 1

    # Save annotated output
    python violence_detector.py --source video.mp4 --output out.mp4

    # Headless mode (no display window, useful for servers)
    python violence_detector.py --source video.mp4 --output out.mp4 --no-display

Press **Q** or **ESC** to quit the live window.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from collections import deque
from typing import List, Optional

import cv2
import mediapipe as mp
import numpy as np

from pose_analyzer import PoseAnalyzer
from violence_classifier import ViolenceClassifier, ViolenceResult

# --------------------------------------------------------------------------- #
# Logging                                                                      #
# --------------------------------------------------------------------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("third_eye")

# --------------------------------------------------------------------------- #
# Visual constants                                                              #
# --------------------------------------------------------------------------- #

_FONT = cv2.FONT_HERSHEY_SIMPLEX
_COLOR_NORMAL = (0, 200, 0)      # green  (BGR)
_COLOR_VIOLENT = (0, 0, 220)     # red    (BGR)
_COLOR_SKELETON = (255, 200, 0)  # cyan-ish (BGR)
_ALERT_ALPHA = 0.35              # transparency of the alert overlay rectangle

# Smoothing: keep a rolling window of N frames and alert only when the
# majority are classified as violent (reduces false positives).
_SMOOTHING_WINDOW = 8
_ALERT_MAJORITY = 0.60  # fraction of window frames that must be violent

# --------------------------------------------------------------------------- #
# Drawing utilities (new Tasks API)                                            #
# --------------------------------------------------------------------------- #

_draw_utils = mp.tasks.vision.drawing_utils
_DrawingSpec = _draw_utils.DrawingSpec
_POSE_CONNECTIONS = mp.tasks.vision.PoseLandmarksConnections.POSE_LANDMARKS


def _draw_pose(frame: np.ndarray, landmarks: List) -> None:
    """Draw the MediaPipe skeleton on *frame* in-place."""
    _draw_utils.draw_landmarks(
        frame,
        landmarks,
        connections=_POSE_CONNECTIONS,
        landmark_drawing_spec=_DrawingSpec(
            color=_COLOR_SKELETON, thickness=2, circle_radius=3
        ),
        connection_drawing_spec=_DrawingSpec(
            color=(200, 200, 200), thickness=2
        ),
    )


def _draw_status(
    frame: np.ndarray,
    result: ViolenceResult,
    fps: float,
    smoothed_violent: bool,
) -> None:
    """Overlay status text and, if violent, a semi-transparent red banner."""
    h, w = frame.shape[:2]
    color = _COLOR_VIOLENT if smoothed_violent else _COLOR_NORMAL
    label = "! VIOLENCE DETECTED" if smoothed_violent else "* Monitoring..."

    # Semi-transparent top banner on alert
    if smoothed_violent:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 180), -1)
        cv2.addWeighted(overlay, _ALERT_ALPHA, frame, 1 - _ALERT_ALPHA, 0, frame)

    # Status text
    cv2.putText(frame, label, (12, 40), _FONT, 1.1, color, 2, cv2.LINE_AA)

    # Confidence bar (bottom-left)
    bar_x, bar_y = 12, h - 55
    bar_w = 220
    conf = result.overall_confidence
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + 18), (60, 60, 60), -1)
    fill = int(bar_w * conf)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill, bar_y + 18), color, -1)
    cv2.putText(
        frame,
        f"Confidence: {conf:.0%}",
        (bar_x, bar_y - 6),
        _FONT, 0.5, (220, 220, 220), 1, cv2.LINE_AA,
    )

    # Detected actions
    if result.detected_actions:
        actions_str = "Actions: " + " | ".join(result.detected_actions)
        cv2.putText(
            frame, actions_str, (12, h - 20),
            _FONT, 0.5, color, 1, cv2.LINE_AA,
        )

    # FPS counter (top-right)
    cv2.putText(
        frame, f"FPS {fps:.1f}", (w - 100, 30),
        _FONT, 0.6, (180, 180, 180), 1, cv2.LINE_AA,
    )


# --------------------------------------------------------------------------- #
# Main detection loop                                                           #
# --------------------------------------------------------------------------- #


def run(
    source: str | int = 0,
    output: Optional[str] = None,
    show: bool = True,
) -> None:
    """
    Run the real-time violence detector.

    Parameters
    ----------
    source : str or int
        Path to a video file, or an integer camera index (default 0).
    output : str, optional
        Path for the annotated output video file.  If ``None`` (default)
        no file is written.
    show : bool
        Whether to open an interactive display window (default ``True``).
        Set to ``False`` for headless / server operation.
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        logger.error("Cannot open source: %s", source)
        sys.exit(1)

    fps_in = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    logger.info("Source: %s  |  %dx%d @ %.1f fps", source, frame_w, frame_h, fps_in)

    writer: Optional[cv2.VideoWriter] = None
    if output:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output, fourcc, fps_in, (frame_w, frame_h))
        logger.info("Writing output to: %s", output)

    analyzer = PoseAnalyzer()
    classifier = ViolenceClassifier()

    violence_window: deque[bool] = deque(maxlen=_SMOOTHING_WINDOW)
    prev_time = time.perf_counter()
    frame_count = 0
    alert_count = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_count += 1

            # --- Pose estimation + classification ---
            features = analyzer.process(frame)
            if features is not None:
                result = classifier.classify(features)
                violence_window.append(result.is_violent)

                if features.landmarks is not None and show:
                    _draw_pose(frame, features.landmarks)
            else:
                result = ViolenceResult(
                    is_violent=False,
                    overall_confidence=0.0,
                    detected_actions=[],
                    action_scores=[],
                )
                violence_window.append(False)

            # --- Smoothed alert decision ---
            violent_ratio = (
                sum(violence_window) / len(violence_window)
                if violence_window
                else 0.0
            )
            smoothed_violent = violent_ratio >= _ALERT_MAJORITY

            if smoothed_violent:
                alert_count += 1
                logger.warning("Frame %d | %s", frame_count, result)

            # --- FPS ---
            now = time.perf_counter()
            fps = 1.0 / max(now - prev_time, 1e-6)
            prev_time = now

            # --- Overlay ---
            _draw_status(frame, result, fps, smoothed_violent)

            # --- Output / display ---
            if writer:
                writer.write(frame)

            if show:
                cv2.imshow("Third Eye - Violence Detection", frame)
                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), ord("Q"), 27):  # Q or ESC
                    break

    finally:
        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()
        analyzer.close()

    logger.info(
        "Processed %d frames | violence alerts fired on %d frames (%.1f%%)",
        frame_count,
        alert_count,
        100.0 * alert_count / max(frame_count, 1),
    )


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Third Eye - Real-Time Violence Detection using Pose Estimation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--source",
        default=0,
        help=(
            "Video source: integer camera index (default: 0) "
            "or path to a video file."
        ),
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="FILE",
        help="Path for the annotated output video (e.g. output.mp4).",
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        help="Run in headless mode without opening a display window.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    # Convert source to int if it looks like a camera index
    source: str | int = args.source
    if isinstance(source, str) and source.isdigit():
        source = int(source)

    run(
        source=source,
        output=args.output,
        show=not args.no_display,
    )
