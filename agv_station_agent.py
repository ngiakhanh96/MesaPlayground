from mesa import Agent
import random


class Agv_Station_Agent(Agent):
    def __init__(self, unique_id, model, coordinate):
        super().__init__(unique_id, model)
        self.coordinate = coordinate

    def step(self):
        return
