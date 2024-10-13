from picamzero import Camera
from time import sleep
import cv2
import numpy as np
from PIL import Image
import piexif
import math

def rotate(filePath,angle):
		try:
			image = Image.open(filePath)
			EXIFData = piexif.load(filePath)

			newOrientation = 1
			if angle == 180:
				newOrientation = 3
				image = image.rotate(180, expand=True)
				
			EXIFData['Orientation'] = newOrientation
			EXIFBytes = piexif.dump(EXIFData)

			image.save(filePath, exif=EXIFBytes)
		except Exception as ex:
			print('Could not rotate ' + filePath + ' ' + str(angle) + ' degrees. ' + str(ex))
			pass
			
def calcular_distancia(f, h_real, h_imagen):
    # f = distancia focal (en píxeles)
    # h_real = altura real de la baliza (en metros)
    # h_imagen = altura de la baliza en la imagen (en píxeles)
    return (f * h_real) / h_imagen
	
	
cam = Camera()


cam.start_preview()
cam.take_photo("new_image.jpg")
cam.stop_preview()

rotate("new_image.jpg",180)

imagen = cv2.imread("new_image.jpg")
imagen = cv2.resize(imagen, (500, 500))

imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Definir el rango de color rojo en HSV (hay dos rangos para rojo)
lower_red1 = np.array([0, 120, 70])   # Primer rango (hacia los tonos más bajos)
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 120, 70])  # Segundo rango (hacia los tonos más altos)
upper_red2 = np.array([180, 255, 255])

# Crear dos máscaras para cubrir ambos rangos de rojo
mask1 = cv2.inRange(imagen_hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(imagen_hsv, lower_red2, upper_red2)
red_mask = mask1 | mask2

#mascara = cv2.inRange(imagen_hsv, rango_bajo_verde, rango_alto_verde)

resultado = cv2.bitwise_and(imagen, imagen, mask=red_mask)

contornos, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print(len(contornos))
        
cv2.drawContours(imagen, contornos, -1, (0, 255, 0), 2)

# Si se detecta al menos un contorno
if len(contornos) > 0:
    # Tomar el contorno más grande (asumiendo que es la baliza)
    contorno_max = max(contornos, key=cv2.contourArea)

    # Obtener el rectángulo delimitador de la baliza
    x, y, w, h = cv2.boundingRect(contorno_max)
    baliza_apparent_size = max(w, h)  # Diámetro aproximado en píxeles
    print(f"Tamaño de la baliza en píxeles: Ancho={w}, Alto={h}")
    
    #for contour in contornos:
    M = cv2.moments(contorno_max)
    if M["m00"] != 0:
	    cX = int(M["m10"] / M["m00"])
	    cY = int(M["m01"] / M["m00"])
	    # Dibujar el centroide
	    cv2.circle(imagen, (cX, cY), 5, (255, 0, 0), -1)
    
    
# # Distancia focal en píxeles (CAMERA V1)
focal_length = 3.6 #mm

#pasar a pixeles

mm2pixels = (focal_length * 500) / 3.76

f = mm2pixels



###########################
h_real = 0.3  # Tamaño real de la baliza (en metros)

# Tamaño de la baliza en píxeles
h_imagen = h  # Altura de la baliza detectada en píxeles (del paso anterior)

# Calcular la distancia
distancia = calcular_distancia(f, h_real, h_imagen)
print(f"Distancia estimada a la baliza: {distancia:.2f} metros")
############################


real_size = 30.0  # Tamaño real de la baliza en centímetros
FOV = 53.37  # Campo de visión horizontal en grados para la Pi Camera
image_width = 500  # Ancho de la imagen en píxeles

# Calcular la distancia focal
focal_length = (image_width / 2) / np.tan(np.radians(FOV / 2))

# Calcular la distancia a la baliza
distance = (real_size * focal_length) / baliza_apparent_size
distance /= 100 #metros 
print(f'Distancia a la balizaaaa: {distance} cm')



width = imagen.shape[1]
height = imagen.shape[0]

#######################################
# Campo de visión de la cámara
horizontal_fov = 53.37  # Grados
vertical_fov = 41.41    # Grados

# Centro de la imagen
cx_img = width / 2
cy_img = height / 2

# Calcular el ángulo horizontal y vertical
theta_h = (cX - cx_img) / width * horizontal_fov
theta_v = (cY - cy_img) / height * vertical_fov

print(f"Ángulo horizontal: {theta_h:.2f}°")
print(f"Ángulo vertical: {theta_v:.2f}°")

# 0    *0.5,      2    *0.5
xb, yb = 0 * 0.5 , 3 * 0.5

# Distancia de la cámara a la baliza (d)
d = distance+0.15


# Ángulo en grados
theta_deg = theta_h

#if(theta_h > 0):
theta_h = -theta_h

print(f"Ángulo nuevo horizontaaaal: {theta_h:.2f}°")

# Convertir ángulo a radianes
theta_rad = math.radians(90+theta_h)

# Calcular la posición de la cámara (xc, yc)
xc = xb - d * math.cos(theta_rad)
yc = yb - d * math.sin(theta_rad)

print(f"Posición de la cámara: ({xc/0.5 :.3f}, {yc/0.5 :.3f})")



# Mostrar los resultados
cv2.imshow('Imagen original',imagen)
#cv2.imshow('Mascara Verde',mascara)
cv2.imshow('Resultado',resultado)

cv2.waitKey(0)
cv2.destroyAllWindows()



