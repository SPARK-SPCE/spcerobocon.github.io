"""
scheduling.py — Randomized scheduling algorithm for Instagram Reels batch posting.
"""

import random
from datetime import datetime, date, time as dtime, timedelta
from typing import List


def generate_schedule(
    num_videos: int,
    start_date: date,
    end_date: date,
    window_start: dtime,
    window_end: dtime,
    min_gap_minutes: int = 60,
    posts_per_day_max: int = 3,
) -> List[datetime]:
    """
    Generates a list of randomized datetime objects for `num_videos` posts.
    
    Parameters:
    - num_videos: total number of videos to schedule
    - start_date: starting date (inclusive)
    - end_date: ending date (inclusive)
    - window_start: earliest time of day allowed (e.g., 09:00)
    - window_end: latest time of day allowed (e.g., 21:00)
    - min_gap_minutes: minimum gap between posts on the same day
    - posts_per_day_max: max posts allowed in a single day
    """
    if num_videos <= 0:
        raise ValueError("Number of videos must be at least 1.")

    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date.")

    # Calculate total days in range
    days_count = (end_date - start_date).days + 1

    # Check max total capacity
    max_possible_posts = days_count * posts_per_day_max
    if num_videos > max_possible_posts:
        raise ValueError(
            f"Cannot schedule {num_videos} videos across {days_count} day(s) with max {posts_per_day_max} post(s)/day. "
            f"Maximum capacity is {max_possible_posts}."
        )

    # Convert window times to minute offsets from midnight
    win_start_min = window_start.hour * 60 + window_start.minute
    win_end_min = window_end.hour * 60 + window_end.minute

    if win_end_min <= win_start_min:
        raise ValueError("window_end time must be strictly after window_start time.")

    window_duration_min = win_end_min - win_start_min

    # Ensure min_gap fit within window for posts_per_day_max
    # For k posts in a day, minimum required window is (k-1) * min_gap_minutes
    # Let's check max posts per day that can fit in window_duration_min with min_gap_minutes
    max_fit_in_window = 1 + (window_duration_min // min_gap_minutes) if min_gap_minutes > 0 else posts_per_day_max
    effective_max_per_day = min(posts_per_day_max, max_fit_in_window)
    if effective_max_per_day <= 0:
        raise ValueError(f"Time window ({window_duration_min} mins) is too small for min gap of {min_gap_minutes} mins.")

    # Distribute post counts per day evenly with random variation
    all_dates = [start_date + timedelta(days=i) for i in range(days_count)]
    day_counts = {d: 0 for d in all_dates}

    remaining = num_videos
    # Round-robin or random distribution across days up to effective_max_per_day
    while remaining > 0:
        available_days = [d for d in all_dates if day_counts[d] < effective_max_per_day]
        if not available_days:
            raise ValueError("Could not fit all videos in the given window and date range constraints.")
        chosen_day = random.choice(available_days)
        day_counts[chosen_day] += 1
        remaining -= 1

    scheduled_datetimes: List[datetime] = []

    # Generate random post times for each day according to count
    for day in sorted(all_dates):
        count = day_counts[day]
        if count == 0:
            continue

        # Try up to 500 attempts to pick `count` random valid timestamps on `day` with min_gap
        valid_times = []
        for _ in range(500):
            candidate_mins = sorted([
                random.randint(win_start_min, win_end_min) for _ in range(count)
            ])
            # Check min gap between consecutive candidate minutes
            is_valid = True
            for j in range(1, len(candidate_mins)):
                if candidate_mins[j] - candidate_mins[j - 1] < min_gap_minutes:
                    is_valid = False
                    break
            if is_valid:
                valid_times = candidate_mins
                break

        if not valid_times:
            # Fallback evenly spaced if random attempt failed
            step = window_duration_min / (count + 1)
            valid_times = [int(win_start_min + (i + 1) * step) for i in range(count)]

        for m in valid_times:
            hour = m // 60
            minute = m % 60
            dt = datetime.combine(day, dtime(hour=hour, minute=minute))
            scheduled_datetimes.append(dt)

    return sorted(scheduled_datetimes)
