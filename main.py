from settings import *
import pygame
from os import path
import random
from assets import *
from highscore import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(title)
clock = pygame.time.Clock()
score = 0
background_img = pygame.image.load('background.png').convert()
background_rect = background_img.get_rect()

font_name = pygame.font.match_font('arial')
player_new_img = pygame.image.load(path.join(img_dir, 'playerShip1_red.png')).convert()
enemies = []
# enemy sprite randomize
for i in all_enemies:
    enemy_img = pygame.image.load(path.join(enemy_dir, i)).convert()
    enemies.append(enemy_img)
# laser sprite randomize
lasers = []
for laser in all_lasers:
    las = pygame.image.load(path.join(laser_dir, laser)).convert()
    lasers.append(las)

# sound section
pygame.mixer.music.load(background_sound)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops=-1)
# laser sound randomize
las_sound = []
for sound in all_laser_sounds:
    snd = pygame.mixer.Sound(path.join(shoot_dir, sound))
    las_sound.append(snd)


def draw_scoreboard(surf, x, y, text, size):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface,  text_rect)


def new_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_new_img, (40, 40))

        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 42
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
        self.image = pygame.transform.scale(random.choice(enemies), (30, 30))
        self.image.set_colorkey(black)
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
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(lasers), (10, 25))

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
                random.choice(las_sound).play()
    # Update
    all_sprites.update()
    # check to  see if bullet hit the Enemy
    damage = pygame.sprite.groupcollide(enemy_sprites, bullet_sprites, True, True)
    for each_hit in damage:
        if each_hit:
            new_enemy()
        if each_hit:
            score += (Enemy().score_hint + 100)

    # check to see if mob hit the player
    hits = pygame.sprite.spritecollide(player, enemy_sprites, False, pygame.sprite.collide_circle)
    for hit in hits:
        if hit:
            high_score(score)
            running = False

    # Draw / render
    screen.fill(black)
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    draw_scoreboard(screen, WIDTH/2, 10, str(score), 15)

    # After drawing everything
    pygame.display.flip()

pygame.quit()




















