from settings import *
import pygame
from os import path
import random
from assets import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(title)
clock = pygame.time.Clock()
score = 0
background_img = pygame.image.load('background.png').convert()
background_rect = background_img.get_rect()

font_name = pygame.font.match_font('arial')
player_new_img = pygame.image.load(path.join(img_dir, '???.png')).convert()


def draw_scoreboard(surf, x, y, text, size):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def new_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_new_img, (80, 60))
        self.image.set_colorkey(white)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 50
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullet_sprites.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(blues)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_x = random.randrange(-3, 8)
        self.speed_y = random.randrange(3, 8)
        self.score_hint = abs(self.speed_x * self.speed_y)

    def update(self, *args):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.left >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.right <= 0:
            self.speed_x = -self.speed_x


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 25))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10

    def update(self, *args):
        self.rect.y += self.speed
        # kill if it moves off the screen
        if self.rect.bottom < 0:

            self.kill()


# sprite Groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()


player = Player()
all_sprites.add(player)
player_sprites.add(player)

for i in range(8):
    new_enemy()

running = True

# Game loop
while running:
    clock.tick(fps)
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    all_sprites.update()
    # check to see if bullet hit the Enemy
    damage = pygame.sprite.groupcollide(enemy_sprites, bullet_sprites, True, True)
    for each_hit in damage:
        if each_hit:
            new_enemy()
        if each_hit:
            score += Enemy().score_hint

    # check to see if mob hit the player
    hits = pygame.sprite.spritecollide(player, enemy_sprites, False)
    for hit in hits:
        if hit:

            running = False

    # Draw / render
    screen.fill(black)
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    draw_scoreboard(screen, WIDTH/2, 10, str(score), 15)

    # After drawing everything
    pygame.display.flip()

pygame.quit()


















