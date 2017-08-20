import blue_player_pilot
from agent import Agent
from bot import Bot
from pathfinder import Pathfinder
from enum import Enum

RECTANGLE_STARTING_X = 900
RECTANGLE_STARTING_Y = 256
MARGIN = 48

RED = (255, 0, 0)


class RedAiPilot(Agent):
    """Controls the behaviors of the red rectangle in the game

    RedAiPilot's decisions are based on its current_behavior state. The state is determined by the conditions of its
    environment. A full list of behaviors can be found at the bottom of the red_ai_pilot module in the
    PilotAgentBehavior class."""

    def __init__(self, environment=None):
        """sets up details about the red rectangle as well as variables for A.I. behavior"""
        super(RedAiPilot, self).__init__("red_ai_pilot", environment)
        self.bot = Bot()
        # set the rectangle's color
        self.bot.image.fill(RED)
        # set the starting position
        self.bot.rect.x = RECTANGLE_STARTING_X
        self.bot.rect.y = RECTANGLE_STARTING_Y
        # place the coordinates of our rectangle in a tuple to update the game manager
        self.red_coordinate = (self.bot.rect.x, self.bot.rect.y)
        self.rect = self.bot.rect

        # these coordinates tell the agent how far away the blue player is
        self.blue_coordinate = None
        self.distance_from_blue_player = 0
        self.current_position = 0

        self.path_course = []
        self.path_found = False
        self.next_node_coordinates = None

        # variables for A.I. behavior
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
                self.path_found = False
                return
            self.find_next_node()
            self.move_to_next_node()
        if self.current_behavior is PilotAgentBehavior.SHOOTING:
            self.determine_enemy_position()
            self.shoot()

    def check_distance_from_opponent(self):
        self.update_coordinates()
        self.distance_from_blue_player = \
            abs(self.blue_coordinate[0] - self.red_coordinate[0]) + abs(self.blue_coordinate[1] - self.red_coordinate[1])

    def determine_behavior(self):
        self.check_distance_from_opponent()
        if self.distance_from_blue_player > 100 and self.bot.hit_points > 50:
            if not self.path_found:
                self.current_behavior = PilotAgentBehavior.FINDING_PATH
            else:
                self.current_behavior = PilotAgentBehavior.CHASING
        elif self.bot.hit_points > 50:
            self.current_behavior = PilotAgentBehavior.SHOOTING
        else:
            self.current_behavior = PilotAgentBehavior.FLEEING

    def determine_enemy_position(self):
        if self.red_coordinate[0] + MARGIN >= self.blue_coordinate[0] >= MARGIN - self.red_coordinate[0]:
            # red player is above blue player
            if self.red_coordinate[1] < self.blue_coordinate[1] - MARGIN:
                self.current_position = PilotCurrentPosition.ABOVE

            # red player is below blue player
            elif self.red_coordinate[1] > self.blue_coordinate[1] + MARGIN:
                self.current_position = PilotCurrentPosition.BELOW

            elif self.red_coordinate[0] > self.blue_coordinate[0]:
                self.current_position = PilotCurrentPosition.RIGHT

            elif self.red_coordinate[0] < self.blue_coordinate[0]:
                self.current_position = PilotCurrentPosition.LEFT

    def find_next_node(self):
        if not (1 <= abs(self.rect.centerx - self.next_node_coordinates[0]) or 1 <= abs(
                    self.rect.centery - self.next_node_coordinates[1])):
            self.path_course.pop(0)
            if self.path_course:
                self.next_node_coordinates = (self.path_course[0].x, self.path_course[0].y)

    def is_healthy(self):
        return self.hit_points > 50

    def make_decision(self):
        self.determine_behavior()
        self.act_out_decision()

    def move_to_next_node(self):

        if self.next_node_coordinates[0] < self.rect.centerx:
            self.bot.move(-2, 0)
        elif self.next_node_coordinates[0] > self.rect.centerx:
            self.bot.move(2, 0)

        # up and down
        if self.next_node_coordinates[1] < self.rect.centery:
            self.bot.move(0, -2)
        elif self.next_node_coordinates[1] > self.rect.centery:
            self.bot.move(0, 2)

    def setup_bot_map(self):
        self.bot.wall_list = self.environment.get_object("wall_list")

    def shoot(self):
        if self.bot.reloaded():
            bullet_list = self.environment.get_object("bullet_list")
            if self.current_position == PilotCurrentPosition.LEFT:
                bullet_list.add(self.bot.shoot_right())
            elif self.current_position == PilotCurrentPosition.RIGHT:
                bullet_list.add(self.bot.shoot_left())
            elif self.current_position == PilotCurrentPosition.ABOVE:
                bullet_list.add(self.bot.shoot_down())
            elif self.current_position == PilotCurrentPosition.BELOW:
                bullet_list.add(self.bot.shoot_up())

    def update_coordinates(self):
        self.red_coordinate = (self.rect.x, self.rect.y)
        self.blue_coordinate = self.ask("blue_player_pilot", "blue_coordinate")


class PilotAgentBehavior(Enum):
    FINDING_PATH = 0
    CHASING = 1
    SHOOTING = 2
    FLEEING = 4
    HIDING = 8


class PilotCurrentPosition(Enum):
    ABOVE = 1
    BELOW = 2
    LEFT = 3
    RIGHT = 4
