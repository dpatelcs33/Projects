import keras
from preprocess import get_train_test
from preprocess import save_data_to_array
from keras.models import Sequential
from keras.layers import BatchNormalization, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Reshape
from keras.utils import to_categorical
import numpy as np
from sklearn import metrics 
import matplotlib.pyplot as plt 
import tensorflow as tf
from sklearn.model_selection import train_test_split

feature_dim_2 = 11

#save_data_to_array(max_len=feature_dim_2)


X_train, X_test, y_train, y_test = get_train_test()
print(X_train.shape)

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=(.10), random_state=42, shuffle=True)


feature_dim_1 = 20

channel = 1
epochs = 15
batch_size = 64
verbose = 1
num_classes = 12

X_train = X_train.reshape(X_train.shape[0], feature_dim_1, feature_dim_2, channel)
X_val = X_val.reshape(X_val.shape[0], feature_dim_1, feature_dim_2, channel)
X_test = X_test.reshape(X_test.shape[0], feature_dim_1, feature_dim_2, channel)

y_train_hot = to_categorical(y_train, num_classes)
y_val_hot = to_categorical(y_val, num_classes)
y_test_hot = to_categorical(y_test, num_classes)

########################### MODEL CREATION ####################################
model = keras.Sequential()

model.add(Conv2D(64, kernel_size=(2, 2), activation='relu', input_shape=(feature_dim_1, 
                 feature_dim_2, channel)))
model.add(Conv2D(64, kernel_size=(2, 2), activation='relu'))
model.add(Conv2D(128, kernel_size=(2, 2), activation='relu'))

model.add(MaxPooling2D(pool_size=(2, 2)))
    
model.add(Dropout(0.30))
    
model.add(Flatten())
    
model.add(Dense(128, activation='relu'))
    
model.add(Dropout(0.30))
    
model.add(Dense(64, activation='relu'))
    
model.add(Dropout(0.40))
    
model.add(Dense(num_classes, activation='softmax'))
########################### MODEL CREATION ####################################

model.summary()

model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])



history = model.fit(X_train, y_train_hot, batch_size=batch_size, epochs=epochs, verbose=verbose, 
                    validation_data=(X_val, y_val_hot))

# Plots training and validation accuracy by epoch.
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'])
plt.show()

test_pred = model.predict(X_test)
test_class= np.argmax(test_pred, axis = 1) 
y_class =  np.argmax(y_test_hot, axis = 1) 
print('Test Error')
print('Correct classification rate (Neural Net):')
print(metrics.accuracy_score(y_class, test_class))
print('Confussion matrix (Neural Net):')
print(metrics.confusion_matrix(y_class, test_class))