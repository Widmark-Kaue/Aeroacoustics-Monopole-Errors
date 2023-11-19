#%%
import numpy as np 
from src.utils import importData, plotSchemesGO
from src.path import PATH_DATA, PATH_IMAGES, Path

analitic_mach02 = PATH_DATA.joinpath('monopoleFlow', 'analytical', 'monopole_10Hz_M0.2.json')
#%% Malha Circular x Malha quadrada

psimS = importData(
    case = 'mach0.2_TCC', 
    test='circMesh_ZU', 
    subcase = 'standardSpacial', 
    keyword='8ppw',
    xsim_range=(-10*42, 10*42, -3*42, 3*42)
    )
psimS['Malha circular'] = psimS.pop('vanLeer 8ppw n4000')

psimS.update(
    importData(
        case = 'mach0.2_TCC', 
        test='quadMesh', 
        subcase = 'standardSpacial', 
        keyword='8ppw',
        xsim_range=(-10*42, 10*42, -3*42, 3*42),
        )
)

psimS['Malha Quadrada'] = psimS.pop('vanLeer 8ppw n4000')

plotSchemesGO(
    psimS, 
    xsim=(-3*42, 3*42), 
    analitc=analitic_mach02, 
    save=True, 
    save_name= 'Spacial_comp_malhas_8PPW',
    format='png',
    windows =True, 
    numlegend=2,
    plotconfig = dict(
        xaxis = dict(
            ticks ='outside',
            linecolor = 'black',
            mirror =True
        ),
        yaxis = dict(
            ticks ='outside',
            linecolor = 'black',
            mirror =True
        )
    )
)
# %%
