# 🎬 ReelBot: Discord Batch Instagram Reels Scheduler Bot

ReelBot is an automated Discord Bot that lets you upload a batch of video files (Instagram Reels), assign a shared thumbnail and caption, randomly schedule their publishing across specified dates and daily time windows, and automatically post them to your Instagram account via Meta's official Graph API.

---

## 🛠️ Features

- **Discord Slash Wizard (`/batch`)**: Interactive step-by-step workflow with dedicated thread collection.
- **Thread Video Collection**: Automatically downloads `.mp4` / `.mov` video files dropped into the batch thread.
- **Shared Assets**: Assigns a single cover thumbnail image and caption across all Reels in the batch.
- **Randomized Anti-Bot Scheduling**: Distributes post publication times randomly within daily time windows and enforces minimum time gaps to avoid repetitive bot patterns.
- **SQLite Database Persistence**: Full async persistence using `aiosqlite` for batch status tracking and scheduled post queues.
- **Automated Background Scheduler**: Polling loop runs every minute to publish due Reels and posts live updates back to the Discord thread.
- **Meta Instagram Graph API Support**: Official API route for safe, reliable posting (with dry-run test mode fallback).

---

## 📂 Project Structure

```
reelbot/
├── bot.py                # Main Discord Bot (slash commands + thread listener + scheduler loop)
├── db.py                 # SQLite schema & asynchronous database management
├── scheduling.py         # Randomized posting schedule generator algorithm
├── instagram_poster.py   # Meta Instagram Graph API publisher (with dry-run mode)
├── requirements.txt      # Python dependencies
└── .env.example          # Environment variables template
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Setup
Clone or navigate to the project directory and install dependencies:

```bash
cd reelbot
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and fill in your tokens:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DISCORD_TOKEN=your_discord_bot_token_here
INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id
INSTAGRAM_ACCESS_TOKEN=your_graph_api_access_token
```

> **Note on Dry-Run Mode**: If `INSTAGRAM_ACCOUNT_ID` or `INSTAGRAM_ACCESS_TOKEN` are omitted, ReelBot automatically runs in **Simulated Dry-Run Mode**. It will log the mock posting actions to Discord and terminal without making live Instagram API calls, perfect for testing the Discord workflow.

---

## 🤖 Discord Bot Setup & Intents

1. Go to [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a **New Application** and add a **Bot**.
3. Under the **Bot** tab:
   - Enable **Message Content Intent** (Required to detect video/image attachments in batch threads).
   - Copy your bot token into `.env` under `DISCORD_TOKEN`.
4. Under **OAuth2 -> URL Generator**:
   - Select scopes: `bot`, `applications.commands`
   - Select permissions: `Send Messages`, `Create Public Threads`, `Send Messages in Threads`, `Add Reactions`, `Attach Files`, `Read Message History`
   - Use the generated link to invite the bot to your Discord server.

---

## 🪄 Discord Slash Command Wizard Walkthrough

| Command | Action |
| :--- | :--- |
| `/batch start` | Starts a new batch session and opens a dedicated Discord public thread for video uploads. |
| *(Upload `.mp4`/`.mov` files)* | Drop your video files directly into the thread. The bot reacts with ✅ for each saved video. |
| `/batch thumbnail` | Prompts you to send **one image file** (`.jpg`, `.png`, `.webp`) in the thread as the cover thumbnail. |
| `/batch caption <text>` | Sets the shared caption text for all reels in the batch. |
| `/batch schedule` | Generates randomized post timestamps based on `start_date`, `end_date`, `window_start`, `window_end`, `min_gap_minutes`, and `posts_per_day_max`. |
| `/batch review` | Previews the current batch details and proposed schedule. |
| `/batch confirm` | Commits the schedule to the database queue for automated posting. |
| `/batch cancel` | Cancels the active batch session. |

---

## 🏃 Running the Bot

Run the main bot script:

```bash
python3 bot.py
```

Once logged in, type `/batch start` in any channel where the bot has thread permissions.
