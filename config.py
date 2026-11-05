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
LAP_NUMBER = 2

#Training settings
RUN_TIME = 2         #measured in hours
POPULATION_SIZE = 20

#Reward functions
CRASH_PENALTY = -100
CHECKPOINT_REWARD = 15
LAP_REWARD = 100
TIME_PENALTY = -0.01

#Neural Network
HIDDEN_LAYERS = 1
NODES_LAYER1 = 6
