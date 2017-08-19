from agent import Agent
from red_ai_pilot import RedAiPilot
from blue_player_pilot import BluePlayerPilot
from map_builder import MapBuilder
from environment import Environment
import pygame

# event values for handling during game play
SHOOTING = pygame.USEREVENT + 1


class GameManager(Agent):
    """The game_manager handles all agents responsible for making the game run"""

    def __init__(self):
        """sets up the game variables and then initializes its employee agents"""
        super(GameManager, self).__init__("game_manager")
        self.play_window = Environment()

        self.screen = None
        # screen size
        self.screen_height = 444
        self.screen_width = 1116
        self.running_game = True

        # player list
        self.player_list = pygame.sprite.Group()
        self.play_window.add_object("player_list", self.player_list)
        # holds bullet list
        self.bullet_list = pygame.sprite.Group()
        self.play_window.add_object("bullet_list", self.bullet_list)
        # holds the sprites that make up the wall
        self.wall_list = pygame.sprite.Group()
        self.play_window.add_object("wall_list", self.wall_list)

        # initialize agents and place them in the environment
        self.map_builder = MapBuilder(self.play_window)
        self.red_ai_pilot = RedAiPilot(self.play_window)
        self.blue_player_pilot = BluePlayerPilot(self.play_window)

    def build_walls(self):
        """calls the map builder agent to parse through the level file and create the map of the game"""
        self.map_builder.build_arena()
        self.wall_list = self.play_window.get_object("wall_list")

    def check_bullet_collisions(self):
        """checks if any bullets have collided with objects and need to be removed"""
        pass

    def check_pygame_events(self):
        """checks any for events such as keys pressed or A.I. actions that change the state of the game"""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running_game = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running_game = False

    def draw(self):
        """displays the game images on the screen"""
        self.screen.fill((0, 0, 0))
        self.player_list.draw(self.screen)
        self.wall_list.draw(self.screen)
        self.bullet_list.draw(self.screen)
        pygame.display.flip()

    def initialize_screen(self):
        # Set up the display
        pygame.display.set_caption("BOT ARENA 3.0!")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def run_game(self):
        """calls the player agent's to perform their moves and check's for bullet movement"""
        self.check_pygame_events()
        self.red_ai_pilot.make_decision()
        self.blue_player_pilot.check_input_for_actions()
        self.check_bullet_collisions()
        self.update()
        self.draw()

    def setup_players(self):
        """adds the player sprites to the list of players for reference"""
        self.player_list.add(self.red_ai_pilot.rectangle, self.blue_player_pilot.rectangle)

    def update(self):
        self.bullet_list = self.play_window.get_object("bullet_list")



