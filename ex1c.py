'''
c) Finally, modify the game loop so that by using the right mouse button,
 you can add particles with radius 0.25 and mass 2.
Hint: The number code for the right mouse button is 3
. Remember to also modify the function "add_particle".
'''
import pygame
import math

class Particle:
    def __init__(self, m=1, x=0, y=0, v_x=0, v_y=0, colour=pygame.Color("orange"), radius=0.5):
        self.m = m
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = 0
        self.a_y = 0

        self.colour = colour
        self.radius = radius

    def draw(self, env):
        centre = env.env_to_screen(self.x, self.y)
        size = self.radius * env.scale
        pygame.draw.circle(env.screen, self.colour, centre, size)


class Environment:
    def __init__(self, screen):
        self.screen = screen

        self.width_pixels = self.screen.get_width()
        self.height_pixels = self.screen.get_height()
        self.width = 10
        self.scale = self.width_pixels / self.width
        self.height = self.height_pixels / self.scale

        self.g = 10
        self.particles = []
        self.dt = 0.01

    def update(self):
        for p in self.particles:
            if p.y > 0:
                p.a_y = -self.g
            elif p.y < 0:
                p.a_y = self.g
            else:
                p.a_y = 0

            p.x += self.dt * p.v_x
            p.y += self.dt * p.v_y

            p.v_x += self.dt * p.a_x
            p.v_y += self.dt * p.a_y

               
            velocity = math.sqrt(p.v_x**2 + p.v_y**2)
            if velocity > 3.0:
                p.colour = pygame.Color("purple")
            else:
                p.colour = pygame.Color("orange")


    def draw(self):
        self.screen.fill(pygame.Color("white"))
        for p in self.particles:
            p.draw(self)

    def env_to_screen(self, x, y):
        x_screen = self.scale * x + self.width_pixels / 2
        y_screen = -self.scale * y + self.height_pixels / 2

        return x_screen, y_screen

    def screen_to_env(self, x_screen, y_screen):
        x = (x_screen - self.width_pixels / 2) / self.scale
        y = -(y_screen - self.height_pixels / 2) / self.scale

        return x, y

    def add_particle(self, x, y, v_x=0, v_y=0, m=1):
        self.particles.append(Particle(m=m, x=x, y=y, v_x=v_x, v_y=v_y))


# Initialise Pygame
pygame.init()

# Screen size
width, height = 1200, 1000

# Create the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collision simulation v0")

# Create a clock
FPS = 60
clock = pygame.time.Clock()

# Create the environment
env = Environment(screen)

# Game loop
running = True
while running:
    # Handle all the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Create a particle with mouse (left click == 1)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_screen_start, y_screen_start = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x_screen_end, y_screen_end = event.pos
            v_x = (x_screen_start - x_screen_end) * 0.03
            v_y = -(y_screen_start - y_screen_end) * 0.03
            x, y = env.screen_to_env(x_screen_start, y_screen_start)
            env.add_particle(x, y, v_x, v_y)

        # Create a particle with right mouse click (right click == 3)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = env.screen_to_env(*event.pos)
            env.add_particle(x, y, 0, 0, radius = 0.25, mass = 2)

    # Update the positions and velocities of the objects
    env.update()

    # Update the screen
    env.draw()
    pygame.display.update()
    clock.tick(FPS)


