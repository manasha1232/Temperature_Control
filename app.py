"""
PID-Based Automatic Room Temperature and Fan Speed Control System
Streamlit Main Dashboard Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import time

from simulation.simulator import Simulator
from analysis.metrics import PerformanceAnalyzer
from visualization.plots import (
    plot_temperature,
    plot_fan_speed,
    plot_error,
    plot_controller_comparison,
    plot_open_vs_closed,
    render_fan_animation_html
)


def main():
    st.set_page_config(
        page_title="PID Room Temp & Fan Control Simulator",
        page_icon="🌡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom Engineering Style CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E293B;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.1rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-top: 4px solid #3B82F6;
            text-align: center;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<div class="main-header">🌡️ PID Room Temperature & Fan Control System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Software-Only Engineering Control System Simulator & Performance Analyzer</div>', unsafe_allow_html=True)

    # Sidebar Configuration
    st.sidebar.header("⚙️ Simulation Controls")

    # Preset Selection
    preset = st.sidebar.selectbox(
        "Load Preset Scenario",
        ["Default Demo Scenario", "Hot Summer Day", "Mild Room Cooling", "High Heat Disturbance"]
    )

    if preset == "Hot Summer Day":
        default_setpoint = 22.0
        default_init = 36.0
        default_ambient = 34.0
    elif preset == "Mild Room Cooling":
        default_setpoint = 24.0
        default_init = 28.0
        default_ambient = 27.0
    elif preset == "High Heat Disturbance":
        default_setpoint = 24.0
        default_init = 32.0
        default_ambient = 30.0
    else:
        default_setpoint = 24.0
        default_init = 32.0
        default_ambient = 30.0

    st.sidebar.subheader("1. Room Thermal Plant")
    setpoint = st.sidebar.slider("Desired Temperature (°C)", 15.0, 35.0, default_setpoint, 0.5)
    initial_temp = st.sidebar.slider("Initial Temperature (°C)", 15.0, 45.0, default_init, 0.5)
    ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 10.0, 45.0, default_ambient, 0.5)
    tau = st.sidebar.slider("Time Constant τ (s)", 10.0, 300.0, 60.0, 5.0)
    k_f = st.sidebar.slider("Fan Cooling Power (Kf)", 0.05, 0.50, 0.20, 0.01)
    duration = st.sidebar.slider("Simulation Time (s)", 60.0, 600.0, 300.0, 30.0)

    st.sidebar.subheader("2. PID Controller Parameters")
    controller_mode = st.sidebar.radio("Controller Mode", ["PID", "PI", "P", "Open-Loop"], index=0)

    col_kp, col_ki, col_kd = st.sidebar.columns(3)
    with col_kp:
        Kp = st.number_input("Kp", min_value=0.0, max_value=10.0, value=1.2, step=0.1)
    with col_ki:
        Ki = st.number_input("Ki", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
    with col_kd:
        Kd = st.number_input("Kd", min_value=0.0, max_value=5.0, value=0.20, step=0.05)

    open_loop_speed = 0.50
    if controller_mode == "Open-Loop":
        open_loop_speed = st.sidebar.slider("Open-Loop Fixed Fan Speed", 0.0, 1.0, 0.50, 0.05)

    st.sidebar.subheader("3. Heat Disturbances")
    enable_d1 = st.sidebar.checkbox("Enable Disturbance 1 (t=100s)", value=True)
    d1_mag = st.sidebar.slider("Disturbance 1 (°C/s)", 0.01, 0.10, 0.03, 0.01) if enable_d1 else 0.0

    enable_d2 = st.sidebar.checkbox("Enable Disturbance 2 (t=200s)", value=True)
    d2_mag = st.sidebar.slider("Disturbance 2 (°C/s)", 0.01, 0.10, 0.03, 0.01) if enable_d2 else 0.0

    disturbances = []
    if enable_d1:
        disturbances.append({"time": 100.0, "magnitude": d1_mag})
    if enable_d2:
        disturbances.append({"time": 200.0, "magnitude": d2_mag})

    # Instantiate Simulator
    simulator = Simulator()

    # Run Simulation
    df = simulator.run_simulation(
        mode=controller_mode,
        setpoint=setpoint,
        initial_temp=initial_temp,
        ambient_temp=ambient_temp,
        tau=tau,
        k_f=k_f,
        Kp=Kp,
        Ki=Ki,
        Kd=Kd,
        open_loop_fan_speed=open_loop_speed,
        disturbances=disturbances,
        duration=duration
    )

    metrics = PerformanceAnalyzer.calculate_metrics(df)

    # Top KPI Cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Final Temp", f"{df['temperature'].iloc[-1]:.2f} °C", f"{df['temperature'].iloc[-1] - setpoint:+.2f} °C")
    with col2:
        st.metric("Setpoint", f"{setpoint:.2f} °C")
    with col3:
        st.metric("Final Fan Speed", f"{df['fan_speed_pct'].iloc[-1]:.1f} %")
    with col4:
        st.metric("Rise Time", f"{metrics['Rise Time (s)']} s" if isinstance(metrics['Rise Time (s)'], float) else metrics['Rise Time (s)'])
    with col5:
        st.metric("Settling Time", f"{metrics['Settling Time (s)']} s" if isinstance(metrics['Settling Time (s)'], (float, int)) else metrics['Settling Time (s)'])
    with col6:
        st.metric("SS Error", f"{metrics['Steady-State Error (°C)']} °C")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Live Simulation & Fan Visualizer",
        "🔄 P vs PI vs PID Comparison",
        "⚡ Open-Loop vs Closed-Loop",
        "📐 Detailed Performance Metrics"
    ])

    # Tab 1: Live Simulation & Fan Visualizer
    with tab1:
        st.subheader("Real-Time Fan Speed & Room Environment Visualization")
        
        final_temp = df["temperature"].iloc[-1]
        final_fan = df["fan_speed_pct"].iloc[-1]
        final_err = df["error"].iloc[-1]

        # Animated Fan HTML
        fan_html = render_fan_animation_html(final_fan, final_temp, setpoint, final_err)
        st.components.v1.html(fan_html, height=180)

        st.subheader("Simulation Response Curves")
        fig_temp = plot_temperature(df, disturbances=disturbances, title=f"Room Temperature Response ({controller_mode} Mode)")
        st.pyplot(fig_temp)

        col_left, col_right = st.columns(2)
        with col_left:
            fig_fan = plot_fan_speed(df, title=f"Fan Control Speed ({controller_mode} Mode)")
            st.pyplot(fig_fan)
        with col_right:
            fig_err = plot_error(df, title=f"Temperature Error ({controller_mode} Mode)")
            st.pyplot(fig_err)

    # Tab 2: P vs PI vs PID Comparison
    with tab2:
        st.subheader("Comparative Analysis: P vs PI vs PID Controllers")
        st.write("Evaluate how Proportional (P), Integral (I), and Derivative (D) terms affect transient speed, steady-state error, overshoot, and disturbance rejection.")

        df_p = simulator.run_simulation(
            mode="P", setpoint=setpoint, initial_temp=initial_temp, ambient_temp=ambient_temp,
            tau=tau, k_f=k_f, Kp=Kp, Ki=Ki, Kd=Kd, disturbances=disturbances, duration=duration
        )
        df_pi = simulator.run_simulation(
            mode="PI", setpoint=setpoint, initial_temp=initial_temp, ambient_temp=ambient_temp,
            tau=tau, k_f=k_f, Kp=Kp, Ki=Ki, Kd=Kd, disturbances=disturbances, duration=duration
        )
        df_pid = simulator.run_simulation(
            mode="PID", setpoint=setpoint, initial_temp=initial_temp, ambient_temp=ambient_temp,
            tau=tau, k_f=k_f, Kp=Kp, Ki=Ki, Kd=Kd, disturbances=disturbances, duration=duration
        )

        fig_comp = plot_controller_comparison(df_p, df_pi, df_pid, disturbances=disturbances)
        st.pyplot(fig_comp)

        # Performance Comparison Table
        metrics_p = PerformanceAnalyzer.calculate_metrics(df_p)
        metrics_pi = PerformanceAnalyzer.calculate_metrics(df_pi)
        metrics_pid = PerformanceAnalyzer.calculate_metrics(df_pid)

        comp_df = pd.DataFrame([metrics_p, metrics_pi, metrics_pid], index=["P Controller", "PI Controller", "PID Controller"])
        st.subheader("Performance Metrics Comparison Table")
        st.table(comp_df)

        st.info("""
        **Controller Comparison Key Insights:**
        - **P Controller**: Provides fast initial cooling response proportional to error, but leaves a **steady-state offset** because fan speed drops as error decreases.
        - **PI Controller**: Accumulates past error via Integral action, completely **eliminating steady-state error** and restoring setpoint even under continuous disturbances.
        - **PID Controller**: Adds Derivative action to anticipate temperature changes, **damping overshoot** and stabilizing thermal recovery when sudden disturbances occur.
        """)

    # Tab 3: Open-Loop vs Closed-Loop
    with tab3:
        st.subheader("Open-Loop vs Closed-Loop Control System Demonstration")
        st.write("Demonstrates why feedback is required for automatic disturbance rejection.")

        df_open = simulator.run_simulation(
            mode="Open-Loop", setpoint=setpoint, initial_temp=initial_temp, ambient_temp=ambient_temp,
            tau=tau, k_f=k_f, open_loop_fan_speed=open_loop_speed, disturbances=disturbances, duration=duration
        )

        fig_ol_cl = plot_open_vs_closed(df_open, df, disturbances=disturbances)
        st.pyplot(fig_ol_cl)

        col_ol, col_cl = st.columns(2)
        with col_ol:
            st.markdown("""
            ### ❌ Open-Loop Control
            - **No Feedback**: Fan speed remains fixed at preset rate (e.g. 50%).
            - **Fails on Disturbance**: When heat enters room at $t=100\text{s}$, room temperature drifts upward uncontrollably.
            - **High Steady-State Error**: Incapable of adjusting fan speed to reach desired setpoint.
            """)
        with col_cl:
            st.markdown("""
            ### ✅ Closed-Loop PID Control
            - **Continuous Feedback**: Sensor continuously feeds room temperature back to controller.
            - **Automatic Disturbance Rejection**: When heat enters at $t=100\text{s}$, PID detects error spike and automatically ramps up fan speed.
            - **Zero Steady-State Error**: Automatically maintains setpoint temperature.
            """)

    # Tab 4: Detailed Performance Metrics
    with tab4:
        st.subheader("Complete Performance Metrics Breakdown")
        
        metrics_df = pd.DataFrame(list(metrics.items()), columns=["Metric Parameter", "Calculated Value"])
        st.table(metrics_df)

        st.subheader("Simulation Time-Series Data")
        st.dataframe(df, use_container_width=True)

        # Download CSV option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Simulation Data (CSV)",
            data=csv,
            file_name="temperature_control_simulation.csv",
            mime="text/csv"
        )




if __name__ == "__main__":
    main()
