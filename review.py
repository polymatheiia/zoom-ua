#!/usr/bin/env python3
"""
Grammar/style review pass on uk.ts.

Smarter than the translation pass:
  - Skips strings ≤ 10 chars (single-word labels rarely have grammar issues)
  - Sends only Ukrainian text, not the English source (saves ~50% tokens)
  - Batch size 80 instead of 50 (fewer API calls)
  → ~60% less token usage than the translation pass

On rate limit: waits 15 minutes and retries indefinitely — safe to leave overnight.

Usage:
    python3 /home/sool/Projects/zoom_ua/review.py
"""

import xml.etree.ElementTree as ET
import subprocess
import json
import re
import time
from pathlib import Path

BASE      = Path('/home/sool/Projects/zoom_ua')
IN_FILE   = BASE / 'uk.ts'
OUT_FILE  = BASE / 'uk.ts'
PROGRESS  = BASE / '.review_progress.json'

BATCH_SIZE    = 80
MODEL         = 'haiku'
RATE_LIMIT_WAIT = 900   # 15 minutes between retries when rate-limited

SYSTEM_PROMPT = """You are a Ukrainian language editor reviewing software UI strings for the Zoom app.

Your task: fix grammar, spelling, and unnatural phrasing in these Ukrainian UI strings. Do NOT change the meaning — only fix genuine language errors.

ERRORS TO FIX:
1. "всі" → "усі" (Ukrainian norm)
2. "кода" → "коду" (genitive of "код")
3. "строк дії" → "термін дії"
4. "мінімізувати" → "згорнути" (Minimize window)
5. Wrong noun case endings
6. Wrong verb aspect — UI action buttons must use perfective infinitive (видалити, зберегти, скасувати, відповісти — NOT відповідь, видалення as button labels)
7. "Відповідь" as a standalone button → "Відповісти"
8. "Закриті субтитри" → "Приховані субтитри" (closed captions)
9. Russian calques — replace with natural Ukrainian
10. Gender/number agreement errors
11. Wrong preposition use calqued from Russian (e.g. "по" where Ukrainian would use "за", "з", "через")
12. Passive voice where active sounds more natural
13. "це не існує" — fix to match the gender of the implied noun
14. "данні" → "дані"
15. Unnecessary filler words that weren't in a natural Ukrainian original

KEEP UNCHANGED:
- Correct strings that need no fixing — return them as-is
- Format specifiers: %1, %2, %n, etc.
- HTML tags: <b>, </b>, <br/>, etc.
- Brand names: Zoom, Zoom Workplace, Zoom Phone, etc.
- Technical acronyms: DLP, AI, SSO, HIPAA, URL, ID, etc.

OUTPUT: Return ONLY a JSON array — no markdown, no explanation:
[{"id": N, "uk": "corrected or unchanged string"}, ...]"""


def is_passthrough(src):
    s = (src or '').strip()
    if not s: return True
    if re.match(r'^(%\d+\s*)+$', s): return True
    if not re.search(r'[^\W\d]', s, re.UNICODE): return True
    return False


def skip_short(uk):
    """Skip very short strings — single-word labels are unlikely to have grammar issues."""
    return len((uk or '').strip()) <= 10


class RateLimitError(Exception):
    pass


def review_batch(batch):
    """batch: list of {id, uk}. Returns {id: corrected_uk}."""
    items = [{'id': item['id'], 'UK': item['uk']} for item in batch]

    prompt = (
        "Review these Ukrainian Zoom UI strings. Fix grammar/spelling/naturalness errors.\n"
        "Return unchanged if already correct.\n"
        "Return ONLY JSON [{\"id\":N,\"uk\":\"...\"}] — no markdown.\n\n"
        + json.dumps(items, ensure_ascii=False)
    )

    result = subprocess.run(
        ['claude', '-p', '--model', MODEL, '--system-prompt', SYSTEM_PROMPT],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=180,
    )

    if result.returncode != 0:
        combined = (result.stderr or result.stdout or '').lower()
        if not result.stdout.strip() or any(w in combined for w in ('rate', 'limit', 'quota', 'exceeded')):
            raise RateLimitError(result.stderr or 'empty response')
        raise RuntimeError(f"claude exited {result.returncode}: {result.stderr[:200]}")

    text = result.stdout.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    parsed = json.loads(text)
    return {r['id']: r['uk'] for r in parsed}


def main():
    print("Parsing file…", flush=True)
    tree = ET.parse(IN_FILE)
    root = tree.getroot()

    progress = {}
    if PROGRESS.exists():
        with open(PROGRESS) as f:
            progress = json.load(f)
        print(f"Resuming: {len(progress)} strings already reviewed", flush=True)

    # Collect candidate strings
    all_msgs = []
    skipped_short = 0
    for ctx in root.findall('context'):
        n = ctx.find('name')
        ctx_name = (n.text or '') if n is not None else ''
        for msg in ctx.findall('message'):
            src   = msg.find('source')
            trans = msg.find('translation')
            if src is None or trans is None: continue
            if is_passthrough(src.text): continue
            all_msgs.append((ctx_name, msg, trans, src.text or ''))

    to_review = []
    for i, (ctx_name, _msg, trans, src_text) in enumerate(all_msgs):
        key = str(i)
        uk_text = (trans.text or '').strip()

        if key in progress:
            trans.text = progress[key]
            continue

        if not uk_text:
            continue

        if skip_short(uk_text):
            skipped_short += 1
            continue

        to_review.append({'id': i, 'uk': uk_text})

    total     = len(to_review)
    n_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    errors    = 0
    print(f"Skipped (≤10 chars): {skipped_short}", flush=True)
    print(f"Queued for review:   {total}  ({n_batches} batches of {BATCH_SIZE})", flush=True)
    print("Rate limits trigger a 15-min wait and indefinite retries.\n", flush=True)

    for b_start in range(0, total, BATCH_SIZE):
        batch = to_review[b_start:b_start + BATCH_SIZE]
        b_num = b_start // BATCH_SIZE + 1
        pct   = 100 * b_start // total
        print(f"  [{b_num:3d}/{n_batches}] {pct:3d}%  {len(batch)} strings … ", end='', flush=True)

        json_retries = 0
        while True:
            try:
                results = review_batch(batch)
                for item in batch:
                    if item['id'] in results:
                        corrected = results[item['id']]
                        all_msgs[item['id']][2].text = corrected
                        progress[str(item['id'])] = corrected
                print("OK", flush=True)
                break

            except RateLimitError:
                wait = RATE_LIMIT_WAIT
                print(f"rate limit — waiting {wait//60} min… ", end='', flush=True)
                time.sleep(wait)
                print("retrying… ", end='', flush=True)

            except json.JSONDecodeError:
                json_retries += 1
                if json_retries <= 3:
                    print(f"JSON err, retry {json_retries}/3… ", end='', flush=True)
                    time.sleep(5)
                else:
                    print("FAILED (JSON)", flush=True)
                    errors += 1
                    break

            except subprocess.TimeoutExpired:
                print("timeout, retrying… ", end='', flush=True)
                time.sleep(10)

            except Exception as exc:
                print(f"err ({exc}), retrying in 10s… ", end='', flush=True)
                time.sleep(10)

        time.sleep(3)

        if b_num % 10 == 0:
            with open(PROGRESS, 'w') as f:
                json.dump(progress, f, ensure_ascii=False)
            print(f"    [checkpoint: {len(progress)} reviewed]", flush=True)

    with open(PROGRESS, 'w') as f:
        json.dump(progress, f, ensure_ascii=False)

    print(f"\nWriting {OUT_FILE} …", flush=True)
    ET.indent(root, space='    ')
    xml_body = ET.tostring(root, encoding='unicode')
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE TS>\n')
        f.write(xml_body)
        f.write('\n')

    print(f"Done.  Errors: {errors}", flush=True)


if __name__ == '__main__':
    main()
