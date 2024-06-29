from PIL import Image

def image_to_binary_text(image_path, output_file):
    # Abrir la imagen en blanco y negro
    img = Image.open(image_path).convert('1')  # '1' convierte la imagen a blanco y negro

    # Obtener tamaño de la imagen
    width, height = img.size

    # Crear un archivo de texto para escribir la representación binaria
    with open(output_file, 'w') as f:
        # Iterar sobre cada pixel de la imagen
        for y in range(height):
            for x in range(width):
                # Obtener el valor del pixel (0 o 255)
                pixel = img.getpixel((x, y))

                # Convertir el valor a binario (0 o 1)
                bit_value = '0' if pixel == 0 else '1'

                # Escribir el valor binario en el archivo de texto
                f.write(bit_value)

            f.write('\n')  # Nueva línea al final de cada fila

# Ejemplo de uso
if __name__ == "__main__":
    image_path = 'colors.png'  # Cambia esto a la ruta de tu imagen XCF
    output_file = 'imagen_binaria.txt'  # Nombre del archivo de salida

    image_to_binary_text(image_path, output_file)
    print(f"Imagen convertida a binario y guardada en '{output_file}'.")
