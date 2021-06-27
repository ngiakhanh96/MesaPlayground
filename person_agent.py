from mesa import Agent
from utilities import *


class Person_Agent(Agent):
    def __init__(self, unique_id, name, model, movement_radius):
        super().__init__(unique_id, model)
        self.name = name
        self.movement_radius = movement_radius
        self.current_product = None
        self.current_product_processing_duration = None
        self.current_doing_duration = None
        self.old_pos = self.pos
        self.is_update_product_agent_waiting_products = False
        self.current_spot_id = None
        self.try_to_continue_if_available = True
        self.setup_data_collector()

    def setup_data_collector(self):
        self.total_moving_step_count = 0
        self.total_working_step_count = 0
        self.total_waiting_step_count = 0

        self.working_step_count_dict = {}
        self.waiting_step_count_dict = {}
        for spot_id in spot_pos_dict_conf.keys():
            self.working_step_count_dict[spot_id] = 0
            self.waiting_step_count_dict[spot_id] = 0

    def advance(self):
        if (self.is_update_product_agent_waiting_products == True):
            self.update_product_agent_waiting_products()
            self.is_update_product_agent_waiting_products = False

    def step(self):
        self.update_current_spot_id()
        self.handle_product_changed()
        if (self.try_manufacture() == True):
            return

        self.old_pos = self.pos
        if (self.find_backward() == False):
            self.find_forward()

    def update_current_spot_id(self):
        if (self.is_in_spot_pos() == True):
            spot_agent = self.get_cellmates(self.pos)[0]
            self.current_spot_id = str(spot_agent.name)

    def handle_product_changed(self):
        current_product = self.model.get_current_processing_product()
        if (current_product != self.current_product):
            self.reset_work()
            self.current_product = current_product

    def is_moving(self):
        current_pos = tuple(self.pos)
        if (self.old_pos == None or is_equal_pos(current_pos, self.old_pos)):
            return False
        return True

    def prepare_work(self):
        self.current_doing_duration = 0
        spot_agent = self.get_cellmates(self.pos)[0]
        self.current_product_processing_duration = spot_agent.product_processing_duration_dict[self.current_product]

    def start_work(self):
        self.prepare_work()
        return self.progress_work()

    def reset_work(self):
        self.current_doing_duration = None

    def progress_work(self):
        kanban_pos = convert_spot_pos_to_kanban_pos(self.pos)
        kanban_agent = self.model.grid.get_cell_list_contents([kanban_pos])[0]
        if (kanban_agent.is_any_available_kanban() == False):
            self.update_waiting_step_count()
            return
        kanban_agent.consume()
        self.current_doing_duration += 1
        self.update_working_step_count()
        return self.handle_done_work()

    def update_working_step_count(self):
        self.total_working_step_count += 1
        self.working_step_count_dict[self.current_spot_id] += 1

    
    def update_waiting_step_count(self):
        self.waiting_step_count_dict[self.current_spot_id] += 1
        self.total_waiting_step_count += 1

    def handle_done_work(self):
        if (self.current_doing_duration >= self.current_product_processing_duration):
            self.is_update_product_agent_waiting_products = True
            self.reset_work()
            return True
        return False

    def try_manufacture(self):
        if (self.current_doing_duration is None):
            # If had just done or waiting, try to continue if available
            if (self.try_to_continue_if_available == True):
                if (self.is_moving() == False and self.check_if_anything_new_to_do() == True):
                    self.start_work()
                    return True

            return False

        self.progress_work()
        return True

    def update_product_agent_waiting_products(self):
        product_pos = convert_spot_pos_to_product_pos(self.pos)
        # Not first_position
        if (product_pos is not None):
            product_agent = self.model.grid.get_cell_list_contents([product_pos])[0]
            product_agent.update_waiting_product(self.current_product, False)

        next_product_pos = convert_spot_pos_to_next_product_pos(self.pos)
        if (next_product_pos is not None):
            next_product_agent = self.model.grid.get_cell_list_contents([next_product_pos])[0]
            next_product_agent.update_waiting_product(self.current_product, True)

        # last_position
        else:
            self.model.update_num_finished_product()

    def check_if_anything_new_to_do(self):
        product_pos = convert_spot_pos_to_product_pos(self.pos)
        if (product_pos is not None):
            is_there_any_product = self.check_if_any_waiting_product(product_pos)
            is_next_waiting_products_max = self.check_if_next_waiting_products_max(self.pos)
            return is_there_any_product == True and is_next_waiting_products_max == False

        # first position
        else:
            return False

    def is_in_spot_pos(self):
        return True in (is_equal_pos(self.pos, spot_pos)
                        for spot_pos in get_spot_pos_list)

    def is_spot_pos_in_vision(self, spot_pos):
        distance = 0
        currentX, currentY = tuple(self.pos)
        spot_posX, spot_posY = spot_pos
        if (is_equal_pos(self.pos, spot_pos) == False and currentX == spot_posX):
            distance += 2
        distance += abs(currentX - spot_posX) + abs(currentY - spot_posY)
        if (distance <= self.movement_radius):
            return True
        return False

    def find_backward(self):
        isSucceeded = False
        reversed_spot_pos_key_list = list(reversed(spot_pos_dict_conf.keys()))
        for key in reversed_spot_pos_key_list:
            spot_pos = get_spot_pos_from_dict(key)
            if (self.is_spot_pos_in_vision(spot_pos) == False):
                continue

            is_there_any_person_agent = self.check_if_any_other_person_agent_in_spot_pos(spot_pos)

            product_pos = convert_spot_pos_to_product_pos(spot_pos)
            is_next_waiting_products_max = self.check_if_next_waiting_products_max(spot_pos)
            if (product_pos is not None):
                is_there_any_product = self.check_if_any_waiting_product(product_pos)
                if (is_there_any_person_agent == False and is_there_any_product == True and is_next_waiting_products_max == False):
                    self.move_agent(spot_pos, True)
                    isSucceeded = True
                    return isSucceeded

            # first position
            else:
                if (is_there_any_person_agent == False and is_next_waiting_products_max == False):
                    self.move_agent(spot_pos, True)
                    isSucceeded = True
                    return isSucceeded
        return isSucceeded

    def check_if_any_waiting_product(self, product_pos):
        product_agent = self.model.grid.get_cell_list_contents([product_pos])[0]
        return product_agent.check_if_any_waiting_product(self.current_product)

    def check_if_next_waiting_products_max(self, spot_pos):
        is_max_waiting_products_next_product_pos = False
        next_product_pos = convert_spot_pos_to_next_product_pos(spot_pos)
        if (next_product_pos is not None):
            next_product_agent = self.model.grid.get_cell_list_contents([next_product_pos])[0]
            is_max_waiting_products_next_product_pos = next_product_agent.check_if_waiting_product_max(self.current_product)
        return is_max_waiting_products_next_product_pos

    def get_cellmates(self, pos):
        all_agents_in_cell = self.model.grid.get_cell_list_contents([pos])
        return [agent for agent in all_agents_in_cell if agent.unique_id != self.unique_id]

    def check_if_any_other_person_agent_in_spot_pos(self, spot_pos):
        cellmates = self.get_cellmates(spot_pos)
        return len(cellmates) > 1

    def find_forward(self):
        for spot_pos in spot_pos_dict_conf.values():
            if (self.is_spot_pos_in_vision(spot_pos) == False):
                continue
            is_there_any_person_agent = self.check_if_any_other_person_agent_in_spot_pos(spot_pos)

            if (is_there_any_person_agent == False):
                self.move_agent(spot_pos, False)
                return

    def move_agent(self, destination_spot, force_start):
        next_pos = self.calculate_next_pos(destination_spot)
        if (is_equal_pos(next_pos, self.pos) == True):
            if (force_start == True):
                self.start_work()
            else:
                self.update_waiting_step_count()
        else:
            self.total_moving_step_count += 1
        self.model.grid.move_agent(self, next_pos)

    def calculate_next_pos(self, destination):
        # if (self.pos is None):
        #     return None
        currentX, currentY = tuple(self.pos)
        destX, destY = destination

        nextPosition = (currentX, currentY)

        is_in_spot_pos = self.is_in_spot_pos()
        if (is_in_spot_pos == True and is_equal_pos(self.pos, destination) == False):
            if (currentX == left_x_pos_spot_column):
                nextPosition = (currentX+1, currentY)
            else:
                nextPosition = (currentX-1, currentY)
        else:
            if (currentY < destY):
                nextPosition = (currentX, currentY+1)
            elif (currentY > destY):
                nextPosition = (currentX, currentY-1)
            else:
                if (currentX < destX):
                    nextPosition = (currentX+1, currentY)
                elif (currentX > destX):
                    nextPosition = (currentX-1, currentY)
        
        return nextPosition
