from disease_model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.batchrunner import BatchRunner
from numpy import arange
import matplotlib.pyplot as plt


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.7}

    if agent.infected == False:
        if agent.immunized == False:
            portrayal["Color"] = "yellow"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.5
        else:
            portrayal["Color"] = "green"
            portrayal["Layer"] = 2
            portrayal["r"] = 0.2
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
total_infected_graph = ChartModule(
    [{"Label": "Total_Infected", "Color": "Red"},
     {"Label": "Total_Immunized", "Color": "Green"}],
    data_collector_name='dataCollector'
)
number_of_agents_slider = UserSettableParameter(
    "slider",
    "Number of Agents",
    20,
    2,
    100,
    1
)

initial_infection_slider = UserSettableParameter(
    "slider",
    "Prop of Initial Infection",
    0.4,
    0.01,
    1,
    0.01
)

transmissibility_slider = UserSettableParameter(
    "slider",
    "Prop of Transmissibility",
    0.3,
    0.01,
    1,
    0.01
)

level_of_movement_slider = UserSettableParameter(
    "slider",
    "Prop of Movement",
    0.5,
    0.01,
    1,
    0.01
)

mean_length_of_disease_slider = UserSettableParameter(
    "slider",
    "Mean Length of Disease (Days)",
    14,
    1,
    100,
    1
)

immunization_prob_slider = UserSettableParameter(
    "slider",
    "Immunization Probability",
    0.5,
    0.01,
    1,
    0.01
)

mean_length_of_immunization_slider = UserSettableParameter(
    "slider",
    "Mean Length of Immunization (Days)",
    20,
    1,
    100,
    1
)

server = ModularServer(
    Disease_Model,
    [grid, total_infected_graph],
    "Disease Spread Model",
    {
        "N": number_of_agents_slider,
        "width": 10,
        "height": 10,
        "initial_infection": initial_infection_slider,
        "transmissibility": transmissibility_slider,
        "level_of_movement": level_of_movement_slider,
        "mean_length_of_disease": mean_length_of_disease_slider,
        "immunization_prob": immunization_prob_slider,
        "mean_length_of_immunization": mean_length_of_immunization_slider
    }
)

server.port = 8521
server.launch()

# fixed_params = {
#     "width": 10,
#     "height": 10,
#     "initial_infection": 0.8,
#     "transmissibility": 0.5,
#     "mean_length_of_disease": 10,
#     "mean_length_of_immunization": 20,
#     "immunization_prob": 0.05}

# variable_params = {
#     "N": range(2, 10, 1),
#     "level_of_movement": arange(0.0, 1.0, 0.1)
# }

# num_iterations = 5
# num_steps = 365

# batch_run = BatchRunner(
#     Disease_Model,
#     fixed_parameters=fixed_params,
#     variable_parameters=variable_params,
#     iterations=num_iterations,
#     max_steps=num_steps,
#     model_reporters={"Total_Infected": calculate_number_of_infected,
#                      "Total_Immunized": calculate_number_of_immunized})

# batch_run.run_all()

# run_data = batch_run.get_model_vars_dataframe()
# plt.scatter(run_data.level_of_movement, run_data.Total_Infected)
