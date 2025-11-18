from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Literal

import numpy as np
import pandas as pd


VALUE_COL = "ScrawTCorr2PCorrJig2Average"
TIME_COL = "Timestamp"
THRESHOLD = 1.035

RECENT_POINTS = 4
MAX_IDLE_MINUTES = 15
DEFAULT_CLEANING_SAMPLES = 20


Mode = Literal[
    "no_data",
    "recent_downtrend_fixed_20",
    "global_slope",
    "no_valid_slope",
]


@dataclass
class ThresholdPrediction:
    """Rezultat napovedi do thresholda."""

    samples_to_threshold: Optional[float]
    samples_to_threshold_ceil: Optional[int]
    time_to_threshold: Optional[timedelta]
    line_stopped: bool
    mode: Mode
    last_value: Optional[float]
    avg_interval: Optional[timedelta]


def _compute_recent_slope(last_df: pd.DataFrame, value_col: str) -> Optional[float]:
    """
    Iz zadnjih RECENT_POINTS podatkov izračuna slope po indeksu.
    Če je podatkov premalo, vrne None.
    """
    if len(last_df) < 2:
        return None

    y = last_df[value_col].to_numpy().astype(float)
    x = np.arange(len(y))

    # linearna regresija: y = a*x + b
    a, b = np.polyfit(x, y, deg=1)
    return float(a)


def _compute_avg_interval(last_df: pd.DataFrame, timestamp_col: str) -> Optional[timedelta]:
    """
    Povprečen časovni interval med zadnjimi RECENT_POINTS timestampi.
    """
    if len(last_df) < 2:
        return None

    ts = pd.to_datetime(last_df[timestamp_col])
    ts = ts.sort_values()
    diffs = ts.diff().dropna()

    if diffs.empty:
        return None

    return diffs.mean()


def predict_threshold(
    df: pd.DataFrame,
    slope_per_sample: Optional[float],
    threshold: float = THRESHOLD,
    value_col: str = VALUE_COL,
    timestamp_col: str = TIME_COL,
    recent_points: int = RECENT_POINTS,
    max_idle_minutes: int = MAX_IDLE_MINUTES,
    cleaning_samples: int = DEFAULT_CLEANING_SAMPLES,
) -> ThresholdPrediction:
    #if empty
    if df is None or df.empty:
        return ThresholdPrediction(
            samples_to_threshold=None,
            samples_to_threshold_ceil=None,
            time_to_threshold=None,
            line_stopped=True,
            mode="no_data",
            last_value=None,
            avg_interval=None,
        )

    df = df.copy()
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df = df.sort_values(timestamp_col).reset_index(drop=True)

    #1) upošteva samo neneničelne podatke
    df_valid = df[df[value_col] > 0].copy()

    if df_valid.empty:
        last_ts = df[timestamp_col].iloc[-1]
        now = pd.Timestamp.now(tz=last_ts.tz if getattr(last_ts, "tz", None) else None)
        return ThresholdPrediction(
            samples_to_threshold=None,
            samples_to_threshold_ceil=None,
            time_to_threshold=None,
            line_stopped=True,
            mode="no_data",
            last_value=None,
            avg_interval=None,
        )

    #2) zadnja neneničelna vrednost
    last_value = float(df_valid[value_col].iloc[-1])
    last_ts = df_valid[timestamp_col].iloc[-1]

    # zadnji trenutek v originalnem df (tudi če ima 0)
    last_ts_raw = df[timestamp_col].iloc[-1]

    # 3) zadnjih N veljavnih točk
    recent_df = df_valid.tail(recent_points)

    recent_slope = _compute_recent_slope(recent_df, value_col=value_col)
    avg_interval = _compute_avg_interval(recent_df, timestamp_col=timestamp_col)

    # 4) ali linija stoji
    now = pd.Timestamp.now(tz=last_ts_raw.tz if getattr(last_ts_raw, "tz", None) else None)
    idle_delta = now - last_ts_raw
    line_stopped = idle_delta > pd.Timedelta(minutes=max_idle_minutes)

    # 5) metoda
    if recent_slope is not None and recent_slope < 0:
        samples_to_threshold = float(cleaning_samples)
        mode: Mode = "recent_downtrend_fixed_20"
    else:
        # slope
        if slope_per_sample is None or slope_per_sample <= 0:
            return ThresholdPrediction(
                samples_to_threshold=None,
                samples_to_threshold_ceil=None,
                time_to_threshold=None,
                line_stopped=line_stopped,
                mode="no_valid_slope",
                last_value=last_value,
                avg_interval=avg_interval,
            )

        delta = threshold - last_value
        if delta <= 0:
            samples_to_threshold = 0.0
        else:
            samples_to_threshold = delta / slope_per_sample

        mode = "global_slope"

    # 6) Izračun časa do thresholda
    if avg_interval is None or samples_to_threshold is None:
        time_to_threshold = None
    else:
        time_to_threshold = avg_interval * samples_to_threshold

    samples_to_threshold_ceil = (
        int(np.ceil(samples_to_threshold)) if samples_to_threshold is not None else None
    )

    return ThresholdPrediction(
        samples_to_threshold=samples_to_threshold,
        samples_to_threshold_ceil=samples_to_threshold_ceil,
        time_to_threshold=time_to_threshold,
        line_stopped=line_stopped,
        mode=mode,
        last_value=last_value,
        avg_interval=avg_interval,
    )

