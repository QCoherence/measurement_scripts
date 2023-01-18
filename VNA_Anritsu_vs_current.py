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
import os
import sys

###############################################################################
#
#                        IMPORTING THE INSTRUMENTS
#
###############################################################################

sys.path.append('C:\QCodes_Driver_And_Scripts\Drivers')

import VNA_Anritsu as VNA_Anritsu
from HP3245A import HP3245A
from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A

try:
    VNA = VNA_Anritsu.MS46522B('VNA', 'TCPIP::192.168.10.52',  init_s_params=False)

except KeyError as er:
    VNA_Anritsu.MS46522B.close_all() #Disconnect and irreversibly tear down the instrument
    VNA = VNA_Anritsu.MS46522B('VNA', 'TCPIP::192.168.10.52',  init_s_params=False)

try:
    I_source = HP3245A('current_source', 'GPIB::17')

except KeyError as er:
    HP3245A.close_all() #Disconnect and irreversibly tear down the instrument
    I_source = HP3245A('current_source', 'GPIB::17')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_vs_current(current_vec, exp, station,ref=False):

    VNA.rf_on()
    I_source.reset()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(I_source.current)
    meas.register_parameter(VNA.channels.S21.trace_mag_phase, setpoints=(I_source.current,))

    meas.write_period = 10

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for current in current_vec:

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
I_start  =  0. #mA
I_end    =  4. #mA
points_I =  100
I_vec    = np.linspace(I_start, I_end, points_I)*1.e-3

points_I = len(I_vec)
# Snapshot parameters
parameter_snap['flux']={'I_start':I_start,'I_end':I_end,'I_points':len(I_vec)}

###############################################################################
#                             VNA PARAMETERS
###############################################################################

step_freq    = 1000*1.e-6
start_freq   = 2.5
end_freq     = 7.9
VNA_power    = 0.
IF_bandwidth = 7000
Averages     = 1
# points_VNA   = int(abs(end_freq - start_freq)/step_freq)+1
points_VNA   = 1001

trace_time   = points_VNA / IF_bandwidth

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=trace_time)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=Averages*points_I*trace_time)))

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
#                                  VNA
###############################################################################

VNA.add_channel('S21')

VNA.channels.S21.bandwidth(IF_bandwidth)
VNA.channels.S21.power(VNA_power)
VNA.channels.S21.avg(Averages)
VNA.channels.npts(points_VNA)
VNA.channels.start(start_freq*1e9)
VNA.channels.stop(end_freq*1e9)

###############################################################################
#                                  COIL
###############################################################################

I_source.current(0.)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_vs_current'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_current(I_vec, exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
I_source.reset()
