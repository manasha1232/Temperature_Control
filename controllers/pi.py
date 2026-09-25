"""
Proportional-Integral (PI) Controller Module
Control Law: u(t) = clamp(Kp * e(t) + Ki * integral(e(t)), 0, 1)

Includes Anti-Windup Protection:
    Prevents integral term from growing unchecked when actuator (fan speed) is saturated at 0% or 100%.
"""

class PIController:
    def __init__(self, Kp: float = 1.2, Ki: float = 0.05):
        """
        Initialize PI Controller.

        Parameters:
            Kp (float): Proportional gain
            Ki (float): Integral gain
        """
        self.Kp = float(Kp)
        self.Ki = float(Ki)
        self.integral = 0.0

    def reset(self):
        """Reset accumulated integral error to zero."""
        self.integral = 0.0

    def compute(self, setpoint: float, current_temp: float, dt: float = 0.1) -> tuple[float, float]:
        """
        Calculate control output u(t) and error e(t) with anti-windup integral accumulation.

        Parameters:
            setpoint (float): Desired target temperature (°C)
            current_temp (float): Actual room temperature (°C)
            dt (float): Time step (seconds)

        Returns:
            tuple[float, float]: (fan_control_signal u in [0, 1], error e in °C)
        """
        error = current_temp - setpoint
        
        # Calculate tentative integral update
        tentative_integral = self.integral + error * dt
        
        # Calculate unconstrained raw output
        u_raw = self.Kp * error + self.Ki * tentative_integral
        
        # Anti-Windup Logic:
        # Only update integral state if output is within bounds OR if error acts to move output out of saturation
        if 0.0 <= u_raw <= 1.0:
            self.integral = tentative_integral
        elif u_raw > 1.0 and error < 0.0:
            self.integral = tentative_integral
        elif u_raw < 0.0 and error > 0.0:
            self.integral = tentative_integral
        
        # Clamp control signal to physical limits [0.0, 1.0]
        u = max(0.0, min(1.0, u_raw))
        return u, error
