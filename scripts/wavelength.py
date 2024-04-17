#%% Libs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.path import *
from src.monopole import pSpacial

from scipy.signal import argrelmax

analitic_mach02 = PATH_DATA.joinpath('monopoleFlow', 'analytical', 'monopole_10Hz_M0.2_t0.2_4.0s.pkl')
#%% Parâmetros
gamma = 1.4
T0    = 298.15
p0    = 101325
R     = 8314.46261815324 / 28.9   # Air
c0    = np.sqrt(gamma * R * T0)
M     = 0.2

omega_num = 20 * np.pi
f         = omega_num / (2 * np.pi)
lamb0     = c0 / f
lambd     = lamb0 * (1 + M)
lambu     = lamb0 * (1 - M)

cd     = c0 * (1 + M)
cu     = c0 * (1 - M)

  
print(f'lambda0 = {lamb0} m')
print(f'lambda montante = {round(lambu,3)} m')
print(f'lambda jusante  = {round(lambd,3)} m')

print(f'Sound speed0 = {c0:.3f} m')
print(f'Sound speed montante = {cu:.3f} m')
print(f'Sound speed jusante  = {cd:.3f} m')

print(f'Raio zona útil = {round(3*lambd)} m')
print(f'Raio zona de saída = {round(15*lambd)} m')

print(f't1 obs = {15*lambd/cu + 15*lambd/cd:.1f} s')
print(f't2 obs = {15*lambd/cd + 15*lambd/cu:.1f} s')
#%% import solução analítica
x, p = pSpacial(analitic=analitic_mach02, time = 4)
id_peak = argrelmax(p)[0]

lambs = np.diff(x[id_peak])
pos   = pd.Series(x[id_peak]).rolling(2).mean().to_numpy()[1:] 
print(f'{lambs=}')
print(f'{pos=}')

plt.plot(x, p, x[id_peak], p[id_peak], 'ko')
plt.grid()
plt.show()

#%% import solução analítica
ypos = [0, 10, 50, -10, -50]

for y in ypos:
    x, p = pSpacial(analitic_mach02, time=4, ypos=y)
    plt.plot(x, p, label = f'{y=}', linestyle = '--' if y < 0 else '-')

plt.grid()
plt.legend()
plt.show()

# %%
