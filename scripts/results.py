#%%
import numpy as np 
import matplotlib.pyplot as plt

from src.utils import importData, plotSchemesGO
from src.path import PATH_DATA, PATH_IMAGES, Path

from plotly.subplots import make_subplots

analitic_mach02 = PATH_DATA.joinpath('monopoleFlow', 'analytical', 'monopole_10Hz_M0.2_3s.json')
# %% MALHA CIRCULAR X MALHA QUADRADA
psimS = importData(
    case = 'mach0.2_TCC', 
    test='circMesh_ZU', 
    subcase = 'standardSpacial',
    time = 3, 
    keyword='8ppw',
    xsim_range=(-10*42, 10*42, -3*42, 3*42)
    )
psimS['Malha circular'] = psimS.pop('vanLeer 8ppw n4000')

psimS.update(
    importData(
        case = 'mach0.2_TCC', 
        test='quadMesh', 
        subcase = 'standardSpacial', 
        time    = 3,
        keyword='8ppw',
        xsim_range=(-10*42, 10*42, -3*42, 3*42),
        )
)

psimS['Malha Quadrada'] = psimS.pop('vanLeer 8ppw n4000')

plotSchemesGO(
    psimS, 
    xsim=(-3*42, 3*42), 
    analitc=analitic_mach02,
    time = 3, 
    save=True, 
    save_name= 'Spacial_comp_malhas_8PPW',
    # format='png',
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
# %% VARIAÇÃO DA DISCRETIZAÇÃO DO DOMÍNIO

psimS = importData(
    case = 'mach0.2_TCC', 
    test='circMesh_ZU',
    time = 3, 
    subcase = 'standardSpacial', 
    xsim_range=(-10*42, 10*42, -3*42, 3*42)
)

for ppw in [8, 16, 32, 64]:
    psimS[f'{ppw} PPW'] = psimS.pop(f'vanLeer {ppw}ppw n4000')


fig = plotSchemesGO(
    psimS, 
    xsim=(-3*42, 3*42), 
    analitc=analitic_mach02, 
    time = 3,
    save=True, 
    save_name= 'Spacial_comp_PPW',
    # format='png',
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

fig2 = make_subplots(2,2)
count = 1
for i in range(2):
    for j in range(2):
        if count>1:
            fig['data'][0]['showlegend'] = False
        else:
            fig['data'][0]['showlegend'] = True
        fig2.add_trace(
            fig['data'][0],
            row=i+1,col=j+1,
            
        )
        fig2.add_trace(
            fig['data'][count],
            row=i+1,col=j+1
        )
        
        fig2.update_xaxes(fig.layout['xaxis'], row=i+1, col = j+1)
        fig2.update_yaxes(fig.layout['yaxis'], row=i+1, col = j+1)
        
        count+=1

fig2.update_layout(template = 'plotly_white')
fig2.show()
fig2.write_image(
    PATH_IMAGES.joinpath('results', 'Spacial_comp_PPW.png'), 
    format = 'png', 
    scale = 8,
    width=1100,
    height=600)
# %% VARIAÇÃO DOS ESQUEMAS ESPACIAIS
for ppw in [16, 32]:
    psimS = importData(
        case = 'mach0.2_TCC', 
        test='circMesh_ZU',
        time = 3, 
        subcase = 'standardSpacial',
        keyword= f'{ppw}ppw',
        xsim_range=(-10*42, 10*42, -10*42, 10*42)
    )
    psimS2 = importData(
        case = 'mach0.2_TCC',
        test='circMesh_ZU',
        time = 3,
        subcase = 'spacialSchemesTest',
        keyword= f'{ppw}ppw',
        xsim_range=(-10*42, 10*42, -10*42, 10*42)
    )

    plotSchemesGO(
        psim = {**psimS, **psimS2}, 
        xsim=(-10*42, 10*42), 
        # analitc=analitic_mach02,
        time = 3, 
        save=False, 
        save_name= f'Spacial_comp_schemes_{ppw}PPW',
        # format='png',
        windows =False,
        rms_acur= 5, 
        numlegend=1,
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
#%% VARIAÇÃO DOS ESQUEMAS TEMPORAIS
for n in [400, 600, 800, 1000]:
    psimS2 = importData(
        case = 'mach0.2_TCC',
        test='circMesh_ZU',
        time = 3,
        subcase = 'timeSchemesTest',
        keyword= f'n{n}',
        xsim_range=(-10*42, 10*42, -3*42, 3*42)
    )

    plotSchemesGO(
        psim = psimS2, 
        xsim=(3*42, 10*42), 
        analitc=analitic_mach02,
        time = 3, 
        save=True, 
        save_name= f'Time_comp_schemes_n{n}',
        # format='png',
        windows =True, 
        numlegend=1,
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
#%% PROBES TEMPORAIS
psim = importData(
    case = 'mach0.2_TCC',
    test='circMesh_ZU', 
    subcase='standardTime',
    keyword='32ppw',
    typeFile='time'
)

t, p = psim['vanLeer 32ppw n4000']
T = 0.1/2

probes = [4,5,6,7,8,9]


for pos in probes:
    lastPos = 0
    pico = []
    for i in range(len(t)):
        if (t[i] - t[lastPos]) >= T:
            pico.append(
                list(np.abs(p[:, pos])).index(
                np.max(np.abs(p[lastPos:i+1, pos]))
                )
            )
            lastPos = i

    plt.plot(t, p[:, pos], 'b')
    plt.plot(t[pico[:]], p[pico[:], pos], 'ko', alpha = 0.5)
    plt.show()

# %%
