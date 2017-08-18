import blue_player_pilot
from agent import Agent
from rectangle import Rectangle
from pathfinder import Pathfinder
from enum import Enum

RECTANGLE_STARTING_X = 900
RECTANGLE_STARTING_Y = 256

RED = (255, 0, 0)


class RedAiPilot(Agent):
    def __init__(self, environment=None):
        super(RedAiPilot, self).__init__("red_ai_pilot", environment)
        self.rectangle = Rectangle()
        # set the rectangle's color
        self.rectangle.image.fill(RED)
        # set the starting position
        self.rectangle.rect.x = RECTANGLE_STARTING_X
        self.rectangle.rect.y = RECTANGLE_STARTING_Y
        # place the coordinates of our rectangle in a tuple to update the game manager
        self.red_coordinate = (self.rectangle.rect.x, self.rectangle.rect.y)
        self.rect = self.rectangle.rect

        # these coordinates tell the agent how far away the blue player is
        self.blue_coordinate = None
        self.distance_from_blue_player = 0

        self.path_course = []
        self.path_found = False
        self.next_node_coordinates = None

        # game variables
        self.score = 0
        self.hit_points = 100
        self.ammo = 100

        # variables for A.I. behavior
        self.healthy = 1.0
        self.is_healthy = True
        self.winning = False

        self.current_behavior = PilotAgentBehavior.FINDING_PATH
        self.pathfinder = Pathfinder()

    def act_out_decision(self):
        if self.current_behavior == PilotAgentBehavior.FINDING_PATH:
            self.path_course = self.pathfinder.find_path(self.blue_coordinate)
            self.path_found = True
            self.next_node_coordinates = (self.path_course[0].x, self.path_course[0].y)
        if self.current_behavior == PilotAgentBehavior.CHASING:
            if not self.path_course:
                return
            self.find_next_node()
            self.move_to_next_node()



    def check_distance_from_opponent(self):
        self.blue_coordinate = self.ask("blue_player_pilot", "blue_coordinate")
        self.distance_from_blue_player = \
            abs(self.blue_coordinate[0] - self.red_coordinate[0]) + abs(self.blue_coordinate[1] - self.red_coordinate[1])

    def determine_behavior(self):
        self.check_distance_from_opponent()
        if self.distance_from_blue_player > 100 and self.hit_points > 50:
            if not self.path_found:
                self.current_behavior = PilotAgentBehavior.FINDING_PATH
            else:
                self.current_behavior = PilotAgentBehavior.CHASING
        elif self.hit_points > 50:
            self.current_behavior = PilotAgentBehavior.SHOOTING
        else:
            self.current_behavior = PilotAgentBehavior.FLEEING

    def find_next_node(self):
        if not (1 <= abs(self.rect.centerx - self.next_node_coordinates[0]) or 1 <= abs(
                    self.rect.centery - self.next_node_coordinates[1])):
            self.path_course.pop(0)
            if self.path_course:
                self.next_node_coordinates = (self.path_course[0].x, self.path_course[0].y)

    def make_decision(self):
        self.determine_behavior()
        self.act_out_decision()

    def move(self, dx, dy):
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

    def move_to_next_node(self):

        if self.next_node_coordinates[0] < self.rect.centerx:
            self.move(-2, 0)
        elif self.next_node_coordinates[0] > self.rect.centerx:
            self.move(2, 0)

        # up and down
        if self.next_node_coordinates[1] < self.rect.centery:
            self.move(0, -2)
        elif self.next_node_coordinates[1] > self.rect.centery:
            self.move(0, 2)


class PilotAgentBehavior(Enum):
    FINDING_PATH = 0
    CHASING = 1
    SHOOTING = 2
    FLEEING = 4
    HIDING = 8
