import os

def rename_audio_files(folder_path):
    # Obtener la lista de archivos en la carpeta
    audio_files = [file for file in os.listdir(folder_path) if file.endswith(".wav")]

    # Iterar sobre cada archivo y renombrarlo
    for i, file in enumerate(audio_files, start=461):
        # Construir el nuevo nombre del archivo
        new_name = f"ej{i}-08-.wav"

        # Crear la ruta completa del archivo antiguo y nuevo
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)

        # Renombrar el archivo
        os.rename(old_path, new_path)

        print(f'Renamed: {old_path} -> {new_path}')

# Ruta de la carpeta que contiene los archivos de audio
carpeta_audio = '/home/victor/Escritorio/tfg/tests/audios/WAV/cambiar_nombres/'


# Llamar a la función para renombrar los archivos en la carpeta especificada
rename_audio_files(carpeta_audio)
