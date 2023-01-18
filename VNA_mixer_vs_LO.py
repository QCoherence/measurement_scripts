# Script to measure VNA trace
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
    LO_source=SMB100A('LO','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
    SMB100A.close_all()
    LO_source=SMB100A('LO','TCPIP0::192.168.10.6::inst0::INSTR')

try:
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

##############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################
def measure_VNA_vs_SMB_freq(freq_vec,exp,station,current_point=0):

    VNA.rf_on()

    LO_source.status('on')

    I_source.reset()
    I_source.current(current_point*1.e-3)

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(LO_source.frequency)
    meas.register_parameter(VNA.channels.S21.trace_mag_phase, setpoints=[LO_source.frequency])

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for freq in tqdm(freq_vec):

            LO_source.frequency(freq*1.e9)

            get_f = LO_source.frequency.get()
            datasaver.add_result((LO_source.frequency,get_f))
            get_v = VNA.channels.S21.trace_mag_phase.get()
            datasaver.add_result((VNA.channels.S21.trace_mag_phase, get_v),(LO_source.frequency,get_f))

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
station.add_component(LO_source)
station.add_component(pump_source)
station.add_component(I_twpa)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='VNA_mixer_vs_LO'
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

qc.initialise_or_create_database_at(data_dir+'\\'+database_name)
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
current = -0.718 #mA
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             VNA PARAMETERS
###############################################################################

start_freq = 8.75
end_freq   = 9.05
step_freq    = 500 *1.e-6
VNA_power    = -20.
IF_bandwidth =  1.
Averages     = 1
points_VNA   = int(abs(end_freq - start_freq)/step_freq)+1
# points_VNA = 801
trace_time=points_VNA / IF_bandwidth * Averages

print('\ntime for one trace : {} s'.format(datetime.timedelta(seconds = trace_time)))

# Snapshot parameters
parameter_snap['vna'] = {'start_freq':start_freq, 'end_freq':end_freq,
                         'VNA_power':VNA_power, 'IF_bandwidth':IF_bandwidth,
                         'Averages':Averages, 'points':points_VNA}

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 5.42
pump_power   = 2.
pump_status  = 'on'
twpa_current = 2.7474747 #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}
###############################################################################
#                                LO SOURCE
###############################################################################

src_power     = 15 #dBm
freq_start    = 5.5
freq_stop     = 6.25
# freq_step        =  5.
# freq_point       = int(abs(freq_stop - freq_start)/freq_step)+1
freq_point = 101

src_freq_vec = np.linspace(freq_start, freq_stop, freq_point)

src_status     = 'on'

# Snapshot parameters
parameter_snap['LO_source'] = {'power':src_power, 'freq_start' : freq_start,
                               'freq_stop':freq_stop,'points':freq_point}

print('\ntotal time : {}'.format(datetime.timedelta(seconds = freq_point*trace_time)))
###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

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

I_source.current(current*1.e-3)

###############################################################################
#                                  COIL TWPA
###############################################################################

I_twpa.current(twpa_current*1.e-3)

###############################################################################
#                                  TWPA
###############################################################################

pump_source.frequency(pump_freq*1.e9)
pump_source.power(pump_power)
pump_source.status(pump_status)

###############################################################################
#                                  SMB
###############################################################################
LO_source.frequency(src_freq_vec[0]*1.e9)
LO_source.power(src_power)
LO_source.status(src_status)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_mixer_vs_LO'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_VNA_vs_SMB_freq(freq_vec=src_freq_vec,exp=exp, station=station,current_point=current)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
LO_source.status('off')
pump_source.status('off')
I_source.reset()
I_twpa.reset()
