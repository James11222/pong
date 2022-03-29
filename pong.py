import pygame
from pygame.locals import *
import random, math, sys

pygame.init()
#initialize and create some variables
width, height = 800, 500
Surface = pygame.display.set_mode((800,500))
pygame.display.set_caption("Pong")
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0,255,255)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def len(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
    def __rmul__(self, other):
        return Vector(self.x * other, self.y * other)
    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)
    def angle(self):
        return math.atan2(self.y, self.x)
    def norm(self):
        if self.x == 0 and self.y == 0:
            return Vector(0, 0)
        return self / self.len()
    def dot(self, other):
        return self.x*other.x + self.y*other.y

class Paddle:
    def __init__(self,x,y):
        self.position = Vector(x, y - 30)
        self.velocity = Vector(0, 0)
        self.width = 20
        self.height = 100

class Ball:
    def __init__(self,x,y):
        self.radius = 10
        self.color = white
        self.position = Vector(x,y)
        self.velocity = Vector(0,0)


def GetInput(ball, Paddles):
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keystate[pygame.K_ESCAPE]:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Paddles[1].velocity.y = -2
            elif event.key == pygame.K_DOWN:
                Paddles[1].velocity.y = 2
            elif event.key == pygame.K_SPACE:
                ball.velocity.x = random.randrange(-2,2)
                ball.velocity.y = random.randrange(-2,2)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                Paddles[1].velocity.y = 0
            elif event.key == pygame.K_DOWN:
                Paddles[1].velocity.y = 0


def Collision(score_c, score_p, ball, Paddles):
    difficulty_factor = (score_p - score_c) / 200
    if ball.position.y < ball.radius and ball.velocity.y < 0:
        ball.velocity.y *= -1.02 + difficulty_factor
    if ball.position.y > height-ball.radius and ball.velocity.y > 0:
        ball.velocity.y *= -1.02 + difficulty_factor
    if ball.position.x < Paddles[0].position.x + Paddles[0].width + ball.radius/2 and ball.velocity.x < 0:
        if ball.position.y > Paddles[0].position.y and ball.position.y < Paddles[0].position.y + Paddles[0].height:
            ball.velocity.x *= -1.02 + difficulty_factor
    if ball.position.x > Paddles[1].position.x - Paddles[1].width + ball.radius/2 and ball.velocity.x > 0:
        if ball.position.y > Paddles[1].position.y and ball.position.y < Paddles[1].position.y + Paddles[1].height:
            ball.velocity.x *= -1.02 + difficulty_factor


def Move(score_c, score_p, ball, Paddles):
    for pad in Paddles:
        pad.position = pad.position + pad.velocity
    ball.position = ball.position + ball.velocity

    difficulty_factor = (score_p - score_c) / 100
    Paddles[0].velocity.y = ball.velocity.y * (0.90 + difficulty_factor)

def Draw(score_c, score_p, ball, Paddles):
    clock = pygame.time.Clock()
    Surface.fill(black)
    pygame.draw.rect(Surface, red, [Paddles[1].position.x,Paddles[1].position.y,Paddles[1].width, Paddles[1].height])
    pygame.draw.rect(Surface, blue, [Paddles[0].position.x,Paddles[0].position.y,Paddles[0].width, Paddles[0].height])
    pygame.draw.circle(Surface,ball.color,(int(ball.position.x),int(ball.position.y)),ball.radius)
    font = pygame.font.Font('batmfa__.ttf', 18)
    text = font.render('Computer: {0:1.0f}'.format(score_c), True, blue,black)
    textRect = text.get_rect()
    textRect.center = (210,25)
    Surface.blit(text, textRect)
    font2 = pygame.font.Font('batmfa__.ttf', 18)
    text2 = font.render('Player: {0:1.0f}'.format(score_p), True, red,black)
    textRect2 = text2.get_rect()
    textRect2.center = (590,25)
    Surface.blit(text2, textRect2)
    pygame.display.flip()

def score(score_c, score_p, ball, Paddles):
    if ball.position.x < Paddles[0].position.x:
        score_p += 1
        ball.position.x = 400
        ball.position.y = 250
        Paddles[0].position.y = 220
        Paddles[1].position.y = 220
        ball.velocity = Vector(0,0)
    elif ball.position.x > Paddles[1].position.x:
        score_c += 1
        ball.position.x = 400
        ball.position.y = 250
        Paddles[0].position.y = 220
        Paddles[1].position.y = 220
        ball.velocity = Vector(0,0)

    return score_c, score_p

def main():
    ball = Ball(400,250)
    R_Paddle = Paddle(750, 250)
    L_Paddle = Paddle(50, 250)
    paddles = [L_Paddle, R_Paddle]
    score_c, score_p = 0,0
    while True:
        GetInput(ball, paddles)
        Move(score_c, score_p, ball, paddles)
        Collision(score_c, score_p, ball, paddles)
        score_c, score_p = score(score_c, score_p, ball, paddles)
        Draw(score_c, score_p, ball, paddles)
        if score_c > 10 or score_p > 10:
            if score_c > 10:
                print("The computer beat you!")
            elif score_p > 10:
                print("Good Job you beat the computer!")
            exit()

        


if __name__ == '__main__':
    main()
