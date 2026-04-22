import pygame
import random
import os

# --- КОНСТАНТЫ И НАСТРОЙКИ ---
SNAKE_BLOCK = 20 
GRID_WIDTH, GRID_HEIGHT = 20, 20
WIDTH, HEIGHT = GRID_WIDTH * SNAKE_BLOCK, GRID_HEIGHT * SNAKE_BLOCK

OFFSET = 30       
MENU_HEIGHT = 90  
WIN_WIDTH = WIDTH + (OFFSET * 2)
WIN_HEIGHT = HEIGHT + MENU_HEIGHT + OFFSET

FPS = 60 
INITIAL_SNAKE_SPEED = 8 

# --- ИНИЦИАЛИЗАЦИЯ ---
try:
    from databass import init_db, save_score, get_top_scores
    init_db()
except ImportError:
    def init_db(): pass
    def save_score(n, s, t): print(f"Saving: {n} {s}")
    def get_top_scores(): return []

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Snake: Gold Edition")
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
font_small = pygame.font.SysFont("Verdana", 18)
font_big = pygame.font.SysFont("Verdana", 50)

# Музыка
try:
    music_path = "Practice10\\snake\\background.mp3"
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
except:
    pass

def draw_grid():
    for x in range(0, WIDTH + 1, SNAKE_BLOCK):
        pygame.draw.line(screen, (35, 35, 35), (x + OFFSET, MENU_HEIGHT), (x + OFFSET, MENU_HEIGHT + HEIGHT))
    for y in range(0, HEIGHT + 1, SNAKE_BLOCK):
        pygame.draw.line(screen, (35, 35, 35), (OFFSET, y + MENU_HEIGHT), (OFFSET + WIDTH, y + MENU_HEIGHT))

def show_ui(score, level):
    pygame.draw.rect(screen, (40, 40, 45), [0, 0, WIN_WIDTH, MENU_HEIGHT])
    val = font_style.render(f"SCORE: {score}  |  LEVEL: {level}", True, (255, 255, 255))
    screen.blit(val, [WIN_WIDTH//2 - val.get_width()//2, 25])
    GAP_HEIGHT = 20
    pygame.draw.rect(screen, (15, 15, 15), [0, MENU_HEIGHT - GAP_HEIGHT, WIN_WIDTH, GAP_HEIGHT])

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
    
    snake_speed = INITIAL_SNAKE_SPEED
    move_delay = 1000 // snake_speed
    last_move_time = pygame.time.get_ticks()
    
    x1, y1 = WIDTH // 2, HEIGHT // 2
    snake_List = [[x1, y1]]
    Length_of_snake = 1
    score, level = 0, 1
    
    def spawn_food(snake_list, is_gold=False):
        while True:
            fx = random.randrange(0, WIDTH, SNAKE_BLOCK)
            fy = random.randrange(0, HEIGHT, SNAKE_BLOCK)
            if [fx, fy] not in snake_list:
                return {
                    "pos": [fx, fy],
                    "type": 2 if is_gold else 1,
                    "spawn_time": pygame.time.get_ticks(),
                    "lifetime": 5000 if is_gold else None
                }
    
    current_direction = "STOP"
    next_direction = "STOP"
    step = 0.05

    food = spawn_food(snake_List)
    gold_food = None 

    while not game_over:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and current_direction != "DOWN":
                    next_direction = "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    next_direction = "RIGHT"
                elif event.key == pygame.K_KP_PLUS:
                    pygame.mixer.music.set_volume(min(1, pygame.mixer.music.get_volume() + step))
                elif event.key == pygame.K_KP_MINUS:
                    pygame.mixer.music.set_volume(max(0, pygame.mixer.music.get_volume() - step))

        # 1. ЛОГИКА ШАГА
        if next_direction != "STOP" and current_time - last_move_time > move_delay:
            current_direction = next_direction
            
            new_x, new_y = x1, y1
            if current_direction == "UP": new_y -= SNAKE_BLOCK
            elif current_direction == "DOWN": new_y += SNAKE_BLOCK
            elif current_direction == "LEFT": new_x -= SNAKE_BLOCK
            elif current_direction == "RIGHT": new_x += SNAKE_BLOCK

            if new_x >= WIDTH or new_x < 0 or new_y >= HEIGHT or new_y < 0:
                game_over = True
            else:
                x1, y1 = new_x, new_y
                snake_Head = [x1, y1]
                
                if snake_Head in snake_List:
                    game_over = True
                
                snake_List.append(snake_Head)

                # 2. ПРОВЕРКА ЕДЫ (только во время шага)
                eaten = False
                for f_obj in [food, gold_food]:
                    if f_obj and x1 == f_obj["pos"][0] and y1 == f_obj["pos"][1]:
                        is_gold = (f_obj["type"] == 2)
                        points = 2 if is_gold else 1
                        score += points
                        Length_of_snake += points
                        
                        if not is_gold:
                            food = spawn_food(snake_List)
                            if random.random() < 0.2 and not gold_food:
                                gold_food = spawn_food(snake_List, is_gold=True)
                        else:
                            gold_food = None
                        
                        eaten = True
                        if score // 3 >= level:
                            level += 1
                            snake_speed += 1
                            move_delay = 1000 // snake_speed
                        break # Выходим из цикла проверки яблок, так как съели одно
                
                if not eaten:
                    if len(snake_List) > Length_of_snake:
                        del snake_List[0]

            last_move_time = current_time

        # 3. ПРОВЕРКА ВРЕМЕНИ ЗОЛОТОГО ЯБЛОКА (вне шага, чтобы исчезло вовремя)
        if gold_food:
            if current_time - gold_food["spawn_time"] > gold_food["lifetime"]:
                gold_food = None

        # 4. ОТРИСОВКА
        screen.fill((15, 15, 15))
        draw_grid()
        
        # Рисуем обычную еду
        pygame.draw.rect(screen, (160, 22, 65), [food["pos"][0] + OFFSET, food["pos"][1] + MENU_HEIGHT, SNAKE_BLOCK, SNAKE_BLOCK])
        
        # Рисуем золотую еду с эффектом мерцания
        if gold_food:
            time_passed = current_time - gold_food["spawn_time"]
            time_left = gold_food["lifetime"] - time_passed
            # Если осталось меньше 2 сек, мигаем
            if time_left > 2000 or (current_time // 100) % 2 == 0:
                pygame.draw.rect(screen, (255, 215, 0), [gold_food["pos"][0] + OFFSET, gold_food["pos"][1] + MENU_HEIGHT, SNAKE_BLOCK, SNAKE_BLOCK])

        # Отрисовка змейки
        for i, (sx, sy) in enumerate(snake_List):
            is_head = (i == len(snake_List) - 1)
            brightness = 100 + (i * (155 // max(1, Length_of_snake)))
            color = (0, min(255, brightness), 0)
            rect = [sx + OFFSET, sy + MENU_HEIGHT, SNAKE_BLOCK, SNAKE_BLOCK]
            pygame.draw.rect(screen, color, rect)
            if is_head:
                pygame.draw.rect(screen, (0, 0, 0), [sx + OFFSET + 4, sy + MENU_HEIGHT + 4, 4, 4])
                pygame.draw.rect(screen, (0, 0, 0), [sx + OFFSET + 12, sy + MENU_HEIGHT + 4, 4, 4])
            else:
                pygame.draw.rect(screen, (15, 15, 15), rect, 1)

        show_ui(score, level)
        pygame.display.update()
        clock.tick(FPS)

    # Финал
    pygame.mixer.music.stop()
    play_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
    nickname = get_input()
    save_score(nickname, score, play_time)
    pygame.quit(); exit()

if __name__ == "__main__":
    gameLoop()