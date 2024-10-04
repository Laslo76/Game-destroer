import pygame
import random
from os import path

snd_dir = path.join(path.dirname(__file__), 'snd')
img_dir = path.join(path.dirname(__file__), 'img')
hiscore_file = path.join(path.dirname(__file__), "hiscore")

WIDTH = 480
HEIGHT = 600
FPS = 60
LEVEL = 1000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("THE STAR DESTROYER")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x: int, y: int):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_health_bar(surf, x: int, y: int, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = int((pct / 100) * bar_length)
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img_obj):
    for iterator in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * iterator
        img_rect.y = y
        surf.blit(img_obj, img_rect)


def new_mob(count=1):
    while count > 0:
        asteroid = Mob()
        all_sprites.add(asteroid)
        mobs.add(asteroid)
        count -= 1


def gethiscore():
    if path.exists(hiscore_file):
        file_top_score = open(hiscore_file)
        lscore = int(file_top_score.readline())
        file_top_score.close()
    else:
        lscore = 0
    return lscore


def show_go_screen():
    pygame.event.clear()
    screen.blit(background, background_rect)
    draw_text(screen, "Ш Е Л Д О Р", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "<- Движение ->, Пробел - огонь!", 22,
              WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Нажминте Пробел для начала", 18, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for key_event in pygame.event.get():
            if key_event.type == pygame.QUIT:
                pygame.quit()
            if key_event.type == pygame.KEYDOWN:
                press_key = key_event.key
                if press_key == pygame.K_SPACE:
                    return True
                if press_key == pygame.K_ESCAPE:
                    return False


def clear_group(group_sprite):
    for item in group_sprite:
        item.kill()


def clear_all_groups(tuple_group):
    for item in tuple_group:
        clear_group(item)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 1
        self.health = 100
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.rule = {pygame.K_LEFT: -8, pygame.K_RIGHT: 8}

    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed_x = -8
        elif key_state[pygame.K_RIGHT]:
            self.speed_x = 8
        else:
            self.speed_x = 0

        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Surprice(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = surprice_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .8)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-10, 10)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir, "playerShip2_blue.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
meteor_images = [pygame.image.load(path.join(img_dir, img)).convert() for img in meteor_list]
bullet_img = pygame.image.load(path.join(img_dir, "laserRed01.png")).convert()
surprice_img = pygame.image.load(path.join(img_dir, "powerupYellow_star.png")).convert()


explosion_anim = {'lg': [], 'sm': []}
for i in range(9):
    filename = f"regularExplosion0{i}.png"
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = [pygame.mixer.Sound(path.join(snd_dir, snd)) for snd in ['expl3.wav', 'expl6.wav']]

pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.5)

player = Player()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
prices = pygame.sprite.Group()

hiscore = gethiscore()
score = 0

game_over, running = True, True

while running:
    if game_over:
        running = show_go_screen()
        if not running:
            continue
        game_over = False
        hiscore = gethiscore()
        score = 0

        clear_all_groups((all_sprites, mobs, bullets, prices))

        pygame.mixer.music.play(loops=-1)

        all_sprites.add(player)
        new_mob(8)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                game_over = True
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += 5 * ((50 - hit.radius) // 10)
        if score > LEVEL:
            price = Surprice()
            all_sprites.add(price)
            prices.add(price)
            new_mob()
            LEVEL += 1000

        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        new_mob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        random.choice(expl_sounds).play()
        player.health -= hit.radius

        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

        new_mob()
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            if player.lives < 1:
                game_over = True
                if hiscore < score:
                    f = open(hiscore_file, 'w')
                    f.writelines(str(score))
                    f.close()

    hits = pygame.sprite.spritecollide(player, prices, True, pygame.sprite.collide_circle)
    for hit in hits:
        if player.health == 100:
            if player.lives < 3:
                player.lives += 1
        player.health = 100

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH // 2, 10)
    draw_text(screen, 'HI SCORE: ' + str(hiscore), 18, WIDTH - 80, 10)
    draw_health_bar(screen, 10, 10, player.health)
    draw_lives(screen, 120, 10, player.lives, player_mini_img)
    pygame.display.flip()

pygame.quit()
