import pygame as pg

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pg.transform.scale(img, size)


def blit_rotate_center(win, image, center, angle):
    rotated_image = pg.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=center)
    win.blit(rotated_image, rect)

def crossed(p_prev, p_now, a, b):
    def side(p, q, r):
        return (q[0]-p[0]) * (r[1]-p[1]) - (q[1]-p[1]) * (r[0]-p[0])
    return (side(a, b, p_prev) * side(a, b, p_now) < 0 and side(p_prev, p_now, a) * side(p_prev, p_now, b) < 0)
    
