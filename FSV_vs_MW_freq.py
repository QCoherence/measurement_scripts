# Script to measure FSV trace vs MW source frequency
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

from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A
from HP3245A import HP3245A
from RS_FSV import RS_FSV
from VNA_RS import VNA

try:
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')


try:
    VNA = VNA('ZNB20', 'TCPIP0::192.168.10.2::inst0::INSTR',
               init_s_params=False,terminator='\n')

except KeyError as er:
    ZNB.close_all() #Disconnect and irreversibly tear down the instrument
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
   MW_source=SMB100A('mw_source','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
   SMB100A.close_all()
   MW_source=SMB100A('mw_source','TCPIP0::192.168.10.6::inst0::INSTR')

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

def measure_vs_frequency(srcfrq_vec,exp,station):

    start = time.time()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.frequency)
    meas.register_parameter(FSV.spectrum)
    meas.register_custom_parameter(name='rs_fsv_spectrum_bck',
                                   paramtype='array')

    MW_source.status(src_status)

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for f in srcfrq_vec:

            MW_source.frequency(f*1e9)

            I_source.current(0*1.e-3)
            get_s_bck = FSV.spectrum.get()

            I_source.current(current*1.e-3)
            get_s = FSV.spectrum.get()

            get_f = MW_source.frequency.get()

            datasaver.add_result((FSV.spectrum,get_s),('rs_fsv_spectrum_bck',get_s_bck),(MW_source.frequency,get_f))

    end = time.time()
    print('elapsed time : {}'.format(datetime.timedelta(seconds=end-start)))

###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################

start_all_logging()

# Create a station
station = qc.Station()
station.add_component(FSV)
station.add_component(pump_source)
station.add_component(I_source)
station.add_component(I_twpa)
station.add_component(MW_source)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='FSV_vs_MW_frequency'
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

current = -0.774 #mA
# current = 0.
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 5.42
pump_power   = 2.
pump_status  = 'off'
twpa_current = 2.7474747 #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}
################################################################################
#                               SMB PARAMETERS
################################################################################
src_power     = -20 #dBm
freq_start    = 8.6
freq_stop     = 9.1
freq_step     = 500.e-6
freq_point    = int(abs(freq_stop - freq_start)/freq_step)+1
# freq_point = 101

src_freq_vec = np.linspace(freq_start, freq_stop, freq_point)

src_status     = 'off'

# Snapshot parameters
parameter_snap['MW_source'] = {'power':src_power, 'freq_start' : freq_start,
                               'freq_stop':freq_stop,'points':freq_point}
################################################################################
#
#             Spectral Analyser parameters
#
################################################################################

FSQ_rbw         = 40*1.e6         #Hz
FSQ_ref         = -20             #dB
FSQ_avg         = 0               #dB
FSQ_att         = 0               #dB
FSQ_npt         = 625
FSQ_center      = 3.06          #GHz
# FSQ_center      = 5.0            #GHz

FSQ_span        = 0               #0 span mode
FSQ_time_sweep  = 20              #s

# Snapshot parameters
parameter_snap['FSQ']={'CW_freq':FSQ_center,'average':FSQ_avg,
                      'resolution_bandwidth':FSQ_rbw,
                      'Npoints':FSQ_npt,'ref':FSQ_ref,'att':FSQ_att,'sweep_time':FSQ_time_sweep}

print('\ntime for one trace : {} '
      .format(datetime.timedelta(seconds=FSQ_time_sweep)))

print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=FSQ_time_sweep * freq_point * 2)))

###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################
##############################################################################
#                                 COIL
##############################################################################

I_source.current(0*1.e-3)

###############################################################################
#                                  COIL TWPA
###############################################################################

I_twpa.current(twpa_current*1.e-3)

###############################################################################
#                                VNA OFF
###############################################################################
VNA.rf_off()
VNA.cont_meas_off()
################################################################################
#
#               Initialization SPECTRAL ANALYZER
#
################################################################################

FSV.res_BW(FSQ_rbw)
FSV.center_freq(FSQ_center*1.e9)
FSV.averages(FSQ_avg)
FSV.n_points(FSQ_npt)
FSV.span(FSQ_span)
FSV.ref_level(FSQ_ref)
FSV.input_att(FSQ_att)
FSV.detector('rms')
FSV.sweep_time(FSQ_time_sweep)

###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.frequency(freq_start*1e9)
MW_source.power(src_power)
MW_source.status(src_status)

###############################################################################
#                                TWPA PUMP SOURCE
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
exp_name = 'FSV_vs_MW_frequency'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_frequency(srcfrq_vec=src_freq_vec,exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
pump_source.status('off')
I_source.reset()
I_twpa.reset()
