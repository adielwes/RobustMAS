from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import RescueAgent, Victim, Hint
import random

def compute_coverage(model):
    # coverage: fraction of the grid visited by at least one agent
    return len(model.visited) / (model.width * model.height)

def compute_success(model):
    # success: rescued victims / total
    if model.total_victims == 0:
        return 1.0
    return model.rescued / model.total_victims

class RescueModel(Model):
    def __init__(self, width=20, height=20, n_agents=6, n_victims=12, n_hints=10,
                 team_profiles=None, fail_prob=0.0, max_steps=500, seed=None):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.rescued = 0
        self.total_victims = n_victims
        self.fail_prob = fail_prob
        self.max_steps = max_steps
        self.step_count = 0
        self.visited = set()

        # Profiles
        if team_profiles is None:
            raise ValueError("team_profiles precisa ser uma lista de dicts de tamanho n_agents.")
        assert len(team_profiles) == n_agents

        # Create rescue agents
        for i in range(n_agents):
            a = RescueAgent(f"A{i}", self, team_profiles[i])
            self.schedule.add(a)
            x, y = random.randrange(self.width), random.randrange(self.height)
            self.grid.place_agent(a, (x, y))

        # Create victms
        for i in range(n_victims):
            v = Victim(f"V{i}", self)
            self.schedule.add(v)
            x, y = random.randrange(self.width), random.randrange(self.height)
            self.grid.place_agent(v, (x, y))

        # Create hints
        for i in range(n_hints):
            h = Hint(f"H{i}", self)
            self.schedule.add(h)
            x, y = random.randrange(self.width), random.randrange(self.height)
            self.grid.place_agent(h, (x, y))

        self.datacollector = DataCollector(
            model_reporters={
                "coverage": compute_coverage,
                "success": compute_success,
                "rescued": lambda m: m.rescued,
                "alive_agents": lambda m: sum(1 for a in m.schedule.agents if isinstance(a, RescueAgent) and a.alive),
            }
        )

    def step(self):
        # marks cells visited by active agents
        for a in self.schedule.agents:
            if isinstance(a, RescueAgent) and a.alive and a.pos is not None:
                self.visited.add(a.pos)

        self.schedule.step()
        self.datacollector.collect(self)
        self.step_count += 1

        # termination condition: all victims rescued or max_steps
        done = (self.rescued >= self.total_victims) or (self.step_count >= self.max_steps)
        return done
