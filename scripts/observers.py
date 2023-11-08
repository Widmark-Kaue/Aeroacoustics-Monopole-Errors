#%% Libs
from src.utils import probes, Path
import numpy as np

#%% Global params
gamma = 1.4
T0    = 298.15
p0    = 101325
R     = 8314.46261815324 / 28.9   # Air
c0    = np.sqrt(gamma * R * T0)
M     = 0.2

#%% Monopole f = 10 Hz
freq      = 10
omega_num = freq * 2 * np.pi
lamb0     = c0 / freq
lambd     = round(lamb0 * (1 + M))
lambu     = round(lamb0 * (1 - M))

nPoints_ZU= round(20*lambd/lambu)   

#%% Spacial probes
for ppw in [8, 16, 32, 64]:
    probes(
        name_of_archive= f'probesSpacial_{ppw}PPW',
        number_of_probes = nPoints_ZU*ppw, 
        lim = (-10*lambd,10*lambd), 
        subpath=Path('mach0.2')
        )

# %%
