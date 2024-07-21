import numpy as np

from pandas import Series
from scipy.integrate import trapz
from scipy.interpolate import interp1d
from scipy.signal import argrelmax, argrelmin


def rmsSpacial(
    pxa: tuple, 
    psim: np.ndarray, 
    xsim: tuple, 
    windows: int = 1
) -> list:

    xa, pa = pxa
    psimf = interp1d(np.linspace(xsim[0], xsim[1], len(psim)), psim, kind='cubic')
    
    if np.min(xa) < xsim[0]:
        min_idx = xa.searchsorted(xsim[0])
        xa = xa[min_idx:]
        pa = pa[min_idx:]
        
    if np.max(xa) > xsim[1]:
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

def rmsTime(p:np.ndarray, t:np.ndarray) -> float:
    den = t[-1]  - t[0]
    prms = np.sqrt(trapz(p**2, t)/den)
    
    return prms

def phaseAmplitude(pta: tuple, ptsim: tuple, freq:float = 10, moving_avg:int = None) -> tuple:

    omega =  freq * 2*np.pi
    ta, pa = pta
    tsim, psim = ptsim
             
    pa_rms = rmsTime(pa, ta)
    psim_rms = rmsTime(psim, tsim)
    
    e_am = np.abs(psim_rms**2 - pa_rms**2)/(pa_rms**2)
    
    idx_peak_a = argrelmax(pa)[0]    
    idx_peak_a = np.concatenate((idx_peak_a ,argrelmin(pa)[0]))    
    
    if moving_avg == None:
        idx_peak_sim = argrelmax(psim)[0]        
        idx_peak_sim = np.concatenate((idx_peak_sim,argrelmin(psim)[0]))        
    else:
        psim_moving_avg = Series(psim, tsim).rolling(moving_avg).mean().to_numpy()[moving_avg-1:]
        tsim            = tsim[moving_avg -1 :]
        
        diff_last = []
        for i in range(1,15):   #increase order of argrelmax and argrelmin
            idx_peak_sim = argrelmax(psim_moving_avg, order=i)[0]        
            idx_peak_sim = np.concatenate((idx_peak_sim,argrelmin(psim_moving_avg, order=i)[0]))
            
            diff = len(idx_peak_a) - len(idx_peak_sim)
            if  diff >= 0 or (i > 3 and all(np.array(diff_last)[-3:]== diff)):
                aux = f'->Order = {i}'
                diffstr = f'->Diff = {diff}'
                print(f'{aux:->20}') 
                print(f'{diffstr:->20}') 
                break
            #elif i == 14:
              #  assert False, f'Error number of peaks analitic - sim = {len(idx_peak_a) - len(idx_peak_sim)}'                       
            
            diff_last.append(diff)
                #     T = 1/freq
                #     number_of_period = (ta[-1] - ta[0])*freq
                #     idx_peak_sim = []
                    
                #     t_initial = ta[0]
                #     for i in range(number_of_period):
                #         # Update tfinal interval
                #         t_final = t_initial + T 
                        
                #         slice_ind = np.where((tsim >= t_initial) & ( tsim <= t_final) )[0]
                #         pslice = psim_moving_avg[slice_ind]
                        
                #         # Two peaks each periods
                #         idx_peak_sim_slice_positive = argrelmax(pslice)[0]
                #         idx_peak_sim_slice_negative = argrelmin(pslice)[0]
                #         idx_peak_sim.append(np.where(pslice[idx_peak_sim_slice_positive] == np.max(pslice[idx_peak_sim_slice_positive]))[0][0]) 
                #         idx_peak_sim.append(np.where(pslice[idx_peak_sim_slice_negative] == np.min(pslice[idx_peak_sim_slice_negative]))[0][0])
                        
                #         #update tinitial interval
                #         t_initial = t_final
                    
                #     idx_peak_sim = np.array(idx_peak_sim)       
             
        if  diff > 0: #Extrapolate peak                
            dt = tsim[idx_peak_sim[-1]] - tsim[idx_peak_sim[-2]]
            for _ in range(len(idx_peak_a)-len(idx_peak_sim)):
                adition_peak = tsim[idx_peak_sim[-1]] + dt
                tsim = np.insert(tsim, len(tsim), adition_peak)
                idx_peak_sim = np.insert(idx_peak_sim, len(idx_peak_sim), len(tsim)-1)
        elif diff < 0:
            idx_peak_sim = idx_peak_sim[:diff]
                

    e_ph = np.rad2deg(omega *np.mean(np.abs(ta[idx_peak_a] - tsim[idx_peak_sim])))
    # e_ph = np.rad2deg(omega *np.abs(ta[idx_peak_a[-1]] - tsim[idx_peak_sim[-1]]))
    
    return e_ph, e_am
    
