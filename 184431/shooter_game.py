from pygame import *
from random import randint

WIN_W = 700
WIN_H = 500
x1 = 200
x2 = 500
x3 = 600
y1 = 370
y2 = 350
FPS = 60
step = 5
step1 = 2
step2 = 10
size = 75
w = 100
h = 100
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
UFOS = 4
font.init()
title_font = font.SysFont('arial', 70)
win = title_font.render('Победа!', True, GREEN)
lost = title_font.render('Поражение', True, RED)

label_font = font.SysFont('arial', 30)
count_txt = label_font.render('Счёт: ', True, WHITE)
missed_txt = label_font.render('Пропущено: ', True, WHITE)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.5)


window = display.set_mode((WIN_W, WIN_H))

clock = time.Clock()

display.set_caption("spaceship")


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            (w, h)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def __init__(self, img, x, y, w, h, speed = step2):
        super().__init__(img, x, y, w, h)
        self.speed = speed
    
    def update(self):
        if self.rect.y <= 0:
            self.kill()
        self.rect.y -= self.speed


class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed = step):
        super().__init__(img, x, y, w, h)
        self.speed = speed
        self.missed = 0
        self.shot = 0 
        self.bullets = sprite.Group()
    
    def update(self, left, right):
        keys_pressed = key.get_pressed()
        if keys_pressed[left] and self.rect.x > 5:
            self.rect.x -= step
        if keys_pressed[right] and self.rect.x < WIN_W - size:
            self.rect.x += step
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + self.rect.width / 2, self.rect.y, 5, 15)
        self.bullets.add(bullet)


class Enemy(Player):
    def __init__(self, img, x, y, w, h, speed = step1):
        super().__init__(img, x, y, w, h)
        self.speed = speed
        self.rect.x = randint(0, 575)
        self.rect.y = randint(0, 40)
    
    def update(self, sprite_player, is_ufo = True):
        if self.rect.y >= WIN_H:
            sprite_player.missed += 1
            self.rect.x = randint(0, 575)
            self.rect.y = randint(0, 40)
        self.rect.y += self.speed


background = GameSprite('galaxy.jpg', 0, 0, WIN_W, WIN_H)

sprite_player = Player('rocket.png', x1, y1, 70, 125)
ufos = sprite.Group()

for i in range(UFOS):
    enemy = Enemy('ufo.png', 0, 0, 90, 60)
    ufos.add(enemy)

finish = False
game = True
while game:
    if not finish:
        background.draw(window)
  
        sprite_player.draw(window)
        sprite_player.update(K_a, K_d)

        sprite_player.bullets.draw(window)
        sprite_player.bullets.update()

        ufos.draw(window)
        ufos.update(sprite_player)

        if sprite.spritecollide(sprite_player, ufos, False):
            window.blit(lost, (200, 200))
            display.update()
            finish = True

        if sprite.groupcollide(ufos, sprite_player.bullets, True, True):
            sprite_player.shot += 1   
            enemy = Enemy('ufo.png', 0, 0, 90, 60)
            ufos.add(enemy)
            if sprite_player.shot >= 20:
                window.blit(win, (200, 200))
                finish = True
        if sprite_player.missed >= 3:
            window.blit(lost, (200, 200))                            
            finish = True
        
        count = label_font.render(str(sprite_player.shot), True, WHITE)
        missed = label_font.render(str(sprite_player.missed), True, WHITE)

        window.blit(count_txt, (10, 10))        
        window.blit(count, (80, 10))
        window.blit(missed_txt, (10, 50))
        window.blit(missed, (160, 50))     

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                sprite_player.fire()
    display.update()
    clock.tick(FPS)