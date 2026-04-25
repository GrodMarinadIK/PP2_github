import pygame
import math
import os
from datetime import datetime


def draw_smooth_line(surf, color, start, end, radius):
    dx, dy = end[0] - start[0], end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surf, color, (x, y), radius)

def drawRect(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), abs(x1-x2), abs(y1-y2)), width)

def drawSquare(surf, color, start, end, width):
    side = min(abs(start[0] - end[0]), abs(start[1] - end[1]))
    new_x = start[0] if end[0] > start[0] else start[0] - side
    new_y = start[1] if end[1] > start[1] else start[1] - side
    pygame.draw.rect(surf, color, (new_x, new_y, side, side), width)

def drawCircle(surf, color, start, end, width):
    rad = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, rad, width)

# Рисование прямоугольного треугольника
def drawRightTriangle(surf, color, start, end, width):
    # Генерируем точки: начальная, угол 90 градусов, конечная
    points = [start, (start[0], end[1]), end]
    
    # Рисуем основной скелет треугольника
    pygame.draw.polygon(surf, color, points, width)
    
    # Если линия толстая, "заплавляем" углы кружками
    if width > 1:
        for p in points:
            # width // 2 — это радиус, чтобы круг идеально вписался в толщину линии
            pygame.draw.circle(surf, color, p, width // 2)

# Рисование равностороннего треугольника
def drawEquilateralTriangle(surf, color, start, end, width):
    x1, y1 = start
    x2, y2 = end
    # Считаем расстояние (сторону)
    side = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
    if side == 0: return
    
    height = int(side * math.sqrt(3) / 2)
    
    # Центрируем треугольник относительно точки нажатия
    points = [
        (x1, y1 - height // 2), 
        (x1 - side // 2, y1 + height // 2), 
        (x1 + side // 2, y1 + height // 2)
    ]
    
    # Рисуем сам полигон
    pygame.draw.polygon(surf, color, points, width)
    
    # ХИТРОСТЬ: Рисуем кружки в вершинах, чтобы закрыть "дырки" в углах
    # Делаем это только если ширина линии большая
    if width > 1:
        for p in points:
            pygame.draw.circle(surf, color, p, width // 2)
        
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

# --- НОВЫЕ ФУНКЦИИ ---

def draw_line(surf, color, start, end, radius):
    pygame.draw.line(surf, color, start, end, radius * 2)

def flood_fill(surf, x, y, new_color):
    """Обычная заливка через стек (чтобы не было RecursionError)"""
    target_color = surf.get_at((x, y))
    if target_color == new_color: return
    
    w, h = surf.get_size()
    pixels = [(x, y)]
    
    while pixels:
        curr_x, curr_y = pixels.pop()
        if surf.get_at((curr_x, curr_y)) != target_color:
            continue
        
        surf.set_at((curr_x, curr_y), new_color)
        
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = curr_x + dx, curr_y + dy
            if 0 <= nx < w and 0 <= ny < h:
                pixels.append((nx, ny))

def save_canvas(surf):
    # Папка saves рядом с файлом скрипта
    base_dir = os.path.dirname(os.path.abspath(__file__))
    saves_dir = os.path.join(base_dir, "saves")
    
    # Создаём папку если её нет
    os.makedirs(saves_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(saves_dir, f"paint_save_{timestamp}.png")
    pygame.image.save(surf, filename)
    print(f"Saved as {filename}")