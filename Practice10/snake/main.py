import pygame
import time
import random


# Настройки
WIDTH, HEIGHT = 400, 400
SNAKE_BLOCK = 20 # Размер одной клетки
FPS = 5 # Начальная скорость

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)

pygame.mixer.music.load("Practice10\\snake\\background.mp3")
pygame.mixer.music.play(-1) # Зацикливаем музыку


def show_score(score, level):
    value = font_style.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(value, [0, 0])

def gameLoop():
    game_over = False
    
    # Начальные координаты головы
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0
    
    snake_List = []
    Length_of_snake = 1
    
    score = 0
    level = 1
    current_fps = FPS

    # Еда
    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

    current_direction = "RIGHT" # initial direction

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.mixer.music.stop()
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
                elif event.key == pygame.K_ESCAPE:
                    game_over = True
                    pygame.mixer.music.stop()
                elif event.key == pygame.K_r and game_over:
                    gameLoop() # Рестарт игры
                elif event.key == pygame.K_KP_PLUS:
                    pygame.mixer.music.set_volume(max(0.0, min(1.0, pygame.mixer.music.get_volume() + 0.1)))
                elif event.key == pygame.K_KP_MINUS:
                    pygame.mixer.music.set_volume(max(0.0, min(1.0, pygame.mixer.music.get_volume() - 0.1)))

        # 1. Проверка на выход за границы (Wall collision)
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True
            pygame.mixer.music.stop()

        x1 += x1_change
        y1 += y1_change
        screen.fill((0, 0, 0))
        
        # Рисуем еду
        pygame.draw.rect(screen, (0, 127, 127), [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        
        # Логика тела змейки
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка на столкновение с самим собой
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True

        # Рисуем змейку
        # Внутри цикла отрисовки змейки
        for i in range(len(snake_List)):
            # По умолчанию цвет тела - зеленый (или любой твой)
            green_val = 100 + (i * (155 // Length_of_snake)) # Градиент от темного к светлому
            color = (0, green_val, 0) 
            
            # Если это ПОСЛЕДНИЙ элемент (Голова)
            if i == len(snake_List) - 1:
                color = (0, 255, 0) # Ярко-зеленый для головы
                pygame.draw.rect(screen, color, [snake_List[i][0], snake_List[i][1], SNAKE_BLOCK, SNAKE_BLOCK])
                
                # МАЖОРСТВО: Рисуем маленькие глазки (черные квадратики)
                eye_size = 4
                # Левый глаз
                pygame.draw.rect(screen, (0, 0, 0), [snake_List[i][0] + 4, snake_List[i][1] + 4, eye_size, eye_size])
                # Правый глаз
                pygame.draw.rect(screen, (0, 0, 0), [snake_List[i][0] + 12, snake_List[i][1] + 4, eye_size, eye_size])
                
            # Если это ПЕРВЫЙ элемент (Хвост)
            elif i == 0:
                color = (0, 100, 0) # Темно-зеленый, чтоб плавно исчезал
                pygame.draw.rect(screen, color, [snake_List[i][0], snake_List[i][1], SNAKE_BLOCK, SNAKE_BLOCK])
                
            # Обычное тело
            else:
                pygame.draw.rect(screen, color, [snake_List[i][0], snake_List[i][1], SNAKE_BLOCK, SNAKE_BLOCK])
                # Добавим обводку, чтобы сегменты не сливались в одну колбасу
                pygame.draw.rect(screen, (0, 0, 0), [snake_List[i][0], snake_List[i][1], SNAKE_BLOCK, SNAKE_BLOCK], 1)

        show_score(score, level)
        pygame.display.update()

        # 2. Если съел еду
        if x1 == foodx and y1 == foody:
            # Генерим новую еду так, чтобы не попала в змейку
            while True:
                foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
                foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
                if [foodx, foody] not in snake_List:
                    break
            
            Length_of_snake += 1
            score += 1
            
            # 3. Уровни: каждые 3 очка растет уровень и скорость
            if score % 3 == 0:
                level += 1
                current_fps += 2 # Увеличиваем скорость

        clock.tick(current_fps)

    pygame.mixer.music.stop()
    pygame.quit()
    quit()
    

gameLoop()