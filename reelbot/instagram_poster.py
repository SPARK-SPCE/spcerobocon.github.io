"""
instagram_poster.py — Module for posting Reels using the official Meta Instagram Graph API.

Provides:
- post_reel(local_file_path, caption, cover_url=None) -> returns media_id string or mock media_id in dry-run mode.
"""

import os
import asyncio
import logging
from typing import Optional
import aiohttp

logger = logging.getLogger("reelbot.instagram")

# Load configuration from environment variables
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v19.0")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL")


async def post_reel(
    local_file_path: str,
    caption: str,
    cover_url: Optional[str] = None
) -> str:
    """
    Publish a Reel to Instagram via Meta Graph API.
    
    If INSTAGRAM_ACCOUNT_ID and INSTAGRAM_ACCESS_TOKEN are not configured,
    operates in simulated dry-run mode to allow full end-to-end testing of Discord bot workflow.
    """
    if not INSTAGRAM_ACCOUNT_ID or not INSTAGRAM_ACCESS_TOKEN:
        logger.warning(
            "[DRY-RUN MODE] Meta Graph API credentials missing. "
            f"Simulating Instagram Reel post for file: {local_file_path}"
        )
        await asyncio.sleep(2)  # Simulate API network delay
        mock_id = f"mock_ig_reel_{os.urandom(4).hex()}"
        print(f"✅ [Simulated IG Post] File: {local_file_path} | Caption: {caption[:40]}... | Media ID: {mock_id}")
        return mock_id

    # Construct accessible media URL
    if PUBLIC_BASE_URL:
        # Assuming static server hosts media directory
        filename = os.path.basename(local_file_path)
        video_url = f"{PUBLIC_BASE_URL.rstrip('/')}/media/{filename}"
    else:
        # Fallback if local_file_path is already a URL or needs explicit URL configuration
        video_url = local_file_path

    base_graph_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

    async with aiohttp.ClientSession() as session:
        # Step 1: Create Container for Reel
        create_container_url = f"{base_graph_url}/{INSTAGRAM_ACCOUNT_ID}/media"
        payload = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        }
        if cover_url:
            payload["cover_url"] = cover_url

        logger.info(f"Creating Reel container for {local_file_path}...")
        async with session.post(create_container_url, data=payload) as resp:
            data = await resp.json()
            if "id" not in data:
                raise RuntimeError(f"Failed to create Instagram Reels container: {data}")
            container_id = data["id"]

        # Step 2: Poll Container Status until READY
        container_status_url = f"{base_graph_url}/{container_id}"
        params = {
            "fields": "status_code,status",
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        }

        attempts = 0
        max_attempts = 30
        is_ready = False

        while attempts < max_attempts:
            await asyncio.sleep(5)
            attempts += 1
            async with session.get(container_status_url, params=params) as resp:
                status_data = await resp.json()
                code = status_data.get("status_code")
                logger.info(f"Container status ({container_id}): {code}")
                if code == "FINISHED":
                    is_ready = True
                    break
                elif code == "ERROR":
                    raise RuntimeError(f"Container processing error: {status_data}")

        if not is_ready:
            raise TimeoutError(f"Container {container_id} timed out while processing video.")

        # Step 3: Publish Media Container
        publish_url = f"{base_graph_url}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        pub_payload = {
            "creation_id": container_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        }

        async with session.post(publish_url, data=pub_payload) as resp:
            pub_data = await resp.json()
            if "id" not in pub_data:
                raise RuntimeError(f"Failed to publish Instagram Reel: {pub_data}")
            
            media_id = pub_data["id"]
            logger.info(f"Successfully published Reel! Media ID: {media_id}")
            return str(media_id)
