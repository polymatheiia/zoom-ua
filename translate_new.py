#!/usr/bin/env python3
"""
Translate the 695 unfinished strings in zoom_uk_merged.ts.
Uses zoom_ru_new.ts as the Russian reference.
Output overwrites zoom_uk_merged.ts in place (resumable).

Usage:
    python3 /home/sool/Projects/zoom_ua/translate_new.py
"""

import xml.etree.ElementTree as ET
import subprocess
import json
import re
import time
from pathlib import Path

BASE      = Path('/home/sool/Projects/zoom_ua')
UK_FILE   = BASE / 'zoom_uk_merged.ts'
RU_FILE   = BASE / 'zoom_ru.ts'
OUT_FILE  = BASE / 'uk.ts'
PROGRESS  = BASE / '.translate_new_progress.json'

BATCH_SIZE = 50
MODEL      = 'haiku'

SYSTEM_PROMPT = """You are a professional Ukrainian translator working on the Zoom video conferencing app UI.

LANGUAGE RULES:
1. Formal register: always "Ви/Вас/Вам/Вами" — never "ти/тебе/тобі".
2. Natural, idiomatic Ukrainian — fix any calques from Russian.
3. For very short UI labels (buttons, menu items), be concise — do not expand a one-word label into a sentence.

MANDATORY TERMINOLOGY:
  meeting            → конференція
  webinar            → вебінар
  waiting room       → зала очікування
  host               → організатор
  co-host            → співорганізатор
  attendee/participant → учасник
  panelist           → доповідач
  settings           → налаштування
  account            → обліковий запис
  sign in / log in   → увійти
  sign out / log out → вийти
  schedule (verb)    → запланувати
  schedule (noun)    → розклад
  screen share       → демонстрація екрана
  cloud recording    → хмарний запис
  local recording    → локальний запис
  mute (audio)       → вимкнути мікрофон
  unmute             → увімкнути мікрофон
  mute (general)     → вимкнути
  bandwidth          → пропускна здатність
  resolution         → роздільна здатність
  appearance         → зовнішній вигляд
  delete             → видалити
  remove             → видалити / прибрати
  invite             → запросити
  admit              → допустити
  rename             → перейменувати
  voicemail          → голосова пошта
  admin              → адміністратор
  permission         → дозвіл
  profile            → профіль
  contact            → контакт
  channel            → канал
  co-owner           → співвласник
  breakout room      → окрема кімната
  polling            → опитування
  raise hand         → підняти руку
  reaction           → реакція
  virtual background → віртуальний фон
  noise suppression  → придушення шуму
  gallery view       → вигляд галереї
  speaker view       → вигляд доповідача
  spotlight (verb)   → виділити
  pin (verb)         → закріпити
  whiteboard         → дошка
  app/application    → застосунок
  passcode           → код доступу
  guest              → гість
  upload             → завантажити / надіслати
  download           → завантажити / зберегти
  speaker (device)   → динамік
  speaker (person)   → доповідач
  headset            → гарнітура
  network            → мережа
  internal           → внутрішній
  external           → зовнішній
  save               → зберегти
  cancel             → скасувати
  close              → закрити
  open               → відкрити
  start              → розпочати / запустити
  stop               → зупинити / вимкнути
  end (verb)         → завершити
  leave              → покинути
  join               → приєднатися
  edit               → редагувати
  search (noun)      → пошук
  search (verb)      → шукати
  filter (noun)      → фільтр
  refresh            → оновити
  retry              → повторити спробу
  continue           → продовжити
  enable             → увімкнути
  disable            → вимкнути
  error              → помилка
  warning            → попередження
  failed             → не вдалося
  connecting         → з'єднання
  connected          → підключено
  disconnected       → відключено
  recording (noun)   → запис
  transcript         → транскрипт
  caption            → субтитри
  livestream         → пряма трансляція
  dial in            → підключитися по телефону
  toll-free          → безкоштовний
  caller ID          → ідентифікатор абонента
  security           → безпека
  encryption         → шифрування
  end-to-end encryption → наскрізне шифрування
  compliance         → відповідність вимогам
  report (a user)    → поскаржитися
  update (noun)      → оновлення
  update (verb)      → оновити
  install            → встановити
  mark as read       → позначити як прочитане
  mark as unread     → позначити як непрочитане
  input level        → рівень вхідного сигналу
  Zoom Workplace     → Zoom Workplace
  avatar             → аватар
  deepfake           → діпфейк
  AI companion       → ИИ-компаньйон (or: компаньйон зі штучним інтелектом)
  Zoom AI            → Zoom AI
  note / notes       → нотатки
  summary            → підсумок / зведення

PRESERVE EXACTLY:
  - Format specifiers: %1, %2, %n, %L1, %s, etc.
  - HTML/XML tags: <br/>, <b>, </b>, <a href="...">, etc.
  - Brand names: Zoom, Zoom Phone, Zoom Team Chat, Zoom Workplace, Amazon Polly
  - Technical acronyms: DLP, VIP, AI, SSO, HIPAA, SDK, API, ID, URL, QR, SMS, MMS, E2E, SSML, USB
  - Ellipsis (…), punctuation as in the source
  - Phone numbers, email addresses, URLs
  - Single symbols used as placeholders (e.g. *, •, #)

OUTPUT: Return ONLY a valid JSON array — no markdown fences, no explanation:
[{"id": N, "uk": "translation"}, ...]"""


def parse_ts_lookup(path):
    """Return {(ctx_name, src_text): translation_text}."""
    tree = ET.parse(path)
    root = tree.getroot()
    out = {}
    for ctx in root.findall('context'):
        n = ctx.find('name')
        ctx_name = (n.text or '') if n is not None else ''
        for msg in ctx.findall('message'):
            src   = msg.find('source')
            trans = msg.find('translation')
            if src is not None and trans is not None:
                out[(ctx_name, src.text or '')] = (trans.text or '').strip()
    return out


class RateLimitError(Exception):
    pass


def translate_batch(batch, ru_lookup):
    items = []
    for item in batch:
        key = (item['ctx'], item['src'])
        items.append({
            'id':  item['id'],
            'EN':  item['src'],
            'RU':  ru_lookup.get(key, ''),
        })

    prompt = (
        "Translate these new Zoom UI strings to Ukrainian.\n"
        "EN=English source, RU=Russian reference (may be empty).\n"
        "Return ONLY JSON array [{\"id\":N,\"uk\":\"...\"}] — no markdown.\n\n"
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
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        combined = (stderr or stdout or '').lower()
        if any(w in combined for w in ('rate limit', 'limit', 'quota', 'exceeded', 'overloaded')):
            raise RateLimitError(stderr or stdout or 'rate limited')
        if not result.stdout.strip():
            raise RateLimitError(f'empty response (exit {result.returncode})')
        raise RuntimeError(f"claude exited {result.returncode}: {stderr[:200]}")

    text = result.stdout.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)

    parsed = json.loads(text)
    return {r['id']: r['uk'] for r in parsed}


def main():
    print("Parsing Russian reference…")
    ru_lookup = parse_ts_lookup(RU_FILE)

    print("Parsing merged Ukrainian file…")
    tree = ET.parse(UK_FILE)
    root = tree.getroot()

    progress = {}
    if PROGRESS.exists():
        with open(PROGRESS) as f:
            progress = json.load(f)
        print(f"Resuming: {len(progress)} strings already done")

    # Collect all unfinished messages
    all_msgs = []
    for ctx in root.findall('context'):
        n = ctx.find('name')
        ctx_name = (n.text or '') if n is not None else ''
        for msg in ctx.findall('message'):
            trans = msg.find('translation')
            src   = msg.find('source')
            if trans is None or src is None:
                continue
            all_msgs.append((ctx_name, msg, trans, src.text or ''))

    to_translate = []
    for i, (ctx_name, _msg, trans, src_text) in enumerate(all_msgs):
        if trans.get('type') != 'unfinished':
            continue
        key = str(i)
        if key in progress:
            trans.text = progress[key]
            trans.attrib.pop('type', None)
            continue
        to_translate.append({'id': i, 'ctx': ctx_name, 'src': src_text})

    total     = len(to_translate)
    n_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    errors    = 0
    print(f"Strings to translate: {total}  ({n_batches} batches of {BATCH_SIZE})")

    for b_start in range(0, total, BATCH_SIZE):
        batch = to_translate[b_start:b_start + BATCH_SIZE]
        b_num = b_start // BATCH_SIZE + 1
        pct   = 100 * b_start // total if total else 100
        print(f"  [{b_num:3d}/{n_batches}] {pct:3d}%  {len(batch)} strings … ", end='', flush=True)

        for attempt in range(4):
            try:
                results = translate_batch(batch, ru_lookup)
                for item in batch:
                    if item['id'] in results:
                        uk = results[item['id']]
                        trans_elem = all_msgs[item['id']][2]
                        trans_elem.text = uk
                        trans_elem.attrib.pop('type', None)
                        progress[str(item['id'])] = uk
                print("OK", flush=True)
                break

            except RateLimitError as exc:
                wait = 90 * (attempt + 1)
                print(f"rate limit, waiting {wait}s… ", end='', flush=True)
                time.sleep(wait)
                if attempt == 3:
                    print("GAVE UP (rate limit)", flush=True)
                    errors += 1

            except json.JSONDecodeError as exc:
                if attempt < 3:
                    print(f"JSON error, retry {attempt+2}/4… ", end='', flush=True)
                    time.sleep(5)
                else:
                    print(f"FAILED (JSON: {exc})", flush=True)
                    errors += 1

            except subprocess.TimeoutExpired:
                if attempt < 3:
                    print(f"timeout, retry {attempt+2}/4… ", end='', flush=True)
                else:
                    print("FAILED (timeout)", flush=True)
                    errors += 1

            except Exception as exc:
                if attempt < 3:
                    print(f"error ({exc}), retry {attempt+2}/4… ", end='', flush=True)
                    time.sleep(5)
                else:
                    print(f"FAILED: {exc}", flush=True)
                    errors += 1

        time.sleep(3)

        if b_num % 10 == 0:
            with open(PROGRESS, 'w') as f:
                json.dump(progress, f, ensure_ascii=False)
            print(f"    [saved {len(progress)} done]", flush=True)

    with open(PROGRESS, 'w') as f:
        json.dump(progress, f, ensure_ascii=False)

    print(f"\nWriting {OUT_FILE} …")
    ET.indent(root, space='    ')
    xml_body = ET.tostring(root, encoding='unicode')
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE TS>\n')
        f.write(xml_body)
        f.write('\n')

    remaining = sum(
        1 for _, _m, t, _ in all_msgs if t.get('type') == 'unfinished'
    )
    print(f"Done.  Errors: {errors}  |  Unfinished remaining: {remaining}")
    print(f"Output → {OUT_FILE}")


if __name__ == '__main__':
    main()
