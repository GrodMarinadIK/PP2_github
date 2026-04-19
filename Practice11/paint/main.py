import pygame
import math

# Функция для плавного рисования кистью
def draw_smooth_line(surf, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surf, color, (x, y), radius)

# Рисование прямоугольника
def drawRect(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    w, h = abs(x1 - x2), abs(y1 - y2)
    pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), w, h), width)

# Рисование квадрата (используем минимальную сторону, чтобы получился ровный квадрат)
def drawSquare(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x1 - x2), abs(y1 - y2))
    new_x = x1 if x2 > x1 else x1 - side
    new_y = y1 if y2 > y1 else y1 - side
    pygame.draw.rect(surf, color, (new_x, new_y, side, side), width)

# Рисование круга
def drawCircle(surf, color, start, end, width):
    rad = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, rad, width)

# Рисование прямоугольного треугольника
def drawRightTriangle(surf, color, start, end, width):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surf, color, points, width)

# Рисование равностороннего треугольника
def drawEquilateralTriangle(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    side = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
    height = int(side * math.sqrt(3) / 2)
    # Вычисляем точки относительно начального нажатия
    points = [
        (x1, y1 - height // 2), 
        (x1 - side // 2, y1 + height // 2), 
        (x1 + side // 2, y1 + height // 2)
    ]
    pygame.draw.polygon(surf, color, points, width)

# Рисование ромба
def drawRhombus(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    points = [
        (x1, y1 - (y1 - y2)), # Верх
        (x1 + (x1 - x2), y1), # Право
        (x1, y1 + (y1 - y2)), # Низ
        (x1 - (x1 - x2), y1)  # Лево
    ]
    pygame.draw.polygon(surf, color, points, width)

def main():
    pygame.init()
    # Увеличили размер окна для удобства
    W, H = 1200, 800
    MENU_HEIGHT = 120
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Paint")
    icon = pygame.image.load("Practice11\\paint\\icon.png")
    pygame.display.set_icon(icon)
    canvas = pygame.Surface((W, H - MENU_HEIGHT))
    canvas.fill((0, 0, 0))
    
    history = [canvas.copy()]
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 12)
    
    radius = 2
    color = (0, 0, 255)
    mode = 'brush'
    drawing = False
    start_pos = None
    last_pos = None

    # Названия всех режимов для кнопок
    tools = ['brush', 'rect', 'square', 'circle', 'right_tri', 'eq_tri', 'rhombus', 'eraser']
    buttons = []
    for i, t in enumerate(tools):
        buttons.append((pygame.Rect(10 + i*90, 10, 80, 80), t))

    colors_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0), (255, 165, 0)]
    color_rects = []
    for i, c in enumerate(colors_list):
        color_rects.append((pygame.Rect(750 + (i%3)*45, 10 + (i//3)*45, 40, 40), c))

    radii_values = [2, 5, 10, 20, 35, 50]
    radius_buttons = []
    for i, r_val in enumerate(radii_values):
        radius_buttons.append((pygame.Rect(W - 140 + (i%3)*45, 10 + (i//3)*45, 40, 40), r_val))

    while True:
        pos = pygame.mouse.get_pos()
        canvas_pos = (pos[0], pos[1] - MENU_HEIGHT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Клики по меню
                for r, m in buttons:
                    if r.collidepoint(pos): mode = m
                for r, c in color_rects:
                    if r.collidepoint(pos): color = c
                for r, v in radius_buttons:
                    if r.collidepoint(pos): radius = v
                    
                # Начало рисования на холсте
                if pos[1] > MENU_HEIGHT:
                # Перед тем как начать рисовать, сохраняем копию холста
                    if len(history) > 20: # Ограничитель
                        history.pop(0)
                    history.append(canvas.copy())
                    drawing = True
                    start_pos = canvas_pos
                    last_pos = canvas_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    # Применяем финальную фигуру к холсту
                    args = (canvas, color, start_pos, canvas_pos, radius)
                    if mode == 'rect': drawRect(*args)
                    elif mode == 'square': drawSquare(*args)
                    elif mode == 'circle': drawCircle(*args)
                    elif mode == 'right_tri': drawRightTriangle(*args)
                    elif mode == 'eq_tri': drawEquilateralTriangle(*args)
                    elif mode == 'rhombus': drawRhombus(*args)
                    drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if mode in ['brush', 'eraser']:
                    c_col = color if mode == 'brush' else (0,0,0)
                    draw_smooth_line(canvas, c_col, last_pos, canvas_pos, radius)
                    last_pos = canvas_pos
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if len(history) > 1:
                        # Убираем текущее состояние и достаем предыдущее
                        history.pop() 
                        canvas.blit(history[-1], (0, 0))
        # Отрисовка
        screen.fill((30, 30, 30))
        screen.blit(canvas, (0, MENU_HEIGHT))
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, W, MENU_HEIGHT))

        # Рисуем кнопки инструментов
        for r, m in buttons:
            pygame.draw.rect(screen, (100, 100, 100) if mode == m else (180, 180, 180), r)
            txt = font.render(m.capitalize(), True, (0, 0, 0))
            screen.blit(txt, txt.get_rect(center=r.center))

        # Рисуем выбор цвета и радиуса
        for r, c in color_rects:
            pygame.draw.rect(screen, c, r)
            if color == c: pygame.draw.rect(screen, (0,0,0), r, 2)
        for r, v in radius_buttons:
            pygame.draw.rect(screen, (100, 100, 100) if radius == v else (200, 200, 200), r)
            txt = font.render(str(v), True, (0,0,0))
            screen.blit(txt, txt.get_rect(center=r.center))

        # Предпросмотр (рисуем на основном screen поверх всего)
        if drawing and mode not in ['brush', 'eraser']:
            scr_start = (start_pos[0], start_pos[1] + MENU_HEIGHT)
            args = (screen, color, scr_start, pos, radius)
            if mode == 'rect': drawRect(*args)
            elif mode == 'square': drawSquare(*args)
            elif mode == 'circle': drawCircle(*args)
            elif mode == 'right_tri': drawRightTriangle(*args)
            elif mode == 'eq_tri': drawEquilateralTriangle(*args)
            elif mode == 'rhombus': drawRhombus(*args)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()