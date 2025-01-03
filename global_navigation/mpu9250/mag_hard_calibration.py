######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code reads data from the MPU9250/MPU9265 board
# (MPU6050 - accel/gyro, AK8963 - mag)
# and solves for tje hard iron offset for a
# magnetometer using a calibration block
#
#
######################################################
#
# wait 5-sec for IMU to connect
import time,sys,math

sys.path.append(".")
t0 = time.time()
start_bool = False # if IMU start fails - stop calibration
while time.time()-t0<5:
    try: 
        from mpu9250_i2c import *
        start_bool = True
        break
    except:
        continue
import numpy as np
import csv
import matplotlib.pyplot as plt

time.sleep(2) # wait for mpu to load

# Variables para el filtro de paso bajo
filtered_magx, filtered_magy = 0, 0
#DECLINATION = -1 * 3.19  # Declinación magnética
DECLINATION = 0.5  # Declinación magnética
heading_angle_in_degrees = 0

# Función de filtro de paso bajo
def low_pass_filter(prev_value, new_value):
    return 0.85 * prev_value + 0.15 * new_value

# Función para obtener la dirección de la brújula
def compass(angle):
    if angle > 337 or angle <= 22:
        direction = 'North'
    elif angle > 22 and angle <= 67:
        direction = 'North East'
    elif angle > 67 and angle <= 112:
        direction = "East"
    elif angle > 112 and angle <= 157:
        direction = "South East"
    elif angle > 157 and angle <= 202:
        direction = "South"
    elif angle > 202 and angle <= 247:
        direction = "South West"
    elif angle > 247 and angle <= 292:
        direction = "West"
    elif angle > 292 and angle <= 337:
        direction = "North West"
    return direction
    
# 
#####################################
# Mag Calibration Functions
#####################################
#
def outlier_removal(x_ii,y_ii):
    x_diff = np.append(0.0,np.diff(x_ii)) # looking for outliers
    stdev_amt = 5.0 # standard deviation multiplier
    x_outliers = np.where(np.abs(x_diff)>np.abs(np.mean(x_diff))+\
                          (stdev_amt*np.std(x_diff)))
    x_inliers  = np.where(np.abs(x_diff)<np.abs(np.mean(x_diff))+\
                          (stdev_amt*np.std(x_diff)))
    y_diff     = np.append(0.0,np.diff(y_ii)) # looking for outliers
    y_outliers = np.where(np.abs(y_diff)>np.abs(np.mean(y_diff))+\
                          (stdev_amt*np.std(y_diff)))
    y_inliers  = np.abs(y_diff)<np.abs(np.mean(y_diff))+\
                 (stdev_amt*np.std(y_diff))
    if len(x_outliers)!=0:
        x_ii[x_outliers] = np.nan # null outlier
        y_ii[x_outliers] = np.nan # null outlier
    if len(y_outliers)!=0:
        y_ii[y_outliers] = np.nan # null outlier
        x_ii[y_outliers] = np.nan # null outlier
    return x_ii,y_ii

def mag_cal():
    print("-" * 50)
    print("Magnetometer Calibration")
    mag_cal_rotation_vec = []  # variable para cálculos de calibración
    min_length = None  # Longitud mínima para las muestras

    for qq, ax_qq in enumerate(mag_cal_axes):
        input("-" * 8 + " Press Enter and Start Rotating the IMU Around the " + ax_qq + "-axis")
        print("\t When Finished, Press CTRL+C")
        mag_array = []
        t0 = time.time()
        while True:
            try:
                mx, my, mz = AK8963_conv()  # leer y convertir datos del magnetómetro
                #print(mx," ---  " ,my," --- " ,mz)
            except KeyboardInterrupt:
                break
            except:
                continue
            mag_array.append([mx, my, mz])  # mag array

        mag_array = mag_array[20:]  # eliminar los primeros puntos (buffer clearing)
        if min_length is None or len(mag_array) < min_length:
            min_length = len(mag_array)  # actualizar longitud mínima
        mag_cal_rotation_vec.append(mag_array)  # agregar al vector de calibración
        print("Sample Rate: {0:2.0f} Hz".format(len(mag_array) / (time.time() - t0)))

    # Ajustar todas las listas a la longitud mínima
    for i in range(len(mag_cal_rotation_vec)):
        mag_cal_rotation_vec[i] = mag_cal_rotation_vec[i][:min_length]

    mag_cal_rotation_vec = np.array(mag_cal_rotation_vec)  # convertir a numpy array
    ak_fit_coeffs = []
    indices_to_save = [0, 0, 1]  # índices para guardar como offsets

    for mag_ii, mags in enumerate(mag_cal_rotation_vec):
        mags = np.array(mags)  # mag numpy array
        x, y = mags[:, cal_rot_indices[mag_ii][0]], \
               mags[:, cal_rot_indices[mag_ii][1]]  # sensores para analizar
        x, y = outlier_removal(x, y)  # eliminación de valores atípicos
        y_0 = (np.nanmax(y) + np.nanmin(y)) / 2.0  # offset en Y
        x_0 = (np.nanmax(x) + np.nanmin(x)) / 2.0  # offset en X
        ak_fit_coeffs.append([x_0, y_0][indices_to_save[mag_ii]])  # agregar al offset

    return ak_fit_coeffs, mag_cal_rotation_vec

#
#########################################
# Plot Values to See Calibration Impact
#########################################
#
def mag_cal_plot():
    plt.style.use('ggplot') # start figure
    fig,axs = plt.subplots(1,2,figsize=(12,7)) # start figure
    corrected_data = []  # Lista para almacenar los datos corregidos

    for mag_ii,mags in enumerate(mag_cal_rotation_vec):
        mags = np.array(mags) # magnetometer numpy array
        x,y = mags[:,cal_rot_indices[mag_ii][0]],\
                    mags[:,cal_rot_indices[mag_ii][1]]
        x,y = outlier_removal(x,y) # outlier removal 
        
        # Aplicar la corrección de hard iron
        x_corrected = x - mag_coeffs[cal_rot_indices[mag_ii][0]]
        y_corrected = y - mag_coeffs[cal_rot_indices[mag_ii][1]]

        # Guardar los datos corregidos para luego escribirlos en el CSV
        corrected_data.extend(zip(x_corrected, y_corrected))
        
        
        axs[0].scatter(x,y,
                       label='Rotation Around ${0}$-axis (${1},{2}$)'.\
                    format(mag_cal_axes[mag_ii],
                           mag_labels[cal_rot_indices[mag_ii][0]],
                           mag_labels[cal_rot_indices[mag_ii][1]]))
        axs[1].scatter(x-mag_coeffs[cal_rot_indices[mag_ii][0]],
                    y-mag_coeffs[cal_rot_indices[mag_ii][1]],
                       label='Rotation Around ${0}$-axis (${1},{2}$)'.\
                    format(mag_cal_axes[mag_ii],
                           mag_labels[cal_rot_indices[mag_ii][0]],
                           mag_labels[cal_rot_indices[mag_ii][1]]))
    axs[0].set_title('Before Hard Iron Offset') # plot title
    axs[1].set_title('After Hard Iron Offset') # plot title
    mag_lims = [np.nanmin(np.nanmin(mag_cal_rotation_vec)),
                np.nanmax(np.nanmax(mag_cal_rotation_vec))] # array limits
    mag_lims = [-1.1*np.max(mag_lims),1.1*np.max(mag_lims)] # axes limits
    for jj in range(0,2):
        axs[jj].set_ylim(mag_lims) # set limits
        axs[jj].set_xlim(mag_lims) # set limits
        axs[jj].legend() # legend
        axs[jj].set_aspect('equal',adjustable='box') # square axes
    fig.savefig('mag_cal_hard_offset_white.png',dpi=300,bbox_inches='tight',
                facecolor='#FFFFFF') # save figure
    plt.show() #show plot
    
    # Guardar los datos corregidos en un archivo CSV
    with open('corrected_mag_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(corrected_data)  # Escribir los datos corregidos

if __name__ == '__main__':
    '''
    while True:
        
        mx, my, mz = AK8963_conv()  # leer y convertir datos del magnetómetro
        #print("SIN CALIBRAR")
        #print(mx," - ",my, " - ", mz)
        magx_new = (mx - (-19.26)) * 1.035070140280561
        magy_new = (my - (73.095)) * 0.9672284644194756
        #magz_cal = mz - (5.3)1.03     0.96
       #[-19.8486328125, 73.828125, -45.7763671875
        
        
        
        
        #print("CALIBRADOOOOO")
        #print(magx_cal," - ",magy_cal, " - ", magz_cal)
        
        # Obtener los valores magnéticos
        #magx_new, magy_new, _ = sensor.readMagnetometerMaster()
        #print(magx_new," ---  " ,magy_new," --- " ,_)

        
        # Aplicar el filtro de paso bajo
        filtered_magx = low_pass_filter(filtered_magx, magx_new)
        filtered_magy = low_pass_filter(filtered_magy, magy_new)
        
        # Calcular el ángulo de dirección
        heading_angle_in_degrees = math.atan2(filtered_magx, filtered_magy) * (180 / math.pi)
        heading_angle_in_degrees_plus_declination = heading_angle_in_degrees + DECLINATION
        
        if heading_angle_in_degrees_plus_declination < 0:
            heading_angle_in_degrees += 360
            heading_angle_in_degrees_plus_declination += 360
        
        # Imprimir los resultados
        print('### Without Declination ###')
        print(heading_angle_in_degrees)
        print(compass(heading_angle_in_degrees))

        time.sleep(0.1)
    '''    
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        #
        ###################################
        # Magnetometer Calibration
        ###################################
        #
        mag_labels = ['m_x','m_y','m_z'] # mag labels for plots
        mag_cal_axes = ['z','y','x'] # axis order being rotated
        cal_rot_indices = [[0,1],[1,2],[0,2]] # indices of heading for each axis
        mag_coeffs,mag_cal_rotation_vec = mag_cal() # grab mag coefficients
        #
        ###################################
        # Plot with and without offsets
        ###################################
        #
        mag_cal_plot() # plot un-calibrated and calibrated results
        #
        print(mag_coeffs)
    
            
            
        
