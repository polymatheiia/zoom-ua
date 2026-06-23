#!/usr/bin/env python3
"""
Rebase zoom_uk_final.ts onto the new zoom_ru_new.ts structure.

For each message in zoom_ru_new.ts:
  - If the source text already has a Ukrainian translation in zoom_uk_final.ts,
    carry it over (context-agnostic match).
  - Otherwise mark as unfinished (to be translated).

Output: zoom_uk_merged.ts  (ready to feed into translate_new.py)
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

BASE      = Path('/home/sool/Projects/zoom_ua')
RU_NEW    = BASE / 'zoom_ru.ts'
UK_FINAL  = BASE / 'uk.ts'
OUT_FILE  = BASE / 'zoom_uk_merged.ts'


def parse_uk_lookup(path):
    """Return {src_text: best_uk_translation} — prefers finished translations."""
    tree = ET.parse(path)
    root = tree.getroot()
    finished = {}
    unfinished = {}
    for ctx in root.findall('context'):
        for msg in ctx.findall('message'):
            src   = msg.findtext('source', '')
            trans = msg.find('translation')
            if not src or trans is None:
                continue
            text = (trans.text or '').strip()
            if trans.get('type') == 'unfinished':
                if src not in unfinished:
                    unfinished[src] = text
            else:
                if text and src not in finished:
                    finished[src] = text
    # merge: finished takes priority
    result = {**unfinished, **finished}
    return result


def main():
    print("Loading existing Ukrainian translations…")
    uk_lookup = parse_uk_lookup(UK_FINAL)
    print(f"  {len(uk_lookup)} unique source strings with translations")

    print("Loading new Russian structure…")
    tree = ET.parse(RU_NEW)
    root = tree.getroot()

    carried = 0
    new_unfinished = 0
    passthrough = 0

    for ctx in root.findall('context'):
        for msg in ctx.findall('message'):
            src   = msg.findtext('source', '')
            trans = msg.find('translation')
            if trans is None:
                # add a translation element
                trans = ET.SubElement(msg, 'translation')

            # Passthrough: empty, format-only, or no letters
            import re
            s = src.strip()
            is_passthrough = (
                not s
                or re.match(r'^(%\d+\s*)+$', s)
                or not re.search(r'[^\W\d]', s, re.UNICODE)
            )

            if is_passthrough:
                trans.text = src
                trans.attrib.pop('type', None)
                passthrough += 1
            elif src in uk_lookup and uk_lookup[src]:
                trans.text = uk_lookup[src]
                trans.attrib.pop('type', None)
                carried += 1
            else:
                # Keep Russian text as a reference hint in a comment? No — keep it clean.
                # Just mark unfinished with empty translation.
                trans.text = ''
                trans.set('type', 'unfinished')
                new_unfinished += 1

    print(f"  Carried over:  {carried}")
    print(f"  Passthrough:   {passthrough}")
    print(f"  New/unfinished:{new_unfinished}")

    ET.indent(root, space='    ')
    xml_body = ET.tostring(root, encoding='unicode')
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<!DOCTYPE TS>\n')
        f.write(xml_body)
        f.write('\n')

    print(f"Written → {OUT_FILE}")


if __name__ == '__main__':
    main()
