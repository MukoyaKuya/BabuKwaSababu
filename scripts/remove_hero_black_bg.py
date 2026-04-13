"""
Remove edge-connected near-black background from hero portrait (PNG).
Preserves subject: only pixels connected to image borders through dark pixels become transparent.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "static" / "images" / "babu.png"
    if not path.exists():
        raise SystemExit(f"Missing {path}")

    img = Image.open(path).convert("RGB")
    w, h = img.size
    raw = img.tobytes()
    t = 42

    def is_bg_idx(i: int) -> bool:
        j = i * 3
        r, g, b = raw[j], raw[j + 1], raw[j + 2]
        return r <= t and g <= t and b <= t

    visited = bytearray(h * w)
    q: deque[int] = deque()

    def push(i: int) -> None:
        if not visited[i] and is_bg_idx(i):
            visited[i] = 1
            q.append(i)

    for x in range(w):
        push(x)  # y=0
        push((h - 1) * w + x)
    for y in range(h):
        push(y * w)
        push(y * w + w - 1)

    while q:
        i = q.popleft()
        y, x = divmod(i, w)
        if x > 0:
            push(i - 1)
        if x < w - 1:
            push(i + 1)
        if y > 0:
            push(i - w)
        if y < h - 1:
            push(i + w)

    out_px = bytearray(h * w * 4)
    for i in range(h * w):
        j3 = i * 3
        j4 = i * 4
        out_px[j4] = raw[j3]
        out_px[j4 + 1] = raw[j3 + 1]
        out_px[j4 + 2] = raw[j3 + 2]
        out_px[j4 + 3] = 0 if visited[i] else 255

    backup = path.with_name("babu_original_backup.png")
    if not backup.exists():
        img.save(backup, "PNG")

    out = Image.frombytes("RGBA", (w, h), bytes(out_px))
    out.save(path, "PNG")
    print(f"Wrote {path} ({sum(visited)} px transparent)")


if __name__ == "__main__":
    main()
