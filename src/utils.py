from numpy import loadtxt, array
from src.path import PATH_DATA

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

    