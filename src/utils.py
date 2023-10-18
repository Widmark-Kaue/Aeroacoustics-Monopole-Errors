import matplotlib.pyplot as plt
import plotly.graph_objects as go

from re import sub
from json import load
from src.path import *
from string import ascii_letters
from src.postprocess import rmsSpacial
from numpy import loadtxt, linspace, round, array

def importData(
        case       : str,
        test       : str,
        subtest    : str    = '',
        time       : float  = 2,
        simulation : str    = 'monopoleFlow' ,
        toPa       : float  = 101325,
        keyword    : str    = None,
        oldfile    : bool   = False
)-> dict:
    
    PATH_IMPORT = PATH_DATA.joinpath(simulation, case, test)
    
    pressure    = {}
    if keyword != None:
        arqList = PATH_IMPORT.joinpath(str(time), subtest).glob(f'*{keyword}*')
    else:
        arqList = PATH_IMPORT.joinpath(str(time), subtest).iterdir()
    
    for arq in arqList:
        p  = loadtxt(arq, comments='#')
        name = sub('_',' ', arq.stem)
        pressure.update({name: p[1:] - toPa})
    
    return pressure

def probes(
    number_of_probes: int = 30,
    lim             : tuple = (2, 102),
    name_of_archive : str = 'probesTime',
    field           : str = 'p',
)->None:
    p = linspace(lim[0], lim[1], number_of_probes)

    arq = open(PATH_PROBES / 'templateProbe.txt', 'r').read()

    arq = sub('&', name_of_archive, arq)
    arq = sub('@', field, arq)

    write = 'probeLocations\n\t\t(\n'
    for i in p:
        write += f'\t\t\t({round(i,3)} 0 0)\n'
    write += '\t\t);'

    arq = sub('#', write, arq)

    with open(PATH_PROBES.joinpath(name_of_archive), 'w') as file:
        file.write(arq)

def microphones(
    number_of_observer: int = 30, 
    lim               : tuple = (2, 102), 
    lenght            : float = 1
)-> None:
    m = linspace(lim[0], lim[1], number_of_observer)
    letter = list(ascii_letters)
    with open(PATH_PROBES.joinpath('microphonesTimeS.txt'), 'w') as file:
        file.write('observers\n{\n')
        for k, i in enumerate(m):
            file.write(f'\tR-{letter[k]}\n' + '\t{\n')
            file.write(f'\t\tposition\t({round(i,3)} 0 {lenght/2});\n')
            file.write('\t\tpRef\t2.0e-5;\n')
            file.write('\t\tfftFreq\t1024;\n\t}\n')
        file.write('}')

def plotSchemes(
    psim    :dict, 
    analitc :Path  = None, 
    xsim    :tuple = (-100, 100), 
    title   :str   = 'unknow', 
    save    :bool  = False
)-> None:
    
    line = ['dashed', 'dashdot', 'dotted', 'solid']
    if analitc != None:
        x, p = loadtxt(analitc, unpack=True)
        plt.plot(x,p, 'k', label = 'analitic solution')
    for i, scheme in enumerate(psim):
        xsimV = linspace(xsim[0],xsim[1], len(psim[scheme]))
        plt.plot(xsimV,psim[scheme], 
                 linestyle  = '--',
                 markersize = 5,
                 alpha      = 0.75,
                 label      = f'{scheme}'
                 ) 

    plt.xlabel(r'$x \ [m]$')
    plt.ylabel(r'$P \ [Pa]$')
    plt.title(fr'{title}')
    plt.legend()
    plt.grid()
    
    if save:
        aux = sub(r'\s', '_', title)
        plt.savefig(PATH_IMAGES.joinpath(f'{aux}.png'), format = 'png', dpi = 720)
    
    plt.show()
    
def plotSchemesGO(
        psim     :dict,
        analitc  :Path = None,
        time     :float = 2,
        xsim     :tuple =( -104 , 104 ),
        title    :str = 'unknow',
        legend   :int = 1,
        windows  :bool = False,
        save     :bool = False
        )-> None:

        assert 0<=legend<=3, "Error: legend could be between 0 and 3"
        
        #figure layout
        layout = go.Layout(
            autosize=False,
            width=1000,
            height=500,
            margin=dict(l=10, r = 10, t = 25, b = 20),
        )
        
        # init object
        fig = go.Figure(layout_xaxis_range = xsim, layout=layout)
        ndata = 2
        
        if analitc !=None:
            if analitc.suffix == '.dat':
                x, p = loadtxt(analitc, unpack=True)
            elif analitc.suffix == '.json':
                with open(analitc, 'r') as file:
                    data = load(file)
                    nx = data['nx']
                    ny = data['ny']
                    ypos  = linspace(data['ylim'][0], data['ylim'][1], ny).searchsorted(0) 
                    x  = linspace(data['xlim'][0], data['xlim'][1], nx)
                    p  = array(data['time'][f'{time}']).T[ypos]
            else:
                assert False, "Erro: Invalid file"
                
            
            
            fig.add_trace(
                 go.Scatter(
                     visible=True,
                     line = dict(width = 3, color = 'black'),
                     name='Analitic Solution',
                     x = x,
                     y = p
                 )
             )
            if windows:
                min_idx = x.searchsorted(xsim[0])
                max_idx = x.searchsorted(xsim[1])+1
                xaux = x[min_idx:max_idx]
                
                win = 3
                window = (xaux[-1]- xaux[0])/win
                pos = 0
                ticks = [xaux[0]]
                for i in range(win):
                    begin = pos
                    pos   = xaux.searchsorted(xaux[0] + (i+1)*window)
                    end   = pos 
                    ticks.append(xaux[end])
                
                fig.update_xaxes(tickvals = round(ticks,1), showgrid = True, gridcolor = 'gray')
        
        
             
        # simulation
        for scheme in psim:
            name = " ".join(scheme.split(' ')[:legend]) 
            addlabel = ''
            if windows:
                 rms =  rmsSpacial((x,p), psim[scheme], xsim = xsim,windows=win)
                 for i in range(len(rms)):
                     addlabel += f'win {i+1} = {round(rms[i]*100,2)} % '
            xsimV = linspace(xsim[0], xsim[1], len(psim[scheme]))
            fig.add_trace(
                go.Scatter(
                    mode= 'lines',
                    visible=True,
                    line=dict(width = 3, backoff = 0.5, dash = 'dashdot'),
                    name = name,
                    hovertext=addlabel,
                    x = xsimV,
                    y = psim[scheme]
                )
            )
            
        fig.update_layout(title = dict(text = title, font = dict(color = 'black', family = 'Arial'), x = 0.5),
                          xaxis_title = 'x [m]',
                          yaxis_title = 'P [Pa]')
        
        fig.show()

        if save:
            fig.write_html(PATH_IMAGES.joinpath(f'{title}.html'))