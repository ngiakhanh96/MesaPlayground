from mesa import Agent
import random
from utilities import *


class Person_Agent(Agent):
    def __init__(self, unique_id, model, each_step_duration):
        super().__init__(unique_id, model)
        self.current_doing_duration = None
        self.each_step_duration = each_step_duration
        self.dest_pos = self.pos

    def step(self):
        if (self.is_manufacturing() == True):
            return
        if (self.model.check_if_running() == False):
            return

        self.dest_pos = self.pos
        if (self.find_backward() == False):
            self.find_forward()

    def is_moving(self):
        current_pos = tuple(self.pos)
        if (self.dest_pos == None or (current_pos[0] == self.dest_pos[0] and current_pos[1] == self.dest_pos[1])):
            return False
        return True

    def is_manufacturing(self):
        if (self.current_doing_duration is None):
            if (self.is_moving() == False and self.check_if_anything_new_to_do() == True):
                self.current_doing_duration = 0
                return True
            return False

        if (self.current_doing_duration >= self.each_step_duration):
            self.update_product_agent_waiting_products()
            if (self.check_if_anything_new_to_do() == True):
                self.current_doing_duration = 0
                return True
            self.current_doing_duration = None
            return False
        else:
            self.current_doing_duration += 1
            return True

    def update_product_agent_waiting_products(self):
        product_pos = convert_spot_pos_to_product_pos(self.pos)
        if (product_pos is not None):
            product_agent = self.model.grid.get_cell_list_contents(
                [product_pos])[0]

            product_agent.num_waiting_products -= 1
            next_product_pos = convert_spot_pos_to_next_product_pos(self.pos)
            if (next_product_pos is not None):
                next_product_agent = self.model.grid.get_cell_list_contents(
                    [next_product_pos])[0]
                next_product_agent.num_waiting_products += 1

            # last_position
            else:
                self.model.update_num_finished_product()

        # first position
        else:
            next_product_pos = convert_spot_pos_to_next_product_pos(self.pos)
            next_product_agent = self.model.grid.get_cell_list_contents(
                [next_product_pos])[0]
            next_product_agent.num_waiting_products += 1

    def check_if_anything_new_to_do(self):
        product_pos = convert_spot_pos_to_product_pos(self.pos)
        if (product_pos is not None):
            is_there_any_product = self.check_if_any_waiting_product(
                product_pos)
            is_next_waiting_products_max = self.check_if_next_waiting_products_max(
                self.pos)
            return is_there_any_product == True and is_next_waiting_products_max == False

        # first position
        else:
            return False

    def calculate_next_pos(self, destination, startDoing=True):
        if (self.pos is None):
            return None
        currentX, currentY = tuple(self.pos)
        destX, destY = destination

        nextPosition = (currentX, currentY)

        if (currentX < destX):
            nextPosition = (currentX+1, currentY)
        elif (currentX > destX):
            nextPosition = (currentX-1, currentY)
        else:
            if (currentY < destY):
                nextPosition = (currentX, currentY+1)
            elif (currentY > destY):
                nextPosition = (currentX, currentY-1)

        if (nextPosition[0] == destX and nextPosition[1] == destY and startDoing == True):
            self.current_doing_duration = 0

        self.dest_pos = destination
        return nextPosition

    def find_backward(self):
        # pass
        isSucceeded = False
        for i in reversed(range(6)):
            spot_pos = get_spot_pos_from_dict(str(i))
            is_there_any_person_agent = self.check_if_any_person_agent_except_me(
                spot_pos)

            product_pos = convert_spot_pos_to_product_pos(spot_pos)
            if (product_pos is not None):
                is_there_any_product = self.check_if_any_waiting_product(
                    product_pos)
                is_next_waiting_products_max = self.check_if_next_waiting_products_max(
                    spot_pos)
                if (is_there_any_person_agent == False and is_there_any_product == True and is_next_waiting_products_max == False):
                    next_pos = self.calculate_next_pos(spot_pos)
                    self.model.grid.move_agent(self, next_pos)
                    isSucceeded = True
                    return isSucceeded

            # first position
            else:
                is_next_waiting_products_max = self.check_if_next_waiting_products_max(
                    spot_pos)
                if (is_there_any_person_agent == False and is_next_waiting_products_max == False):
                    next_pos = self.calculate_next_pos(spot_pos)
                    self.model.grid.move_agent(self, next_pos)
                    isSucceeded = True
                    return isSucceeded
        return isSucceeded

    def check_if_any_waiting_product(self, product_pos):
        product_agent = self.model.grid.get_cell_list_contents(
            [product_pos])[0]

        return product_agent.num_waiting_products > 0

    def check_if_next_waiting_products_max(self, spot_pos):
        is_max_waiting_products_next_product_pos = False
        next_product_pos = convert_spot_pos_to_next_product_pos(spot_pos)
        if (next_product_pos is not None):
            next_product_agent = self.model.grid.get_cell_list_contents(
                [next_product_pos])[0]
            is_max_waiting_products_next_product_pos = next_product_agent.num_waiting_products >= next_product_agent.num_max_waiting_products
        return is_max_waiting_products_next_product_pos

    def check_if_any_person_agent_except_me(self, spot_pos):
        cellmates = self.model.grid.get_cell_list_contents([spot_pos])
        return len(
            list(filter(lambda x: x.unique_id != self.unique_id, cellmates))) > 1

    def find_forward(self):
        last_available_person_agent = False
        for i in range(6):
            spot_pos = get_spot_pos_from_dict(str(i))
            is_there_any_person_agent = self.check_if_any_person_agent_except_me(
                spot_pos)

            if (is_there_any_person_agent == True):
                last_available_person_agent = is_there_any_person_agent
            elif (last_available_person_agent == True):
                next_pos = self.calculate_next_pos(spot_pos, False)
                self.model.grid.move_agent(self, next_pos)
                return
