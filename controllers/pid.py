"""
Proportional-Integral-Derivative (PID) Controller Module
Control Law: u(t) = clamp(Kp * e(t) + Ki * integral(e(t)) + Kd * de(t)/dt, 0, 1)

Features:
- Anti-Windup Clamping on Integral Term
- Smooth Derivative on Error
- Settable Gains Kp, Ki, Kd
"""

class PIDController:
    def __init__(self, Kp: float = 1.2, Ki: float = 0.05, Kd: float = 0.20):
        """
        Initialize PID Controller.

        Parameters:
            Kp (float): Proportional gain
            Ki (float): Integral gain
            Kd (float): Derivative gain
        """
        self.Kp = float(Kp)
        self.Ki = float(Ki)
        self.Kd = float(Kd)
        self.integral = 0.0
        self.prev_error = 0.0
        self.first_step = True

    def reset(self):
        """Reset internal integrator and derivative states."""
        self.integral = 0.0
        self.prev_error = 0.0
        self.first_step = True

    def compute(self, setpoint: float, current_temp: float, dt: float = 0.1) -> tuple[float, float]:
        """
        Calculate control output u(t) and error e(t) using PID control law with anti-windup.

        Parameters:
            setpoint (float): Desired target temperature (°C)
            current_temp (float): Actual room temperature (°C)
            dt (float): Time step (seconds)

        Returns:
            tuple[float, float]: (fan_control_signal u in [0, 1], error e in °C)
        """
        error = current_temp - setpoint
        
        # Derivative term calculation
        if self.first_step:
            derivative = 0.0
            self.first_step = False
        else:
            derivative = (error - self.prev_error) / dt if dt > 0 else 0.0

        # Tentative integral accumulate
        tentative_integral = self.integral + error * dt
        
        # Raw unconstrained PID control signal
        u_raw = self.Kp * error + self.Ki * tentative_integral + self.Kd * derivative
        
        # Anti-Windup Clamping
        if 0.0 <= u_raw <= 1.0:
            self.integral = tentative_integral
        elif u_raw > 1.0 and error < 0.0:
            self.integral = tentative_integral
        elif u_raw < 0.0 and error > 0.0:
            self.integral = tentative_integral

        self.prev_error = error
        
        # Final saturated fan output
        u = max(0.0, min(1.0, u_raw))
        return u, error
