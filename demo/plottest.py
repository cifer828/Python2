import matplotlib.pyplot as plt
import numpy as np
x = np.arange(1,1000,1)
r = -2
c = 5
y = [5*(a**r) for a in x]



fig = plt.figure()

ax = fig.add_subplot(111)
ax.loglog(x,y,label = r"$y = \frac{1}{2\sigma_1^2}, c=5,\sigma_1=-2$")
ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
plt.show()