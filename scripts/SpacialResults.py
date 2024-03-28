#%%
from src.utils import importData, plotSchemesGO
from src.path import PATH_DATA, PATH_IMAGES
from plotly.subplots import make_subplots

analitic_mach02 = PATH_DATA.joinpath('monopoleFlow', 'analytical', 'monopole_10Hz_M0.2_t0.2_4.0s.pkl')
time = 4
case = 'mach0.2_TCC_retol0'
# %% MALHA CIRCULAR X MALHA QUADRADA
psimS = importData(
    case = case, 
    test='circMesh_ZU', 
    subcase = 'standardSpacial',
    time = time, 
    keyword='8ppw',
    xsim_range=(-10*42, 10*42, -3*42, 3*42)
    )
psimS['Malha circular'] = psimS.pop('vanLeer 8ppw n4000')

psimS.update(
    importData(
        case = case, 
        test='quadMesh', 
        subcase = 'standardSpacial', 
        time = time,
        keyword='8ppw',
        xsim_range=(-10*42, 10*42, -3*42, 3*42),
        )
)

psimS['Malha Quadrada'] = psimS.pop('vanLeer 8ppw n4000')

plotSchemesGO(
    psimS, 
    xsim=(-3*42, 3*42), 
    analitc=analitic_mach02,
    time = time, 
    save=True, 
    save_name= 'Spacial_comp_malhas_8PPW',
    format='pdf',
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
    case = case, 
    test='circMesh_ZU',
    time = time, 
    subcase = 'standardSpacial', 
    xsim_range=(-10*42, 10*42, -3*42, 3*42)
)

for ppw in [8, 16, 32, 64]:
    psimS[f'{ppw} PPW'] = psimS.pop(f'vanLeer {ppw}ppw n4000')


fig = plotSchemesGO(
    psimS, 
    xsim=(-3*42, 3*42), 
    analitc=analitic_mach02, 
    time = time,
    save=True, 
    save_name= 'Spacial_comp_PPW',
    format='pdf',
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
fig2.write_html(
     PATH_IMAGES.joinpath('plotly-interactive', f'spacial-{float(time)}s' ,'Spacial_comp_PPW.html')
)
fig2.write_image(
    PATH_IMAGES.joinpath('results', f'spacial-{float(time)}s' ,'Spacial_comp_PPW.pdf'), 
    format = 'pdf', 
    scale = 8,
    width=1100,
    height=600)
# %% VARIAÇÃO DOS ESQUEMAS ESPACIAIS
for ppw in [16, 32]:
    psimS = importData(
        case = case, 
        test='circMesh_ZU',
        time = time, 
        subcase = 'standardSpacial',
        keyword= f'{ppw}ppw',
        # xsim_range=(-10*42, 10*42, -10*42, 10*42)
        xsim_range=(-10*42, 10*42, -3*42, 3*42)
    )
    psimS2 = importData(
        case = case,
        test='circMesh_ZU',
        time = time,
        subcase = 'spacialSchemesTest',
        keyword= f'{ppw}ppw',
        # xsim_range=(-10*42, 10*42, -10*42, 10*42)
        xsim_range=(-10*42, 10*42, -3*42, 3*42)
    )

    plotSchemesGO(
        psim = {**psimS, **psimS2}, 
        # xsim=(-10*42, 10*42), 
        xsim=(-3*42, 3*42), 
        analitc=analitic_mach02,
        time = time, 
        save=True, 
        save_name= f'Spacial_comp_schemes_{ppw}PPW',
        format='pdf',
        windows =True,
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
# n = [400, 600, 800, 1000]
ntime = [400, 800, 1000]
for n in ntime:
    psimS2 = importData(
        case = case,
        test='circMesh_ZU',
        time = time,
        subcase = 'timeSchemesTest',
        keyword= f'n{n}',
        xsim_range=(-10*42, 10*42, -3*42, 3*42)
    )

    plotSchemesGO(
        psim = psimS2, 
        xsim=(-3*42, 3*42), 
        analitc=analitic_mach02,
        time = time, 
        save=True, 
        save_name= f'Time_comp_schemes_n{n}',
        format='pdf',
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


# %%

