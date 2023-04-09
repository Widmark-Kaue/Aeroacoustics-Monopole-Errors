from src.path import *

################################################################
# Configurações para rodar o módulo src em qualquer pasta
################################################################

# Caminho do projeto
PROJECT = PATH_DATA.parent

# Caminho do virtualenv activate
activate_path = PROJECT.joinpath('.venv','bin','activate')

# Modificação do arquivo
export_line = f'export PYTHONPATH="{PROJECT.as_posix()}"\n'
with open(activate_path, 'r+') as file:
    lines = file.readlines()
    if not export_line in lines:
        for i, line in enumerate(lines):
            if 'VIRTUAL_ENV=' in line:                
                lines.insert(i + 1, f'{export_line}')
                break
        #Início do arquivo
        file.seek(0)
        file.writelines(lines)
    else:
        pass
