from disease_model import Disease_Model
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if agent.infected == False:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
total_infected_graph = ChartModule(
    [{"Label": "Total_Infected", "Color": "Red"}],
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
        "mean_length_of_disease": mean_length_of_disease_slider
    }
)

server.port = 8521
server.launch()
