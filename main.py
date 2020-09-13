import pygame
from pygame import mixer
import time
import numpy as np
import random

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('City Cycling')
icon = pygame.image.load('visuals/bicycle.png')
pygame.display.set_icon(icon)

fps, direction, ground, dir2, jumping = 120, 'right', 402, 'up', 'no'
count, car_pos, life_status, level = 0, 'ground', 'alive', 1

obsimg = pygame.image.load('visuals/barrier.png')
background = pygame.image.load('visuals/bk.png')
car1img = pygame.image.load('visuals/cycling.png')
car2img = pygame.image.load('visuals/cycling2.png')
blastimg = pygame.image.load('visuals/blast.png')
coneimg = pygame.image.load('visuals/cone.png')
helicopterimg = pygame.image.load('visuals/helicopter.png')
bulletimg = pygame.image.load('visuals/bomb.png')
helicopterimg2 = pygame.image.load('visuals/helicopter2.png')
heartimg = pygame.image.load('visuals/heart.png')
goalimg = pygame.image.load('visuals/goal.png')

death_sound = mixer.Sound('audio/lose.wav')
mixer.music.load('audio/bgm.wav')
mixer.music.play(-1)

font = pygame.font.Font('freesansbold.ttf', 24)

clock = pygame.time.Clock()
goal_x, bike_x, bike_y, bike_x_change, cary_change = 11000, 200, ground, 0, 0
bk_x, bk_y, bk_change, obstacle_y, count11, cone_y = 0, -100, 9, 402, 0, 434
heli_x, heli_y, dir4, bul_x, bul_y = 100, 100, 'right', 124, 124
fire, bul_change, life = False, 5, 5
life_list = np.array([0, 35, 70, 105, 140])


def dothis():
    global X, X2
    X = np.array([800, 955, 1110, 1265, 1420, 1575, 2575, 2730, 2885,
                  3040, 3195, 3350, 4350, 4505, 4660, 4815, 4970, 5125,
                  6125, 6280, 6435, 6590, 6745, 6900, 7900, 8055, 8210,
                  8365, 8520, 8675, 8830, 9830, 9985, 10140, 10295,
                  10450, 10605])
    X2 = np.arange(X.size * 3).reshape(X.size, 3)
    count9 = 0
    for _ in range(X.size):
        X2[count9][0] = X[count9] + 65
        X2[count9][1] = X2[count9][0] + 25
        X2[count9][2] = X2[count9][0] + 50
        count9 += 1


dothis()


def lifes():
    global life, life_list, life_status, bike_x, level
    global heli_y, bk_x, bul_x, bul_y, X, X2, goal_x, heli_x
    if life > 0:
        for i in life_list:
            heart(i, 0)
        if life_status == 'dead':
            screen.blit(blastimg, (bike_x, bike_y))
            life_list = np.delete(life_list, -1)
            death_sound.play()
            bike_x, bk_x, heli_y, heli_x = 150, 0, 100, 100
            bul_x, goal_x, bul_y = -100, 11000, 124
            dothis()
            life_status = 'alive'
            life -= 1
    elif life <= 0:
        time.sleep(1)
        life = 5
        life_list = np.array([0, 35, 70, 105, 140])
        if level > 1:
            level = 1


def scoreboard(x, y):
    screen.blit(font.render(f'level : {level}', True, (255, 255, 255)), (x, y))


def cone(x, y):
    screen.blit(coneimg, (x, y))


def car1(x, y):
    screen.blit(car1img, (x, y))


def car2(x, y):
    screen.blit(car2img, (x, y))


def heart(x, y):
    screen.blit(heartimg, (x, y))


def obstacle(x, y):
    screen.blit(obsimg, (x, y))


def heli1(x, y):
    screen.blit(helicopterimg, (x, y))


def heli2(x, y):
    screen.blit(helicopterimg2, (x, y))


def bullet(x, y):
    screen.blit(bulletimg, (x, y))


def goal(x, y):
    screen.blit(goalimg, (x, y))


def jump():
    global dir2, bike_y, jumping, count, car_pos, ground
    if dir2 == 'up':
        count += 1
        bike_y -= 50
    if count == 15:
        dir2 = 'down'
    if bike_y >= ground - 3:
        count = 0
        dir2 = 'up'
        jumping = 'no'


def car_motion():
    global bike_x, X, bk_x, bul_x, goal_x, sc_x
    if bike_x <= 0:
        bike_x = 0
    if bike_x >= 420:
        bike_x = 420
        bk_x -= bk_change
        goal_x -= bk_change
        for count5 in range(0, len(X)):
            X[count5] -= bk_change
        count7 = 0
        while count7 < len(X2):
            for count6 in range(0, len(X2[count7])):
                X2[count7][count6] -= bk_change
            count7 += 1


def obstaclecol(x, y):
    global ground, bike_x, bike_y, car_pos
    if bike_x >= x - 64 and bike_x <= x - 50 and bike_y > 350:
        bike_x = x - 64
    if bike_x > x + 50 and bike_x <= x + 64 and bike_y > 350:
        bike_x = x + 64
    if bike_x >= x - 60 and bike_x <= x + 60:
        ground = 350
        car_pos = 'obstacle'
    else:
        car_pos = 'ground'
    if ground >= 402:
        car_pos = 'ground'


def conecol(x, y):
    global bike_x, bike_y, life_status
    if bike_x >= x - 50 and bike_x <= x + 20 and not bike_y < 402:
        life_status = 'dead'


def heli_movement():
    global heli_x, heli_y, dir4, bul_x, fire
    heli_change = 5
    if heli_x > bike_x + 330:
        dir4 = 'left'
        fire = True
    if heli_x < bike_x - 150:
        dir4 = 'right'
        fire = True
    if dir4 == 'right':
        heli_x += heli_change
        bul_x += bul_change
        bullet(bul_x, bul_y)
        heli1(heli_x, heli_y)
    if dir4 == 'left':
        heli_x -= heli_change
        bul_x -= bul_change
        bullet(bul_x, bul_y)
        heli2(heli_x, heli_y)


def bullet_fire():
    global count11, bul_y, fire, bul_change, bul_x
    ran = random.randint(int(bike_x), int(bike_x + 30))
    if heli_x >= ran:
        fire = True
    if fire:
        bul_y += 4 + level
        bul_x -= 4
        bul_change = 0
    else:
        bul_change = 5
    if bul_y >= 460:
        screen.blit(blastimg, (bul_x, 430))
        bul_x = heli_x
        bul_y = 124


def collision():
    global life_status
    if (bul_x > bike_x and bul_x + 24 < bike_x + 60 and
            bul_y in range(bike_y, bike_y + 50)):
        screen.blit(blastimg, (bike_x, bike_y))
        life_status = 'dead'


def main():
    global count11, bul_x, bk_x, bike_x, bike_y, ground, X, X2, fire
    global goal_x, level, bul_y, heli_x, heli_y, life_status
    bike_x += bike_x_change
    bike_y += 44
    count11 += 1
    if jumping == 'yes':
        jump()
    elif jumping == 'no':
        bike_y = ground
    if car_pos == 'ground':
        ground = 402
    if bk_x > 0:
        bk_x = 0
    if bk_x < -10800:
        heli_x, heli_y = 100, 100
        time.sleep(1)
        level += 1
        bk_x, bike_x, goal_x, bul_x, bul_y = 1, 200, 11000, 124, 124
        dothis()
        life_status = 'alive'
    if bike_x > 600:
        bike_x = 600
    if bike_x < 0:
        bike_x = 0
    goal(goal_x, 402)
    scoreboard(700, 10)
    if direction == 'right':
        car1(bike_x, bike_y)
    elif direction == 'left':
        car2(bike_x, bike_y)
    car_motion()
    for count2 in range(X.size):
        obstacle(X[count2], obstacle_y)
        obstaclecol(X[count2], obstacle_y)
    count4 = 0
    while count4 < len(X2):
        for count3 in X2[count4]:
            cone(count3, cone_y)
            conecol(count3, cone_y)
        count4 += 1
    lifes()
    bullet_fire()
    heli_movement()
    collision()
    clock.tick(fps)
    pygame.display.update()


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (bk_x, bk_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_a:
                direction = 'left'
                bike_x_change = -9
                bk_change = 9
            if event.key == pygame.K_d:
                direction = 'right'
                bike_x_change = 9
                bk_change = 9
            if event.key == pygame.K_SPACE:
                jumping = 'yes'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                bike_x_change = 0
                bk_change = 0
    main()
