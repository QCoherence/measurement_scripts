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

def measure(ts_vec,exp,station,current_point=0):

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(FSQ.sweep_time_direct)
    meas.register_parameter(FSQ.channel_power,setpoints=[FSQ.sweep_time_direct])

    with meas.run() as datasaver:

        for idx, ts in enumerate(ts_vec):

            FSQ.sweep_time_direct(ts)

            get_t = float(FSQ.sweep_time_direct.get())
            get_p = FSQ.channel_power.get()

            sleep(0.01)

            datasaver.add_result((FSQ.sweep_time_direct, get_t),
                                (FSQ.channel_power,get_p))

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
station.add_component(FSQ)
station.add_component(pump_source)
# station.add_component(I_source)
station.add_component(I_twpa)
station.add_component(MW_source)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='FSQ_channel_power_vs_SWEEP_TIME'
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

current = 0.0                       #mA

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
src_power      = -36                 #dBm
src_status     = 'off'

# Snapshot parameters
parameter_snap['MW_source'] = {'freq':src_frequency,'power':src_power,'status':src_status}

################################################################################
#
#             Spectral Analyser parameters
#
################################################################################

FSQ_span   = 100*1.e-6    #GHz
FSQ_rbw    = FSQ_span * 0.01  #GHz
FSQ_vbw    = FSQ_rbw*3       #Hz
FSQ_ref    = 0  #dB
FSQ_att    = 0      #dB
FSQ_avg    = 0
FSQ_npt    = 1001
FSQ_center = 3.         #GHz

FSQ_ratio  = np.logspace(0, 4 , 50)
# FSQ_ratio          = np.ones(20)
FSQ_time_sweep_vec = 1./(300*1.e3) * FSQ_npt * FSQ_ratio

# Snapshot parameters
parameter_snap['FSQ']={'CW_freq':FSQ_center,'average':FSQ_avg,
                      'video_bandwidth':FSQ_vbw,
                      'resolution_bandwidth':FSQ_rbw,
                      'Npoints':FSQ_npt,'ref':FSQ_ref,'att':FSQ_att}

print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=sum(FSQ_time_sweep_vec))))

###############################################################################
#                                  COIL TWPA
###############################################################################

I_twpa.current(twpa_current*1.e-3)

################################################################################
#
#               Initialization SPECTRAL ANALYZER
#
################################################################################

FSQ.res_BW(FSQ_rbw*1.e9)
FSQ.video_BW(FSQ_vbw*1.e9)
FSQ.center_freq(FSQ_center*1.e9)
FSQ.span(FSQ_span*1.e9)
FSQ.averages(FSQ_avg)
FSQ.main_channel_bandwidth(FSQ_span*1.e9)
FSQ.ref_level(FSQ_ref)
FSQ.input_att(FSQ_att)

FSQ.detector('rms')
FSQ.no_adjacent_channels(0)
FSQ.channel_power_mode('ABS')
FSQ.channel_power_type('CPOW')
FSQ.sweep_time_direct(FSQ_time_sweep_vec[0])

###############################################################################
#                                VNA OFF
###############################################################################
VNA.rf_off()
VNA.cont_meas_off()

###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.status(src_status)
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
exp_name = 'FSQ_channel_power_vs_SWEEP_TIME'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure(ts_vec=FSQ_time_sweep_vec,exp=exp, station=station,current_point=current)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
pump_source.status('off')
I_twpa.reset()
