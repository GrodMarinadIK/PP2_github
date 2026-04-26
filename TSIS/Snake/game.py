"""
game.py – core Snake gameplay logic + rendering.

Responsibilities:
  • Snake movement, collision detection
  • Food spawning  (normal / gold / poison)
  • Power-up spawning and effects
  • Obstacle placement (Level 3+)
  • HUD rendering inside the arena section
"""

import pygame
import random
from dataclasses import dataclass, field
from typing import Optional

import config as C


# ═══════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════

def cell(px: int, py: int):
    """Convert pixel to cell tuple (col, row)."""
    return (px // C.CELL, py // C.CELL)


def to_px(col: int, row: int):
    """Cell (col, row) → top-left pixel in the ARENA (not window)."""
    return col * C.CELL, row * C.CELL


def all_cells():
    return {(c, r) for c in range(C.COLS) for r in range(C.ROWS)}


def free_cells(occupied: set) -> list:
    """All cells minus occupied ones."""
    return list(all_cells() - occupied)


def random_free(occupied: set, min_dist_from: Optional[tuple] = None, min_dist: int = 2) -> Optional[tuple]:
    """
    Pick a random free cell.
    If min_dist_from is given, skip cells within Chebyshev distance < min_dist.
    Returns None if no free cell exists.
    """
    candidates = free_cells(occupied)
    if min_dist_from is not None:
        hx, hy = min_dist_from
        candidates = [
            c for c in candidates
            if max(abs(c[0] - hx), abs(c[1] - hy)) >= min_dist
        ]
    if not candidates:
        return None
    return random.choice(candidates)


# ═══════════════════════════════════════════
# Data classes
# ═══════════════════════════════════════════

@dataclass
class FoodItem:
    cell: tuple          # (col, row)
    kind: str            # "normal" | "gold" | "poison"
    spawn_ms: int = 0
    lifetime_ms: Optional[int] = None   # None = immortal

    def color(self):
        return {
            "normal": C.C_FOOD,
            "gold":   C.C_GOLD,
            "poison": C.C_POISON,
        }[self.kind]

    def points(self):
        return {"normal": 1, "gold": 2, "poison": 0}[self.kind]

    def is_expired(self, now_ms: int) -> bool:
        if self.lifetime_ms is None:
            return False
        return now_ms - self.spawn_ms > self.lifetime_ms


@dataclass
class PowerUp:
    cell: tuple
    kind: str            # "speed" | "slow" | "shield"
    spawn_ms: int = 0

    def color(self):
        return {
            "speed":  C.C_PU_SPEED,
            "slow":   C.C_PU_SLOW,
            "shield": C.C_PU_SHIELD,
        }[self.kind]

    def is_expired(self, now_ms: int) -> bool:
        return now_ms - self.spawn_ms > C.PU_FIELD_TIME


# ═══════════════════════════════════════════
# Main game state
# ═══════════════════════════════════════════

class SnakeGame:
    """
    Manages all gameplay state.
    Call .update(now_ms) each frame, .handle_key(key) for input.
    .game_over is set True when the player dies.
    """

    def __init__(self, snake_color: list):
        self.snake_color = tuple(snake_color)
        self._reset()

    def _reset(self):
        # Snake: list of (col, row), tail first, head last
        mid_c, mid_r = C.COLS // 2, C.ROWS // 2
        self.body: list[tuple] = [(mid_c, mid_r)]
        self.target_len = 1          # grow to this length at start
        self.direction  = (1, 0)    # (dc, dr)
        self.next_dir   = (1, 0)

        self.score      = 0
        self.level      = 1

        self.game_over  = False
        self.shield_active = False

        # Speed
        self.base_speed   = C.INITIAL_SPEED
        self._step_ms     = 1000 // self.base_speed
        self._last_step   = 0
        self._speed_boost_until = 0   # ms timestamp
        self._slow_until        = 0

        # Items
        self.food_items: list[FoodItem]  = []
        self.powerup: Optional[PowerUp]  = None
        self.obstacles: set              = set()

        # Poison/powerup spawn cooldowns
        self._last_poison_check = 0
        self._last_pu_check     = 0

        # Spawn initial food
        self._spawn_food("normal")

    # ─── Properties ───────────────────────

    @property
    def head(self) -> tuple:
        return self.body[-1]

    def _occupied(self) -> set:
        """All cells that cannot be used for spawning."""
        s = set(self.body) | self.obstacles
        for fi in self.food_items:
            s.add(fi.cell)
        if self.powerup:
            s.add(self.powerup.cell)
        return s

    # ─── Input ────────────────────────────

    def handle_key(self, key):
        dirs = {
            pygame.K_UP:    (0, -1),
            pygame.K_w:     (0, -1),
            pygame.K_DOWN:  (0,  1),
            pygame.K_s:     (0,  1),
            pygame.K_LEFT:  (-1, 0),
            pygame.K_a:     (-1, 0),
            pygame.K_RIGHT: (1,  0),
            pygame.K_d:     (1,  0),
        }
        if key in dirs:
            nd = dirs[key]
            # disallow 180°
            if (nd[0] != -self.direction[0] or nd[1] != -self.direction[1]):
                self.next_dir = nd

    # ─── Update ───────────────────────────

    def update(self, now_ms: int):
        if self.game_over:
            return

        self._expire_items(now_ms)
        self._maybe_spawn_poison(now_ms)
        self._maybe_spawn_powerup(now_ms)

        # Effective speed
        eff_speed = self.base_speed
        if now_ms < self._speed_boost_until:
            eff_speed = int(self.base_speed * 1.7)
        elif now_ms < self._slow_until:
            eff_speed = max(2, int(self.base_speed * 0.5))
        step_ms = 1000 // eff_speed

        if now_ms - self._last_step < step_ms:
            return

        self._last_step = now_ms
        self.direction  = self.next_dir

        dc, dr = self.direction
        hc, hr = self.head
        nc, nr = hc + dc, hr + dr

        # Wall collision
        if not (0 <= nc < C.COLS and 0 <= nr < C.ROWS):
            if self.shield_active:
                self.shield_active = False
                return           # shield absorbs it
            self.game_over = True
            return

        # Obstacle collision
        if (nc, nr) in self.obstacles:
            if self.shield_active:
                self.shield_active = False
                return
            self.game_over = True
            return

        # Self collision
        # The tail tip will vacate this frame only if we're at full length
        tail_tip = self.body[0] if len(self.body) >= self.target_len else None
        if (nc, nr) in set(self.body) and (nc, nr) != tail_tip:
            if self.shield_active:
                self.shield_active = False
                return
            self.game_over = True
            return

        # Move
        self.body.append((nc, nr))
        if len(self.body) > self.target_len:
            self.body.pop(0)

        # Check food
        self._check_food(now_ms)
        self._check_powerup(now_ms)

    # ─── Food ─────────────────────────────

    def _spawn_food(self, kind: str):
        now = pygame.time.get_ticks()
        occ = self._occupied()
        pos = random_free(occ, min_dist_from=self.head, min_dist=2)
        if pos is None:
            pos = random_free(occ)   # fallback: anywhere free
        if pos is None:
            return   # board full, skip
        lifetimes = {
            "normal": None,           # immortal
            "gold":   C.GOLD_LIFETIME,
            "poison": C.POISON_LIFETIME,
        }
        self.food_items.append(FoodItem(
            cell=pos,
            kind=kind,
            spawn_ms=now,
            lifetime_ms=lifetimes[kind],
        ))

    def _expire_items(self, now_ms: int):
        before = len(self.food_items)
        self.food_items = [f for f in self.food_items if not f.is_expired(now_ms)]
        # If normal food expired (it doesn't, but gold/poison can), ensure normal present
        if not any(f.kind == "normal" for f in self.food_items):
            self._spawn_food("normal")
        if self.powerup and self.powerup.is_expired(now_ms):
            self.powerup = None

    def _maybe_spawn_poison(self, now_ms: int):
        if now_ms - self._last_poison_check < 3000:
            return
        self._last_poison_check = now_ms
        has_poison = any(f.kind == "poison" for f in self.food_items)
        if not has_poison and self.level >= 2 and random.random() < 0.35:
            self._spawn_food("poison")

    def _maybe_spawn_powerup(self, now_ms: int):
        if self.powerup is not None:
            return
        if now_ms - self._last_pu_check < 5000:
            return
        self._last_pu_check = now_ms
        if random.random() < 0.3:
            occ = self._occupied()
            pos = random_free(occ, min_dist_from=self.head, min_dist=3)
            if pos:
                kind = random.choice(["speed", "slow", "shield"])
                self.powerup = PowerUp(cell=pos, kind=kind, spawn_ms=now_ms)

    def _check_food(self, now_ms: int):
        head = self.head
        for fi in list(self.food_items):
            if fi.cell != head:
                continue
            self.food_items.remove(fi)
            if fi.kind == "poison":
                # Shield absorbs poison — breaks shield, no other penalty
                if self.shield_active:
                    self.shield_active = False
                    break

                # Steal score (3 pts, clamped to 0)
                stolen = min(self.score, 3)
                self.score -= stolen

                # Shorten snake by the amount of score stolen
                self.target_len = max(1, self.target_len - stolen)
                while len(self.body) > self.target_len:
                    self.body.pop(0)

                # Sync level down after poison penalty
                self._sync_level()

                if self.target_len <= 1 and len(self.body) <= 1:
                    self.game_over = True
                    return
            else:
                pts = fi.points()
                self.score += pts
                self.target_len += pts
                if fi.kind == "normal":
                    # Maybe spawn gold
                    if not any(f.kind == "gold" for f in self.food_items):
                        if random.random() < 0.25:
                            self._spawn_food("gold")
                    self._spawn_food("normal")   # replenish
                self._sync_level()
            break

    def _check_powerup(self, now_ms: int):
        if self.powerup is None:
            return
        if self.powerup.cell != self.head:
            return
        kind = self.powerup.kind
        self.powerup = None
        if kind == "speed":
            self._speed_boost_until = now_ms + C.PU_EFFECT_TIME
        elif kind == "slow":
            self._slow_until = now_ms + C.PU_EFFECT_TIME
        elif kind == "shield":
            self.shield_active = True

    def _sync_level(self):
        """
        Deterministic level from score. No counters, no drift.

        Score ranges and levels:
          Level 1:  0 – 4      (starting level, no lower bound)
          Level 2:  5 – 9
          Level 3:  10 – 14
          ...
          Level N:  (N-1)*5 … (N-1)*5 + 4
          Level 13: 60+        (max)

        Formula:  level = min(MAX_LEVEL, score // FOOD_PER_LEVEL + 1)
        """
        MAX_LEVEL = 13
        new_level = min(MAX_LEVEL, self.score // C.FOOD_PER_LEVEL + 1)

        if new_level > self.level:
            # Level up — add speed and obstacles for each new level
            for lvl in range(self.level + 1, new_level + 1):
                self.base_speed += C.SPEED_PER_LEVEL
                if lvl >= C.OBSTACLE_START:
                    self._place_obstacles()
            self.level = new_level

        elif new_level < self.level:
            # Level down (poison) — remove speed and obstacles for each lost level
            for lvl in range(self.level, new_level, -1):
                self.base_speed = max(C.INITIAL_SPEED,
                                      self.base_speed - C.SPEED_PER_LEVEL)
                if lvl >= C.OBSTACLE_START and self.obstacles:
                    to_remove = set(list(self.obstacles)[:C.OBSTACLES_PER_LEVEL])
                    self.obstacles -= to_remove
            self.level = new_level

    def _place_obstacles(self):
        """Add OBSTACLES_PER_LEVEL new wall blocks, never surrounding head."""
        head = self.head
        # Safety zone: 3-cell radius around head
        safe = {(head[0]+dc, head[1]+dr) for dc in range(-3, 4) for dr in range(-3, 4)}
        candidates = [
            c for c in all_cells()
            if c not in self.obstacles
            and c not in set(self.body)
            and c not in safe
            and not any(f.cell == c for f in self.food_items)
        ]
        random.shuffle(candidates)
        for pos in candidates[:C.OBSTACLES_PER_LEVEL]:
            self.obstacles.add(pos)


# ═══════════════════════════════════════════
# Renderer  (draws the arena section only)
# ═══════════════════════════════════════════

class GameRenderer:
    """
    Draws everything that lives inside (and just above) the arena.
    All drawing uses arena-relative coords then adds SIDE / PANEL_TOP offset.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_hud  = pygame.font.SysFont("bahnschrift", 22)
        self.font_small = pygame.font.SysFont("Verdana", 16)

    # ─── Coordinate helpers ───────────────

    def _cell_rect(self, col: int, row: int) -> pygame.Rect:
        x = C.SIDE  + col * C.CELL
        y = C.PANEL_TOP + row * C.CELL
        return pygame.Rect(x, y, C.CELL, C.CELL)

    # ─── Full frame draw ──────────────────

    def draw(self, game: SnakeGame, personal_best: Optional[int],
             show_grid: bool, now_ms: int, settings: dict):
        s = self.screen

        # Background
        s.fill(C.C_BG)

        # HUD panel
        pygame.draw.rect(s, C.C_PANEL, (0, 0, C.WIN_W, C.PANEL_TOP))
        self._draw_hud(game, personal_best, now_ms)

        # Arena border (always visible)
        arena_rect = pygame.Rect(C.SIDE - 1, C.PANEL_TOP - 1,
                                 C.ARENA_W + 2, C.ARENA_H + 2)
        pygame.draw.rect(s, C.C_BORDER, arena_rect, 2)

        # Inner grid (optional)
        if show_grid:
            self._draw_grid()

        # Game objects
        self._draw_obstacles(game)
        self._draw_food(game, now_ms)
        self._draw_powerup(game, now_ms)
        self._draw_snake(game, settings)

    def _draw_hud(self, game: SnakeGame, pb: Optional[int], now_ms: int):
        s = self.screen
        cx = C.WIN_W // 2

        # Score / level
        txt = self.font_hud.render(
            f"SCORE: {game.score}    LEVEL: {game.level}", True, C.C_TEXT)
        s.blit(txt, txt.get_rect(center=(cx, 22)))

        # Personal best
        pb_str = f"Personal Best: {pb}" if pb is not None else "Personal Best: —"
        pb_surf = self.font_small.render(pb_str, True, C.C_TEXT_DIM)
        s.blit(pb_surf, pb_surf.get_rect(center=(cx, 46)))

        # Active effects (right side)
        effects = []
        if game.shield_active:
            effects.append(("SHIELD", C.C_PU_SHIELD))
        if now_ms < game._speed_boost_until:
            rem = (game._speed_boost_until - now_ms) // 1000 + 1
            effects.append((f"SPEED +{rem}s", C.C_PU_SPEED))
        if now_ms < game._slow_until:
            rem = (game._slow_until - now_ms) // 1000 + 1
            effects.append((f"SLOW  +{rem}s", C.C_PU_SLOW))

        ex = C.WIN_W - 10
        for label, color in effects:
            es = self.font_small.render(label, True, color)
            s.blit(es, es.get_rect(right=ex, centery=30))
            ex -= es.get_width() + 14

    def _draw_grid(self):
        s = self.screen
        for c in range(C.COLS + 1):
            x = C.SIDE + c * C.CELL
            pygame.draw.line(s, C.C_GRID,
                             (x, C.PANEL_TOP),
                             (x, C.PANEL_TOP + C.ARENA_H))
        for r in range(C.ROWS + 1):
            y = C.PANEL_TOP + r * C.CELL
            pygame.draw.line(s, C.C_GRID,
                             (C.SIDE, y),
                             (C.SIDE + C.ARENA_W, y))

    def _draw_obstacles(self, game: SnakeGame):
        for (c, r) in game.obstacles:
            rect = self._cell_rect(c, r)
            pygame.draw.rect(self.screen, C.C_OBSTACLE, rect)
            pygame.draw.rect(self.screen, C.C_BG, rect, 1)

    def _draw_food(self, game: SnakeGame, now_ms: int):
        for fi in game.food_items:
            c, r = fi.cell
            rect = self._cell_rect(c, r)
            color = fi.color()

            # Blink gold in last 2s
            if fi.kind == "gold" and fi.lifetime_ms is not None:
                time_left = fi.lifetime_ms - (now_ms - fi.spawn_ms)
                if time_left < 2000 and (now_ms // 150) % 2 == 0:
                    continue   # skip drawing → blink

            # Poison: pulsing opacity effect (just alternate brightness)
            if fi.kind == "poison":
                if (now_ms // 200) % 2 == 0:
                    color = tuple(min(255, v + 40) for v in color)

            # Draw as circle inside cell
            cx = rect.centerx
            cy = rect.centery
            r_px = C.CELL // 2 - 2
            pygame.draw.circle(self.screen, color, (cx, cy), r_px)

    def _draw_powerup(self, game: SnakeGame, now_ms: int):
        pu = game.powerup
        if pu is None:
            return
        c, r = pu.cell
        rect = self._cell_rect(c, r)
        color = pu.color()
        # Blink in last 2s
        time_left = C.PU_FIELD_TIME - (now_ms - pu.spawn_ms)
        if time_left < 2000 and (now_ms // 150) % 2 == 0:
            return
        # Draw as diamond
        cx, cy = rect.centerx, rect.centery
        half = C.CELL // 2 - 1
        pts = [(cx, cy - half), (cx + half, cy), (cx, cy + half), (cx - half, cy)]
        pygame.draw.polygon(self.screen, color, pts)
        pygame.draw.polygon(self.screen, C.C_BG, pts, 1)

        # Label (S/W/P)
        labels = {"speed": "S", "slow": "W", "shield": "P"}
        lbl = self.font_small.render(labels[pu.kind], True, C.C_BG)
        self.screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

    def _draw_snake(self, game: SnakeGame, settings: dict):
        s = self.screen
        body = game.body
        n = len(body)
        base_color = tuple(settings.get("snake_color", [0, 200, 80]))

        for i, (c, r) in enumerate(body):
            rect = self._cell_rect(c, r)
            is_head = (i == n - 1)

            if is_head:
                color = C.C_SNAKE_HEAD
                # Shield glow
                if game.shield_active:
                    glow = rect.inflate(4, 4)
                    pygame.draw.rect(s, C.C_PU_SHIELD, glow, 2)
            else:
                # Gradient: dimmer towards tail
                t = i / max(1, n - 1)
                factor = 0.4 + 0.6 * t
                color = tuple(int(v * factor) for v in base_color)

            pygame.draw.rect(s, color, rect)

            if is_head:
                # Eyes
                d = game.direction
                eye_off = [(4, 4), (12, 4)] if d != (0, -1) else [(4, 4), (12, 4)]
                # Rotate eye positions based on direction
                if d == (1, 0):    offsets = [(12, 4), (12, 12)]
                elif d == (-1, 0): offsets = [(4, 4),  (4, 12)]
                elif d == (0, -1): offsets = [(4, 4),  (12, 4)]
                else:              offsets = [(4, 12), (12, 12)]
                for ox, oy in offsets:
                    pygame.draw.rect(s, C.C_BG,
                                     (rect.x + ox, rect.y + oy, 3, 3))
            else:
                # Subtle cell border
                pygame.draw.rect(s, C.C_BG, rect, 1)