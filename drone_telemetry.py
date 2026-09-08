"""Drone Telemetry & State Tracker."""

from dataclasses import dataclass
import time


@dataclass
class DroneState:
    altitude: float  # meters
    pitch: float     # degrees
    roll: float      # degrees
    yaw: float       # degrees
    battery: float   # percentage (0-100)

    def is_safe_to_fly(self) -> bool:
        """Safety checks before automated flight commands."""
        return self.battery > 20.0 and abs(self.pitch) < 30.0 and abs(self.roll) < 30.0

    def print_status(self) -> None:
        print(f"[{time.strftime('%H:%M:%S')}] Alt: {self.altitude}m | "
              f"Bat: {self.battery}% | Status: {'SAFE' if self.is_safe_to_fly() else 'ALERT'}")


if __name__ == "__main__":
    quad = DroneState(altitude=12.5, pitch=2.1, roll=-1.4, yaw=90.0, battery=85.0)
    quad.print_status()
