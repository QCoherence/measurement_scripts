# Script to measure 2T
#                            -- Dorian

from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
from qcodes.loops import Loop
from time import sleep
from tqdm import tqdm

import matplotlib.pyplot as plt
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
from qcodes.instrument_drivers.yokogawa.GS200 import GS200

from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A
from HP3245A import HP3245A
from RS_FSQ import RS_FSQ
from VNA_RS import VNA

try:
    VNA = VNA('ZNB20', 'TCPIP0::192.168.10.2::inst0::INSTR',
               init_s_params=False,terminator='\n')

except KeyError as er:
    VNA.close_all() #Disconnect and irreversibly tear down the instrument
    VNA = VNA('ZNB20', 'TCPIP0::192.168.10.2::inst0::INSTR',
               init_s_params=False,terminator='\n')
try:
    I_source = GS200("gs200", address='TCPIP::192.168.10.3::INSTR', terminator="\n")

except KeyError as er:
    GS200.close_all() #Disconnect and irreversibly tear down the instrument
    I_source = GS200("gs200", address='TCPIP::192.168.10.3::INSTR', terminator="\n")

try:
    MW_source=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
    SMB100A.close_all()
    MW_source=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_2T(exp,station,current_point):

    VNA.channels.S21.initialize_two_tone_spectroscopy()

    VNA.channels.S21.cw_frequency(cwfrequency)
    VNA.rf_on()

    MW_source.status('on')
    MW_source.restartsweep()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.freq_vec)
    meas.register_parameter(VNA.channels.S21.point_fixed_frequency_mag_phase_trace)

    with meas.run() as datasaver:

        MW_source.start_sweep()

        for freq in freqs:
            sleep(dwelltime*1.e-3)

        get_f=MW_source.freq_vec.get()
        get_v = VNA.channels.S21.point_fixed_frequency_mag_phase_trace.get(initiate=False)

        datasaver.add_result((VNA.channels.S21.point_fixed_frequency_mag_phase_trace, get_v),
                             (MW_source.freq_vec, get_f))

    id=datasaver.dataset.run_id
    qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                         json.dumps(parameter_snap))

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
station.add_component(MW_source)
# station.add_component(pump_source)
# station.add_component(I_twpa)

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='2T_VNA_vs_SMB'
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

# current = -0.72926 #mA
current = -14.568
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             VNA PARAMETERS
###############################################################################

cwfrequency        = 8.4722*1.e9
averages           = 1
sweeps             = averages
detector_power     = -10         #dBm
detector_bandwidth =  30         #Hz

# Snapshot parameters
parameter_snap['vna'] = {'cw_freq':cwfrequency, 'power':detector_power,
                         'IF_bandwidth':detector_bandwidth, 'Averages':averages}

###############################################################################
#                        SPECTROSCOPY TONE PARAMETERS
###############################################################################
f_min    = 1.9*1.e9                          #Hz
f_max    = 3.2*1.e9                          #Hz
f_step = 1.*1.e6
# N_points = 501
N_points   = int((f_max - f_min)/f_step)
freqs    = np.linspace(f_min,f_max+f_step,N_points)  #Hz

# Dwell time security time [ms]: to ensure the SMA is not sweeping too fast
# compared to the VNA capabilities

DTsecurity=100
# Dwell time of the frequency sweep [ms]
dwelltime=1./detector_bandwidth*1000+DTsecurity

power=-10.

parameter_snap['mw_source'] = {'start_freq':f_min, 'stop_freq':f_max,
                               'step_freq':f_step, 'N_points':N_points,
                               'power':power}

trace_time   = N_points*(1*dwelltime*1.e-3)*averages

print('time for one trace : {} s'.format(datetime.timedelta(seconds = trace_time)))


###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 5.209
pump_power   = -0.28
pump_status  = 'off'
twpa_current = 2.7474747 #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}

###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###############################################################################
#                                  COIL
###############################################################################

if I_source.output()=='on':
    I_source.output('off')

I_source.source_mode('CURR')
I_source.range(100e-3)

I_source.current(current*1.e-3)

I_source.output('on')

###############################################################################
#                                  COIL TWPA
###############################################################################

# I_twpa.current(twpa_current*1.e-3)
###############################################################################
#                                  VNA
###############################################################################

VNA.add_channel('S21',vna_parameter='S21')
VNA.channels.S21.format('dB')

VNA.channels.S21.avg(averages)
VNA.channels.S21.power(detector_power)
VNA.channels.S21.bandwidth(detector_bandwidth)
VNA.channels.S21.npts(N_points)

###############################################################################
#                                 MW SOURCE
###############################################################################

MW_source.power(power)
MW_source.sourcemode('sweep')
MW_source.dwell_time(dwelltime*1.e-3)
MW_source.sweepmode('single')
MW_source.spacing_freq('LIN')
MW_source.freq_start(f_min-f_step) # Hack to take into account that the first
                                   # frequency point of MW_source doesn't send
                                   # a trigger to the VNA
MW_source.freq_stop(f_max)
MW_source.freq_step(f_step)
MW_source.freq_points(N_points+1)
MW_source.set_gui_update('on')

###############################################################################
#                                TWPA PUMP SOURCE
###############################################################################

# pump_source.frequency(pump_freq*1.e9)
# pump_source.power(pump_power)
# pump_source.status(pump_status)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = '2T_VNA_vs_SMB_freq'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_2T(exp=exp, station=station,current_point=current)

VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
# pump_source.status('off')
I_source.reset()
# I_twpa.reset()
