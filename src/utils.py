import matplotlib.pyplot as plt
import plotly.graph_objects as go


from re import sub
from json import load
from src.path import *
from string import ascii_letters
from src.postprocess import rmsSpacial
from plotly.colors import DEFAULT_PLOTLY_COLORS as COLORS
from numpy import loadtxt, linspace, round, array, searchsorted

def importSpacialData(arqList: list, toPa: float, xsim_range: tuple) -> dict:
    pressure    = {}
    for arq in arqList:
        p  = loadtxt(arq, comments='#')
        p = p[1:]
        name = sub('_',' ', arq.stem)
        
        if not xsim_range == None:
            xsimVec = linspace(xsim_range[0], xsim_range[1], len(p))
            left = searchsorted(xsimVec,xsim_range[2], side='left')
            right =  searchsorted(xsimVec, xsim_range[3], side='right') + 1
            p = p[left:right]   
        pressure.update({name: p - toPa})
    return pressure

def importTimeData(arqList: list, toPa: float, num_probe:int) -> dict:
    pressure = {}
    for arq in arqList:
        data = loadtxt(arq, comments='#')
        p = data[:, 1:]
        t = data[:,0]
        name = sub('_', ' ', arq.stem)
        
        if not num_probe == None:
            _,col = p.shape
            assert num_probe <= col, 'Error: Num probe exceed number of probes'
            p = p[:,num_probe]
        pressure.update({name: (t, p - toPa)})
    return pressure

def importData(
        case       : str,
        test       : str,
        subcase    : str    = '',
        subtest    : str    = '',
        time       : float  = 2,
        simulation : str    = 'monopoleFlow' ,
        toPa       : float  = 101325,
        keyword    : str    = None,
        oldfile    : bool   = False,
        xsim_range : tuple  = None,
        num_probe  : int    = None,
        typeFile   : str    = 'spacial' 
)-> dict:
    
    PATH_IMPORT = PATH_DATA.joinpath(simulation, case, test, subcase)
    
    if typeFile == 'spacial':
        if keyword != None:
            arqList = PATH_IMPORT.joinpath(str(time), subtest).glob(f'*{keyword}*')
        else:
            arqList = PATH_IMPORT.joinpath(str(time), subtest).iterdir()
        
        pressure = importSpacialData(arqList=arqList, toPa=toPa, xsim_range=xsim_range)
    elif typeFile == 'time':
        if keyword != None:
            arqList = PATH_IMPORT.joinpath(subtest).glob(f'*{keyword}*')
        else:
            arqList = PATH_IMPORT.joinpath(subtest).iterdir()
        pressure = importTimeData(arqList=arqList, toPa=toPa, num_probe=num_probe)
    else:
        assert False, 'Error: typeFile not recognized.'
    
    return pressure
    
def probes(
    name_of_archive : str,
    number_of_probes: int = 30,
    lim             : tuple = (2, 102),
    field           : str = 'p',
    subpath         : Path = None,
    p               : array = None
)->None:

    arq = open(PATH_PROBES / 'templateProbe.txt', 'r').read()

    arq = sub('&', name_of_archive, arq)
    arq = sub('@', field, arq)

    write = 'probeLocations\n\t\t(\n'
    
    if p.any() == None:
        p = linspace(lim[0], lim[1], number_of_probes)
    
        for i in p:
            write += f'\t\t\t({round(i,3)} 0 0)\n'
        write += '\t\t);'
    else:
        for i in range(len(p)):
            write += f'\t\t\t({round(p[i,0],3)} {round(p[i,1],3)} 0)\n'
        write += '\t\t);'
         
    arq = sub('#', write, arq)

    
    if subpath == None:
        path = PATH_PROBES.joinpath(name_of_archive) 
    else: 
        path = PATH_PROBES.joinpath(subpath,name_of_archive)
        
    with open(path, 'w') as file:
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
        title    :str = '',
        numlegend:int = 1,
        legend   :list = None,
        windows  :bool = False,
        save     :bool = False,
        show     :bool = True,
        format   :str  = 'html',
        save_name:str  = None,
        plotconfig:dict= dict()
        )-> None:

        assert 0<=numlegend<=3, "Error: numlegend could be between 0 and 3"
        if not legend == None:
            assert len(legend) == len(list(psim.keys())), 'Error: lengend list must be the same dimension of psim keys'
        
        #figure layout
        layout = go.Layout(
            autosize=False,
            width=1000,
            height=500,
            margin=dict(l=10, r = 10, t = 25, b = 20),
        )
        
        # init object
        fig = go.Figure(layout=layout)
        
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
                     line = dict(width = 2, color = 'black'),
                     name='Solução analítica',
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
                
                fig.update_xaxes(
                    tickvals = round(ticks,1), 
                    ticktext = [-3, -1, 1, 3],
                    showgrid = True, 
                    gridcolor = 'gray',
                    range = data['xlim']
                    )
             
        # simulation
        for j, scheme in enumerate(psim):
            if legend == None:
                name = " ".join(scheme.split(' ')[:numlegend])
            else:
                name = legend[j] 
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
                    line=dict(width = 2, backoff = 0.5, color = COLORS[j]),
                    name = name,
                    hovertext=addlabel,
                    x = xsimV,
                    y = psim[scheme],
                    opacity=0.75
                )
            )
            
        fig.update_layout(
                        title = dict(
                            text = title, 
                            font = dict(
                                color = 'black', 
                                family = 'Times'
                                ), 
                            x = 0.5
                        ),
                        xaxis_title = dict(text = r'$x/\lambda_d$'),
                        yaxis_title = dict( text = r'$P \ [Pa]$'),
                        font = dict(
                            color = 'black', 
                            family = 'Times New Roman', 
                            size = 22
                        ),
                        template = 'plotly_white',
                        legend = dict(
                            yanchor = 'top', 
                            xanchor = 'right',
                            x = 0.95, 
                            font = dict(
                                family = 'Times New Roman',
                                size = 16,
                                color = 'black'
                            ) 
                        ),
                        **plotconfig
        )
        
        
        if show: fig.show()

        if save:
            name_image = save_name if save_name != None else 'unknow'
            if format == 'html':
                fig.write_html(PATH_IMAGES.joinpath('plotly-interactive',f'{name_image}.html'))
            else:
                if format not in name_image: name_image = f'{name_image}.{format}'
                fig.write_image(PATH_IMAGES.joinpath('results',f'{name_image}'), format = format, scale = 5)
        
        return fig