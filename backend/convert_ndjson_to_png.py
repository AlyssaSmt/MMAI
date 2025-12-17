"""
Konvertiert QuickDraw NDJSON-Dateien zu PNG-Bildern (64x64).

✔ erkennt automatisch, WO gemalt wurde
✔ croppt auf den gemalten Bereich (Bounding Box)
✔ zentriert die Zeichnung
✔ fügt Padding hinzu
✔ robust gegen:
  - leere Zeichnungen
  - Ein-Punkt-Strokes
  - Float-Koordinaten
  - kaputte NDJSON-Zeilen

Erwartete Struktur:
backend/
 ├─ data/
 │   ├─ ndjson/
 │   │   ├─ full_raw_arm.ndjson
 │   │   └─ ...
 │   └─ images/
"""

import json
from pathlib import Path
from PIL import Image, ImageDraw

# -----------------------------
# Pfade
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
NDJSON_DIR = BASE_DIR / "data" / "ndjson"
OUT_DIR = BASE_DIR / "data" / "images"

# -----------------------------
# Parameter
# -----------------------------
OUTPUT_SIZE = 64      # Zielgröße für CNN
PADDING = 10          # Rand um die Zeichnung
LINE_WIDTH = 6        # Strichdicke
MAX_IMAGES = 1500     # pro Klasse (WICHTIG: für ALLE Klassen gleich!)

CANVAS_LIMIT = 255    # QuickDraw Koordinatenbereich (0–255)


# -----------------------------
# Kernfunktion: Zeichnen + Crop
# -----------------------------
def draw_strokes(strokes):
    all_x, all_y = [], []

    # Alle Punkte sammeln
    for stroke in strokes:
        if len(stroke) < 2:
            continue
        xs = stroke[0]
        ys = stroke[1]

        all_x.extend([int(x) for x in xs])
        all_y.extend([int(y) for y in ys])

    # Falls nichts Sinnvolles gemalt wurde
    if len(all_x) < 2 or len(all_y) < 2:
        return Image.new("L", (OUTPUT_SIZE, OUTPUT_SIZE), 255)

    # Bounding Box
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Padding + Begrenzen
    min_x = max(0, min_x - PADDING)
    min_y = max(0, min_y - PADDING)
    max_x = min(CANVAS_LIMIT, max_x + PADDING)
    max_y = min(CANVAS_LIMIT, max_y + PADDING)

    if max_x <= min_x or max_y <= min_y:
        return Image.new("L", (OUTPUT_SIZE, OUTPUT_SIZE), 255)

    width = int(max_x - min_x + 1)
    height = int(max_y - min_y + 1)

    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)

    # Striche relativ zur Bounding Box zeichnen
    for stroke in strokes:
        if len(stroke) < 2:
            continue
        xs = stroke[0]
        ys = stroke[1]

        points = [
            (int(x) - min_x, int(y) - min_y)
            for x, y in zip(xs, ys)
        ]

        if len(points) > 1:
            draw.line(points, fill=0, width=LINE_WIDTH)

    # Quadratisch machen (zentrieren)
    side = max(width, height)
    square = Image.new("L", (side, side), 255)
    square.paste(
        img,
        ((side - width) // 2, (side - height) // 2)
    )

    # Final resize
    return square.resize(
        (OUTPUT_SIZE, OUTPUT_SIZE),
        Image.Resampling.BILINEAR
    )


# -----------------------------
# Datei verarbeiten
# -----------------------------
def convert_file(path: Path):
    class_name = path.stem.replace("full_raw_", "")
    out_dir = OUT_DIR / class_name
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Konvertiere {class_name} …")

    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= MAX_IMAGES:
                break

            try:
                data = json.loads(line)
                img = draw_strokes(data["drawing"])
                img.save(out_dir / f"{class_name}_{i:05}.png")
            except Exception as e:
                # kaputte Zeilen einfach überspringen
                continue


# -----------------------------
# Main
# -----------------------------
def main():
    files = list(NDJSON_DIR.glob("*.ndjson"))
    if not files:
        print("❌ Keine NDJSON-Dateien gefunden")
        return

    for f in files:
        convert_file(f)

    print("✅ Konvertierung abgeschlossen")


if __name__ == "__main__":
    main()
