# Script to measure VNA trace
#                            -- Dorian
from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
from qcodes.plots.pyqtgraph import QtPlot
from qcodes.loops import Loop
from time import sleep

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

except KeError as er:
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

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_single_trace(freq_lo,exp,station):

    VNA.rf_on()

    LO_source.status(LO_status)
    LO_source.restartsweep()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(LO_source.freq_vec)
    meas.register_parameter(VNA.channels.S21.cw_frequency)
    meas.register_parameter(VNA.channels.S21.point_fixed_frequency_mag_phase_trace,setpoints=[LO_source.freq_vec])

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                            json.dumps(parameter_snap))

        for f in freq_lo:

            LO_source.frequency(f*1.e9)
            VNA.channels.S21.port2_IF_freq(f*1.e9)

            get_v = VNA.channels.S21.point_fixed_frequency_mag_phase_trace.get(initiate=True)

            get_cw = VNA.channels.S21.cw_frequency.get()
            get_f = MW_source.frequency.get()

            datasaver.add_result((VNA.channels.S21.point_fixed_frequency_mag_phase_trace, get_v),
                                (MW_source.freq_vec, get_f),(VNA.channels.S21.cw_frequency, get_cw))

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
description='VNA_single_trace_freq_conv'
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
current = 0.0 #mA
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             VNA PARAMETERS
###############################################################################
cw_freq      =  9.0
VNA_power    = -20
IF_bandwidth =  1.
points_VNA   =  201 #number of points to average
Averages     =  1   #number of trace avergage, let it to one because setting avg with n Points

# Snapshot parameters
parameter_snap['vna'] = {'cw_freq':start_freq, 'VNA_power':VNA_power,
                         'IF_bandwidth':IF_bandwidth,'Averages':Averages,
                         'points':points_VNA}

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
#                                MW SOURCE
###############################################################################

LO_frequency  =  6                       #GHz
LO_power      = 14.                      #dBm
LO_status     = 'on'

# Snapshot parameters
parameter_snap['LO_source'] = {'freq':LO_frequency,'power':LO_power,'status':LO_status}
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

VNA.channels.S21.initialize_frequency_conversion(lmcorr = 'off',conversion_side = 'down')
VNA.channels.S21.port2_IF_freq(LO_frequency)

print('\ntime for one trace : {} s'.format(datetime.timedelta(seconds = trace_time)))

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
LO_source.frequency(LO_frequency*1.e9)
LO_source.power(LO_power)
LO_source.status(LO_status)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_single_trace_freq_conv'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_single_trace(exp=exp, station=station,current_point=current)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
LO_source.status('off')
pump_source.status('off')
I_source.reset()
I_twpa.reset()
