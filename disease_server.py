from disease_model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.batchrunner import BatchRunner
from numpy import arange
import matplotlib.pyplot as plt


def agent_portrayal(agent):
    portrayal = {"Filled": "true", "Layer": 0}
    if (isinstance(agent, Spot_Agent)):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.8
    elif (isinstance(agent, Person_Agent)):
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        portrayal["text"] = str(agent.unique_id)
        portrayal["text_color"] = "black"
    elif (isinstance(agent, Product_Agent)):
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = False
        portrayal["text"] = str(agent.num_waiting_products) + '/' + str(agent.num_max_waiting_products)
        portrayal["text_color"] = "black"
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
# total_infected_graph = ChartModule(
#     [{"Label": "Total_Infected", "Color": "Red"},
#      {"Label": "Total_Immunized", "Color": "Green"}],
#     data_collector_name='dataCollector'
# )
number_of_agents_slider = UserSettableParameter(
    "slider",
    "Number of Agents",
    3,
    1,
    6,
    1
)

num_max_waiting_products_slider = UserSettableParameter(
    "slider",
    "Max number of waiting products on station",
    2,
    1,
    5,
    1
)

number_of_products_A_slider = UserSettableParameter(
    "slider",
    "Number of Product A",
    3,
    0,
    20,
    1
)

num_step_to_finish_product_A_slider = UserSettableParameter(
    "slider",
    "Number of step to finish product A",
    2,
    1,
    5,
    1
)

number_of_products_B_slider = UserSettableParameter(
    "slider",
    "Number of Product B",
    3,
    0,
    20,
    1
)

num_step_to_finish_product_B_slider = UserSettableParameter(
    "slider",
    "Number of step to finish product B",
    2,
    1,
    5,
    1
)

server = ModularServer(
    Disease_Model,
    # [grid, total_infected_graph],
    [grid],
    "Disease Spread Model",
    {
        "width": 10,
        "height": 10,
        "num_person_agent": number_of_agents_slider,
        "num_product_A": number_of_products_A_slider,
        "each_step_duration_A": num_step_to_finish_product_A_slider,
        "num_product_B": number_of_products_B_slider,
        "each_step_duration_B": num_step_to_finish_product_B_slider,
        "num_max_waiting_products": num_max_waiting_products_slider
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
