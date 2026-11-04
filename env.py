import pygame as pg
from car import AbstractCar
from track import (TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK,
                   FINISH_POSITION, FINISH_SIGN, WIDTH, HEIGHT, CHECKPOINTS)
from config import MAX_TRAINING_STEPS, CRASH_PENALTY, LAP_REWARD, CHECKPOINT_REWARD, LAP_NUMBER
from utils import crossed

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
        self.checkpoint = 0

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
                print(self.turns)
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
        

    def checkpoint_progress(self):
        if self.done:
            return
        if self.checkpoint == 32:
            self.checkpoint = 0
        dx = self.car.x - self.car.x_prev
        dy = self.car.y - self.car.y_prev
        if dx == 0 and dy == 0:
            return
        a, b, needed_speed, _ = CHECKPOINTS[self.checkpoint]
        
        forward = needed_speed[0] * dx + needed_speed[1] * dy > 0
        if forward and crossed((self.car.x_prev, self.car.y_prev), (self.car.x, self.car.y), a, b):
            self.checkpoint += 1
            print(self.checkpoint)
                
        

    def step(self, action):
        steer, throttle = action
        self.car.update(steer, throttle)
        self.collision()
        self.check_finish()
        self.checkpoint_progress()
        
        if self.steps >= MAX_TRAINING_STEPS:
            self.done = True
            return 0
        
        if self.done == True and self.turns != LAP_NUMBER+1:
            self.reward += CRASH_PENALTY
   
        elif self.turns == LAP_NUMBER+1:
            self.reward += LAP_REWARD 
        self.steps += 1
        return self.reward


        
        