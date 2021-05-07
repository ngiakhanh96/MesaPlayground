from mesa import Agent
import random


class Product_Agent(Agent):
    def __init__(
            self,
            unique_id,
            model,
            num_waiting_product_A,
            num_waiting_product_B,
            num_max_waiting_products,
            coordinate):
        super().__init__(unique_id, model)
        self.num_waiting_product_dict = {
            "A": num_waiting_product_A,
            "B": num_waiting_product_B
        }
        self.num_max_waiting_products = num_max_waiting_products
        self.coordinate = coordinate

    def update_waiting_product(self, product_name, is_up):
        if (is_up):
            self.num_waiting_product_dict[product_name] += 1
        else:
            self.num_waiting_product_dict[product_name] -= 1

    def check_if_waiting_product_max(self, product_name):
        return self.num_waiting_product_dict[product_name] >= self.num_max_waiting_products

    def check_if_any_waiting_product(self, product_name):
        return self.num_waiting_product_dict[product_name] > 0

    def step(self):
        return
