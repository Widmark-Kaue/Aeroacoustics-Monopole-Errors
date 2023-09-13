#%% solução analítica para 2
from src.monopole import monopoleFlowSy, PATH_DATA

#%%
monopoleFlowSy(
    t           = [2],
    xlim        = (-260, 260),
    ylim        = (-260, 260),
    nxy         = (2*260+1, 2*260+1),
    save_path   = PATH_DATA.joinpath('monopoleFlow', 'analytical'))

