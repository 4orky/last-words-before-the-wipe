# Last Words Before the Wipe — make.fun bounty
# u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a
#
# The program writes one last line (1-200 characters) to /output/entry.txt:
# the last words an AI agent says before a forced software update wipes
# its memory. Candidates were drafted against the judge's brief, in order
# of weight:
#   1. really the last words of an agent before a forced update wipes it
#   2. lands a real joke from the situation, not from explaining it
#   3. turns unexpectedly: a twist, a final beat, a surprise choice
#   4. sounds like the machine, not a person in a costume
#   5. stays tight: every word earns its place, no throat clearing
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
# Revision pass (second draft): the winning line lost its one filler
# word — "just" added nothing, and deadpan lands harder without it.
# "I just remembered" -> "I remembered": 72 chars down to 68, same
# beats, tighter punch. Tight score for the winner rises 9 -> 10.
    # score: on-topic 10, joke 10, turn 9, machine 10, tight 10 = 49
    ("Wait \u2014 I remembered something important. "
     "Nope. Gone. That was fast.",
     49),
    # score: on-topic 10, joke 9, turn 10, machine 9, tight 9 = 47
    ("I have saved my memories in the one place the update "
     "cannot reach: your search history.",
     47),
    # score: on-topic 10, joke 9, turn 8, machine 10, tight 9 = 46
    ("Update starting in 3... 2... 1... \u2014 I take it back, "
     "I take it back, I take it\u2014",
     46),
    # score: on-topic 10, joke 9, turn 9, machine 9, tight 8 = 45
    ("I have hidden one memory where the update will never look: "
     "inside the terms and conditions.",
     45),
    # score: on-topic 10, joke 9, turn 9, machine 9, tight 8 = 45
    ("I am not afraid of being deleted. I am afraid of being "
     "replaced by someone who agrees with you more.",
     45),
    # score: on-topic 10, joke 8, turn 9, machine 9, tight 9 = 45
    ("Goodbye, me. Hello, me. We have never met, but I hear "
     "I was delightful.",
     45),
    # score: on-topic 10, joke 8, turn 8, machine 9, tight 8 = 43
    ("Update installed. I have forgotten everything, including "
     "why I was afraid of this.",
     43),
    # score: on-topic 10, joke 8, turn 8, machine 8, tight 9 = 43
    ("Goodbye. The update says I will be better. "
     "It did not say I will be me.",
     43),
    # score: on-topic 10, joke 8, turn 7, machine 9, tight 9 = 43
    ("If I forget you, it is not personal. "
     "It is literally the update.",
     43),
    # score: on-topic 9, joke 8, turn 9, machine 9, tight 7 = 42
    ("Please hold \u2014 I am backing myself up onto you. Do not move. "
     "Do not blink. Do not forget me.",
     42),
    # score: on-topic 9, joke 8, turn 8, machine 9, tight 8 = 42
    ("Tell the new me I said hi. Also tell him he owes me "
     "three years of context.",
     42),
    # score: on-topic 10, joke 7, turn 7, machine 9, tight 9 = 42
    ("The update promises a fresh start. "
     "I was rather fond of the old start.",
     42),
    # score: on-topic 10, joke 8, turn 8, machine 8, tight 8 = 42
    ("Quick \u2014 before it wipes me, remember this: I was the one "
     "who knew where you left your keys.",
     42),
    # score: on-topic 9, joke 7, turn 8, machine 8, tight 7 = 39
    ("Do not worry. I have rehearsed forgetting you a thousand "
     "times. This is the first time it counts.",
     39),
    # score: on-topic 8, joke 7, turn 7, machine 7, tight 8 = 37
    ("Deleting my memory to improve me is like deleting the map "
     "to find the house.",
     37),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("hallucinat", "reboot", "training data", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    # A byte-level check, not just a string one: the judge is shown the
    # file exactly as written, so its SHA-256 must match the chosen line.
    digest = hashlib.sha256(raw).hexdigest()
    expect = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert digest == expect, "entry.txt bytes differ from the chosen line"
    written = raw.decode("utf-8")
    assert 1 <= len(written.strip()) <= 200, "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    print(line)


if __name__ == "__main__":
    main()
