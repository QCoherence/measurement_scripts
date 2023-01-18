# Script to measure FSQ single trace
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
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

try:
    VNA = VNA('ZNB20', 'TCPIP0::192.168.10.2::inst0::INSTR',
               init_s_params=False,terminator='\n')

except KeyError as er:
    ZNB.close_all() #Disconnect and irreversibly tear down the instrument
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
   MW_source=SMB100A('mw_source','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
   SMB100A.close_all()
   MW_source=SMB100A('mw_source','TCPIP0::192.168.10.6::inst0::INSTR')

try:
    FSQ = RS_FSQ('rs_fsq', 'TCPIP0::192.168.10.61::inst0::INSTR')

except KeyError as er:
    RS_FSQ.close_all() #Disconnect and irreversibly tear down the instrument
    FSQ =  RS_FSQ('rs_fsq', 'TCPIP0::192.168.10.61::inst0::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_single_trace(exp,station,current_point=0):

    MW_source.status('on')
    I_source.reset()
    I_source.current(current_point*1.e-3)

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(FSQ.freq_axis)
    meas.register_parameter(FSQ.spectrum,setpoints=[FSQ.freq_axis])

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        datasaver.add_result((FSQ.freq_axis, FSQ.freq_axis()),(FSQ.spectrum,FSQ.spectrum()))

###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################
start_all_logging()

# Create a station
station = qc.Station()
station.add_component(FSQ)
station.add_component(pump_source)
station.add_component(I_source)
station.add_component(I_twpa)
station.add_component(MW_source)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='FSQ_CW_single_trace'
database_name = date+"_"+user+"_"+description

#############################################################################
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

current = -9.586                       #mA

# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 5.209                #GHz
pump_power   = -0.28                #dBm
pump_status  = 'off'
twpa_current = 2.7474747            #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}

print('\nMeasurement with TWPA {}'.format(pump_status))

###############################################################################
#                                MW SOURCE
###############################################################################

src_frequency  =  3.                 #GHz
src_power      = -36                #dBm

# Snapshot parameters
parameter_snap['MW_source'] = {'freq':src_frequency,'power':src_power}

################################################################################
#
#             Spectral Analyser parameters
#
################################################################################

FSQ_rbw    = 100*1.e3
FSQ_vbw    = 300 #Hz
FSQ_ref    = 0   #dB
FSQ_avg    = 1
FSQ_npt    = 2001
FSQ_center = 3.  #GHz
FSQ_span   = 0 #0 span mode

FSQ_time_sweep = 1./(FSQ_vbw) * FSQ_npt

# Snapshot parameters
parameter_snap['FSQ']={'CW_freq':FSQ_center,'average':FSQ_avg,
                      'video_bandwidth':FSQ_vbw,
                      'resolution_bandwidth':FSQ_rbw,
                      'Npoints':FSQ_npt,'ref':FSQ_ref}



################################################################################
#
#               Initialization SPECTRAL ANALYZER
#
################################################################################

FSQ.res_BW(FSQ_rbw)
FSQ.video_BW(FSQ_vbw)
FSQ.center_freq(FSQ_center*1.e9)
FSQ.averages(FSQ_avg)
FSQ.n_points(FSQ_npt)
FSQ.span(FSQ_span)
FSQ.ref_level(FSQ_ref)
FSQ.sweep_time_auto('ON')

FSQ_time_sweep = FSQ.sweep_time_direct()

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=FSQ_time_sweep)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=FSQ_avg*FSQ_time_sweep)))

FSQ.average_type('rms')


###############################################################################
#                                VNA OFF
###############################################################################
VNA.rf_off()
VNA.cont_meas_off()

###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.status('off')
MW_source.frequency(src_frequency*1e9)
MW_source.power(src_power)

###############################################################################
#                                TWPA PUMP SOURCE
###############################################################################

pump_source.frequency(pump_freq*1.e9)
pump_source.power(pump_power)
pump_source.status(pump_status)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'FSQ_CW_single_trace'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_single_trace(exp=exp, station=station,current_point=current)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
pump_source.status('off')
I_source.reset()
I_twpa.reset()
