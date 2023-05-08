#%% test import time data
from src.utils import importData

pressure = importData(case='newMesh0', test='spacialTest', time = None)
# %% test import spacial data
from src.utils import importData, plotSchemes

psimT = importData(case='circMesh', test='timeTest')
psimS = importData(case = 'circMesh', test='spacialTest')


plotSchemes(psimT, title='CircMesh - Time Schemes')
plotSchemes(psimS, title='CircMesh - Spacial Schemes')

# %% test import specify spacial data
from src.utils import importData, plotSchemes
psimS = importData(case = 'newMesh0', test='spacialTest', keyword='vanLeer')


plotSchemes(psimS, title='NewMesh 0 - Spacial Schemes')


# %%
