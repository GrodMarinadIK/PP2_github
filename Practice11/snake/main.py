import pygame
import time
import random
import sqlite3
import os
from databass import init_db, save_score, get_top_scores

# --- КОНСТАНТЫ И НАСТРОЙКИ ---
SNAKE_BLOCK = 20 
GRID_WIDTH, GRID_HEIGHT = 20, 20
WIDTH, HEIGHT = GRID_WIDTH * SNAKE_BLOCK, GRID_HEIGHT * SNAKE_BLOCK

OFFSET = 30       
MENU_HEIGHT = 90  
WIN_WIDTH = WIDTH + (OFFSET * 2)
WIN_HEIGHT = HEIGHT + MENU_HEIGHT + OFFSET

FPS = 7 # Чуть ускорим для азарта

# --- БАЗА ДАННЫХ ---

# --- ИНИЦИАЛИЗАЦИЯ PYGAME ---
init_db()
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Snake Game: No Cuts Edition")
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
font_small = pygame.font.SysFont("Verdana", 18)
font_big = pygame.font.SysFont("Verdana", 50)

# Музыка с защитой от вылета
music_path = "Practice10\\snake\\background.mp3"
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
step = 0.05

def draw_grid():
    for x in range(0, WIDTH + 1, SNAKE_BLOCK):
        pygame.draw.line(screen, (35, 35, 35), (x + OFFSET, MENU_HEIGHT), (x + OFFSET, MENU_HEIGHT + HEIGHT))
    for y in range(0, HEIGHT + 1, SNAKE_BLOCK):
        pygame.draw.line(screen, (35, 35, 35), (OFFSET, y + MENU_HEIGHT), (OFFSET + WIDTH, y + MENU_HEIGHT))

def show_ui(score, level):
    # 1. Основной серый фон шапки
    pygame.draw.rect(screen, (40, 40, 45), [0, 0, WIN_WIDTH, MENU_HEIGHT])
    
    # 2. Текст (центрируем по вертикали, но чуть выше середины)
    val = font_style.render(f"SCORE: {score}  |  LEVEL: {level}", True, (255, 255, 255))
    screen.blit(val, [WIN_WIDTH//2 - val.get_width()//2, 25])
    
    # 3. ТОТ САМЫЙ ЧЕРНЫЙ ПРЯМОУГОЛЬНИК (Зазор)
    # Рисуем его высотой в 20 пикселей в самом низу MENU_HEIGHT
    GAP_HEIGHT = 20
    pygame.draw.rect(screen, (15, 15, 15), [0, MENU_HEIGHT - GAP_HEIGHT, WIN_WIDTH, GAP_HEIGHT])
    
    # Можно еще тонкую серую линию добавить для стиля, если хочешь
    # pygame.draw.line(screen, (60, 60, 60), (0, MENU_HEIGHT), (WIN_WIDTH, MENU_HEIGHT), 1)

def get_input():
    user_name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(user_name) == 3: return user_name
                elif event.key == pygame.K_BACKSPACE: user_name = user_name[:-1]
                elif len(user_name) < 3 and event.unicode.isalpha(): user_name += event.unicode.upper()
        
        screen.fill((10, 10, 10))
        prompt = font_small.render("ENTER 3 LETTERS TO SAVE :", True, (255, 255, 255))
        screen.blit(prompt, (WIN_WIDTH//2 - prompt.get_width()//2, 150))
        name_surf = font_big.render(user_name, True, (0, 255, 0))
        screen.blit(name_surf, (WIN_WIDTH//2 - name_surf.get_width()//2, 200))
        pygame.display.update()

def gameLoop():
    game_over = False
    start_ticks = pygame.time.get_ticks()
    
    x1, y1 = WIDTH // 2, HEIGHT // 2
    x1_change, y1_change = 0, 0
    
    snake_List = []
    Length_of_snake = 1
    score, level, current_fps = 0, 1, FPS
    current_direction = "STOP"

    foodx = random.randrange(0, WIDTH, SNAKE_BLOCK)
    foody = random.randrange(0, HEIGHT, SNAKE_BLOCK)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and current_direction != "DOWN":
                    x1_change, y1_change = 0, -SNAKE_BLOCK
                    current_direction = "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    x1_change, y1_change = 0, SNAKE_BLOCK
                    current_direction = "DOWN"
                elif event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    x1_change, y1_change = -SNAKE_BLOCK, 0
                    current_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    x1_change, y1_change = SNAKE_BLOCK, 0
                    current_direction = "RIGHT"
                elif event.key == pygame.K_KP_PLUS:
                    pygame.mixer.music.set_volume(min(1, pygame.mixer.music.get_volume() + step))
                elif event.key == pygame.K_KP_MINUS:
                    pygame.mixer.music.set_volume(max(0, pygame.mixer.music.get_volume() - step))

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0: game_over = True

        x1 += x1_change
        y1 += y1_change
        screen.fill((15, 15, 15))
        draw_grid()
        
        # Еда
        pygame.draw.rect(screen, (160, 22, 65), [foodx + OFFSET, foody + MENU_HEIGHT, SNAKE_BLOCK, SNAKE_BLOCK])
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake: del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head: game_over = True

        # --- ОТРИСОВКА ЗМЕЙКИ С ГРАДИЕНТОМ ---
        for i, (sx, sy) in enumerate(snake_List):
            is_head = (i == len(snake_List) - 1)
            # Плавный градиент: от хвоста (темный) к голове (яркий)
            # Чем ближе к голове (индекс i выше), тем ярче зеленый
            brightness = 100 + (i * (155 // max(1, Length_of_snake)))
            color = (0, min(255, brightness), 0)
            
            rect = [sx + OFFSET, sy + MENU_HEIGHT, SNAKE_BLOCK, SNAKE_BLOCK]
            pygame.draw.rect(screen, color, rect)
            
            if is_head:
                # Глаза
                pygame.draw.rect(screen, (0, 0, 0), [sx + OFFSET + 4, sy + MENU_HEIGHT + 4, 4, 4])
                pygame.draw.rect(screen, (0, 0, 0), [sx + OFFSET + 12, sy + MENU_HEIGHT + 4, 4, 4])
            else:
                # Обводка сегментов, чтобы не сливались
                pygame.draw.rect(screen, (15, 15, 15), rect, 1)

        show_ui(score, level)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            while True:
                foodx = random.randrange(0, WIDTH, SNAKE_BLOCK)
                foody = random.randrange(0, HEIGHT, SNAKE_BLOCK)
                if [foodx, foody] not in snake_List: break
            Length_of_snake += 1
            score += 1
            if score % 3 == 0:
                level += 1
                current_fps += 1

        clock.tick(current_fps)

    # --- ФИНАЛ ---
    pygame.mixer.music.stop()
    play_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
    
    nickname = get_input()
    save_score(nickname, score, play_time)
    
    print("\n--- LEADERBOARD ---")
    for row in get_top_scores():
        print(f"{row[0]} : {row[1]} pts")
    
    pygame.quit(); exit()

gameLoop()