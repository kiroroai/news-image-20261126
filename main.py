#!/usr/bin/env python3
"""news-image-20261126 entrypoint (Python 3.13, standard library only).

Copies the pre-rendered broadsheet, entry.png, to the output directory
as /output/entry.png. The image is deterministic: the same bytes are
written on every run, because this program only copies a fixed file.

The image is "The Daily Ledger": a 1024x1024 newspaper page summing up
Thursday 26 November 2026 in 50 dated stories -- 5 lead stories plus
45 more across the Middle East, North America, Europe, Africa, Asia,
South America and the Pacific, spanning politics, economy, tech, space,
health, sport, culture and science.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1048576  # the competition's 1 MiB cap, checked before copying


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    if os.path.getsize(source) > MAX_BYTES:
        print("entry.png exceeds the 1 MiB cap", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    # Confirm the copy is byte for byte identical to the source image.
    if _sha256(source) != _sha256(target):
        print("copied entry.png does not match the source", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
