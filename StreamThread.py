from threading import Thread, Event
import numpy as np
import sounddevice as sd

class StreamThread(Thread):
    def __init__(self, app):
        super().__init__()
        self.dispoitivo_input = 1
        self.dispoitivo_output = 4
        self.tamano_bloque = 8000
        self.frecuencia_muestreo = 44100
        self.canales = 1
        self.tipo_dato = np.int16
        self.latencia = "high"
        self.app = app

    def callback_stream(self, indata, outdata, frames, time, status):

        data = indata[:,0]
        transformada = np.fft.rfft(data)
        periodo_muestreo = 1/self.frecuencia_muestreo
        frecuencias = np.fft.rfftfreq(len(data), periodo_muestreo)
        frecuencia_fundamental = frecuencias[np.argmax(np.abs(transformada))]

        # print("Frecuencia Fundamental: ", frecuencia_fundamental)

        if frecuencia_fundamental > 200:
            self.app.comprobar_color = True
        if frecuencia_fundamental < 200:
            self.app.comprobar_color = False

        # if frecuencia_fundamental > 595 and frecuencia_fundamental < 605:
        #     print("Pintar la nave de rojo")
        #     self.app.nave.herido = True
        # else:
        #     self.app.nave.herido = False

        #Obtener frecuencia fundamental
        #Actualizar el texto de la etiqueta_valor_ff para que muestre la frecuencia fundamental

        #app.etiqueta_valor_ff["text"] = frec_fundamental
        return

    def run(self):
        try:
            self.event = Event()
            with sd.Stream(
                device=(self.dispoitivo_input, self.dispoitivo_output), #Se eligen dispositivos (entrada, salida)
                blocksize= self.tamano_bloque, # 0 significa que la tarjeta de sonido decide el mejor tamaño
                samplerate= self.frecuencia_muestreo, # frecuencia de muestreo
                channels= self.canales, #numero de canales
                dtype= self.tipo_dato, #Tipo de dato (profundidad de bits)
                latency=self.latencia, # Latencia, que tanto tiempo pasa desde entrada hasta la salida
                callback= self.callback_stream
            ) as self.stream:
                self.event.wait()

        except Exception as e:
            print(str(e))