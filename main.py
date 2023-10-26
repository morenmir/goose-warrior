import pygame
import random
from os import listdir

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
pygame.init()

FPS = pygame.time.Clock()
screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
ORANGE = 255, 97, 3

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

#player = pygame.Surface((20, 20))
#player.fill(WHITE)
#player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player_imgs = [pygame.transform.scale(pygame.image.load(IMGS_PATH + '/' + file).convert_alpha(), [120,50]) for file in listdir(IMGS_PATH)]
#player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(), [120,50])
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 10


def create_enemy():
    #enemy = pygame.Surface((20,20))
    #enemy.fill(RED)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), [120,50])
    enemy_rect = pygame.Rect(width, random.randint(0, (height-50)), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

scores = 0
enemies = []

def create_bonus():
    #bonus = pygame.Surface((20,20))
    #bonus.fill(CYAN2)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), [100,100])
    bonus_rect = pygame.Rect(random.randint(0, (width-100)), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]

def show_game_over_message():
    
    game_over_text = font.render("Game Over", True, RED)
    text_rect = game_over_text.get_rect(center=(width/2, height/2))
    main_surface.blit(game_over_text, text_rect)
    
    pygame.display.flip()
    pygame.time.delay(3000)


bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0

bonuses = []

is_working = True

while is_working:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]


    
    pressed_keys = pygame.key.get_pressed()

    #main_surface.blit(bg, (0, 0))
    #main_surface.fill(WHITE)

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < - bg.get_width():
        bgX = bg.get_width()

    if bgX2 < - bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))


    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, ORANGE), (width - 40, 20))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False
            show_game_over_message()


    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1


    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <=0:
        player_rect = player_rect.move(-player_speed, 0)

    

    #enemy_rect = enemy_rect.move(-enemy_speed, 0)
    
    pygame.display.flip()





