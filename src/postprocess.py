from scipy.integrate import trapz
from numpy import linspace, sqrt, array, abs
from scipy.interpolate import interp1d


def rmsSpacial(
    pxa: tuple, 
    psim: array, 
    xsim: tuple, 
    windows: int = 1
) -> list:

    xa, pa = pxa
    psimf = interp1d(linspace(xsim[0], xsim[1], len(psim)), psim, kind='cubic')
    
    if min(xa) < xsim[0]:
        min_idx = xa.searchsorted(xsim[0])
        xa = xa[min_idx:]
        pa = pa[min_idx:]
        
    if max(xa) > xsim[1]:
        max_idx = xa.searchsorted(xsim[1])+1
        xa = xa[:max_idx]
        pa = pa[:max_idx]
    
    psimf = psimf(xa)

    
    rms = []
    window = (xa[-1] - xa[0]) / windows
    pos = 0
    
    # Windows RMS
    for i in range(windows):
        begin = pos
        pos = xa.searchsorted(xa[0] + (i + 1) * window)
        end = pos
        num = trapz((psimf[begin:end] - pa[begin:end]) ** 2, xa[begin:end])
        den = trapz(pa[begin:end] ** 2, xa[begin:end])
        rms.append(num / den)

    # Total RMS
    num = trapz((psimf - pa)**2, xa)
    den = trapz(pa**2, xa)
    rms.append(num/den)    
    
    return rms

def rmsTime(p:array, t:array) -> float:
    den = t[-1]  - t[0]
    prms = sqrt(trapz(p**2, t)/den)
    
    return prms

def phaseAmplitude( pta: tuple, ptsim: tuple, ttran : float) -> tuple:

    ta, pa = pta
    tsim, psim = ptsim
        
    na = ta.searchsorted(ttran)
    ns = tsim.searhsorted(ttran)
    
    pa_rms = rmsTime(pa[na:], ta[na:])
    psim_rms = rmsTime(psim[ns:], tsim[ns:])
    
    e_am = abs(psim_rms**2 - pa_rms**2)/(pa_rms**2)
    
    
    """
    1º passo: identificar onde dentro da solução análitica e numérica começa o regime estacionário
    2º passo: definir esse ponto como uso para o cálculo prms
    3º passo: calcular prms para solução análitica e numérica
    4º passo: calcular erro de amplitude
    5º passo: 
    """
    
    return 
    
