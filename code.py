import pygame as pg
import random
import math
from pygame import mixer

# Initialize pygame
pg.init()


# Screen
wn = pg.display.set_mode((800, 600))

# Background
background = pg.image.load("Background.png")
background = pg.transform.scale(background, (800, 600))

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load("Logo.png")
icon = pg.transform.scale(icon, (64, 64))
pg.display.set_icon(icon)

# Player
playerImg = pg.image.load("Player.png")
playerImg = pg.transform.scale(playerImg, (64, 64))
playerX = 368
playerY = 486
playerX_change = 0

# Bullet
# State = Ready: the bullet isn't visible
# State = Fire: the bullet is fired
bulletImg = pg.image.load("Bullet.png")
bulletImg = pg.transform.scale(bulletImg, (32, 32))
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# Bullet 2
bulletImg2 = pg.image.load("Bullet.png")
bulletImg2 = pg.transform.scale(bulletImg2, (32, 32))
bulletX2 = 370
bulletY2 = 480
bulletX_change2 = 0
bulletY_change2 = 2
bullet_state2 = "ready"

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pg.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(20)

# Score
score_value = 0
font = pg.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game over text
over_font = pg.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 225))
    wn.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    wn.blit(over_text, (200, 250))


def player(x, y):
    wn.blit(playerImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    wn.blit(bulletImg, (x - 16, y + 10))


def fire_bullet2(x, y):
    global bullet_state2
    bullet_state2 = "fire"
    wn.blit(bulletImg, (x + 46, y + 10))


def enemy(x, y, i):
    wn.blit(enemyImg[i], (x, y))


def is_collision(x, y, xx, yy):
    distance = math.sqrt((math.pow(x - xx, 2)) + (math.pow(y - yy, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game main loop
game_continue = True
while game_continue:
    wn.fill((45, 45, 65))
    wn.blit(background, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_continue = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change -= 0.4
            if event.key == pg.K_RIGHT:
                playerX_change += 0.4
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                if bullet_state2 == "ready":
                    bulletX2 = playerX
                    fire_bullet2(bulletX2, bulletY2)
                    bullet_sound = mixer.Sound("shoot.wav")
                    bullet_sound.play()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_enemies):

        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] -= 0.3
            enemyY[i] += enemyY_change[i]

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        collision2 = is_collision(enemyX[i], enemyY[i], bulletX2, bulletY2)
        if collision2:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY2 = 480
            bullet_state2 = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"

    if bulletY2 < 0:
        bulletY2 = 480
        bullet_state2 = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bullet_state2 == "fire":
        fire_bullet2(bulletX2, bulletY2)
        bulletY2 -= bulletY_change2

    player(playerX, playerY)
    show_score(textX, textY)
    pg.display.update()
