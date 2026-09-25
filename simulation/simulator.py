"""
Simulation Engine Module
Handles numerical integration, controller step updating, disturbance scheduling, and time-series data collection.
"""

import pandas as pd
import numpy as np
from models.room_model import RoomModel
from controllers.p import PController
from controllers.pi import PIController
from controllers.pid import PIDController


class Simulator:
    def __init__(self):
        """Initialize the Simulation Engine."""
        pass

    def run_simulation(
        self,
        mode: str = "PID",
        setpoint: float = 24.0,
        initial_temp: float = 32.0,
        ambient_temp: float = 30.0,
        tau: float = 60.0,
        k_f: float = 0.20,
        Kp: float = 1.2,
        Ki: float = 0.05,
        Kd: float = 0.20,
        open_loop_fan_speed: float = 0.50,
        disturbances: list = None,
        duration: float = 300.0,
        dt: float = 0.1
    ) -> pd.DataFrame:
        """
        Run complete simulation over duration with specified controller and disturbances.

        Parameters:
            mode (str): 'P', 'PI', 'PID', or 'Open-Loop'
            setpoint (float): Desired target temperature (°C)
            initial_temp (float): Starting room temperature (°C)
            ambient_temp (float): Outside ambient temperature (°C)
            tau (float): Thermal time constant (seconds)
            k_f (float): Fan cooling power coefficient (°C/(s*u))
            Kp (float): Proportional gain
            Ki (float): Integral gain
            Kd (float): Derivative gain
            open_loop_fan_speed (float): Fixed fan speed signal [0, 1] for open-loop mode
            disturbances (list): List of dicts [{'time': t, 'magnitude': q}, ...]
            duration (float): Simulation duration in seconds
            dt (float): Integration step size in seconds

        Returns:
            pd.DataFrame: Time-series result containing columns:
                ['time', 'temperature', 'setpoint', 'fan_speed', 'fan_speed_pct',
                 'error', 'disturbance', 'mode']
        """
        if disturbances is None:
            # Default demonstration disturbances at t=100s and t=200s
            disturbances = [
                {"time": 100.0, "magnitude": 0.03},  # Heat disturbance at t=100s
                {"time": 200.0, "magnitude": 0.03}   # Secondary heat disturbance at t=200s
            ]

        # Initialize Plant Model
        room = RoomModel(
            initial_temp=initial_temp,
            ambient_temp=ambient_temp,
            tau=tau,
            k_f=k_f
        )

        # Instantiate selected controller
        if mode == "P":
            controller = PController(Kp=Kp)
        elif mode == "PI":
            controller = PIController(Kp=Kp, Ki=Ki)
        elif mode == "PID":
            controller = PIDController(Kp=Kp, Ki=Ki, Kd=Kd)
        else:
            controller = None  # Open-Loop mode

        time_steps = np.arange(0.0, duration + dt / 2.0, dt)
        
        # Preallocate records
        records = []
        current_u = open_loop_fan_speed if mode == "Open-Loop" else 0.0

        for t in time_steps:
            # Calculate active disturbance heat rate Q at time t
            active_Q = sum(d["magnitude"] for d in disturbances if t >= d["time"])

            # Current room temperature before step update
            current_temp = room.current_temp

            if mode == "Open-Loop":
                current_u = max(0.0, min(1.0, float(open_loop_fan_speed)))
                error = current_temp - setpoint
            else:
                # Closed-Loop Feedback Control: Compute fan output u and error e
                current_u, error = controller.compute(setpoint=setpoint, current_temp=current_temp, dt=dt)

            # Record state at time t
            records.append({
                "time": round(float(t), 2),
                "temperature": float(current_temp),
                "setpoint": float(setpoint),
                "fan_speed": float(current_u),
                "fan_speed_pct": float(current_u * 100.0),
                "error": float(error),
                "disturbance": float(active_Q),
                "mode": mode
            })

            # Advance plant thermal model by step dt
            room.step(u=current_u, Q=active_Q, dt=dt)

        df = pd.DataFrame(records)
        return df
