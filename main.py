"""
Master Entry Point for Personal Hub Simulations & Systems.
Run this script to launch any project demonstration interactively.
"""

import subprocess
import sys

MODULES = {
    "1": ("Drone State Telemetry", "drone_telemetry.py"),
    "2": ("PID Altitude Controller", "pid_controller.py"),
    "3": ("2D Obstacle Avoidance", "obstacle_avoidance.py"),
    "4": ("Flight Telemetry Logger", "flight_logger.py"),
    "5": ("Reynolds Boids Swarm Flocking", "swarm_flocking.py"),
    "6": ("EKF GPS-Denied Localization", "ekf_localization.py"),
    "7": ("Planar Robotic Arm Kinematics", "arm_kinematics.py"),
    "8": ("LIF Spiking Neuron Simulation", "lif_neuron_sim.py"),
    "9": ("Multi-Agent Planner Loop", "multi_agent_system.py"),
    "10": ("Post-Quantum LWE Encryption", "toy_lwe_encryption.py"),
    "11": ("BCI EEG Alpha Bandpass Filter", "eeg_signal_filter.py"),
}

def display_menu():
    print("\n" + "=" * 50)
    print("      PERSONAL HUB SIMULATION SUITE")
    print("=" * 50)
    for key, (name, _) in MODULES.items():
        print(f" [{key:>2}] {name}")
    print(" [ 0] Run All Modules Sequentially")
    print(" [ q] Quit")
    print("-" * 50)

def run_script(script_name: str):
    print(f"\n---> Executing {script_name}...\n")
    result = subprocess.run([sys.executable, script_name])
    if result.returncode == 0:
        print(f"\n[PASS] {script_name} completed successfully.")
    else:
        print(f"\n[FAIL] {script_name} exited with code {result.returncode}.")

def main():
    while True:
        display_menu()
        choice = input("Select an option: ").strip().lower()

        if choice in ("q", "quit", "exit"):
            print("Exiting suite. Goodbye!")
            break
        elif choice == "0":
            for _, filename in MODULES.values():
                run_script(filename)
        elif choice in MODULES:
            _, filename = MODULES[choice]
            run_script(filename)
        else:
            print("[!] Invalid choice, please try again.")

if __name__ == "__main__":
    main()
