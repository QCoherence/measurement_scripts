import sys
import numpy as np
import lmfit
import os

def linfunc(p,x):
    a=p['slop']
    b=p['y_intercept']
    return a*x+b

def linresidual(p,x,y):

    return linfunc(p.valuesdict(),x) - y

def linfit(xData,yData):

    initSlop          = (yData[-1]-yData[0])/(xData[-1]-xData[0])
    initY_intercept   = xData[0]*initSlop
    print(initSlop)
    print(initY_intercept)
    params = lmfit.Parameters()
    params.add_many(('slop',initSlop),
                    ('y_intercept', initY_intercept),)

    result = lmfit.minimize(linresidual, params, args=(xData,yData))
    lmfit.printfuncs.report_fit(result.params)

    return result.params.values()

def mag_to_dB(magData):

    return 20*np.log(magData)

def phase_treatment(phaseData,freqData,sweepParam=None):

    '''
    Unwraps the phase and remove the cable delays by fitting a linear slope.
    If they are several traces for a swept parameters this version fits only the
    first trace. To compare with v2.
    '''

    if sweepParam is None :

        phaseUwrpd=np.unwrap(phaseData.T,axis=0)

        slp,offset=linfit(freqData,phaseUwrpd)

        phaseLin=slp*freqData + offset

        phaseCorr=phaseUnwrpd - phaseLin

    else :

        phaseUwrpd=np.unwrap(phaseData.T,axis=0)

        slp,offset=linfit(freqData,phaseUwrpd[:,0])

        linPhase=np.array([slp*_freq*np.ones(len(sweepParam)) for _freq in freqData]) + offset

        phaseCorr=phaseUnwrpd-linPhase

    return phaseCorr

# def phase_treatment_v2(phaseData,freqData):
#
#     '''
#     Unwraps the phase and remove the cable delays by fitting a linear slope.
#     Fits only the slope for all traces of the swept parameter. To compare with v2.
#     '''
#
#
#     phaseUwrpd=np.unwrap(phaseData.T,axis=0)
#
#     slop   = np.zeros(len(phaseData[:,0]))
#     offset = np.zeros(len(phaseData[:,0]))
#
#     print(len(slop))
#
#     for i,phase in enumerate(phaseUwrpd.T):
#
#         slop[i],offset[i]=linfit(freqData,phase)
#
#     linPhase=np.array([slop*_freq + offset for _freq in freqData])
#
#     phaseCorr=phaseUwrpd-linPhase
#
#     return phaseCorr

def phase_treatment_v2(phaseData,freqData):

    phase_unwrapped=np.unwrap(phaseData.T,axis=0)

    slop   = np.zeros(len(phaseData[:,0]))
    offset = np.zeros(len(phaseData[:,0]))

    for i,phase in enumerate(phase_unwrapped.T):

        slop[i],offset[i]=linfit(freqData,phase)

    lin_phase=np.array([slop*_freq + offset for _freq in freqData])

    phase_corrected=phase_unwrapped-lin_phase

    return phase_corrected

def wrap(phaseData):

    return (phaseData + np.pi) % (2 * np.pi) - np.pi
