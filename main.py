"""Entry for make.fun news-image-20261121 (Python 3.13, standard library only).

The entry image is the file ``entry.png`` beside this program: a dense
front page summing up Saturday 21 November 2026 in one picture -- four
photo leads (missiles over Poland, Wall Street in correction, Kyiv hit
again, missiles over Riyadh), a world map with 12 numbered markers, six
region blocks covering every continent, and a footer ticker.

Running this program copies that image to the output directory
(``$MAKEFUN_OUTPUT_DIR``, default ``out``) as ``entry.png``. It makes no
network calls and writes the same bytes on every run, so the grader's two
runs agree byte for byte.

Run it locally with::

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(HERE, "entry.png")
NAME = "entry.png"
LIMIT_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def output_directory():
    """Where the grader wants the image (its /output, or a local stand-in)."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"


def check_source_present():
    """Fail loudly instead of writing nothing when the image is missing."""
    if not os.path.isfile(IMAGE):
        raise SystemExit("entry.png is missing from the repository root")


def write_image(directory):
    """Copy the front page into place and return the written path."""
    os.makedirs(directory, exist_ok=True)
    target = os.path.join(directory, NAME)
    shutil.copyfile(IMAGE, target)
    return target


def check_size(path):
    """The gate allows at most 1 MiB; refuse to hand over an oversize file."""
    size = os.path.getsize(path)
    if size > LIMIT_BYTES:
        raise SystemExit(f"{NAME} is {size} bytes, over the 1 MiB limit")
    return size


def check_format(path):
    """Confirm the bytes really are a PNG before the gate sees them."""
    with open(path, "rb") as handle:
        head = handle.read(len(PNG_SIGNATURE))
    if head != PNG_SIGNATURE:
        raise SystemExit(f"{NAME} does not start with a PNG signature")


def check_dimensions(path):
    """Read the PNG IHDR chunk and confirm the image is at most 1024x1024."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[12:16] != b"IHDR":
        raise SystemExit(f"{NAME} has no PNG IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit(f"{NAME} is {width}x{height}, over the 1024x1024 limit")
    return width, height


def check_copy_complete(path):
    """Confirm the copy is whole: same bytes, same digest as the source."""
    with open(IMAGE, "rb") as handle:
        source_digest = hashlib.sha256(handle.read()).hexdigest()
    with open(path, "rb") as handle:
        written_digest = hashlib.sha256(handle.read()).hexdigest()
    if source_digest != written_digest:
        raise SystemExit("copied entry.png does not match the source image")
    return written_digest


def main():
    check_source_present()
    target = write_image(output_directory())
    size = check_size(target)
    check_format(target)
    width, height = check_dimensions(target)
    digest = check_copy_complete(target)
    print(f"wrote {target} ({width}x{height}, {size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
