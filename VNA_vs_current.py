from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
from qcodes.loops import Loop
from time import sleep
from tqdm.notebook import tqdm

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

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_vs_current(current_vec, exp, station):

    VNA.rf_on()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(I_source.current)
    meas.register_parameter(VNA.channels.S21.trace_mag_phase,
                            setpoints=[I_source.current])

    meas.write_period = 10

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for current in tqdm(current_vec):

            I_source.current(current)

            get_v = VNA.channels.S21.trace_mag_phase.get()
            get_i = I_source.current.get()

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
# station.add_component(MW_source)
# station.add_component(pump_source)
# station.add_component(I_twpa)

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
I_start  =  -1
I_end    =  0
# I_step   =   0.0016*0.5
# points_I = int(np.abs(I_start-I_end)/I_step)
points_I =  100
I_vec    = np.linspace(I_start, I_end, points_I)*1.e-3
#
# points_I = len(I_vec)
# Snapshot parameters
parameter_snap['flux']={'I_start':I_vec[0]*1.e3,'I_end':I_vec[-1]*1.e3,'I_points':len(I_vec)}

###############################################################################
#                             VNA PARAMETERS
###############################################################################

start_freq = 7
end_freq   = 9
step_freq    = 1*1.e-3
VNA_power    = 0
IF_bandwidth = 3000
Averages     = 1
# points_VNA   = int(abs(end_freq - start_freq)/step_freq)+1
points_VNA   = 2001

trace_time   = points_VNA / IF_bandwidth

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=trace_time)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=Averages*len(I_vec)*trace_time)))

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
#
# pump_freq    = 5.42
# pump_power   = 2.
# pump_status  = 'off'
# # twpa_current = 2.7474747 #mA
# twpa_current = 0.
#
#
# # Snapshot parameters
# parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
#                                 'current' : twpa_current}
#
# print('\nMeasurement with TWPA {}'.format(pump_status))
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
I_source.range(100e-3)

I_source.current(I_vec[0])

I_source.output('on')

###############################################################################
#                                  COIL TWPA
###############################################################################
#
# I_twpa.current(twpa_current*1.e-3)

###############################################################################
#                                  TWPA
###############################################################################
#
# pump_source.frequency(pump_freq*1.e9)
# pump_source.power(pump_power)
# pump_source.status(pump_status)

###############################################################################
#                                MW SOURCE
###############################################################################

# MW_source.status('off')

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_vs_current'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_current(I_vec, exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
# MW_source.status('off')
I_source.output('off')
