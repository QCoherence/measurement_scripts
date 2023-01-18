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

def measure(rbw_vec, exp, station):

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(FSV.res_BW)
    meas.register_parameter(FSV.spectrum,setpoints=[FSV.res_BW])

    with meas.run() as datasaver:

        for idx, f in enumerate(rbw_vec):

            FSV.res_BW(f)

            get_f = int(FSV.res_BW.get())
            get_s = FSV.spectrum.get()

            sleep(0.01)

            datasaver.add_result((FSV.res_BW, get_f),
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
description='FSV_CW_vs_RBW'
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
################################################################################
#
#             Spectral Analyser parameters
#
################################################################################

FSV_ref        = -20   #dB
FSV_avg        = 0
FSV_att        = 0 #dB
FSV_npt        = 1001
FSV_center     = 3.5  #GHz
FSV_span       = 0   #0 span mode
FSV_time_sweep = 2#s

rbw_min = FSV_npt / FSV_time_sweep

FSV_rbw_vec    = np.array([1,2,3,5,10,20,30,50,100,200,0.3e3,0.5e3,1e3,2.e3,3e3,5.e3,10e3,20e3,30e3,50e3,100e3,200e3,300e3,500e3,1e6,2e6,3e6,5e6,10e6,20e6,28e6,30e6,40e6])

idx_min = np.argmin(np.abs(rbw_min - FSV_rbw_vec))

FSV_rbw_vec = FSV_rbw_vec[idx_min:]

FSV_rbw_points = len(FSV_rbw_vec)

# Snapshot parameters
parameter_snap['FSV']={'center_freq':FSV_center,'average':FSV_avg,
                      'ref':FSV_ref,'att':FSV_att,'sweep_time':FSV_time_sweep,'FSV_npoints' : FSV_npt}

################################################################################
#
#               Initialization SPECTRAL ANALYZER
#
################################################################################

FSV.res_BW(FSV_rbw_vec[0])
FSV.center_freq(FSV_center*1.e9)
FSV.averages(FSV_avg)
FSV.n_points(FSV_npt)
FSV.span(FSV_span)
FSV.ref_level(FSV_ref)
FSV.input_att(FSV_att)
FSV.sweep_time(FSV_time_sweep)

FSV.detector('rms')

parameter_snap['FSV']['Npoints'] = FSV.n_points()

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=FSV_time_sweep)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=(FSV_avg+1)*FSV_rbw_points*FSV_time_sweep)))

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'FSV_CW_vs_RBW'

sample_name = 'FSV_TEST_BENCH'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure(FSV_rbw_vec,exp=exp, station=station)
