import pygame as pg
import random
import math
from pygame import mixer

# initialize pygame library
pg.init()

# Create screen
screen = pg.display.set_mode((800, 600))

# Background
background = pg.image.load('background.jpg')

# Background Sound


# Title and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load('001-spaceship.png')
pg.display.set_icon(icon)

# Player
playerImg = pg.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemyImg.append(pg.image.load('palak.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(70)

# Bullet
bulletImg = pg.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 1
bullet_state = "ready"

explosionImg = pg.image.load('explosion.png')


score_value = 0
score_font = pg.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
over_font = pg.font.Font('freesansbold.ttf', 64)

# Pause Text
pause_font = pg.font.Font('freesansbold.ttf', 64)


def start_menu():
    start_text = pause_font.render('MAIN MENU', True, pg.color.Color('White'))
    start_msg = score_font.render('Press Spacebar to Begin', True, pg.color.Color('White'))
    starttxt_rect = start_text.get_rect(center=(800 / 2, 600 / 2))
    startmsg_rect = start_msg.get_rect(center=(800 / 2, 700 / 2))
    screen.blit(start_text, starttxt_rect)
    screen.blit(start_msg, startmsg_rect)


def pause_menu():
    pause_text = pause_font.render('PAUSE', True, pg.color.Color('White'))
    pause_msg = score_font.render('Press Spacebar to Resume', True, pg.color.Color('White'))
    pausetxt_rect = pause_text.get_rect(center=(800 / 2, 600 / 2))
    pausemsg_rect = pause_msg.get_rect(center=(800 / 2, 700 / 2))
    screen.blit(pause_text, pausetxt_rect)
    screen.blit(pause_msg, pausemsg_rect)


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
RUNNING, PAUSE, START = 0, 1, 2
state = START

gamerunning = True
while gamerunning:

    screen.fill((0, 0, 0))
    # bg image
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            gamerunning = False

        # If keystroke, check right or left
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -0.5
            if event.key == pg.K_RIGHT:
                playerX_change = 0.5

            # Bullet event
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('lasersound.wav')
                    bullet_Sound.play()
                    bulletX = playerX  # X Coord of spaceship
                    fire_bullet(bulletX, bulletY)

            # Pause and Play button
            if event.key == pg.K_ESCAPE:
                state = PAUSE

            if event.key == pg.K_SPACE:
                state = RUNNING

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0

    if state == RUNNING:
        # Create X border so player can't leave screen
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        if playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            # Enemy screen border and movement
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.2
                enemyY[i] += enemyY_change[i]
            if enemyX[i] >= 736:
                enemyX_change[i] = -0.2
                enemyY[i] += enemyY_change[i]

            # Collision check
            collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                screen.blit(explosionImg, (enemyX[i], enemyY[i])) # IDK WHY THIS GUY WONT SHOW UP
                pg.time.delay(50)
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
                collision_Sound = mixer.Sound('killsound.wav')
                collision_Sound.play()

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    elif state == PAUSE:
        pause_menu()

    elif state == START:
        start_menu()

    pg.display.update()
