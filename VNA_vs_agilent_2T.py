# Script to measure 2T
#                            -- Dorian

from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
from qcodes.plots.pyqtgraph import QtPlot
from qcodes.loops import Loop
from time import sleep
from tqdm import tqdm

import matplotlib.pyplot as plt
import qcodes as qc
import numpy as np
import datetime
import visa
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

from Agilent_E8257D import E8257D
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
    MW_source=E8257D('mw_source','TCPIP0::192.168.10.70::inst0::INSTR')

except KeyError as er:
    E8257D.close_all()
    MW_source=E8257D('mw_source','TCPIP0::192.168.10.70::inst0::INSTR')

try:
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_2T(exp,station,current_point):

    VNA.rf_on()

    I_source.reset()
    I_source.current(current_point*1.e-3)

    MW_source.status('ON')

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.freq_vec)
    meas.register_parameter(VNA.channels.S21.point_fixed_frequency_mag_phase_trace)

    with meas.run() as datasaver:

        MW_source.timeout(2*trace_time)
        MW_source.startsweep()
        # print(MW_source.ask('*OPC?'))

        # for freq in freqs:
        #     sleep(dwelltime*1.e-3)

        # opc=0
        # while opc==0:
        #     try :
        #         opc=int(MW_source.ask('*OPC?'))
        #     except visa.VisaIOError as er :
        #         opc=0

        get_f = MW_source.freq_vec()
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
station.add_component(pump_source)
station.add_component(I_twpa)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='2T_VNA_vs_Agilent'
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

current = 0.0 #mA

# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             VNA PARAMETERS
###############################################################################

cwfrequency        = 10.312*1.e9
averages           = 1
sweeps             = averages
detector_power     = -10         #dBm
detector_bandwidth =  100          #Hz

# Snapshot parameters
parameter_snap['vna'] = {'cw_freq':cwfrequency, 'power':detector_power,
                         'IF_bandwidth':detector_bandwidth, 'Averages':averages}

###############################################################################
#                        SPECTROSCOPY TONE PARAMETERS
###############################################################################
f_min    = 20*1.e9                          #Hz
f_max    = 23*1.e9                          #Hz

f_step   = 1699830.0169983*2
# N_points = 10001
N_points   = int((f_max - f_min)/f_step)
freqs    = np.linspace(f_min,f_max+f_step,N_points)  #Hz

# Dwell time security time [ms]: to ensure the SMA is not sweeping too fast
# compared to the VNA capabilities

DTsecurity=100
# Dwell time of the frequency sweep [ms]
dwelltime=1./detector_bandwidth*1000+DTsecurity
# dwelltime = 100
# dwellime =5
power=6.

parameter_snap['mw_source'] = {'start_freq':f_min, 'stop_freq':f_max,
                               'step_freq':f_step, 'N_points':N_points,
                               'power':power}

trace_time   = N_points*(1*dwelltime*1.e-3)
print('time for one trace : {} s'.format(trace_time))

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

I_source.current(current*1.e-3)

###############################################################################
#                                  VNA
###############################################################################


VNA.add_channel('S21',vna_parameter='S21')
VNA.channels.S21.format('dB')

VNA.channels.S21.initialize_two_tone_spectroscopy()

VNA.channels.S21.cw_frequency(cw_freq_vec[0])
VNA.channels.S21.avg(averages)
VNA.channels.S21.power(detector_power)
VNA.channels.S21.bandwidth(detector_bandwidth)
VNA.channels.S21.npts(N_points)

###############################################################################
#                                 MW SOURCE
###############################################################################

MW_source.power(power)
MW_source.dwell_time(dwelltime*1.e-3)
# MW_source.sweepmode('SINGLE')
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

pump_source.frequency(pump_freq*1.e9)
pump_source.power(pump_power)
pump_source.status(pump_status)

###############################################################################
#                                  COIL TWPA
###############################################################################

I_twpa.current(twpa_current*1.e-3)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = '2T_VNA_vs_Agilent_freq'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_2T(exp=exp, station=station,current_point=current)


# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('OFF')
pump_source.status('off')
I_source.reset()
I_twpa.reset()
