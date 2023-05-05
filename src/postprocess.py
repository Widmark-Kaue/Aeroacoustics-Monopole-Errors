from scipy.integrate import trapz
from numpy import linspace, sqrt, array, abs
from scipy.interpolate import interp1d


def rmsSpacial(
    pxa: tuple, 
    psim: array, 
    xsim: tuple = (-100, 100), 
    windows: int = 1
) -> tuple:

    xa, pa = pxa
    psimf = interp1d(linspace(xsim[0], xsim[1], len(psim)), psim, kind='cubic')
    psimf = psimf(xa)

    rms = []
    window = (xa[-1] - xa[0]) / windows
    pos = 0
    for i in range(windows):
        begin = pos
        pos = xa.searchsorted(xa[0] + (i + 1) * window)
        end = pos
        num = trapz((psimf[begin:end] - pa[begin:end]) ** 2, xa[begin:end])
        den = trapz(pa[begin:end] ** 2, xa[begin:end])
        rms.append(num / den)

    return tuple(rms)


def phaseAmplitude(
    pta: tuple, 
    sim: array,
    ttran : float,
) -> tuple:

    ta, pa = pta
    ts, ps = sim
    
    assert len(ta) ==  len(ts), "Vetores de tempo precisam ter o mesmo tamanho"
    
    na = ta.searchsorted(ttran)
    ns = ts.searhsorted(ttran)
    
    parms2 = 1/(ta[-1] - ttran) * trapz(pa[na:]**2, ta[na:])
    psrms2 = 1/(ts[-1] - ttran) * trapz(ps[ns:]**2, ts[ns:])
    
    Aerror = abs(psrms2 - parms2)/parms2
    
    return Aerror
    

    """
    1º passo: identificar onde dentro da solução análitica e numérica começa o regime estacionário
    2º passo: definir esse ponto como uso para o cálculo prms
    3º passo: calcular prms para solução análitica e numérica
    4º passo: calcular erro de amplitude
    5º passo: 
    """
