import pygame
import os
from tools import *

def main():
    pygame.init()
    W, H = 1600, 800
    MENU_HEIGHT = 120
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Paint")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon = pygame.image.load(os.path.join(current_dir, "assets", "icon.png"))
    pygame.display.set_icon(icon)
    
    canvas = pygame.Surface((W, H - MENU_HEIGHT))
    canvas.fill((0, 0, 0))
    
    history = [canvas.copy()]
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 14)
    
    radius = 2
    color = (255, 255, 255)
    mode = 'brush'
    drawing = False
    start_pos = None
    last_pos = None
    
    # Текстовый ввод
    text_input = ""
    text_pos = None
    typing = False

    tools = ['brush', 'line', 'rect', 'square', 'circle', 'right_tri', 'eq_tri', 'rhombus', 'fill', 'text', 'eraser']
    buttons = [(pygame.Rect(10 + i*90, 10, 85, 40), t) for i, t in enumerate(tools)]
    
    # Цвета и быстрые радиусы
    colors_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 0, 0), (255, 255, 255)]
    color_rects = [(pygame.Rect((W*0.75) + i*45, 10, 40, 40), c) for i, c in enumerate(colors_list)]

    while True:
        pos = pygame.mouse.get_pos()
        canvas_pos = (pos[0], pos[1] - MENU_HEIGHT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            
            # --- Обработка текста ---
            if typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Тот же динамический шрифт для финального рендера на холст
                        dynamic_font = pygame.font.SysFont("Verdana", radius + 12)
                        txt_surf = dynamic_font.render(text_input, True, color)
                        canvas.blit(txt_surf, text_pos)
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                continue # Пока печатаем, другие действия игнорим

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Меню
                for r, m in buttons:
                    if r.collidepoint(pos): mode = m
                for r, c in color_rects:
                    if r.collidepoint(pos): color = c
                    
                # Холст
                if pos[1] > MENU_HEIGHT:
                    if len(history) > 20: # Оставляем последние 20 шагов
                        history.pop(0)    # Удаляем самый старый "скриншот"
                    history.append(canvas.copy())
                    if mode == 'fill':
                        flood_fill(canvas, canvas_pos[0], canvas_pos[1], color)
                    elif mode == 'text':
                        typing = True
                        text_pos = canvas_pos
                    else:
                        drawing = True
                        start_pos = canvas_pos
                        last_pos = canvas_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    args = (canvas, color, start_pos, canvas_pos, radius)
                    if mode == 'line': draw_line(*args)
                    elif mode == 'rect': drawRect(*args)
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
                # Бинды радиуса
                if event.key == pygame.K_1: radius = 2
                if event.key == pygame.K_2: radius = 5
                if event.key == pygame.K_3: radius = 10
                if event.key == pygame.K_4: radius = 20
                if event.key == pygame.K_5: radius = 35
                if event.key == pygame.K_6: radius = 50
                # Undo и Save
                if (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    if event.key == pygame.K_z and len(history) > 1:
                        canvas.blit(history.pop(), (0, 0))
                    if event.key == pygame.K_s:
                        save_canvas(canvas)

        # --- ОТРИСОВКА ---
        screen.fill((30, 30, 30))
        screen.blit(canvas, (0, MENU_HEIGHT))
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, W, MENU_HEIGHT))

        # UI Кнопки
        for r, m in buttons:
            pygame.draw.rect(screen, (100, 100, 100) if mode == m else (180, 180, 180), r)
            txt = font.render(m.capitalize(), True, (0, 0, 0))
            screen.blit(txt, txt.get_rect(center=r.center))

        for r, c in color_rects:
            pygame.draw.rect(screen, c, r)
            if color == c: pygame.draw.rect(screen, (200, 0, 0), r, 3)

        # Инфо панель
        info = font.render(f"Mode: {mode} | Size: {radius} | Ctrl+Z: Undo | Ctrl+S: Save", True, (200, 200, 200))
        screen.blit(info, (10, 70))

        # Предпросмотр и текст
        if drawing and mode not in ['brush', 'eraser']:
            scr_start = (start_pos[0], start_pos[1] + MENU_HEIGHT)
            args = (screen, color, scr_start, pos, radius)
            if mode == 'line': draw_line(*args)
            elif mode == 'rect': drawRect(*args)
            elif mode == 'square': drawSquare(*args)
            elif mode == 'circle': drawCircle(*args)
            elif mode == 'right_tri': drawRightTriangle(*args)
            elif mode == 'eq_tri': drawEquilateralTriangle(*args)
            elif mode == 'rhombus': drawRhombus(*args)
        
        if typing:
            dynamic_font = pygame.font.SysFont("Verdana", radius + 12)  # <-- динамический размер
            txt_surface = dynamic_font.render(text_input + "|", True, color)
            screen.blit(txt_surface, (text_pos[0], text_pos[1] + MENU_HEIGHT))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()