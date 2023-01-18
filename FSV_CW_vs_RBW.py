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

from qcodes.instrument_drivers.yokogawa.GS200 import GS200

from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A
from HP3245A import HP3245A
from RS_FSV import RS_FSV
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

try:
    MW_source=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
    SMB100A.close_all()
    MW_source=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')

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
# station.add_component(pump_source)
station.add_component(I_source)
# station.add_component(I_twpa)
station.add_component(MW_source)

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

###############################################################################
#                             COIL PARAMETERS
###############################################################################

current = -0.774 #mA

# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 5.209                #GHz
pump_power   = -0.28                #dBm
pump_status  = 'off'
twpa_current = 2.7474747            #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}

print('\nMeasurement with TWPA {}'.format(pump_status))

###############################################################################
#                                MW SOURCE
###############################################################################

src_frequency  =  3.                #GHz
src_power      = -36                #dBm
src_status     = 'off'

# Snapshot parameters
parameter_snap['MW_source'] = {'freq':src_frequency,'power':src_power}

################################################################################
#
#             Spectral Analyser parameters
#
################################################################################

FSV_rbw_vec    = np.array([1,2,3,5,10,20,30,50,100,200,0.3e3,0.5e3,1e3,2.e3,3e3,5.e3,10e3,20e3,30e3,50e3,100e3,200e3,300e3,500e3,1e6,2e6,3e6,5e6,10e6,20e6,28e6,30e6,40e6])
FSV_rbw_points =  len(FSV_rbw_vec)

FSV_vbw        = 100 #Hz
FSV_ref        = -20   #dB
FSV_avg        = 0
FSV_att        = 0 #dB
FSV_npt        = 1001
FSV_center     = 3.5  #GHz
FSV_span       = 0   #0 span mode
FSV_time_sweep = 2*FSV_npt/FSV_vbw #s

# Snapshot parameters
parameter_snap['FSV']={'center_freq':FSV_center,'average':FSV_avg,
                      'video_bandwidth':FSV_vbw,
                      'Npoints':FSV_npt,'ref':FSV_ref,'att':FSV_att,'sweep_time':FSV_time_sweep}

###############################################################################
#                                  COIL
###############################################################################

if I_source.output()=='on':
    I_source.output('off')

I_source.source_mode('CURR')
I_source.range(10e-3)

I_source.current(current*1.e-3)

I_source.output('on')

###############################################################################
#                                  COIL TWPA
###############################################################################

# I_twpa.current(twpa_current*1.e-3)

################################################################################
#
#               Initialization SPECTRAL ANALYZER
#
################################################################################

FSV.res_BW(FSV_rbw_vec[0])
FSV.video_BW(FSV_vbw)
FSV.center_freq(FSV_center*1.e9)
FSV.averages(FSV_avg)
FSV.n_points(FSV_npt)
FSV.span(FSV_span)
FSV.ref_level(FSV_ref)
FSV.input_att(FSV_att)
FSV.sweep_time(FSV_time_sweep)

FSV.detector('rms')

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=FSV_time_sweep)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=(FSV_avg+1)*FSV_rbw_points*FSV_time_sweep)))

###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.status(src_status)

###############################################################################
#                                VNA OFF
###############################################################################
VNA.rf_off()
VNA.cont_meas_off()

###############################################################################
#                                TWPA PUMP SOURCE
###############################################################################

# pump_source.frequency(pump_freq*1.e9)
# pump_source.power(pump_power)
# pump_source.status(pump_status)

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'FSV_CW_vs_RBW'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure(FSV_rbw_vec,exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
I_source.output('off')
