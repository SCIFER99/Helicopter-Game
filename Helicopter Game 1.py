# By: Tim Tarver
# Helicopter Game

import pygame
import random
import os

pygame.init()

screen_width = 600
screen_height = 400
gap = int(screen_height / 2)
start_gravity = 0.1


class Actor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.graphics = pygame.image.load(os.path.join('actor.gif'))

    def draw(self):
        screen.blit(self.graphics, (self.x, self.y))

    def move(self, v):
        self.y = self.y + v
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)


class Obstacle:
    def __init__(self, x, obstacle_width):
        self.x = x
        self.obstacle_width = obstacle_width
        self.y_upper = 0
        self.y_upper_height = random.randint(screen_height // 4, screen_height // 2)
        self.obstacle_gap = gap
        # yLower = 100+200=300
        # yLowerHeight = 400-300=100
        self.y_lower = self.y_upper_height + self.obstacle_gap
        self.y_lower_height = screen_height - self.y_lower
        self.color = (0, 255, 0)
        self.shape_upper = pygame.Rect(self.x, self.y_upper, self.obstacle_width, self.y_upper_height)
        self.shape_lower = pygame.Rect(self.x, self.y_lower, self.obstacle_width, self.y_lower_height)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.shape_upper, 0)
        pygame.draw.rect(screen, self.color, self.shape_lower, 0)

    def move(self, v):
        self.x = self.x - v
        self.shape_upper = pygame.Rect(self.x, self.y_upper, self.obstacle_width, self.y_upper_height)
        self.shape_lower = pygame.Rect(self.x, self.y_lower, self.obstacle_width, self.y_lower_height)

    def crash(self, player_rect):
        if self.shape_upper.colliderect(player_rect) or self.shape_lower.colliderect(player_rect):
            return True
        else:
            return False


screen = pygame.display.set_mode((screen_width, screen_height))


def write(text, x, y, size):
    writing_font = pygame.font.SysFont("Arial", size)
    rend = writing_font.render(text, True, (255, 100, 100))
    screen.blit(rend, (x, y))


def write_in_middle(text, size):
    writing_font = pygame.font.SysFont("Arial", size)
    rend = writing_font.render(text, True, (255, 100, 100))
    x = (screen_width - rend.get_rect().width) / 2
    y = (screen_height - rend.get_rect().height) / 2
    screen.blit(rend, (x, y))


active_screen = "menu"
dy = start_gravity
obstacles = []

for i in range(21):
    obstacles.append(Obstacle(i * screen_width / 20, screen_width / 20))

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = dy - 0.2
            if event.key == pygame.K_DOWN:
                dy = dy + 0.2
            if event.key == pygame.K_SPACE:
                if active_screen != "play":
                    player = Actor(screen_width / 2, gap / 2 + screen_height / 3)
                    dy = start_gravity
                    active_screen = "play"
                    points = 0

    if active_screen == "menu":
        write("HELICOPTER", 20, 20, 50)
        write_in_middle("Press space bar to start...", 25)
        logo = pygame.image.load(os.path.join('actor.gif'))
        screen.blit(logo, (400, 40))

    elif active_screen == "end":
        write("HELICOPTER", 20, 20, 50)
        write("You have crashed! Your result: " + str(points), 20, 100, 25)
        write_in_middle("Press space bar to start again...", 25)
        logo = pygame.image.load(os.path.join('actor.gif'))
        screen.blit(logo, (400, 40))

    elif active_screen == "play":
        for p in obstacles:
            p.move(1)
            p.draw()
            if p.crash(player.shape):
                active_screen = "end"
        for p in obstacles:
            if p.x <= -p.obstacle_width:
                obstacles.remove(p)
                obstacles.append(Obstacle(screen_width, screen_width / 20))
                points = points + 1
        player.draw()
        player.move(dy)
        write("P: " + str(points), screen_width - 100, screen_height - 30, 20)

    pygame.display.update()
