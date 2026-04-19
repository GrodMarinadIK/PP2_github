import pygame

def draw_smooth_line(surf, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surf, color, (x, y), radius)

def drawRect(surf, color, start, end, width): # Добавили width
    x1, y1 = start
    x2, y2 = end
    w, h = abs(x1 - x2), abs(y1 - y2)
    # Рисуем рамку толщиной в width
    pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), w, h), width)

def drawCircle(surf, color, start, end, width): # Добавили width
    x1, y1 = start
    x2, y2 = end
    rad = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
    # Рисуем окружность толщиной в width
    pygame.draw.circle(surf, color, start, rad, width)
    
def main():
    pygame.init()
    W, H = 900, 600
    MENU_HEIGHT = 100
    screen = pygame.display.set_mode((W, H))
    
    canvas = pygame.Surface((W, H - MENU_HEIGHT))
    canvas.fill((0, 0, 0))
    
    history = [canvas.copy()]
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 15)
    
    # Состояние
    radius = 15
    color = (0, 0, 255)
    mode = 'brush'
    drawing = False
    start_pos = None
    last_pos = None

    # --- Определение кнопок инструментов ---
    btn_brush = pygame.Rect(10, 10, 80, 80)
    btn_rect = pygame.Rect(100, 10, 80, 80)
    btn_circle = pygame.Rect(190, 10, 80, 80)
    btn_eraser = pygame.Rect(280, 10, 80, 80)
    
    # Кнопки цветов
    colors = [
        (pygame.Rect(370, 10, 40, 40), (255, 0, 0)),   # Red
        (pygame.Rect(415, 10, 40, 40), (0, 255, 0)),   # Green
        (pygame.Rect(370, 55, 40, 40), (0, 0, 255)),   # Blue
        (pygame.Rect(415, 55, 40, 40), (255, 255, 255))# White
    ]

    # Кнопки радиуса (сетка 3x2 справа)
    radius_buttons = []
    radii_values = [2, 5, 10, 20, 35, 50]
    for i in range(6):
        col, row = i % 3, i // 3
        rect = pygame.Rect(W - 140 + col * 45, 10 + row * 45, 40, 40)
        radius_buttons.append((rect, radii_values[i], str(i+1)))

    while True:
        pos = pygame.mouse.get_pos()
        canvas_pos = (pos[0], pos[1] - MENU_HEIGHT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            if event.type == pygame.KEYDOWN:
                # Ctrl + Z (Undo)
                if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if len(history) > 1:
                        history.pop()
                        canvas.blit(history[-1], (0, 0))

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка кнопок инструментов
                if btn_brush.collidepoint(pos): mode = 'brush'
                elif btn_rect.collidepoint(pos): mode = 'rect'
                elif btn_circle.collidepoint(pos): mode = 'circle'
                elif btn_eraser.collidepoint(pos): mode = 'eraser'
                
                # Проверка цветов
                for r, c in colors:
                    if r.collidepoint(pos): color = c
                
                # Проверка радиусов
                for r, val, label in radius_buttons:
                    if r.collidepoint(pos): radius = val
                
                # Начало рисования
                if pos[1] > MENU_HEIGHT:
                    drawing = True
                    start_pos = canvas_pos
                    last_pos = canvas_pos
                    if len(history) > 20: history.pop(0)
                    history.append(canvas.copy())
            
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    if mode == 'rect': 
                        drawRect(canvas, color, start_pos, canvas_pos, radius) # Передали radius
                    elif mode == 'circle': 
                        drawCircle(canvas, color, start_pos, canvas_pos, radius) # Передали radius
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if mode in ['brush', 'eraser']:
                    curr_col = color if mode == 'brush' else (0, 0, 0)
                    draw_smooth_line(canvas, curr_col, last_pos, canvas_pos, radius)
                    last_pos = canvas_pos

        # --- ОТРИСОВКА ---
        screen.fill((30, 30, 30))
        screen.blit(canvas, (0, MENU_HEIGHT))
        
        # Панель меню
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, W, MENU_HEIGHT))
        
        # Отрисовка кнопок инструментов
        for r, txt, m in [(btn_brush, "Brush", 'brush'), (btn_rect, "Rect", 'rect'), 
                          (btn_circle, "Circle", 'circle'), (btn_eraser, "Eraser", 'eraser')]:
            col = (150, 150, 150) if mode == m else (200, 200, 200)
            pygame.draw.rect(screen, col, r)
            t_surf = font.render(txt, True, (0, 0, 0))
            screen.blit(t_surf, t_surf.get_rect(center=r.center))

        # Цвета
        for r, c in colors:
            pygame.draw.rect(screen, c, r)
            if color == c: pygame.draw.rect(screen, (255, 255, 255), r, 2)

        # Радиусы
        for r, val, label in radius_buttons:
            col = (150, 150, 150) if radius == val else (200, 200, 200)
            pygame.draw.rect(screen, col, r)
            t_surf = font.render(label, True, (0, 0, 0))
            screen.blit(t_surf, t_surf.get_rect(center=r.center))

        # Предпросмотр
        if drawing and start_pos:
            scr_start = (start_pos[0], start_pos[1] + MENU_HEIGHT)
            if mode == 'rect': 
                drawRect(screen, color, scr_start, pos, radius) # Передали radius
            elif mode == 'circle': 
                drawCircle(screen, color, scr_start, pos, radius) # Передали radius

        pygame.display.flip()
        clock.tick(60)

main()