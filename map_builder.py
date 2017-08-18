from agent import Agent
import pygame

class MapBuilder(Agent):

    def __init__(self, environment=None):
        super(MapBuilder, self).__init__("map_builder", environment)
        self.wall_list = self.environment.get_object("wall_list")
        self.map_with_nodes = []
        self.node_list = []
        self.node_step = 2
        self.GRID_INCREMENT = 12
        self.screen_width = self.ask("game_manager", "screen_width")

    def convert_map_to_2d_array(self):
        multidimensional_map_array = []
        for y, line in enumerate(self.map_with_nodes):
            line_list = []
            for x, letter in enumerate(line):
                line_list.append(letter)
            # print(line_list)
            multidimensional_map_array.append(line_list)
        return multidimensional_map_array

    def create_node_graph(self):
        self.form_nodes()
        self.form_node_connections()

    def form_nodes(self):
        x = y = matrix_position_counter = 0
        for row in self.map_with_nodes:
            for column in row:
                if column == "N":
                    node = Node(matrix_position_counter, x, y, None)
                    # add the new node to our list
                    self.node_list.append(node)
                x += 12
                matrix_position_counter += 1
            y += 12
            x = 0

    def form_node_connections(self):
        multidimensional_array_map = self.convert_map_to_2d_array()
        # for each node we check 8 directions (Top, Top Right, Right, etc.) for neighboring nodes to connect to.
        # if the node exists in that position we create a connection to it
        for node in self.node_list:
            x = int(node.x / self.GRID_INCREMENT)
            y = int(node.y / self.GRID_INCREMENT)
            direction = 1
            while direction <= 8:
                counter = 1
                is_clear = True
                # Direction starts at top above the current node and moves in a clockwise direction
                if direction == 1:
                    dy = -1
                    dx = 0
                elif direction == 2:
                    dy = -1
                    dx = 1
                elif direction == 3:
                    dy = 0
                    dx = 1
                elif direction == 4:
                    dy = 1
                    dx = 1
                elif direction == 5:
                    dy = 1
                    dx = 0
                elif direction == 6:
                    dy = 1
                    dx = -1
                elif direction == 7:
                    dy = 0
                    dx = -1
                elif direction == 8:
                    dy = -1
                    dx = -1

                # these variables help us increment through the matrix
                inc_dy = dy
                inc_dx = dx
                # we check our matrix for any wall objects ('W') that exist between our node and the neighboring
                # node. If there are no walls in between, then the path is clear and we can add the node to our list of
                # connections.
                while counter <= self.node_step:
                    if multidimensional_array_map[y + dy][x + dx] != 'W':
                        if counter != self.node_step:
                            dy += inc_dy
                            dx += inc_dx
                        counter += 1
                    else:
                        is_clear = False
                        break
                if is_clear:
                    node_connection_number = (y + dy) * (self.screen_width / self.GRID_INCREMENT) + (x + dx)
                    node.connections.append(node_connection_number)
                direction += 1

    '''
    Here we iterate through our starting map and look for spaces where we can insert nodes. Nodes are represented by the
    letter N and wall symbols are represented by W. We place a node every certain number of spaces, determined by the node
    step.
    '''
    def insert_nodes_into_map(self):
            for y, line in enumerate(level_map):
                if y % self.node_step == 0:
                    letter_list = []
                    for x, letter in enumerate(line):

                        if x % self.node_step == 0 and letter != 'W':
                            letter = 'N'
                        letter_list.append(letter)
                    node_line = ''.join(letter_list)
                    self.map_with_nodes.append(node_line)
                else:
                    self.map_with_nodes.append(line)



    def build_arena(self):
        self.construct_walls()
        self.insert_nodes_into_map()
        self.create_node_graph()

    def construct_walls(self):
        # Parse the level_map string.
        x = y = 0
        for row in level_map:
            for col in row:
                if col == "W":
                    wall = Wall(x, y, 4, 4)
                    self.wall_list.add(wall)

                x += self.GRID_INCREMENT
            y += self.GRID_INCREMENT
            x = 0


level_map = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                           W                                               W",
    "W                                           W                                               W",
    "W                                           W                                W              W",
    "W                                           W                                W              W",
    "W                                           W                                W              W",
    "W                                           W                                W              W",
    "W                                           W                                W              W",
    "W                                           W                                W              W",
    "W                                           W                                W              W",
    "W                               WWWWWWWWWWWWWWWWWWWWWWWWWW                   W              W",
    "W                                                                            W              W",
    "W                                                             WWWWWWWWWWWWWWWW              W",
    "W                                                             W                             W",
    "W                                                             W                             W",
    "W                                                             W                             W",
    "W               WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW                   W",
    "W               W                                                                           W",
    "W               W                                                                           W",
    "W               W                                              W                            W",
    "W        WWWWWWWW                                              W                            W",
    "W               W                                              W              WWWWW         W",
    "W               W               WWWWW    WWWWWWWWWWWWWWWWWWWWWWW                 W          W",
    "W               WWWWWWWWWWWWWWWWW                              W                 WWWWWWWWWWWW",
    "W                                                              W                 W          W",
    "W                                                              W                 W          W",
    "W               W                                              W                 W          W",
    "W               W                            WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW   W          W",
    "WWWWWWWWWWWWWWWWW                            W                                              W",
    "W               W                            W                                              W",
    "W               W                            W                                              W",
    "W               W                            W                                              W",
    "W               W                            W                                              W",
    "W                             WWWWWWWWWWWWWWWW                    WWWWWWWWWWW               W",
    "W                             W                                             W               W",
    "W                             W                                             W               W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, length, width):
        super(Wall, self).__init__()
        self.image = pygame.Surface([length, width])
        self.rect = pygame.Rect(x, y, length, width)
        self.image.fill((255, 255, 255))


class Node:
    def __init__(self, name, x, y, connections):
        self.name = name
        self.x = x
        self.y = y
        self.connections = []

        # this variable keeps track of which node preceded it in our path
        previous_node = None

        # value for A* algorithm
        self.f = 0
        self.g = 0

        if connections is None:
            return

        for i in range(len(connections) - 1):
            self.connections += [connections[i]]
            print("connection: " + connections[i])