import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 32)
y = np.sin(x)
plt.plot(x, y)
plt.show()