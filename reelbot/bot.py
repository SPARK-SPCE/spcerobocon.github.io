"""
bot.py — Discord bot: /batch slash command wizard + background scheduler loop.

Wizard flow:
    /batch start                -> creates a batch, opens a thread, tells you to drop videos in it
    (drop .mp4/.mov files in the thread — each is auto-added)
    /batch thumbnail            -> attach one image in your next message; sets the shared thumbnail
    /batch caption <text>       -> sets the shared caption
    /batch schedule <...>       -> generates randomized post times (uses scheduling.py)
    /batch review               -> shows the generated schedule before you commit
    /batch confirm              -> locks it in; background loop will post at the scheduled times
    /batch cancel               -> abandons the current batch

Background loop (`scheduler_loop`) polls the DB every minute for due posts
and calls instagram_poster.post_reel() for each.
"""

import os
import asyncio
from datetime import datetime, date, time as dtime
from pathlib import Path
from typing import Dict, List, Tuple

import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

import db
import scheduling
import instagram_poster

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
MEDIA_DIR = Path(__file__).parent / "media"
MEDIA_DIR.mkdir(exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# In-memory tracking:
# active_wizard: user_id -> batch_id
active_wizard: Dict[int, int] = {}

# pending_schedules: batch_id -> list of (video_id, datetime)
pending_schedules: Dict[int, List[Tuple[int, datetime]]] = {}


# ---------- helpers ----------

def is_video(attachment: discord.Attachment) -> bool:
    return attachment.filename.lower().endswith((".mp4", ".mov", ".m4v"))


def is_image(attachment: discord.Attachment) -> bool:
    return attachment.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))


async def save_attachment(attachment: discord.Attachment, batch_id: int) -> str:
    dest_dir = MEDIA_DIR / str(batch_id)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / attachment.filename
    await attachment.save(dest_path)
    return str(dest_path)


def parse_hhmm(s: str) -> dtime:
    s = s.strip()
    parts = s.split(":")
    if len(parts) != 2:
        raise ValueError("Time must be in HH:MM format (e.g. 14:30)")
    return dtime(int(parts[0]), int(parts[1]))


def parse_date(s: str) -> date:
    s = s.strip()
    return datetime.strptime(s, "%Y-%m-%d").date()


# ---------- batch command group ----------

batch_group = app_commands.Group(name="batch", description="Manage a batch of Instagram Reels to schedule")


@batch_group.command(name="start", description="Start a new reel batch (opens a thread to collect videos)")
async def batch_start(interaction: discord.Interaction):
    if not interaction.guild_id or not interaction.channel:
        await interaction.response.send_message("This command must be run inside a server channel.", ephemeral=True)
        return

    existing = await db.get_active_batch_for_user(interaction.guild_id, interaction.user.id)
    if existing:
        await interaction.response.send_message(
            f"You already have an in-progress batch (#{existing['id']}, status: `{existing['status']}`). "
            f"Use `/batch cancel` to abandon it first, or continue where you left off.",
            ephemeral=True,
        )
        return

    await interaction.response.send_message("Starting a new reel batch...", ephemeral=True)

    # Create thread in channel
    channel = interaction.channel
    if hasattr(channel, "create_thread"):
        thread = await channel.create_thread(
            name=f"reel-batch-{interaction.user.display_name}",
            type=discord.ChannelType.public_thread,
        )
    else:
        await interaction.followup.send("Cannot create thread in this channel type.", ephemeral=True)
        return

    batch_id = await db.create_batch(interaction.guild_id, interaction.user.id, thread.id)
    active_wizard[interaction.user.id] = batch_id

    await thread.send(
        f"🎬 {interaction.user.mention} **Batch #{batch_id} Started!**\n\n"
        f"1️⃣ Drop your `.mp4` or `.mov` video files here (one message or several).\n"
        f"2️⃣ When done uploading videos, run `/batch thumbnail` in this channel."
    )


@batch_group.command(name="thumbnail", description="Set the shared thumbnail (attach an image to your next message)")
async def batch_thumbnail(interaction: discord.Interaction):
    batch_id = active_wizard.get(interaction.user.id)
    if not batch_id:
        await interaction.response.send_message("No active batch found. Run `/batch start` first.", ephemeral=True)
        return

    videos = await db.get_videos_for_batch(batch_id)
    if not videos:
        await interaction.response.send_message(
            "⚠️ No videos added yet! Please drop `.mp4` or `.mov` files into the batch thread first.", ephemeral=True
        )
        return

    await db.update_batch_status(batch_id, "awaiting_thumbnail")
    await interaction.response.send_message(
        f"🖼️ Registered {len(videos)} video(s) for Batch #{batch_id}.\n"
        f"Now send **one image** (`.jpg`, `.png`, `.webp`) in this thread to set the thumbnail.",
        ephemeral=False,
    )


@batch_group.command(name="caption", description="Set the shared caption for all reels in this batch")
@app_commands.describe(text="Caption text (used on every reel in this batch)")
async def batch_caption(interaction: discord.Interaction, text: str):
    batch_id = active_wizard.get(interaction.user.id)
    if not batch_id:
        await interaction.response.send_message("No active batch found. Run `/batch start` first.", ephemeral=True)
        return

    batch = await db.get_batch(batch_id)
    if not batch or not batch.get("thumbnail_path"):
        await interaction.response.send_message(
            "⚠️ Set a thumbnail image first with `/batch thumbnail`.", ephemeral=True
        )
        return

    await db.set_batch_caption(batch_id, text)
    await db.update_batch_status(batch_id, "awaiting_schedule")
    await interaction.response.send_message(
        f"📝 Caption saved for Batch #{batch_id} ({len(text)} characters).\n"
        f"Next, run `/batch schedule` to configure publication timing.",
        ephemeral=False,
    )


@batch_group.command(name="schedule", description="Generate a randomized posting schedule")
@app_commands.describe(
    start_date="First publication date (YYYY-MM-DD)",
    end_date="Last publication date (YYYY-MM-DD)",
    window_start="Earliest daily post time (HH:MM 24h format)",
    window_end="Latest daily post time (HH:MM 24h format)",
    min_gap_minutes="Minimum minutes between posts on the same day (default 60)",
    posts_per_day_max="Maximum posts allowed per day (default 3)",
)
async def batch_schedule(
    interaction: discord.Interaction,
    start_date: str,
    end_date: str,
    window_start: str,
    window_end: str,
    min_gap_minutes: int = 60,
    posts_per_day_max: int = 3,
):
    batch_id = active_wizard.get(interaction.user.id)
    if not batch_id:
        await interaction.response.send_message("No active batch found. Run `/batch start` first.", ephemeral=True)
        return

    batch = await db.get_batch(batch_id)
    if not batch or not batch.get("caption"):
        await interaction.response.send_message("⚠️ Set a caption first using `/batch caption`.", ephemeral=True)
        return

    videos = await db.get_videos_for_batch(batch_id)

    try:
        s_date = parse_date(start_date)
        e_date = parse_date(end_date)
        w_start = parse_hhmm(window_start)
        w_end = parse_hhmm(window_end)

        times = scheduling.generate_schedule(
            num_videos=len(videos),
            start_date=s_date,
            end_date=e_date,
            window_start=w_start,
            window_end=w_end,
            min_gap_minutes=min_gap_minutes,
            posts_per_day_max=posts_per_day_max,
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Schedule error: {e}", ephemeral=True)
        return

    pending_schedules[batch_id] = list(zip([v["id"] for v in videos], times))
    await db.update_batch_status(batch_id, "reviewing_schedule")

    lines = "\n".join(
        f"• {v['original_filename']} -> {t.strftime('%Y-%m-%d %H:%M')}"
        for v, (_, t) in zip(videos, pending_schedules[batch_id])
    )

    await interaction.response.send_message(
        f"📅 **Proposed Posting Schedule for Batch #{batch_id} ({len(videos)} Reels):**\n"
        f"```\n{lines}\n```\n"
        f"Run `/batch confirm` to lock it in, or `/batch schedule` with different parameters to regenerate.",
        ephemeral=False,
    )


@batch_group.command(name="review", description="Show current batch details and proposed schedule")
async def batch_review(interaction: discord.Interaction):
    batch_id = active_wizard.get(interaction.user.id)
    if not batch_id:
        await interaction.response.send_message("No active batch found.", ephemeral=True)
        return

    batch = await db.get_batch(batch_id)
    videos = await db.get_videos_for_batch(batch_id)

    cap = batch.get('caption') or 'Not set'
    cap_preview = cap[:80] + '...' if len(cap) > 80 else cap

    lines = [
        f"📊 **Batch #{batch_id} Review**",
        f"• Status: `{batch.get('status')}`",
        f"• Total Videos: {len(videos)}",
        f"• Thumbnail: {'✅ Set' if batch.get('thumbnail_path') else '❌ Not set'}",
        f"• Caption: {cap_preview}",
    ]

    if batch_id in pending_schedules:
        lines.append("\n**Proposed Schedule:**")
        v_map = {v["id"]: v for v in videos}
        for vid, t in pending_schedules[batch_id]:
            fname = v_map.get(vid, {}).get("original_filename", f"Video #{vid}")
            lines.append(f"  • {fname} -> {t.strftime('%Y-%m-%d %H:%M')}")

    await interaction.response.send_message("\n".join(lines), ephemeral=True)


@batch_group.command(name="confirm", description="Confirm and schedule the batch for posting")
async def batch_confirm(interaction: discord.Interaction):
    batch_id = active_wizard.get(interaction.user.id)
    if not batch_id:
        await interaction.response.send_message("No active batch found.", ephemeral=True)
        return

    schedule = pending_schedules.get(batch_id)
    if not schedule:
        await interaction.response.send_message("⚠️ Run `/batch schedule` first before confirming.", ephemeral=True)
        return

    assignments = [(vid, t.isoformat()) for vid, t in schedule]
    await db.create_scheduled_posts(batch_id, assignments)
    await db.update_batch_status(batch_id, "confirmed")

    # Clean up state
    pending_schedules.pop(batch_id, None)
    active_wizard.pop(interaction.user.id, None)

    await interaction.response.send_message(
        f"🚀 **Batch #{batch_id} Confirmed!**\n"
        f"Successfully scheduled {len(assignments)} Reel post(s). "
        f"The background poster will execute each post automatically and notify this thread.",
        ephemeral=False,
    )


@batch_group.command(name="cancel", description="Cancel and abandon the current in-progress batch")
async def batch_cancel(interaction: discord.Interaction):
    batch_id = active_wizard.get(interaction.user.id)
    if not batch_id:
        await interaction.response.send_message("No active batch found.", ephemeral=True)
        return

    await db.cancel_batch(batch_id)
    pending_schedules.pop(batch_id, None)
    active_wizard.pop(interaction.user.id, None)

    await interaction.response.send_message(f"🚫 Batch #{batch_id} cancelled.", ephemeral=False)


bot.tree.add_command(batch_group)


# ---------- passive file collection in batch threads ----------

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    batch_id = active_wizard.get(message.author.id)
    if batch_id and isinstance(message.channel, discord.Thread):
        batch = await db.get_batch(batch_id)
        if batch and batch.get("thread_id") == message.channel.id:
            status = batch.get("status")

            if status == "collecting":
                added = 0
                for att in message.attachments:
                    if is_video(att):
                        path = await save_attachment(att, batch_id)
                        await db.add_video(batch_id, path, att.filename)
                        added += 1
                if added > 0:
                    await message.add_reaction("✅")

            elif status == "awaiting_thumbnail":
                img_atts = [a for a in message.attachments if is_image(a)]
                if img_atts:
                    path = await save_attachment(img_atts[0], batch_id)
                    await db.set_batch_thumbnail(batch_id, path)
                    await db.update_batch_status(batch_id, "awaiting_caption")
                    await message.reply(
                        "✅ **Thumbnail set!**\n"
                        "Now run `/batch caption <your text here>` to assign the caption."
                    )

    await bot.process_commands(message)


# ---------- background scheduler loop ----------

@tasks.loop(minutes=1)
async def scheduler_loop():
    now_iso = datetime.now().isoformat()
    due_posts = await db.get_due_posts(now_iso)

    for post in due_posts:
        await db.mark_post_status(post["post_id"], "posting")
        try:
            media_id = await instagram_poster.post_reel(
                local_file_path=post["file_path"],
                caption=post["caption"],
            )
            await db.mark_post_status(post["post_id"], "posted", ig_media_id=media_id)
            await notify_thread(
                post,
                f"✨ **Reel Published Successfully!**\n"
                f"• Video: `{post['original_filename']}`\n"
                f"• Instagram Media ID: `{media_id}`"
            )
        except Exception as e:
            await db.mark_post_status(post["post_id"], "failed", error_message=str(e))
            await notify_thread(
                post,
                f"❌ **Failed to Publish Reel** (`{post['original_filename']}`):\n`{e}`"
            )


async def notify_thread(post: dict, text: str):
    thread_id = post.get("thread_id")
    if not thread_id:
        return
    channel = bot.get_channel(thread_id)
    if not channel:
        try:
            channel = await bot.fetch_channel(thread_id)
        except Exception:
            channel = None

    if channel:
        try:
            await channel.send(text)
        except Exception:
            pass


@scheduler_loop.before_loop
async def before_scheduler_loop():
    await bot.wait_until_ready()


# ---------- lifecycle ----------

@bot.event
async def on_ready():
    await db.init_db()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Slash command sync error: {e}")

    if not scheduler_loop.is_running():
        scheduler_loop.start()

    print(f"Logged in as {bot.user} (ID: {bot.user.id}) — reelbot ready.")


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("ERROR: DISCORD_TOKEN environment variable not set. Please update .env before running.")
    else:
        bot.run(DISCORD_TOKEN)
