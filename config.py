import pygame as pg
from utils import scale_image

CAR_IMG = scale_image(pg.image.load('car_black.png'), 0.3)
MAX_VEL = 10
ROTATION_VEL = 4
MAX_SENSOR_RANGE = 100
NUMBER_OF_SENSORS = 7
SENSOR_ANGLES = (90, 60, 30, 0, -30, -60, -90)
FPS = 60
MAX_TRAINING_STEPS = 7200