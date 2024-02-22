import numpy as np 
import matplotlib.pyplot as plt
from src.utils import probes

lambdaD = 42
theta = np.linspace(0,np.pi, 15)
r = np.array([1,  3])*lambdaD

x = lambda r: r*np.cos(theta)
y = lambda r: r*np.sin(theta)
for ri in r:
    p = np.zeros((len(x(ri)), 2))
    p[:,0] = x(ri)
    p[:,1] = y(ri)

    probes(
        name_of_archive=f'probesRadial_R{1 if ri == r[0] else 3}',
        subpath='mach0.2',
        p = p
        )

    plt.plot(p[:,0], p[:,1], 'o', label =  f'r = {ri}')

plt.legend()
plt.show()