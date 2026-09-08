"""Neuromorphic Leaky Integrate-and-Fire (LIF) Spiking Neuron Simulation."""

from dataclasses import dataclass


@dataclass
class LIFNeuron:
    tau_m: float = 10.0          # Membrane time constant (ms)
    v_rest: float = -70.0        # Resting potential (mV)
    v_reset: float = -75.0       # Post-spike reset potential (mV)
    v_thresh: float = -50.0      # Action potential firing threshold (mV)
    refractory_period: float = 2.0  # Refractory period duration (ms)

    def __post_init__(self):
        self.v_membrane = self.v_rest
        self.refractory_timer = 0.0

    def step(self, i_input: float, dt: float = 0.5) -> bool:
        """Simulates one time step. Returns True if an action potential spike fires."""
        if self.refractory_timer > 0.0:
            self.refractory_timer -= dt
            self.v_membrane = self.v_reset
            return False

        # Leaky integration: dV/dt = (-(V - V_rest) + R*I) / tau
        # Assuming membrane resistance R = 1.0
        dv = (-(self.v_membrane - self.v_rest) + i_input) / self.tau_m * dt
        self.v_membrane += dv

        # Spike detection
        if self.v_membrane >= self.v_thresh:
            self.v_membrane = self.v_reset
            self.refractory_timer = self.refractory_period
            return True

        return False


if __name__ == "__main__":
    neuron = LIFNeuron()
    simulation_duration_ms = 40.0
    dt_step = 1.0
    input_current = 25.0  # Constant injected micro-current

    print(f"Simulating LIF Neuron (Input Current = {input_current} pA):")
    print("Time(ms) | Membrane(mV) | Event")
    print("-" * 35)

    current_time = 0.0
    while current_time <= simulation_duration_ms:
        spiked = neuron.step(i_input=input_current, dt=dt_step)
        event_str = "⚡ SPIKE!" if spiked else ("(Refractory)" if neuron.refractory_timer > 0 else "")
        print(f"{current_time:7.1f} | {neuron.v_membrane:11.2f} | {event_str}")
        current_time += dt_step
