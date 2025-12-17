import json
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, models

# =========================
# Pfade
# =========================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "images"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

# =========================
# Parameter
# =========================
IMG_SIZE = 64
BATCH_SIZE = 64
EPOCHS = 25
AUTOTUNE = tf.data.AUTOTUNE
SEED = 42

# =========================
# Dataset laden
# =========================
def load_datasets():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="training",
        seed=SEED,
        image_size=(IMG_SIZE, IMG_SIZE),
        color_mode="grayscale",
        batch_size=BATCH_SIZE
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR,
        validation_split=0.2,
        subset="validation",
        seed=SEED,
        image_size=(IMG_SIZE, IMG_SIZE),
        color_mode="grayscale",
        batch_size=BATCH_SIZE
    )

    class_names = train_ds.class_names

    # Normalisierung
    normalization = layers.Rescaling(1.0 / 255)

    train_ds = train_ds.map(lambda x, y: (normalization(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization(x), y))

    train_ds = train_ds.cache().shuffle(1000).prefetch(AUTOTUNE)
    val_ds = val_ds.cache().prefetch(AUTOTUNE)

    return train_ds, val_ds, class_names

# =========================
# Modell
# =========================
def build_model(input_shape, num_classes):
    data_augmentation = models.Sequential([
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.1),
        layers.RandomTranslation(0.1, 0.1),
    ])

    model = models.Sequential([
        layers.Input(shape=input_shape),
        data_augmentation,

        layers.Conv2D(32, 3, activation="relu", padding="same"),
        layers.Conv2D(32, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(),

        layers.Conv2D(64, 3, activation="relu", padding="same"),
        layers.Conv2D(64, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(),

        layers.Conv2D(128, 3, activation="relu", padding="same"),
        layers.Conv2D(128, 3, activation="relu", padding="same"),
        layers.MaxPooling2D(),

        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),

        layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

# =========================
# Main
# =========================
def main():
    train_ds, val_ds, class_names = load_datasets()

    model = build_model(
        input_shape=(IMG_SIZE, IMG_SIZE, 1),
        num_classes=len(class_names)
    )

    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            patience=5,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            MODELS_DIR / "quickdraw_cnn.h5",
            save_best_only=True
        )
    ]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    with open(MODELS_DIR / "class_indices.json", "w", encoding="utf-8") as f:
        json.dump(
            {i: name for i, name in enumerate(class_names)},
            f,
            indent=2,
            ensure_ascii=False
        )

    print("✅ Modell & Klassen gespeichert")

if __name__ == "__main__":
    main()
