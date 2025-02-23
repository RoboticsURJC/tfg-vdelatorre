#!/usr/bin/python3

import numpy as np
import soundfile
# matplotlib complains about the behaviour of librosa.display, so we'll ignore those warnings:
#import warnings; warnings.filterwarnings('ignore')
import librosa

import joblib
import RPi.GPIO as GPIO
import time
import subprocess
import sys

#from motor_new import move_forward, cleanup

import threading

GPIO.setwarnings(False)

ena = 18
enb = 12
out1 = 20 #right coil MARRON
out2 = 26 #right coil BLANCO
out3 = 19 # left coil NEGRO
out4 = 16 # left coil ROJO

GPIO.setmode( GPIO.BCM )
GPIO.setup( ena, GPIO.OUT )
GPIO.setup( enb, GPIO.OUT )

GPIO.setup( out1, GPIO.OUT )
GPIO.setup( out2, GPIO.OUT )
GPIO.setup( out3, GPIO.OUT )
GPIO.setup( out4, GPIO.OUT )

pa = GPIO.PWM(ena,500)
pb = GPIO.PWM(enb,500)

pa.start(100)
pb.start(100)


def feature_chromagram(waveform, sample_rate):
    # STFT computed here explicitly; mel spectrogram and MFCC functions do this under the hood
    stft_spectrogram=np.abs(librosa.stft(waveform))
    # Produce the chromagram for all STFT frames and get the mean of each column of the resulting matrix to create a feature array
    chromagram=np.mean(librosa.feature.chroma_stft(S=stft_spectrogram, sr=sample_rate).T,axis=0)
    #print(chromagram)
    return chromagram

def feature_melspectrogram(waveform, sample_rate):
    # Produce the mel spectrogram for all STFT frames and get the mean of each column of the resulting matrix to create a feature array
    # Using 8khz as upper frequency bound should be enough for most speech classification tasks
    # 128 features

    melspectrogram=np.mean(librosa.feature.melspectrogram(y=waveform, sr=sample_rate, n_mels=128, fmax=8000).T,axis=0)
    return melspectrogram

def feature_mfcc(waveform, sample_rate):
    # Compute the MFCCs for all STFT frames and get the mean of each column of the resulting matrix to create a feature array
    # 40 filterbanks = 40 coefficients
    # 40 features
    mfc_coefficients=np.mean(librosa.feature.mfcc(y=waveform, sr=sample_rate, n_mfcc=40).T, axis=0)
    return mfc_coefficients

def get_features(file):
    # load an individual soundfile
     with soundfile.SoundFile(file) as audio:
        waveform = audio.read(dtype="float32")
        sample_rate = audio.samplerate
        # compute features of soundfile
        chromagram = feature_chromagram(waveform, sample_rate)
        melspectrogram = feature_melspectrogram(waveform, sample_rate)
        mfc_coefficients = feature_mfcc(waveform, sample_rate)

        feature_matrix=np.array([])

        print("Chromagram shape:", chromagram.shape)
        print("Melspectrogram shape:", melspectrogram.shape)
        print("MFC coefficients shape:", mfc_coefficients.shape)

        # use np.hstack to stack our feature arrays horizontally to create a feature matrix
        feature_matrix = np.hstack((chromagram, melspectrogram, mfc_coefficients))#180 features in total
        #print(feature_matrix)
        return feature_matrix

####### Default Random Forest  ########
'''model = RandomForestClassifier(
    random_state = 69
)'''



#hilo1 = threading.Thread(target=move_forward)

#//////////////////////////////////////////////////
#comando_arecord = ['/usr/bin/arecord', '-D', 'hw:3,0' ,'-d' ,'2' ,'-f' ,'cd' ,'/home/torre/Desktop/WAV/prueba_fold/dorm.wav' ,'-c' ,'1' ] 
comando_arecord = ['/usr/bin/arecord', '-f', 'S16_LE', '-r' ,'44000' ,'-D', 'hw:3,0' ,'-d' ,'2' ,'-f' ,'cd' ,'/home/torre/Desktop/WAV/prueba_fold/dorm.wav' ,'-c' ,'1' ] 

proceso = subprocess.run(comando_arecord, check=True)
result = subprocess.run([sys.executable, "-c", "print('ocean')"])


#/////////////////////////////////////////////////
#joblib.dump(model, 'modelo_mlp_entrenado.pkl')
loaded_model = joblib.load('modelo_final_entrenado.pkl')

audio_path_prueba = '/home/torre/Desktop/WAV/prueba_fold/dorm.wav'
audio_prueba = get_features(audio_path_prueba)

audio_prueba = audio_prueba.reshape(1, -1)

# Predict with Random Forest
prediccion = loaded_model.predict(audio_prueba)
#print(f'Clase predicha: {prediccion[0]}')
print(prediccion[0])

#if(prediccion[0] == "delante"):
 #   print("delante")
 
#hilo1.start()

#hilo1.join()


'''
elif(prediccion[0] == "atras"):
    print("atras")
    move_ccw()
'''



#cleanup()
exit( 0 )

