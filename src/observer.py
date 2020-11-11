from math import floor
import pygame
from src.maze import Maze
from src.player import Player


class Observer:
    def __init__(self):
        self.width = 1000
        self.height = 800
        self.player = Player(x=15, y=15, width=10, height=10, speed=1)
        self.game_display = None
        self.tile_size = 25
        self.wall_size = 1
        self.maze = Maze(x=20, y=10, tile_size=self.tile_size,
                         wall_size=self.wall_size)  # , file="..\\image\\maze.png")

    def draw(self):
        self.game_display.fill((255, 255, 255))
        self.game_display.blit(self.maze.img, (0, 0))

        # player
        pygame.draw.rect(self.game_display, (255, 0, 0), self.player.get_rect())

        pygame.display.update()

    def update(self):
        self.get_input()
        self.draw()

    def add_game_display(self, game_display):
        self.game_display = game_display
        self.maze.convert_image()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0]:
            self.player.x = pygame.mouse.get_pos()[0]
            self.player.y = pygame.mouse.get_pos()[1]

        new_x, new_y = self.player.x, self.player.y
        if keys[pygame.K_UP]:
            new_y -= self.player.speed
        if keys[pygame.K_DOWN]:
            new_y += self.player.speed
        if keys[pygame.K_LEFT]:
            new_x -= self.player.speed
        if keys[pygame.K_RIGHT]:
            new_x += self.player.speed

        # moving vertically
        player_up_tile = floor((new_y - self.player.height / 2) / self.tile_size)
        player_down_tile = floor((new_y + self.player.height / 2) / self.tile_size)
        player_left_tile = floor((self.player.x - self.player.width / 2) / self.tile_size)
        player_right_tile = floor((self.player.x + self.player.width / 2) / self.tile_size)

        if self.can_move_vert(player_up_tile, player_down_tile, player_left_tile, player_right_tile):
            self.player.y = new_y

        # moving horizontally
        player_up_tile = floor((self.player.y - self.player.height / 2) / self.tile_size)
        player_down_tile = floor((self.player.y + self.player.height / 2) / self.tile_size)
        player_left_tile = floor((new_x - self.player.width / 2) / self.tile_size)
        player_right_tile = floor((new_x + self.player.width / 2) / self.tile_size)

        if self.can_move_hori(player_up_tile, player_down_tile, player_left_tile, player_right_tile):
            self.player.x = new_x

    def can_move_vert(self, player_up_tile, player_down_tile, player_left_tile, player_right_tile):
        if player_up_tile < 0 or player_down_tile >= self.maze.height:
            return False
        if player_up_tile == player_down_tile:
            return True
        if player_left_tile != player_right_tile:
            return not (self.maze.horizontal[player_up_tile, player_left_tile] or
                        self.maze.horizontal[player_up_tile, player_right_tile] or
                        self.maze.vertical[player_up_tile, player_left_tile] or
                        self.maze.vertical[player_down_tile, player_left_tile])
        else:
            return not self.maze.horizontal[player_up_tile, player_left_tile]

    def can_move_hori(self, player_up_tile, player_down_tile, player_left_tile, player_right_tile):
        if player_left_tile < 0 or player_right_tile >= self.maze.width:
            return False
        if player_left_tile == player_right_tile:
            return True
        if player_up_tile != player_down_tile:
            return not (self.maze.vertical[player_up_tile, player_left_tile] or
                        self.maze.vertical[player_down_tile, player_left_tile] or
                        self.maze.horizontal[player_up_tile, player_left_tile] or
                        self.maze.horizontal[player_up_tile, player_right_tile])
        else:
            if player_left_tile == player_right_tile:
                return True
            else:
                return not self.maze.vertical[player_up_tile, player_left_tile]
