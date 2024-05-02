#%%
from src.monopole import pRadial
from src.path import PATH_DATA

#%%
analitic_mach02 = PATH_DATA.joinpath('monopoleFlow', 'analytical', 'monopole_10Hz_M02_radial.pkl')
time = 4


test = pRadial(analitic=analitic_mach02, time=time, radius=1)