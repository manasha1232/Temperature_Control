"""
Plant Model: Room Thermal Dynamics
Mathematical representation of a room's thermal behavior.

Differential Equation:
    dT/dt = -(T - T_ambient) / tau - K_f * u + Q

Where:
    T          : Current room temperature (°C)
    T_ambient  : Outside/ambient temperature (°C)
    tau        : Thermal time constant of the room (seconds)
    K_f        : Fan cooling effectiveness coefficient (°C / (s * normalized_u))
    u          : Fan control signal in [0.0, 1.0] (0% to 100%)
    Q          : Heat disturbance rate (°C / s)
"""

class RoomModel:
    def __init__(
        self,
        initial_temp: float = 32.0,
        ambient_temp: float = 30.0,
        tau: float = 60.0,
        k_f: float = 0.20
    ):
        """
        Initialize the Room Thermal Plant Model.

        Parameters:
            initial_temp (float): Starting room temperature (°C)
            ambient_temp (float): Outside ambient temperature (°C)
            tau (float): Room thermal time constant (seconds)
            k_f (float): Fan cooling power coefficient (°C/(s*u))
        """
        self.initial_temp = float(initial_temp)
        self.ambient_temp = float(ambient_temp)
        self.tau = float(tau)
        self.k_f = float(k_f)
        self.current_temp = float(initial_temp)

    def reset(self, initial_temp: float = None):
        """Reset the room temperature to initial state."""
        if initial_temp is not None:
            self.initial_temp = float(initial_temp)
        self.current_temp = self.initial_temp

    def compute_dT_dt(self, T: float, u: float, Q: float = 0.0) -> float:
        """
        Compute rate of temperature change (dT/dt).

        Parameters:
            T (float): Current temperature (°C)
            u (float): Normalized fan control signal [0.0, 1.0]
            Q (float): External heat disturbance (°C/s)

        Returns:
            float: dT/dt rate of change (°C/s)
        """
        # Clamp fan signal between 0 and 1
        u_clamped = max(0.0, min(1.0, float(u)))
        
        # Natural thermal dissipation to ambient + fan cooling effect + external heat
        dT_dt = -(T - self.ambient_temp) / self.tau - self.k_f * u_clamped + Q
        return dT_dt

    def step(self, u: float, Q: float = 0.0, dt: float = 0.1) -> float:
        """
        Advance room simulation by time step dt using Euler numerical integration.

        Parameters:
            u (float): Fan speed control signal [0.0, 1.0]
            Q (float): External heat disturbance rate (°C/s)
            dt (float): Integration step size (seconds)

        Returns:
            float: Updated room temperature (°C)
        """
        dT_dt = self.compute_dT_dt(self.current_temp, u, Q)
        self.current_temp += dT_dt * dt
        return self.current_temp
