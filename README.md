# PID-Based Automatic Room Temperature and Fan Speed Control System

A complete, software-only engineering mini project demonstrating automatic room temperature and fan speed control using PID controllers, plant dynamics simulation, performance metrics analysis, and an interactive Streamlit dashboard.

---

## 1. Project Title
**PID-Based Automatic Room Temperature and Fan Speed Control System**

---

## 2. Problem Statement
Manual control of room temperature using fixed fan speed settings is inefficient and fails to compensate for ambient thermal variations or external heat disturbances (such as electronic appliances or room occupancy). Closed-loop control is required to continuously measure temperature, compute error, and automatically regulate fan cooling power to maintain thermal comfort.

---

## 3. Objective
- Develop a software-only simulation of room thermal dynamics and fan speed control.
- Implement Proportional (P), Proportional-Integral (PI), and Proportional-Integral-Derivative (PID) controllers with anti-windup protection.
- Demonstrate disturbance rejection and compare Open-Loop vs Closed-Loop feedback performance.
- Automatically calculate control performance metrics: Rise Time, Settling Time, Overshoot %, Steady-State Error, Peak Error, Integral Absolute Error (IAE), and Integral Squared Error (ISE).
- Provide an interactive web dashboard with dynamic fan speed animation and viva-friendly educational resources.

---

## 4. Motivation
Physical hardware setups (Arduino, sensors, relays, fans) can be costly, prone to physical noise, and limited in tuning flexibility. A software-only simulator allows control engineering students and researchers to inspect plant dynamics, experiment with PID gains, analyze disturbances, and visualize feedback control theory cleanly without hardware requirements.

---

## 5. Control System Architecture
The system operates as a negative-feedback closed-loop control system:
1. **Setpoint ($T_{\text{set}}$)**: User-defined desired temperature (°C).
2. **Sensor / Feedback**: Continuous measurement of simulated room temperature $T(t)$.
3. **Error Detector**: Calculates cooling error $e(t) = T(t) - T_{\text{set}}$.
4. **PID Controller**: Computes required fan signal $u(t) \in [0.0, 1.0]$.
5. **Actuator**: Fan cooling mechanism running between 0% and 100% speed.
6. **Plant**: Room thermal environment governed by first-order differential equations.
7. **Disturbance ($Q$)**: External heat influx (step heat additions at scheduled timestamps).

---

## 6. Mathematical Model

### Room Thermal Differential Equation
$$\frac{dT}{dt} = -\frac{T - T_{\text{ambient}}}{\tau} - K_f \cdot u + Q$$

Where:
- $T$: Room temperature (°C)
- $T_{\text{ambient}}$: Ambient/outside temperature (°C, default: 30°C)
- $\tau$: Thermal time constant (seconds, default: 60s)
- $K_f$: Cooling effectiveness coefficient of fan (°C/(s · normalized_u), default: 0.20)
- $u$: Fan control signal normalized to $[0.0, 1.0]$ (0% to 100% speed)
- $Q$: External heat disturbance rate (°C/s)

---

## 7. PID Controller Theory

### PID Control Law
$$u(t) = \text{clamp}\left(K_p e(t) + K_i \int_0^t e(\tau)d\tau + K_d \frac{de(t)}{dt}, 0.0, 1.0\right)$$

- **Proportional Term ($K_p e(t)$)**: Produces control action proportional to current temperature error.
- **Integral Term ($K_i \int e(t)dt$)**: Accumulates past error to eliminate steady-state offset.
- **Derivative Term ($K_d \frac{de}{dt}$)**: Responds to rate of error change to damp overshoot and stabilize transient response.
- **Anti-Windup Protection**: Integrator accumulation pauses when control output saturates at 0% or 100%, preventing severe overshoot delays upon returning from saturation.

---

## 8. Block Diagrams

### High-Level Closed-Loop Block Diagram
```
             +---------------------------------------+
             |                                       |
             ↓                                       |
Setpoint --> (+) --> Error --> PID Controller --> Fan Speed --> Room Thermal Plant
  T_set      (-)                   u(t)                       T_actual
                      |                                                  |
                      |                                                  |
                      +-------------- Temperature Feedback --------------+
```

### Detailed Signal Flow Diagram
```
Reference Temp (T_set)
       │
       ▼
   Comparator ──(Error e)──► PID Controller ──(Control Signal u)──► Fan Cooling Model
       ▲                                                                   │
       │                                                                   ▼
       └──────── Sensor Feedback ◄── Actual Temp (T) ◄── Room Thermal Plant (dT/dt)
                                                                   ▲
                                                                   │
                                                           Heat Disturbance (Q)
```

---

## 9. Algorithm

```
1. Initialize RoomModel with initial_temp, ambient_temp, tau, k_f.
2. Initialize Controller (P, PI, or PID) with gains Kp, Ki, Kd.
3. For time t = 0 to duration with step dt:
    a. Determine active heat disturbance Q(t).
    b. Measure current room temperature T(t).
    c. Compute error e(t) = T(t) - T_setpoint.
    d. If Open-Loop mode: u = open_loop_speed.
       Else: Compute u(t), e(t) using Controller.compute(setpoint, T(t), dt).
    e. Record state: {t, T(t), T_setpoint, u(t), error, Q(t)}.
    f. Advance room model: T(t+dt) = room.step(u(t), Q(t), dt).
4. Compute performance metrics (Rise Time, Settling Time, Overshoot, SS Error, IAE, ISE).
5. Render dynamic graphs and animated fan SVG widget in dashboard.
```

---

## 10. Software Requirements
- **Python**: 3.9+ (Tested on Python 3.14)
- **Libraries**:
  - `numpy`
  - `scipy`
  - `pandas`
  - `matplotlib`
  - `streamlit`

---

## 11. Installation

1. Open terminal / PowerShell in project root directory:
   ```bash
   cd temperature_control
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 12. How to Run

### Run Automated Unit Verification Test
```bash
python test_simulation.py
```

### Run Interactive Streamlit Dashboard
```bash
python -m streamlit run app.py
```

---

## 13. Simulation Results

- **P Controller**: Provides rapid initial cooling, but leaves a steady-state error (e.g. $\sim 0.9^\circ\text{C}$) because fan speed drops as error decreases.
- **PI Controller**: Completely eliminates steady-state error ($e_{ss} < 0.01^\circ\text{C}$), restoring setpoint temperature even under continuous external heat disturbances.
- **PID Controller**: Delivers smooth, well-damped cooling response with minimal overshoot, fast settling time, and robust disturbance rejection.

---

## 14. Performance Metrics

| Metric | Definition |
| :--- | :--- |
| **Rise Time ($T_r$)** | Time required for response to move from 10% to 90% of total temperature change |
| **Settling Time ($T_s$)** | Time required for temperature to stay within $\pm 2\%$ tolerance band of setpoint |
| **Overshoot (%)** | Maximum percentage temperature drop below setpoint |
| **Steady-State Error ($e_{ss}$)** | $|T(t_{\text{final}}) - T_{\text{setpoint}}|$ |
| **Peak Error** | Maximum absolute error $\max_t |T(t) - T_{\text{setpoint}}|$ |
| **IAE** | Integral Absolute Error: $\int |e(t)| dt$ |
| **ISE** | Integral Squared Error: $\int e(t)^2 dt$ |

---

## 15. P vs PI vs PID Comparison

| Characteristic | P Controller | PI Controller | PID Controller |
| :--- | :--- | :--- | :--- |
| **Transient Speed** | Fast | Moderate | Fast & Damped |
| **Steady-State Error** | Present ($e_{ss} > 0$) | Zero ($e_{ss} \approx 0$) | Zero ($e_{ss} \approx 0$) |
| **Overshoot** | Low | Moderate | Low (Damped by $K_d$) |
| **Disturbance Rejection** | Partial | Complete | Complete & Rapid |

---

## 16. Advantages
- **Software-Only**: Requires no physical hardware, sensors, or microcontroller boards.
- **Interactive Tuning**: Real-time slider adjustments for Kp, Ki, Kd, time constant, ambient temperature, and disturbances.
- **Visual Real-Time Animation**: Dynamic fan speed blade rotation and thermometer visualizer.
- **Comprehensive Metrics**: Automatic mathematical evaluation of control quality.

---

## 17. Limitations
- Thermal model assumes uniform room air mixing (single thermal node model).
- Fan actuator power saturation is limited to 100% capacity ($K_f \cdot 1.0$).
- Environmental ambient temperature is modeled as constant during single simulation runs.

---

## 18. Future Improvements
- Multi-zone thermal modeling (multiple rooms/walls).
- Variable ambient temperature profile (day/night diurnal cycle).
- Fuzzy Logic and Auto-Tuning PID algorithms (Ziegler-Nichols method).

---

## 19. Conclusion
This project successfully demonstrates a software-only simulation of an automatic room temperature control system. Closed-loop PID control dynamically adjusts fan speed to maintain target temperatures, eliminate steady-state offsets, and reject heat disturbances, providing a practical platform for control systems education.
