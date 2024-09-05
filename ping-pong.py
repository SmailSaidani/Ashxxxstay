from random import *
from pygame import *
print("Hail to the king")
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
        if keys[K_UP] and self.rect.x > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.x < win_width - 80:
            self.rect.y += self.speed

    def update1(self):
        keys = key.get_pressed()
        if keys[K_s] and self.rect.x > 5:
            self.rect.y -= self.speed
        if keys[K_w] and self.rect.x < win_width - 80:
            self.rect.y += self.speed

back = (200, 255, 255)  # background color (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

# flags responsible for game state
game = True
finish = False
clock = time.Clock()
FPS = 60

# creating ball and paddles
racket1 = Player('racket.png', 30, 200, 50, 50, 150)
racket2 = Player('racket.png', 520, 200, 50, 50, 150)
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)

speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.fill(back)
        racket1.update1()
        racket2.update()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
        # if the ball reaches screen edges, change its movement direction
        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1
        # if ball flies behind this paddle, display loss condition for player 1
        
        racket1.reset()
