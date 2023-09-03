"""
Baseado no código do prof. Juan
"""
import numpy as np
import sympy as sy

from json import dump
from scipy.signal import fftconvolve
from src.path import PATH_DATA, Path


def monopoleFlowSy (
    t:          float or list = 2,
    xlim:       tuple = (-200, 200),
    ylim:       tuple = (-200, 200),
    nxy:        tuple = (401, 401),
    alpha:      float = np.log(2) / 9,
    freq:       float = 10,
    M:          float = 0.5,
    gamma:      float = 1.4,
    PTR:        tuple = (101325, 298.15, 8314.46261815324 / 28.9),
    save_path:  Path  = PATH_DATA,
    outName:    str(None)  = None
)->None:
    assert 0 <= M <= 1, 'mach number must be between 0 and 1'
    
    
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
    
    # hankel01Sy = sy.hankel1(0, ksiSy)
    # hankel11Sy = sy.hankel1(1, ksiSy)
    
    # dGdxSy     = omega / (4*c0**3 *(1 - M**2)**(3/2))
    # dGdxSy    *= (M * hankel01Sy - sy.I * xSy *hankel11Sy/sy.sqrt(xSy**2 + (1 - M**2)*ySy**2))
    # dGdxSy    *= sy.exp(etaSy)
    
    # dGdtSy     = GSy *(-sy.I*omega)
    
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
        'ny'        : ny
    }
    
    try:
        t = list(t)
    except:
        t = [t]
    for tk in t:
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
            if xi%10 == 0:
                print(f' - X = {xi} - Complete')
        pFlow = fftconvolve(f, H, 'same')*deltax*deltay
        DATA.update({f'{tk}': pFlow.tolist()})
    
    if outName == None:
        outName = f'monopole_M{M}.json'
    
    save_path.mkdir(exist_ok=True, parents=True)
    with open(save_path.joinpath(outName), 'w') as file:
        dump(DATA, file)

    

    