import numpy as np
import matplotlib.pyplot as plt

# Función para generar un tren de deltas separado por N


def tren_de_deltas(N, length):
    """
    Genera un tren de deltas separado por N.

    Args:
    N (int): Separación entre deltas.
    length (int): Longitud total del array.

    Returns:
    np.array: Array con el tren de deltas.
    """
    tren = np.zeros(length)
    tren[::N] = 1
    return tren


# Definir las funciones discretas con deltas centradas en el eje y
f1 = np.array([0, 1, 2, 3, 2, 1, 0])  # Delta en el segundo punto
f1_centrada = np.concatenate(
    (np.zeros(len(f1) - 1), f1, np.zeros(len(f1) - 1)))

# Crear f2 como un tren de deltas separado por N=6
N = 6
length = 1000  # Longitud total del array, suficientemente grande para simular infinito
f2 = tren_de_deltas(N, length)

# Reflejar f1_centrada para obtener los valores negativos del eje x
f1_reflejada = f1_centrada[::-1]

# Concatenar f1_reflejada con f1_centrada para obtener una función simétrica
f1_simetrica = np.concatenate((f1_reflejada[:-1], f1_centrada))

# Realizar la convolución
convolucion = np.convolve(f1_simetrica, f2)

# Imprimir el resultado
print("f1:", f1)
print("f2:", f2)
print("f1_centrada:", f1_centrada)
print("f1_simetrica:", f1_simetrica)
print("Convolución:", convolucion)

# Graficar las funciones y su convolución
plt.figure(figsize=(10, 8))

plt.subplot(5, 1, 1)
plt.stem(f1, use_line_collection=True)
plt.title('Función f1 Original')

plt.subplot(5, 1, 2)
plt.stem(f1_centrada, use_line_collection=True)
plt.title('Función f1 Centrada')

plt.subplot(5, 1, 3)
plt.stem(f2, use_line_collection=True)
plt.title('Función f2 (Tren de Deltas)')

plt.subplot(5, 1, 4)
plt.stem(f1_simetrica, use_line_collection=True)
plt.title('Función f1 Simétrica')

plt.subplot(5, 1, 5)
plt.stem(convolucion, use_line_collection=True)
plt.title('Convolución de f1 Simétrica y f2')

plt.tight_layout()
plt.show()
