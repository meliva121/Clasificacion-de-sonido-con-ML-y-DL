# -*- coding: utf-8 -*-
"""clasificacion_generomusical_xgb_deep-learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jn5bJW6Wg4NZ-xWVyfvmEkgvn6CoOdtC

## **DESCRIPCION DEL TRABAJO Y CONCEPTOS BASICOS DE AUDIO**

####**Clasificación de géneros musicales con el conjunto de datos GTZAN**
####Archivos de audio | Espectrogramas Mel | CSV con características extraídas

En este proyecto, clasificaremos las señales de audio musicales en generos musicales utilizando:
- Aprendizaje automatico (Machine Learning, ML)
- Aprendizaje profundo (Deep Learning, DL)

Para los modelos de ML y DL, se requieren que los sonidos musicales se representen mediante espectogramas de MEL.

Para obtener más información sobre el conjunto de datos, utilice el siguiente enlace de Kaggle:
https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification

## **INICIO**
---
"""

pip install tensorflow

import tensorflow 
from tensorflow.python.client import device_lib
def print_info():
     print('  Versión de TensorFlow: {}'.format(tensorflow.__version__))
     print('  GPU: {}'.format([x.physical_device_desc for x in device_lib.list_local_devices() if x.device_type == 'GPU']))
     print('  Versión Cuda  -> {}'.format(tensorflow.sysconfig.get_build_info()['cuda_version']))
     print('  Versión Cudnn -> {}\n'.format(tensorflow.sysconfig.get_build_info()['cudnn_version']))

print_info()

"""**Montando Google Drive**"""

from google.colab import drive
drive.mount('/content/drive')

"""**Estableciendo una variable de ambiente para la ruta donde descargar el dataset GTZAN**"""

import os
os.environ['KAGGLE_CONFIG_DIR'] = "/content/drive/MyDrive/dataset_GTZAN_kaggle"

"""**Cambiando el directorio de trabajo donde se descargara el dataset GTZAN**"""

cd  /content/drive/MyDrive/dataset_GTZAN_kaggle

"""**Descargando el dataset GTZAN en formato zip desde kaggle**"""

!kaggle datasets download -d andradaolteanu/gtzan-dataset-music-genre-classification

"""**Desempaquetando el dataset en formato zip**"""

!unzip gtzan-dataset-music-genre-classification.zip

"""## **SECCION I - PREPROCESAMIENTO DE DATOS DE AUDIO**
---

**Importando librerías**
"""

# Commented out IPython magic to ensure Python compatibility.
# importando librerias
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

from glob import glob # nos permite listar todos los archivos en un directorio
import IPython
import IPython.display as ipd # para reproducir los archivos de audio

import librosa # paquete principal para trabajar con datos de audio
import librosa.display

"""**Leer los archivos de audio**
Con el uso del paquete glob, podemos enumerar todos los archivos en las carpetas.
"""

# Haga una lista de todos los archivos wav en el conjunto de datos y guárdelos en una variable
audio_files = glob("/content/drive/MyDrive/dataset_GTZAN_kaggle/Data/genres_original/*/*.wav")

"""Con el uso de '*' (asteriscos) podemos enumerar todos los elementos en el conjunto de datos. Reemplaza los asteriscos con cualquier archivo que exista en el conjunto de datos.

**Escuchar los archivos de audio**
Con el uso del módulo de visualización de IPhytons podemos mostrar los archivos de audio. Obtenemos un reproductor en el cuaderno donde podemos escuchar el archivo de audio. Tomar en cuenta que en realidad no leímos el archivo y no podemos manipularlo todavía.
"""

# Reproducir el primer archivo de audio
ipd.Audio(audio_files[0])

"""**Carga de los archivos de audio**   
Aquí usamos librosa y su función load() para leer los archivos de audio. Guardamos las salidas como 'y' y sr':

- y: datos sin procesar del archivo de audio (matriz numpy)
- sr: valor entero de la frecuencia de muestreo
"""

# cargue el archivo de audio y muestre los datos sin procesar y la frecuencia de muestreo
y, sr = librosa.load(audio_files[0])
print("Y is a numpy array:", y)
print("Shape of Y:", y.shape)
print("Sample Rate:", sr)

"""Podemos ver que los datos sin procesar de nuestros archivos de audio (y) son matrices numpy y, en este caso, nuestra frecuencia de muestreo (sr) es 22050.

**Grafica de los archivos de audio**   
Una forma de graficar la matriz de datos de audio sin procesar es convertirla en una serie de pandas y usar la función plot().
"""

# convierta la matriz de datos sin procesar en serie pd y trace el ejemplo de audio
pd.Series(y).plot(figsize=(10,5), title="Raw Audio Example", color='blue');

"""También podemos usar la función display.waveshow() de librosa."""

plt.figure(figsize=(10,5))
librosa.display.waveshow(y, color = "Green")
plt.show()

"""**Aplicando STFT (Short Time Fourier Transform)**

Queremos llevarlo al siguiente nivel observando las diferentes frecuencias según su potencia.
Hacemos esto aplicando una **transformada de Fourier** a los datos de audio. Eso nos permite extraer qué frecuencias suenan en diferentes partes del archivo de audio. Usamos la función stft() (**Short-time Fourier Transform**, Transformada de Fourier de tiempo corto).
Luego aplicamos la función de amplitud a db a la salida de STFT, que es una transformación comúnmente utilizada para datos de audio para convertir valores de amplitud a decibelios (dB).
Con esto obtenemos datos que podemos alimentar a los modelos ML normales.
"""

# Use STFT en datos de audio sin procesar
D = librosa.stft(y)
# convertir valores de amplitud a decibelios tomando el valor absoluto de D en referencia a cuál sería el valor máximo
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
# ver la forma de los datos transformados
print("Nueva forma de datos transformados", S_db.shape)

"""**Grafica de un archivo de audio como un espectrograma**  
Un espectrograma es una representación visual del espectro de frecuencias en un sonido u otra señal a medida que varía con el tiempo. El gráfico resultante es un gráfico bidimensional, con la frecuencia en el eje vertical y el tiempo en el eje horizontal. Los espectrogramas se utilizan a menudo en el análisis y la manipulación de señales de audio, especialmente en los campos de la música, el habla y la acústica.
"""

# trazar datos transformados como espectrograma
fig, ax = plt.subplots(figsize=(10,5))
img = librosa.display.specshow(S_db, x_axis='time', y_axis='log', ax=ax)
ax.set_title('Spectogram Example', fontsize=20)
fig.colorbar(img, ax=ax, format=f'%0.2f');

"""**Crear un Espectrograma Mel (Espectrograma Melódico)**  
Un espectrograma Mel es un tipo de espectrograma que representa el contenido espectral de un sonido o señal en una escala que se basa en el tono percibido de las diferentes frecuencias. La escala de Mel es una escala logarítmica que asigna la frecuencia al tono de una manera que está más estrechamente relacionada con la forma en que el sistema auditivo humano percibe el tono.
"""

# aplicar espectrograma mel sin STFT
S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128*2)
print("Shape of Mel Spectogram", S.shape)
# use esa función de conversión como arriba
S_db_mel = librosa.amplitude_to_db(S, ref=np.max)

# trazar el espectrograma de mel
fig, ax = plt.subplots(figsize=(10,5))
img = librosa.display.specshow(S_db_mel, x_axis='time', y_axis='log', ax=ax)
ax.set_title('Mel Spectogram Example', fontsize=20)
fig.colorbar(img, ax=ax, format=f'%0.2f');

"""**EDA - Exploratory Data Analysis (Análisis de datos exploratorios)**

"""

# cargar el archivo csv 
df = pd.read_csv("/content/drive/MyDrive/dataset_GTZAN_kaggle/Data/features_3_sec.csv")

df.head() # primeras 5 entradas

df.shape # ver la forma de df

df.info() # información sobre las muestras, características y tipos de datos

"""**Se verifica si hay valores perdidos**"""

df.isnull().sum() # comprobación de valores perdidos

sns.countplot(x=df.label) # grafica de las categoriaes
plt.xticks(rotation=90);

"""Tenemos una cantidad uniforme de todas las categorías con 9990 muestras.

**Estandarizacion y etiquetado de los datos**  
Después de colocar la columna de nombre de archivo y asignar nuestra x e y, usamos StandardScaler en nuestros valores de x para estandarizar nuestros datos y LabelEncoder para nuestras etiquetas. Luego dividimos nuestros datos en datos de entrenamiento y prueba.
"""

# elimina la columna de nombre de archivo y muestre las primeras nuevas 5 entradas de df
df = df.drop(labels='filename',axis=1)
df.head()

# importar codificador de etiquetas y escalador
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
encoder = LabelEncoder()
scaler = StandardScaler()

data = df.iloc[:, :-1] # obtener las otras columnas
data

labels = df.iloc[:, -1] # obtener columna de etiquetas
labels.to_frame()

"""**Preparando x e y**"""

# asignar x e y, escalar x y codificar y
x = np.array(data, dtype = float)
x = scaler.fit_transform(data)
y = encoder.fit_transform(labels)
x.shape, y.shape

# dividir datos para entrenar y datos para probar
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
x_train.shape, x_test.shape, y_train.shape, y_test.shape
#((6693, 58), (3297, 58), (6693,), (3297,))

"""# **SECCION II - CONSTRUYENDO LOS MODELOS DE APRENDIZAJE AUTOMATICO**
---

### **Modelos GaussianNB, BernoulliNB, KNeighborClassifier, DecisionTreeClassifier y XGBClassifier con sklearn**
"""

from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
    
# crear una instancia de cada algoritmo de clasificación
g=GaussianNB()
b=BernoulliNB()
KN=KNeighborsClassifier()
D=DecisionTreeClassifier()
XGB=XGBClassifier()

algos=[g,b,KN,D,XGB]
algo_names=['GaussianNB','BernoulliNB','KNeighborsClassifier','DecisionTreeClassifier','XGBClassifier']

"""# **SECCION III - EVALUACION DE LOS MODELOS DE APRENDIZAJE AUTOMATICO**
---

### **Evaluacion de los modelos**
"""

accuracy_scored=[]
    
# ajustar y predecir para cada Algoritmo
for item in algos:
    item.fit(x_train,y_train)
    item.predict(x_test)
    accuracy_scored.append(accuracy_score(y_test,item.predict(x_test)))

"""### **Mostrar los resultados en una tabla Dataframe**"""

# mostrar resultados en un DataFrame
result = pd.DataFrame(accuracy_scored, columns=["Accuracy"])
result['Algos']=algo_names
result.sort_values('Accuracy',ascending=False)

"""El mejor resultado lo muestra el **XGBClassifier** con una **Precisión del 87,41%**.   
Veamos si podemos lograr mejores resultados usando Deep Learning.

#**SECCION IV - CONSTRUCCION Y EVALUACION DE UNA RED NEURONAL PARA APRENDIZAJE PROFUNDO**
---

**Contruyendo el modelo con tensorflow y keras**
"""

# importar bibliotecas de aprendizaje profundo
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential

"""**Arquitectura sin redes convolucionales**"""

# Construcción del modelo
model = keras.models.Sequential([
    keras.layers.Dense(512, activation="relu", input_shape=(x_train.shape[1],)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(256,activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(128,activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64,activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation="softmax"),  
])

"""**Resumen del modelo**"""

print(model.summary()) # muestra el resumen del modelo

"""**Compilando el modelo**"""

# Compilando el modelo  
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics='accuracy')

"""**Entrenando el modelo**"""

# Ajuste del modelo - entrenamiento
history = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=300, batch_size=128)

"""**Evaluando la precision del modelo**"""

# evaluar el modelo
_, accuracy = model.evaluate(x_test, y_test, batch_size=128)
#26/26 [==============================] - 0s 3ms/step - loss: 0.4606 - accuracy: 0.9284
print("Accuracy:",accuracy) # print accuracy
#Accuracy: 0.9284197688102722

"""Con Deep Learning logramos una **Precisión del 92,44%**.

**Grafica de la exactitud por epocas**
"""

# Plot results
pd.DataFrame(history.history).plot(figsize=(12,6))
plt.show()

pd.DataFrame(history.history).shape

pd.DataFrame(history.history).min()

pd.DataFrame(history.history).max()

"""#**Construccion de red neuronal preentrenada**

**Cargar Modelo pre-entrenado DenseNet:**
"""

# https://www.tensorflow.org/api_docs/python/tf/keras/applications
img_width = 224
img_height = 224
batch_size = 40

pretrained_model_name = 'VGG16'
project_folder = "/content/drive/MyDrive/DrFIIS/2022-2/covid19-pretrained-models"

from tensorflow.keras.applications.vgg16 import VGG16

# Cargando modelo
pretrained_model = VGG16(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))

pretrained_model.summary();

"""**Se indica que la parte de caracterización no es entrenable**"""

for layer in pretrained_model.layers:
    layer.trainable = False

pretrained_model.summary()

"""**Agregando el clasificador nuevo**"""

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import GlobalAveragePooling2D
from keras.layers import Flatten
from keras.layers import Dropout

# Definiendo una Red Neuronal vacía
model = Sequential()

# Agregando la parte convolucional (base)
model.add(pretrained_model)               # Modelo base

# Clasificador propio
model.add(GlobalAveragePooling2D())       # GlobalAveragePooling2D https://adventuresinmachinelearning.com/global-average-pooling-convolutional-neural-networks/
model.add(Dense(1000, activation='relu'))
model.add(Dropout(rate=0.2))
model.add(Dense(1, activation='sigmoid'))

print("Arquitectura final:")
model.summary()

"""**Grafica de la arquitectura del modelo**"""

from tensorflow.keras.utils import plot_model
plot_model(model, show_dtype=True, show_shapes=True, show_layer_names=True, rankdir='TB',to_file=project_folder + '/output/' + pretrained_model_name + '_plot.png',dpi=80)

"""**Compilando la red neuronal**"""

from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adam

opt = SGD(learning_rate=0.008, momentum=0.9)
# opt = Adam(lr=0.008, beta_1=0.9, beta_2=0.999)

# COMPILANDO la Red Neuronal Convolucional
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

"""**Entrenando la red nuronal**"""

num_imgs_testin=len(x_test)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# batch_size=40
# epochs=20
# training_set_imgs=x_train
# testing_set_imgs=x_test
# num_imgs_training=len(x_train)
# num_imgs_testing=len(x_test)
# 
# 
# # Entrenar
# history = model.fit(training_set_imgs,
#                     epochs=epochs,
#                     steps_per_epoch=np.ceil(num_imgs_training/batch_size),
#                     validation_data=testing_set_imgs,
#                     validation_steps=np.ceil(num_imgs_testing/batch_size))