"""
main.py – entry point and screen manager.

Screens:
  main_menu()
  game_screen(username)
  game_over_screen(username, score, level, personal_best)
  leaderboard_screen()
  settings_screen()
"""

import pygame
import sys
import os

import config as C
import settings as S
from game import SnakeGame, GameRenderer
import db


# ═══════════════════════════════════════════
# Init
# ═══════════════════════════════════════════

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((C.WIN_W, C.WIN_H))
pygame.display.set_caption("Snake — Gold Edition")
clock = pygame.time.Clock()

# Fonts
F_TITLE  = pygame.font.SysFont("bahnschrift", 52, bold=True)
F_MENU   = pygame.font.SysFont("bahnschrift", 30)
F_SMALL  = pygame.font.SysFont("Verdana", 18)
F_TINY   = pygame.font.SysFont("Verdana", 14)
F_INPUT  = pygame.font.SysFont("bahnschrift", 56, bold=True)


file_path = os.path.dirname(__file__)
assets_path = os.path.join(file_path, "assets")

icon = pygame.image.load(os.path.join(assets_path, "icon.png"))
pygame.display.set_icon(icon)
# Music
def _try_music():
    try:
        pygame.mixer.music.load(os.path.join(assets_path, "background.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.15)
    except Exception:
        pass

_try_music()


# ═══════════════════════════════════════════
# UI primitives
# ═══════════════════════════════════════════

def _apply_sound(cfg: dict):
    vol = 0.15 if cfg.get("sound", True) else 0.0
    pygame.mixer.music.set_volume(vol)


def _draw_bg(color=C.C_BG):
    screen.fill(color)


def _centered_text(surf: pygame.Surface, text: str, font, color, cy: int):
    s = font.render(text, True, color)
    screen.blit(s, s.get_rect(center=(C.WIN_W // 2, cy)))
    return s.get_height()


class Button:
    PAD_X, PAD_Y = 36, 10

    def __init__(self, label: str, cx: int, cy: int,
                 color=C.C_ACCENT, text_color=C.C_BG):
        self.label = label
        self.color = color
        self.text_color = text_color
        surf = F_MENU.render(label, True, text_color)
        self.rect = surf.get_rect(center=(cx, cy))
        self.rect.inflate_ip(self.PAD_X * 2, self.PAD_Y * 2)
        self._surf = surf

    def draw(self, hovered=False):
        col = tuple(min(255, v + 30) for v in self.color) if hovered else self.color
        pygame.draw.rect(screen, col, self.rect, border_radius=8)
        pygame.draw.rect(screen, C.C_BORDER, self.rect, 2, border_radius=8)
        screen.blit(self._surf, self._surf.get_rect(center=self.rect.center))

    def is_hovered(self, pos) -> bool:
        return self.rect.collidepoint(pos)

    def clicked(self, pos, event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(pos))


def _make_buttons(labels: list[str], start_y: int, gap: int = 58) -> list[Button]:
    cx = C.WIN_W // 2
    return [Button(lbl, cx, start_y + i * gap) for i, lbl in enumerate(labels)]


# ═══════════════════════════════════════════
# Username input
# ═══════════════════════════════════════════

def _username_input(prompt: str = "ENTER YOUR NAME (3 LETTERS)") -> str:
    """Blocking input loop. Returns 3-letter uppercase name."""
    name = ""
    cursor_visible = True
    cursor_timer = 0

    while True:
        now = pygame.time.get_ticks()
        if now - cursor_timer > 500:
            cursor_visible = not cursor_visible
            cursor_timer = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) == 3:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 3 and event.unicode.isalpha():
                    name += event.unicode.upper()

        _draw_bg()
        _centered_text(screen, "SNAKE", F_TITLE, C.C_ACCENT, C.WIN_H // 2 - 120)
        _centered_text(screen, prompt, F_SMALL, C.C_TEXT_DIM, C.WIN_H // 2 - 50)

        # Name display with cursor
        display = name + ("|" if cursor_visible else " ")
        _centered_text(screen, display, F_INPUT, C.C_TEXT, C.WIN_H // 2 + 20)

        hint = F_TINY.render("Press ENTER to confirm", True, C.C_TEXT_DIM)
        screen.blit(hint, hint.get_rect(center=(C.WIN_W // 2, C.WIN_H // 2 + 100)))

        pygame.display.flip()
        clock.tick(C.FPS)


# ═══════════════════════════════════════════
# Main Menu
# ═══════════════════════════════════════════

def main_menu() -> str:
    """Returns chosen username."""
    username = _username_input()

    btns = _make_buttons(["PLAY", "LEADERBOARD", "SETTINGS", "QUIT"],
                         start_y=C.WIN_H // 2 - 60)

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btns[0].clicked(pos, event):
                return username
            if btns[1].clicked(pos, event):
                leaderboard_screen()
            if btns[2].clicked(pos, event):
                settings_screen()
            if btns[3].clicked(pos, event):
                pygame.quit(); sys.exit()

        _draw_bg()
        _centered_text(screen, "SNAKE", F_TITLE, C.C_ACCENT, C.WIN_H // 2 - 160)
        _centered_text(screen, f"Welcome, {username}!", F_SMALL, C.C_TEXT_DIM,
                       C.WIN_H // 2 - 100)

        for btn in btns:
            btn.draw(hovered=btn.is_hovered(pos))

        pygame.display.flip()
        clock.tick(C.FPS)


# ═══════════════════════════════════════════
# Game Screen
# ═══════════════════════════════════════════

def game_screen(username: str):
    cfg = S.load()
    _apply_sound(cfg)

    personal_best = db.get_personal_best(username)
    game  = SnakeGame(snake_color=cfg.get("snake_color", [0, 200, 80]))
    rend  = GameRenderer(screen)

    while not game.game_over:
        now_ms = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return    # back to menu without saving
                game.handle_key(event.key)

        game.update(now_ms)
        rend.draw(game, personal_best, cfg.get("grid", True), now_ms, cfg)
        pygame.display.flip()
        clock.tick(C.FPS)

    # Auto-save
    db.save_result(username, game.score, game.level)
    new_pb = db.get_personal_best(username)

    game_over_screen(username, game.score, game.level, new_pb)


# ═══════════════════════════════════════════
# Game Over Screen
# ═══════════════════════════════════════════

def game_over_screen(username: str, score: int, level: int,
                     personal_best: int | None):
    btns = _make_buttons(["RETRY", "MAIN MENU"], start_y=C.WIN_H // 2 + 60)

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btns[0].clicked(pos, event):
                game_screen(username)
                return
            if btns[1].clicked(pos, event):
                return    # back to main_menu loop

        _draw_bg()
        _centered_text(screen, "GAME OVER", F_TITLE,
                       (220, 60, 70), C.WIN_H // 2 - 140)
        _centered_text(screen, username, F_MENU, C.C_TEXT_DIM,
                       C.WIN_H // 2 - 75)
        _centered_text(screen, f"Score: {score}    Level: {level}",
                       F_MENU, C.C_TEXT, C.WIN_H // 2 - 30)
        pb_str = f"Personal Best: {personal_best}" if personal_best else "Personal Best: —"
        _centered_text(screen, pb_str, F_SMALL, C.C_ACCENT, C.WIN_H // 2 + 12)

        for btn in btns:
            btn.draw(hovered=btn.is_hovered(pos))

        pygame.display.flip()
        clock.tick(C.FPS)


# ═══════════════════════════════════════════
# Leaderboard Screen
# ═══════════════════════════════════════════

def leaderboard_screen():
    rows = db.get_top10()
    btn_back = Button("BACK", C.WIN_W // 2, C.WIN_H - 50,
                      color=C.C_PANEL, text_color=C.C_TEXT)

    col_positions = [40, 110, 230, 320, 420]   # rank, name, score, level, date

    while True:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_back.clicked(pos, event):
                return

        _draw_bg()
        _centered_text(screen, "LEADERBOARD", F_TITLE, C.C_ACCENT, 55)

        # Header
        headers = ["#", "NAME", "SCORE", "LEVEL", "DATE"]
        for hdr, x in zip(headers, col_positions):
            s = F_SMALL.render(hdr, True, C.C_TEXT_DIM)
            screen.blit(s, (x, 110))
        pygame.draw.line(screen, C.C_BORDER, (30, 132), (C.WIN_W - 30, 132), 1)

        # Rows
        if not rows:
            _centered_text(screen, "No records yet", F_SMALL, C.C_TEXT_DIM, 200)
        for i, row in enumerate(rows):
            y = 145 + i * 34
            color = C.C_ACCENT if i == 0 else C.C_TEXT
            values = [
                str(row["rank"]),
                row["username"],
                str(row["score"]),
                str(row["level_reached"]),
                str(row["played_at"])[:10],
            ]
            for val, x in zip(values, col_positions):
                s = F_SMALL.render(val, True, color)
                screen.blit(s, (x, y))

        btn_back.draw(hovered=btn_back.is_hovered(pos))
        pygame.display.flip()
        clock.tick(C.FPS)


# ═══════════════════════════════════════════
# Settings Screen
# ═══════════════════════════════════════════

def settings_screen():
    cfg = S.load()

    COLOR_OPTIONS = [
        ([0, 200, 80],   "Green"),
        ([0, 180, 220],  "Cyan"),
        ([200, 80, 200], "Purple"),
        ([220, 140, 0],  "Orange"),
        ([200, 200, 60], "Yellow"),
    ]

    def _color_index():
        cur = cfg.get("snake_color", [0, 200, 80])
        for i, (rgb, _) in enumerate(COLOR_OPTIONS):
            if rgb == cur:
                return i
        return 0

    color_idx = _color_index()

    btn_save = Button("SAVE & BACK", C.WIN_W // 2, C.WIN_H - 60)

    CX = C.WIN_W // 2

    while True:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Grid toggle
                grid_rect = pygame.Rect(CX - 80, 200, 160, 36)
                if grid_rect.collidepoint(pos):
                    cfg["grid"] = not cfg["grid"]

                # Sound toggle
                sound_rect = pygame.Rect(CX - 80, 270, 160, 36)
                if sound_rect.collidepoint(pos):
                    cfg["sound"] = not cfg["sound"]
                    _apply_sound(cfg)

                # Color left/right
                left_rect  = pygame.Rect(CX - 130, 355, 36, 36)
                right_rect = pygame.Rect(CX + 94, 355, 36, 36)
                if left_rect.collidepoint(pos):
                    color_idx = (color_idx - 1) % len(COLOR_OPTIONS)
                    cfg["snake_color"] = COLOR_OPTIONS[color_idx][0]
                if right_rect.collidepoint(pos):
                    color_idx = (color_idx + 1) % len(COLOR_OPTIONS)
                    cfg["snake_color"] = COLOR_OPTIONS[color_idx][0]

            if btn_save.clicked(pos, event):
                S.save(cfg)
                return

        _draw_bg()
        _centered_text(screen, "SETTINGS", F_TITLE, C.C_ACCENT, 60)

        def _toggle(label, value, y):
            _centered_text(screen, label, F_MENU, C.C_TEXT, y - 18)
            col = C.C_ACCENT if value else (100, 100, 120)
            r = pygame.Rect(CX - 80, y, 160, 36)
            pygame.draw.rect(screen, col, r, border_radius=6)
            txt = F_SMALL.render("ON" if value else "OFF", True, C.C_BG)
            screen.blit(txt, txt.get_rect(center=r.center))

        _toggle("Inner Grid", cfg.get("grid", True), 200)
        _toggle("Sound", cfg.get("sound", True), 270)

        # Color picker
        _centered_text(screen, "Trail Color", F_MENU, C.C_TEXT, 330)
        rgb, name = COLOR_OPTIONS[color_idx]
        swatch_rect = pygame.Rect(CX - 90, 355, 180, 36)
        pygame.draw.rect(screen, rgb, swatch_rect, border_radius=6)
        pygame.draw.rect(screen, C.C_BORDER, swatch_rect, 2, border_radius=6)
        clr_txt = F_SMALL.render(name, True,
                                  (0, 0, 0) if sum(rgb) > 400 else (255, 255, 255))
        screen.blit(clr_txt, clr_txt.get_rect(center=swatch_rect.center))

        # Arrow buttons
        for arrow, rx in [("<", CX - 130), (">", CX + 94)]:
            r = pygame.Rect(rx, 355, 36, 36)
            pygame.draw.rect(screen, C.C_PANEL, r, border_radius=6)
            pygame.draw.rect(screen, C.C_BORDER, r, 2, border_radius=6)
            a = F_MENU.render(arrow, True, C.C_TEXT)
            screen.blit(a, a.get_rect(center=r.center))

        btn_save.draw(hovered=btn_save.is_hovered(pos))
        pygame.display.flip()
        clock.tick(C.FPS)


# ═══════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════

def main():
    db.init_db()
    while True:
        username = main_menu()
        game_screen(username)


if __name__ == "__main__":
    main()