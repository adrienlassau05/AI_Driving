import pygame as pg
from config import FPS, LAP_NUMBER
from env import Env
from track import WIDTH, HEIGHT


def move_player():
    keys = pg.key.get_pressed()
    steer, throttle = 0, 0
    if keys[pg.K_a]:
        steer = -1
    if keys[pg.K_d]:
        steer = 1
    if keys[pg.K_w]:
        throttle = 1
    if keys[pg.K_s]:
        throttle = -1
    return (steer, throttle)

running = True
clock = pg.time.Clock()
env = Env(render=True, bounce=True, show_gates=True)
print(WIDTH, HEIGHT)
while running:
    clock.tick(FPS)
    env.draw()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            break
    if env.done == True and env.turns != LAP_NUMBER+1:
        env.done = False
    action = move_player()
    env.step(action)
    
pg.quit()