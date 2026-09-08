"""Flight Log Telemetry Recorder and ASCII Visualizer."""

from dataclasses import dataclass, field
import time


@dataclass
class TelemetryPoint:
    timestamp: float
    altitude: float
    battery: float


class FlightLogger:
    def __init__(self):
        self.logs: list[TelemetryPoint] = []

    def log(self, altitude: float, battery: float):
        self.logs.append(TelemetryPoint(timestamp=time.time(), altitude=altitude, battery=battery))

    def render_ascii_profile(self, max_height: int = 10):
        """Renders an ASCII elevation plot of the flight path."""
        if not self.logs:
            print("No telemetry logged.")
            return

        altitudes = [p.altitude for p in self.logs]
        peak = max(altitudes) if max(altitudes) > 0 else 1.0

        print("\n--- Flight Altitude Profile ---")
        for row in range(max_height, 0, -1):
            threshold = (row / max_height) * peak
            line = f"{threshold:5.1f}m | "
            for alt in altitudes:
                line += "█ " if alt >= threshold else "  "
            print(line)
        print("       +" + "--" * len(altitudes))
        print("        " + " ".join(str(i + 1) for i in range(len(altitudes))))
        print(f"Total Points: {len(self.logs)} | Peak Altitude: {peak:.1f}m\n")


if __name__ == "__main__":
    logger = FlightLogger()
    simulated_altitudes = [0.0, 2.2, 5.8, 9.4, 10.0, 10.1, 9.8, 6.2, 3.1, 0.0]
    battery = 100.0

    for alt in simulated_altitudes:
        logger.log(altitude=alt, battery=battery)
        battery -= 1.5

    logger.render_ascii_profile()
