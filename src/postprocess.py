from numpy import linspace,array
from scipy.integrate import trapz
from scipy.interpolate import interp1d

def rmsSpacial(pxa:tuple, psim:array, xsim:tuple = (-100,100)) -> float:
    
    xa,pa = pxa
    psimf  = interp1d(linspace(xsim[0], xsim[1], len(psim)), psim, kind='cubic')(xa)

    num = trapz((psimf - pa)**2, xa)
    den = trapz(pa**2,xa)
    rms = num/den

    return rms