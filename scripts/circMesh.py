#%% lib
import numpy as np
import matplotlib.pyplot as plt

import gmsh as gm
import pygmsh as pg
import pyvista as pv
import meshio

from scipy.optimize import fsolve
from pathlib import Path 

PATH_MESH = Path().absolute().joinpath('mesh', 'monopoleFlow', 'mach0.2', 'circMesh.geo')
PATH_SAVE_MESH = PATH_MESH.parent.parent.joinpath('msh')
PATH_SAVE_MESH.mkdir(exist_ok=True)

if not PATH_MESH.exists():
    assert False, 'File not found'
#%% loading mesh and save vtk file
# gm.initialize()
# gm.open(PATH_MESH.as_posix())
# gm.write(PATH_SAVE_MESH.joinpath('circMesh.vtk').as_posix())
# #%% pyvista manipulation
# mesh = pv.read(PATH_SAVE_MESH.joinpath('circMesh.vtk'))
# pl = pv.Plotter()

# pl.add_mesh(mesh, style = 'wireframe', color ='k')
# pl.camera_position = 'xy'
# pl.show()
# %%
def is_parallel(u, v, tol = 1E-5):
    # Verificando se os vetores diretores são proporcionais
    cond1 = abs( u - v ) < tol
    if cond1:
        return True
    else:
        return False
    
def  is_intercepted(triangle_points:np.ndarray, star_point:np.ndarray, final_point:np.ndarray) -> bool:
    # pontos do triângulo
    p1 = triangle_points[0, :2]
    p2 = triangle_points[1, :2]
    p3 = triangle_points[2, :2]
    
    # vetores diretores
    v0 = final_point -star_point
    v1 = p2 - p1
    v2 = p3 - p1
    v3 = p3 - p2
    
    m0 = v0[1]/v0[0] 
    m1 = v1[1]/v1[0] 
    m2 = v2[1]/v2[0] 
    m3 = v3[1]/v3[0] 
    
    
    
    # equação da reta 
    ray_trace = lambda x: m0*(x - star_point[0]) + star_point[1]
    
    cond1 = False
    if not is_parallel(m0,m1):
        r1 = lambda x: m1*(x - p1[0]) + p1[1] 
        f1 =  lambda x: ray_trace(x) - r1(x)
        x_intersec = fsolve(f1, x0 = p1[0])
        x_interval = sorted([p1[0], p2[0]])
        y_interval = sorted([p1[1], p2[1]])
        if ( x_interval[0] <= x_intersec <= x_interval[1] ) and (y_interval[0] <= r1(x_intersec) <= y_interval[1]):
            cond1 = True
           
    cond2 = False
    if not is_parallel(m0, m2):
        r2 = lambda x: m2*(x - p1[0]) + p1[1]
        f2 =  lambda x: ray_trace(x) - r2(x)
        x_intersec = fsolve(f2, x0 = p1[0])
        x_interval = sorted([p1[0], p3[0]])
        y_interval = sorted([p1[1], p3[1]])
        if ( x_interval[0] <= x_intersec <= x_interval[1] ) and (y_interval[0] <= r2(x_intersec) <= y_interval[1]):
            cond2 = True
            
    
    cond3 = False
    if not is_parallel(m0,m3):
        r3 = lambda x: m3*(x - p2[0]) + p2[1]
        f3 =  lambda x: ray_trace(x) - r3(x)
        x_intersec = fsolve(f3, x0 = p2[0])
        x_interval = sorted([p3[0], p2[0]])
        y_interval = sorted([p3[1], p2[1]])
        if ( x_interval[0] <= x_intersec <= x_interval[1] ) and (y_interval[0] <= r3(x_intersec) <= y_interval[1]):
            cond3 = True

    if cond1 == True or cond2 == True or cond3 == True :
        return True
    else:
        return False   
    
# Carregar o arquivo .msh
mesh = meshio.read(PATH_MESH.with_name('miolo.msh'))

# Definir a linha de interceptação
ponto_inicial = np.array([0, 0])# Coordenadas do ponto inicial da linha
ponto_final = np.array([100, 0])  # Vetor direção da linha

# Encontrar os elementos interceptados
interceptados = []
cells = mesh.cells_dict['triangle']
for i in range(len(cells)):
    triangle_points = np.array([mesh.points[j] for j in cells[i]])           
    if is_intercepted(triangle_points=triangle_points, star_point=ponto_inicial, final_point=ponto_final):
        bar_centers = np.sum(triangle_points, axis = 0)/3
        plt.plot(bar_centers[0], bar_centers[1], 'b^')  
        interceptados.append(cells[i])

plt.plot([0,100], [0,0], 'r')
plt.ylim([-100,100])
plt.show()

# Contar o número de elementos interceptados
num_interceptados = len(interceptados)
print(f"O número de elementos interceptados é: {num_interceptados}")
