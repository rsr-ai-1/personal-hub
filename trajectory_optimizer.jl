# Non-linear Rocket Descent & Touchdown Optimizer
# High-precision numerical dynamics for autonomous landing

struct VehicleParams
    dry_mass::Float64       # kg
    fuel_mass::Float64      # kg
    isp::Float64            # Specific impulse (s)
    max_thrust::Float64     # N
    gravity::Float64        # m/s^2
end

mutable struct RocketState
    altitude::Float64       # m
    velocity::Float64       # m/s
    mass::Float64           # kg
end

function simulate_step(state::RocketState, thrust::Float64, dt::Float64, params::VehicleParams)
    clamped_thrust = clamp(thrust, 0.0, params.max_thrust)
    
    # Fuel depletion
    mass_flow = clamped_thrust / (params.isp * params.gravity)
    fuel_burn = mass_flow * dt
    state.mass = max(params.dry_mass, state.mass - fuel_burn)

    # Net acceleration (T - mg) / m
    accel = (clamped_thrust / state.mass) - params.gravity
    state.velocity += accel * dt
    state.altitude += state.velocity * dt

    return state
end

function run_descent_profile()
    params = VehicleParams(1500.0, 500.0, 310.0, 25000.0, 9.80665)
    rocket = RocketState(1000.0, -85.0, 2000.0) # 1km alt, -85 m/s descent
    dt = 0.2

    println("=== Julia Rocket Trajectory Solver ===")
    println("Initial: Alt = $(rocket.altitude)m, Vel = $(rocket.velocity)m/s\n")

    for step in 1:15
        # Soft touchdown guidance feedback law
        error_v = -2.0 - rocket.velocity
        thrust_cmd = rocket.mass * (params.gravity + 1.2 * error_v)
        simulate_step(rocket, thrust_cmd, dt, params)

        println("Step $(rpad(step, 2)) | Alt: $(lpad(round(rocket.altitude, digits=1), 6))m | Vel: $(lpad(round(rocket.velocity, digits=1), 5))m/s | Mass: $(round(rocket.mass, digits=1))kg")
    end
end

run_descent_profile()
