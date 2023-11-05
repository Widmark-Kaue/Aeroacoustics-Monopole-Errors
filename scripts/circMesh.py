#%% lib
import numpy as np
import matplotlib.pyplot as plt

import gmsh as gm
import pygmsh as pg
import pyvista as pv

from pathlib import Path 

PATH_MESH = Path().absolute().joinpath('..', 'mesh', 'monopoleFlow', 'mach0.2', 'circMesh.geo')
PATH_SAVE_MESH = PATH_MESH.parent.parent.joinpath('msh')
PATH_SAVE_MESH.mkdir(exist_ok=True)

if not PATH_MESH.exists():
    assert False, 'File not found'
#%% loading mesh and save vtk file
gm.initialize()
gm.open(PATH_MESH.as_posix())
gm.write(PATH_SAVE_MESH.joinpath('circMesh.vtk').as_posix())
#%% pyvista manipulation
mesh = pv.read(PATH_SAVE_MESH.joinpath('circMesh.vtk'))
pl = pv.Plotter()

pl.add_mesh(mesh, style = 'wireframe', color ='k')
pl.camera_position = 'xy'
pl.show()
# %%
