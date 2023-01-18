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
from HP3245A import HP3245A
from AS_ZVL6 import ZVL6

try :
    RS_SA = ZVL6('ZVL6','TCPIP::192.168.10.3',terminator='\n')

except KeyError as er:
    ZVL6.close_all()
    RS_SA = ZVL6('ZVL6', 'TCPIP::192.168.10.3',terminator='\n')

try:
    I_source = HP3245A('current_source', 'GPIB::17')

except KeyError as er:
    HP3245A.close_all() #Disconnect and irreversibly tear down the instrument
    I_source = HP3245A('current_source', 'GPIB::17')

try:
   MW_source=SMB100A('mw_source','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
   SMB100A.close_all()
   MW_source=SMB100A('mw_source','TCPIP0::192.168.10.6::inst0::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure(freq_vec, exp, station,avg=1,current_point=0.):

    I_source.reset()
    I_source.current(current_point*1.e-3)

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.frequency)
    meas.register_parameter(RS_SA.zero_span_trace,setpoints=[MW_source.frequency])
    meas.register_custom_parameter(name='ZVL6_zero_span_trace_norm',
                                  paramtype='array')

    meas.write_period = 10

    with meas.run() as datasaver:

        for idx, f in enumerate(freq_vec):

            MW_source.frequency(f*1e9)

            get_f = MW_source.frequency.get()

            get_s_off_lin=np.zeros(RS_SA.npts())
            get_s_lin    =np.zeros(RS_SA.npts())

            for i in range(avg) :

                MW_source.status('off')
                get_s_off_lin += 1.e-3*10**(RS_SA.zero_span_trace.get()*0.1)

                sleep(0.01)

                MW_source.status('on')
                get_s_lin += 1.e-3*10**(RS_SA.zero_span_trace.get()*0.1)

            sleep(0.01)

            get_s_norm_avg =1./avg * ( get_s_lin - get_s_off_lin )

            datasaver.add_result((MW_source.frequency, get_f),
                                 ('ZVL6_zero_span_trace_norm',get_s_norm_avg))

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
station.add_component(RS_SA)
station.add_component(I_source)
station.add_component(MW_source)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='SA_ZNL_CW_vs_MW_freq'
database_name = date+"_"+user+"_"+description+'.db'

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

current = -0.665  #mA
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                                MW SOURCE
###############################################################################

src_power     =  -35.
freq_start    =  8.8
freq_stop     =  8.99
# freq_step     =  0.002
#freq_step     =  0.0005
#freq_points   =  int(abs(freq_stop - freq_start)/freq_step)+1
freq_points   = 51
src_freq_vec = np.linspace(freq_start, freq_stop, freq_points)

# Snapshot parameters
parameter_snap['MW_source'] = {'power':src_power,'freq_start':freq_start,
                               'freq_stop':freq_stop,'points':freq_points}
###############################################################################
#                                SPECTRUM ANALYZER
###############################################################################

SA_rbw        = 10.e6
SA_vbw        = 3
SA_ref        = 0
SA_avg        = 1
SA_npt        = 201
SA_center     = 3.06
SA_span       = 0 #0 span mode
SA_avg        = 10
SA_time_sweep = 1./(SA_vbw) * SA_npt

# Snapshot parameters
parameter_snap['SA']={'CW_freq':SA_center,'average':SA_avg,
                      'video_bandwidth':SA_vbw,'res_bandwidth':SA_rbw,
                      'Npoints':SA_npt,'ref':SA_ref}

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=SA_avg*2*SA_time_sweep)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=SA_avg*2*freq_points*SA_time_sweep)))

###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.frequency(src_freq_vec[0]*1e9)
MW_source.power(src_power)

###############################################################################
#                            SPECTRUM ALALYZER
###############################################################################

RS_SA.center(SA_center*1e9)
RS_SA.span(SA_span*1.e9)
RS_SA.rbw(SA_rbw)
RS_SA.vbw(SA_vbw)
RS_SA.avg(1)
RS_SA.ref_lvl(SA_ref)
RS_SA.npts(SA_npt)
RS_SA.sweep_time(SA_time_sweep)

RS_SA.free_run()
RS_SA.external_ref()

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'SA_ZNL_CW_vs_MW_freq'

sample_name = 'Batch_3_G3_SQ_100_R1'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure(src_freq_vec,exp=exp, station=station,avg=SA_avg,current_point=current)

# Shutdown devices
MW_source.status('off')
I_source.reset()
