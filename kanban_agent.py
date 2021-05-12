from mesa import Agent
import random


class Kanban_Agent(Agent):
    def __init__(self, unique_id, model, coordinate, num_available_kanban, max_kanban):
        super().__init__(unique_id, model)
        self.coordinate = coordinate
        self.num_available_kanban = num_available_kanban
        self.max_kanban = max_kanban
        self.is_update_consume = False
        self.is_update_refill = False

    def advance(self):
        if (self.is_update_consume == True):
            self.num_available_kanban -= 1
            self.is_update_consume = False
        if (self.is_update_refill == True):
            self.num_available_kanban += 1
            self.is_update_refill = False

    def step(self):
        return

    def consume(self):
        self.is_update_consume = True

    def refill(self):
        self.is_update_refill = True

    def is_any_available_kanban(self):
        return self.num_available_kanban > 0
