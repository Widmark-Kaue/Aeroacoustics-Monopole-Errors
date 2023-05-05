import matplotlib.pyplot as plt

from re import sub
from src.path import *
from string import ascii_letters
from numpy import loadtxt, linspace

def importData(
        case       : str,
        test       : str,
        time       : float  = 2,
        simulation : str    = 'monopoleFlow' ,
        toPa       : float  = 101325
)-> dict:
    
    PATH_IMPORT = PATH_DATA.joinpath(simulation, case, test)
    pressure    = {}
    if time != None:
        for arq in PATH_IMPORT.joinpath(str(time)).iterdir():
            p  = loadtxt(arq, comments='#')
            name = arq.stem.split('_')[-1]
            pressure.update({name: p[1:] - toPa})
    else:
        for arq in PATH_IMPORT.glob('*.dat'):
            tp = loadtxt(arq, comments='#')
            tp[:,1:] = tp[:,1:] - toPa
            name = arq.stem.split('_')[-1]
            pressure.update({name: tp})
    
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
