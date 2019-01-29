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
bullet_lvl_down_counter = 50000
hide_timer = 5000

life = pygame.image.load(pro).convert()
life.set_colorkey(black)
snde = pygame.mixer.Sound(boss_sound)


def draw_lives(surf, x_pos, y_pos, lives, lives_image):
    for live in range(lives):
        img_rect = lives_image.get_rect()

        img_rect.x = x_pos + 35 * live
        img_rect.y = y_pos
        surf.blit(lives_image, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_len = 100
    bar_height = 10
    fill = (pct / 100) * bar_len
    outline_rect = pygame.Rect(x, y, bar_len, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)


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
# explosion animation
exp = []  # all explosions list
for item in listdir(explosion_dir):
    new_img = pygame.image.load(path.join(explosion_dir, item)).convert()
    exp.append(new_img)
# Power_ups ----
powers = {}

powers['shield'] = pygame.image.load(path.join(power_ups, 'shield.png')).convert()
powers['bullet'] = pygame.image.load(path.join(power_ups, 'bolt.png')).convert()

# sound section ----

# background sound
pygame.mixer.music.load(background_sound)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)
# laser sound randomize
las_sound = []
for sound in all_laser_sounds:
    snd = pygame.mixer.Sound(path.join(shoot_dir, sound))
    las_sound.append(snd)

# critical sound
critical_sound = pygame.mixer.Sound(critical_dir)


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

        self.image = pygame.transform.scale(player_new_img, (40, 40))

        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 42
        self.speed = 8
        self.shield = 100
        self.bullet_level = 1
        self.last_update = pygame.time.get_ticks()
        self.life = 3

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.last_update >= bullet_lvl_down_counter:
            self.last_update = now
            self.bullet_level -= 1
        if self.bullet_level <= 1:
            self.bullet_level = 1
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

        if self.bullet_level == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)

        if self.bullet_level == 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullet_sprites.add(bullet1)
            bullet_sprites.add(bullet2)

        if self.bullet_level >= 3:
            self.bullet_level = 3
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            bullet3 = Bullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            bullet_sprites.add(bullet1)
            bullet_sprites.add(bullet2)
            bullet_sprites.add(bullet3)


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
        if score > 200:
            self.kill()
            boss = Boss()
            all_sprites.add(boss)
            snde.set_volume(0.05)
            snde.play()
            pygame.mixer.music.stop()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(lasers), (10, 25))

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10
        self.bullet_level = 1
        self.last_update = pygame.time.get_ticks()

    def update(self, *args):
        self.rect.y += self.speed
        # kill if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, anim_x, anim_y):
        pygame.sprite.Sprite.__init__(self)

        self.n = 0
        self.image = pygame.transform.scale(exp[self.n], (60, 60))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = anim_x
        self.rect.y = anim_y
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self, *args):

        try:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                self.n += 1
                self.image = pygame.transform.scale(exp[self.n], (60, 60))
                self.image.set_colorkey(black)
            if self.frame == len(exp):
                self.kill()
        except IndexError:
            pass


class PowerUps(pygame.sprite.Sprite):
    def __init__(self, pow_x, pow_y):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'bullet'])
        self.image = pygame.transform.scale(powers[self.type], (30, 30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = pow_x
        self.rect.y = pow_y
        self.speed = random.randint(7, 10)

    def update(self, *args):
        self.rect.y += self.speed


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(boss_dir).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = -150
        self.damage = random.randint(15, 45)
        self.hp = 1000
        self.speed = 5
        self.last_update = pygame.time.get_ticks()

    def update(self, *args):  # Todo Movement algorithm
        self.rect.y += self.speed
        """if self.rect.y > HEIGHT / 2:
            self.speed = 0
            self.rect.x += 5"""
        self.movement()

    def hide(self):
        now = pygame.time.get_ticks()
        if random.random() > 0.99:
            self.rect.x = -100
            self.rect.y = HEIGHT + 500
        if now - self.last_update > hide_timer:
            self.rect.x = WIDTH / 2
            self.rect.y = 120
            self.last_update = now

    def movement(self):
        if self.rect.y > HEIGHT / 2:
            self.speed = 0
            self.rect.x += 5
            bul = Bullet(self.rect.x, self.rect.y)
            all_sprites.add(bul)
            if self.rect.right > WIDTH + 40:
                self.rect.x = -40
            if self.rect.left < -40:
                self.rect.x = WIDTH


# sprite Groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
PowerUp_sprites = pygame.sprite.Group()
if score > 2000:
    print(123)  #

player = Player()
all_sprites.add(player)
player_sprites.add(player)

for i in range(8):
    new_enemy()

running = True

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
        if each_hit:
            explosion = Explosion(each_hit.rect.x, each_hit.rect.y)
            all_sprites.add(explosion)
        if random.randint(1, 2) > 0:
            pow_up = PowerUps(each_hit.rect.x, each_hit.rect.y)
            all_sprites.add(pow_up)
            PowerUp_sprites.add(pow_up)

    # check to see if mob hit the player
    hits = pygame.sprite.spritecollide(player, enemy_sprites, True, pygame.sprite.collide_circle)
    for hit in hits:

        new_enemy()
        high_score(score)
        k = random.randint(10, 25)
        player.shield -= k
        if k > 20:  # if damage > 20 critical sound will play (Phantom assassin Ult)
            critical_sound.play()

        if player.shield <= 0:
            player.life -= 1
            player.shield = 100
    # check to see if powerUp hit the player
    pow_ = pygame.sprite.spritecollide(player, PowerUp_sprites, True)
    for each_power in pow_:
        if each_power.type == 'shield':
            player.shield += random.randint(10, 25)
            if player.shield >= 100:
                player.shield = 100
        if each_power.type == 'bullet':
            player.bullet_level += 1
    # Draw / render
    screen.fill(black)
    screen.blit(background_img, background_rect)
    draw_shield_bar(screen, 10, 10, player.shield)
    all_sprites.draw(screen)
    draw_scoreboard(screen, WIDTH / 2, 10, str(score), 15)
    draw_lives(screen, WIDTH - 123, 15, player.life, pygame.transform.scale(life, (25, 25)))
    # check_score(score)
    # After drawing everything
    pygame.display.flip()

pygame.quit()
