from PIL import Image

def image_to_binary_text(image_path, output_file):
    # Abrir la imagen en blanco y negro
    img = Image.open(image_path).convert('1')  # '1' convierte la imagen a blanco y negro

    width, height = img.size

    # Crear un archivo de texto para escribir la representación binaria
    with open(output_file, 'w') as f:
        # Iterar sobre cada pixel de la imagen
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))

                bit_value = '0' if pixel == 0 else '1'

                f.write(bit_value)

            f.write('\n') 

# Ejemplo de uso
if __name__ == "__main__":
    image_path = 'colors.png'
    output_file = 'imagen_binaria.txt'

    image_to_binary_text(image_path, output_file)
    print(f"Imagen convertida a binario y guardada en '{output_file}'.")
