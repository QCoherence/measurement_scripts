from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
from qcodes.plots.pyqtgraph import QtPlot
from qcodes.loops import Loop
from datetime import datetime
from time import sleep

import matplotlib.pyplot as plt
import qcodes as qc
import numpy as np
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

from HP3245A import HP3245A
from RS_SMB_100A import SMB100A
from RS_FSQ import RS_FSQ

try:
    I_source = HP3245A('current_source', 'GPIB::24')

except KeyError as er:
    HP3245A.close_all() #Disconnect and irreversibly tear down the instrument
    I_source = HP3245A('current_source', 'GPIB::24')

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

def measure_vs_power(power_vec,exp,station,current_point=0):

    MW_source.status('on')
    I_source.reset()
    I_source.current(current_point*1.e-3)

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.power)
    meas.register_parameter(FSQ.freq_axis)
    meas.register_parameter(FSQ.spectrum,setpoints=[FSQ.freq_axis])
    meas.register_custom_parameter(name='freq_axis_off')
    meas.register_custom_parameter(name='spectrum_off')

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for pow in power_vec:

            MW_source.power(pow)
            get_p = MW_source.power.get()
            datasaver.add_result((FSQ.freq_axis, FSQ.freq_axis()),(FSQ.spectrum,FSQ.spectrum()),(MW_source.power,get_p))

        MW_source.status('off')

        datasaver.add_result(('freq_axis_off', FSQ.freq_axis()),('spectrum_off',FSQ.spectrum()))

###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################

start_all_logging()

# Create a station
station = qc.Station()
station.add_component(I_source)
station.add_component(FSQ)
station.add_component(MW_source)

station.snapshot()
station.components

# Experiment details
user='DF_LR'
date=datetime.today().strftime('%Y_%m_%d')
description='FSQ_vs_power'
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

################################################################################
#
#
#             SMB parameters
#
#
################################################################################

# Power sweep
p_start  = -30.
p_end    = -20.
p_points = 3
p_vec=np.linspace(p_start, p_end, p_points)

# Snapshot parameters
parameter_snap['power_source']={'p_start':p_start,'p_end':p_end,'npts':p_points}

# src_frequency = 8.692      #GHz
src_frequency = 3.9625      #GHz
# Snapshot parameters
parameter_snap['mw_source']={'src_power': 'sweep' ,
                             'src_frequency' : src_frequency}

########################################################
#
#             Spectral Analyser parameters
#
#########################################################

rBW = 500e3            #Hz
vBW = 1           #Hz
aver_num = 1
span=120e6           #Hz
npoint = int(span/rBW) + 1
center_freq = 3.9013    #Hz
ref_lvl = -40

# Snapshot parameters
parameter_snap['FSQ'] = {'center':center_freq,
                                       'span' : span,
                                       'RBW': rBW,
                                       'VBW': vBW,
                                       'Averages': aver_num,
                                       'points': npoint,
                                       'ref_lvl':ref_lvl}

###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###########################################################
#
#
#               Initialization SPECTRAL ANALYZER
#
#
###########################################################

FSQ.res_BW(rBW)
FSQ.video_BW(vBW)
FSQ.center_freq(center_freq*1e9)
FSQ.averages(aver_num)
FSQ.n_points(npoint)
FSQ.span(span)
FSQ.ref_level(ref_lvl)
FSQ.average_type('rms')

trace_time = int(FSQ.sweep_time_direct()) * (p_points+1) * aver_num /3600
print('Experience time : {} h'.format(trace_time))
###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.frequency(src_frequency*1e9)
MW_source.power(p_start)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'FSQ_vs_power'

sample_name = 'Batch_3_G3_SQ_100_R1'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_power(power_vec=p_vec,exp=exp, station=station,current_point=current)

# Shutdown devices
I_source.reset()
MW_source.status('off')
