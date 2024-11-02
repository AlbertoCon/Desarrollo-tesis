import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore


# Definir el tamaño de las imágenes
IMG_SIZE = (128, 128)

def cargar_datos():
    dataset_dir = './media/dataset/'

    ia_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir + 'ia',
        image_size=IMG_SIZE,
        label_mode='binary',
        batch_size=32
    )

    human_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir + 'human',
        image_size=IMG_SIZE,
        label_mode='binary',
        batch_size=32
    )

    dataset = ia_ds.concatenate(human_ds).shuffle(1000)
    return dataset


def crear_modelo():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model