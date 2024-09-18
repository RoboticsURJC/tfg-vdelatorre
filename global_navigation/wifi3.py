import subprocess
from math import sqrt
import time
import statistics


# Función para obtener la intensidad de la señal de un punto de acceso Wi-Fi
def get_signal_strength(ap_name):
    try:
        # Usamos iwconfig para obtener los detalles de la red Wi-Fi
        result = subprocess.check_output(["iwconfig","wlan0"]).decode('utf-8')
        lines = result.split('\n')
        for line in lines:
            
            if "level" in line:
                # Parseamos el nivel de la señal                
                parts = line.split()
                for part in parts:
                    if "level=" in part:
                        signal_level = part.split('=')[1]
                        print(signal_level,'\n')
                        return int(signal_level)
    except Exception as e:
        print(f"Error al obtener la señal Wi-Fi: {e}")
        return None
        
# Función para tomar múltiples muestras de RSSI y calcular la media
def get_average_rssi(interface, samples, delay):
    rssi_values = []
    for _ in range(samples):
        rssi = get_signal_strength(interface)
        if rssi is not None:
            rssi_values.append(rssi)
        time.sleep(delay)  # Esperar un poco entre muestras

    if rssi_values:
        avg_rssi = sum(rssi_values) / len(rssi_values)
        return avg_rssi
    return None

#mediana
def get_median_rssi(interface, samples, delay):
    rssi_values = []
    for _ in range(samples):
        rssi = get_signal_strength(interface)
        if rssi is not None:
            rssi_values.append(rssi)
        time.sleep(delay)
    
    if rssi_values:
        median_rssi = statistics.median(rssi_values)
        return median_rssi
    return None

# Función para calcular la distancia aproximada basada en el RSSI
def calculate_distance(rssi, A=-44, n=2):
    """
    rssi: el nivel de señal en dBm
    A: valor RSSI a 1 metro (dependerá del AP, por defecto -30)
    n: factor de propagación (depende del entorno, en interiores suele ser 2-3)
    """
    return 10 ** ((A - rssi) / (10 * n))

# Función para conectarse a una red Wi-Fi específica
def connect_to_wifi(ssid, password):
    try:
        # Usa nmcli para conectarse a la red Wi-Fi
        subprocess.run(["nmcli", "d", "wifi", "connect", ssid, "password", password], check=True)
        print(f"Conectado a {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error al conectar a {ssid}: {e}")
        
def connect_to_home_wifi(ssid, password):
    try:
        # Usa nmcli para conectarse a la red Wi-Fi
        subprocess.run(["nmcli", "d", "wifi", "connect", ssid, "password", password], check=True)
        print(f"Conectado a {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error al conectar a {ssid}: {e}")

# Información del punto de acceso (incluye coordenadas)
ap_info = {
    "ssid": "IphoneVictor",
    "password": "polopolo",
    "coords": (0, -2)  # Coordenadas del punto de acceso en el mapa
}

home_wifi = {
    "ssid": "MOVISTAR-WIFI6-BC08",
    "password": "WFXR97K377JXUXCMa33X",
    "coords": (20, -20)  # Coordenadas del punto de acceso en el mapa
}

# Conectarse al punto de acceso y obtener la señal
connect_to_wifi(ap_info['ssid'], ap_info['password'])


# Espera a que la conexión se estabilice
subprocess.run(["sleep", "5"])


#rssi = get_signal_strength(ap_info['ssid'])

#rssi = get_average_rssi("wlan0", 10, 1)
rssi = get_median_rssi("wlan0", 10, 1)

#rssi = round(rssi)
print("Media: ", rssi)


if rssi is not None:
    distance = calculate_distance(rssi)
    print(f"Distancia al AP: {distance:.2f} metros")
    print(f"Coordenadas del AP: {ap_info['coords']}")
else:
    print("No se pudo obtener la señal del AP")
    
    
#connect_to_wifi(home_wifi['ssid'], home_wifi['password'])

