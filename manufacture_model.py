from mesa import Agent, Model
from mesa.time import SimultaneousActivation, RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from person_agent import *
from spot_agent import *
from product_agent import *
from kanban_agent import *
from agv_station_agent import *
from agv_agent import *
from utilities import *
import random
from random import randint

"""A model of manufacture."""


class Manufacture_Model(Model):

    def __init__(
            self,
            width,
            height,
            num_person_agent,
            num_product_A,
            num_product_B,
            num_max_waiting_products,
            num_agv,
            num_min_kanban_to_refill,
            movement_radius,
            num_max_kanban,
            num_agv_loading_step):
        super().__init__()

        # setup Grid and Schedule
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)

        # setup product_dict
        self.num_product_dict = {
            "A": num_product_A,
            "B": num_product_B
        }

        # setup product array
        self.current_unprocessed_product_arr = []
        for i in range(self.num_product_dict["A"]):
            self.current_unprocessed_product_arr.append("A")
        for i in range(self.num_product_dict["B"]):
            self.current_unprocessed_product_arr.append("B")
        random.shuffle(self.current_unprocessed_product_arr)

        # setup Spot_Agent, Product_Agent, Kanban_Agent
        self.num_max_waiting_products = num_max_waiting_products
        self.num_max_kanban = num_max_kanban
        self.kanban_agent_dict = {}
        for key,spot_pos in spot_pos_dict_conf.items():
            spot_agent = Spot_Agent(
                "S"+key,
                key,
                self,
                spot_pos,
                product_processing_duration_dict_conf[key]["A"],
                product_processing_duration_dict_conf[key]["B"])
            self.grid.place_agent(spot_agent, spot_agent.coordinate)

            product_agent = Product_Agent(
                "P"+key,
                key,
                self,
                0,
                0,
                self.num_max_waiting_products,
                convert_spot_pos_to_product_pos(spot_pos))
            if (product_agent.coordinate is not None):
                self.grid.place_agent(product_agent, product_agent.coordinate)

            kanban_pos = get_kanban_pos_from_dict(key)
            kanban_agent = Kanban_Agent(
                "K"+key,
                key,
                self,
                kanban_pos,
                randint(0, self.num_max_kanban),
                self.num_max_kanban
            )
            self.grid.place_agent(kanban_agent, kanban_agent.coordinate)
            self.kanban_agent_dict[key] = kanban_agent

        # setup Person_Agent
        self.num_person_agent = num_person_agent
        default_coordinates = get_spot_pos_list
        random_coordinates = random.sample(
            default_coordinates, self.num_person_agent)
        for i in range(self.num_person_agent):
            person_agent = Person_Agent(
                "A"+str(i),
                i,
                self,
                movement_radius)
            self.grid.place_agent(person_agent, random_coordinates[i])
            self.schedule.add(person_agent)

        # setup Agv_Station_Agent, Agv_Agent
        self.num_agv = num_agv
        self.num_min_kanban_to_refill = num_min_kanban_to_refill
        self.agv_agent_dict = {}
        for i in range(2):
            agv_station_pos = get_agv_station_pos_from_dict(str(i))
            agv_station_agent = Agv_Station_Agent(
                "AgvS"+str(i),
                i,
                self,
                agv_station_pos
            )
            self.grid.place_agent(agv_station_agent, agv_station_agent.coordinate)

            agv_agent = Agv_Agent(
                "Agv"+str(i),
                i,
                self,
                agv_station_pos,
                num_agv_loading_step,
                Agv_Type.Left if i == 0 else Agv_Type.Right
            )
            self.grid.place_agent(agv_agent, agv_agent.home_coordinate)
            self.agv_agent_dict[agv_agent.type.name] = agv_agent

        # setup DataCollector
        self.data_collector = DataCollector(
            model_reporters={},
            agent_reporters={"Total_Working_Seconds": lambda agent: agent.total_working_step_count,
                             "Total_Moving_Seconds": lambda agent: agent.total_moving_step_count,
                             "Total_Waiting_Seconds": lambda agent: agent.total_waiting_step_count}
        )
        self.data_collector.collect(self)

    def get_current_processing_product(self):
        if (self.check_if_running() == True):
            return self.current_unprocessed_product_arr[0]
        return None

    def update_num_finished_product(self):
        self.current_unprocessed_product_arr.pop(0)
        if (self.check_if_running() == False):
            self.running = False

    def check_if_running(self):
        return len(self.current_unprocessed_product_arr) > 0

    def step(self):
        self.schedule.step()
        self.orchestrate_agv()
        self.update_kanban()
        self.data_collector.collect(self)

    def update_kanban(self):
        for kanban_agent in self.kanban_agent_dict.values():
            kanban_agent.advance()

    def step_agvs(self):
        for agv_agent in self.agv_agent_dict.values():
            self.step_agv(agv_agent)

    def step_agv(self, agv_agent):
        is_working_agv = True
        if (agv_agent.fulfill_duty() == False):
            kanban_pos_key_list = list(agv_agent.kanban_pos_dict.keys())

            need_to_refill_kanban_key_list = [
                kanban_pos_key for kanban_pos_key in kanban_pos_key_list 
                if self.kanban_agent_dict[kanban_pos_key].num_available_kanban <= self.num_min_kanban_to_refill]
             
            need_to_refill_kanban_key_list.sort(key=lambda kanban_key: self.kanban_agent_dict[
                kanban_key].num_available_kanban)
            if (len(need_to_refill_kanban_key_list) > 0):
                chosen_kanban_key = need_to_refill_kanban_key_list[0]
                chosen_kanban_pos = self.kanban_agent_dict[chosen_kanban_key].coordinate
                agv_agent.refill_kanban(chosen_kanban_pos)
            else:
                is_working_agv = False
        return is_working_agv

    def advance_agvs(self):
        for agv_agent in self.agv_agent_dict.values():
            agv_agent.advance()

    def orchestrate_agv(self):
        if (self.num_agv > 1):
            self.step_agvs()

        else:
            agv_agent_list = list(self.agv_agent_dict.values())
            if (agv_agent_list[0].fulfill_duty() == False and agv_agent_list[1].fulfill_duty() == False):
                agv_agent_dict_keys = list(self.agv_agent_dict.keys())
                random.shuffle(agv_agent_dict_keys)
                for key in agv_agent_dict_keys:
                    if (self.step_agv(self.agv_agent_dict[key]) == True):
                        break

        self.advance_agvs()
