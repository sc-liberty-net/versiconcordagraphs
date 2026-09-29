# Kickoff — Gesenius transcription, lean-reader pilot

```
Project: Biblography — Ethan's own Bible edition; this session transcribes
Gesenius's Hebrew lexicon (Tregelles 1857) from page scans.
Working folder: C:\Users\ethan\Desktop\Biblography (already on this machine).

Read first, in this order:
  bible-sources/RULES.md          — standing rules for Gesenius: Opus reads the
                                    Hebrew, from crops, never supplying unseen points
  .claude/agents/gesenius-reader.md — the lean reader (Read and Write only) and
                                    its transcription rules
  bible-sources/gesenius_pages.py — the page tool: status, prepare, check, run, done
  bible-sources/lexicons/gesenius/transcript/PROGRESS.md and runs.jsonl
                                  — pages done so far, and token use per run

Mode: measuring. The reader, the crops (now margin-trimmed) and the checks are
built and were verified on pages I–XXV; do not rebuild or re-test them.

Definition of done, in this order:
  1. Read the plan usage meters (get_usage) and note them.
  2. In bible-sources: python gesenius_pages.py run 5 1
     (pages XXVI–XXX, images 45–49, one page per run, in the background)
  3. python gesenius_pages.py status, and read the meters again.
  4. Compare per page against the batch-of-5 run in runs.jsonl
     (images 40–44: 150,081 tokens and $0.54 list cost per page).
If a run fails, fix the cause. Never loosen a check to make it pass.

To see the work: bible-sources/lexicons/gesenius/transcript/n045.txt etc.,
and `python gesenius_pages.py check N` for any page. Spot-check one page
against its scan (prepare N re-cuts the crops) before reporting quality.

Off limits: no pages beyond image 49; no transcribing the rest of the book
(it costs about a week or more of the plan allowance); no changes to the
reader's rules or to the checks.

Manual override: if I write "manual override" I am suspending Mode and Off
Limits for that request. Name the specific consequence and ask before you
act on it.

What I want:
  1. Finish the 10-page pilot and tell me what a page costs one-at-a-time
     versus five-at-a-time, in tokens and in plan usage, and which to use.
  2. Then stop and wait for my go-ahead before any larger run.

Ask before making a change I have not asked for.
Report what you verified, not what you intended.
```

## Still to fill in

Nothing guessed. The one-at-a-time vs five-at-a-time comparison is the open
question; the usage meters also move with other Claude activity on the
account (the Fable meter rose during the first pilot), so read them close to
the run.

## Notes on this version

First kickoff for the Gesenius work. It exists because the first pilot was
driven from a long conversation whose every turn re-read ~400,000 tokens;
running from a fresh session with the page tool's `run` loop avoids that.
