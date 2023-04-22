#%% Library
from pathlib import Path
#%% Caminhos Importantes do repositório
path      = Path().absolute()
dir       = 'Aeroacoustics-Resonators' 

if not(path.name == dir): 
    condition = any(i.name == dir for i in path.parents[:])
    assert condition, "Diretório não existe"
    for i in range(len(path.parents)):
        if path.parents[i].name == dir:
            path = path.parents[i]
            break
    
PATH_IMAGES = path.joinpath('images')
PATH_DATA   = path.joinpath('data')
PATH_PROBES = path.joinpath('observers')

PATH_IMAGES.mkdir(exist_ok=True)
PATH_PROBES.mkdir(exist_ok=True)
PATH_DATA.mkdir(exist_ok=True)