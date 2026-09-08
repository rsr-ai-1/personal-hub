"""PID Controller for Drone Altitude Hold."""


class AltitudePID:
    def __init__(self, kp: float, ki: float, kd: float, target_altitude: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.target = target_altitude
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, current_altitude: float, dt: float = 0.1) -> float:
        """Calculates thrust adjustment to reach target altitude."""
        error = self.target - current_altitude
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error

        # PID formula
        thrust_adjustment = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        return thrust_adjustment


if __name__ == "__main__":
    controller = AltitudePID(kp=1.2, ki=0.05, kd=0.3, target_altitude=10.0)
    current_alt = 0.0  # starting on the ground

    print("Simulating takeoff to 10m target:")
    for step in range(5):
        output = controller.compute(current_altitude=current_alt, dt=0.5)
        current_alt += output * 0.5  # mock physics update
        print(f"Step {step + 1}: Current Alt = {current_alt:.2f}m | Thrust Adj = {output:.2f}")
