from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from person_agent import *
from spot_agent import *
from product_agent import *
from utilities import *
import random

"""A model of manufacture."""


class Manufacture_Model(Model):

    def __init__(
            self,
            width,
            height,
            num_person_agent,
            num_product_A,
            each_step_duration_A,
            num_product_B,
            each_step_duration_B,
            num_max_waiting_products):
        super().__init__()
        self.num_person_agent = num_person_agent
        # self.total_product = num_product_A + num_product_B
        self.product_dict = {
            "A": {
                "each_step_duration": each_step_duration_A,
                "num_product": num_product_A
            },
            "B": {
                "each_step_duration": each_step_duration_B,
                "num_product": num_product_B
            }
        }

        self.num_max_waiting_products = num_max_waiting_products

        self.grid = MultiGrid(width, height, False)

        self.schedule = SimultaneousActivation(self)

        self.current_unprocessed_product_arr = []
        for i in range(self.product_dict["A"]["num_product"]):
            self.current_unprocessed_product_arr.append("A")
        for i in range(self.product_dict["B"]["num_product"]):
            self.current_unprocessed_product_arr.append("B")
        random.shuffle(self.current_unprocessed_product_arr)

        for i in range(6):
            spot_pos = get_spot_pos_from_dict(str(i))
            new_agent = Spot_Agent(
                i,
                self,
                spot_pos)
            self.grid.place_agent(new_agent, new_agent.coordinate)

            product_agent = Product_Agent(
                i,
                self,
                0,
                0,
                self.num_max_waiting_products,
                convert_spot_pos_to_product_pos(spot_pos))
            if (product_agent.coordinate is not None):
                self.grid.place_agent(product_agent, product_agent.coordinate)

        default_coordinates = get_spot_pos_list()
        random_coordinates = random.sample(
            default_coordinates, self.num_person_agent)
        for i in range(self.num_person_agent):
            new_agent = Person_Agent(
                "A"+str(i),
                self,
                self.get_current_processing_product(),
                self.get_current_processing_product_step())
            self.grid.place_agent(new_agent, random_coordinates[i])
            self.schedule.add(new_agent)

        self.data_collector = DataCollector(
            model_reporters={},
            agent_reporters={"Total_Working_Step": lambda agent: agent.working_step_count,
                             "Total_Moving_Step": lambda agent: agent.moving_step_count}
        )
        self.data_collector.collect(self)

    def get_current_processing_product(self):
        if (self.check_if_running() == True):
            return self.current_unprocessed_product_arr[0]
        return None

    def get_current_processing_product_step(self):
        current_processing_product_step = self.get_current_processing_product()
        if (current_processing_product_step is None):
            return None
        return self.product_dict[current_processing_product_step]["each_step_duration"]

    def update_num_finished_product(self):
        self.current_unprocessed_product_arr.pop(0)
        if (self.check_if_running() == False):
            self.running = False

    def check_if_running(self):
        return len(self.current_unprocessed_product_arr) > 0

    def step(self):
        self.schedule.step()
        self.data_collector.collect(self)
