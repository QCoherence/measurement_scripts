# Script to measure 2T vs source power
#                            -- Dorian
from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
from qcodes.plots.pyqtgraph import QtPlot
from qcodes.loops import Loop
from time import sleep
from tqdm import tqdm

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
from VNA_RS import VNA

try:
    VNA = VNA('ZNB20', 'TCPIP0::192.168.10.2::inst0::INSTR',
               init_s_params=False,terminator='\n')

except KeyError as er:
    VNA.close_all() #Disconnect and irreversibly tear down the instrument
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
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

except KeyError as er:
   SGS100A.close_all()
   pump_source=SGS100A('pump_source','USB0::0x0AAD::0x0088::112061::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_vs_CW_freq(freq_vec,exp,station):

    VNA.rf_on()

    MW_source.status(src_status)
    MW_source.restartsweep()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.freq_vec)
    meas.register_parameter(VNA.channels.S21.cw_frequency)
    meas.register_parameter(VNA.channels.S21.point_fixed_frequency_mag_phase_trace,setpoints=[VNA.channels.S21.cw_frequency])

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for cw in freq_vec:

            MW_source.freq_start(cw-f_down_center - 0.5*f_down_span - f_step)
            MW_source.freq_stop(cw-f_down_center + 0.5*f_down_span)

            for i in tqdm(range(averages)):

                MW_source.restartsweep()
                VNA.channels.S21.cw_frequency(cw)
                MW_source.start_sweep()

                get_v = VNA.channels.S21.point_fixed_frequency_mag_phase_trace.get(initiate=True)

                get_cw = VNA.channels.S21.cw_frequency.get()
                get_f = MW_source.freq_vec.get()

            datasaver.add_result((VNA.channels.S21.point_fixed_frequency_mag_phase_trace, get_v),
                                 (MW_source.freq_vec, get_f),(VNA.channels.S21.cw_frequency, get_cw))

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
station.add_component(MW_source)
station.add_component(pump_source)
station.add_component(I_twpa)

station.snapshot()
station.components

# Experiment details
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='VNA_CW_vs_SMB_vs_cwfreq'
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

current = -0.71837 #mA
# current = 0.0  #mA
# Snapshot parameters
parameter_snap['flux']={'current': current}

###############################################################################
#                             VNA PARAMETERS
###############################################################################

center_freq_cw     = 8.86325*1.e9                                                #Hz
span_cw            = 50*1.e6                                                #Hz
points_cw          = 10
averages           = 100
sweeps             = averages
detector_power     =  0                                                    #dBm
detector_bandwidth =  1                                                   #Hz

# cw_freq_vec = np.linspace(center_freq_cw - 0.5*span_cw,center_freq_cw + 0.5*span_cw,points_cw)
cw_freq_vec = np.array([8.8525])*1.e9
# Snapshot parameters
parameter_snap['vna'] = {'points_cw':len(cw_freq_vec), 'power':detector_power,
                         'IF_bandwidth':detector_bandwidth, 'Averages':averages}

###############################################################################
#                              SMB PARAMETERS
###############################################################################
f_down_center =   3.*1.e9                                                   #Hz

f_down_span   = 200.*1.e6                                                   #Hz
# f_min    = f_center -0.5*f_span                                           #Hz
# f_max    = f_center +0.5*f_span                                           #Hz
# f_step   = 500*1.e3
N_points = 501
f_step   = f_down_span/N_points                                             #Hz
# freqs    = np.linspace(f_min,f_max+f_step,N_points+1)                     #Hz

smb_power  = 15                                                             #dBm
src_status = 'on'

# Dwell time security time [ms]: to ensure the SMA is not sweeping too fast
# compared to the VNA capabilities

DTsecurity=100

# Dwell time of the frequency sweep [ms]
dwelltime=1./detector_bandwidth*1000+DTsecurity

if dwelltime<5:
    dwelltime=5

# N_points     = int(round((f_max - f_min)/f_step))
trace_time = N_points*(1*dwelltime*1.e-3)*averages

parameter_snap['mw_source'] = {'f_down_center':f_down_center,'step_freq':f_step,
                                'N_points':N_points,'Power':smb_power,
                                'status':src_status}

print('time for one trace : {} s'.format(datetime.timedelta(seconds = trace_time)))
print('total time : {} s'.format(datetime.timedelta(seconds = trace_time*len(cw_freq_vec))))

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################

pump_freq    = 5.42
pump_power   = 2.
pump_status  = 'on'
twpa_current = 2.7474747 #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,
                               'pump_status' : pump_status,
                               'current' : twpa_current}

###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###############################################################################
#                                  COIL
###############################################################################

I_source.current(current*1.e-3)

###############################################################################
#                                  COIL TWPA
###############################################################################

I_twpa.current(twpa_current*1.e-3)

###############################################################################
#                                     VNA
###############################################################################

VNA.add_channel('S21',vna_parameter='S21')
VNA.channels.S21.format('dB')

VNA.channels.S21.initialize_two_tone_spectroscopy()

VNA.channels.S21.cw_frequency(cw_freq_vec[0])
VNA.channels.S21.avg(averages)
VNA.channels.S21.power(detector_power)
VNA.channels.S21.bandwidth(detector_bandwidth)
VNA.channels.S21.npts(N_points)

###############################################################################
#                                 MW SOURCE
###############################################################################

MW_source.power(smb_power)
MW_source.sourcemode('sweep')
MW_source.dwell_time(dwelltime*1.e-3)
MW_source.sweepmode('single')
MW_source.spacing_freq('LIN')
MW_source.freq_start(cw_freq_vec[0]-f_down_center - 0.5*f_down_span - f_step)
                                   # Hack to take into account that the first
                                   # frequency point of MW_source doesn't send
                                   # a trigger to the VNA
MW_source.freq_stop(cw_freq_vec[0]-f_down_center + 0.5*f_down_span)
MW_source.freq_step(f_step)
MW_source.freq_points(N_points+1)
MW_source.set_gui_update('on')

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
exp_name = 'VNA_CW_vs_SMB_vs_cwfreq'

sample_name = 'B3_G3SQ100R1_RKTWPA'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_CW_freq(cw_freq_vec,exp=exp, station=station)


# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
pump_source.status('off')
I_source.reset()
I_twpa.reset()
