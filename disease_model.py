from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from person_agent import *
from spot_agent import *
from product_agent import *
from utilities import *
import random

"""A model of disease spread."""


class Disease_Model(Model):

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
        self.num_product_A = num_product_A
        self.each_step_duration_A = each_step_duration_A
        self.num_product_B = num_product_B
        self.each_step_duration_B = each_step_duration_B
        self.num_max_waiting_products = num_max_waiting_products
        self.num_finished_product = 0
        self.total_product = self.num_product_A + self.num_product_B
        self.grid = MultiGrid(width, height, False)

        self.schedule = RandomActivation(self)

        self.current_unprocessed_product_step_arr = []
        for i in range(num_product_A):
            self.current_unprocessed_product_step_arr.append(self.each_step_duration_A)
        for i in range(num_product_B):
            self.current_unprocessed_product_step_arr.append(self.each_step_duration_B)
        random.shuffle(self.current_unprocessed_product_step_arr)

        default_coordinates = [(3, 1), (3, 3), (3, 5), (6, 1), (6, 3), (6, 5)]
        for i in range(6):
            new_agent = Spot_Agent(
                i,
                self,
                default_coordinates[i])
            self.grid.place_agent(new_agent, new_agent.coordinate)

            product_agent = Product_Agent(
                i,
                self,
                0,
                self.num_max_waiting_products,
                convert_spot_pos_to_product_pos(default_coordinates[i]))
            if (product_agent.coordinate is not None):
                self.grid.place_agent(product_agent, product_agent.coordinate)

        random_coordinates = random.sample(default_coordinates, self.num_person_agent)
        for i in range(self.num_person_agent):
            new_agent = Person_Agent(
                "A"+str(i),
                self,
                self.current_unprocessed_product_step_arr[0])
            self.grid.place_agent(new_agent, random_coordinates[i])
            self.schedule.add(new_agent)

        # self.dataCollector = DataCollector(
        #     model_reporters={"Total_Infected": calculate_number_of_infected,
        #                      "Total_Immunized": calculate_number_of_immunized},
        #     agent_reporters={}
        # )

    def get_current_processing_product_step(self):
        if (len(self.current_unprocessed_product_step_arr) > 0):
            return self.current_unprocessed_product_step_arr[0]
        return None

    def update_num_finished_product(self):
        self.num_finished_product += 1
        self.current_unprocessed_product_step_arr.pop(0)
        if (self.check_if_running() == False):
            self.running = False

    def check_if_running(self):
        return self.num_finished_product < self.total_product

    def step(self):
        self.schedule.step()
        # self.dataCollector.collect(self)


def calculate_number_of_infected(model):
    number_of_infected = 0
    for agent in model.schedule.agents:
        if agent.infected == True:
            number_of_infected += 1
    return number_of_infected


def calculate_number_of_immunized(model):
    number_of_immunized = 0
    for agent in model.schedule.agents:
        if agent.immunized == True:
            number_of_immunized += 1
    return number_of_immunized
