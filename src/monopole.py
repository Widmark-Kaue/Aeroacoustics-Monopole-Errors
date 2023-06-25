import numpy as np
import json as js
import sympy as sy

from scipy.signal import fftconvolve


def monopoleFlow (
    t:      list(float) = 2,
    xlim:   tuple = (-200, 200),
    ylim:   tuple = (-200, 200),
    nxy:    tuple = (401, 401),
    alpha:  float = np.log(2) / 9,
    freq:   float = 10,
    M:      float = 0.5,
    gamma:  float = 1.4,
    PTR:    tuple = (101325, 298.15, 8314.46261815324 / 28.9),
):
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
    xSy, ySy, tSy, etaSy =  sy.symbols('xSy ySy tSy etaSy', real=True)
    
    GSy  = sy.I/(4*c0**2 *sy.sqrt(1 - M**2)) 
    GSy *= sy.hankel1(0, omega*sy.sqrt(xSy**2 + (1-M**2)*ySy**2)/(c0*(1-M**2))) 
    GSy *= sy.exp(etaSy)
    
    hankel01Sy = sy.hankel1(0, omega* sy.sqrt(xSy**2 + (1 - M**2)*ySy**2)/(c0*(1-M**2)))
    hankel11Sy = sy.hankel1(1, omega*sy.sqrt(xSy**2+(1 - M**2)*ySy**2)/(c0*(1-M**2)))


    