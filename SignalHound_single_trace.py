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
import os
import sys

###############################################################################
#
#                        IMPORTING THE INSTRUMENTS
#
###############################################################################

sys.path.append('C:\QCodes_Driver_And_Scripts\Drivers')

from VNA_ZNB20 import ZNB
from VNA_ZNB20 import ZNBChannel
from HP3245A import HP3245A
from SignalHound_USB_SA124B import SignalHound_USB_SA124B
from RS_SMB_100A import SMB100A

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
    SH = SignalHound_USB_SA124B('hound_SHG_vs_flux')

except KeyError as er:
   SignalHound_USB_SA124B.close_all()
   SH = SignalHound_USB_SA124B('hound_SHG_vs_flux')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_single_trace(exp,station,current_point=0):
    start = time.time()

    MW_source.status('on')
    I_source.reset()
    I_source.current(current_point*1.e-3)

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(SH.freq_sweep)
    meas.register_custom_parameter(name='frequency_axis_off')
    meas.register_custom_parameter(name='freq_sweep_off')

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        datasaver.add_result((SH.frequency_axis, SH.frequency_axis()),(SH.freq_sweep,SH.freq_sweep()))

        MW_source.status('off')

        datasaver.add_result(('frequency_axis_off', SH.frequency_axis()),('freq_sweep_off',SH.freq_sweep()))

    end = time.time()
    print('elapsed time : ', end-start)

###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################

start_all_logging()

# Create a station
station = qc.Station()
station.add_component(I_source)
station.add_component(SH)
station.add_component(MW_source)

station.snapshot()
station.components

# Experiment details
user='DF_LR'
date=datetime.today().strftime('%Y_%m_%d')
description='SA_single_trace'
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
# current = -0.645 #mA
current = -1.0 #mA

# Snapshot parameters
parameter_snap['flux']={'current': current}

################################################################################
#
#
#             SMB parameters
#
#
################################################################################

src_power = -20-26      #dBm
# src_frequency = 8.9013        #GHz
src_frequency = 3.9625        #GHz
# Snapshot parameters
parameter_snap['mw_source']={'src_power': src_power ,
                             'src_frequency' : src_frequency}

###############################################################################
#
#             Spectrum Analyser parameters
#
################################################################################
#RBW < 40Hz if span < 0.1*1e6 Hz
#RBW < 100kHZ if span < 100*1e6 Hz
#VBW = 0.1 * RBW

resBW = 250*1.e3            #Hz
videoBW = 6.5*1.e3        #Hz
aver_num = 2000
span=8*1.e6              #Hz
npoint = int(span/resBW) + 1
center_freq = 3.94e9        #Hz
ref_lvl = -30

#########################
# Contraintes SH
#########################

if span > 100*1e6 :
    if resBW<6.5*1e3 :
        print ('too little resBW')
    else :
        pass

elif span > 200*1e3 :
    if resBW<30 :
        print ('too little resBW')
    elif center_freq<16*1e6 and resBW < 6.5*1e3:
        print ('too little resBW')
    else:
        pass

# k = 120/1000 ### Le coeff n est pas correct
trace_time= span / (resBW**2)

print('time for one trace : {} s'.format(trace_time))
# Snapshot parameters
parameter_snap['SH'] = {'center':center_freq,
                                       'span' : span,
                                       'RBW': resBW,
                                       'VBW': videoBW,
                                       'Averages': aver_num,
                                       'points': npoint,
                                       'ref_lvl':ref_lvl}

###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.frequency(src_frequency*1e9)
MW_source.power(src_power)

###############################################################################
#                                SA SOURCE
###############################################################################

SH.frequency(center_freq)
SH.span(span)
SH.avg(aver_num)
SH.external_reference(True)
SH.rbw(resBW)
SH.vbw(videoBW)
SH.ref_lvl(ref_lvl)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'SA_single_trace'

sample_name = 'Batch_3_G3_SQ_100_R1'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_single_trace(exp=exp, station=station,current_point=current)

# Shutdown devices
I_source.reset()
MW_source.status('off')
