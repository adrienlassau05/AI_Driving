from track import TRACK_BORDER_MASK
import math

def sensor(car, offset):
    radians = math.radians(car.angle)
    offset_rads = math.radians(offset)
    dx = math.sin(radians + offset_rads)
    dy = math.cos(radians + offset_rads)
    position = [car.x, car.y]
    while not TRACK_BORDER_MASK.get_at((int(position[0]), int(position[1]))):
        position[0] -= dx
        position[1] -= dy
    return position