from mesa import Agent
import random
from utilities import *
import enum


class Status(enum.Enum):
    Free = 1
    GoingTo = 2
    Comeback = 3,
    Filling = 4,
    Loading = 5


class Agv_Agent(Agent):
    def __init__(self, unique_id, model, home_coordinate, loading_step):
        super().__init__(unique_id, model)
        self.home_coordinate = home_coordinate
        self.loading_step = loading_step
        self.current_loading_step = 0
        self.filling_pos = None
        self.kanban_pos = None
        self.status = Status.Free
        self.set_status_loading = False
        self.distance_from_home_to_cornerX = 3
        if (self.unique_id == 0):
            self.cornerX = self.home_coordinate[0] - \
                self.distance_from_home_to_cornerX
        else:
            self.cornerX = self.home_coordinate[0] + \
                self.distance_from_home_to_cornerX

    def refill_kanban(self, destination):
        self.kanban_pos = destination
        self.filling_pos = convert_kanban_pos_to_filling_pos(
            destination, str(self.unique_id))
        self.status = Status.GoingTo
        self.fulfill_duty()

    def advance(self):
        if (self.set_status_loading == True):
            self.status = Status.Loading
            self.set_status_loading = False

    def fulfill_duty(self):
        if (self.status == Status.Loading):
            self.status = Status.Free
            return True
        if (self.status == Status.Free):
            return False
        if (self.status == Status.GoingTo):
            if (self.current_loading_step >= self.loading_step):
                self.current_loading_step = 0
                self.goTo()
            else:
                self.current_loading_step += 1
        elif (self.status == Status.Filling):
            self.filling_kanban()
            self.status = Status.Comeback
        elif (self.status == Status.Comeback):
            self.comeBack()
        return True

    def goTo(self):
        if (self.go_horizontally() == True):
            self.go_vertically()

    def comeBack(self):
        if (self.comeback_vertically() == True):
            self.comeback_horizontally()

    def filling_kanban(self):
        kanban_agent = self.model.grid.get_cell_list_contents(
            [self.kanban_pos])[0]
        kanban_agent.refill()

    def comeback_vertically(self):
        currentX, currentY = tuple(self.pos)
        if (currentY == self.home_coordinate[1]):
            return True
        next_posX = currentX
        next_posY = currentY + 1
        next_pos = (next_posX, next_posY)
        self.model.grid.move_agent(self, next_pos)
        return False

    def go_vertically(self):
        currentX, currentY = tuple(self.pos)
        next_posX = currentX
        next_posY = currentY - 1
        next_pos = (next_posX, next_posY)
        if (is_equal_pos(self.filling_pos, next_pos) == True):
            self.status = Status.Filling
        self.model.grid.move_agent(self, next_pos)

    def comeback_horizontally(self):
        currentX, currentY = tuple(self.pos)
        next_posX = int(currentX -
                        ((self.cornerX - self.home_coordinate[0]) /
                         self.distance_from_home_to_cornerX))
        next_posY = currentY
        next_pos = (next_posX, next_posY)
        if (is_equal_pos(self.home_coordinate, next_pos) == True):
            self.set_status_loading = True
        self.model.grid.move_agent(self, next_pos)

    def go_horizontally(self):
        currentX, currentY = tuple(self.pos)
        if (currentX == self.cornerX):
            return True
        next_posX = int(currentX -
                        ((self.home_coordinate[0] - self.cornerX) /
                         self.distance_from_home_to_cornerX))
        next_posY = currentY
        next_pos = (next_posX, next_posY)
        self.model.grid.move_agent(self, next_pos)
        return False

    def is_at_home(self):
        if (self.status == Status.Loading or self.status == Status.Free):
            return True
        return False

    def step(self):
        return
