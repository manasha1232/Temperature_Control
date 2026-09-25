"""
Proportional (P) Controller Module
Control Law: u(t) = clamp(Kp * e(t), 0, 1)

Error Convention for Cooling:
    e(t) = T_actual(t) - T_setpoint
    When room is hotter than setpoint (T_actual > T_setpoint), e(t) > 0, driving fan speed u > 0.
"""

class PController:
    def __init__(self, Kp: float = 1.2):
        """
        Initialize Proportional Controller.

        Parameters:
            Kp (float): Proportional gain
        """
        self.Kp = float(Kp)

    def reset(self):
        """Reset controller internal state (stateless for P controller)."""
        pass

    def compute(self, setpoint: float, current_temp: float, dt: float = 0.1) -> tuple[float, float]:
        """
        Calculate control output u(t) and error e(t).

        Parameters:
            setpoint (float): Desired target temperature (°C)
            current_temp (float): Actual room temperature (°C)
            dt (float): Time step (seconds)

        Returns:
            tuple[float, float]: (fan_control_signal u in [0, 1], error e in °C)
        """
        # Cooling error: room temperature minus desired setpoint
        error = current_temp - setpoint
        
        # Unconstrained control output
        u_raw = self.Kp * error
        
        # Clamp output to fan limits [0.0, 1.0] (0% to 100%)
        u = max(0.0, min(1.0, u_raw))
        return u, error
