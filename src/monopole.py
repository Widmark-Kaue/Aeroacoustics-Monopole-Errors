"""
Baseado no código do prof. Juan
"""
import numpy as np
import sympy as sy
import pandas as pd
import pickle as pc

from json import dump, load
from scipy.signal import fftconvolve
from scipy.special import hankel1
from src.path import PATH_DATA, Path
from typing import Union, Iterable
from joblib import Parallel, delayed

def monopoleFlowSy (
    t:              Union[float, list] = 2,
    xlim:           tuple = (-200, 200),
    ylim:           tuple = (-200, 200),
    nxy:            tuple = (401, 401),
    alpha:          float = np.log(2) / 9,
    freq:           float = 10,
    M:              float = 0.5,
    gamma:          float = 1.4,
    PTR:            tuple = (101325, 298.15, 8314.46261815324 / 28.9),
    writeInterval:  int   = 1,
    printInterval:  float = 10,
    savePath:       Path  = PATH_DATA,
    outName:        str   = None
)->None:
    assert 0 <= M <= 1, 'mach number must be between 0 and 1'
    
    # Save configurations
    savePath.mkdir(exist_ok=True, parents=True)
    
    if outName == None:
        outName = f'monopole_M{M}.json'
    elif outName.split('.')[-1] != 'json':
        outName = f'{outName}.json'
        
    filePath = savePath.joinpath(outName) 
    
    # variables
    P0, T0, R   = PTR
    omega       = freq * 2 * np.pi
    c0          = np.sqrt(gamma*R*T0)
    k           = omega/c0
    epsilon     = P0*gamma
     
    # vectors
    nx, ny      = nxy
    x           = np.linspace(xlim[0], xlim[1], nx, dtype = float)
    y           = np.linspace(ylim[0], ylim[1], ny, dtype = float)
    deltax      = x[1] - x[0] 
    deltay      = y[1] - y[0]
    f           = np.zeros(nxy, dtype=float)
    H           = np.zeros(nxy, dtype=float)
    
    # simbolic variables
    xSy, ySy, tSy =  sy.symbols('xSy ySy tSy', real=True)
    
    ksiSy = omega*sy.sqrt(xSy**2 + (1-M**2)*ySy**2)/(c0*(1-M**2))
    etaSy = -sy.I*M/(1 - M**2)*k*xSy - sy.I*omega*tSy
    
        
    GSy   = sy.I/(4*c0**2 *np.sqrt(1 - M**2)) 
    GSy  *= sy.hankel1(0, ksiSy) 
    GSy  *= sy.exp(etaSy)
    
    dGdxSy = sy.diff(GSy, xSy)
    dGdtSy = sy.diff(GSy, tSy)
    
    Hsy        = sy.im(dGdtSy + M * c0*dGdxSy)
    
    # create dict
    [X,Y] = np.meshgrid(x,y)
    DATA = {
        'X'         : X.tolist(),
        'Y'         : Y.tolist(),
        'freq'      : freq,
        'M'         : M,
        'c0'        : c0,
        'gamma'     : gamma,
        'P0'        : P0,
        'T0'        : T0,
        'R'         : R,
        'alpha'     : alpha,
        'epsilon'   : epsilon,
        'k'         : k,
        'xlim'      : xlim,
        'ylim'      : ylim,
        'nx'        : nx,
        'ny'        : ny,
        'time'      : {}
    }
    with open(filePath, 'w') as file:
        dump(DATA, file)
    
    # Time iterarion
    time = {}
    try:
        t = list(t)
    except:
        t = [t]
    for it, tk in enumerate(t):
        print(5*'-'+f' t obs = {tk} '+'-'*5)
        for i, xi in enumerate(x):
            for j, yj in enumerate(y):
                H[i,j] = Hsy.xreplace(
                    {
                        xSy: xi,
                        ySy: yj,
                        tSy: tk,
                    }
                ).evalf()

                # Gaussian distribution of amplitude
                f[i, j] = epsilon * np.exp(-alpha * (xi**2 + yj**2))
            if xi%printInterval == 0:
                print(f' - X = {xi} - Complete')
        
        #Field resolution
        pFlow = fftconvolve(f, H, 'same')*deltax*deltay
        time.update({f'{tk}': pFlow.tolist()})

        cond = True if writeInterval == 1 else (it+1)%writeInterval == 0
        if cond:
            with open(filePath, 'r') as file:
                data = load(file)
            
            # update time dictionary
            data['time'] = time
            with open(filePath, 'w') as file:
                dump(data, file)
        
def monopoleFlowSyE (
    t:              Union[float, list] = 2,
    xlim:           tuple = (-200, 200),
    ylim:           tuple = (-200, 200),
    nxy:            tuple = (401, 401),
    alpha:          float = np.log(2) / 9,
    freq:           float = 10,
    M:              float = 0.5,
    gamma:          float = 1.4,
    PTR:            tuple = (101325, 298.15, 8314.46261815324 / 28.9),
    writeInterval:  int   = 1,
    printInterval:  float = 10,
    savePath:       Path  = PATH_DATA,
    outName:        str   = None,
    parrallel:      bool  = False,
    njobs:          int   = -1 
)->None:
    assert 0 <= M <= 1, 'mach number must be between 0 and 1'
    
    # Save configurations
    savePath.mkdir(exist_ok=True, parents=True)
    
    if outName == None:
        outName = f'monopole_M{M}'
    
    
    filePath = savePath.joinpath(outName)
    if filePath.suffix != '.pkl':
        filePath = filePath.with_suffix('.pkl')
    
    
    # variables
    P0, T0, R   = PTR
    omega       = freq * 2 * np.pi
    c0          = np.sqrt(gamma*R*T0)
    k           = omega/c0
    epsilon     = P0*gamma
     
    # vectors
    nx, ny      = nxy
    x           = np.linspace(xlim[0], xlim[1], nx, dtype = float)
    y           = np.linspace(ylim[0], ylim[1], ny, dtype = float)
    deltax      = x[1] - x[0] 
    deltay      = y[1] - y[0]
    f           = np.zeros(nxy, dtype=float)
    H           = np.zeros(nxy, dtype=float)
    
    # simbolic variables
    xSy, ySy, tSy =  sy.symbols('xSy ySy tSy', real=True)
    
    ksiSy = omega*sy.sqrt(xSy**2 + (1-M**2)*ySy**2)/(c0*(1-M**2))
    etaSy = -sy.I*M/(1 - M**2)*k*xSy - sy.I*omega*tSy
        
    GSy   = sy.I/(4*c0**2 *np.sqrt(1 - M**2)) 
    GSy  *= sy.hankel1(0, ksiSy) 
    GSy  *= sy.exp(etaSy)
    
    dGdxSy = sy.diff(GSy, xSy)
    dGdtSy = sy.diff(GSy, tSy)
    
    Hsy        = sy.im(dGdtSy + M * c0*dGdxSy)
    Hsy        = sy.simplify(Hsy)
    Hsy_np     = sy.lambdify((xSy, ySy, tSy), Hsy.xreplace({sy.hankel1: hankel1}), 'scipy')
    
    # create dict
    [X,Y] = np.meshgrid(x,y)
    DATA = {
        'X'         : X,
        'Y'         : Y,
        'freq'      : freq,
        'M'         : M,
        'c0'        : c0,
        'gamma'     : gamma,
        'P0'        : P0,
        'T0'        : T0,
        'R'         : R,
        'alpha'     : alpha,
        'epsilon'   : epsilon,
        'k'         : k,
        'xlim'      : xlim,
        'ylim'      : ylim,
        'nx'        : nx,
        'ny'        : ny,
        'time'      : {}
    }
    with open(filePath, 'wb') as file:
        pc.dump(DATA, file)
    
    # Time iterarion
    time = {}
    try:
        t = list(t)
    except:
        t = [t]
        
    # cache
    y_squared = y**2
    for it, tk in enumerate(t):
        print(5*'-'+f' t obs = {tk} '+'-'*5)
        
        if parrallel:
            result = Parallel(n_jobs=njobs) (delayed(solve_parallel)(
                Hsy = Hsy, 
                Hsy_np = Hsy_np, 
                y = y,
                y_squared = y_squared,
                tk = tk, 
                xi = xi,
                epsilon =epsilon,
                alpha = alpha,
                symbols = (xSy, ySy, tSy), 
                printInterval = printInterval) for xi in x)
        
        for i, xi in enumerate(x):
            if not parrallel:
                    xi_squared = xi**2      # cache
                    if xi == 0:
                        zero_pos = list(y).index(0)
                        H[i, :zero_pos  ] = Hsy_np(xi,   y[:zero_pos  ], tk)
                        H[i, zero_pos+1:] = Hsy_np(xi, y[zero_pos+1:], tk)
                        H[i, zero_pos] = Hsy.xreplace(
                            {
                                xSy: xi,
                                ySy: y[zero_pos],
                                tSy: tk,
                            }
                        ).evalf()
                    else:
                        H[i] = Hsy_np(xi, y, tk)
                        
                    # Gaussian distribution of amplitude
                    f[i] = epsilon * np.exp(-alpha * (xi_squared + y_squared))
                    if xi%printInterval == 0:
                        print(f' - X = {xi} - Complete')
            else:
                faux, Haux = result[i]
                H[i] = Haux
                f[i] = faux
                
        
        #Field resolution
        pFlow = fftconvolve(f, H, 'same')*deltax*deltay
        time.update({f'{float(tk)}': pFlow})

        
        if writeInterval == 1 or tk == t[-1]:
            cond = True
        else:
            cond = (it+1)%writeInterval == 0 
        
        if cond:    
            data = pd.read_pickle(filePath)
            
            # update time dictionary
            data['time'] = time
            with open(filePath, 'wb') as file:
                pc.dump(data, file)

def pTime(analitic:Path, probePosition: tuple) -> tuple:
    
    if analitic.exists():
        sim = pd.read_pickle(analitic)
                       
        x, y = probePosition
        idx = list(sim['X'][0]).index(x)                 
        idy = list(sim['Y'][:, 0]).index(y)                 
        
        t = np.array(list(sim['time'].keys())).astype(float)
        p = np.array([sim['time'][f'{time}'].T[idy, idx] for time in t])
    else:
        assert False, "Erro: Invalid file"
    
    return t, p        
    
def pSpacial(analitic:Path, time: float, xpos: float = None, ypos: float = 0) -> tuple:
    time = float(time)
    if analitic.exists():
        if analitic.suffix == '.dat':
                x, p = np.loadtxt(analitic, unpack=True)
        
        elif analitic.suffix == '.json':
            with open(analitic, 'r') as file:
                data = load(file)
                nx = data['nx']
                ny = data['ny']
                idy  = np.searchsorted(np.linspace(data['ylim'][0], data['ylim'][1], ny), ypos)
                x  = np.linspace(data['xlim'][0], data['xlim'][1], nx)
                p  = np.array(data['time'][f'{time}']).T[idy]
        
        elif analitic.suffix == '.pkl':
            sim = pd.read_pickle(analitic)            
            idy = np.searchsorted(sim['Y'][:,0], ypos)
            x = sim['X'][0]
            p = sim['time'][f'{time}'].T[idy]
        else:
            assert False, "Erro: Invalid file"
        
    return x, p

def pRadial(analitic: Path, time: float, radius: Iterable[Union[float, int]], theta:list = None, dtheta:float = 15) -> tuple:
    # load solution
    time = float(time)
    
    if analitic.exists():
        if analitic.suffix == '.json':
            with open(analitic, 'r') as file:
                sim = load(file)
                X   = sim['X'][0]
                Y   = sim['Y'][:,0] 
                p   = np.array(sim['time'][f'{time}']).T
        
        elif analitic.suffix == '.pkl':
            sim = pd.read_pickle(analitic)            
            X   = sim['X'][0]
            Y   = sim['Y'][:,0]
            p   = sim['time'][f'{time}'].T
        else:
            assert False, "Erro: Invalid file"
    
    # Create theta vector
    theta = np.arange(0, 90 + dtheta, dtheta)

    theta = np.deg2rad(theta)
    
    if not isinstance(radius, Iterable):
        radius = [radius]
        
    # Create data matrix
    thetaS = []
    pS = []        
    for r in radius:
        cond = any(X <= r) or any (Y <= r)

        if cond:
            x = np.round(r*np.cos(theta), 3)
            y = np.round(r*np.sin(theta), 3)
        
            xpos = np.searchsorted(X, x)
            ypos = np.searchsorted(Y, y)
            
            xdiff = np.insert(np.diff(xpos), 0, -1)
            ydiff = np.insert(np.diff(ypos),len(ypos)-1, -1)
            
            xpos[xdiff==0] = xpos[xdiff==0] + 1
            ypos[ydiff==0] = ypos[ydiff==0] + 1
            
            # 1º quadrant
            xcoord = X[xpos]
            ycoord = Y[xpos]

            # 1º and 2 º quadrant
            xcoord = np.insert(xcoord, len(xcoord), -xcoord[:-1])
            ycoord = np.insert(ycoord, len(ycoord), ycoord[-2::-1])
            
            # 3º and 4º quadrant
            xcoord = np.insert(xcoord, len(xcoord), xcoord[-2::-1])
            ycoord = np.insert(ycoord, len(ycoord), -ycoord[1:])
            
            pS.append(p[xcoord, ycoord])
        else:
            print(f"Error: {r=} is out of boundary domain")
    
    
    p = p[xpos[:], ypos]
    return theta, p
        
def solve_parallel(
    Hsy:any, 
    Hsy_np:any, 
    y:np.ndarray, 
    y_squared:np.ndarray,
    tk:float, 
    xi:float,
    epsilon:float,
    alpha:float,
    symbols:tuple,
    printInterval:float 
    )-> tuple:
    
        xSy, ySy, tSy = symbols
        H = np.zeros(len(y))
        f = np.zeros(len(y))
        xi_squared = xi**2      # cache
        if xi == 0:
            zero_pos = list(y).index(0)
            H[:zero_pos] = Hsy_np(xi,   y[:zero_pos  ], tk)
            H[zero_pos+1:] = Hsy_np(xi, y[zero_pos+1:], tk)
            H[zero_pos] = Hsy.xreplace(
                {
                    xSy: xi,
                    ySy: y[zero_pos],
                    tSy: tk,
                }
            ).evalf()
        else:
            H= Hsy_np(xi, y, tk)
            
        # Gaussian distribution of amplitude
        f = epsilon * np.exp(-alpha * (xi_squared + y_squared))
        if xi%printInterval == 0:
            print(f' - X = {xi} - Complete')
        return f, H