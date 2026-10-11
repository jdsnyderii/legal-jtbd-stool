#!/usr/bin/env python3
"""Decode gzip+base64 large artifacts committed as *.gz.b64 text.

If a .gz.b64 file is missing, corrupted, or a placeholder, this script
explains that and skips it. Prefer unpacking jtbd-models-complete.zip
when available.
"""
from __future__ import annotations

import base64
import gzip
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAMES = ["jobs-instance.yaml", "sample-data.json", "jtbd-editor.html"]


def restore_one(name: str) -> bool:
    p = ROOT / f"{name}.gz.b64"
    if not p.exists():
        print(f"skip {name}: {p.name} not found")
        return False
    text = p.read_text(encoding="utf-8").strip()
    if not text or text.upper() == "PLACEHOLDER" or len(text) < 32:
        print(
            f"skip {name}: {p.name} is empty/placeholder (not real encoded data).\n"
            f"  Use jtbd-models-complete.zip or copy the real file into the repo."
        )
        return False
    # Fix missing padding if any (some editors strip '=')
    pad = (-len(text)) % 4
    if pad:
        text = text + ("=" * pad)
    try:
        raw = gzip.decompress(base64.b64decode(text, validate=False))
    except Exception as e:
        print(f"skip {name}: decode failed ({e})")
        print("  File is not valid gzip+base64. Replace it from the modeling zip.")
        return False
    out = ROOT / name
    out.write_bytes(raw)
    print(f"wrote {name} ({len(raw)} bytes)")
    return True


def main() -> int:
    ok = 0
    for name in NAMES:
        if restore_one(name):
            ok += 1
    if ok == 0:
        print(
            "\nNo artifacts restored. Large catalog files were never fully pushed;\n"
            "only a PLACEHOLDER may exist for jobs-instance.yaml.gz.b64.\n"
            "Unpack jtbd-models-complete.zip into this directory instead."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
