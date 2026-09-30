#!/usr/bin/env python3
"""Decode gzip+base64 large artifacts committed as *.gz.b64 text."""
import base64, gzip
from pathlib import Path
ROOT = Path(__file__).resolve().parent
for name in ['jobs-instance.yaml', 'sample-data.json', 'jtbd-editor.html']:
    p = ROOT / f'{name}.gz.b64'
    if not p.exists():
        print('skip', name)
        continue
    raw = gzip.decompress(base64.b64decode(p.read_text().encode()))
    (ROOT / name).write_bytes(raw)
    print('wrote', name, len(raw))
