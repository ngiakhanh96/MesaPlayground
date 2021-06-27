from mesa import Agent


class Spot_Agent(Agent):
    def __init__(
        self, 
        unique_id,
        name,
        model, 
        coordinate,
        product_A_processing_duration,
        product_B_processing_duration):
        super().__init__(unique_id, model)
        self.name = name
        self.coordinate = coordinate
        self.product_processing_duration_dict = {
            "A": product_A_processing_duration,
            "B": product_B_processing_duration
        }

    def step(self):
        return
