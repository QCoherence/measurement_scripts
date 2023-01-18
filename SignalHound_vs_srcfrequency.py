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

def measure_vs_frequency(srcfrq_vec,exp,station,current_point=0):

    start = time.time()

    MW_source.status('on')
    I_source.reset()
    I_source.current(current_point*1.e-3)

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.frequency)
    meas.register_parameter(SH.freq_sweep,setpoints=[MW_source.frequency])
    meas.register_custom_parameter(name='frequency_axis_off')
    meas.register_custom_parameter(name='freq_sweep_off')

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for f in srcfrq_vec:

            MW_source.frequency(f*1e9)
            get_f = int(MW_source.frequency.get())
            datasaver.add_result((SH.frequency_axis, SH.frequency_axis()),(SH.freq_sweep,SH.freq_sweep()),(MW_source.frequency,get_f))

        MW_source.status('off')

        datasaver.add_result(('frequency_axis_off', SH.frequency_axis()),('freq_sweep_off',SH.freq_sweep()))

    end = time.time()
    print('elapsed time : ', (end-start)/3600.)

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
description='SA_vs_frequency'
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

current = -0.645 #mA

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
f_center = 8.886
f_span  = 0.1
f_start = f_center - f_span/2.
f_stop  = f_center + f_span/2.
f_step  = 5*1.e-4

f_points = int(abs(f_stop - f_start)/f_step)+1

f_vec=np.linspace(f_start, f_stop, f_points)

src_power = -30.

# Snapshot parameters
parameter_snap['f_source']={'f_start': f_start,'f_stop':f_stop,'f_step':f_step,'npts':f_points}

# Snapshot parameters
parameter_snap['mw_source']={'src_power': src_power ,
                             'src_frequency' : 'sweep'}

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
aver_num = 500
span=50*1.e6              #Hz
npoint = int(span/resBW) + 1
center_freq = 3.0e9        #Hz
ref_lvl = -20

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
# trace_time= span / (resBW**2)

# print('time for one trace : {} s'.format(trace_time))
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

MW_source.frequency(f_start*1e9)
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
exp_name = 'SA_vs_srcfrequency'

sample_name = 'Batch_3_G3_SQ_100_R1'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_frequency(srcfrq_vec=f_vec,exp=exp, station=station,current_point=current)

# Shutdown devices
I_source.reset()
MW_source.status('off')
