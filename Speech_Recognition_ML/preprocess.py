import librosa
import numpy as np
import os
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from os import listdir
from os.path import isfile, join


DATA_PATH = "C:/Users/dhava/Desktop/School/COMSC 415/Final Project/data/"


# Extracts the word labels.
def get_labels(path=DATA_PATH):
    labels = os.listdir(path)
    label_indices = np.arange(0, len(labels))
    return labels, label_indices, to_categorical(label_indices)


# Converts .WAV files to MFCC (mono and up to 8000Hz).
def wav2mfcc(file_path, max_len=11):
    # Sets audio to Mono, and the sampling rate to 16,000Hz.
    wave, sr = librosa.load(file_path, mono=True, sr=None)
    wave = wave[::3]
    mfcc = librosa.feature.mfcc(wave, sr=16000)

    # If the maximum length exceeds the MFCC length, pad those MFCC out.
    if (max_len > mfcc.shape[1]):
        pad_width = max_len-mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    # Else, clip the MFCC length.
    else:
        mfcc = mfcc[:, :max_len]
    
    return mfcc


# Adds each MFCC to its respective word array (twelve categories are needed).
def save_data_to_array(path=DATA_PATH, max_len=11):
    labels, _, _ = get_labels(path)

    for label in labels:
        mfcc_arrays = []

        wavfiles = [path + label + '/' + wavfile for wavfile in os.listdir(path + "/" + label)]
        for wavfile in tqdm(wavfiles, "Saving vectors of label - '{}'".format(label)):
            mfcc = wav2mfcc(wavfile, max_len=max_len)
            mfcc_arrays.append(mfcc)
        np.save(label + '.npy', mfcc_arrays)



def get_train_test(split_ratio=0.90, random_state=42):
    labels, indices, _ = get_labels(DATA_PATH)

    X = np.load(labels[0] + '.npy')
    y = np.zeros(X.shape[0])

    for i, label in enumerate(labels[1:]):
        x = np.load(label + '.npy')
        X = np.vstack((X, x))
        y = np.append(y, np.full(x.shape[0], fill_value= (i + 1)))

    assert X.shape[0] == len(y)

    return train_test_split(X, y, test_size=(1-split_ratio), random_state=random_state, shuffle=True)


def prepare_dataset(path=DATA_PATH):
    labels, _, _ = get_labels(path)
    data = {}
    for label in labels:
        data[label] = {}
        data[label]['path'] = [path + label + "/" + wavfile for wavfile in os.listdir(path + label)]

        vectors = []

        for wavfile in data[label]['path']:
            wave, sr = librosa.load(wavfile, mono=True, sr=None)
            
            wave = wave[::3]
            mfcc = librosa.feature.mfcc(wave, sr=16000)
            vectors.append(mfcc)

        data[label]['mfcc'] = vectors

    return data


def load_dataset(path=DATA_PATH):
    data = prepare_dataset(path)

    dataset = []

    for key in data:
        for mfcc in data[key]['mfcc']:
            dataset.append((key, mfcc))

    return dataset[:100]

#prepare_dataset(DATA_PATH)