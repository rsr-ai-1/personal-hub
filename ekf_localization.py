"""1D Extended Kalman Filter (EKF) for GPS-Denied Autonomous Navigation."""

import math
import random


class EKF1D:
    def __init__(self, initial_pos: float = 0.0, initial_vel: float = 1.0):
        # State: [position, velocity]
        self.x = initial_pos
        self.v = initial_vel

        # Estimate error covariance
        self.p_pos = 1.0
        self.p_vel = 1.0

        # Process noise (system uncertainty)
        self.q_pos = 0.05
        self.q_vel = 0.05

        # Measurement noise (sensor uncertainty)
        self.r_sensor = 0.5

    def predict(self, dt: float = 0.1, accel: float = 0.0):
        """Predicts the next state using dead-reckoning kinematics."""
        self.x += (self.v * dt) + (0.5 * accel * dt**2)
        self.v += accel * dt

        # Update error covariance
        self.p_pos += self.q_pos
        self.p_vel += self.q_vel

    def update(self, beacon_dist: float, beacon_pos: float):
        """Corrects state estimate using range-to-beacon measurement."""
        expected_dist = abs(self.x - beacon_pos)
        measurement_residual = beacon_dist - expected_dist

        # Kalman Gain for position
        k_pos = self.p_pos / (self.p_pos + self.r_sensor)

        # State correction
        direction = 1.0 if (self.x >= beacon_pos) else -1.0
        self.x += k_pos * measurement_residual * direction

        # Covariance correction
        self.p_pos *= (1.0 - k_pos)


if __name__ == "__main__":
    ekf = EKF1D(initial_pos=0.0, initial_vel=2.0)
    beacon_station = 15.0  # Fixed beacon location
    true_position = 0.0

    print("Step | True Pos | Sensor Dist | EKF Estimate | Error")
    print("-" * 55)

    for step in range(1, 8):
        dt = 0.5
        true_position += 2.0 * dt  # Moving at constant 2 m/s

        # Predict step
        ekf.predict(dt=dt)

        # Noisy beacon range reading (GPS-denied environment)
        noise = random.uniform(-0.6, 0.6)
        sensor_range = abs(beacon_station - true_position) + noise

        # Update step
        ekf.update(beacon_dist=sensor_range, beacon_pos=beacon_station)
        error = abs(true_position - ekf.x)

        print(f"{step:4d} | {true_position:8.2f} | {sensor_range:11.2f} | {ekf.x:12.2f} | {error:5.2f}")
