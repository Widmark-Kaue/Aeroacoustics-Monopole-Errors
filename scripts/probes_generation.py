#%% Libs
from src.utils import probes

#%% Spacial probes
c0 = 349.5369
f = 10
lamb = c0/f
ppw = lamb/200

probes(number_of_probes=int(200/ppw), lim = (-100,100), name_of_archive='probesSpacial')
print(f'lambda = {lamb} [m]')
print(f'ppw = {200/ppw}')

#%% Time probes
probes(number_of_probes = 22, lim = (-99, 99), name_of_archive = 'probesTime')