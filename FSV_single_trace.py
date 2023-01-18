# Script to measure FSV single trace
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
import os
import sys

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
from RS_FSV import RS_FSV
from VNA_RS import VNA

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

try:
   pump_source=SGS100A('pump_source','TCPIP0::192.168.10.56::inst0::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','TCPIP0::192.168.10.56::inst0::INSTR')

try:
    FSV = RS_FSV('rs_fsv', 'TCPIP0::192.168.10.66::inst0::INSTR')

except KeyError as er:
    RS_FSV.close_all() #Disconnect and irreversibly tear down the instrument
    FSV =  RS_FSV('rs_fsv', 'TCPIP0::192.168.10.66::inst0::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_single_trace(exp,station):

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(FSV.freq_axis)
    meas.register_parameter(FSV.spectrum,setpoints=[FSV.freq_axis])
    meas.register_custom_parameter(name='spectrum_mw_off',paramtype='array',setpoints=[FSV.freq_axis])

    with meas.run() as datasaver:

        MW_source.status('off')

        get_s_off = FSV.spectrum.get()

        MW_source.status('on')

        get_c = FSV.freq_axis()
        get_s = FSV.spectrum.get()

        sleep(0.01)

        datasaver.add_result((FSV.freq_axis, get_c),
                            (FSV.spectrum,get_s),
                            ("spectrum_mw_off",get_s_off))

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
station.add_component(FSV)
station.add_component(pump_source)
station.add_component(I_source)
# station.add_component(I_twpa)
station.add_component(MW_source)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='FSV_single_trace'
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

current = 0.24 #mA
# current = 0.
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 4.63
pump_power   = 0.43
pump_status  = 'off'
# twpa_current = 2.7474747 #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status}

print('\nMeasurement with TWPA {}'.format(pump_status))

###############################################################################
#                                MW SOURCE
###############################################################################

src_frequency  =  3.                 #GHz
src_power      = 0.                   #dBm
src_status     = 'on'

# Snapshot parameters
parameter_snap['MW_source'] = {'freq':src_frequency,'power':src_power,'status':src_status}

################################################################################
#
#             Spectral Analyser parameters
#
################################################################################

FSV_rbw         = 40.e3            #Hz
FSV_ref         = -40              #dB
FSV_avg         = 0               #dB
FSV_att         = 0               #dB
FSV_center      = 3               #GHz
FSV_span        = 1e6              #s
# FSV_npt         = int(FSV_span/FSV_rbw) + 1
FSV_npt         =  1001
sweep_time_min  = FSV_npt / FSV_rbw
# FSV_vbw         = 10e6
FSV_time_sweep  = 1
FSV_time_sweep  = max(sweep_time_min,FSV_time_sweep)
# Snapshot parameters
parameter_snap['FSV']={'center_freq':FSV_center,'average':FSV_avg,
                      'resolution_bandwidth':FSV_rbw,
                      'Npoints':FSV_npt,'ref':FSV_ref,'att':FSV_att,'sweep_time':FSV_time_sweep}
if FSV_time_sweep < sweep_time_min :
    raise ValueError("sweeptime to small with respect to the sweep points and rbw")

print('\ntime for one trace : {} '
      .format(datetime.timedelta(seconds=2*FSV_time_sweep)))


###############################################################################
#                                  COIL
###############################################################################

if I_source.output()=='on':
    I_source.output('off')

I_source.source_mode('CURR')
I_source.range(10e-3)

I_source.current(current*1.e-3)

I_source.output('on')

###############################################################################
#                                  COIL TWPA
###############################################################################

# I_twpa.current(twpa_current*1.e-3)

################################################################################
#
#               Initialization SPECTRAL ANALYZER
#
################################################################################

FSV.res_BW(FSV_rbw)
FSV.center_freq(FSV_center*1.e9)
FSV.averages(FSV_avg)
FSV.n_points(FSV_npt)
FSV.span(FSV_span)
FSV.ref_level(FSV_ref)
FSV.input_att(FSV_att)
FSV.write('SWE:TYPE AUTO')
FSV.detector('rms')
FSV.sweep_time(FSV_time_sweep)

###############################################################################
#                                VNA OFF
################################################################################
# VNA.rf_off()
# VNA.cont_meas_off()

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
exp_name = 'FSV_single_trace'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_single_trace(exp=exp, station=station)

# Shutdown devices
# VNA.rf_off()
# VNA.cont_meas_off()
MW_source.status('off')
pump_source.status('off')
I_source.output('off')
