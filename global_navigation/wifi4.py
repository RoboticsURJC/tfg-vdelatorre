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
def calculate_distance(rssi, A, n=2.5):
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
        
def trilateration(p1,p2,p3,d1,d2,d3):
    
    A = 2 * (p2[0] - p1[0])
    B = 2 * (p2[1] - p1[1])
    C = 2 * (p3[0] - p1[0])
    D = 2 * (p3[1] - p1[1])
    
    E = d1**2 - d2**2 - p1[0]**2 + p2[0]**2 -p1[1]**2 + p2[1]**2
    F = d1**2 - d3**2 - p1[0]**2 + p3[0]**2 -p1[1]**2 + p3[1]**2    
    
    x = (E - F * ( D / B)) / (A - C * (D / B))
    y = (E - A * x ) / B
    
    return x,y
    
    
n = 0.5

# Información del punto de acceso (incluye coordenadas)
iphone_victor = {
    "ssid"    : "IphoneVictor",
    "password": "polopolo",
    "coords"  : (-1 * n, 2 * n),  # Coordenadas del punto de acceso en el mapa
    "dBm"     : -50 #potencia a 1 metro

}

iphone_papa = {
    "ssid"    : "iPhone",
    "password": "0Manuel0",
    "coords"  : (1 * n, 1 * n) , # Coordenadas del punto de acceso en el mapa
    "dBm"     : -51 #potencia a 1 metro

}

iphone_mama = {
    "ssid"    : "iPhoneManoli",
    "password": "palapala",
    "coords"  : (-2 * n, 0 * n),  # Coordenadas del punto de acceso en el mapa
    "dBm"     : -54 #potencia a 1 metro
}

home_wifi = {
    "ssid": "MOVISTAR-WIFI6-BC08",
    "password": "WFXR97K377JXUXCMa33X",
    "coords": (20, -20)  # Coordenadas del punto de acceso en el mapa
}

'''
ap_info = iphone_victor

if ap_info['ssid'] == "iPhone":
    print("papaaaaaaa")
    A = -42
elif ap_info['ssid'] == "IphoneVictor":
    print("victorrrrr")
    A = -38
else:
    print("mamaaaaaaa")
    A = -36
'''
    

ap_info =[iphone_victor, iphone_papa, iphone_mama]
distances = []

for i in range(3):

    # Conectarse al punto de acceso y obtener la señal
    connect_to_wifi(ap_info[i]['ssid'], ap_info[i]['password'])


    # Espera a que la conexión se estabilice
    subprocess.run(["sleep", "5"])


    #rssi = get_signal_strength(ap_info['ssid'])

    #rssi = get_average_rssi("wlan0", 10, 1)
    rssi = get_median_rssi("wlan0", 12, 1)

    #rssi = round(rssi)
    print("Media: ", rssi)


    if rssi is not None:
        dist = calculate_distance(rssi,ap_info[i]['dBm'])
        print(f"Distancia al AP: {dist:.2f} metros")
        print(f"Coordenadas del AP: {ap_info[i]['coords']}")
        
        distances.append(dist)
    else:
        print("No se pudo obtener la señal del AP")
        
        
    
#distances = [1.2,0.76,1.0] # con distancias exactas sale que las raspberry está en la -0.13 , -0.4
print("DISTANCIAS" , distances[0]," , " ,distances[1]," , " ,distances[2])

posx, posy = trilateration(iphone_victor['coords'],iphone_papa['coords'], iphone_mama['coords'], distances[0],distances[1], distances[2])
    
posx_grid = posx / 0.5
posy_grid = posy / 0.5
print("X: ",posx_grid, " Y :", posy_grid)
    
connect_to_wifi(home_wifi['ssid'], home_wifi['password'])

    
    
    
    

