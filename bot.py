import pygame
from bullet import Bullet


class Bot(pygame.sprite.Sprite):

    def __init__(self):
        super(Bot, self).__init__()
        self.image = pygame.Surface([16, 16])
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.wall_list = None

        # game variables
        self.score = 0
        self.hit_points = 100
        self.ammo = 100

        # time between bullet shots in milliseconds
        self.reload_time = 500
        self.last_shot_time = pygame.time.get_ticks()

    def reloaded(self):
        if self.last_shot_time > pygame.time.get_ticks() - self.reload_time:
            return False
        else:
            return True


    def move(self, dx, dy):
        """takes movement parameters and applies the value to the x and y coordinates"""
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        """checks for collision into walls while moving coordinates"""
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
        # If you collide with an wall, set the side of the rectangle equal to the wall to give the appearance of
        # collision
        for wall in self.wall_list:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                elif dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                elif dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                elif dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    def shoot_up(self):
            bullet = Bullet(1)
            bullet.rect.x = self.rect.centerx
            bullet.rect.y = self.rect.y - 8
            self.last_shot_time = pygame.time.get_ticks()
            return bullet

    def shoot_down(self):
            bullet = Bullet(2)
            bullet.rect.x = self.rect.centerx
            bullet.rect.y = self.rect.y + 16
            self.last_shot_time = pygame.time.get_ticks()
            return bullet

    def shoot_left(self):
            bullet = Bullet(3)
            bullet.rect.x = self.rect.x - 16
            bullet.rect.y = self.rect.centery
            self.last_shot_time = pygame.time.get_ticks()
            return bullet

    def shoot_right(self):
            bullet = Bullet(4)
            bullet.rect.x = self.rect.x + 16
            bullet.rect.y = self.rect.centery
            self.last_shot_time = pygame.time.get_ticks()
            return bullet
