#%%
from src.monopole import  monopoleFlowSyE, PATH_DATA

PATH_ANALYTICAL = PATH_DATA.joinpath('monopoleFlow', 'analytical')
#%%
timeSteps = [3, 4]

# Solução otimizada
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
# %%
