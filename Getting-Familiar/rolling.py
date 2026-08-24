import numpy as np
import pygame
import pygame.freetype
import pygame_gui as gui

WIDTH, HEIGHT = 1200, 600
fps = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rolling Objects Simulation")
timer = pygame.time.Clock()
display_font = pygame.freetype.SysFont('Arial', 15)
gui_manager = gui.UIManager((WIDTH, HEIGHT))
run = True

class RollingObject:
    def __init__(self, x, y, rotation, mass, radius, friction, id):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.mass = mass
        self.radius = radius
        self.friction = friction
        self.id = id

    def draw(self):
        self.rect = pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

obj1 = RollingObject(20, 85, 0, 1, 20, 0.5, 1)

while (run):
    time_delta = timer.tick(fps)/1000.0
    screen.fill('lightblue')
    display_font.render_to(screen, (WIDTH/2, 10), "Rolling Objects Simulation", (0, 0, 0))
    pygame.draw.polygon(screen, 'black', [(0, 100), (WIDTH, HEIGHT), (0, HEIGHT)])
    obj1.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
    timer.tick(fps)
