#%% libs
import numpy as np 
import matplotlib.pyplot as plt

from re import findall
from scipy.signal import argrelmax
from reloading import reloading

from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import DEFAULT_PLOTLY_COLORS as COLORS

from src.monopole import pTime
from src.postprocess import phaseAmplitude
from src.path import PATH_DATA, PATH_IMAGES
from src.utils import importData, plotTempGO


#%%  parameters
probes = [0, 1, 3, 9, 11, 12]
probesPos = [-126, -105, -63, 63, 105, 126]
coord = [-3, -2.5, -1.5, 1.5, 2.5, 3]

# probes = [ 1, 3, 9, 11]
# probesPos = [-105, -63, 63, 105]
# coord = [-2.5, -1.5, 1.5, 2.5]
transientTime = 2
finalTime     = 4

analitic_mach02 = PATH_DATA.joinpath('monopoleFlow', 'analytical', 'monopole_10Hz_M0.2_t0.2_4.0s.pkl')
plotconfig = dict(
        xaxis = dict(
            ticks ='outside',
            linecolor = 'black',
            mirror =True,
            range = (3.4, 4)
        ),
        yaxis = dict(
            ticks ='outside',
            linecolor = 'black',
            mirror =True
        ),
        )

plotconfig2 = dict(
            ticks ='outside',
            linecolor = 'black',
            mirror =True,
        )
       
#%% TransientTime
psim = importData(
    case = 'mach0.2_TCC_retol0',
    test='circMesh_ZU', 
    subcase='standard-TimeData',
    typeFile='time'
)
tsim, psimTest = psim['vanLeer 32ppw n4000']
for i, pos in enumerate(probes):
    lb = fr'Probes nº {coord[i]}$\lambda_d$ - x = {probesPos[i]}'
    idx_peak_sim = argrelmax(psimTest[:, pos])[0]
    tsim_peak = tsim[idx_peak_sim]
    psim_peak = psimTest[idx_peak_sim, pos]
    
    psim_peak_rel = np.abs(psim_peak - psim_peak[-1])/psim_peak[-1] * 100
    
    # plt.plot(tsim, np.abs(psimTest[:, pos]), 'r',label = fr'Probes nº {coord[i]}$\lambda_d$ - x = {probesPos[i]}')
    # plt.plot(tsim_peak, psim_peak, 'ko')
    
    plt.plot(tsim_peak, psim_peak_rel, 'ko', alpha = 0.8, label = 'Relative Peak')
    plt.axhline(y = 1, color = 'gray')
    plt.fill_between(x=tsim_peak, y1=1, y2=0, color = 'gray', alpha = 0.5)

    plt.xlim([tsim_peak[0], tsim_peak[-1]])
    plt.ylim([0, np.max(psim_peak_rel) + 1])
    plt.title(lb)
    plt.legend()
    plt.show()

#%% EVOLTUTION OF ERROR WITH DISCRETIZATION
psim = importData(
    case = 'mach0.2_TCC_retol0',
    test='circMesh_ZU', 
    subcase='standard-TimeData',
    typeFile='time'
)

fig = make_subplots(1,2)

for i, pos in enumerate(probes):
    plotTempGO(
        psim=psim,
        probePosition=(probesPos[i], 0),
        numProbe=pos,
        numlegend=3,
        analitic= analitic_mach02,
        plotconfig=plotconfig,
        format='pdf',
        save_name=f'Probe_{pos}_comp_PPW',
        save=True
    )
    
    ta, pa = pTime(analitic_mach02, (probesPos[i], 0))
    
    inital_time_a = np.searchsorted(ta, transientTime)
    final_time_a  = np.searchsorted(ta, finalTime) + 1
    
    ErrorPhase = np.empty(len(psim))
    ErrorAmp = np.empty(len(psim))
    ppw = []
    for j, scheme in enumerate(psim):
        tprobe, pprobe = psim[scheme]
        
        inital_time_probe = np.searchsorted(tprobe, transientTime)
        final_time_probe  = np.searchsorted(tprobe, finalTime) + 1
        
        EPhase, EAmp = phaseAmplitude(pta = (ta[inital_time_a:final_time_a], pa[inital_time_a:final_time_a]),
                                     ptsim = (tprobe[inital_time_probe:final_time_probe], pprobe[inital_time_probe:final_time_probe, pos])
                                     )
        ErrorPhase[j]=EPhase
        ErrorAmp[j]=EAmp
        ppw .append( float( findall(r'\d+',scheme.split(' ')[1])[0] ) )
        

    sortIdx = np.argsort(ppw)
    ppw     = np.sort(ppw)
    ErrorPhase = ErrorPhase[sortIdx]
    ErrorAmp = ErrorAmp[sortIdx]
    
    legend = f'x = {coord[i]:^2}λd'
    fig.add_trace(
        go.Scatter(
            x = ppw,
            y = ErrorAmp*100,
            mode = 'lines+markers',
            line = dict(color = COLORS[i]),
            name =  legend,
            
        ),
        row = 1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x = ppw,
            y = ErrorPhase,
            mode = 'lines+markers',
            line = dict(color = COLORS[i]),
            showlegend=False,
            name= f'Probe n º {pos}',
        ),
        row = 1, col=2
    )
    
fig.update_layout(
        font = dict(
            color = 'black', 
            family = 'Times New Roman', 
            size = 22
        ),
        template = 'plotly_white',
        legend = dict(
            # x = 0.95,
            font = dict(
                family = 'Times New Roman',
                size = 16,
                color = 'black'
            ) 
        ),
        autosize=False,
        width=1200,
        height=500,
        margin=dict(l=10, r = 10, t = 25, b = 20),
)
fig.update_xaxes(title_text = r'$PPW$', tickvals = ppw, **plotconfig2, row=1, col=1)
fig.update_xaxes(title_text = r'$PPW$', tickvals = ppw, **plotconfig2, row=1, col=2)
fig.update_yaxes(title_text = r'$Erro \ de \ Amplitude \ [\%]$',  **plotconfig2, row = 1, col=1)
fig.update_yaxes(title_text = r'$Erro \ de \ Fase \ [deg]$',    **plotconfig2, row = 1, col=2)

fig.show()

name = 'erros_time_comp_ppw'
save_interaticve = PATH_IMAGES.joinpath('plotly-interactive', 'error', f'{name}.html')
save_image = PATH_IMAGES.joinpath('results', 'error', f'{name}.pdf')
fig.write_html(save_interaticve)
fig.write_image(save_image, format ='pdf', scale = 5)
 # %% VARIAÇÃO DOS ESQUEMAS ESPACIAIS
for ppw in [16, 32]:
    aux = f'{ppw} PPW'
    print(f'{aux:-^20}')
    psimS = importData(
        case = 'mach0.2_TCC_retol0',
        test='circMesh_ZU', 
        subcase='spacialSchemes-TimeData',
        typeFile='time',
        keyword=f'{ppw}ppw'
    )
    psimaux = importData(
        case = 'mach0.2_TCC_retol0',
        test='circMesh_ZU', 
        subcase='standard-TimeData',
        typeFile='time',
        keyword=f'{ppw}ppw'
    )
    psim = {**psimS, **psimaux}
    schemes = [i.split(' ')[0] for i in list(psim.keys())]

    fig = make_subplots(1,2, specs= [[{'type':'bar'}]*2])
    
    dataAmp = []
    dataPhase = []
    
    for i, pos in enumerate(probes):
        plotTempGO(
        psim=psim,
        probePosition=(probesPos[i], 0),
        numProbe=pos,
        numlegend=1,
        analitic= analitic_mach02,
        plotconfig=plotconfig,
        format='pdf',
        save_name=f'Probe_{pos}_comp_spacial_schemes_{ppw}PPW',
        save=True
    )
        
        ta, pa = pTime(analitic_mach02, (probesPos[i], 0))
        
        inital_time_a = np.searchsorted(ta, transientTime)
        final_time_a  = np.searchsorted(ta, finalTime) + 1
        
        ErrorPhase = np.empty(len(psim))
        ErrorAmp = np.empty(len(psim))
        for j, scheme in enumerate(psim):
            tprobe, pprobe = psim[scheme]
            
            inital_time_probe = np.searchsorted(tprobe, transientTime)
            final_time_probe  = np.searchsorted(tprobe, finalTime) + 1
            
            EPhase, EAmp = phaseAmplitude(pta = (ta[inital_time_a:final_time_a], pa[inital_time_a:final_time_a]),
                                        ptsim = (tprobe[inital_time_probe:final_time_probe], pprobe[inital_time_probe:final_time_probe, pos])
                                        )
            ErrorPhase[j]=EPhase
            ErrorAmp[j]=EAmp
            

        
        legend = f'x = {coord[i]:^2}λd'
        dataAmp.append(go.Bar(
            x = schemes, y = ErrorAmp*100, 
            name = legend, 
            showlegend=True   , marker=dict(color = COLORS[i]),
            text = [f'{erro:.1f}' for erro in ErrorAmp*100],
            textposition = 'outside'
            ))
        dataPhase.append(go.Bar(
            x = schemes, y = ErrorPhase, 
            name=legend, 
            showlegend=False, marker=dict(color = COLORS[i]),
            text = [f'{erro:.1f}' for erro in ErrorPhase],
            textposition = 'outside'
            ))
    
    fig.add_traces(dataAmp, rows=1, cols=1)
    fig.add_traces(dataPhase, rows=1, cols=2)
        
    fig.update_layout(
            font = dict(
                color = 'black', 
                family = 'Times New Roman', 
                size = 22
            ),
            template = 'plotly_white',
            legend = dict(
                # x = 0.95,
                font = dict(
                    family = 'Times New Roman',
                    size = 16,
                    color = 'black'
                ) 
            ),
            autosize=False,
            width=1200,
            height=500,
            margin=dict(l=10, r = 10, t = 25, b = 20),
            barmode = 'group'
    )
    fig.update_xaxes(title_text = r'$Esquemas Espaciais$', **plotconfig2, row=1, col=1)
    fig.update_xaxes(title_text = r'$Esquemas Espaciais$', **plotconfig2, row=1, col=2)
    fig.update_yaxes(title_text = r'$Erro \ de \ Amplitude \ [\%]$',  **plotconfig2, row = 1, col=1)
    fig.update_yaxes(title_text = r'$Erro \ de \ Fase \ [deg]$',    **plotconfig2, row = 1, col=2)

    fig.show()

    name = f'erros_time_comp_spacial_schemes_{ppw}PPW'
    save_interaticve = PATH_IMAGES.joinpath('plotly-interactive', 'error', f'{name}.html')
    save_image = PATH_IMAGES.joinpath('results', 'error', f'{name}.pdf')
    fig.write_html(save_interaticve)
    fig.write_image(save_image, format ='pdf', scale = 5)

# %% VARIAÇÃO DOS ESQUEMAS TEMPORAIS
moving_avg = [10, 5, 5]
for ni,n in enumerate([400, 800, 1000]):
    aux = f'n = {n}'
    print(f'{aux:-^20}')
    psim = importData(
        case = 'mach0.2_TCC_retol0',
        test='circMesh_ZU', 
        subcase='timeSchemes-TimeData',
        typeFile='time',
        keyword=f'n{n}'
    )
  
    schemes = [i.split(' ')[0] for i in list(psim.keys())]

    fig = make_subplots(1,2, specs= [[{'type':'bar'}]*2])
    
    dataAmp = []
    dataPhase = []
    
    for i, pos in enumerate(probes):
        aux = f'Probe n º{pos}'
        print(f'{aux:-^20}')
        plotTempGO(
        psim=psim,
        probePosition=(probesPos[i], 0),
        numProbe=pos,
        numlegend=1,
        analitic= analitic_mach02,
        plotconfig=plotconfig,
        format='pdf',
        save_name=f'Probe_{pos}_comp_time_schemes_n{n}',
        save=True
    )
        
        ta, pa = pTime(analitic_mach02, (probesPos[i], 0))
        
        inital_time_a = np.searchsorted(ta, transientTime)
        final_time_a  = np.searchsorted(ta, finalTime) + 1
        
        ErrorPhase = np.empty(len(psim))
        ErrorAmp = np.empty(len(psim))
        for j, scheme in enumerate(psim):
            tprobe, pprobe = psim[scheme]
            
            inital_time_probe = np.searchsorted(tprobe, transientTime)
            final_time_probe  = np.searchsorted(tprobe, finalTime) + 1
            
            EPhase, EAmp = phaseAmplitude(pta = (ta[inital_time_a:final_time_a], pa[inital_time_a:final_time_a]),
                                        ptsim = (tprobe[inital_time_probe:final_time_probe], pprobe[inital_time_probe:final_time_probe, pos]),
                                        moving_avg= moving_avg[ni]
                                        )
            ErrorPhase[j]=EPhase
            ErrorAmp[j]=EAmp
            

        
        legend = f'x = {coord[i]:^2}λd'
        dataAmp.append(go.Bar(
            x = schemes,  y = ErrorAmp*100, 
            name = legend, 
            showlegend=True, marker=dict(color = COLORS[i]), 
            text = [f'{erro:.1f}' for erro in ErrorAmp*100],
            textposition = 'outside'
            ))
        dataPhase.append(go.Bar(
            x = schemes, y = ErrorPhase, 
            name=legend, 
            showlegend=False, marker=dict(color = COLORS[i]), 
            text = [f'{erro:.1f}' for erro in ErrorPhase],
            textposition = 'outside'
            ))
    
    fig.add_traces(dataAmp, rows=1, cols=1)
    fig.add_traces(dataPhase, rows=1, cols=2)
        
    fig.update_layout(
            font = dict(
                color = 'black', 
                family = 'Times New Roman', 
                size = 22
            ),
            template = 'plotly_white',
            legend = dict(
                # x = 0.95,
                font = dict(
                    family = 'Times New Roman',
                    size = 16,
                    color = 'black'
                ) 
            ),
            autosize=False,
            width=1200,
            height=500,
            margin=dict(l=10, r = 10, t = 25, b = 20),
            barmode = 'group'
    )
    fig.update_xaxes(title_text = r'$Esquemas Temporais$', **plotconfig2, row=1, col=1)
    fig.update_xaxes(title_text = r'$Esquemas Temporais$', **plotconfig2, row=1, col=2)
    fig.update_yaxes(title_text = r'$Erro \ de \ Amplitude \ [\%]$',  **plotconfig2, row = 1, col=1)
    fig.update_yaxes(title_text = r'$Erro \ de \ Fase \ [deg]$',    **plotconfig2, row = 1, col=2)

    fig.show()

    name = f'erros_time_comp_time_schemes_n{n}'
    save_interaticve = PATH_IMAGES.joinpath('plotly-interactive', 'error', f'{name}.html')
    save_image = PATH_IMAGES.joinpath('results', 'error', f'{name}.pdf')
    fig.write_html(save_interaticve)
    fig.write_image(save_image, format ='pdf', scale = 5)
# %%
