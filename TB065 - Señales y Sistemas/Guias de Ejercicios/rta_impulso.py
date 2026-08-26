"""
-----------------------------------------------------------
Graficador de rta al impulso
-----------------------------------------------------------
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import impulse, TransferFunction

# Definir la función de transferencia H(s)
# Coeficientes del numerador y denominador
numerador = [1, -1]  # Ejemplo: H(s) = 1 / (s^2 + 3s + 2)
denominador = [1, -1/2]

# Crear la función de transferencia
H = TransferFunction(numerador, denominador)

# Calcular la respuesta al impulso
t, y = impulse(H)

# Graficar la respuesta al impulso
plt.figure(figsize=(8, 5))
plt.plot(t, y, label='Respuesta al impulso')
plt.title('Respuesta al Impulso de H(s)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()
