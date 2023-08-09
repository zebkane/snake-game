import math
import random

import pygame

pygame.init()
surface = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

grid_size = 10
grid_width = math.floor(surface.get_width() / grid_size)
grid_height = math.floor(surface.get_height() / grid_size)

keys = [False, False, False, False]

apples = []


def px_to_grid(px):
    return px * grid_size


def draw_grid():
    for i in range(grid_width):
        pygame.draw.line(surface, "white", [grid_size * i, 0], [grid_size * i, surface.get_height()], width=1)

    for i in range(grid_height):
        pygame.draw.line(surface, "white", [0, grid_size * i], [surface.get_height(), grid_size * i], width=1)


class Player:
    def __init__(self, color, pos):
        self.pos = pos
        self.parts = 1
        self.past_pos = [pos]
        self.color = color
        self.direction = 2
        self.move_cooldown = 0
        self.move_cooldown_max = 5

    def check_next_pos(self, vel):
        clone_pos = self.pos.copy()
        clone_pos[0] += vel[0]
        clone_pos[1] += vel[1]

        return clone_pos[0] < 0 or clone_pos[0] > grid_width - 1 or clone_pos[1] < 0 or clone_pos[1] > grid_height - 1

    def add_part(self):
        pos = self.pos.copy()
        self.parts += 1
        self.past_pos.append(pos)

    def change_direction(self):
        if keys[0]:
            self.direction = 0
        if keys[1]:
            self.direction = 1
        if keys[2]:
            self.direction = 2
        if keys[3]:
            self.direction = 3

    def update_past_pos(self):
        pos = self.pos.copy()
        self.past_pos.insert(0, pos)
        self.past_pos.pop()

    def check_apples(self):
        for apple in apples:
            if apple.pos == self.pos:
                self.add_part()
                apples.remove(apple)
                apples.append(Apple("red", [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]))

    def move(self):
        if self.move_cooldown >= self.move_cooldown_max:
            self.move_cooldown = 0
            self.update_past_pos()

            if self.direction == 0:
                if not self.check_next_pos([0, -1]):
                    self.pos[1] -= 1
                else:
                    pygame.quit()
            elif self.direction == 1:
                if not self.check_next_pos([1, 0]):
                    self.pos[0] += 1
                else:
                    pygame.quit()
            elif self.direction == 2:
                if not self.check_next_pos([0, 1]):
                    self.pos[1] += 1
                else:
                    pygame.quit()
            elif self.direction == 3:
                if not self.check_next_pos([-1, 0]):
                    self.pos[0] -= 1
                else:
                    pygame.quit()
        else:
            self.move_cooldown += 1

    def draw(self):
        for i in range(self.parts):
            pygame.draw.rect(surface, self.color,
                             pygame.Rect(px_to_grid(self.past_pos[i][0]), px_to_grid(self.past_pos[i][1]), grid_size,
                                         grid_size))

    def update(self):
        self.check_apples()
        self.change_direction()
        self.move()
        self.draw()


class Apple:
    def __init__(self, color, pos):
        self.pos = pos
        self.color = color

    def draw(self):
        pygame.draw.rect(surface, self.color, pygame.Rect(px_to_grid(self.pos[0]), px_to_grid(self.pos[1]), grid_size, grid_size))

    def update(self):
        self.draw()


player = Player("white", [math.floor(grid_width / 2), 0])


def add_apples():
    for i in range(3):
        apples.append(Apple("red", [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]))


add_apples()


def update_apples():
    for apple in apples:
        apple.update()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys[0] = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys[2] = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                keys[3] = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys[1] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys[0] = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys[2] = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                keys[3] = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys[1] = False

    surface.fill("black")

    update_apples()
    player.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
