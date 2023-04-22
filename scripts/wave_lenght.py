#%% Libs
import numpy as np
import matplotlib.pyplot as plt

from src.path import *
from scipy.optimize import bisect
from scipy.interpolate import interp1d

#%% Parâmetros
gamma = 1.4
T0    = 298.15
p0    = 101325
R     = 8314.46261815324 / 28.9   # Air
c0    = np.sqrt(gamma * R * T0)
M     = 0.5

theta     = 0
omega_num = 20 * np.pi
f         = omega_num / (2 * np.pi)
lamb0     = c0 / f
lamb1     = lamb0 * (1 + M * np.cos(theta))
lamb2     = lamb0 * (1 - M * np.cos(theta))
print(f'lambda0 = {lamb0} m')
print(f'lambda montante = {lamb1} m')
print(f'lambda jusante  = {lamb2} m')
#%% import solução analítica
x, p = np.loadtxt(
    PATH_DATA.joinpath('monopoleFlow', 'analiticSolution2s.dat'), unpack=True
)
pf = interp1d(x, p, kind='cubic')

plt.plot(x, pf(x))
plt.grid()
plt.show()

#%% raizes
sign = np.sign(p)
roots = []
tol = 1e-5
for i in range(len(sign) - 1):
    if sign[i] * sign[i + 1] < 0:
        root = bisect(pf, x[i], x[i + 1])
        roots.append(root)
        if len(roots) > 1 and abs(roots[-2] - roots[-1]) < tol:
            roots.pop()
roots = np.array(roots)
#%% plot com as raizes e comprimentos de onda
lamb = np.diff(roots)

ticks = (roots[:-1] + roots[1:]) / 2

plt.plot(x, pf(x), 'k')
plt.plot(roots, pf(roots),
    'm^',
    markersize=5,
    label=r'$\lambda_{min}=$' + f'{round(min(lamb),3)} m',
)
plt.xticks(np.round(ticks, 2), [f'{round(i,2)}' for i in lamb], rotation=45)

plt.xlabel(r'$\lambda \ [m]$')
plt.ylabel(r'$P \ [Pa]$')
plt.legend()
plt.grid(axis='y')
plt.show()


# %%
