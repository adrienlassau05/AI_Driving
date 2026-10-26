import pygame as pg
import time, math
from utils import scale_image, blit_rotate_center

TRACK = scale_image(pg.image.load('training_track_1.png'), 1)
BLACK_CAR = scale_image(pg.image.load('car_black.png'), 0.3)
TRACK_BORDER = scale_image(pg.image.load('border_training_track_mask_hard.png'), 1)
TRACK_BORDER_MASK = pg.mask.from_surface(TRACK_BORDER)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Epic Lassau Training Track for AIs')

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.15
        
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
        
        self.y -= verticle
        self.x -= horizontal
        
    def collide(self, mask, x=0, y=0):
        rotated = pg.transform.rotate(self.img, self.angle)
        rect = rotated.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        car_mask = pg.mask.from_surface(rotated)
        offset = (int(rect.x - x), int(rect.y - y))
        return mask.overlap(car_mask, offset)
        
        
class PlayerCar(AbstractCar):
    IMG = BLACK_CAR
    START_POS = (100, 200)
    
    def reduce_speed(self):
            self.vel = max(self.vel - self.acceleration/2, 0)
            self.move()
    
    def bounce(self, mask, x=0, y=0):
        self.vel = - self.vel
        self.move()

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
    player_car.draw(win)
    pg.display.update()

def move_player(player_car):
    keys = pg.key.get_pressed()
    moved = False
    if keys[pg.K_a]:
        player_car.rotate(left=True)
    if keys[pg.K_d]:
        player_car.rotate(right=True)
    if keys[pg.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pg.K_s]:
        moved = True
        player_car.move_backward()
        
    if not moved:
        player_car.reduce_speed()


running = True
clock = pg.time.Clock()
images = [(TRACK, (0, 0)), (TRACK_BORDER, (0,0))]
player_car = PlayerCar(8, 4)

while running:
    clock.tick(FPS)
    
    draw(WINDOW, images, player_car)
        
    for event in pg.event.get():
         if event.type == pg.QUIT:
             running = False
             break
    move_player(player_car)
    
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce(TRACK_BORDER_MASK)

pg.quit()