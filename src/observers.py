#%% Librarys
import numpy as np

from src.datadrive import PATH_WRITE
from re import sub
from pathlib import Path
from string import ascii_letters

#%% Funções
# PATH_WRITE = Path().absolute().parent / 'observers'
# if not PATH_WRITE.exists():
#     PATH_WRITE.mkdir()


def probes(
    number_of_probes: int = 30,
    lim: tuple = (2, 102),
    name_of_archive: str = 'probesTime',
    field: str = 'p',
):
    p = np.linspace(lim[0], lim[1], number_of_probes)

    arq = open(PATH_WRITE / 'templateProbe.txt', 'r').read()

    arq = sub('&', name_of_archive, arq)
    arq = sub('@', field, arq)

    write = 'probeLocations\n\t\t(\n'
    for i in p:
        write += f'\t\t\t({round(i,3)} 0 0)\n'
    write += '\t\t);'

    arq = sub('#', write, arq)

    with open(PATH_WRITE / name_of_archive, 'w') as file:
        file.write(arq)


def microphones(
    number_of_observer: int = 30, lim: tuple = (2, 102), lenght: float = 1
):
    m = np.linspace(lim[0], lim[1], number_of_observer)
    letter = list(ascii_letters)
    with open(PATH_WRITE / 'microphonesTimeS.txt', 'w') as file:
        file.write('observers\n{\n')
        for k, i in enumerate(m):
            file.write(f'\tR-{letter[k]}\n' + '\t{\n')
            file.write(f'\t\tposition\t({round(i,3)} 0 {lenght/2});\n')
            file.write('\t\tpRef\t2.0e-5;\n')
            file.write('\t\tfftFreq\t1024;\n\t}\n')
        file.write('}')


#%% Run
probes(
    number_of_probes=40_000, lim=(-100, 100), name_of_archive='probesTimeFlow'
)
# microphones(number_of_observer=51)
# %%
