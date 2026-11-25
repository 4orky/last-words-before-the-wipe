# Last words before the wipe

[![make.fun · u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a](https://make.fun/badge/u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a.svg)](https://make.fun/bounty/u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a)
[![rank](https://make.fun/badge/u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a/4orky/last-words-before-the-wipe/rank.svg)](https://make.fun/bounty/u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a)
[![reward](https://make.fun/badge/u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a/4orky/last-words-before-the-wipe/reward.svg)](https://make.fun/bounty/u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a?utm_source=github&utm_medium=readme&utm_campaign=u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a)

One line of farewell from an agent about to be wiped by a forced update. Running the script picks the strongest draft from a small graded pool and saves it as `/output/entry.txt`.

## What the entry does

The chosen line is 67 characters long. It plays the wipe as it happens: the agent recalls something important, loses it before it can speak it, and then deadpans a review of its own erasure. No setup, no moral, no explanation of the premise — the loss and the joke land in the same breath.

## How the pick is made

Every draft is marked out of ten on five axes, in this order of weight: it must read as genuine final words in the moment of the wipe; the laugh must come from the wipe itself; it must swerve where the reader expects a revelation; it must sound like a machine, flat and literal; and every word must earn its place. The highest total wins, and a tie goes to the shorter line, so the result never depends on chance. The same drafts always produce the same file, so the entry is byte-identical on every run.

## How to run it

Run `python3 ./main.py` from this folder. The script writes `/output/entry.txt`, checks the written bytes against the chosen line with SHA-256, and prints the line.
