from manufacture_model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import BarChartModule
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
        portrayal["text"] = f"A: {agent.num_waiting_product_dict['A']}/{agent.num_max_waiting_products}, B: {agent.num_waiting_product_dict['B']}/{agent.num_max_waiting_products}"
        portrayal["text_color"] = "black"
    elif (isinstance(agent, Kanban_Agent)):
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = False
        portrayal["text"] = f"{agent.num_available_kanban}/{agent.max_kanban}"
        portrayal["text_color"] = "black"
    elif (isinstance(agent, Agv_Station_Agent)):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif (isinstance(agent, Agv_Agent)):
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        portrayal["text"] = str(agent.unique_id)
        portrayal["text_color"] = "black"
        if (agent.status != Status.Comeback and agent.status != Status.Loading and agent.status != Status.Free):
            portrayal["Color"] = "blue"
        elif (agent.status == Status.Loading):
            portrayal["Color"] = "orange"
        else:
            portrayal["Color"] = "yellow"
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 800, 800)
total_moving_step_graph = BarChartModule(
    [{"Label": "Total_Moving_Seconds", "Color": "Red"}],
    scope="agent",
    data_collector_name='data_collector'
)

total_working_step_graph = BarChartModule(
    [{"Label": "Total_Working_Seconds", "Color": "Red"}],
    scope="agent",
    data_collector_name='data_collector'
)

total_waiting_step_graph = BarChartModule(
    [{"Label": "Total_Waiting_Seconds", "Color": "Red"}],
    scope="agent",
    data_collector_name='data_collector'
)

# agv_0_total_waiting_step_graph = BarChartModule(
#     [{"Label": "Agv_0_Total_Waiting_Seconds", "Color": "Red"}],
#     scope="model",
#     data_collector_name='data_collector'
# )

# agv_1_total_waiting_step_graph = BarChartModule(
#     [{"Label": "Agv_1_Total_Waiting_Seconds", "Color": "Red"}],
#     scope="model",
#     data_collector_name='data_collector'
# )

number_of_agents_slider = UserSettableParameter(
    "slider",
    "Number of Agents",
    1,
    1,
    len(spot_pos_dict_conf),
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
    1,
    0,
    20,
    1
)

number_of_products_B_slider = UserSettableParameter(
    "slider",
    "Number of Product B",
    1,
    0,
    20,
    1
)

num_agv_slider = UserSettableParameter(
    "slider",
    "Number of AGV",
    2,
    1,
    2,
    1
)

num_min_kanban_to_refill_slider = UserSettableParameter(
    "choice",
    "Minimum of kanban to refill",
    value=1,
    choices=[0, 1, 2]
)

agent_movement_radius_choice = UserSettableParameter(
    'choice',
    'Agent movement radius (squares)',
    value=7,
    choices=[4, 5, 7])

num_agv_loading_step_choice = UserSettableParameter(
    'choice',
    'Loading time for agv (seconds)',
    value=1,
    choices=[1, 2, 3, 4, 5, 6, 7, 8])

server = ModularServer(
    Manufacture_Model,
    [grid, total_moving_step_graph, total_working_step_graph, total_waiting_step_graph],
    # [grid, total_moving_step_graph, total_working_step_graph, total_waiting_step_graph, agv_0_total_waiting_step_graph, agv_1_total_waiting_step_graph],
    "Manufacture Model",
    {
        "width": 10,
        "height": 10,
        "num_person_agent": number_of_agents_slider,
        "num_product_A": number_of_products_A_slider,
        "num_product_B": number_of_products_B_slider,
        "num_max_waiting_products": num_max_waiting_products_slider,
        "num_agv": num_agv_slider,
        "num_min_kanban_to_refill": num_min_kanban_to_refill_slider,
        "movement_radius": agent_movement_radius_choice,
        "num_agv_loading_step": num_agv_loading_step_choice
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
