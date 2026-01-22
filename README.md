# MMAI – Montagsmaler mit KI

Ein interaktives Zeichenspiel, bei dem eine KI versucht zu erraten, was der Benutzer auf einer Zeichenfläche malt.  
Das Projekt orientiert sich am Spielprinzip von *Montagsmaler* und demonstriert die Möglichkeiten und Grenzen der KI-gestützten Erkennung von handgezeichneten Skizzen.

---

## Features

- Zeichnen im Browser (HTML5 Canvas)
- KI-Vorhersagen mit Konfidenzwerten
- Anzeige der Top-1- und Top-3-Predictions
- Speichern korrekt erkannter Zeichnungen
- Galerie mit gespeicherten Ergebnissen
- Sichtbare Unsicherheit bei unvollständigen Skizzen

---

## Verwendete Technologien

- **TensorFlow / Keras** – Training eines Convolutional Neural Networks (CNN)
- **FastAPI** – Backend und Modell-Inferenz
- **Python** – Datenverarbeitung, Training und Backend-Logik
- **HTML / CSS / JavaScript** – Frontend
- **Google Quick, Draw! Dataset** – Trainingsdaten

---

## How to get started

1. Virtuelle Umgebung erstellen und aktivieren
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate    # macOS / Linux
```
2. Abhängigkeiten installieren
```bash
    pip install reqquirements.txt
```
3. NDJSON → Bilder konvertieren
```bash
    cd backend
    python convert_ndjson_to_png.py
```
4. KI trainieren
```bash
    python train_model.py
```
5. Backend starten (FastAPI)
```bash
    uvicorn backend.main:app --reload --port 8001
```
Test (optional):
    Browser öffnen:
    http://127.0.0.1:8001/docs

6. Frontend starten
```bash
    frontend/index.html
```

