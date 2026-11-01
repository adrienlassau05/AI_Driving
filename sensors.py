import math
from config import MAX_SENSOR_RANGE, NUMBER_OF_SENSORS, SENSOR_ANGLES


def sensor(car, mask, track, offset=0):
    WIDTH, HEIGHT = track.get_width(), track.get_height()

    radians = math.radians(car.angle)
    offset_rads = math.radians(offset)
    dx = math.sin(radians + offset_rads)
    dy = math.cos(radians + offset_rads)
    position = [car.x, car.y]
    distance = 0

    while not mask.get_at((int(position[0]), int(position[1]))):
        if position[0] - dx >= WIDTH or position[0] - dx < 0:
            break
        elif position[1] - dy >= HEIGHT or position[1] - dy < 0:
            break
        else:
            position[0] -= dx
            position[1] -= dy
        x_distance = position[0] - car.x
        y_distance = position[1] - car.y
        distance = math.sqrt(x_distance**2 + y_distance**2)
        if distance >= MAX_SENSOR_RANGE:
            break
    return distance

def observation_vector(car, mask, track):        
    vector = [car.vel / car.max_vel]
    for i in range(NUMBER_OF_SENSORS):
        distance = sensor(car, mask, track, SENSOR_ANGLES[i])
        vector.append(distance / MAX_SENSOR_RANGE)
    return vector