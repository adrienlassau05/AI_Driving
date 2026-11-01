import pygame as pg
from car import AbstractCar
from track import (TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK,
                   FINISH_POSITION, FINISH_SIGN, WIDTH, HEIGHT)


class Env:
    def __init__(self, render=False, bounce=False):
        self.render = render
        self.bounce = bounce
        self.images = [(TRACK, (0, 0)), (TRACK_BORDER, (0, 0)), (FINISH, FINISH_POSITION)]
        if self.render:
            self.window = pg.display.set_mode((WIDTH, HEIGHT))
            pg.display.set_caption('Epic Lassau Training Track for AIs')
        self.reset()

    def reset(self):
        self.car = AbstractCar()
        self.turns = 0
        self.crossing = True    
        self.done = False

    def collision(self):
        if self.car.collide(TRACK_BORDER_MASK) is not None:
            if self.bounce:
                self.car.bounce()
            else:
                self.done = True

    def check_finish(self):
        finish_collide = self.car.collide(FINISH_MASK, *FINISH_POSITION)

        if finish_collide and self.crossing:
            dy = self.car.y - self.car.y_prev
            if dy < 0:
                self.turns += 1
                self.crossing = False
            elif dy > 0:
                self.turns -= 1
                self.crossing = False
        elif not finish_collide:
            self.crossing = True

        if self.turns == 4:
            self.done = True

    def draw(self):
        if not self.render:
            return
        for img, pos in self.images:
            self.window.blit(img, pos)
        self.car.draw(self.window)
        if self.turns == 4:
            self.window.blit(FINISH_SIGN, (0, 0))
        pg.display.update()