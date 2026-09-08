"""2-Link Planar Robotic Arm Kinematics (Forward & Inverse)."""

import math


class PlanarRobotArm:
    def __init__(self, l1: float = 2.0, l2: float = 1.5):
        self.l1 = l1  # Length of link 1
        self.l2 = l2  # Length of link 2

    def forward_kinematics(self, theta1_deg: float, theta2_deg: float) -> tuple[float, float]:
        """Calculates end-effector (x, y) coordinates from joint angles."""
        t1 = math.radians(theta1_deg)
        t2 = math.radians(theta2_deg)

        x = self.l1 * math.cos(t1) + self.l2 * math.cos(t1 + t2)
        y = self.l1 * math.sin(t1) + self.l2 * math.sin(t1 + t2)
        return round(x, 3), round(y, 3)

    def inverse_kinematics(self, target_x: float, target_y: float) -> tuple[float, float] | None:
        """Calculates joint angles (theta1, theta2) in degrees to reach a target point."""
        r = math.hypot(target_x, target_y)
        max_reach = self.l1 + self.l2

        if r > max_reach:
            print(f"Target ({target_x}, {target_y}) is out of reach (max reach: {max_reach}).")
            return None

        # Law of Cosines for elbow angle theta2
        cos_t2 = (target_x**2 + target_y**2 - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)
        cos_t2 = max(-1.0, min(1.0, cos_t2))  # Numerical clamping
        t2 = math.acos(cos_t2)

        # Shoulder angle theta1
        k1 = self.l1 + self.l2 * math.cos(t2)
        k2 = self.l2 * math.sin(t2)
        t1 = math.atan2(target_y, target_x) - math.atan2(k2, k1)

        return round(math.degrees(t1), 2), round(math.degrees(t2), 2)


if __name__ == "__main__":
    arm = PlanarRobotArm(l1=2.0, l2=1.5)

    print("--- Forward Kinematics ---")
    angles = (30.0, 45.0)
    pos = arm.forward_kinematics(*angles)
    print(f"Joint Angles: {angles} deg -> End-Effector Position: {pos}")

    print("\n--- Inverse Kinematics ---")
    target = pos
    solved_angles = arm.inverse_kinematics(target[0], target[1])
    print(f"Target Position: {target} -> Calculated Angles: {solved_angles} deg")
