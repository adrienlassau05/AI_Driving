import math
import pygame as pg
from utils import blit_rotate_center
from config import MAX_VEL, ROTATION_VEL, CAR_IMG
from track import START_ANGLE, START_POSITION


class AbstractCar:
    def __init__(self):
        self.img = CAR_IMG
        self.max_vel = MAX_VEL
        self.vel = 0
        self.rotation_vel = ROTATION_VEL
        self.angle = START_ANGLE
        self.x, self.y = START_POSITION
        self.x_prev, self.y_prev = START_POSITION
        self.acceleration = 0.15

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        radians = math.radians(self.angle)
        verticle = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.x_prev, self.y_prev = self.x, self.y
        self.y -= verticle
        self.x -= horizontal

    def update(self, steer, throttle):   # steer in [-1, 1], throttle in [-1, 1]
        self.angle -= steer * self.rotation_vel
        if throttle > 0:
            self.vel = min(self.vel + throttle * self.acceleration, self.max_vel)
        elif throttle < 0:
            self.vel = max(self.vel + throttle * self.acceleration, -self.max_vel / 2)
        else:
            self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        rotated = pg.transform.rotate(self.img, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        car_mask = pg.mask.from_surface(rotated)
        offset = (int(rect.x - x), int(rect.y - y))
        return mask.overlap(car_mask, offset)

    def bounce(self):
        self.vel = -self.vel
        self.move()