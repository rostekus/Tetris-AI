import pygame
import random
import config

pygame.font.init()


# TODO
# quit button
# scorea save to file
# add background


class Object(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = config.shape_colors[config.shapes.index(shape)]
        self.rotation = 0


class Game:
    def __init__(self):
        self.s_width = config.s_width
        self.s_height = config.s_height
        self.play_width = config.play_width
        self.play_height = config.play_height
        self.block_size = config.block_size
        self.shapes = config.shapes

        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = self.s_height - self.play_height

    def create_grid(self, locked_pos={}):  # *
        grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j, i)]
                    grid[i][j] = c
        return grid

    def convert_shape_format(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, shape, grid):
        accepted_pos = [
            [(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)
        ]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True

        return False

    def get_shape(self):
        return Object(5, 0, random.choice(self.shapes))

    def draw_text_middle(self, surface, text, size, color):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        surface.blit(
            label,
            (
                self.top_left_x + self.play_width / 2 - (label.get_width() / 2),
                self.top_left_y + self.play_height / 2 - label.get_height() / 2,
            ),
        )

    def draw_grid(self, surface, grid):
        sx = self.top_left_x
        sy = self.top_left_y

        for i in range(len(grid)):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (sx, sy + i * self.block_size),
                (sx + self.play_width, sy + i * self.block_size),
            )
            for j in range(len(grid[i])):
                pygame.draw.line(
                    surface,
                    (128, 128, 128),
                    (sx + j * self.block_size, sy),
                    (sx + j * self.block_size, sy + self.play_height),
                )

    def clear_rows(self, grid, locked):

        inc = 0
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue

        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

        return inc

    def draw_next_shape(self, shape, surface):
        font = pygame.font.SysFont("comicsans", 30)
        label = font.render("Next Shape", 1, (255, 255, 255))

        sx = self.top_left_x + self.play_width + 50
        sy = self.top_left_y + self.play_height / 2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    pygame.draw.rect(
                        surface,
                        shape.color,
                        (
                            sx + j * self.block_size,
                            sy + i * self.block_size,
                            self.block_size,
                            self.block_size,
                        ),
                        0,
                    )

        surface.blit(label, (sx + 10, sy - 30))

    def update_score(self, nscore):
        score = self.max_score()

        # with open('scores.txt', 'w') as f:
        #     if int(score) > nscore:
        #         f.write(str(score))
        #     else:
        #         f.write(str(nscore))

    def max_score(self):
        # with open('scores.txt', 'r') as f:
        #     lines = f.readlines()
        #     score = lines[0].strip()
        score = 0
        return score

    def draw_window(self, surface, grid, score=0, last_score=0):
        surface.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        label = font.render("Tetris", 1, (255, 255, 255))

        surface.blit(
            label, (self.top_left_x + self.play_width / 2 - (label.get_width() / 2), 30)
        )

        # current score
        font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        label = font.render("Score: " + str(score), 1, (255, 255, 255))

        sx = self.top_left_x + self.play_width + 50
        sy = self.top_left_y + self.play_height / 2 - 100

        surface.blit(label, (sx + 20, sy + 160))
        # last score
        # label = font.render('High Score: ' + last_score, 1, (255,255,255))

        sx = self.top_left_x - 200
        sy = self.top_left_y + 200

        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(
                    surface,
                    grid[i][j],
                    (
                        self.top_left_x + j * self.block_size,
                        self.top_left_y + i * self.block_size,
                        self.block_size,
                        self.block_size,
                    ),
                    0,
                )

        pygame.draw.rect(
            surface,
            (255, 0, 0),
            (self.top_left_x, self.top_left_y, self.play_width, self.play_height),
            5,
        )

        self.draw_grid(surface, grid)

    def play(self, win):  # *
        last_score = self.max_score()
        locked_positions = {}
        grid = self.create_grid(locked_positions)

        change_Object = False
        run = True
        current_Object = self.get_shape()
        next_Object = self.get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        level_time = 0
        score = 0

        while run:
            grid = self.create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
            clock.tick()

            if level_time / 1000 > 5:
                level_time = 0
                if level_time > 0.12:
                    level_time -= 0.005

            if fall_time / 1000 > fall_speed:
                fall_time = 0
                current_Object.y += 1
                if (
                    not (self.valid_space(current_Object, grid))
                    and current_Object.y > 0
                ):
                    current_Object.y -= 1
                    change_Object = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_Object.x -= 1
                        if not (self.valid_space(current_Object, grid)):
                            current_Object.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_Object.x += 1
                        if not (self.valid_space(current_Object, grid)):
                            current_Object.x -= 1
                    if event.key == pygame.K_DOWN:
                        current_Object.y += 1
                        if not (self.valid_space(current_Object, grid)):
                            current_Object.y -= 1
                    if event.key == pygame.K_UP:
                        current_Object.rotation += 1
                        if not (self.valid_space(current_Object, grid)):
                            current_Object.rotation -= 1

            shape_pos = self.convert_shape_format(current_Object)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_Object.color

            if change_Object:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_Object.color
                current_Object = next_Object
                next_Object = self.get_shape()
                change_Object = False
                score += self.clear_rows(grid, locked_positions) * 10

            self.draw_window(win, grid, score, last_score)
            self.draw_next_shape(next_Object, win)
            pygame.display.update()

            if self.check_lost(locked_positions):
                self.draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
                pygame.display.update()
                pygame.time.delay(1500)
                run = False
                self.update_score(score)

    def main_menu(self, win):
        run = True
        while run:
            win.fill((0, 0, 0))
            self.draw_text_middle(win, "Press Any Key To Play", 60, (255, 255, 255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    self.play(win)

        pygame.display.quit()


if __name__ == "__main__":
    game = Game()
    win = pygame.display.set_mode((config.s_width, config.s_height))
    pygame.display.set_caption("Tetris")
    game.main_menu(win)
