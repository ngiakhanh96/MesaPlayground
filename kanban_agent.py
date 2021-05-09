from mesa import Agent
import random


class Kanban_Agent(Agent):
    def __init__(self, unique_id, model, coordinate, num_available_kanban, max_kanban):
        super().__init__(unique_id, model)
        self.coordinate = coordinate
        self.num_available_kanban = num_available_kanban
        self.max_kanban = max_kanban

    def step(self):
        return

    def consume_kanban(self):
        self.num_available_kanban -= 1

    def refill_kanban(self):
        self.num_available_kanban += 1

    def is_any_available_kanban(self):
        return self.num_available_kanban > 0
