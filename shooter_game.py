#Create your own shooter
from random import *
from pygame import *
font.init()
font2 = font.Font(None, 36)
lost = 0
win = 0

class GameSprite(sprite.Sprite):
    # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire_bullets(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 50, 50, 20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost        
        if self.rect.y > win_height:            
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost +1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Game scene:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("shooter_game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

rocket = Player('rocket.png', 5, win_height - 80, 80, 100, 10)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
boom = mixer.Sound('fire.ogg')

finish = False
game = True
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
winn = font.render('YOU WIN!', True, (255, 215, 0))
loss = font.render('YOU LOSE!', True, (180, 0, 0))  

img_enemy = "ufo.png"
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

img_asteroid = "asteroid.png"
asteroid = sprite.Group()
for i in range(1, 4):
   monster = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   asteroid.add(monster)

bullets = sprite.Group()

no_of_lives = 5
print(no_of_lives) 

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire_bullets()
                boom.play()
    if not finish:
        window.blit(background,(0,0))
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        text_scoree = font2.render("score: " + str(win), 1, (255, 255, 255))
        lives = font2.render("lives: " + str(no_of_lives), 1, (255, 255, 255))

        window.blit(text_lose, (10, 50))
        window.blit(text_scoree, (10, 20))
        window.blit(lives, (10, 80))

        rocket.reset()
        rocket.update()

        monsters.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)

        asteroid.update()
        asteroid.draw(window)
        
        if sprite.spritecollide(rocket, asteroid, False):
            sprite.spritecollide(rocket, asteroid, True)
            no_of_lives = no_of_lives -1
            monster = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroid.add(monster)

        if no_of_lives == 0:
            loss = font.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(loss, (200, 200))
            finish = True  

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for sproote in collides:
            win = win+1      
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)  
        if lost >= 10:
            finish = True
            window.blit(loss, (200, 200))  

        if win >= 10 :
            finish = True 
            window.blit(winn, (200, 200))  
        display.update()
        clock.tick(FPS)