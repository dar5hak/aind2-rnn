import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Activation
import keras


def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = [
        series[window_start:window_start + window_size]
        for window_start in range(len(series) - window_size)
    ]
    y = series[window_size:]

    # reshape each
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y), 1)

    return X, y


def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1)))
    model.add(Dense(1))

    return model


def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']

    # all unique characters appearing in the text
    all_chars = set(text)

    # replace anything that isn't an alphabet or a punctuation with a space
    text = text.translate({
        ord(char): ' '
        for char in all_chars
        if char not in punctuation and (ord(char) < 97 or ord(char) > 122)
    })

    return text


def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    # iterate over the text with steps of given size
    for start in range(0, len(text), step_size):
        end = start + window_size

        # avoid potential IndexError
        if end < len(text):
            inputs.append(text[start:end])
            outputs.append(text[end])

    return inputs, outputs


def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))

    return model
