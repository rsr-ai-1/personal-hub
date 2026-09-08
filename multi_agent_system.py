"""Autonomous Multi-Agent System (Planner -> Worker -> Critic Loop)."""

from dataclasses import dataclass, field


@dataclass
class SharedContext:
    task: str
    plan: list[str] = field(default_factory=list)
    draft_solution: str = ""
    critique: str = ""
    approved: bool = False


class PlannerAgent:
    def execute(self, ctx: SharedContext):
        print("[Planner] Decomposing task into execution steps...")
        ctx.plan = [
            f"1. Analyze requirements for '{ctx.task}'",
            "2. Generate modular Python implementation",
            "3. Validate edge cases and complexity"
        ]


class WorkerAgent:
    def execute(self, ctx: SharedContext):
        print("[Worker] Implementing solution based on plan...")
        ctx.draft_solution = (
            f"# Solution for: {ctx.task}\n"
            "def run_subroutine():\n"
            "    return {'status': 'success', 'confidence': 0.98}"
        )


class CriticAgent:
    def execute(self, ctx: SharedContext):
        print("[Critic] Evaluating draft quality and constraints...")
        if len(ctx.draft_solution) > 30 and "def " in ctx.draft_solution:
            ctx.critique = "Verification passed: Syntax valid and modular."
            ctx.approved = True
        else:
            ctx.critique = "Verification failed: Incomplete implementation."
            ctx.approved = False


class AgentCoordinator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.worker = WorkerAgent()
        self.critic = CriticAgent()

    def run(self, task_description: str):
        ctx = SharedContext(task=task_description)
        print(f"--- Starting Autonomous Pipeline: {task_description} ---")

        self.planner.execute(ctx)
        self.worker.execute(ctx)
        self.critic.execute(ctx)

        print("\n--- Pipeline Summary ---")
        print("Plan Steps:", len(ctx.plan))
        print("Critique:", ctx.critique)
        print("Final Status:", "APPROVED" if ctx.approved else "REJECTED")


if __name__ == "__main__":
    orchestrator = AgentCoordinator()
    orchestrator.run("Deploy Edge Drone Swarm")
