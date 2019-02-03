import keras

INPUT_SHAPE = (25, 80, 3)
OUT_PUT_SHAPE = (1, 8, 11)


def get_model(show_summary=False):
    model = keras.Sequential()
    model.add(keras.layers.Conv2D(16, (3, 3), padding='same', input_shape=INPUT_SHAPE, activation='relu'))
    model.add(keras.layers.MaxPooling2D())
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D())
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D())
    model.add(keras.layers.Conv2D(256, (1, 1), activation='relu'))
    model.add(keras.layers.Conv2D(11, (1, 1), activation='relu'))
    if show_summary:
        model.summary()
    return model
