from math import floor

import numpy as np
import random

import pygame
from PIL import Image
from PIL import ImageDraw


class Maze:
    def __init__(self, x, y, tile_size, wall_size, file=""):
        self.width = x
        self.height = y
        self.horizontal = None
        self.vertical = None
        self.create_maze(file)
        self.img = self.create_maze_img()

    def create_maze(self, file_name):
        if file_name != "":  # load maze from file
            array = np.array(Image.open(file_name))
            com_array = np.sum(array, axis=2)
            black_array = com_array == (array.shape[2] - 3) * 255
            self.horizontal = black_array[1:2 * self.height:2, 0:2 * self.width:2]
            self.vertical = black_array[0:2 * self.height:2, 1:2 * self.width:2]
        else:  # generate maze
            self.horizontal = np.full((self.height - 1, self.width), True)
            self.vertical = np.full((self.height, self.width - 1), True)
            visited = np.full((self.height, self.width), False)

            current = (0, 0)
            stack = [current]
            while stack:
                visited[current[0], current[1]] = True
                nexts = []
                if current[0] > 0 and not visited[current[0] - 1, current[1]]:
                    nexts.append((current[0] - 1, current[1]))
                if current[0] < self.height - 1 and not visited[current[0] + 1, current[1]]:
                    nexts.append((current[0] + 1, current[1]))
                if current[1] > 0 and not visited[current[0], current[1] - 1]:
                    nexts.append((current[0], current[1] - 1))
                if current[1] < self.width - 1 and not visited[current[0], current[1] + 1]:
                    nexts.append((current[0], current[1] + 1))

                if nexts:
                    next_tile = random.choice(nexts)
                    if current[0] == next_tile[0]:  # if the same row
                        self.vertical[current[0], min(current[1], next_tile[1])] = False
                    else:
                        self.horizontal[min(current[0], next_tile[0]), current[1]] = False
                    stack.append(current)
                    current = next_tile
                else:
                    current = stack.pop()

    def create_maze_img(self):
        tile_size = 25
        wall_size = 1
        img = Image.new("RGB", (self.width * tile_size + wall_size,
                                self.height * tile_size + wall_size), color="white")
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, self.width * tile_size + wall_size - 1,
                        self.height * tile_size + wall_size - 1),
                       outline=(0, 0, 0), fill=(255, 255, 255), width=wall_size)

        for i in range(self.width):
            for j in range(self.height - 1):
                if self.horizontal[j, i]:
                    rect = (i * tile_size + wall_size - wall_size,
                            (j + 1) * tile_size,
                            (i + 1) * tile_size + wall_size - 1,
                            (j + 1) * tile_size + wall_size - 1)
                    draw.rectangle(rect, fill=(0, 0, 0))
        for i in range(self.width - 1):
            for j in range(self.height):
                if self.vertical[j, i]:
                    rect = ((i + 1) * tile_size,
                            j * tile_size + wall_size,
                            (i + 1) * tile_size + wall_size - 1,
                            (j + 1) * tile_size + wall_size -1)
                    draw.rectangle(rect, fill=(0, 0, 0))

        img.save("..\\image\\maze_img.png")
        return img

    def convert_image(self):
        self.img = pygame.image.fromstring(self.img.tobytes(), self.img.size, self.img.mode).convert()
