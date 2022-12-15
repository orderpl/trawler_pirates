import pygame, sys, random, math
from pygame.locals import *
from pygame.math import Vector2

pygame.init()
screen = pygame.display.set_mode((0,0))
res = pygame.display.get_window_size()
clock = pygame.time.Clock()

def degrees(x):
    return x * 180 / math.pi

def radians(x):
    return x * math.pi / 180

def write(text, x, y, font=pygame.font.SysFont("Arial", 20), color=(255, 255, 255)):
    screen.blit(font.render(str(text), 1, color), (x, y))

class WindArrow(object):
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.pos.x = res[0] - 250
        self.pos.y = res[1] - 250

        self.angle = 0

        self.image = pygame.image.load("wind_arrow.png")

    def draw(self):
        imgrot = pygame.transform.rotate(self.image, self.angle)
        img = pygame.transform.scale(imgrot, Vector2(imgrot.get_rect().width, imgrot.get_rect().height) * 3)
        imgrect = img.get_rect()
        imgrect.center = self.pos
        screen.blit(img, imgrect)

    def update(self):
        self.angle = degrees((windAngle + radians(self.angle) * 4) / 5)

class Player(object):
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.sizes = Vector2(20, 50)
        self.speed = 0.25
        self.image = pygame.image.load("ship.png")

    def updateRect(self, image):
        self.rect = image.get_rect()
        self.rect.center = Vector2(res[0] / 2, res[1] / 2)

    def update(self):
        keys = pygame.key.get_pressed()

        speed = self.speed + (self.acc.x + self.acc.y) / 5
        if keys[K_w]:
            self.addForce(Vector2(0, -speed))
        if keys[K_s]:
            self.addForce(Vector2(0, speed))
        if keys[K_a]:
            self.addForce(Vector2(-speed, 0))
        if keys[K_d]:
            self.addForce(Vector2(speed, 0))

        self.addForce(current)

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        self.vel *= 0.925

    def draw(self):
        image = pygame.transform.rotate(pygame.transform.scale(self.image, (self.image.get_rect().width, self.image.get_rect().height)), self.vel.angle_to(Vector2(0, -1)))
        self.updateRect(image)
        # pygame.draw.rect(screen, (255, 120, 120), self.rect)
        screen.blit(image, self.rect)

    def addForce(self, force):
        self.acc += force

player = Player()

windArrow = WindArrow()

windAngle = random.random() * 2 * math.pi
wind = Vector2(0, 0)
windPower = random.random() / 15
current = Vector2(0, 0)

cam = player.pos

tick = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        
    # updating
    player.update()

    if tick % 60 == 0:
        if random.random() < 0.01:
            windAngle += random.randint(-5, 5)
        else:
            windAngle += random.randint(-1, 1) / 3
        
        windAngle = abs(windAngle % (2 * math.pi)) # making sure that theese are user friendly

        wind.x = math.sin(windAngle)
        wind.y = math.cos(windAngle)

        windPower = random.random() / 15
        wind *= windPower

        windArrow.update()

    current = (current * 9 + wind) / 10 # wind affecting current

    cam = player.pos

    # drawing
    player.draw()
    windArrow.draw()

    pygame.display.update()
    screen.fill((40, 80, 160))
    clock.tick(60)
    tick += 1