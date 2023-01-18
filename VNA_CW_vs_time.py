# Script to measure single frequency transmission vs time
#                            -- Dorian
from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.logger.logger import start_all_logging
from time import sleep

import matplotlib.pyplot as plt
import qcodes as qc
import numpy as np
import datetime
import json
import time
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
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_CW_vs_time(exp,station):

    VNA.rf_on()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(VNA.channels.S21.point_fixed_frequency_mag_phase_trace)

    with meas.run() as datasaver:

        # sleep(N_points*dwelltime*1.e-3)

        get_v=VNA.channels.S21.point_fixed_frequency_mag_phase_trace.get()
        datasaver.add_result((VNA.channels.S21.point_fixed_frequency_mag_phase_trace, get_v))

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
station.add_component(pump_source)
station.add_component(I_source)
station.add_component(I_twpa)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='VNA_CW_vs_time'
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

# current = -0.73 #mA
current = 0.
# Snapshot parameters
parameter_snap['flux']={'current': current}
VNA.add_channel('S21',vna_parameter='S21')

###############################################################################
#                             TWPA PARAMETERS
###############################################################################

pump_freq    = 5.209                #GHz
pump_power   = -0.28                #dBm
pump_status  = 'off'
twpa_current = 2.7474747            #mA
# twpa_current = 0.
# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}

print('\nMeasurement with TWPA {}'.format(pump_status))

###############################################################################
#                             VNA PARAMETERS
###############################################################################

cwfrequency        = 9*1.e9      #Hz
averages           = 1
sweeps             = averages
detector_power     = 0.          #dB
detector_bandwidth = 1           #Hz
duration           = 3600*1.5      #s

N_points           = int(duration * detector_bandwidth) + 1

DTsecurity=100
# Dwell time of the frequency sweep [ms]
dwelltime=1./detector_bandwidth*1000+DTsecurity

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=duration)))
# Snapshot parameters
parameter_snap['vna'] = {'cw_freq':cwfrequency, 'power':detector_power,
                         'IF_bandwidth':detector_bandwidth, 'Averages':averages,'N_points': N_points}

###############################################################################
#                             TIME PARAMETERS
###############################################################################

# Snapshot parameters
parameter_snap['time'] = {'duration':duration, 'N_points': N_points}

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


VNA.channels.S21.sweep_type('CW_Point')
VNA.channels.S21.trigger('Immediate')
VNA.channels.S21.average_clear()

VNA.channels.S21.cw_frequency(cwfrequency)
VNA.channels.S21.avg(averages)
VNA.channels.S21.power(detector_power)
VNA.channels.S21.bandwidth(detector_bandwidth)
VNA.channels.S21.npts(N_points)

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
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_CW_vs_time'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_CW_vs_time(exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
pump_source.status('off')
I_source.reset()
I_twpa.reset()
