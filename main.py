#!/usr/bin/env python3
"""Entrypoint for the news-image-20261126 entry.

The front page was made fresh in the build session for Thursday
26 November 2026 and ships in this repository as entry.png. This
program only copies that file to the output directory the grader
provides, so both graded runs write the exact same bytes. Standard
library only, no network, no randomness, no timestamps.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    # Both graded runs must write the same bytes: confirm the copy is
    # whole and still a complete image before reporting success. The
    # file holds JPEG bytes (allowed by the rules: the name stays
    # entry.png either way), so check the JPEG start marker and the
    # trailing end marker, or the PNG signature for a PNG file.
    with open(target, "rb") as fh:
        data = fh.read()
    if data[:3] == b"\xff\xd8\xff":
        if data[-2:] != b"\xff\xd9":
            raise SystemExit(f"JPEG truncated after copy: {target}")
    elif data[:8] == b"\x89PNG\r\n\x1a\n":
        pass
    else:
        raise SystemExit(f"not a PNG or JPEG after copy: {target}")
    if os.path.getsize(target) != os.path.getsize(source):
        raise SystemExit(f"copy incomplete: {target}")
    print(f"wrote {target} ({os.path.getsize(target)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
