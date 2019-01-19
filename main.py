from settings import *
import pygame
import os
import random

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(title)
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 30
        self.speed = 8

    def update(self, *args):
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_RIGHT]:
            self.rect.x += 8
        if key_press[pygame.K_LEFT]:
            self.rect.x -= 8
        if self.rect.right > WIDTH + 40:
            self.rect.x = -40
        if self.rect.left < -40:
            self.rect.x = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(blues)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_x = random.randrange(-5, 10)
        self.speed_y = random.randrange(3, 12)

    def update(self, *args):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.left >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.right <= 0:
            self.speed_x = -self.speed_x
        if self.rect.top > HEIGHT:
            self.kill()


# sprite Groups
all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player = Player()
enemy = Enemy()
all_sprites.add(player)
player_sprites.add(player)
all_sprites.add(enemy)
enemy_sprites.add(enemy)

running = True

# Game loop
while running:
    clock.tick(fps)
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(black)
    all_sprites.draw(screen)

    # After drawing everything
    pygame.display.flip()

pygame.quit()


