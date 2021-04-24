from mesa import Agent
import random


class Product_Agent(Agent):
    def __init__(self, unique_id, model, num_waiting_products, coordinate):
        super().__init__(unique_id, model)
        self.num_max_waiting_products = 2
        self.num_waiting_products = num_waiting_products
        self.coordinate = coordinate

    def step(self):
        return
