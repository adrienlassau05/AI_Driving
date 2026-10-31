import pygame as pg
from utils import scale_image


TRACK = scale_image(pg.image.load('training_track_1.png'), 1)
TRACK_BORDER = scale_image(pg.image.load('border_training_track_mask_hard.png'), 1)
TRACK_BORDER_MASK = pg.mask.from_surface(TRACK_BORDER)

FINISH = scale_image(pg.image.load('finish.png'), 1.22)
FINISH_SIGN = pg.image.load('finish_sign.png')
FINISH_MASK = pg.mask.from_surface(FINISH)
FINISH_POSTION =  (75, 250)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Epic Lassau Training Track for AIs')