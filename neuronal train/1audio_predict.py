import numpy as np
import soundfile
# matplotlib complains about the behaviour of librosa.display, so we'll ignore those warnings:
#import warnings; warnings.filterwarnings('ignore')
import librosa

import joblib




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





#joblib.dump(model, 'modelo_mlp_entrenado.pkl')
loaded_model = joblib.load('modelo_mlp_entrenado.pkl')

audio_path_prueba = '/home/victor/Escritorio/tfg/tests/audios/WAV/prueba_fold/delante_rasp_45-.wav'
audio_prueba = get_features(audio_path_prueba)

audio_prueba = audio_prueba.reshape(1, -1)

# Predict with Random Forest
prediccion = loaded_model.predict(audio_prueba)
#print(f'Clase predicha: {prediccion[0]}')
print(prediccion[0])
