import pygame
from agent import Agent
from rectangle import Rectangle

RECTANGLE_STARTING_X = 64
RECTANGLE_STARTING_Y = 64

BLUE = (0, 0, 255)


class BluePlayerPilot(Agent):

    def __init__(self, environment=None):
        super(BluePlayerPilot, self).__init__("blue_player_pilot", environment)

        self.rectangle = Rectangle()
        self.rectangle.image.fill(BLUE)
        self.rectangle.rect.x = RECTANGLE_STARTING_X
        self.rectangle.rect.y = RECTANGLE_STARTING_Y

        self.rect = self.rectangle.rect
        self.blue_coordinate = (self.rect.x, self.rect.y)

    def check_input_for_actions(self):
        self.make_movements()
        self.shoot()

    def make_movements(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.move(-2, 0)
        if key[pygame.K_RIGHT]:
            self.move(2, 0)
        if key[pygame.K_UP]:
            self.move(0, -2)
        if key[pygame.K_DOWN]:
            self.move(0, 2)

    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with an wall, set the side of the rectangle equal to the wall to give the appearance of
        # collision
        for wall in self.environment.get_object("wall_list"):
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                elif dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                elif dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                elif dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    def shoot(self):
        pass

