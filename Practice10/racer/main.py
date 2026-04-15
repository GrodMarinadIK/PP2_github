import pygame, sys
from pygame.locals import *
import time
from classes import Enemy, Player, Coin
import constants
import classes
import random
from databass import init_db, save_score, get_top_scores

pygame.init()
pygame.mixer.init()

DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer")
FramePerSec = pygame.time.Clock()
background = pygame.image.load("Practice10\\racer\\images\\AnimatedStreet.png")


init_db()  # Initialize the database at the start of the game

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# render(текст, сглаживание, цвет)
game_over_text = font.render("Game Over", True, (0, 0, 0))

# Create objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

coin_render = pygame.image.load("Practice10\\racer\\images\\Coin.png")
coin_render_scaled = pygame.transform.scale(coin_render, (25, 25))

# Event for increasing speed 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000) # accelerate every 1 second

# Загружаем фоновую музыку
pygame.mixer.music.load("Practice10\\racer\\sounds\\background.mp3")

# Запускаем бесконечное воспроизведение (-1 значит зациклить)
pygame.mixer.music.play(-1)

def get_input():
    user_name = ""
    input_active = True
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(user_name) == 3: # Подтверждаем только если 3 буквы
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    # Добавляем только буквы и если их меньше 3
                    if len(user_name) < 3 and event.unicode.isalpha():
                        user_name += event.unicode.upper()

        # Отрисовка
        DISPLAYSURF.fill((0, 0, 0)) # Черный фон
        
        # Инструкция
        prompt_surf = font_small.render("ENTER 3 LETTERS:", True, constants.WHITE)
        DISPLAYSURF.blit(prompt_surf, (constants.SCREEN_WIDTH // 2 - 100, 200))
        
        # Тот самый ник, который мы печатаем
        name_surf = font.render(user_name, True, (0, 255, 0)) # Зеленый цвет как в терминале
        DISPLAYSURF.blit(name_surf, (constants.SCREEN_WIDTH // 2 - 50, 250))
        
        if len(user_name) == 3:
            hint_surf = font_small.render("Press ENTER to save", True, (200, 200, 200))
            DISPLAYSURF.blit(hint_surf, (constants.SCREEN_WIDTH // 2 - 90, 350))

        pygame.display.update()
    
    return user_name



while True:     
    constants.TOTAL_TIME += (1 / constants.FPS)  # Update total time survived
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            constants.SPEED += 0.1     # Increasing difficulty every second 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))

    # Drawing and moving all objects
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        
    # render(текст, сглаживание, цвет)
    scores = font_small.render(str(constants.COINS_COUNT), True, constants.BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    if constants.COINS_COUNT < 10:
        DISPLAYSURF.blit(coin_render_scaled, (26, 10))
    elif 10 <= constants.COINS_COUNT < 100:
        DISPLAYSURF.blit(coin_render_scaled, (36, 10))
    else:
        DISPLAYSURF.blit(coin_render_scaled, (46, 10))
    

    # End screen
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()  # Stop background musicx
        DISPLAYSURF.fill(constants.RED)
        DISPLAYSURF.blit(game_over_text, (30, 250))
        pygame.display.update()
        pygame.mixer.Sound("Practice10\\racer\\sounds\\crash.wav").play()
        time.sleep(2)
        print("GAME OVER!")
        nickname = get_input()
        save_score(nickname, constants.COINS_COUNT, constants.TOTAL_TIME)

        print("--- LEADERBOARD ---")
        for row in get_top_scores():    
            print(f"{row[0]} : {row[1]}")
        
        pygame.quit()
        sys.exit()
        
    if pygame.sprite.collide_rect(P1, C1):
        constants.COINS_COUNT += 1
        C1.rect.top = 0
        C1.rect.center = (random.randint(30, 370), 0)
         
    pygame.display.update()
    FramePerSec.tick(constants.FPS)