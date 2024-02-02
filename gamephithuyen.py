import pygame, random
from math import sqrt, pow
from tkinter import messagebox, Tk
from time import sleep

# tạo modun trong pygame
pygame.init()

# tạo màn hình
screen = pygame.display.set_mode((800, 600))

# tạo nền
background = pygame.image.load("background.png")

# tiêu đề và biểu tượng
pygame.display.set_caption("My game")
obj = pygame.image.load("intro.png")
pygame.display.set_icon(obj)

# tạo con tàu vũ trụ hiển thị trên màn hình
spaceship = pygame.image.load("spaceship.png")
x, y, delta_x, delta_y = 0, 0, 0, 0

# ranh giới va chạm với các UFO
right_collision = [False] * 8

# tạo danh sách ufo trên màn hình
ufo = [pygame.image.load("ufo.png")] * 8
a, b = 0, 0

# tạo dấu đầu dòng
bullet = pygame.image.load("bullet.png")
bullet_X, bullet_Y, bullet_fired = 0, 0, 0

# hiển thị điểm

score = 0


def display_score(score):
    font1 = pygame.font.Font("freesansbold.ttf", 32)
    text = font1.render("Score: " + str(score), True, "#3333FF")
    screen.blit(text, (0, 0))


# âm thanh nền

pygame.mixer.music.load("background_sound.wav")
pygame.mixer.music.play(loops=-1)


# trò chơi kết thúc

def game_over():
    font2 = pygame.font.Font("freesansbold.ttf", 96)
    text = font2.render("GAME OVER", True, "#FFFFFF")
    screen.blit(text, (150, 300))


# khởi tạo các yếu tố của trò chơi


def init_game():
    global x
    global y
    global delta_x
    global delta_y
    global a
    global b
    global bullet_fired
    global bullet_X
    global bullet_Y
    global right_collision
    global score
    x, y = 300, 400
    delta_x = delta_y = 0
    right_collision = [False] * 8
    b = random.sample(range(5, 21), 8)
    a = random.sample(range(300, 701), 8)
    bullet_fired = False
    bullet_X, bullet_Y = x + 31, y
    score = 0


# lặp lại trò chơi

init_game()

executing = True
while executing:
    screen.fill("#990099")
    screen.blit(background, (0, 0))
    display_score(score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executing = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                delta_x = -6
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                delta_x = 6
            if event.key in (pygame.K_UP, pygame.K_w):
                delta_y = -6
            if event.key in (pygame.K_DOWN, event.key == pygame.K_s):
                delta_y = 6
            if event.key == pygame.K_SPACE:
                bullet_fired = True
                cannon_sound = pygame.mixer.Sound("cannon_sound.wav")
                cannon_sound.play()
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                             pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                delta_x = delta_y = 0

    if -30 < x + delta_x < 700:
        x += delta_x
    if 0 < y + delta_y < 470:
        y += delta_y

    for i in range(8):
        if (x <= a[i] <= x + 128 and y <= b[i] <= y + 128) or b[i] >= 580:
            root = Tk()
            root.withdraw()
            game_over()
            pygame.display.update()
            sleep(1)
            message = messagebox.askyesno(title="New game?", message="Do you want to restart game?")
            if not message:
                executing = False
            else:
                init_game()
            break

        if not right_collision[i]:
            a[i] += 3
        else:
            a[i] -= 3
        if a[i] >= 780:
            right_collision[i] = True
            b[i] += 25
        if a[i] <= 0:
            right_collision[i] = False
            b[i] += 25
        screen.blit(ufo[i], (a[i], b[i]))

        bullet_to_ufo = sqrt(pow(bullet_X - a[i], 2) + pow(bullet_Y - b[i], 2))

        if bullet_Y <= 0 or bullet_to_ufo <= 20:
            bullet_Y = y
            bullet_fired = False
            if bullet_to_ufo <= 20:
                a[i], b[i] = random.randint(330, 370), random.randint(5, 20)
                screen.blit(ufo[i], (a[i], b[i]))
                score += 1
                explosion_sound = pygame.mixer.Sound("explosion_sound.wav")
                explosion_sound.play()

    if bullet_fired:
        bullet_Y -= 15
    else:
        bullet_X, bullet_Y = x + 47, y

    screen.blit(bullet, (bullet_X, bullet_Y))

    screen.blit(spaceship, (x, y))

    # lưa trữ màn hình cũ đến khi xuất hiện màn hình mới
    pygame.display.update()
