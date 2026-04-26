"""
db.py – PostgreSQL persistence layer (psycopg2).

Schema:
    players(id, username)
    game_sessions(id, player_id, score, level_reached, played_at)
"""

import datetime

try:
    import psycopg2
    import psycopg2.extras
    _HAS_PG = True
except ImportError:
    _HAS_PG = False

from config import DB_CONFIG


# ──────────────────────────────────────────
# Connection helper
# ──────────────────────────────────────────

def _connect():
    if not _HAS_PG:
        raise RuntimeError("psycopg2 not installed")
    return psycopg2.connect(**DB_CONFIG)


# ──────────────────────────────────────────
# Init
# ──────────────────────────────────────────

def init_db():
    """Create tables if they don't exist. Silent on failure."""
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS players (
                        id       SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    )
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id            SERIAL PRIMARY KEY,
                        player_id     INTEGER REFERENCES players(id),
                        score         INTEGER   NOT NULL,
                        level_reached INTEGER   NOT NULL,
                        played_at     TIMESTAMP DEFAULT NOW()
                    )
                """)
        conn.close()
        return True
    except Exception as e:
        print(f"[DB] init_db failed: {e}")
        return False


# ──────────────────────────────────────────
# Save
# ──────────────────────────────────────────

def save_result(username: str, score: int, level: int) -> bool:
    """
    Upsert player, then insert session.
    Returns True on success.
    """
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                # upsert player
                cur.execute("""
                    INSERT INTO players (username)
                    VALUES (%s)
                    ON CONFLICT (username) DO NOTHING
                """, (username,))
                cur.execute("SELECT id FROM players WHERE username = %s", (username,))
                row = cur.fetchone()
                if row is None:
                    return False
                player_id = row[0]

                # insert session
                cur.execute("""
                    INSERT INTO game_sessions (player_id, score, level_reached)
                    VALUES (%s, %s, %s)
                """, (player_id, score, level))
        conn.close()
        return True
    except Exception as e:
        print(f"[DB] save_result failed: {e}")
        return False


# ──────────────────────────────────────────
# Leaderboard
# ──────────────────────────────────────────

def get_top10():
    """
    Returns list of dicts:
        rank, username, score, level_reached, played_at
    """
    try:
        conn = _connect()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    ROW_NUMBER() OVER (ORDER BY gs.score DESC) AS rank,
                    p.username,
                    gs.score,
                    gs.level_reached,
                    gs.played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT 10
            """)
            rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"[DB] get_top10 failed: {e}")
        return []


def get_personal_best(username: str) -> int | None:
    """Returns the player's highest score, or None if no record."""
    try:
        conn = _connect()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(gs.score)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s
            """, (username,))
            row = cur.fetchone()
        conn.close()
        if row and row[0] is not None:
            return int(row[0])
        return None
    except Exception as e:
        print(f"[DB] get_personal_best failed: {e}")
        return None