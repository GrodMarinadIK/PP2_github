# 🏎️ Racer — Not F1

A top-down arcade racing game built with **Pygame** as part of the PP2 course at KBTU.

---

## 🎮 Gameplay

Survive as long as possible on a busy road. Dodge oncoming traffic, avoid road hazards, collect coins, and grab power-ups to stay alive.

- **← →** to steer your car
- Collect coins to boost your score
- Don't run out of lives

---

## 🚗 Traffic System

Two types of enemy vehicles share the road with you:

| Type | Behavior |
|------|----------|
| **Oncoming** | Drives toward you at high speed — react fast |
| **Traffic** | Drives in the same direction, slower than you — weave around it |

Vehicles use a **time-based spawn system**: new cars check whether they would arrive at the same place at the same time as existing ones, preventing pile-ups before they happen.

---

## 🛣️ Road Events

Every 15 seconds a random lane gets blocked by a series of barriers — find a gap or switch lanes in time.

---

## ⭐ Coins

Three tiers of coins spawn on the road:

| Coin | Color | Value |
|------|-------|-------|
| Common | 🟡 Gold | 1 pt |
| Rare | 🟣 Purple | 2 pts |
| Epic | 🔴 Red | 5 pts |

---

## ⚡ Power-Ups

| Power-Up | Letter | Effect |
|----------|--------|--------|
| Nitro | **N** | Speed boost for 4 seconds |
| Shield | **S** | Absorbs one hit |
| Repair | **R** | Restores one life (max 3) |

Only one power-up appears on screen at a time. Uncollected power-ups disappear after 8 seconds.

---

## ⚙️ Settings

Accessible from the main menu:

- **Sound** — toggle background music and crash sound
- **Car color** — choose from Yellow, Red, Blue, Green, Magenta, Turquoise
- **Difficulty** — Easy / Normal / Hard (affects starting speed and rate of acceleration)

Settings are saved to `settings.json` and loaded automatically on startup.

---

## 🏆 Leaderboard

- Enter a 3-letter name before each run
- Top 10 scores are saved to `leaderboard.json`
- Score = coins × 10 + distance bonus
- View the leaderboard from the main menu at any time

---

## 📁 Project Structure

```
TSIS3/
├── main.py          # Game loop, spawn logic, HUD
├── racer.py         # Sprite classes: Player, Enemy, Coin, PowerUp, Obstacle
├── ui.py            # All screens: Menu, Settings, Leaderboard, Game Over
├── persistence.py   # Load/save settings and leaderboard (JSON)
├── constants.py     # Screen size, FPS, speed
├── settings.json    # Saved user preferences
├── leaderboard.json # Top 10 scores
└── assets/
    ├── images/      # Car sprites, coins, road background, oil spill
    └── sounds/      # Background music, crash sound
```

---

## 🚀 How to Run

```bash
pip install pygame
python main.py
```

Requires Python 3.10+ and Pygame 2.x.

---

## 📚 Built With

- [Pygame](https://www.pygame.org/) — game framework
- Python `json` — settings and leaderboard persistence
- Python `os` / `datetime` — file handling

---

*PP2 | KBTU 2025–2026*