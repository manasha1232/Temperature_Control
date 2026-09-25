# Control System Architecture Diagram

## PID-Based Automatic Room Temperature and Fan Speed Control System

Below is the complete 2D engineering block diagram illustrating the closed-loop negative feedback system, including the comparator, PID controller, fan cooling actuator, room thermal plant ODE, external heat disturbance influx, and temperature sensor feedback loop.

![Control System Architecture Diagram](file:///C:/Users/manas/.gemini/antigravity/scratch/temperature_control/architecture_diagram.jpg)

---

### Diagram Breakdown & Signal Flow

1. **Desired Temperature Setpoint ($T_{\text{set}}$)**: Input target room temperature (e.g. 24.0°C).
2. **Comparator Junction**: Calculates instantaneous error signal $e(t) = T(t) - T_{\text{set}}$.
3. **PID Controller**: Evaluates Proportional, Integral, and Derivative terms with Anti-Windup protection to compute raw control output.
4. **Fan Cooling Actuator**: Normalizes control output $u(t)$ to physical fan bounds $[0\%, 100\%]$.
5. **Room Thermal Plant Dynamics**: Solves first-order differential equation:
   $$\frac{dT}{dt} = -\frac{T - T_{\text{ambient}}}{\tau} - K_f \cdot u + Q$$
6. **External Heat Disturbance ($Q(t)$)**: Heat influx entering plant at scheduled times ($t=100\text{s}$ and $t=200\text{s}$).
7. **Temperature Sensor & Feedback**: Measures actual room temperature $T(t)$ and feeds back to comparator to maintain closed-loop control.
