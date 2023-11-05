#%%
from pathlib import Path

a = Path().absolute()
print(a.as_posix())
with open(a.joinpath('test.txt'), 'r+') as file:
    print(file.read())
    file.write('sim')

from src.path import PATH_MESH
# %%
