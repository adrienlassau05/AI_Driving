import pygame as pg
from car import AbstractCar
from track import (TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK,
                   FINISH_POSITION, FINISH_SIGN, WIDTH, HEIGHT, CHECKPOINTS)
from config import MAX_TRAINING_STEPS, CRASH_PENALTY, LAP_REWARD, CHECKPOINT_REWARD, LAP_NUMBER


class Env:
    def __init__(self, render=False, bounce=False, show_gates=False):
        self.render = render
        self.bounce = bounce
        self.show_gates = show_gates
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
        self.steps = 0
        self.reward = 0
        self.checkpoint = 15

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

        if self.turns == LAP_NUMBER+1:
            self.done = True

    def draw(self):
        if not self.render:
            return
        for img, pos in self.images:
            self.window.blit(img, pos)
        if self.show_gates:
            for pos in CHECKPOINTS:
                pg.draw.line(self.window, (0, 255, 0), pos[0], pos[1], 2)
        self.car.draw(self.window)
        if self.turns == 4:
            self.window.blit(FINISH_SIGN, (0, 0))
        
        pg.display.update()
        
    def check_checkpoint(self):
        dx = self.car.x - self.car.x_prev
        dy = self.car.y - self.car.y_prev
        checkpoint_list = [i for i, v in enumerate(CHECKPOINTS) if v[3] - 1 == self.checkpoint]
        needed_speed = CHECKPOINTS[checkpoint_list[0]][2]
        checkpoint_position = (CHECKPOINTS[checkpoint_list[0]][0], CHECKPOINTS[checkpoint_list[0]][1])
        if needed_speed[0] == 0 and needed_speed[1] * dy > 0:
            if self.car.y < checkpoint_position[0][1] and needed_speed[1] < 0:
                self.checkpoint += 1
            elif self.car.y > checkpoint_position[0][1] and needed_speed[1] > 0:
                self.checkpoint += 1
                print('it worked')
        elif needed_speed[1] == 0 and needed_speed[0] * dx > 0:
            if self.car.x == 12002:
                print('wow')

    def step(self, action):
        steer, throttle = action
        self.car.update(steer, throttle)
        self.collision()
        self.check_finish()
        self.check_checkpoint()
        if self.steps >= MAX_TRAINING_STEPS:
            self.done = True
        
        
        if self.done == True and self.turns != LAP_NUMBER+1:
            self.reward += CRASH_PENALTY
        elif self.turns == LAP_NUMBER+1:
            self.reward += LAP_REWARD 
        self.steps += 1
        


        
        