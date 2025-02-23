import subprocess
import time
import statistics
import numpy as np

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

#mediana
def get_median_rssi(interface):
    rssi_values = []
    for _ in range(5):
        rssi = get_signal_strength(interface)
        if rssi is not None:
            rssi_values.append(rssi)
        time.sleep(1)
    
    if rssi_values:
        median_rssi = statistics.median(rssi_values)
        return median_rssi
    return None

# Función para calcular la distancia en base al RSSI
def calculate_distance(rssi, A, n=2.5):
    return 10 ** ((A - rssi) / (10 * n))

# Función para conectarse a una red Wi-Fi
def connect_to_wifi(ssid, password):
    try:
        subprocess.run(["nmcli", "d", "wifi", "connect", ssid, "password", password], check=True)
        print(f"Conectado a {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error al conectar a {ssid}: {e}")

# Función para resolver trilateración con mínimos cuadrados
def multilateration(ap_coords, distances):
    A, b = [], []
    for i in range(4):
        x, y = ap_coords[i]
        A.append([2 * (x - ap_coords[0][0]), 2 * (y - ap_coords[0][1])])
        b.append(distances[0]**2 - distances[i]**2 - ap_coords[0][0]**2 + x**2 - ap_coords[0][1]**2 + y**2)
    A, b = np.array(A[1:]), np.array(b[1:])
    position = np.linalg.lstsq(A, b, rcond=None)[0]
    return position[0], position[1]

def robot_position():
    
    # Definición de los puntos de acceso Wi-Fi
    n = 0.5
    # Información del punto de acceso (incluye coordenadas)
    AP1 = {
        "ssid"    : "IphoneVictor",
        "password": "polopolo",
        "coords"  : (3 * n, 0 * n),  # Coordenadas del punto de acceso en el mapa
        "dBm"     : -50 #potencia a 1 metro

    }

    AP2 = {
        "ssid"    : "iPhone",
        "password": "0Manuel0",
        "coords"  : (10 * n, 5 * n) , # Coordenadas del punto de acceso en el mapa
        "dBm"     : -51 #potencia a 1 metro

    }

    AP3 = {
        "ssid"    : "iPhoneManoli",
        "password": "palapala",
        "coords"  : (-3 * n, 1 * n),  # Coordenadas del punto de acceso en el mapa
        "dBm"     : -54 #potencia a 1 metro
    }

    AP4 = {
        "ssid": "MOVISTAR-WIFI6-BC08",
        "password": "WFXR97K377JXUXCMa33X",
        "coords": (-13 * n, 10 * n)  # Coordenadas del punto de acceso en el mapa
    }


    ap_info =[AP1, AP2, AP3, AP4]

        
    distances = []
    for i in range(4):
        connect_to_wifi(ap_info[i]['ssid'], ap_info[i]['password'])
        time.sleep(2)  # Espera para estabilizar la conexión
        rssi = get_median_rssi("wlan0")
        if rssi is not None:
            dist = calculate_distance(rssi,ap_info[i]['dBm'])
            distances.append(dist)
            print(f"Distancia al AP: {dist:.2f} metros")
            print(f"Coordenadas del AP: {ap_info[i]['coords']}")
        else:
            distances.append(None)
            print("No se pudo obtener la señal del AP")
      


    coords_list = [(-1 * n, 2 * n),(1 * n, 1 * n),(-2 * n, 0 * n),(0 * n, 1 * n)]

    #elimina los valores None si los hubiese
    valid_distances = list(filter(None, distances))




    if len(valid_distances) == 4:
        #se selecciona los 4 primeros puntos de acceso
        posx, posy = multilateration(coords_list, valid_distances)
        
        posx_grid = posx / 0.5
        posy_grid = posy / 0.5

        print(f"Posición grid: X = {posx_grid/0.5}, Y = {posy_grid/0.5}")
        print("X: ",int(posx_grid), " Y :", int(posy_grid))
        return int(posx_grid), int(posy_grid)

    else:
        print("No hay suficientes datos para calcular la ubicación.")
        return None
#x,y = robot_position()
#print(x,y)

