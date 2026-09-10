//! High-Precision Discrete PID Controller for Autonomous Flight Systems
//! Target: Embedded Systems / no_std compatible logic

#[derive(Debug, Clone, Copy)]
pub struct PidGains {
    pub kp: f64,
    pub ki: f64,
    pub kd: f64,
}

#[derive(Debug)]
pub struct FlightPidController {
    gains: PidGains,
    integral: f64,
    previous_error: f64,
    output_min: f64,
    output_max: f64,
}

impl FlightPidController {
    pub fn new(gains: PidGains, output_min: f64, output_max: f64) -> Self {
        Self {
            gains,
            integral: 0.0,
            previous_error: 0.0,
            output_min,
            output_max,
        }
    }

    pub fn compute(&mut self, setpoint: f64, measurement: f64, dt: f64) -> f64 {
        let error = setpoint - measurement;
        
        // Anti-windup integrated accumulation
        self.integral += error * dt;
        
        // Derivative on error
        let derivative = if dt > 0.0 {
            (error - self.previous_error) / dt
        } else {
            0.0
        };

        let raw_output = (self.gains.kp * error) 
            + (self.gains.ki * self.integral) 
            + (self.gains.kd * derivative);

        self.previous_error = error;

        // Saturation clamping
        raw_output.clamp(self.output_min, self.output_max)
    }

    pub fn reset(&mut self) {
        self.integral = 0.0;
        self.previous_error = 0.0;
    }
}

fn main() {
    let gains = PidGains { kp: 1.25, ki: 0.05, kd: 0.4 };
    let mut controller = FlightPidController::new(gains, -100.0, 100.0);

    let target_altitude = 50.0; // meters
    let mut current_altitude = 0.0;
    let dt = 0.1; // 100ms cycle

    println!("--- Initializing Rust PID Control Loop ---");
    for step in 1..=10 {
        let throttle = controller.compute(target_altitude, current_altitude, dt);
        current_altitude += throttle * 0.08;
        println!("Step {:02} | Alt: {:5.2}m | Command: {:5.2}%", step, current_altitude, throttle);
    }
}
