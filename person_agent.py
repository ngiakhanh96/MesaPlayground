from mesa import Agent
from utilities import *


class Person_Agent(Agent):
    def __init__(self, unique_id, model, current_product, each_step_duration):
        super().__init__(unique_id, model)
        self.current_product = current_product
        self.each_step_duration = each_step_duration
        self.current_doing_duration = None
        self.old_pos = self.pos
        self.is_update_product_agent_waiting_products = False
        self.moving_step_count = 0
        self.working_step_count = 0

    def advance(self):
        if (self.is_update_product_agent_waiting_products == True):
            self.update_product_agent_waiting_products()
            self.is_update_product_agent_waiting_products = False

    def step(self):
        self.check_if_change_product()
        if (self.is_manufacturing() == True):
            return

        self.old_pos = self.pos
        if (self.find_backward() == False):
            self.find_forward()

    def check_if_change_product(self):
        current_product = self.model.get_current_processing_product()
        if (current_product != self.current_product):
            self.reset_work()
            self.each_step_duration = self.model.get_current_processing_product_step()
            self.current_product = current_product

    def is_moving(self):
        current_pos = tuple(self.pos)
        if (self.old_pos == None or is_equal_pos(current_pos, self.old_pos)):
            return False
        return True

    def prepare_work(self):
        self.current_doing_duration = 0

    def start_work(self):
        self.prepare_work()
        return self.progress_work()

    def reset_work(self):
        self.current_doing_duration = None

    def progress_work(self):
        kanban_pos = convert_spot_pos_to_kanban_pos(self.pos)
        kanban_agent = self.model.grid.get_cell_list_contents(
            [kanban_pos])[0]
        if (kanban_agent.is_any_available_kanban() == False):
            return
        kanban_agent.consume()
        self.current_doing_duration += 1
        self.working_step_count += 1
        return self.check_if_done_work()

    def check_if_done_work(self):
        if (self.current_doing_duration >= self.each_step_duration):
            self.is_update_product_agent_waiting_products = True
            self.reset_work()
            return True
        return False

    def is_manufacturing(self):
        if (self.current_doing_duration is None):
            # If had just done or waiting
            if (self.is_moving() == False and self.check_if_anything_new_to_do() == True):
                self.start_work()
                return True
            return False

        self.progress_work()
        return True

    def update_product_agent_waiting_products(self):
        product_pos = convert_spot_pos_to_product_pos(self.pos)
        if (product_pos is not None):
            product_agent = self.model.grid.get_cell_list_contents(
                [product_pos])[0]

            product_agent.update_waiting_product(self.current_product, False)
            next_product_pos = convert_spot_pos_to_next_product_pos(self.pos)
            if (next_product_pos is not None):
                next_product_agent = self.model.grid.get_cell_list_contents(
                    [next_product_pos])[0]
                next_product_agent.update_waiting_product(
                    self.current_product, True)

            # last_position
            else:
                self.model.update_num_finished_product()

        # first position
        else:
            next_product_pos = convert_spot_pos_to_next_product_pos(self.pos)
            next_product_agent = self.model.grid.get_cell_list_contents(
                [next_product_pos])[0]
            next_product_agent.update_waiting_product(
                self.current_product, True)

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

    def calculate_next_pos(self, destination, start_doing=True):
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

        if (is_equal_pos(nextPosition, destination) and start_doing == True):
            self.prepare_work()

        if (is_equal_pos(nextPosition, self.pos) and start_doing == True):
            self.start_work()

        return nextPosition

    def find_backward(self):
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
                    self.move_agent(spot_pos, True)
                    isSucceeded = True
                    return isSucceeded

            # first position
            else:
                is_next_waiting_products_max = self.check_if_next_waiting_products_max(
                    spot_pos)
                if (is_there_any_person_agent == False and is_next_waiting_products_max == False):
                    self.move_agent(spot_pos, True)
                    isSucceeded = True
                    return isSucceeded
        return isSucceeded

    def check_if_any_waiting_product(self, product_pos):
        product_agent = self.model.grid.get_cell_list_contents(
            [product_pos])[0]

        return product_agent.check_if_any_waiting_product(self.current_product)

    def check_if_next_waiting_products_max(self, spot_pos):
        is_max_waiting_products_next_product_pos = False
        next_product_pos = convert_spot_pos_to_next_product_pos(spot_pos)
        if (next_product_pos is not None):
            next_product_agent = self.model.grid.get_cell_list_contents(
                [next_product_pos])[0]
            is_max_waiting_products_next_product_pos = next_product_agent.check_if_waiting_product_max(
                self.current_product)
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
                self.move_agent(spot_pos, False)
                return

    def move_agent(self, destination_spot, start_doing):
        next_pos = self.calculate_next_pos(destination_spot, start_doing)
        if (is_equal_pos(self.pos, next_pos) == False):
            self.moving_step_count += 1
        self.model.grid.move_agent(self, next_pos)
