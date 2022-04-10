from gc import get_objects
from re import X
import pygame
import random
import time
from gym import Env
from gym.spaces import Box, Discrete
import numpy as np
import sys
from tensorflow import keras

sys.path.append("./game/")
import config
import statistics

pygame.font.init()


# TODO
# quit button
# scorea save to file
# add background
# done, reward, info
# speed parameter
# after teaching learn sklearn basen on outoput of ai
# finish cleaing function

# if ---- change y
class Object(object):
    def __init__(self, x, y, shape=None):
        if not shape:
            self.shape = random.choice(config.shapes)
        else:
            self.shape = shape
        self._rotation = 0
        self.current_position = self.get_positions()
        self._x = self.current_position[0][0]
        self._y = self.current_position[0][1]

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self._x = self.current_position[0][0]
        self._y = self.current_position[0][1]
        self.current_position = self.get_positions(self._x, self._y, rotate=True)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.current_position = self.get_positions()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.current_position = self.get_positions()

    def get_positions(self, x=7, y=0, rotate=False):
        position = []
        if rotate:
            x += 2
            y += 1
        rot = self.rotation % len(self.shape)
        for i, row in enumerate(self.shape[rot][::-1]):
            for j, element in enumerate(row):
                if element == "0":
                    position.append((x - i - 1, y - j))

        return position


class Game(Env):
    def __init__(self, user=False):
        self.grid = self.create_grid()
        self.current_object = self.get_object(config.shapes[2])
        self.user = user
        self.done = False
        self.reward = 0
        self.iter = 0
        self.action_space = Discrete(4)
        self.observation_space = Box(low=0, high=1, dtype=int, shape=(20, 10))
        self.state = self.get_state()
        self.locked_positions = []
        self.grid_reward = 0

    def create_grid(self):
        return np.zeros(20 * 10).reshape(20, 10)

    def reset(self):
        self.grid = self.create_grid()
        self.iter = 0
        self.done = False
        self.locked_positions = []
        self.current_object = self.get_object(config.shapes[2])
        return self.grid

    def draw_locked_pos(self):
        for y, x in self.locked_positions:
            if y < 20:
                self.grid[y][x] = 1

    def draw_object(self):
        for x, y in self.current_object.current_position:
            if y >= 0:
                try:
                    self.grid[y][x] = 1
                except:
                    self.done = True

    def check_object_lock(self):
        for y, x in self.locked_positions:
            if (x, y - 1) in self.current_object.current_position:
                for x, y in self.current_object.current_position:
                    self.locked_positions.append((y, x))

                self.iter = 0
                return True

        for x, y in self.current_object.current_position:
            if y >= 19:
                for y, x in self.current_object.current_position:
                    self.locked_positions.append((x, y))

                self.iter = 0
                return True
        return False

    def object_rotate(self):
        pass

    def get_state(self):
        return self.grid

    def get_object(self, shape=None):
        return Object(5, 0, shape)

    def possible_move(self, move):
        for x, y in self.current_object.current_position:
            x_next = x + move
            if x_next < 0 or x_next > 9:

                return False
            if (x_next, y) in self.locked_positions:

                return False
        for y, x in self.locked_positions:
            if (x - 1, y) in self.current_object.current_position:

                return False
            elif (x + 1, y) in self.current_object.current_position:

                return False

        return True

    def move_object(self, move_x, move_y=1):
        if move_x:
            if self.possible_move(move_x):
                for i, (x, y) in enumerate(self.current_object.current_position):
                    self.current_object.current_position[i] = (x + move_x, y + move_y)
        else:
            for i, (x, y) in enumerate(self.current_object.current_position):
                self.current_object.current_position[i] = (x, y + move_y)

    def clear_row(self):
        cleared = 0
        for i, row in enumerate(self.grid):
            if all(row):
                cleared += 1
                for x in range(10):
                    self.grid[i][x] = 0
                for row_id in range(i - 1, -1, -1):
                    for x in range(10):
                        self.grid[row_id + 1][x] = self.grid[row_id][x]

                self.locked_positions = []
                for i, row in enumerate(self.grid[::-1]):
                    if any(row):
                        for j, x in enumerate(row):
                            if x:
                                self.locked_positions.append((19 - i, j))
                    else:
                        break
        return 100 * cleared

    def reward_fun(self):
        grid_copy = self.grid.copy()

        for y, x in self.current_object.current_position:
            grid_copy[x][y] = 0
        number_of_blocks = []
        height = []
        non_empty_columns = 0
        for x in range(0, 10):
            number_of_blocks.append(sum(grid_copy[:, x]))
            if number_of_blocks[-1]:
                non_empty_columns += 1
                height.append(20 - np.where(grid_copy[:, x] == 1)[0][0])
            else:
                height.append(0)
        holes = []
        for h, n in zip(height, number_of_blocks):
            holes.append(h - n)

        bump = []

        bump.append(height[0] - height[1])

        for i in range(1, 9):
            average_height = int((height[i - 1] + height[i + 1]) / 2)
            bump.append(height[i] - average_height)
        bump.append(height[9] - height[9])

        reward = 0
        reward -= np.sum(holes)
        if not 1 / (np.sum(bump) / 10) > 100:
            reward += 1 / (np.sum(bump) / 10)
        reward += non_empty_columns * 2
        reward -= np.sum(height)
        self.grid_reward = reward

        return self.grid_reward

    def check_lost(self):
        for pos in self.locked_positions:
            x, y = pos
            if y < 0:
                return True
            else:
                return False

    def draw_grid(self):
        self.grid = self.create_grid()
        self.draw_locked_pos()
        self.draw_object()

    def step(self, action):
        move = 0
        self.reward = 0
        if not self.user:
            if action == 1:
                self.move_object(-1)

            elif action == 2:
                self.move_object(1)

            elif action == 3:
                self.move_object(0)
                if self.check_object_lock():
                    self.current_object = self.get_object()
                else:
                    self.move_object(0)

            elif action == 0:
                old_position = self.current_object.current_position

                self.current_object.rotation += 1
                if not self.possible_move(0):
                    self.reward -= 10
                    self.current_object.current_position = old_position
                self.move_object(0)

        added_locked = False

        if self.user:
            flag = True
            while flag:
                for event in pygame.event.get():

                    if event.type == pygame.KEYDOWN:
                        event.key == pygame.K_DOWN
                        if event.key == pygame.K_LEFT:
                            self.move_object(-1)
                            move = 1
                            flag = False

                        elif event.key == pygame.K_RIGHT:
                            self.move_object(1)
                            move = 2
                            flag = False

                        elif event.key == pygame.K_DOWN:

                            self.move_object(0)
                            move = 3
                            if self.check_object_lock():
                                added_locked = True
                                self.current_object = self.get_object()
                            else:
                                self.move_object(0)
                            flag = False

                        elif event.key == pygame.K_UP:
                            old_position = self.current_object.current_position

                            self.current_object.rotation += 1
                            if not self.possible_move(0):
                                self.reward -= 2
                                self.current_object.current_position = old_position
                            self.move_object(0)
                            flag = False

        self.iter += 1
        self.draw_grid()

        if self.check_object_lock():

            self.current_object = self.get_object()
            added_locked = True

        for y, _ in self.locked_positions:
            if y < 0:
                self.reward -= 10
                self.done = True
                self.iter = 0
        info = {}

        self.reward += self.clear_row()

        if self.done == True:
            self.reset()

        if added_locked:
            self.reward += self.reward_fun()

        return self.grid, move, self.done, info

    def render(self, mode=None):
        print(self.reward)
        print(self.grid)


if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((70, 70))
    env = Game(user=True)
    model = keras.models.load_model('model.h5')
    state = env.reset()
    step = model.predict(np.array([state]))
    done = False
    while not done:
        grid, move, done, info  = env.step(step)
        step = model.predict(np.array([state]))
    
  