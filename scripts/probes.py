
from src.utils import probes

c0 = 349.5369
f = 10
lamb = c0/f
ppw = lamb/200

probes(number_of_probes=int(200/ppw), lim = (-100,100), name_of_archive='probes_200ppw')
print(f'lambda = {lamb} [m]')
print(f'ppw = {200/ppw}')