#%% code
from src.monopole import monopoleFlowSy, monopoleFlowSyE, PATH_DATA

PATH_ANALYTICAL = PATH_DATA.joinpath('monopoleFlow', 'analytical')
#Teste symengine
d = 3*42
monopoleFlowSyE(
    t           = [2],
    M           = 0.2,  
    xlim        = (-d, d),
    ylim        = (-d, d),
    nxy         = (2*d+1, 2*d+1),
    savePath    = PATH_ANALYTICAL,
    outName     = 'monopole_10Hz_M0.2_teste.json'
)
# %%
