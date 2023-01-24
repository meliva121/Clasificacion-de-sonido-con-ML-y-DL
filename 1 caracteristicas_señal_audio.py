# -*- coding: utf-8 -*-
"""descripcion_estadistica_audio.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/171qOMPDbGQsyqZy68_nLVDtwHbpP1bSn

https://joserzapata.github.io/courses/mineria-audio/descripcion_estadistica/

#**Descripción de sonidos**
Se describe en este notebook:
- Señales en le tiempo de notas musicales
- Descripcion estadistica
- Represntacion en frecuencia
- Percepcion audible de sonidos (Psicoacustica)

# **Señales en el tiempo de sonidos musicales**
---

**Señal de sonidos silbido, clarinete en el tiempo**
"""

#Importar Modulo scipy para leer y grabar audio
from scipy.io import wavfile
import numpy as np
import IPython.display as ipd
from os import rename as rn

!wget http://waveevents.com/MyFilez/wavs/variety/copwhisl.wav
rn("copwhisl.wav", "Whistle.wav")
AudioName = "Whistle.wav" # Archivo de Audio

# Salida fs: Frecuencia de muestreo and data: Señal de audio -> int16
fs, Audiodata = wavfile.read(AudioName)
print(f'Duracion = {Audiodata.shape[0]/fs} , Frecuencia de Muestreo = {fs} [=] Muestras/Seg' \
      f', Wav format = {Audiodata.dtype}')

ipd.Audio(AudioName) # Reproduce el audio directamente en el Jupyter notebook.

import matplotlib.pyplot as plt #Libreria para realizar graficos

#plt.rcParams['figure.figsize'] = (15, 5) # Definir el tamaño de graficas
# Definir los valores de los datos de amplitud entre [-1 : 1] Audiodata.dtype es int16
AudiodataScaled = Audiodata / (2.**15)

#definir los valores del eje x en milisegundos
timeValues = np.arange(0, len(AudiodataScaled), 1)/ fs # Convertir Muestras/Seg a Segundos
timeValues = timeValues * 1000  #Escala de tiempo en milisegundos

####IMPORTACION DE LIBRERIAS PARA GRAFICAR FUERA DE LINEA
# importar la libreria plotly offline para graficar
import plotly.offline as pyo # realizar graficas offline
from plotly.offline import iplot, init_notebook_mode #para poder graficar dentro del jupyter notebook
import plotly.graph_objs as go
import plotly

#####Problema: los comandos fig.show() o
#####iplot(fig, filename='Audio'); muestra el marco de la figura en blanco
#####Solucion: lineas agregadas para mostrar las figuras
import plotly.io as pio
pio.renderers.default = 'colab'

datos = [go.Scatter(x = timeValues,y = 3*10e3*AudiodataScaled,mode = 'lines')]
layout = go.Layout(title = 'Señal de Audio de silbido',xaxis = dict(title = 'Tiempo (ms)'),yaxis = dict(title = 'Amplitud'))
fig = go.Figure(data=datos,layout=layout)
#fig.show()
iplot(fig, filename='Audio')
#plt.plot(timeValues,3*10e3*AudiodataScaled)

"""**Señal del oboe en el Tiempo**   
La señal de audio es una serie de tiempo de como cambiar la presión, ¿Como son estadísticamente los datos de una señal de audio?
"""

!wget https://ccrma.stanford.edu/workshops/dsp2008/sound-library/oboe/Oboe1/Oboe-C6.wav
rn("Oboe-C6.wav", "oboe_c6.wav")
AudioName = "oboe_c6.wav" # Archivo de Audio

# Salida fs: Frecuencia de muestreo and data: Señal de audio -> int16
fs, Audiodata = wavfile.read(AudioName)
Audiodata = Audiodata / (2.**15) #convertirla entre [-1,1]
timeValues = np.arange(0, len(Audiodata), 1)/ fs # Convertir Muestras/Seg a Segundos
timeValues = timeValues * 1000 
print(f'Frecuencia de Muestreo = {fs} [=] Muestras/Seg, Numero de datos: {len(Audiodata)}')

datos1 = [go.Scatter(x = timeValues,y = Audiodata,mode = 'lines')]
layout1 = go.Layout(title = 'Señal de Audio de oboe',xaxis = dict(title = 'Tiempo (ms)'),yaxis = dict(title = 'Amplitud'))
fig = go.Figure(data=datos1,layout=layout1)
#fig.show()
pyo.iplot(fig, filename='Audio1')
ipd.Audio(AudioName)

"""#**Descripcion Estadistica de los datos**
---

- **Histograma**
- **Varianza**
- **boxplot**

**Señal del oboe**
"""

import pandas as pd # convertir arreglo numpy en una serie de pandas
X = pd.Series(Audiodata)
X.describe()

print('Varianza = {}'.format( X.var())) # Varianza
print('Desviacion Standard = {}'.format( X.std())) # Desviacion estandard
print('Skewnesss = {}'.format( X.skew())) # Skewness
print('Kurtosis = {}'.format( X.kurt())) # Kurtosis

# Histograma y densidad
import plotly.figure_factory as ff
hist_data = [X]
group_labels = ['Oboe']
fig = ff.create_distplot(hist_data, group_labels,bin_size=0.01,show_rug=False)
fig['layout'].update(title='Histograma y KDE Señal de Audio del oboe')
pyo.iplot(fig, filename='Basic Distplot')

trace0 = [go.Box(y=X, name = 'Oboe')] # Boxplot
fig = go.Figure(data=trace0)
fig['layout'].update(title='Boxplot Señal de Audio del oboe')
pyo.iplot(fig, filename='Grafica-boxplot')

"""#**Si se comparan varios audios: ¿serán diferentes?**
---


"""

pip install pydub

"""**Importacion de la señal de clarinete**"""

from pydub import AudioSegment
import librosa
import soundfile as sf

!wget https://ccrma.stanford.edu/workshops/mir2014/audio/Instrument%20Samples/clarinet/Clarnt/Clarnt-C6.wav
#rn('Clarnt-C6.wav', 'clarinet_c6.wav')

clarinete=AudioSegment.from_wav("Clarnt-C6.wav")
clarinete = clarinete + clarinete + clarinete + clarinete
clarinete.export("clarinet_c6.wav", format="wav")

"""###Señal en el tiempo del silbido, oboe y clarinete"""

fs1, Audiodata1 = wavfile.read('oboe_c6.wav')
Audiodata1 = Audiodata1 / (2.**15)
ipd.display(ipd.Audio('oboe_c6.wav'))

fs2, Audiodata2 = wavfile.read('clarinet_c6.wav')
Audiodata2 = Audiodata2 / (2.**15)
ipd.display(ipd.Audio('clarinet_c6.wav'))

fs3, Audiodata3 = wavfile.read('Whistle.wav')
Audiodata3 = Audiodata3 / (2.**15)
ipd.display(ipd.Audio('Whistle.wav'))

# Graficar las formas de onda
plt.rcParams['figure.figsize'] = (15, 5) # Definir el tamaño de graficas
for n in range(3):
    pos = n+1
    plt.subplot(3,1,pos) # posicion de la grafica
    nombre_variable = vars()['Audiodata'+str(pos)] #convertir string a nombre de variable
    plt.plot(nombre_variable); #graficar cada forma de onda
plt.tight_layout()

df = pd.DataFrame([Audiodata1,Audiodata2,Audiodata3]).T
print(f'frecuencias de muestreo de los archivos: fs1 = {fs1}, fs2 = {fs2} y fs3 = {fs3}')
print('Tamaño del data frame = {}'.format( df.shape))   # Tamaño del dataframe
print('Duracion en Segundos = {}'.format(len(df)/fs3)) # numero_de_datos / fs = tiempo

"""140626 datos!!!!

Si es monofonico como de 3 segundos¿Por que tantos?

¿Entonces el audio tiene muchos datos? -> SI
"""

#df.plot.box(title = 'Boxplot de las señales de audio');
Oboe = go.Box(y=df[0], name = 'Oboe');
Clarinete = go.Box(y=df[1], name = 'Clarinete');Whistle = go.Box(y=df[2], name = 'Whistle')
datos = [Oboe, Clarinete,Whistle]
fig = go.Figure(data=datos);
fig['layout'].update(title='Boxplot Señales de Audio')
pyo.iplot(fig, filename='Grafica-boxplot2')

"""#**Descripcion Estadistica de los datos: Tabla y correlacion**
---

**Descripcion Estadistica general de los datos**
"""

df.describe()

"""**Correlacion de los datos**"""

# Correlation Matrix 
import numpy as np # se deben rotar los datos 90 grados
data = ff.create_annotated_heatmap( z=np.rot90((np.array(df.corr()))), 
                                    x =  ['Whistle','Clarinete','Oboe'],
                                    y= ['Oboe', 'Clarinete','Whistle'])
pyo.iplot(data, filename='corr-heatmap')

"""¡Al parecer las diferencias no son notables con las estadísticas básicas en estos tres sonidos diferentes!  
pero la correlacion muestra que son muy diferentes

¿Que Caracteristicas se extraen del Audio para Usarlo en Ciencia de datos?

#**REPRESENTACION EN EL TIEMPO DE SEÑALES DE AUDIO MEDIANTE DIFERENTES LIBRERIAS**
---

**Representación del audio en el tiempo**  
**usando librerias mas utilizadas**  
Las ondas acusticas es el que se transmite a traves del aire como oscilaciones de presion de aire. En esencia, el sonido es simplemente vibración del aire.

El Sonido se refiere a la producción, transmisión o recepción de sonidos audibles por los humanos. Una señal de audio es una representación digital del sonido que representa la fluctuación en la presión del aire causada por la vibración en función del tiempo. A diferencia de las partituras o las representaciones simbólicas, las representaciones de audio codifican todo lo que es necesario para reproducir un sonido.

**Señales de audio en python**
- Lectura y reproducción de archivos de audio
- Visualización de señales de audio
- Escribir archivos de audio

**Librerias de Python para analisis de audio**  
Scipy (scipy.signal , scipy.fftpack , scipy.io)  
Librosa (https://librosa.github.io/)  
PyAudioAnalysis (https://github.com/tyiannak/pyAudioAnalysis)  
Essentia (http://essentia.upf.edu)  
Madmon (https://github.com/CPJKU/madmom)  
OpenSmile (https://audeering.com/technology/opensmile/)  

**Manejo de Audio Python**
Python tiene incluidos varios módulos para usar archivos de audio, pero son librerías muy básicas
- **audioop**: Manipular datos de audio en bruto(raw)
- **wave**: Leer y escribir archivos WAV
- **sndhdr**: Determinar el tipo de archivo de audio

**Escuchar sonidos en Jupyter Notebook**
"""

import IPython.display as ipd # Para reproducir audio en el Jupyter Notebook
#Crear una sinusoidal artificial y escucharla
import numpy as np
sr = 22050 # Frecuencia de Muestreo
T = 3.0    # segundos
t = np.linspace(0, T, int(T*sr), endpoint=False) # Variable de tiempo
x = 0.5*np.sin(2*np.pi*440*t)                # Sinusoidal pura a 440 Hz
ipd.Audio(x, rate=sr) # Escuchar el array Numpy

"""**Libreria scipy.io**  
Es un ecosistema en Python de software de código abierto para Matemáticas, ciencia e ingeniería. En particular, estos son algunos de los paquetes principales:
- Numpy ( http://numpy.org/ )
- Matplotlib ( http://matplotlib.org/ )
- Pandas ( http://pandas.pydata.org/ )

**Leer y reproducir audio de silbido**
"""

#Importar Modulo scipy para leer y grabar audio
from scipy.io import wavfile 
AudioName = "Whistle.wav" # Archivo de Audio

# Salida fs: Frecuencia de muestreo and data: Señal de audio -> int16
fs, Audiodata = wavfile.read(AudioName)
print(f'Duracion = {Audiodata.shape[0]/fs} , Frecuencia de Muestreo = {fs} [=] Muestras/Seg' \
      f', Wav format = {Audiodata.dtype}')

ipd.Audio(AudioName) # Reproduce el audio directamente en el Jupyter notebook.

"""**Grafica de señal en el tiempo (Visualizar la Señal de Audio)**"""

import matplotlib.pyplot as plt #Libreria para realizar graficos

plt.rcParams['figure.figsize'] = (15, 5) # Definir el tamaño de graficas
plt.plot(Audiodata) # Audiodata es un numpy array
plt.text(0-5000, np.max(Audiodata), 'Máximo', fontsize = 16,bbox=dict(facecolor='red', alpha=0.5))
plt.title('Señal de Audio sin valores adecuados en los ejes',size=16);

"""**Definir los ejes adecuados**  
Las Señales de Audio se representan con la amplitud entre -1 y 1 , y el eje Horizontal en tiempo
"""

# Importar Numpy para realizar operaciones en el vector de audio

import numpy as np
plt.rcParams['figure.figsize'] = (15, 5) # Definir el tamaño de graficas
# Definir los valores de los datos de amplitud entre [-1 : 1] Audiodata.dtype es int16
AudiodataScaled = Audiodata/(2**15)

#definir los valores del eje x en milisegundos
timeValues = np.arange(0, len(AudiodataScaled), 1)/ fs # Convertir Muestras/Seg a Segundos
timeValues = timeValues * 1000  #Escala de tiempo en milisegundos

plt.plot(timeValues, AudiodataScaled);plt.title('Señal de Audio Con Informacion de Ejes',size=16)
plt.text(0-100, np.max(AudiodataScaled), 'Máximo', fontsize = 16,bbox=dict(facecolor='red', alpha=0.5))
plt.ylabel('Amplitud'); plt.xlabel('Tiempo (ms)');

"""**Grabar Archivos de Audio**

**Agarrar un INT 16**
"""

# Realizando algunos cambios en la señal de audio original
LessGaindata = AudiodataScaled/2.0 # Dividiendo por dos la amplitud de la señal

# Convertir nuevamente la señal a int16 patra gabar el archivo a 16 Bits @ 441000 Hz
LessGaindataInt = LessGaindata*(2.**15)
LessGaindataInt = LessGaindataInt.astype(np.int16)

wavfile.write('LessGainInt.wav',fs,LessGaindataInt)

"""### Se graba en formato punto flotante cuando no se indica nada



"""

# Escribir la señal de audio a un archivo
wavfile.write('LessGainFloat.wav',fs,LessGaindata)

# La ventaja es: La amplitud del archivo de audio estara entre [-1 : 1]
# Entonces cuadno se lee el archivo de audio ya estara bien el eje vertical

#Leer los archivos de audio grabados
fs1, FileInt = wavfile.read('LessGainInt.wav')
fs2, FileFloat = wavfile.read('LessGainFloat.wav')

plt.subplot(121)
plt.plot(timeValues,FileInt);plt.title('Señal de audio Int transformada',size=16)
plt.ylabel('Amplitud'); plt.xlabel('Tiempo (ms)');
plt.subplot(122)
plt.plot(timeValues,FileFloat);plt.title('Señal de audio Float transformada',size=16)
plt.ylabel('Amplitud'); plt.xlabel('Tiempo (ms)');

"""**Librería Librosa**  
Libreria para procesamiento de audio y musica en python, https://librosa.github.io/ La instalacion puede ser:  
- **Anaconda**: conda install -c conda-forge librosa  
- **Pepita**: pip install librosa

Además para leer archivos con compresión:conda install -c conda-forge ffmpeg

Las computadoras digitales solo pueden capturar estos datos en momentos discretos. La velocidad a la que una computadora captura datos de audio se denomina frecuencia de prueba (a menudo abreviado fs) o tasa de prueba (a menudo abreviado sr). La frecuencia de prueba de las grabaciones de CD es de 44100 Hz a 16 bits.

fs = muestra de frecuencia  
sr = frecuencia de muestreo

**Leer archivos de audio de silbido**
"""

import shutil
!mkdir Data
shutil.copy('Whistle.wav','./Data/Whistle.wav')
import librosa # importar a libreria librosa
print(f'Version de Librosa: {librosa.__version__}')
#x, sr = librosa.load('Data/Whistle.wav',sr=None) 
x, sr = librosa.load('Data/Whistle.wav',sr=None)
#Si no se especifica sr=None, entonces el audio se cambia de sampling a 22050
# automaticamente carga el audio como un float
print(f'Tamaño del archivo de audio = {x.shape}, Frecuencia de Muestreo = {sr} y tipo de dato = {x.dtype}')

"""**Señal en el tiempo (Visualizar la señal de Audio)**  
El cambio en la presión del aire en un momento determinado se representa gráficamente mediante un **gráfico de presión-tiempo**, o simplemente **forma de onda**.
"""

import matplotlib.pyplot as plt
import librosa.display
plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr); plt.title('Librosa configura los ejes automaticamente');

"""**Grabar Archivo de Audio**  
se puede realizar con la libreria soundfile

**sf.write** Graba un arreglo NumPy como un archivo WAV.
"""

import soundfile as sf
sf.write('Data/Librosa_audio.wav', x, sr)

"""#**Representación en Frecuencia - PARTE 1**
---

**CONTENIDO**  
- Transformada Rápida de Fourier (FFT)
- Espectro de magnitud(2D)
- Espectrograma (3D)
"""

AudioName

fs, Audiodata = wavfile.read(AudioName) # Leer archivo de audio
Audiodata = Audiodata / (2.**15) # definir amplitud de los datos entre [-1 : 1]

from scipy.fftpack import fft # modulo para calcular la transformada de fourier
n = len(Audiodata) 
AudioFreq = fft(Audiodata) # Calcular la transformada de Fourier
# La salida de la FFT es un array de numeros complejos
print(f'Tipo de datos de la fft = {AudioFreq.dtype} un valor cualquiera es = {AudioFreq[100]}')

# La salida de la FFT es un array de numeros complejos
# los numeros complejos se representan en Magnitud y fase
MagFreq = np.abs(AudioFreq) # Valor absoluto para obtener la magnitud

# Escalar por el numero de puntos para evitar que los valores de magnitud
# dependan del tamaño de la señal o de su frecuencia de muestreo
MagFreq = MagFreq / float(n)

plt.plot(MagFreq) #Espectro de magnitud
plt.ylabel('Magnitud'); plt.title('FFT total');

"""###**Escala de magnitud**
A menudo, la amplitud original de una señal en el dominio de tiempo o de la frecuencia no es perceptualmente relevante para los humanos como la amplitud convertida en otras unidades, Ej: usar una escala logarítmica.

Por ejemplo, consideramos un tono puro cuya amplitud aumenta de forma lineal. Definir la variable de tiempo:
"""

T = 5.0      # duracion en segundos
sr = 22050   # Frecuencia de muestreo en Hz
t = np.linspace(0, T, int(T*sr), endpoint=False)

"""Crear una señal que su amplitud aumente linealmente"""

amplitude = np.linspace(0, 1, int(T*sr), endpoint=False) # Amplitud variable en el tiempo
x = amplitude*np.sin(2*np.pi*440*t) #Señal sinusoidal

ipd.Audio(x, rate=sr)

# Grafica de la señal:
librosa.display.waveplot(x, sr=sr);

"""Ahora considere una señal cuya amplitud crece exponencialmente, es decir, el logaritmo de la amplitud es lineal:"""

amplitude = np.logspace(-2, 0, int(T*sr), endpoint=False, base=10.0)
x = amplitude*np.sin(2*np.pi*440*t)

ipd.Audio(x, rate=sr)

"""A pesar de que la amplitud crece exponencialmente, para nosotros, el aumento en el volumen parece más gradual. Este fenómeno es un ejemplo de la ley Weber-Fechner law ([**Wikipedia**](https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law)) que establece que la relación entre un estímulo y la percepción humana es logarítmica."""

# Las señales se representan en el espectro de potencia
# las señales tienen comportamiento logaritmico

# Calcular el espectro de potencia
MagFreq = MagFreq**2
plt.plot(10*np.log10(MagFreq)) #Espectro de potencia
plt.ylabel('Potencia (dB)'); plt.title('FFT total');

AudioFreq = AudioFreq[0:int(np.ceil((n+1)/2.0))]
# La salida de la FFT es un array de numeros complejos
MagFreq = np.abs(AudioFreq) # Valor absoluto para obtener la magnitud

# Escalar por el numero de puntos para evitar que los valores de magnitud
# dependan del tamaño de la señal o de su frecuencia de muestreo
MagFreq = MagFreq / float(n)
# Calcular el espectro de potencia
MagFreq = MagFreq**2

"""**Espectro de Magnitud (2D)**"""

# Importar Plotly para realizar graficos interactivos
# conda install -c anaconda plotly 
import plotly.express as px

# Verificar si nfft es impar para encontrar el punto de Nyquist en el espectro

if n % 2 > 0: # Si tenemos un numero impar de puntos de la fft
    MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
else:# Si tenemos un numero par de puntos de la fft
    MagFreq[1:len(MagFreq) -1] = MagFreq[1:len(MagFreq) - 1] * 2 

freqAxis = np.arange(0,int(np.ceil((n+1)/2.0)), 1.0) * (fs / n);
fig = px.line(x = freqAxis/1000.0, 
              y = 10*np.log10(MagFreq),
              title = 'Espectro Interactivo',
              labels={'x':'Frecuencia (kHz)', 'y':'Potencia (dB)'}
              ) #Espectro de potencia
fig.show()

## Solo por verificar una propiedad basica
# El valor RMS de la señal de audio en el tiempo
# debe ser igual a la raiz cuadrada de la suma de las magnitudes en la frecuencia

rms_val = np.sqrt(np.mean(Audiodata**2))

SumMagnitude = np.sqrt(np.sum(MagFreq))

print(f'RMS (tiempo) = {rms_val} y la suma de los picos de Magnitud (Frec) = {SumMagnitude}')
print('Los valores son iguales \U0001f603');

"""#**Representación en Frecuencia - PARTE 2**
---

**Espectrograma**

**Librerias paraobtener los espectogramas**

- Matplotlib ( https://matplotlib.org/api/_as_gen/matplotlib.pyplot.specgram.html )
- Scipy ( https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html )
- Librosa ()

**matplotlib**
"""

Fs, data = wavfile.read(AudioName)
data = data/(2.**15) # Escalar la señal entre [-1, 1] para un audio de 16 bits
N = 512 #Numero de puntos de la fft
from scipy import signal
Pxx, freqs, bins, im = plt.specgram(data, NFFT=N, Fs=Fs,window = signal.blackman(N),noverlap = 128)
plt.title('Espectrograma con Matplotlib',size=16);
plt.ylabel('Frecuencia [Hz]'); plt.xlabel('Tiempo [Seg]');

"""**Plotly (Interactivo) 3D**"""

# importar la libreria plotly offline para graficar
import plotly.offline as pyo # realizar graficas offline
from plotly.offline import iplot, init_notebook_mode #para poder graficar dentro del jupyter notebook
import plotly.graph_objs as go
import plotly
#init_notebook_mode() # inicializar el uso de pltly dentro del jupyter noteboo

from scipy.io import wavfile # scipy library to read wav files
AudioName = "Whistle.wav" # Audio File
fs, Audiodata = wavfile.read(AudioName)
Audiodata = Audiodata / (2.**15)

#Spectrogram
from scipy import signal
plt.figure()
N = 512 #Number of point in the fft
w = signal.blackman(N)
freqs, bins, Pxx = signal.spectrogram(Audiodata, fs,window = w,nfft=N)

# Plot with plotly
trace = [go.Surface(x= bins,y= freqs,z=10*np.log10(Pxx))]

layout = go.Layout(
    title = 'Espectrograma con plotly',
    yaxis = dict(title = 'Frecuencia'), # x-axis label
    xaxis = dict(title = 'Tiempo'), # y-axis label
);

fig = go.Figure(data=trace, layout=layout)
fig.show()
#iplot(fig, filename='Spectrogram');

"""**Plotly (Interactivo) Mapa de calor**"""

trace = [go.Heatmap(
    x= bins,
    y= freqs,
    z= Pxx,
    colorscale='Jet',
    )]
layout = go.Layout(
    title = 'Espectrograma',
    yaxis = dict(title = 'Frequency'), # x-axis label
    xaxis = dict(title = 'Time'), # y-axis label
    
)
fig = go.Figure(data=trace, layout=layout)

pyo.iplot(fig, filename='Espectrograma')

"""**Scipy**"""

#Espectro usando scipy
Fs, data = wavfile.read(AudioName)
data = data/(2.**15) # Escalar la señal entre [-1, 1] para un audio de 16 bits
N = 512 #Numero de puntos de la fft
from scipy import signal
f, t, Sxx = signal.spectrogram(data, Fs,window = signal.blackman(N),nfft=N)
plt.pcolormesh(t, f,10*np.log10(Sxx)) # Espectro de magnitud en dB
#plt.pcolormesh(t, f,Sxx) #Espectro de Magnitud Lineal
plt.ylabel('Frecuencia [Hz]')
plt.xlabel('Tiempo [seg]')
plt.title('Espectrograma usando scipy.signal',size=16);

"""**librosa**"""

X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X)) # convertir la amplitud a dB
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz');

"""**alias**"""

from scipy.signal import chirp
fs = 44100 # frecuencia de muestreo
T = 10 # Duracion en segundos
t = np.linspace(0, T, T*fs, endpoint=False)
# crear un sonido que va subiendo en frecuencia 20 Hz a 22050 Hz
w = np.float32(chirp(t, f0=20, f1=22050, t1=T, method='linear'))
wavfile.write('sine_sweep_44100.wav',fs,w)

plt.figure(figsize=(15,3))
plt.specgram(w, Fs=44100); plt.colorbar(); plt.title('Espectrograma Sine sweep')
_=plt.axis((0,10,0,22050))
ipd.Audio('sine_sweep_44100.wav')

down_sampled = w[::2] # tomar datos con un brinco de 2
wavfile.write('sine_sweep_downsampled.wav',22050, down_sampled)
plt.figure(figsize=(16,4))
plt.specgram(down_sampled, Fs=22050); plt.colorbar();plt.title('Especrograma Bad Downsampling')
_=plt.axis((0,10,0,22050))
ipd.Audio('sine_sweep_downsampled.wav')

"""#**Analisis en el tiempo y frecuenxia de la caracteristica del _timbre_ en señales musicales**

El timbre es la calidad del sonido que distingue el tono de diferentes instrumentos y voces, incluso si los sonidos tienen el mismo tono y volumen.

**Variaciones en el Tiempo**  
Una característica del timbre es su evolución temporal. La **envolvente** de una señal es una curva suave que se aproxima a los extremos de amplitud de una forma de onda a lo largo del tiempo.

Cuando se produce un sonido su volumen y el contenido espectral cambia a través del tiempo. El “ataque” (ataque) y “decay” (decaimiento) tienen un gran efecto sobre las cualidades del sonido la llamada envolvente [ADSR (Attack Decay Sustain Release)](https://es.wikipedia.org/wiki/Sintetizador#Envolvente_ADSR) . El comportamiento de una envolvente de ADSR está especificado a través de cuatro parámetros:

- **Attack time (tiempo de ataque)**: es el tiempo que le toma ir de un valor inicial a un valor pico.
- **Decay time (tiempo de decaimiento)**: es el tiempo, posterior al ataque, que le toma llegar a un nivel determinado de sustain.
- **Sustain level (tiempo de sostenimiento)**: es el nivel que mantiene la secuencia del sonido durante el tiempo que dure el mismo.
- **Release time (tiempo de liberación)**: es el tiempo que le toma decaer al sonido, después del sustain, a un nivel igual a cero.

La envolvente ADSR es una simplificacion y no obstante modela todos los sonidos
![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/ADSR_parameter.svg/640px-ADSR_parameter.svg.png)

**Variaciones en la frecuencia**  
Otra propiedad utilizada para caracterizar el timbre es la existencia de parciales y sus amplitudes relativas. Los **parciales** son las frecuencias dominantes en un tono, siendo el más parcial bajo la **frecuencia fundamental**.

Los parciales de un sonido se visualizan con un **espectrograma**. Un espectrograma muestra la intensidad de los componentes de frecuencia a lo largo del tiempo.

**Tono puro**  
Vamos a crear un tono artificial a 1047 HZ, equivalente a un DO en la sexta octava (C6)
"""

T = 2.0 # segundos
f0 = 1047.0 #Frecuencia del tono
sr = 22050 # Frecuencia de Muestreo
t = np.linspace(0, T, int(T*sr), endpoint=False) # creacion del eje de tiempo
x = 0.1*np.sin(2*np.pi*f0*t) # Señal Sinusoidal
ipd.Audio(x, rate=sr)

"""espectro del tono puro"""

X = fft(x[:4096])
X1_mag = np.absolute(X)        # Espectro de magnitud
f = np.linspace(0, sr, 4096)  # frequency variable
px.line(x = f[:2000], y= 10*np.log10(X1_mag[:2000]), labels={'x':'Frecuencia [Hz]'})

"""**Oboe**  
Sonido de un oboe tocando un C6:
"""

sr,x = wavfile.read('oboe_c6.wav')
ipd.Audio(x, rate=sr)

x=x/(2**15) # Normalizar el audio entre 1 y -1
print(x.shape)

"""Espectro del oboe"""

X = fft(x[10000:14096])
X2_mag = np.absolute(X)
px.line(x =f[:2000], y= 10*np.log10(X2_mag[:2000]), labels={'x':'Frecuencia [Hz]'}) # Espectro de magnitud

"""**Clarinete**  
Clarinete tocando un C6
"""

x, sr = librosa.load('clarinet_c6.wav')
ipd.Audio(x, rate=sr)

print(x.shape)

"""Espectro del clarinete"""

X = fft(x[10000:14096])
X3_mag = np.absolute(X)
px.line(x =f[:2000], y= 10*np.log10(X3_mag[:2000]), labels={'x':'Frecuencia [Hz]'}) # Espectro de magnitud

"""**Superposicion de las señales musicales en frecuencia paracomparacion de contenido espectral**"""

# Grafica con Matplotlib
#plt.plot(f[:2000], 10*np.log10(X1_mag[:2000]),'r',label = 'Sinusoidal') # magnitude spectrum
#plt.plot(f[:2000], 10*np.log10(X2_mag[:2000]),'b',label = 'Oboe') # magnitude spectrum
#plt.plot(f[:2000], 10*np.log10(X3_mag[:2000]),'g',label = 'Clarinete') # magnitude spectrum
#plt.title('Espectro de Sinusoide, Oboe y Clarinete en la misma nota');plt.legend();

#Grafica con Plotly
from itertools import cycle

fig = px.line(x = f[:2000], 
        y= [10*np.log10(X1_mag[:2000]), 10*np.log10(X2_mag[:2000]), 10*np.log10(X3_mag[:2000])],
        title = 'Espectro de Sinusoide, Oboe y Clarinete en la misma nota'
        )
names = cycle(['Sinusoidal', 'Oboe', 'Clarinete'])
fig.for_each_trace(lambda t:  t.update(name = next(names)))
fig.show()

"""Observe la diferencia en las amplitudes relativas de los componentes parciales. Las tres señales tienen aproximadamente el mismo tono y frecuencia fundamental, sin embargo, sus timbres son diferentes.

#**Psicoacustica**
---
"""

import numpy as np
import IPython.display as ipd
import librosa, librosa.display
import matplotlib.pyplot as plt

"""**Escala de magnitud**  
A menudo, la amplitud original de una señal en el dominio de tiempo o de la frecuencia no es perceptualmente relevante para los humanos como la amplitud convertida en otras unidades, Ej: usar una escala logarítmica.

Por ejemplo, consideramos un tono puro cuya amplitud aumenta de forma lineal. Definir la variable de tiempo:
"""

T = 5.0      # duracion en segundos
sr = 22050   # Frecuencia de muestreo en Hz
t = np.linspace(0, T, int(T*sr), endpoint=False)

"""Crear una señal que su amplitud aumente linealmente"""

amplitude = np.linspace(0, 1, int(T*sr), endpoint=False) # Amplitud variable en el tiempo
x = amplitude*np.sin(2*np.pi*440*t) #Señal sinusoidal

ipd.Audio(x, rate=sr)

"""Gráfica de la señal:"""

librosa.display.waveplot(x, sr=sr);

"""Ahora considere una señal cuya amplitud crece exponencialmente, es decir, el logaritmo de la amplitud es lineal:"""

amplitude = np.logspace(-2, 0, int(T*sr), endpoint=False, base=10.0)
x = amplitude*np.sin(2*np.pi*440*t)

ipd.Audio(x, rate=sr)

"""A pesar de que la amplitud crece exponencialmente, para nosotros, el aumento en el volumen parece más gradual. Este fenómeno es un ejemplo de la ley Weber-Fechner law ( Wikipedia ) que establece que la relación entre un estímulo y la percepción humana es logarítmica.

**Percepción de la amplitud según la frecuencia**
"""

T = 4.0      # duracion en segundos
sr = 44100   # Frecuencia de muestreo en Hz
t = np.linspace(0, T, int(T*sr), endpoint=False)

"""**100 Hz**"""

# 100 Hz
x1 = np.sin(2*np.pi*100*t)
ipd.Audio(x1, rate=sr)

"""**250 Hz**"""

# 250 Hz
x2 = np.sin(2*np.pi*250*t)
ipd.Audio(x2, rate=sr)

"""**400 Hz**"""

# 400 Hz
x3 = np.sin(2*np.pi*400*t)
ipd.Audio(x3, rate=sr)

"""**1000 Hz**"""

# 1000 Hz
x4 = np.sin(2*np.pi*1000*t)
ipd.Audio(x4, rate=sr)

"""**4000 Hz**"""

# 4000 Hz
x5 = np.sin(2*np.pi*4000*t)
ipd.Audio(x5, rate=sr)

"""**10000 Hz**"""

# 10000 Hz
x6 = np.sin(2*np.pi*10000*t)
ipd.Audio(x6, rate=sr)

"""**15000 Hz**"""

# 15000 Hz
x7 = np.sin(2*np.pi*15000*t)
ipd.Audio(x7, rate=sr)

"""**18000 Hz**"""

# 18000 Hz
x8 = np.sin(2*np.pi*18000*t)
ipd.Audio(x8, rate=sr)

"""**Grafica de las señales**"""

plt.figure(figsize=(12,10))
for n in range(8):
    plt.subplot(4,2,n+1)
    plt.plot(eval('x'+str(n+1))[:1000])# graficar los primeros 1000 valores

"""**Enmascaramiento Simultáneo**  
**400 Hz**
"""

# Audio de 400 Hz
wavfile.write('./Data/400Hz.wav',22050, x3)

x1, sr1 = librosa.load('./Data/400Hz.wav',sr=None)
X1 = librosa.stft(x1)
Xdb1 = librosa.amplitude_to_db(abs(X1)) # convertir la amplitud a dB
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb1, sr=sr1, x_axis='time', y_axis='hz');
ipd.Audio(x1,rate=sr1)

"""**500 Hz**"""

x = np.sin(2*np.pi*500*t)
wavfile.write('./Data/500Hz.wav',22050, x)

x2, sr2 = librosa.load('./Data/500Hz.wav',sr=None)
X2 = librosa.stft(x2)
Xdb2 = librosa.amplitude_to_db(abs(X2)) # convertir la amplitud a dB
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb2, sr=sr2, x_axis='time', y_axis='hz');
ipd.Audio(x2,rate=sr2)

"""**400 Hz + 500 Hz**"""

x_suma = x1 + x2
wavfile.write('./Data/400Hz+500Hz.wav',22050, x_suma)

x3, sr3 = librosa.load('./Data/400Hz+500Hz.wav',sr=None)
X3 = librosa.stft(x3)
Xdb3 = librosa.amplitude_to_db(abs(X3)) # convertir la amplitud a dB
plt.figure(figsize=(14, 5))
librosa.display.specshow(Xdb3, sr=sr3, x_axis='time', y_axis='hz');
ipd.Audio(x3,rate=sr3)

"""**audios finales**"""

ipd.display(ipd.Audio(x1,rate=sr1)) #400 Hz
ipd.display(ipd.Audio(x2,rate=sr2)) #500 Hz
ipd.display(ipd.Audio(x3,rate=sr3)) #400 Hz + 500 Hz

"""#**Extracción de Características de Audio**
---

**Extracción de Características (Ejemplo)**  
Debemos extraer las características de nuestra señal de audio que son más relevantes para el problema que estamos tratando de resolver. Por ejemplo, si queremos clasificar algunos sonidos por el timbre, buscaremos características que distingan los sonidos por su timbre y no por su tono. Si queremos realizar la detección de tono, queremos características que distingan el tono y no el timbre.

Este proceso se conoce como extracción de características.

Vamos a hacer un ejemplo con veinte archivos de audio: diez muestras de bombo (Kick Drum) y diez muestras de redoblante de batería (snare drum). Cada archivo de audio contiene un golpe de batería.
"""

# Importar librerias
from pathlib import Path
from scipy.io import wavfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display
import os

"""**Celda para activar la funcion de borrar carpetas con contenido**"""

#from shutil import rmtree
#rmtree("/Data/drum_samples")

"""**instalacion del comando wget para descargar ficheros de internet**"""

pip install wget

"""**Crear directorio donde descargar los archivos de audio snare y kick**"""

import shutil 
import wget
os.makedirs('/content/Data/drum_samples/train')

"""**Importar los 10 archivos snare que requiere el notebook**"""

for num in range(1, 10):
    wdir = 'https://github.com/stevetjoa/musicinformationretrieval.com/blob/gh-pages/audio/drum_samples/test/snare_0{}.mp3'.format(num)
    wget.download(wdir)
    mover='snare_0{}.mp3'.format(num)
    shutil.move(mover,'/content/Data/drum_samples/train')
!wget https://github.com/stevetjoa/musicinformationretrieval.com/blob/gh-pages/audio/drum_samples/test/snare_10.mp3 \
   -P /content/Data/drum_samples/train

"""**Importar los 10 archivos kick que requiere el notebook**"""

for num in range(1, 10):
    wdir = 'https://github.com/stevetjoa/musicinformationretrieval.com/blob/gh-pages/audio/drum_samples/test/kick_0{}.mp3'.format(num)
    wget.download(wdir) 
    mover='kick_0{}.mp3'.format(num)
    shutil.move(mover,'/content/Data/drum_samples/train')
!wget https://github.com/stevetjoa/musicinformationretrieval.com/blob/gh-pages/audio/drum_samples/test/kick_10.mp3 \
   -P /content/Data/drum_samples/train