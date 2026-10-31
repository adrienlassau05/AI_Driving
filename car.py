from utils import blit_rotate_center, scale_image
import math
import pygame as pg

BLACK_CAR = scale_image(pg.image.load('car_black.png'), 0.3)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.x_prev, self.y_prev = self.START_POS
        self.acceleration = 0.15
        self.on_finish = False
        
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
            
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
            
    def move(self):
        radians = math.radians(self.angle)
        verticle = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.x_prev, self.y_prev = self.x, self.y
        self.y -= verticle
        self.x -= horizontal
        
    def collide(self, mask, x=0, y=0):
        rotated = pg.transform.rotate(self.img, self.angle)
        rect = rotated.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        car_mask = pg.mask.from_surface(rotated)
        offset = (int(rect.x - x), int(rect.y - y))
        return mask.overlap(car_mask, offset)
    
    def update(self, steer, throttle):   # steer in [-1, 1], throttle in [-1, 1]
        self.angle -= steer * self.rotation_vel
        if throttle > 0:   
            self.vel = min(self.vel + throttle * self.acceleration, self.max_vel)
        elif throttle < 0: 
            self.vel = max(self.vel + throttle * self.acceleration, -self.max_vel / 2)
        else:              
            self.vel = max(self.vel - self.acceleration / 2, 0)  
        self.move()
        
    def get_sensor_data(self):
        data = {'speed':self.vel, 'acceleration':self.acceleration, 'angle':self.angle}
        
        
        
class PlayerCar(AbstractCar):
    IMG = BLACK_CAR
    START_POS = (100, 300)
    
    def reduce_speed(self):
            self.vel = max(self.vel - self.acceleration/2, 0)
            self.move()
    
    def bounce(self, mask, x=0, y=0):
        self.vel = - self.vel
        self.move()