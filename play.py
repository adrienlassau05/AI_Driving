import pygame as pg
from utils import scale_image, blit_rotate_center
from car import PlayerCar, BLACK_CAR
from track import TRACK, TRACK_BORDER, TRACK_BORDER_MASK, FINISH, FINISH_POSTION, FINISH_MASK, FINISH_SIGN, WINDOW
from sensors import sensor

FPS = 60

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
    player_car.draw(win)

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
    hit_point = sensor(player_car, 0)
    pg.draw.line(WINDOW, (0, 255, 0), (int(player_car.x), int(player_car.y)), (int(hit_point[0]), int(hit_point[1])), 2) 
    pg.draw.circle(WINDOW, (255, 0, 0), (int(hit_point[0]), int(hit_point[1])), 5)
    hit_point = sensor(player_car, 30)
    pg.draw.line(WINDOW, (0, 255, 0), (int(player_car.x), int(player_car.y)), (int(hit_point[0]), int(hit_point[1])), 2) 
    pg.draw.circle(WINDOW, (255, 0, 0), (int(hit_point[0]), int(hit_point[1])), 5)
    hit_point = sensor(player_car, -30)
    pg.draw.line(WINDOW, (0, 255, 0), (int(player_car.x), int(player_car.y)), (int(hit_point[0]), int(hit_point[1])), 2) 
    pg.draw.circle(WINDOW, (255, 0, 0), (int(hit_point[0]), int(hit_point[1])), 5)
    
    pg.draw.circle(
    WINDOW,
    (255, 0, 255),
    (int(player_car.x), int(player_car.y)),
    5
)
    pg.display.update()
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce(TRACK_BORDER_MASK)
    
    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSTION)
    
    if finish_poi_collide and player_car.check_finish == True:
        dy = player_car.y - player_car.y_prev
        if dy < 0:
            turns += 1
            player_car.check_finish = False
        elif dy > 0:
            turns -= 1
            player_car.check_finish = False
    elif not finish_poi_collide:
        player_car.check_finish = True

    if turns == 4:
        player_car.bounce(FINISH_MASK)
        images.append((FINISH_SIGN, (0, 0)))
    
        

pg.quit()