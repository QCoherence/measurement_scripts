from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
# from qcodes.plots.pyqtgraph import QtPlot
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

from RS_FSV import RS_FSV

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

def measure(ts_vec, exp, station):

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(FSV.sweep_time)
    meas.register_parameter(FSV.spectrum,setpoints=[FSV.sweep_time])

    with meas.run() as datasaver:

        for idx, ts in enumerate(ts_vec):

            FSV.sweep_time(ts)

            get_t = float(FSV.sweep_time.get())
            get_s = FSV.spectrum.get()

            sleep(0.01)

            datasaver.add_result((FSV.sweep_time, get_t),
                                (FSV.spectrum,get_s))

            id=datasaver.dataset.run_id
            qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                                 json.dumps(parameter_snap))



###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################

#############################################################################

start_all_logging()

# Create a station
station = qc.Station()
station.add_component(FSV)
station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='FSV_CW_vs_SWEEP_TIME'
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

################################################################################
#
#             Spectral Analyser parameters
#
################################################################################

FSV_rbw        = 40*1.e6
FSV_ref        = -20     #dB
FSV_avg        = 0
FSV_att        = 0 #dB
FSV_npt        = 625
FSV_center     = 3.5  #GHz
FSV_span       = 0   #0 span mode

sweep_time_min = FSV_npt / FSV_rbw
# FSQ_ratio          = np.ones(20)
FSV_time_sweep_vec = np.logspace(np.log10(sweep_time_min),2,50)

# Snapshot parameters
parameter_snap['FSV']={'center_freq':FSV_center,'average':FSV_avg,'res_bandwidth':FSV_rbw,'ref':FSV_ref,'att':FSV_att,'span':FSV_span}

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

FSV.detector('rms')

parameter_snap['FSV']['Npoints'] = FSV.n_points()
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=sum(FSV_time_sweep_vec))))

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'FSV_CW_vs_SWEEP_TIME'

sample_name = 'FSV_TEST_BENCH'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure(ts_vec=FSV_time_sweep_vec,exp=exp, station=station)

# Shutdown devices
