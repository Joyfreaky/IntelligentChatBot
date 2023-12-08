import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import time

# Import warnings
import warnings
warnings.filterwarnings("ignore")

def train_and_evaluate_model():
    """
    Trains and evaluates a convolutional neural network model on the MNIST dataset.
    
    This function loads the MNIST dataset, preprocesses the data, defines a model architecture,
    compiles the model, trains the model, evaluates the model, and prints the training time,
    test loss, and test accuracy. Its uses a tensorflow-rocm GPU to train the model.
    """
    # Ensure TensorFlow is using GPU
    if tf.test.gpu_device_name():
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    else:
        print("Please install GPU version of TF")

    # Load MNIST dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Preprocess the data
    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255

    # Define a model
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    # Compile the model
    model.compile(loss=tf.keras.losses.sparse_categorical_crossentropy, optimizer=tf.keras.optimizers.Adadelta(), metrics=['accuracy'])

    # Train the model and measure the time taken
    start = time.time()
    model.fit(x_train, y_train, batch_size=128, epochs=10, verbose=1, validation_data=(x_test, y_test))
    end = time.time()

    print("Time taken to train the model: {} seconds".format(end - start))

    # Evaluate the model
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

train_and_evaluate_model()
