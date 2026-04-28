import pygame
import sys
import os
import random
from pygame.locals import *

from racer import Player, Enemy, Coin, PowerUp, Obstacle, RoadObject, LANES
from ui import main_menu, game_over_screen, leaderboard_screen, username_input, settings_screen
from persistence import load_settings, save_score
import constants

# ── Пути ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMG_DIR    = os.path.join(ASSETS_DIR, "images")
SND_DIR    = os.path.join(ASSETS_DIR, "sounds")

# ── Difficulty presets ───────────────────────────────────────────────────────
DIFF = {
    "easy":   {"speed": 3,  "inc": 0.05},
    "normal": {"speed": 5,  "inc": 0.10},
    "hard":   {"speed": 8,  "inc": 0.18},
}

# ── Динамический спавн ───────────────────────────────────────────────────────
# Лимиты объектов на экране одновременно
MAX_ENEMIES   = 2   # врагов (растёт до 3 после уровня 50)
MAX_OBSTACLES = 1   # препятствий всегда не больше 1
MAX_COINS     = 2   # монет

SPAWN_CHANCE = 0.02

def get_max_enemies(level):
    """До уровня 50 — максимум 2 врага, после — 3."""
    return 3 if level >= 50 else 2

def _free_lane(enemy_group, obstacle_group):
    """
    Возвращает True если хотя бы одна полоса из LANES
    не занята объектом в нижней половине экрана (y > 200).
    Это гарантирует игроку всегда есть куда свернуть.
    """
    occupied = set()
    for obj in list(enemy_group) + list(obstacle_group):
        if obj.rect.top > 200:   # объект уже виден на экране
            for lane in LANES:
                if abs(obj.rect.centerx - lane) < 60:
                    occupied.add(lane)
    return len(occupied) < len(LANES)   # хоть одна полоса свободна

def update_spawn(level, enemy_group, obstacle_group, all_sprites, player):
    max_enemies = get_max_enemies(level)

    # Проверяем лимиты отдельно для врагов и препятствий
    can_spawn_enemy    = len(enemy_group)    < max_enemies
    can_spawn_obstacle = len(obstacle_group) < MAX_OBSTACLES

    if not (can_spawn_enemy or can_spawn_obstacle):
        return
    if not random.random() < SPAWN_CHANCE:
        return

    # Не спавним если все полосы заняты в нижней части экрана
    if not _free_lane(enemy_group, obstacle_group):
        return

    if can_spawn_enemy and (not can_spawn_obstacle or random.random() < 0.6):
        e = Enemy(player_rect=player.rect)
        enemy_group.add(e); all_sprites.add(e)
    elif can_spawn_obstacle:
        o = Obstacle(player_rect=player.rect)
        obstacle_group.add(o); all_sprites.add(o)

# ── Инициализация ────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

icon_path = os.path.join(IMG_DIR, "icon.png")
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path).convert_alpha()
    icon = pygame.transform.scale(icon, (64, 64))
    pygame.display.set_icon(icon)

clock = pygame.time.Clock()

ROAD_EVENT    = USEREVENT + 3
INC_SPEED     = USEREVENT + 1
SPAWN_POWERUP = USEREVENT + 2
pygame.time.set_timer(ROAD_EVENT,    15000)
pygame.time.set_timer(INC_SPEED,      1000)
pygame.time.set_timer(SPAWN_POWERUP,  7000)

# ── Основной игровой цикл ────────────────────────────────────────────────────
def run_game(settings):
    # Очищаем реестр от прошлой игры
    RoadObject.clear_registry()

    d = DIFF[settings.get("difficulty", "normal")]
    constants.SPEED = d["speed"]

    bg   = pygame.image.load(os.path.join(IMG_DIR, "AnimatedStreet.png")).convert()
    bg_y = 0

    music_path = os.path.join(SND_DIR, "background.mp3")
    if settings.get("sound") and os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    # ── Спрайты ─────────────────────────────────────────────────────────────
    player         = Player(car_color=settings.get("car_color", "yellow"))
    all_sprites    = pygame.sprite.Group()
    enemy_group    = pygame.sprite.Group()
    coin_group     = pygame.sprite.Group()
    powerup_group  = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()

    all_sprites.add(player)

    # Старт: 1 встречная + 1 попутная + 1 препятствие
    for kind in ['oncoming', 'traffic']:
        e = Enemy(kind=kind, player_rect=player.rect)
        enemy_group.add(e); all_sprites.add(e)

    o = Obstacle(player_rect=player.rect)
    obstacle_group.add(o); all_sprites.add(o)

    for _ in range(2):
        c = Coin(player.rect)
        coin_group.add(c); all_sprites.add(c)

    # ── Счётчики ────────────────────────────────────────────────────────────
    score    = 0
    coins    = 0
    distance = 0

    font   = pygame.font.SysFont("Verdana", 16)
    font_b = pygame.font.SysFont("Verdana", 14, bold=True)

    running = True
    while running:
        dt = clock.tick(constants.FPS) / 1000.0

        # ── События ─────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()

            if event.type == INC_SPEED:
                constants.SPEED += d["inc"]

            if event.type == SPAWN_POWERUP:
                if len(powerup_group) == 0:
                    pu = PowerUp(player_rect=player.rect)
                    powerup_group.add(pu); all_sprites.add(pu)

            if event.type == ROAD_EVENT:
                # Перекрываем случайную полосу тремя барьерами подряд
                blocked = random.choice(LANES)
                for i in range(3):
                    if random.random() < 0.5:
                        o = Obstacle(player_rect=player.rect,
                                    lane=blocked, offset_y=-60 - i * 120)
                        obstacle_group.add(o); all_sprites.add(o)

        # ── Обновление ────────────────────────────────────────────────────
        player.update_timers(dt)
        player.move()

        for e in enemy_group:     e.move()
        for c in coin_group:      c.move()
        for o in obstacle_group:  o.move()
        for pu in list(powerup_group):
            pu.move(dt)

        distance += int(constants.SPEED)
        score    += int(constants.SPEED * 0.1)

        level = coins * 2 + (distance // 100)
        update_spawn(level, enemy_group, obstacle_group, all_sprites, player)

        # ── Коллизии ────────────────────────────────────────────────────────
        for c in pygame.sprite.spritecollide(player, coin_group, False):
            coins += c.value
            score += c.value * 10
            c._spawn(player.rect)

        for pu in pygame.sprite.spritecollide(player, powerup_group, True):
            player.apply_powerup(pu.kind)

        if pygame.sprite.spritecollideany(player, enemy_group):
            if player.take_hit():
                running = False

        for obs in pygame.sprite.spritecollide(player, obstacle_group, False):
            if player.take_hit():
                running = False
            obs._spawn(player.rect)

        # ── Фон ─────────────────────────────────────────────────────────────
        bg_y += int(constants.SPEED)
        if bg_y >= constants.SCREEN_HEIGHT:
            bg_y = 0
        screen.blit(bg, (0, bg_y - constants.SCREEN_HEIGHT))
        screen.blit(bg, (0, bg_y))

        # ── Спрайты ─────────────────────────────────────────────────────────
        for spr in all_sprites:
            if hasattr(spr, 'draw_rect'):
                screen.blit(spr.image, spr.draw_rect)
            else:
                screen.blit(spr.image, spr.rect)

        # ── HUD ─────────────────────────────────────────────────────────────
        for i in range(player.lives):
            pygame.draw.circle(screen, (255, 60, 60), (15 + i * 22, 15), 8)

        for i, line in enumerate([
            f"Score: {score}",
            f"Coins: {coins}",
            f"Dist:  {distance // 100} m",
        ]):
            screen.blit(font.render(line, True, (255, 255, 255)), (10, 30 + i * 20))

        if player.nitro_active:
            screen.blit(font_b.render(f"NITRO  {player.nitro_timer:.1f}s", True, (255, 220, 0)),
                        (constants.SCREEN_WIDTH - 130, 10))
        if player.shield_active:
            screen.blit(font_b.render("SHIELD", True, (0, 200, 255)),
                        (constants.SCREEN_WIDTH - 130, 30))

        if player.invincible_timer > 0 and int(player.invincible_timer * 10) % 2 == 0:
            flash = pygame.Surface(player.draw_rect.size, pygame.SRCALPHA)
            flash.fill((255, 255, 255, 80))
            screen.blit(flash, player.draw_rect)
            

        pygame.display.flip()

    # ── Конец игры ───────────────────────────────────────────────────────────
    pygame.mixer.music.stop()
    crash_path = os.path.join(SND_DIR, "crash.wav")
    if settings.get("sound") and os.path.exists(crash_path):
        pygame.mixer.Sound(crash_path).play()

    return score, distance // 100, coins


# ── Точка входа ──────────────────────────────────────────────────────────────
def main():
    settings = load_settings()

    while True:
        action = main_menu(screen)

        if action == 'quit':
            pygame.quit(); sys.exit()
        elif action == 'settings':
            settings = settings_screen(screen)
        elif action == 'leaderboard':
            leaderboard_screen(screen)
        elif action == 'play':
            name = username_input(screen)
            while True:
                score, distance, coins = run_game(settings)
                choice = game_over_screen(screen, score, distance, coins)
                if choice != 'retry':
                    break
            save_score(name, score, distance, coins)


if __name__ == "__main__":
    main()