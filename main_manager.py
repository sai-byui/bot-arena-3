from agent import Agent
from game_manager import GameManager
import pygame
import os


class MainManager(Agent):

    def __init__(self):
        super(MainManager, self).__init__("main_manager")
        self.game_manager = GameManager()
        self.clock = None


    def initialize_pygame(self):
        # initialize pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        # clock to keep track of frame rate
        self.clock = pygame.time.Clock()



    def manage_bot_arena(self):
        self.initialize_pygame()
        self.game_manager.initialize_screen()
        self.game_manager.setup_players()
        self.game_manager.build_walls()

        while self.game_manager.running_game:
            self.clock.tick(60)
            self.game_manager.run_game()

main_manager = MainManager()
main_manager.manage_bot_arena()


