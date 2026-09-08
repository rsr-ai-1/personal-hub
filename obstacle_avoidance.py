"""2D Vector Obstacle Avoidance for Autonomous Drones."""

import math
from dataclasses import dataclass


@dataclass
class Obstacle:
    x: float
    y: float
    radius: float = 1.0


class AvoidancePlanner:
    def __init__(self, safety_margin: float = 2.5):
        self.safety_margin = safety_margin

    def get_steer_vector(self, drone_pos: tuple[float, float], goal: tuple[float, float], obstacles: list[Obstacle]) -> tuple[float, float]:
        """Calculates a resultant velocity vector toward the goal while avoiding obstacles."""
        dx = goal[0] - drone_pos[0]
        dy = goal[1] - drone_pos[1]
        dist_to_goal = math.hypot(dx, dy)

        # Base attractive vector to goal
        steer_x = dx / dist_to_goal if dist_to_goal > 0 else 0.0
        steer_y = dy / dist_to_goal if dist_to_goal > 0 else 0.0

        # Repulsive force from obstacles
        for obs in obstacles:
            ox = drone_pos[0] - obs.x
            oy = drone_pos[1] - obs.y
            dist = math.hypot(ox, oy)

            if dist < (obs.radius + self.safety_margin) and dist > 0:
                repulsion = (self.safety_margin + obs.radius - dist) / dist
                steer_x += (ox / dist) * repulsion * 2.0
                steer_y += (oy / dist) * repulsion * 2.0

        return round(steer_x, 3), round(steer_y, 3)


if __name__ == "__main__":
    planner = AvoidancePlanner()
    obstacles = [Obstacle(x=2.0, y=2.0, radius=0.8)]
    pos = (1.0, 1.0)
    target = (5.0, 5.0)

    steer = planner.get_steer_vector(pos, target, obstacles)
    print(f"Current Position: {pos}")
    print(f"Goal: {target}")
    print(f"Recommended Steering Vector: {steer}")
