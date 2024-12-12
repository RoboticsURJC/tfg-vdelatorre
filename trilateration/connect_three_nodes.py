import subprocess
from math import sqrt
import time
import statistics


# Función para obtener la intensidad de la señal de un punto de acceso Wi-Fi
def get_signal_strength(ap_name):
    try:
        # Usamos iwconfig para obtener los detalles de la red Wi-Fi
        result = subprocess.check_output(["iwconfig","wlan0"]).decode('utf-8')
        
        print(result)
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
cont = 0
with open("rssi_values_new_3.txt","a") as file:
    
    file.write("\n\n")

    for i in range(140):
        cont+=1
        print("CONTADOR VA POR: ", cont)
        file.write("\n")

        for i in range(3):

            # Conectarse al punto de acceso y obtener la señal
            connect_to_wifi(ap_info[i]['ssid'], ap_info[i]['password'])


            # Espera a que la conexión se estabilice
            subprocess.run(["sleep", "5"])


            rssi = get_signal_strength(ap_info[i]['ssid'])
            print("RSSI FINAL: ", rssi)
            file.write(f"{rssi},")

            #rssi = get_average_rssi("wlan0", 10, 1)
            #rssi = get_median_rssi("wlan0", 12, 12
            #if (i < 2):
             #   file.write(f"{rssi},")
            #else:
             #   file.write(f"{rssi},")
        print("---------------------------------------------------------------------------------------")
        #connect_to_wifi(home_wifi['ssid'], home_wifi['password'])



            
            
        


        
        
        
        

