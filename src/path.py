#%% Library
from pathlib import Path
#%% Caminhos Importantes do repositório
path = Path().absolute()
if not(path.name == 'Aeroacoustics-Resonators'): 
    for i in range(len(path.parents)):
        if path.parents[i].name == 'Aeroacoustics-Resonators':
            path = path.parents[i]
            break
    
    assert False, "Diretório não existe"

PATH_DATA = path.joinpath('data')
PATH_PROBES = path.joinpath('observers')

PATH_PROBES.mkdir(exist_ok=True)
PATH_DATA.mkdir(exist_ok=True)