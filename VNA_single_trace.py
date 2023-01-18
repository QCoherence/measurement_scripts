# Script to measure VNA trace
#                            -- Dorian
from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
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

from qcodes.instrument_drivers.yokogawa.GS200 import GS200

from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A
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
   pump_source=SGS100A('pump_source','TCPIP0::192.168.10.56::inst0::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','TCPIP0::192.168.10.56::inst0::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_single_trace(exp,station):

    VNA.rf_on()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(VNA.channels.S21.trace_mag_phase)

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        get_v = VNA.channels.S21.trace_mag_phase.get()
        datasaver.add_result((VNA.channels.S21.trace_mag_phase, get_v))

###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################

start_all_logging()

# Create a station
station = qc.Station()
station.add_component(VNA)
# station.add_component(I_source)
# station.add_component(MW_source)
station.add_component(pump_source)
# station.add_component(I_twpa)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='VNA_single_trace'
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
#normalized flux

current = -0.5
# current = -2.525
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             VNA PARAMETERS
###############################################################################
# center_freq  = 3.058
# span_freq    = 0.1
# start_freq   = center_freq - 0.75*span_freq
# end_freq     = center_freq + 0.25*span_freq
start_freq = 2
end_freq  = 11
# step_freq    = 2*1.e-3
VNA_power    = -20
IF_bandwidth =  10
Averages     =  1
# points_VNA   = int(abs(end_freq - start_freq)/step_freq)+1
points_VNA = 2001
trace_time=points_VNA / IF_bandwidth * Averages

print('\ntime for one trace : {} s'.format(datetime.timedelta(seconds = trace_time)))

# Snapshot parameters
parameter_snap['vna'] = {'start_freq':start_freq, 'end_freq':end_freq,
                         'VNA_power':VNA_power, 'IF_bandwidth':IF_bandwidth,
                         'Averages':Averages, 'points':points_VNA}

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 4.998
pump_power   = .5
pump_status  = 'off'
twpa_current = -0.5 #mA
#
# # pump_freq    = 7.014
# # pump_power   = 3.17
# # pump_status  = 'off'
# # twpa_current = 2.7474747 #mA
#
# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}
###############################################################################
#                                MW SOURCE
###############################################################################
#
# src_frequency  =  6.156                #GHz
# src_power      = 0.84                 #dBm
# src_status     = 'off'
#
# # Snapshot parameters
# parameter_snap['MW_source'] = {'freq':src_frequency,'power':src_power,'status':src_status}
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

###############################################################################
#                                  TWPA
###############################################################################
#
pump_source.frequency(pump_freq*1.e9)
pump_source.power(pump_power)
pump_source.status(pump_status)

###############################################################################
#                                  SMB
###############################################################################
# MW_source.frequency(src_frequency*1.e9)
# MW_source.power(src_power)
# MW_source.status(src_status)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_single_trace'

sample_name = 'twpa_rkw0310'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_single_trace(exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
# MW_source.status('off')
pump_source.status('off')
I_source.reset()
# I_twpa.reset()
