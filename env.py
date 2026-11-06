import pygame as pg
from car import AbstractCar
from track import (TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_MASK,
                   FINISH_POSITION, FINISH_SIGN, WIDTH, HEIGHT, CHECKPOINTS)
from config import MAX_TRAINING_STEPS, CRASH_PENALTY, LAP_REWARD, CHECKPOINT_REWARD, LAP_NUMBER, TIME_PENALTY
from utils import crossed
import math

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
        self.crossing = True   
        self.finish = False 
        self.done = False
        self.steps = 0
        self.reward = 0
        self.checkpoint = 0
        self.total_checkpoint = 0
        self.prev_dist = None
        self.last_cp = 0 
        self.idle = 0

    def collision(self):
        if self.car.collide(TRACK_BORDER_MASK) is not None:
            if self.bounce:
                self.car.bounce()
            else:
                self.done = True

    # def check_finish(self):
    #     finish_collide = self.car.collide(FINISH_MASK, *FINISH_POSITION)

    #     if finish_collide and self.crossing:
    #         dy = self.car.y - self.car.y_prev
    #         if dy < 0:
    #             self.turns += 1
    #             self.crossing = False
    #         elif dy >= 0:
    #             self.turns -= 1
    #             self.crossing = False
    #     elif not finish_collide:
    #         self.crossing = True

    #     if self.turns == LAP_NUMBER+1:
    #         self.finish = True

    def draw(self):
        if not self.render:
            return
        for img, pos in self.images:
            self.window.blit(img, pos)
        if self.show_gates:
            for pos in CHECKPOINTS:
                pg.draw.line(self.window, (0, 255, 0), pos[0], pos[1], 2)
        self.car.draw(self.window)
        if self.finish:
            self.window.blit(FINISH_SIGN, (0, 0))
        
        pg.display.update()
        

    def checkpoint_progress(self):
        if self.done:
            return

        dx = self.car.x - self.car.x_prev
        dy = self.car.y - self.car.y_prev
        if dx == 0 and dy == 0:
            return
        a, b, needed_speed, _ = CHECKPOINTS[self.checkpoint]
        
        forward = needed_speed[0] * dx + needed_speed[1] * dy > 0
        if forward and crossed((self.car.x_prev, self.car.y_prev), (self.car.x, self.car.y), a, b):
            self.checkpoint = (self.checkpoint + 1) % len(CHECKPOINTS)
            self.total_checkpoint += 1
            self.prev_dist = None
            self.reward += CHECKPOINT_REWARD
        
        a, b, _, _ = CHECKPOINTS[self.checkpoint]
        mid = ((a[0]+b[0])/2, (a[1]+b[1])/2)
        dist = math.hypot(self.car.x - mid[0], self.car.y - mid[1])
        
        if self.prev_dist is not None:
            self.reward += 0.1*(self.prev_dist - dist)
        self.prev_dist = dist


    def step(self, action):
        steer, throttle = action
        self.car.update(steer, throttle)
        self.collision()
        self.checkpoint_progress()

        if self.total_checkpoint >= 32 * LAP_NUMBER:
            self.finish = True
            self.done = True
            
        if self.total_checkpoint > self.last_cp:
            self.last_cp = self.total_checkpoint
            self.idle = 0
        else:
            self.idle += 1
            if self.idle > 300:
                self.done = True
        
        if self.steps >= MAX_TRAINING_STEPS:
            self.done = True
            return self.reward
        
        
        if self.done and not self.finish:
            self.reward += CRASH_PENALTY
   
        elif self.finish:
            self.reward += LAP_REWARD 
            self.done = True
            
        self.steps += 1
        self.reward += TIME_PENALTY
        return self.reward


        
        