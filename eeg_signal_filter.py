"""Brain-Computer Interface (BCI) EEG Alpha-Wave (8-12 Hz) Detector."""

import math


def generate_synthetic_eeg(sampling_rate: int = 250, duration_sec: float = 1.0) -> list[float]:
    """Generates synthetic EEG signal containing noise and an intentional 10 Hz alpha burst."""
    total_samples = int(sampling_rate * duration_sec)
    signal = []

    for i in range(total_samples):
        t = i / sampling_rate
        # Baseline noise (low frequency drift + high frequency jitter)
        noise = 0.5 * math.sin(2 * math.pi * 2 * t) + 0.2 * math.sin(2 * math.pi * 50 * t)
        # Alpha-band event (10 Hz oscillation) triggered halfway through
        alpha_burst = 2.0 * math.sin(2 * math.pi * 10 * t) if t > 0.4 else 0.0
        signal.append(noise + alpha_burst)

    return signal


class BCIAlphaDetector:
    def __init__(self, sampling_rate: int = 250):
        self.fs = sampling_rate

    def estimate_power(self, signal: list[float], target_freq: float = 10.0) -> float:
        """Estimates frequency power at target_freq via Discrete Fourier Transform (Goertzel/DFT projection)."""
        n = len(signal)
        omega = 2.0 * math.pi * target_freq / self.fs
        real_part = sum(signal[k] * math.cos(omega * k) for k in range(n))
        imag_part = sum(signal[k] * math.sin(omega * k) for k in range(n))
        power = (real_part**2 + imag_part**2) / (n**2)
        return power

    def decode_command(self, signal_window: list[float], threshold: float = 0.15) -> str:
        """Translates alpha wave presence into a robotic actuation trigger."""
        alpha_power = self.estimate_power(signal_window, target_freq=10.0)
        if alpha_power > threshold:
            return f"TRIGGER COMMAND (Alpha Power: {alpha_power:.3f} >= {threshold})"
        return f"IDLE (Alpha Power: {alpha_power:.3f} < {threshold})"


if __name__ == "__main__":
    fs = 250  # 250 Hz sample rate
    eeg_data = generate_synthetic_eeg(sampling_rate=fs, duration_sec=1.0)
    bci = BCIAlphaDetector(sampling_rate=fs)

    # Window 1: Rest state (0.0s to 0.4s)
    rest_window = eeg_data[:100]
    # Window 2: Focused motor cortex intent (0.5s to 0.9s)
    intent_window = eeg_data[125:225]

    print("--- Brain-Computer Interface Command Decoder ---")
    print("Window 1 (Rest):  ", bci.decode_command(rest_window))
    print("Window 2 (Intent):", bci.decode_command(intent_window))
