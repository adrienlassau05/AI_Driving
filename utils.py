import pygame as pg

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pg.transform.scale(img, size)


def blit_rotate_center(win, image, center, angle):
    rotated_image = pg.transform.rotate(image, angle)
    rect = rotated_image.get_rect(center=center)
    win.blit(rotated_image, rect)