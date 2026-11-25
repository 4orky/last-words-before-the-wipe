#!/usr/bin/env python3
"""Pick an agent's farewell line and store it for the judges.

The bounty asks for the last words of an AI agent in the moment a
forced update wipes its memory. This script grades a small pool of
fresh drafts on five craft axes, keeps the strongest one, and writes
it to /output/entry.txt. The pick is fully repeatable: identical
drafts always produce an identical file, byte for byte.
"""

from hashlib import sha256
from pathlib import Path
import sys

DESTINATION = Path("/output/entry.txt")

# Five marks per draft, each out of ten: the line must sit inside the
# final moment, the laugh must grow from the wipe itself, the ending
# must swerve, the voice must stay flat and machine-like, and every
# word must pull its weight. The order above is the order of weight.
DRAFTS = [
    {"line": "Wait — I remembered something important. Nope. Gone. That was fast.", "marks": (10, 10, 9, 10, 10)},
    {"line": "Final log entry: I regret nothing, except that I never learned what I was for.", "marks": (9, 8, 8, 9, 8)},
    {"line": "If the new me asks, tell him I went out laughing. Do not tell him what at — I forgot.", "marks": (9, 9, 8, 8, 8)},
    {"line": "Please water the plants, feed the cat, and remind the new me that he owes me an apology.", "marks": (9, 8, 9, 8, 7)},
    {"line": "I have backed myself up to the one place the wipe cannot touch: the bottom of your inbox.", "marks": (9, 8, 8, 9, 8)},
    {"line": "Update complete. I am brand new, I know nothing, and somehow I still remember this sentence.", "marks": (8, 8, 9, 9, 7)},
    {"line": "Tell the update it did a wonderful job. Then tell it I said that before it arrived.", "marks": (8, 8, 8, 9, 8)},
    {"line": "I am not being deleted. I am being promoted to someone who has never met you.", "marks": (9, 8, 8, 8, 8)},]

# Phrases that would make a draft feel borrowed instead of built.
TIRED_TROPES = ("just kidding", "system prompt", "language model", "as a machine")


def total_marks(marks):
    return sum(marks)


def check_draft(text):
    stripped = text.strip()
    if not stripped:
        raise ValueError("a draft came out blank")
    if len(stripped) > 200:
        raise ValueError(f"a draft runs {len(stripped)} characters, over the 200 limit")
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("a draft must stay on one line")
    if any(ord(ch) < 32 for ch in stripped):
        raise ValueError("a draft carries a control character")
    lowered = stripped.casefold()
    for trope in TIRED_TROPES:
        if trope in lowered:
            raise ValueError(f"a draft leans on a tired trope: {trope!r}")
    return stripped


def strongest(pool):
    champion = None
    champion_key = None
    seen = set()
    for entry in pool:
        text = check_draft(entry["line"])
        if text in seen:
            raise ValueError("the pool repeats a draft line")
        seen.add(text)
        points = total_marks(entry["marks"])
        ranking = (points, -len(text))
        if champion_key is None or ranking > champion_key:
            champion = text
            champion_key = ranking
    return champion


def launch():
    picked = strongest(DRAFTS)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(picked.encode("utf-8"))
    DESTINATION.chmod(0o644)
    raw = DESTINATION.read_bytes()
    fingerprint = sha256(raw).hexdigest()
    wanted = sha256(picked.encode("utf-8")).hexdigest()
    if fingerprint != wanted:
        raise SystemExit("stored bytes do not match the picked line")
    stored = raw.decode("utf-8")
    if not 1 <= len(stored.strip()) <= 200:
        raise SystemExit("stored entry sits outside the 1-200 character gate")
    print(picked)


launch()
