#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.monopole import  monopoleFlowSyE, PATH_DATA
from time import time

PATH_ANALYTICAL = PATH_DATA.joinpath('monopoleFlow', 'analytical')
#%% Solução para análise radial
timeSteps = [3, 4]

d = 3*42
d = int(d)
monopoleFlowSyE(
    t               = timeSteps,
    M               = 0.2,  
    xlim            = (-d, d),
    ylim            = (-d, d),
    nxy             = (40*d+1, 40*d+1),
    savePath        = PATH_ANALYTICAL,
    printInterval   = 100,
    writeInterval   = 100,
    outName         = 'monopole_10Hz_M02_radial'
)
#%% Solução para domínio extendido
timeSteps = np.round(np.arange(0.2, 4.001, 0.001), 3)
print(len(timeSteps))

t0 = time()
d = 6*42
d = int(d)
monopoleFlowSyE(
    t               = timeSteps,
    M               = 0.2,  
    xlim            = (-d, d),
    ylim            = (-d, d),
    nxy             = (2*d+1, 2*d+1),
    savePath        = PATH_ANALYTICAL,
    printInterval   = 100,
    writeInterval   = 100,
    outName         = 'monopole_10Hz_M02_t02_4s_ZU6.pkl'
)
tf = time()
print(f'Tempo = {tf - t0} s')
#%%
file_path  = PATH_ANALYTICAL.joinpath('monopole_10Hz_M02_t02_4s_ZU6.pkl')
mono = pd.read_pickle(file_path)


nx = mono['nx']
ny = mono['ny']
ypos  = np.linspace(mono['ylim'][0], mono['ylim'][1], ny).searchsorted(0) 
x2  = np.linspace(mono['xlim'][0], mono['xlim'][1], nx)
X = np.array(mono['X'])
Y = np.array(mono['Y'])
pressure  = mono['time']

plt.contourf(X, Y, pressure['4.0'].T)
plt.xlabel('x')
plt.ylabel('y')

plt.title('Countour Plot - time: 4 s')
plt.show()

p2 = np.array(pressure['4.0']).T[ypos]
plt.plot(x2, p2, 'm', label = 'Otimized solution')
plt.legend()
plt.show()
#%% 