import pygame
import numpy as np
import pygame.freetype
import pygame_gui as gui

WIDTH, HEIGHT = 1200, 600
pygame.init()
display_font = pygame.freetype.SysFont('Arial', 15)
title_font = pygame.freetype.SysFont('Arial', 22)
ui_manager = gui.UIManager((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
run = True

fps = 60
wall_thickness = 15
starting_offset = 50
stopper = 0.5

gravity = 0.98
friction_coeff = 0.25
static_friction_coeff = 0.4
air_coeff = 0.001

v = [20, 30, 15]
angles = [45, 75, 30]

restart_button = gui.elements.UIButton(relative_rect = pygame.Rect((WIDTH - 150, 10), (100, 30)), text = "Restart", manager = ui_manager)
input_field_v1 = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((WIDTH - 300, 10), (100, 30)), manager = ui_manager, object_id = "input_field_v1", initial_text = "20", placeholder_text = "Enter Speed for 1")
input_field_v2 = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((WIDTH - 300, 40), (100, 30)), manager = ui_manager, object_id = "input_field_v2", initial_text = "30", placeholder_text = "Enter Speed for 2")
input_field_v3 = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((WIDTH - 300, 70), (100, 30)), manager = ui_manager, object_id = "input_field_v3", initial_text = "15", placeholder_text = "Enter Speed for 3")
angle_field_1 = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((WIDTH - 450, 10), (100, 30)), manager = ui_manager, object_id = "angle_field_1", initial_text = "45", placeholder_text = "Enter Angle for 1")
angle_field_2 = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((WIDTH - 450, 40), (100, 30)), manager = ui_manager, object_id = "angle_field_2", initial_text = "75", placeholder_text = "Enter Angle for 2")
angle_field_3 = gui.elements.UITextEntryLine(relative_rect = pygame.Rect((WIDTH - 450, 70), (100, 30)), manager = ui_manager, object_id = "angle_field_3", initial_text = "30", placeholder_text = "Enter Angle for 3")

def draw_walls():
    left = pygame.draw.line(screen, (255, 255, 255), (0, 0), (0, HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, (255, 255, 255), (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, (255, 255, 255), (0, 0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, (255, 255, 255), (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness)
    wall_list = [left, right, top, bottom]
    return wall_list

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
            if abs(self.mass * gravity * friction_coeff * self.speed[0]) > abs(self.mass * gravity * static_friction_coeff):
                self.speed[0] -= friction_coeff * self.mass * gravity * (self.speed[0] / abs(self.speed[0]))
            else:
                self.speed[0] = 0
        return self.speed[0]

    def check_air_resistance(self):
        if abs(self.speed[0]) > stopper:
            self.speed[0] += air_coeff * -self.speed[0] * abs(self.speed[0])
        else:
            self.speed[0] = 0
        if self.speed[1] != 0:
            self.speed[1] += air_coeff * -self.speed[1] * abs(self.speed[1])
        return self.speed[0], self.speed[1]

def make_projectiles(v, angles):
    projectiles = []
    projectiles.append(Projectile(wall_thickness/2 + starting_offset, HEIGHT - wall_thickness/2 - starting_offset, 25, 'blue', 5, v[0], angles[0], 0.65, 1))
    projectiles.append(Projectile(wall_thickness/2 + starting_offset, HEIGHT - wall_thickness/2 - starting_offset, 20, 'red', 7, v[1], angles[1], 0.7, 2))
    projectiles.append(Projectile(wall_thickness/2 + starting_offset, HEIGHT - wall_thickness/2 - starting_offset, 40, 'green', 10, v[2], angles[2], 0.45, 3))
    return projectiles

projectiles = make_projectiles(v, angles)

while (run):
    time_delta = timer.tick(fps) / 1000.0
    screen.fill('lightblue')
    title_font.render_to(screen, (WIDTH/2 - 100, 10), 'Projectile Motion Visualisation', (0, 0, 0))
    walls = draw_walls()
    display_font.render_to(screen, (10, 90), f"Gravity: {gravity}, Friction coeffs: {friction_coeff}, {static_friction_coeff}, Air Resistance: {air_coeff}")
    for projectile in projectiles:
        projectile.draw()
        projectile.update_position()
        projectile.speed[0], projectile.speed[1] = projectile.check_gravity()
        projectile.speed[0] = projectile.check_friction()
        projectile.speed[0], projectile.speed[1] = projectile.check_air_resistance()
        display_font.render_to(screen, (10, 10 + projectile.id * 20), f"Projectile{projectile.id} Position: {round(projectile.x)}, {round(projectile.y)} Projectile {projectile.id} Speed : {round(projectile.speed[0], 2)}, {round(projectile.speed[1], 2)}", (0, 0, 0))
        display_font.render_to(screen, (projectile.x, projectile.y), f"{projectile.id}", (0, 0, 0))

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == restart_button:
                v = []
                angles = []
                for input_field in [input_field_v1, input_field_v2, input_field_v3]:
                    try:
                        if input_field.get_text() != '':
                            value = float(input_field.get_text())
                            if value < 0:
                                raise ValueError("Value must be non-negative.")
                        else:
                            value = 0
                        v.append(value)
                    except ValueError as e:
                        print(f"Invalid input: {e}")

                for angle_field in [angle_field_1, angle_field_2, angle_field_3]:
                    try:
                        if angle_field.get_text() != '':
                            value = float(angle_field.get_text())
                            if value < 0 or value > 180:
                                raise ValueError("Angle must be within 1st and 2nd quadrant.")
                        else:
                            value = 0
                        angles.append(value)
                    except ValueError as e:
                        print(f"Invalid input: {e}")

                if len(v) == 3 and len(angles) == 3: 
                    projectiles = make_projectiles(v, angles)

        ui_manager.process_events(event)
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()