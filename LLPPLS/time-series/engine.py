import tensorflow as tf


def compile_and_fit(model, window, patience=2, epochs=20):
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=patience,
        mode='min'
    )

    model.compile(
        loss=tf.losses.MeanSquaredError(),
        optimizer=tf.optimizers.Adam(),
        metrics=[tf.metrics.MeanAbsoluteError()]
    )

    history = model.fit(
        window.train,
        epochs=epochs,
        validation_data=window.val,
        callbacks=[early_stopping]
    )

    return history


def run(model, window):
    history = compile_and_fit(model, window)

    # IPython.display.clear_output()
    val_performance = model.evaluate(window.val)
    performance = model.evaluate(window.test, verbose=0)

    return history, val_performance, performance


def linear_model():
    return tf.keras.Sequential([
        tf.keras.layers.Dense(units=1)
    ])


def dense_model():
    return tf.keras.Sequential([
        # Shape: (time, features) => (time*features)
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=1),
        # Add back the time dimension.
        # Shape: (outputs) => (1, outputs)
        tf.keras.layers.Reshape([1, -1]),
    ])


def conv_model(width=3):
    return tf.keras.Sequential([
        tf.keras.layers.Conv1D(
            filters=32,
            kernel_size=(width,),
            activation='relu'
        ),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=1),
    ])
