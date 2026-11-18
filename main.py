"""news-image-20261117 entry: copy the bundled image to the output path.

The image (entry.png, drawn by draw.py from the news of Tuesday
17 November 2026) is stored in this repository; this program only
copies it, so it needs no network and writes identical bytes on
every run. Standard library only.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Deterministic by construction: a byte-for-byte copy of a fixed file,
# so two runs always produce identical output.
shutil.copyfile(HERE / "entry.png", OUT_DIR / "entry.png")
