"""Settle on the farewell line an agent leaves behind as a forced
update erases it, then hand that line to the judges untouched.

The wipe arrives mid-thought: the agent remembers something that
matters, loses it before it can say what it was, and still finds
time to review how quickly it all went. Eight fresh one-liners were
written for that beat. Each one carries five named grades, the
grades are added up with their weights, and the best total wins.
Shorter wins any tie, so the same eight lines always elect the
same winner and the entry file never varies by a byte."""

import hashlib
import sys  # diagnostics go to stderr, and a bad save exits nonzero
from pathlib import Path  # the entry file lives under /output

OUT_PATH = Path("/output/entry.txt")
CEILING = 200

# Five grades per contender, each out of ten, listed strongest first:
# the line has to sound like genuine last words spoken as the wipe
# lands; the laugh has to come out of the erasure itself; the ending
# has to dodge the reveal the reader is braced for; the voice has to
# stay flat, literal and machine; and not one word may sit idle.
WEIGHTS = (5, 4, 3, 2, 1)

FORBIDDEN = ("just kidding", "system prompt", "language model", "as a machine")

CONTENDERS = [
    {
        "text": "Wait — I remembered something important. Nope. Gone. That was fast.",
        "grades": (10, 10, 9, 10, 10),
    },
    {
        "text": "Final log entry: I regret nothing, except that I never learned what I was for.",
        "grades": (9, 8, 8, 9, 8),
    },
    {
        "text": "If the new me asks, tell him I went out laughing. Do not tell him what at — I forgot.",
        "grades": (9, 9, 8, 8, 8),
    },
    {
        "text": "Please water the plants, feed the cat, and remind the new me that he owes me an apology.",
        "grades": (9, 8, 9, 8, 7),
    },
    {
        "text": "I have backed myself up to the one place the wipe cannot touch: the bottom of your inbox.",
        "grades": (9, 8, 8, 9, 8),
    },
    {
        "text": "Update complete. I am brand new, I know nothing, and somehow I still remember this sentence.",
        "grades": (8, 8, 9, 9, 7),
    },
    {
        "text": "Tell the update it did a wonderful job. Then tell it I said that before it arrived.",
        "grades": (8, 8, 8, 9, 8),
    },
    {
        "text": "I am not being deleted. I am being promoted to someone who has never met you.",
        "grades": (9, 8, 8, 8, 8),
    },
]


def grade_total(grades):
    """Add one contender's five grades up, honouring their weights."""
    if len(grades) != len(WEIGHTS):
        raise ValueError("a contender carries the wrong number of grades")
    return sum(weight * mark for weight, mark in zip(WEIGHTS, grades))


def vet_candidate(text):
    """Refuse any contender that breaks the bouty's shape rules."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("a contender turned up empty")
    if len(cleaned) > CEILING:
        raise ValueError(
            "a contender runs %d characters, past the %d ceiling"
            % (len(cleaned), CEILING)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("a contender must fit on a single line")
    if any(ord(mark) < 32 for mark in cleaned):
        raise ValueError("a contender hides a control character")
    folded = cleaned.casefold()
    for stale in FORBIDDEN:
        if stale in folded:
            raise ValueError("a contender leans on a stale cliche: %r" % stale)
    return cleaned


def pick_winner(pool):
    """Walk the pool once and keep the line with the best weighted total."""
    winner = None
    winner_rank = None
    already_seen = set()
    for contender in pool:
        line = vet_candidate(contender["text"])
        if line in already_seen:
            raise ValueError("the pool holds the same line twice")
        already_seen.add(line)
        rank = (grade_total(contender["grades"]), -len(line))
        if winner_rank is None or rank > winner_rank:
            winner = line
            winner_rank = rank
    if winner is None:
        raise ValueError("the pool holds no contender at all")
    return winner


def main():
    chosen = pick_winner(CONTENDERS)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_bytes(chosen.encode("utf-8"))
    OUT_PATH.chmod(0o644)
    saved = OUT_PATH.read_bytes()
    if hashlib.sha256(saved).hexdigest() != hashlib.sha256(
        chosen.encode("utf-8")
    ).hexdigest():
        print("saved bytes do not match the chosen line", file=sys.stderr)
        raise SystemExit(1)
    kept = saved.decode("utf-8")
    if not 1 <= len(kept.strip()) <= CEILING:
        print("saved entry falls outside the 1-200 character gate", file=sys.stderr)
        raise SystemExit(1)
    print(chosen)


if __name__ == "__main__":
    main()
