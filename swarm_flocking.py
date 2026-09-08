"""Decentralized 2D Swarm Flocking Simulation (Reynolds Boids)."""

import math
import random
from dataclasses import dataclass


@dataclass
class DroneBoid:
    id: int
    x: float
    y: float
    vx: float
    vy: float


class SwarmSimulator:
    def __init__(self, num_drones: int = 10, visual_range: float = 5.0, min_distance: float = 1.5):
        self.visual_range = visual_range
        self.min_distance = min_distance
        self.drones = [
            DroneBoid(
                id=i,
                x=random.uniform(5.0, 15.0),
                y=random.uniform(5.0, 15.0),
                vx=random.uniform(-0.5, 0.5),
                vy=random.uniform(-0.5, 0.5)
            )
            for i in range(num_drones)
        ]

    def _distance(self, b1: DroneBoid, b2: DroneBoid) -> float:
        return math.hypot(b1.x - b2.x, b1.y - b2.y)

    def update(self, dt: float = 0.5):
        for boid in self.drones:
            sep_x, sep_y = 0.0, 0.0
            align_vx, align_vy = 0.0, 0.0
            center_x, center_y = 0.0, 0.0
            neighbors = 0

            for other in self.drones:
                if boid.id == other.id:
                    continue
                dist = self._distance(boid, other)

                # Rule 1: Separation
                if dist < self.min_distance and dist > 0:
                    sep_x += (boid.x - other.x) / dist
                    sep_y += (boid.y - other.y) / dist

                # Rules 2 & 3: Alignment & Cohesion
                if dist < self.visual_range:
                    align_vx += other.vx
                    align_vy += other.vy
                    center_x += other.x
                    center_y += other.y
                    neighbors += 1

            if neighbors > 0:
                align_vx /= neighbors
                align_vy /= neighbors
                center_x /= neighbors
                center_y /= neighbors

                boid.vx += (align_vx - boid.vx) * 0.1 + (center_x - boid.x) * 0.02
                boid.vy += (align_vy - boid.vy) * 0.1 + (center_y - boid.y) * 0.02

            boid.vx += sep_x * 0.2
            boid.vy += sep_y * 0.2

            # Velocity clamping
            speed = math.hypot(boid.vx, boid.vy)
            max_speed = 1.5
            if speed > max_speed:
                boid.vx = (boid.vx / speed) * max_speed
                boid.vy = (boid.vy / speed) * max_speed

            boid.x += boid.vx * dt
            boid.y += boid.vy * dt

    def render_grid(self, width: int = 30, height: int = 15):
        grid = [["." for _ in range(width)] for _ in range(height)]
        for d in self.drones:
            gx = int(d.x) % width
            gy = int(d.y) % height
            grid[gy][gx] = "▲"

        print("\n" + "=" * width)
        for row in grid:
            print("".join(row))
        print("=" * width)


if __name__ == "__main__":
    swarm = SwarmSimulator(num_drones=8)
    print("Initial Swarm Distribution:")
    swarm.render_grid()

    for step in range(3):
        swarm.update(dt=0.5)
        print(f"Swarm Step {step + 1}:")
        swarm.render_grid()
