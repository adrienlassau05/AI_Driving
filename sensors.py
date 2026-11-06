import math
from config import MAX_SENSOR_RANGE, NUMBER_OF_SENSORS, SENSOR_ANGLES


def sensor(car, mask, offset=0, step=2):
    WIDTH, HEIGHT = mask.get_size()
    radians = math.radians(car.angle + offset)
    dx, dy = math.sin(radians), math.cos(radians)
    x, y = car.x, car.y
    dist = 0
    while dist < MAX_SENSOR_RANGE:
        nx, ny = x-dx, y-dy
        if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
            break
        x, y = nx, ny
        dist += step
        if mask.get_at((int(x), int(y))):
            break
    return dist


def observation_vector(car, mask):        
    vector = [car.vel / car.max_vel]
    for i in range(NUMBER_OF_SENSORS):
        distance = sensor(car, mask, SENSOR_ANGLES[i])
        vector.append(distance / MAX_SENSOR_RANGE)
    return vector