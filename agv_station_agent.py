from mesa import Agent
import random


class Agv_Station_Agent(Agent):
    def __init__(self, unique_id, name, model, coordinate):
        super().__init__(unique_id, model)
        self.name = name
        self.coordinate = coordinate

    def step(self):
        return
