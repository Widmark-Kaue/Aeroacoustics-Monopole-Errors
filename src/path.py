#%% Library
from pathlib import Path
#%% Caminhos Importantes do repositório
if not Path('/workspaces') in Path().cwd().parents:
    for path in Path.home().glob('**/Aeroacoustics-Resonators'):
        PATH_DATA = path.joinpath('data')
        break
else:
    for path in Path.home().parent.with_name('workspaces').glob('Aeroacoustics-Resonators'):
        PATH_DATA = path.joinpath('data')
        break
PATH_DATA.mkdir(exist_ok=True) 