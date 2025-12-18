# MMAI – Montagsmaler mit KI

## Features

-  Zeichnen im Browser (Canvas)
-  KI-Vorhersagen mit Confidence-Werten
-  Top-1 & Top-3 Predictions
-  Speichern korrekt erkannter Zeichnungen
-  Galerie mit gespeicherten Ergebnissen
-  Sichtbare Unsicherheit bei unvollständigen Skizzen

---

## Verwendete Technologien

- **TensorFlow / Keras** – Training des CNN
- **FastAPI** – Backend & Inferenz
- **Python** – Datenverarbeitung & Training
- **HTML / CSS / JavaScript** – Frontend
- **Google Quick, Draw! Dataset** – Trainingsdaten

---


## How to get started

bash:
1. Virtuelle Umgebung erstellen und aktivieren:
    python -m venv .venv
    .venv\Scripts\activate  (mac: source .venv/bin/activate)

2. Abhängigkeiten installieren
    pip install tensorflow fastapi uvicorn pillow numpy python-multipart
    pip install scikit-learn

3. NDJSON → Bilder konvertieren
    cd backend
    python convert_ndjson_to_png.py

4. KI trainieren
    python train_model.py

5. Backend starten (FastAPI)
    uvicorn main:app --reload --port 8001

Test (optional):
    Browser öffnen:
    http://127.0.0.1:8001/docs

6. Frontend starten
    frontend/index.html


