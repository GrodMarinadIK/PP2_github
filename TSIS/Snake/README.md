# Snake — Gold Edition (TSIS 4)

## Structure

```
TSIS4/
├── main.py                 # Screen manager: menus, game loop, UI
├── game.py                 # Core gameplay: snake, food, powerups, obstacles
├── db.py                   # PostgreSQL persistence (psycopg2)
├── config.py.example       # All constants and DB credentials
├── settings.py             # settings.json load/save
├── settings.json           # User preferences (auto-created)
└── assets/
    └── background.mp3      (optional)
```

## Setup

### 1. Install dependencies

```bash
pip install pygame psycopg2-binary
```

### 2. Create the database

```sql
CREATE DATABASE snake_db;
```

The tables (`players`, `game_sessions`) are created automatically on first run via `db.init_db()`.

### 3. Configure DB credentials

Edit `config.py.exmaple`:

```python
DB_CONFIG = dict(
    host="localhost",
    port=5432,
    dbname="snake_db",
    user="postgres",
    password="YOUR_PASSWORD",
)
```

### 4. Run

```bash
python main.py
```

---

## Controls

| Key | Action |
|-----|--------|
| Arrow keys / WASD | Move |
| ESC | Quit to main menu (no save) |

---

## Features

### From Practice 10–11
- Wall/border collision → Game Over
- Random food placement — uses free-cell list (no retry loop), avoids snake body, spawns at least 2 cells from head
- Level progression every 5 score points
- Speed increases each level (`base_speed += 1` steps/sec)
- Score and level displayed in HUD
- Weighted food: normal = 1pt, gold = 2pt
- Gold food disappears after 6 s (blinking in last 2 s)

### TSIS 4 — New

#### Leaderboard (PostgreSQL)
- Username entered on startup (3 letters)
- Score + level auto-saved after game over
- Top 10 leaderboard screen with rank, name, score, level, date
- Personal best shown in-game HUD

#### Poison Food (purple circle)
- Appears from level 2, 35% chance every 3 s if none present
- Eating it shortens snake by 2 segments
- If snake length ≤ 1 after eating → Game Over

#### Power-ups (diamond shape)
| Icon | Color | Effect | Duration |
|------|-------|--------|----------|
| S | Orange | Speed ×1.7 | 5 s |
| W | Blue | Speed ×0.5 | 5 s |
| P | Yellow | Shield (absorbs 1 collision) | Until used |

- Max 1 powerup on field at a time
- Disappears after 8 s if not collected (blinks in last 2 s)

#### Obstacles
- Appear from Level 3
- 3 new wall blocks each level-up
- Safe zone: 3-cell radius around snake head guaranteed clear
- Food and powerups never spawn on obstacle cells

#### Settings (settings.json)
- Snake color (5 options)
- Inner grid on/off
- Sound on/off

#### Game Screens
- **Main Menu** — username entry + Play / Leaderboard / Settings / Quit
- **Game Over** — score, level, personal best + Retry / Main Menu
- **Leaderboard** — Top 10 table + Back
- **Settings** — color picker, grid toggle, sound toggle + Save & Back