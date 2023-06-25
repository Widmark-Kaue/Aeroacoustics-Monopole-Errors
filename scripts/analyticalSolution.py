#%% solução analítica para 9 e 9.2 s
from src.monopole import monopoleFlowSy, PATH_DATA

monopoleFlowSy(
    t           = [9, 9.2],
    xlim        = (-1560, 1560),
    ylim        = (-1560, 1560),
    nxy         = (2*1560+1, 2*1560+1),
    save_path   = PATH_DATA.joinpath('monopoleFlow', 'analytical'))



# %%
