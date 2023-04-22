from numpy import linspace, sqrt, array
from scipy.integrate import trapz
from scipy.interpolate import interp1d

def rmsSpacial(pxa:tuple, psim:array, xsim:tuple = (-100,100), windows:int = 1) -> tuple:
    
    xa, pa = pxa
    psimf  = interp1d(linspace(xsim[0], xsim[1], len(psim)), psim, kind='cubic')(xa)

    rms = []
    window = (xa[-1] - xa[0])/windows
    pos = 0
    for i in range(windows):
        begin = pos
        pos   = xa.searchsorted(xa[0] + (i+1)*window)
        end   = pos 
        num   = trapz((psimf[begin:end] - pa[begin:end])**2, xa[begin:end])
        den   = trapz(pa[begin:end]**2,xa[begin:end])
        rms.append(num/den)

    return tuple(rms)

def phaseAmplitude(pta:tuple, psim:array, tsim:tuple)-> tuple:

    t1, t2 = tsim
    ta, pa = pta

    '''
    1º passo: identificar onde dentro da solução análitica e numérica começa o regime estacionário
    2º passo: definir esse ponto como uso para o cálculo prms
    3º passo: calcular prms para solução análitica e numérica
    4º passo: calcular erro de amplitude
    5º passo: 
    '''
