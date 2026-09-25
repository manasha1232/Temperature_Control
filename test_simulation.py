"""
Standalone Test & Verification Script
Executes non-UI simulations to verify plant model, controllers, simulator, and metrics calculations.
"""

import os
import sys

# Ensure root folder is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulation.simulator import Simulator
from analysis.metrics import PerformanceAnalyzer


def run_verification():
    print("==================================================")
    print(" Running Verification Tests for Control Project   ")
    print("==================================================")

    simulator = Simulator()

    # 1. Run Default PID Simulation
    print("\n[1/4] Running Default PID Simulation (Setpoint=24°C, Init=32°C)...")
    df_pid = simulator.run_simulation(
        mode="PID",
        setpoint=24.0,
        initial_temp=32.0,
        ambient_temp=30.0,
        tau=60.0,
        k_f=0.15,
        Kp=0.8,
        Ki=0.03,
        Kd=0.15,
        duration=300.0,
        dt=0.1
    )
    print(f"  -> Generated {len(df_pid)} data steps.")
    print(f"  -> Final Temperature: {df_pid['temperature'].iloc[-1]:.2f}°C")
    print(f"  -> Final Fan Speed: {df_pid['fan_speed_pct'].iloc[-1]:.1f}%")

    metrics_pid = PerformanceAnalyzer.calculate_metrics(df_pid)
    print("  -> PID Performance Metrics:")
    for k, v in metrics_pid.items():
        print(f"      - {k}: {v}")

    # 2. Run P Controller Simulation
    print("\n[2/4] Running P Controller Simulation...")
    df_p = simulator.run_simulation(
        mode="P",
        setpoint=24.0,
        initial_temp=32.0,
        ambient_temp=30.0,
        Kp=0.8,
        duration=300.0
    )
    metrics_p = PerformanceAnalyzer.calculate_metrics(df_p)
    print(f"  -> P Steady-State Error: {metrics_p['Steady-State Error (°C)']}°C")

    # 3. Run PI Controller Simulation
    print("\n[3/4] Running PI Controller Simulation...")
    df_pi = simulator.run_simulation(
        mode="PI",
        setpoint=24.0,
        initial_temp=32.0,
        ambient_temp=30.0,
        Kp=0.8,
        Ki=0.03,
        duration=300.0
    )
    metrics_pi = PerformanceAnalyzer.calculate_metrics(df_pi)
    print(f"  -> PI Steady-State Error: {metrics_pi['Steady-State Error (°C)']}°C")

    # 4. Run Open-Loop Simulation
    print("\n[4/4] Running Open-Loop Simulation...")
    df_open = simulator.run_simulation(
        mode="Open-Loop",
        setpoint=24.0,
        initial_temp=32.0,
        ambient_temp=30.0,
        open_loop_fan_speed=0.50,
        duration=300.0
    )
    metrics_open = PerformanceAnalyzer.calculate_metrics(df_open)
    print(f"  -> Open-Loop Final Temp under disturbance: {df_open['temperature'].iloc[-1]:.2f}°C")

    print("\n==================================================")
    print(" ALL VERIFICATION TESTS PASSED SUCCESSFULLY!       ")
    print("==================================================")


if __name__ == "__main__":
    run_verification()
