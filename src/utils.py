from re import sub
from src.path import *
from string import ascii_letters
from numpy import loadtxt, linspace

def importData(
        case: str,
        test: str,
        time: float = 2,
        simulation: str = 'monopoleFlow' ,
)-> dict:

    toPa     = 101325 
    pressure = {}

    PATH_IMPORT = PATH_DATA.joinpath(simulation, case, test, str(time))
    for arq in PATH_IMPORT.iterdir():
        p  = loadtxt(arq, comments='#')
        name = arq.stem.split('_')[-1]
        pressure.update({name: p[1:] - toPa})

    return pressure

def probes(
    number_of_probes: int = 30,
    lim: tuple = (2, 102),
    name_of_archive: str = 'probesTime',
    field: str = 'p',
):
    p = linspace(lim[0], lim[1], number_of_probes)

    arq = open(PATH_PROBES / 'templateProbe.txt', 'r').read()

    arq = sub('&', name_of_archive, arq)
    arq = sub('@', field, arq)

    write = 'probeLocations\n\t\t(\n'
    for i in p:
        write += f'\t\t\t({round(i,3)} 0 0)\n'
    write += '\t\t);'

    arq = sub('#', write, arq)

    with open(PATH_PROBES / name_of_archive, 'w') as file:
        file.write(arq)


def microphones(
    number_of_observer: int = 30, lim: tuple = (2, 102), lenght: float = 1
):
    m = linspace(lim[0], lim[1], number_of_observer)
    letter = list(ascii_letters)
    with open(PATH_PROBES / 'microphonesTimeS.txt', 'w') as file:
        file.write('observers\n{\n')
        for k, i in enumerate(m):
            file.write(f'\tR-{letter[k]}\n' + '\t{\n')
            file.write(f'\t\tposition\t({round(i,3)} 0 {lenght/2});\n')
            file.write('\t\tpRef\t2.0e-5;\n')
            file.write('\t\tfftFreq\t1024;\n\t}\n')
        file.write('}')