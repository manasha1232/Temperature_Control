"""
Performance Analyzer Module
Calculates standard control systems metrics:
- Rise Time
- Settling Time (±2% tolerance band)
- Overshoot (%)
- Steady-State Error
- Peak Error
- Integral Absolute Error (IAE)
- Integral Squared Error (ISE)
"""

import pandas as pd
import numpy as np


class PerformanceAnalyzer:
    @staticmethod
    def calculate_metrics(df: pd.DataFrame, tolerance_pct: float = 2.0) -> dict:
        """
        Calculate control performance metrics from simulation data.

        Parameters:
            df (pd.DataFrame): Simulation output containing 'time', 'temperature', 'setpoint', 'error'
            tolerance_pct (float): Settling time tolerance percentage around total step magnitude (default ±2%)

        Returns:
            dict: Dictionary of performance metrics
        """
        time = df["time"].values
        temp = df["temperature"].values
        setpoint = df["setpoint"].iloc[0]
        initial_temp = temp[0]

        dt = time[1] - time[0] if len(time) > 1 else 0.1
        total_change = initial_temp - setpoint  # E.g. 32°C - 24°C = 8°C

        # 1. Steady-State Error (final error)
        ss_error = abs(temp[-1] - setpoint)

        # 2. Peak Error (maximum absolute deviation)
        errors = np.abs(temp - setpoint)
        peak_error = np.max(errors)

        # 3. Integral Absolute Error (IAE) & Integral Squared Error (ISE)
        iae = np.sum(errors) * dt
        ise = np.sum(errors ** 2) * dt

        # 4. Rise Time (Time to go from 10% change to 90% change of initial temperature drop)
        if total_change > 0:
            target_10 = initial_temp - 0.10 * total_change
            target_90 = initial_temp - 0.90 * total_change

            idx_10 = np.where(temp <= target_10)[0]
            idx_90 = np.where(temp <= target_90)[0]

            if len(idx_10) > 0 and len(idx_90) > 0:
                t_10 = time[idx_10[0]]
                t_90 = time[idx_90[0]]
                rise_time = t_90 - t_10
            else:
                rise_time = None
        else:
            rise_time = None

        # 5. Settling Time (±2% of total change or setpoint tolerance)
        tolerance_band = max(0.2, (tolerance_pct / 100.0) * abs(total_change))
        within_band = errors <= tolerance_band

        # Find the last index where system was OUTSIDE the tolerance band
        outside_indices = np.where(~within_band)[0]
        if len(outside_indices) == 0:
            settling_time = 0.0  # Settled immediately
        elif outside_indices[-1] == len(time) - 1:
            settling_time = None  # Never settled within simulation duration
        else:
            settling_time = time[outside_indices[-1] + 1]

        # 6. Overshoot (cooling below setpoint)
        min_temp = np.min(temp)
        if min_temp < setpoint and total_change > 0:
            overshoot_deg = setpoint - min_temp
            overshoot_pct = (overshoot_deg / abs(total_change)) * 100.0
        else:
            overshoot_deg = 0.0
            overshoot_pct = 0.0

        return {
            "Rise Time (s)": round(rise_time, 2) if rise_time is not None else "N/A",
            "Settling Time (s)": round(settling_time, 2) if settling_time is not None else "Not Settled",
            "Overshoot (°C)": round(overshoot_deg, 2),
            "Overshoot (%)": round(overshoot_pct, 2),
            "Steady-State Error (°C)": round(ss_error, 3),
            "Peak Error (°C)": round(peak_error, 2),
            "IAE (°C·s)": round(iae, 2),
            "ISE (°C²·s)": round(ise, 2)
        }
