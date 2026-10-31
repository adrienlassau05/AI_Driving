import pygame as pg
from utils import scale_image, blit_rotate_center
from car import PlayerCar
from track import TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_POSTION, FINISH_MASK, FINISH_SIGN, WINDOW

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
turns = 0
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
    
    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSTION)
    if finish_poi_collide:
        dy = player_car.y - player_car.y_prev
        if not player_car.on_finish:
            if dy > 0:            #clear this up as its not working correctly atm 
                turns += 1
            elif dy < 0:
                turns -= 1
            print(turns)
        player_car.on_finish = True
    else:
        player_car.on_finish = False
    if turns == 4:
        player_car.bounce(FINISH_MASK)
        images.append((FINISH_SIGN, (0, 0)))
    
        

pg.quit()