"""
--------------------------------
Graficador de diagramas de Bode
--------------------------------
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import bode, TransferFunction

# Definir la función de transferencia H(s)
# Coeficientes del numerador y denominador

numerador = [1/20, 2]
denominador = [1/(300e6), 1/375000, 23/6000, 1]

# Crear la función de transferencia
H = TransferFunction(numerador, denominador)

# Calcular el diagrama de Bode
frequencies, magnitude, phase = bode(H)

# Graficar la magnitud
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.semilogx(frequencies, magnitude)  # Gráfica en escala logarítmica
plt.title('Diagrama de Bode de H(s)')
plt.ylabel('Magnitud (dB)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Graficar la fase
plt.subplot(2, 1, 2)
plt.semilogx(frequencies, phase)  # Gráfica en escala logarítmica
plt.xlabel('Frecuencia (rad/s)')
plt.ylabel('Fase (grados)')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.show()
