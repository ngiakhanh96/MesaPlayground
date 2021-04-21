from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import random


class Person_Agent(Agent):
    def __init__(self, unique_id, model, initial_infection, transmissibility,
                 level_of_movement, mean_length_of_disease, immunization_prob, mean_length_of_immunization):
        super().__init__(unique_id, model)
        self.transmissibility = transmissibility
        self.level_of_movement = level_of_movement
        self.initial_infection = initial_infection
        self.mean_length_of_disease = mean_length_of_disease
        self.infected = False
        self.immunization_prob = immunization_prob
        self.mean_length_of_immunization = mean_length_of_immunization
        self.immunized = False
        self.infect(self, self.initial_infection)

    def move(self):
        if random.uniform(0, 1) < self.level_of_movement:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False)
            new_position = random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

    def infect(self, inhabitant, infectionProbability):
        if random.uniform(0, 1) < infectionProbability:
            inhabitant.infected = True
            inhabitant.disease_duration = int(round(random.expovariate
                                                    (1.0 / inhabitant.mean_length_of_disease), 0))

    def try_to_infect(self):
        if self.infected == True:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            if len(cellmates) > 1:
                for inhabitant in cellmates:
                    if inhabitant.infected == False and inhabitant.immunized == False:
                        self.infect(inhabitant, self.transmissibility)

    def recover(self):
        if self.infected == True:
            self.disease_duration -= 1
            if self.disease_duration <= 0:
                self.infected = False

    def beImmunized(self):
        if self.immunized == True:
            self.immunization_duration -= 1
            if self.immunization_duration <= 0:
                self.immunized = False
            return
        if self.infected == False and self.immunized == False:
            if random.uniform(0, 1) < self.immunization_prob:
                self.immunized = True
                self.immunization_duration = int(round(random.expovariate
                                                       (1.0 / self.mean_length_of_immunization), 0))

    def step(self):
        self.beImmunized()
        self.move()
        self.try_to_infect()
        self.recover()


"""A model of disease spread."""


class Disease_Model(Model):
    def __init__(self, N, width, height, initial_infection, transmissibility,
                 level_of_movement, mean_length_of_disease, immunization_prob, mean_length_of_immunization):
        super().__init__()
        self.num_agents = N

        self.grid = MultiGrid(width, height, True)

        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            new_agent = Person_Agent(
                i,
                self,
                initial_infection,
                transmissibility,
                level_of_movement,
                mean_length_of_disease,
                immunization_prob,
                mean_length_of_immunization
            )
            self.schedule.add(new_agent)

            try:
                start_cell = self.grid.find_empty()
                self.grid.place_agent(new_agent, start_cell)
            except:
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)
                self.grid.place_agent(new_agent, (x, y))

        self.dataCollector = DataCollector(
            model_reporters={"Total_Infected": calculate_number_of_infected,
                             "Total_Immunized": calculate_number_of_immunized},
            agent_reporters={}
        )

    def step(self):
        self.schedule.step()
        self.dataCollector.collect(self)


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
