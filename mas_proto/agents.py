from mesa import Agent
import random

class RescueAgent(Agent):
    """
    Agent with stable behavioral profile:
    - attention_radius: range of perception/attention
    - monitor_interval: goal rechecking frequency
    - comm_prob: self-memory broadcast probability
    - wm_decay: working memory decay (0..1)
    """
    def __init__(self, unique_id, model, profile):
        super().__init__(unique_id, model)
        self.profile = profile
        self.alive = True
        self.step_count = 0
        # working memory: set of suspected positions (tuples)
        self.working_memory = set()

    def _neighbors_in_radius(self, radius):
        x, y = self.pos
        cells = []
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x+dx) % self.model.width, (y+dy) % self.model.height
                cells.append((nx, ny))
        return cells

    def perceive(self):
        # Percebe vítimas e pistas no raio de atenção
        for cell in self._neighbors_in_radius(self.profile["attention_radius"]):
            cell_contents = self.model.grid.get_cell_list_contents([cell])
            for obj in cell_contents:
                if isinstance(obj, Victim):
                    self.working_memory.add(cell)
                elif isinstance(obj, Hint):
                    # pistas aumentam chance de lembrar (simplesmente guardar posição)
                    self.working_memory.add(cell)

    def decay_memory(self):
        # Esquecimento simplificado: remove aleatoriamente uma fração dos itens
        if self.profile["wm_decay"] <= 0:
            return
        if len(self.working_memory) == 0:
            return
        k = max(0, int(len(self.working_memory) * self.profile["wm_decay"]))
        for _ in range(k):
            self.working_memory.pop()

    def move(self):
        # Estratégia simples: se tem algo na memória, vá até o mais próximo; senão, random walk
        target = None
        if self.working_memory:
            # alvo mais próximo (distância de Manhattan)
            x, y = self.pos
            target = min(self.working_memory, key=lambda p: abs(p[0]-x)+abs(p[1]-y))
        if target:
            self._move_towards(target)
        else:
            self._random_move()

    def _move_towards(self, target):
        x, y = self.pos
        tx, ty = target
        dx = 0 if tx == x else (1 if (tx - x) % self.model.width <= self.model.width//2 else -1)
        dy = 0 if ty == y else (1 if (ty - y) % self.model.height <= self.model.height//2 else -1)
        new_pos = ((x + dx) % self.model.width, (y + dy) % self.model.height)
        self.model.grid.move_agent(self, new_pos)

    def _random_move(self):
        x, y = self.pos
        dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        new_pos = ((x + dx) % self.model.width, (y + dy) % self.model.height)
        self.model.grid.move_agent(self, new_pos)

    def communicate(self):
        # Broadcast simples: compartilha 1 item da memória com vizinhos Moore radius=1
        if random.random() > self.profile["comm_prob"]:
            return
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        if not self.working_memory or not neighbors:
            return
        info = random.choice(list(self.working_memory))
        for n in neighbors:
            if isinstance(n, RescueAgent) and n.alive:
                n.working_memory.add(info)

    def act_on_cell(self):
        # Se chegar numa célula com vítima, “resgata”
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in list(cell_contents):
            if isinstance(obj, Victim):
                self.model.rescued += 1
                self.model.grid.remove_agent(obj)
                self.model.schedule.remove(obj)
                # remove alvo da memória (se estiver)
                if self.pos in self.working_memory:
                    self.working_memory.remove(self.pos)

    def maybe_fail(self):
        # Falhas de agente (para simular sistemas críticos): prob. pequena por passo
        if self.model.fail_prob > 0 and random.random() < self.model.fail_prob:
            self.alive = False

    def step(self):
        if not self.alive:
            return
        self.step_count += 1
        self.perceive()
        # monitoramento: a cada N passos, reforça prioridade (já embutido ao tentar mover)
        if self.step_count % self.profile["monitor_interval"] == 0:
            pass  # hook: poderíamos priorizar alvos por frequência, mas mantemos simples
        self.move()
        self.act_on_cell()
        self.communicate()
        self.decay_memory()
        self.maybe_fail()


class Victim(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Hint(Agent):
    """simple cue to enhance detection/recall; passive only."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
