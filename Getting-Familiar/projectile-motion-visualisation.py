import pygame
import numpy as np
pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fps = 60
timer = pygame.time.Clock()
run = True
wall_thickness = 15
gravity = 0.5
stopper = 0.4
starting_offset = 50
friction_coeff = 0.25
air_coeff = 0.000

class Projectile:
    def __init__(self, x, y, radius, color, mass, speed, angle, retention, id):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.speed = [speed * np.cos(np.radians(angle)), -speed * np.sin(np.radians(angle))]
        self.retention = retention
        self.id = id

    def draw(self):
        self.rect = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_gravity(self):
        if self.y < HEIGHT - self.radius - (wall_thickness/2):
            self.speed[1] += gravity
        else:
            if self.speed[1] > stopper: 
                self.speed[1] *= -self.retention
            elif abs(self.speed[1]) <= stopper:
                self.speed[1] = 0
        if (self.x < self.radius + (wall_thickness/2) and self.speed[0] < 0):
            self.speed[0] *= -self.retention
        if (self.x > WIDTH - self.radius - (wall_thickness/2) and self.speed[0] > 0):
            self.speed[0] *= -self.retention
        return self.speed[0], self.speed[1]


    def update_position(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

    def check_friction(self):
        if self.y >= HEIGHT - self.radius - (wall_thickness/2):
            if abs(self.speed[0]) > stopper:
                self.speed[0] -= friction_coeff * self.mass * gravity * (self.speed[0] / abs(self.speed[0]))
            else:
                self.speed[0] = 0
        return self.speed[0]

    def check_air_resistance(self):
        if (abs(self.speed[0]) > stopper):
            self.speed[0] += air_coeff * -self.speed[0] * abs(self.speed[0])
        else:
            self.speed[0] = 0
        if self.speed[1] != 0:
            self.speed[1] += air_coeff * -self.speed[1] * abs(self.speed[1])
        return self.speed[0], self.speed[1]



main_projectile = Projectile(wall_thickness/2 + starting_offset, HEIGHT - wall_thickness/2 - starting_offset, 25, 'blue', 5, 20, 45, 0.65, 1)

def draw_walls():
    left = pygame.draw.line(screen, (255, 255, 255), (0, 0), (0, HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, (255, 255, 255), (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, (255, 255, 255), (0, 0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, (255, 255, 255), (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness)
    wall_list = [left, right, top, bottom]
    return wall_list

while (run):
    timer.tick(fps)
    screen.fill('lightblue')
    screen.blit(pygame.font.SysFont('Arial', 20).render('Projectile Motion Visualisation', True, (0, 0, 0)), (WIDTH/2 - 100, 10))
    walls = draw_walls()
    main_projectile.draw()
    main_projectile.update_position()
    main_projectile.speed[0], main_projectile.speed[1] = main_projectile.check_gravity()
    main_projectile.speed[0] = main_projectile.check_friction()
    main_projectile.speed[0], main_projectile.speed[1] = main_projectile.check_air_resistance()
    pygame.draw.circle(screen, 'red', (main_projectile.x, main_projectile.y), 5)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
