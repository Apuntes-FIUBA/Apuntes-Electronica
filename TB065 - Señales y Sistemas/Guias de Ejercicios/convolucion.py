import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Definir la función de la señal u(t)
def u(t):
    return np.where(t >= 0, 1, 0)

# Definir las funciones h(t) y x(t)
def h(t):
    return u(t)

def x(t):
    return np.exp(t) * u(-t)

# Definir el rango de tiempo
t = np.linspace(-30, 30, 500)

# Calcular las señales h(t) y x(t)
h_t = h(t)
x_t = x(t)

# Realizar la convolución
conv_t = np.convolve(h_t, x_t, mode='full') * (t[1] - t[0])
t_conv = np.linspace(2 * t[0], 2 * t[-1], len(conv_t))

# Graficar las señales h(t), x(t) y su convolución
plt.figure(figsize=(12, 8))

# Graficar h(t)
plt.subplot(3, 1, 1)
plt.plot(t, h_t, label='h(t) = e^(-t)u(t)')
plt.title('Señal h(t)')
plt.xlabel('Tiempo t')
plt.ylabel('h(t)')
plt.grid(True)
plt.legend()

# Graficar x(t)
plt.subplot(3, 1, 2)
plt.plot(t, x_t, label='x(t) = e^(-3t)u(t)')
plt.title('Señal x(t)')
plt.xlabel('Tiempo t')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()

# Graficar la convolución
plt.subplot(3, 1, 3)
plt.plot(t_conv, conv_t, label='y(t) = h(t) * x(t)')
plt.title('Convolución de h(t) y x(t)')
plt.xlabel('Tiempo t')
plt.ylabel('y(t)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()