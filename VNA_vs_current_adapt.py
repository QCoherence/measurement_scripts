from qcodes.logger.logger import start_all_logging
from utilities import *
from time import sleep
from glob import glob

import matplotlib.pyplot as plt
import scipy.optimize as sci
import qcodes as qc
import numpy as np
import datetime
import time
import json
import sys
import os

###############################################################################
#
#                        IMPORTING THE INSTRUMENTS
#
###############################################################################

sys.path.append('C:\QCodes_Driver_And_Scripts\Drivers')

from VNA_RS import VNA
from HP3245A import HP3245A
from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A

try:
    VNA = VNA('ZNB20', 'TCPIP0::192.168.10.2::inst0::INSTR',
               init_s_params=False,terminator='\n')

except KeyError as er:
    VNA.close_all() #Disconnect and irreversibly tear down the instrument
    VNA = VNA('ZNB20', 'TCPIP0::192.168.10.2::inst0::INSTR',
               init_s_params=False,terminator='\n')

try:
    I_source = HP3245A('current_source', 'GPIB::24')

except KeyError as er:
    HP3245A.close_all() #Disconnect and irreversibly tear down the instrument
    I_source = HP3245A('current_source', 'GPIB::24')

try:
    I_twpa = HP3245A('current_source_twpa', 'GPIB::17')

except KeyError as er:
    HP3245A.close_all() #Disconnect and irreversibly tear down the instrument
    I_twpa = HP3245A('current_source_twpa', 'GPIB::17')

try:
    MW_pump=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
    SMB100A.close_all()
    MW_pump=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')

##############################################################################
#
#                         FIT
#
###############################################################################
def model(freq, Qi, Qe,fr,Xe,Phixe):

        df = (freq - fr)
        dw=2*np.pi*df

        kappa=fr / Qe
        gamma=fr / Qi

        S11 = (kappa-gamma + 2*1j*dw) /(kappa + gamma -2*1j*dw)
        y   = (S11 + Xe*np.exp(1j*Phixe))

        y_db =  20 * np.log10(np.abs(y))

        y_ph = np.unwrap(-np.angle(y))
        y_ph = wrap(y_ph - np.pi)

        return np.concatenate((y_db, y_ph))

def fit(w,data,function,ini):

    b_inf = [0, 0, ini[2]*0.9, -100,0]
    b_sup = [1e8, 1e8, ini[2]*1.1,100,2*np.pi]

    # print b_inf, b_sup

    popt,pcov = sci.curve_fit(model,w,data,p0=ini,maxfev = 50000,
                bounds=(b_inf, b_sup), xtol= 1e-15, gtol= 1e-15, ftol= 1e-15)

    p_err = np.sqrt(np.diag(pcov))

    return popt,p_err

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_vs_current(current_vec, init, exp, station):

    fname   = glob('reference_CD9_noTWPA.dat')
    dataRef = np.loadtxt(fname[0],delimiter = ',')

    _freqRef  = dataRef[:,0]
    _magRef   = dataRef[:,1]
    _phaseRef = dataRef[:,2]

    VNA.rf_on()
    I_source.reset()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(I_source.current)
    meas.register_parameter(VNA.channels.S21.trace_mag_phase,
                            setpoints=[I_source.current])

    meas.write_period = 10

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for idx,current in enumerate(current_vec):

            I_source.current(current)

            get_i = I_source.current.get()

            f_start = (init[2]-0.5*span)*1.e9
            f_stop  = (init[2]+0.5*span)*1.e9

            VNA.channels.start(f_start)
            VNA.channels.stop(f_stop)

            get_v = VNA.channels.S21.trace_mag_phase.get()

            mag   = 20*np.log10(get_v[0])
            phase = get_v[1]
            freq  = np.array(VNA.channels.S21.trace_mag_phase.setpoints[0][0])*1.e-9

            normFreq = np.array([np.abs(_freqRef - _f) for _f in freq])
            idxRef   = np.argmin(normFreq,axis=1)
            magRef   = _magRef[idxRef]

            phaseRef = _phaseRef[idxRef]
            phaseRef = np.unwrap(phaseRef)

            mag_slice = mag - magRef

            phase_slice = phase - phaseRef
            phase_slice = wrap(phase_slice)

            data_slice  = np.concatenate((mag_slice,phase_slice))

            if idx == 0 :

                Qi_0    = 500
                Qe_0    = 2543
                Xe_0    = 0
                PhiXe_0 = 0
                fr_0    =  freq[np.argmin(mag_slice)]

                init    = [Qi_0,Qe_0,fr_0,Xe_0,PhiXe_0]

            try :
                [Qi,Qe,fr,Xe,PhiXe],[Qi_err,Qe_err,fr_err,Xe_err,PhiXe_err]  = fit(freq,data_slice,model,init)
                print([Qi,Qe,fr,Xe,PhiXe])

            except :
                print('No fit')

                if idx == 0 :

                    [Qi,Qe,fr,Xe,PhiXe] = init

            init = [Qi,Qe,fr,Xe,PhiXe]

            f_fit = np.linspace(freq[0],freq[-1],1000)
            y_model = model(f_fit, Qi, Qe, fr, Xe, PhiXe)
            plt.plot(freq, mag_slice, '.', markersize=10)
            plt.plot(f_fit, y_model[:int(len(f_fit))], color='black')
            plt.show()

            datasaver.add_result((VNA.channels.S21.trace_mag_phase, get_v),(I_source.current,get_i))

###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################

start_all_logging()

# Create a station
station = qc.Station()
station.add_component(VNA)
station.add_component(I_source)
station.add_component(I_twpa)

station.snapshot()
station.components

# Experiment details
date=datetime.datetime.today().strftime('%Y_%m_%d')
user='DF'
description='VNA_vs_current'
database_name = date+"_"+user+"_"+description

###############################################################################
#                           DATA FOLDER CREATION
###############################################################################

script_dir=os.path.dirname(__file__)
data_dir=os.path.join('C:\\QCodes_Driver_And_Scripts\\Data_QCodes\\Dorian\\'+date)

try :
    os.mkdir(data_dir)
except FileExistsError:
    pass

data_dir=data_dir +'\\'+description

try :
    os.mkdir(data_dir)
except FileExistsError:
    pass

###############################################################################
#                       CREATE OR INITIALIZE DATABASE
################################################################################

qc.initialise_or_create_database_at(data_dir+'\\'+database_name+'.db')
qc.config.core.db_location

parameter_snap={}

###############################################################################
#
#                          INSTRUMENTS PARAMETERS
#
###############################################################################

###############################################################################
#                             COIL PARAMETERS
###############################################################################

I_start  =  -1.688
I_end    =  0.0814
# I_end    =  -1.2

points_I =  201
I_vec    = np.linspace(I_start, I_end, points_I)*1.e-3

points_I = len(I_vec)
# Snapshot parameters
parameter_snap['flux']={'I_start':I_start,'I_end':I_end,'I_points':len(I_vec)}

###############################################################################
#                             VNA PARAMETERS
###############################################################################
center_freq  = 3.96
span         = 0.4
step_freq    = 250*1.e-6
# start_freq   = 7.5
# end_freq     = 11.
start_freq   = center_freq - 0.5*span
end_freq     = center_freq + 0.5*span
VNA_power    = -20
IF_bandwidth = 100
Averages     = 1
points_VNA   = int(abs(end_freq - start_freq)/step_freq)+1
# points_VNA   = 2001

fit_init = [189,945,3.960,0,0]

trace_time   = points_VNA / IF_bandwidth

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=trace_time)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=Averages*points_I*trace_time)))

# Snapshot parameters
parameter_snap['vna'] = {'start_freq':start_freq, 'end_freq':end_freq,
                         'VNA_power':VNA_power, 'IF_bandwidth':IF_bandwidth,
                         'Averages':Averages, 'points':points_VNA}

###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 5.209
pump_power   = -0.28
pump_status  = 'off'
twpa_current = 2.75 #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}
###############################################################################
#                                  VNA
###############################################################################

VNA.add_channel('S21',vna_parameter='S21')

VNA.channels.S21.format('dB')
VNA.channels.S21.bandwidth(IF_bandwidth)
VNA.channels.S21.power(VNA_power)
VNA.channels.S21.avg(Averages)
VNA.channels.npts(points_VNA)
VNA.channels.start(start_freq*1e9)
VNA.channels.stop(end_freq*1e9)

###############################################################################
#                                  COIL
###############################################################################

I_source.current(0.)

###############################################################################
#                                  COIL TWPA
###############################################################################

I_twpa.current(twpa_current*1.e-3)

###############################################################################
#                                  TWPA
###############################################################################

MW_pump.frequency(pump_freq*1.e9)
MW_pump.power(pump_power)
MW_pump.status(pump_status)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_vs_current'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_current(I_vec, init=fit_init, exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_pump.status('off')
I_source.reset()
I_twpa.reset()
