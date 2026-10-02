"""
db.py — SQLite schema and async database functions for batches, videos, and scheduled posts.
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
import aiosqlite

DB_PATH = Path(__file__).parent / "reelbot.db"


async def init_db(db_path: Path = DB_PATH) -> None:
    """Initialize database tables if they do not exist."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS batches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                thread_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'collecting',
                thumbnail_path TEXT,
                caption TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE CASCADE
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id INTEGER NOT NULL,
                video_id INTEGER NOT NULL,
                scheduled_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                ig_media_id TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (batch_id) REFERENCES batches (id) ON DELETE CASCADE,
                FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE
            )
        """)
        await db.commit()


async def create_batch(guild_id: int, user_id: int, thread_id: int, db_path: Path = DB_PATH) -> int:
    """Create a new batch in collecting state."""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(
            """
            INSERT INTO batches (guild_id, user_id, thread_id, status)
            VALUES (?, ?, ?, 'collecting')
            """,
            (guild_id, user_id, thread_id),
        )
        await db.commit()
        return cursor.lastrowid


async def get_batch(batch_id: int, db_path: Path = DB_PATH) -> Optional[Dict[str, Any]]:
    """Fetch batch details by ID."""
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM batches WHERE id = ?", (batch_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def get_active_batch_for_user(guild_id: int, user_id: int, db_path: Path = DB_PATH) -> Optional[Dict[str, Any]]:
    """Get active in-progress batch for user in guild (not confirmed or cancelled)."""
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
            SELECT * FROM batches
            WHERE guild_id = ? AND user_id = ? AND status NOT IN ('confirmed', 'cancelled')
            ORDER BY id DESC LIMIT 1
            """,
            (guild_id, user_id),
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def update_batch_status(batch_id: int, status: str, db_path: Path = DB_PATH) -> None:
    """Update batch status."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE batches SET status = ? WHERE id = ?", (status, batch_id))
        await db.commit()


async def set_batch_thumbnail(batch_id: int, thumbnail_path: str, db_path: Path = DB_PATH) -> None:
    """Set the thumbnail path for a batch."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "UPDATE batches SET thumbnail_path = ? WHERE id = ?",
            (thumbnail_path, batch_id),
        )
        await db.commit()


async def set_batch_caption(batch_id: int, caption: str, db_path: Path = DB_PATH) -> None:
    """Set the caption for a batch."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "UPDATE batches SET caption = ? WHERE id = ?",
            (caption, batch_id),
        )
        await db.commit()


async def cancel_batch(batch_id: int, db_path: Path = DB_PATH) -> None:
    """Mark a batch as cancelled."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute("UPDATE batches SET status = 'cancelled' WHERE id = ?", (batch_id,))
        await db.execute("UPDATE scheduled_posts SET status = 'cancelled' WHERE batch_id = ? AND status = 'pending'", (batch_id,))
        await db.commit()


async def add_video(batch_id: int, file_path: str, original_filename: str, db_path: Path = DB_PATH) -> int:
    """Add a video entry to a batch."""
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(
            """
            INSERT INTO videos (batch_id, file_path, original_filename)
            VALUES (?, ?, ?)
            """,
            (batch_id, file_path, original_filename),
        )
        await db.commit()
        return cursor.lastrowid


async def get_videos_for_batch(batch_id: int, db_path: Path = DB_PATH) -> List[Dict[str, Any]]:
    """Retrieve all videos attached to a batch."""
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM videos WHERE batch_id = ? ORDER BY id ASC", (batch_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def create_scheduled_posts(
    batch_id: int,
    assignments: List[tuple],
    db_path: Path = DB_PATH
) -> None:
    """
    Create scheduled post entries.
    assignments is a list of (video_id, scheduled_time_iso_string)
    """
    async with aiosqlite.connect(db_path) as db:
        for video_id, sched_time in assignments:
            await db.execute(
                """
                INSERT INTO scheduled_posts (batch_id, video_id, scheduled_time, status)
                VALUES (?, ?, ?, 'pending')
                """,
                (batch_id, video_id, sched_time),
            )
        await db.commit()


async def get_due_posts(now_iso: str, db_path: Path = DB_PATH) -> List[Dict[str, Any]]:
    """Get all pending posts whose scheduled_time <= now_iso."""
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        query = """
            SELECT
                p.id as post_id,
                p.batch_id,
                p.video_id,
                p.scheduled_time,
                p.status as post_status,
                v.file_path,
                v.original_filename,
                b.thumbnail_path,
                b.caption,
                b.thread_id,
                b.guild_id
            FROM scheduled_posts p
            JOIN videos v ON p.video_id = v.id
            JOIN batches b ON p.batch_id = b.id
            WHERE p.status = 'pending' AND p.scheduled_time <= ?
            ORDER BY p.scheduled_time ASC
        """
        async with db.execute(query, (now_iso,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def mark_post_status(
    post_id: int,
    status: str,
    ig_media_id: Optional[str] = None,
    error_message: Optional[str] = None,
    db_path: Path = DB_PATH
) -> None:
    """Update execution status for a scheduled post."""
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            """
            UPDATE scheduled_posts
            SET status = ?, ig_media_id = ?, error_message = ?
            WHERE id = ?
            """,
            (status, ig_media_id, error_message, post_id),
        )
        await db.commit()
