from mesa import Agent
import random
from utilities import *
import enum


class Status(enum.Enum):
    Free = 1
    GoingTo = 2
    Comeback = 3,
    Filling = 4


class Agv_Agent(Agent):
    def __init__(self, unique_id, model, home_coordinate):
        super().__init__(unique_id, model)
        self.home_coordinate = home_coordinate
        self.destination = None
        self.status = Status.Free
        self.set_status_free = False
        self.distance_from_home_to_cornerX = 3
        if (self.unique_id == 0):
            self.cornerX = self.home_coordinate[0] - \
                self.distance_from_home_to_cornerX
        else:
            self.cornerX = self.home_coordinate[0] + \
                self.distance_from_home_to_cornerX

    def refill_kanban(self, destination):
        destinationX, destinationY = destination
        if (self.unique_id == 0):
            destinationX -= 1
        else:
            destinationX += 1
        self.destination = (destinationX, destinationY)
        self.status = Status.GoingTo
        self.fulfill_duty()

    def advance(self):
        if (self.set_status_free == True):
            self.Status = Status.Free
            self.set_status_free = False

    def fulfill_duty(self):
        if (self.status == Status.Free):
            return False
        if (self.status == Status.GoingTo):
            if (self.go_horizontally() == True):
                self.go_vertically()
        elif (self.status == Status.Filling):
            self.status = Status.Comeback
        elif (self.status == Status.Comeback):
            if (self.comeback_vertically() == True):
                self.comeback_horizontally()
        return True

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
        if (is_equal_pos(self.destination, next_pos) == True):
            self.status = Status.Filling
        self.model.grid.move_agent(self, next_pos)

    def comeback_horizontally(self):
        currentX, currentY = tuple(self.pos)
        next_posX = (currentX -
                     ((self.home_coordinate[0] - self.cornerX) /
                      self.distance_from_home_to_cornerX)) * -1
        next_posY = currentY
        next_pos = (next_posX, next_posY)
        if (is_equal_pos(self.home_coordinate, next_pos) == True):
            self.set_status_free = True
        self.model.grid.move_agent(self, next_pos)

    def go_horizontally(self):
        currentX, currentY = tuple(self.pos)
        if (currentX == self.cornerX):
            return True
        next_posX = currentX - \
            ((self.home_coordinate[0] - self.cornerX) /
             self.distance_from_home_to_cornerX)
        next_posY = currentY
        next_pos = (next_posX, next_posY)
        self.model.grid.move_agent(self, next_pos)
        return False

    def is_at_home(self):
        if (self.pos is None or is_equal_pos(self.pos, self.home_coordinate) == True):
            return True
        return False

    def step(self):
        return
