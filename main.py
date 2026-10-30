import pygame as pg
import time, math
from utils import scale_image, blit_rotate_center
from car import PlayerCar

TRACK = scale_image(pg.image.load('training_track_1.png'), 1)
TRACK_BORDER = scale_image(pg.image.load('border_training_track_mask_hard.png'), 1)
TRACK_BORDER_MASK = pg.mask.from_surface(TRACK_BORDER)

FINISH = scale_image(pg.image.load('finish.png'), 1.22)
FINISH_MASK = pg.mask.from_surface(FINISH)
FINISH_POSTION =  (75, 250)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Epic Lassau Training Track for AIs')

FPS = 60


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
images = [(TRACK, (0, 0)), (TRACK_BORDER, (0,0)), (FINISH, FINISH_POSTION)]
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
    
    # finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSTION)
    
    # if finish_poi_collide != None:
    #     if finish_poi_collide[1] == 0:
    #         player_car.bounce(FINISH_MASK)
        

pg.quit()