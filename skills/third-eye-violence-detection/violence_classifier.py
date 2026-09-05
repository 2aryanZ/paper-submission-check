"""
violence_classifier.py – Rule-based violence classifier using pose features.

Detects four common violent actions from a :class:`~pose_analyzer.PoseFeatures`
object and aggregates them into an overall :class:`ViolenceResult`.

Actions detected
----------------
* **PUNCH** – rapid wrist movement with arm raised and extended toward the target.
* **KICK**  – rapid ankle movement with knee partially extended and leg raised.
* **CHOKE** – both wrists close together and elevated (near the neck/face region).
* **AGGRESSIVE_POSE** – arms raised above shoulders with a wide, threatening stance.

Each detector returns a confidence score in [0, 1].  The overall result is
classified as *violent* when the maximum individual confidence exceeds
:data:`VIOLENCE_THRESHOLD`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from pose_analyzer import PoseFeatures

# --------------------------------------------------------------------------- #
# Tunable thresholds                                                           #
# --------------------------------------------------------------------------- #

VIOLENCE_THRESHOLD: float = 0.55  # overall confidence above which alert fires

# Punch detection
_PUNCH_MIN_WRIST_VEL: float = 18.0    # pixels/frame; minimum wrist speed
_PUNCH_MIN_ELBOW_ANGLE: float = 90.0  # arm must be at least this extended (°)
_PUNCH_MIN_WRIST_ELEV: float = 0.05   # wrist must be above hip (normalised)

# Kick detection
_KICK_MIN_ANKLE_VEL: float = 20.0    # pixels/frame
_KICK_MIN_KNEE_ANGLE: float = 100.0  # knee must be reasonably extended (°)
_KICK_MIN_HIP_RAISE: float = 0.10    # ankle above hip in normalised coords

# Choke detection
_CHOKE_MAX_WRIST_DIST: float = 0.6   # wrists close together (normalised)
_CHOKE_MIN_ELEV: float = 0.15        # both wrists elevated above shoulder

# Aggressive pose detection
_AGG_MIN_SHOULDER_ANGLE: float = 70.0  # arms raised from the side (°)
_AGG_MIN_WRIST_ELEV: float = 0.0       # at least at shoulder height


# --------------------------------------------------------------------------- #
# Result dataclass                                                             #
# --------------------------------------------------------------------------- #


@dataclass
class ViolenceResult:
    """Aggregated per-frame violence assessment."""

    is_violent: bool
    overall_confidence: float
    detected_actions: List[str] = field(default_factory=list)
    action_scores: List[Tuple[str, float]] = field(default_factory=list)

    def __str__(self) -> str:
        actions = ", ".join(self.detected_actions) if self.detected_actions else "none"
        status = "VIOLENT" if self.is_violent else "normal"
        return (
            f"[{status}] confidence={self.overall_confidence:.2f} "
            f"actions=[{actions}]"
        )


# --------------------------------------------------------------------------- #
# Individual action detectors                                                  #
# --------------------------------------------------------------------------- #


def _detect_punch(features: PoseFeatures) -> float:
    """Return punch confidence in [0, 1]."""
    scores: list[float] = []

    for wrist_vel, elbow_ang, wrist_elev in (
        (features.left_wrist_velocity, features.left_elbow_angle, features.left_wrist_elevation),
        (features.right_wrist_velocity, features.right_elbow_angle, features.right_wrist_elevation),
    ):
        vel_score = min(wrist_vel / (_PUNCH_MIN_WRIST_VEL * 2), 1.0) if wrist_vel >= _PUNCH_MIN_WRIST_VEL else 0.0
        elbow_score = min((elbow_ang - _PUNCH_MIN_ELBOW_ANGLE) / 90.0, 1.0) if elbow_ang >= _PUNCH_MIN_ELBOW_ANGLE else 0.0
        elev_score = 1.0 if wrist_elev >= _PUNCH_MIN_WRIST_ELEV else 0.0
        combined = (vel_score * 0.5 + elbow_score * 0.3 + elev_score * 0.2)
        scores.append(combined)

    return max(scores)


def _detect_kick(features: PoseFeatures) -> float:
    """Return kick confidence in [0, 1]."""
    scores: list[float] = []

    for ankle_vel, knee_ang in (
        (features.left_ankle_velocity, features.left_knee_angle),
        (features.right_ankle_velocity, features.right_knee_angle),
    ):
        vel_score = min(ankle_vel / (_KICK_MIN_ANKLE_VEL * 2), 1.0) if ankle_vel >= _KICK_MIN_ANKLE_VEL else 0.0
        knee_score = min((knee_ang - _KICK_MIN_KNEE_ANGLE) / 80.0, 1.0) if knee_ang >= _KICK_MIN_KNEE_ANGLE else 0.0
        combined = vel_score * 0.6 + knee_score * 0.4
        scores.append(combined)

    return max(scores)


def _detect_choke(features: PoseFeatures) -> float:
    """Return choke confidence in [0, 1]."""
    dist_score = max(0.0, 1.0 - features.wrist_distance / _CHOKE_MAX_WRIST_DIST)
    l_elev_ok = 1.0 if features.left_wrist_elevation >= _CHOKE_MIN_ELEV else 0.0
    r_elev_ok = 1.0 if features.right_wrist_elevation >= _CHOKE_MIN_ELEV else 0.0
    elev_score = (l_elev_ok + r_elev_ok) / 2.0
    return dist_score * 0.5 + elev_score * 0.5


def _detect_aggressive_pose(features: PoseFeatures) -> float:
    """Return aggressive-stance confidence in [0, 1]."""
    l_raised = (
        features.left_shoulder_angle >= _AGG_MIN_SHOULDER_ANGLE
        and features.left_wrist_elevation >= _AGG_MIN_WRIST_ELEV
    )
    r_raised = (
        features.right_shoulder_angle >= _AGG_MIN_SHOULDER_ANGLE
        and features.right_wrist_elevation >= _AGG_MIN_WRIST_ELEV
    )
    arms_raised = (int(l_raised) + int(r_raised)) / 2.0
    return arms_raised


# --------------------------------------------------------------------------- #
# Main classifier                                                              #
# --------------------------------------------------------------------------- #


class ViolenceClassifier:
    """
    Stateless rule-based violence classifier.

    Call :meth:`classify` on a :class:`~pose_analyzer.PoseFeatures` object
    obtained from :class:`~pose_analyzer.PoseAnalyzer`.
    """

    _DETECTORS = [
        ("PUNCH", _detect_punch),
        ("KICK", _detect_kick),
        ("CHOKE", _detect_choke),
        ("AGGRESSIVE_POSE", _detect_aggressive_pose),
    ]

    def classify(self, features: PoseFeatures) -> ViolenceResult:
        """Classify a single frame and return a :class:`ViolenceResult`."""
        action_scores: list[tuple[str, float]] = []
        for name, detector in self._DETECTORS:
            score = float(detector(features))
            action_scores.append((name, round(score, 3)))

        overall = max(score for _, score in action_scores)
        detected = [name for name, score in action_scores if score >= VIOLENCE_THRESHOLD]

        return ViolenceResult(
            is_violent=overall >= VIOLENCE_THRESHOLD,
            overall_confidence=round(overall, 3),
            detected_actions=detected,
            action_scores=action_scores,
        )
