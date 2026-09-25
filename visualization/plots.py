"""
Visualization Module
Generates engineering graphs using Matplotlib and HTML/CSS animation widget for fan speed visualization.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Apply modern clean style
plt.style.use("ggplot")
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8


def plot_temperature(df: pd.DataFrame, disturbances: list = None, title: str = "Room Temperature vs Time"):
    """Plot Temperature vs Time with Setpoint line and disturbance markers."""
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=100)
    
    ax.plot(df["time"], df["temperature"], label="Actual Room Temp (°C)", color="#1f77b4", linewidth=2.5)
    ax.plot(df["time"], df["setpoint"], label="Desired Setpoint (°C)", color="#d62728", linestyle="--", linewidth=2.0)

    # Highlight disturbance events
    if disturbances:
        for d in disturbances:
            t_d = d["time"]
            mag = d.get("magnitude", 0)
            if t_d in df["time"].values or t_d <= df["time"].max():
                ax.axvline(x=t_d, color="#ff7f0e", linestyle=":", linewidth=1.8, label=f"Disturbance @ {t_d}s (+{mag}°C/s)")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Time (seconds)", fontsize=11)
    ax.set_ylabel("Temperature (°C)", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)
    plt.tight_layout()
    return fig


def plot_fan_speed(df: pd.DataFrame, title: str = "Fan Control Signal vs Time"):
    """Plot Fan Speed (%) vs Time."""
    fig, ax = plt.subplots(figsize=(10, 3.5), dpi=100)
    
    ax.plot(df["time"], df["fan_speed_pct"], label="Fan Speed (%)", color="#2ca02c", linewidth=2.0)
    ax.axhline(y=100, color="#d62728", linestyle=":", label="100% Saturation Max", alpha=0.6)
    ax.axhline(y=0, color="#7f7f7f", linestyle=":", label="0% Min", alpha=0.6)

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Time (seconds)", fontsize=11)
    ax.set_ylabel("Fan Speed (%)", fontsize=11)
    ax.set_ylim(-5, 105)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)
    plt.tight_layout()
    return fig


def plot_error(df: pd.DataFrame, title: str = "Temperature Error vs Time"):
    """Plot Temperature Error vs Time."""
    fig, ax = plt.subplots(figsize=(10, 3.5), dpi=100)
    
    ax.plot(df["time"], df["error"], label="Error = T_actual - T_set (°C)", color="#ff7f0e", linewidth=2.0)
    ax.axhline(y=0, color="#2ca02c", linestyle="--", linewidth=1.5, label="Zero Error Target")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Time (seconds)", fontsize=11)
    ax.set_ylabel("Error (°C)", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)
    plt.tight_layout()
    return fig


def plot_controller_comparison(df_p: pd.DataFrame, df_pi: pd.DataFrame, df_pid: pd.DataFrame, disturbances: list = None):
    """Plot superimposed Temperature and Fan Speed responses for P, PI, and PID controllers."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, dpi=100)

    # Temperature plot
    ax1.plot(df_p["time"], df_p["temperature"], label="P Controller", color="#e377c2", linewidth=2.0)
    ax1.plot(df_pi["time"], df_pi["temperature"], label="PI Controller", color="#9467bd", linewidth=2.0)
    ax1.plot(df_pid["time"], df_pid["temperature"], label="PID Controller", color="#1f77b4", linewidth=2.5)
    ax1.plot(df_pid["time"], df_pid["setpoint"], label="Setpoint", color="#d62728", linestyle="--", linewidth=1.8)

    if disturbances:
        for d in disturbances:
            ax1.axvline(x=d["time"], color="#ff7f0e", linestyle=":", alpha=0.7, label=f"Disturbance @ {d['time']}s")

    ax1.set_title("Controller Comparison: Temperature Response", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Temperature (°C)", fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)

    # Fan Speed plot
    ax2.plot(df_p["time"], df_p["fan_speed_pct"], label="P Fan Speed (%)", color="#e377c2", linewidth=1.5, linestyle="--")
    ax2.plot(df_pi["time"], df_pi["fan_speed_pct"], label="PI Fan Speed (%)", color="#9467bd", linewidth=1.5, linestyle="-.")
    ax2.plot(df_pid["time"], df_pid["fan_speed_pct"], label="PID Fan Speed (%)", color="#2ca02c", linewidth=2.0)

    ax2.set_title("Controller Comparison: Fan Control Action", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Time (seconds)", fontsize=11)
    ax2.set_ylabel("Fan Speed (%)", fontsize=11)
    ax2.set_ylim(-5, 105)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)

    plt.tight_layout()
    return fig


def plot_open_vs_closed(df_open: pd.DataFrame, df_closed: pd.DataFrame, disturbances: list = None):
    """Plot Open-Loop vs Closed-Loop comparative temperature response under disturbance."""
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=100)

    ax.plot(df_open["time"], df_open["temperature"], label="Open-Loop (Fixed Fan Speed)", color="#d62728", linewidth=2.2, linestyle="-.")
    ax.plot(df_closed["time"], df_closed["temperature"], label="Closed-Loop (PID Controller)", color="#1f77b4", linewidth=2.5)
    ax.plot(df_closed["time"], df_closed["setpoint"], label="Desired Setpoint", color="#2ca02c", linestyle="--", linewidth=1.8)

    if disturbances:
        for d in disturbances:
            ax.axvline(x=d["time"], color="#ff7f0e", linestyle=":", linewidth=1.8, label=f"Heat Disturbance @ {d['time']}s")

    ax.set_title("Open-Loop vs Closed-Loop Disturbance Rejection", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Time (seconds)", fontsize=11)
    ax.set_ylabel("Temperature (°C)", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)
    plt.tight_layout()
    return fig


def render_fan_animation_html(fan_speed_pct: float, current_temp: float, setpoint: float, error: float) -> str:
    """
    Generate clean CSS/HTML string for rendering an animated rotating fan graphic and thermometer widget.
    Rotation speed scales dynamically based on fan_speed_pct.
    """
    fan_speed_pct = max(0.0, min(100.0, float(fan_speed_pct)))
    
    # Calculate animation duration (faster speed = smaller duration)
    if fan_speed_pct < 1.0:
        anim_speed_css = "animation: none;"
        speed_category = "OFF (0%)"
        speed_badge_color = "#6c757d"
    elif fan_speed_pct < 20.0:
        anim_duration = 3.0 - (fan_speed_pct / 20.0) * 1.5
        anim_speed_css = f"animation: spin {anim_duration:.2f}s linear infinite;"
        speed_category = "SLOW (<20%)"
        speed_badge_color = "#17a2b8"
    elif fan_speed_pct < 50.0:
        anim_duration = 1.5 - ((fan_speed_pct - 20.0) / 30.0) * 0.9
        anim_speed_css = f"animation: spin {anim_duration:.2f}s linear infinite;"
        speed_category = "MEDIUM (20-50%)"
        speed_badge_color = "#ffc107"
    else:
        anim_duration = 0.6 - ((fan_speed_pct - 50.0) / 50.0) * 0.45
        anim_speed_css = f"animation: spin {anim_duration:.2f}s linear infinite;"
        speed_category = "HIGH (50-100%)"
        speed_badge_color = "#dc3545"

    html_code = f"""
    <div style="background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
        <style>
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            .fan-blade-container {{
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .fan-blade {{
                width: 110px;
                height: 110px;
                {anim_speed_css}
            }}
        </style>
        <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-around;">
            <!-- Fan Animation -->
            <div style="text-align: center; margin: 10px;">
                <h4 style="margin-bottom: 8px; color: #212529;">Simulated Cooling Fan</h4>
                <div class="fan-blade-container">
                    <svg class="fan-blade" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="10" fill="#343a40" />
                        <!-- Blade 1 -->
                        <path d="M 50 50 C 45 30 30 15 50 5 C 70 15 55 30 50 50 Z" fill="#007bff" />
                        <!-- Blade 2 -->
                        <path d="M 50 50 C 70 45 85 30 95 50 C 85 70 70 55 50 50 Z" fill="#007bff" />
                        <!-- Blade 3 -->
                        <path d="M 50 50 C 55 70 70 85 50 95 C 30 85 45 70 50 50 Z" fill="#007bff" />
                        <!-- Blade 4 -->
                        <path d="M 50 50 C 30 55 15 70 5 50 C 15 30 30 45 50 50 Z" fill="#007bff" />
                    </svg>
                </div>
                <div style="margin-top: 10px;">
                    <span style="background-color: {speed_badge_color}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">
                        {speed_category}
                    </span>
                </div>
            </div>

            <!-- Digital Thermometer Status -->
            <div style="text-align: center; margin: 10px; min-width: 220px;">
                <h4 style="margin-bottom: 12px; color: #212529;">Room Environment State</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left;">
                    <div style="background: white; padding: 8px 12px; border-radius: 8px; border-left: 4px solid #007bff;">
                        <span style="font-size: 0.8em; color: #6c757d;">Actual Temp</span><br>
                        <strong style="font-size: 1.2em; color: #212529;">{current_temp:.2f} °C</strong>
                    </div>
                    <div style="background: white; padding: 8px 12px; border-radius: 8px; border-left: 4px solid #dc3545;">
                        <span style="font-size: 0.8em; color: #6c757d;">Setpoint</span><br>
                        <strong style="font-size: 1.2em; color: #212529;">{setpoint:.2f} °C</strong>
                    </div>
                    <div style="background: white; padding: 8px 12px; border-radius: 8px; border-left: 4px solid #28a745;">
                        <span style="font-size: 0.8em; color: #6c757d;">Fan Speed</span><br>
                        <strong style="font-size: 1.2em; color: #212529;">{fan_speed_pct:.1f} %</strong>
                    </div>
                    <div style="background: white; padding: 8px 12px; border-radius: 8px; border-left: 4px solid #ffc107;">
                        <span style="font-size: 0.8em; color: #6c757d;">Error</span><br>
                        <strong style="font-size: 1.2em; color: #212529;">{error:+.2f} °C</strong>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return html_code
