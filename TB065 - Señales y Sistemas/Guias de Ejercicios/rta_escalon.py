"""
-----------------------------------------------------------
Graficador de rta al escalón
-----------------------------------------------------------
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import step, TransferFunction

# Definir la función de transferencia H(s)
# Coeficientes,  del numerador y denominador
numerador = [1, 0]  # Ejemplo: H(s) = 1 / (s^2 + 3s + 2)
denominador = [1, -3/2]

# Crear la función de transferencia
H = TransferFunction(numerador, denominador)

# Calcular la respuesta al escalón
t, y = step(H)

# Graficar la respuesta al escalón
plt.figure(figsize=(8, 5))
plt.plot(t, y, label='Respuesta al escalón', color='blue')
plt.title('Respuesta al Escalón de H(s)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()
plt.show()
