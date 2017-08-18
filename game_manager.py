from agent import Agent
from red_ai_pilot import RedAiPilot
from blue_player_pilot import BluePlayerPilot
from map_builder import MapBuilder
from environment import Environment
import pygame
import os




# event values for handling during gameplay
SHOOTING = pygame.USEREVENT + 1



class GameManager(Agent):

    def __init__(self):
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

    # place the agents in the environment
        self.map_builder = MapBuilder(self.play_window)
        self.red_ai_pilot = RedAiPilot(self.play_window)
        self.blue_player_pilot = BluePlayerPilot(self.play_window)


    def build_walls(self):
        self.map_builder.build_arena()
        self.wall_list = self.play_window.get_object("wall_list")

    def check_bullet_collisions(self):
        pass

    def check_pygame_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running_game = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running_game = False

    def draw(self):
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
        self.check_pygame_events()
        self.red_ai_pilot.make_decision()
        self.blue_player_pilot.check_input_for_actions()
        self.check_bullet_collisions()
        self.update()
        self.draw()

    def setup_players(self):
        self.player_list.add(self.red_ai_pilot.rectangle, self.blue_player_pilot.rectangle)

    def update(self):
        self.bullet_list = self.play_window.get_object("bullet_list")


    # # this list is for any object that stops bullets
    # solid_object = pygame.sprite.Group(player_list, wall_list)
    # Player.set_objects(solid_object)
    #
    # # This object holds all of our AI code
    # ai = AIHandler(red_player, blue_player, health_pack)
    #
    # # shoot 2 rounds per second
    # pygame.time.set_timer(SHOOTING, 500)
    #
    # game_running = True
    #
    # while game_running:
    #
    #     clock.tick(60)
    #
    #     for e in pygame.event.get():
    #         if e.type == pygame.QUIT:
    #             game_running = False
    #         if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
    #             game_running = False
    #         if e.type == pygame.MOUSEBUTTONDOWN:
    #             bullet_list.add(blue_player.shoot_left())
    #         if e.type == SHOOTING and ai.current_action == ai.SHOOTING:
    #             bullet_list.add(ai.shoot_bullets())
    #
    #     # handle ai actions
    #     ai.run_battle()
    #
    #     # Blue Player Movement
    #     key = pygame.key.get_pressed()
    #     if key[pygame.K_LEFT]:
    #         blue_player.move(-2, 0)
    #     if key[pygame.K_RIGHT]:
    #         blue_player.move(2, 0)
    #     if key[pygame.K_UP]:
    #         blue_player.move(0, -2)
    #     if key[pygame.K_DOWN]:
    #         blue_player.move(0, 2)
    #
    #     # Red Player Movement
    #     move = pygame.key.get_pressed()
    #     if move[pygame.K_a]:
    #         red_player.move(-2, 0)
    #     if move[pygame.K_d]:
    #         red_player.move(2, 0)
    #     if move[pygame.K_w]:
    #         red_player.move(0, -2)
    #     if move[pygame.K_s]:
    #         red_player.move(0, 2)
    #     if move[pygame.K_SPACE]:
    #         bullet_list.add(red_player.shoot_right())
    #
    #     for bullet in bullet_list:
    #         collided = bullet.update(solid_object)
    #         if collided:
    #             bullet_list.remove(bullet)
    #


