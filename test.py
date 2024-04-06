import numpy as np
from cal import sigmoid

x = np.linspace(-20, 20, 100)  # Generate 100 values between -10 and 10
y = sigmoid(x)

# Plotting the sigmoid function
import matplotlib.pyplot as plt

plt.plot(x, y)
plt.title("Sigmoid Function")
plt.xlabel("Input")
plt.ylabel("Output")
plt.grid(True)
plt.show()
