#%% solução analítica para 9 e 9.2 s
# from src.monopole import monopoleFlowSy, PATH_DATA
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
# monopoleFlowSy(
#     t           = [9, 9.2],
#     xlim        = (-1560, 1560),
#     ylim        = (-1560, 1560),
#     nxy         = (2*1560+1, 2*1560+1),
#     save_path   = PATH_DATA.joinpath('monopoleFlow', 'analytical'))

#%% exponencial
x = [ -93.96,-76.05, -58.43, -41.12, -23.82, -6.29]
y = [ 185.26, 205.8, 238, 282.90, 374.49, 737.93]

f = interp1d(x,y, kind = 'cubic')

x2 = np.linspace(x[0], x[-1])
plt.plot(x2, f(x2))
plt.show()
