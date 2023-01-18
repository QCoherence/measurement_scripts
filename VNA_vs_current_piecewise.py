# Dorian oct 2021
from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
from qcodes.plots.pyqtgraph import QtPlot
from qcodes.loops import Loop
from utilities import *
from time import sleep
from tqdm import tqdm
from glob import glob

import matplotlib.pyplot as plt
import scipy.optimize as sci
import qcodes as qc
import numpy as np
import datetime
import time
import json
import sys
import os

###############################################################################
#
#                     IMPORTING FREQ VS CURRENT VECTOR
#
###############################################################################

fname   = glob('fr_vs_current\\f2_vs_current_CD9_big.dat')
dataRef = np.loadtxt(fname[0],delimiter = ',')

_flux  = dataRef[:,0]
_freq   = dataRef[:,1]

###############################################################################
#
#                        IMPORTING THE INSTRUMENTS
#
###############################################################################

sys.path.append('C:\QCodes_Driver_And_Scripts\Drivers')

from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A
from HP3245A import HP3245A
from RS_FSQ import RS_FSQ
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

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_vs_current(current_vec, center_freq_vec, exp, station,ref=False):

    if len(current_vec)!=len(center_freq_vec):

        raise Exception('Current and frequency vector must have the same length')

    VNA.rf_on()
    I_source.reset()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(I_source.current)
    meas.register_parameter(VNA.channels.S21.trace_mag_phase,
                            setpoints=[I_source.current])

    meas.write_period = 10

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        for current,center in zip(tqdm(current_vec),center_freq_vec):

            I_source.current(current*1.e-3)
            VNA.channels.start((center-0.5*span)*1e9)
            VNA.channels.stop((center+0.5*span)*1e9)

            get_v = VNA.channels.S21.trace_mag_phase.get()
            get_i = I_source.current.get()

            datasaver.add_result((VNA.channels.S21.trace_mag_phase, get_v),
                                 (I_source.current,get_i))

###############################################################################
#
#                      INITIALIZE QCODES EXPERIMENT
#
###############################################################################

start_all_logging()

# Create a station
station = qc.Station()
station.add_component(VNA)
station.add_component(MW_source)
station.add_component(pump_source)
station.add_component(I_source)
station.add_component(I_twpa)

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
# phi_max = 0
# phi_min =-0.1
#
# points_I  = 4
# array_cos = np.linspace(np.cos(np.pi*phi_min),np.cos(np.pi*phi_max),points_I//2)
# #
# array_phi_1 = 1/np.pi * np.arccos(array_cos) - 1
# array_phi_2 = -0.5 + np.abs(array_phi_1 + 0.5)
# # array_phi_2 = array_phi_2[1:]
# # array_phi_2 = array_phi_2
# array_phi_tot = np.sort(np.concatenate((array_phi_1,array_phi_2)))-5
# # array_phi_tot = array_phi_2[::-1] - 5
# print(array_phi_tot)
#
#
# # array_phi_tot = np.linspace(phi_min,phi_max,points_I)
#
# # Flux points from the file
# normFlux = np.array([np.abs(_flux - _p) for _p in array_phi_tot])
# idxFlux  = np.argmin(normFlux,axis=1)
#
#
# # Convert to current
# A = 0.59514
# B = 0.05716
#
# # shift = -0.0561
# # shift = -0.0906 - 0.092
# shift = 0
# I_vec = 1./A * (array_phi_tot - B) + shift

I_vec = np.linspace(-11.2,-11.2,1)

# Current points from the file
normFlux = np.array([np.abs(_flux - _p) for _p in I_vec])
idxFlux  = np.argmin(normFlux,axis=1)
print(I_vec)

# Snapshot parameters
parameter_snap['flux']={'I_start':I_vec[0],'I_end':I_vec[-1],'I_points':len(I_vec)}

###############################################################################
#                             VNA PARAMETERS
###############################################################################
center_vec     = _freq[idxFlux]+0.6
print(center_vec)

span         = 0.5
step_freq    = 250*1.e-6
VNA_power    = -30
IF_bandwidth = 10
Averages     = 1
points_VNA   = int(span/step_freq)+1
# points_VNA   = 4001

trace_time   = points_VNA / IF_bandwidth

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=trace_time)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=Averages*len(I_vec)*trace_time)))

# Snapshot parameters
parameter_snap['vna'] = {'start_freq':center_vec[0], 'end_freq':center_vec[-1],
                         'VNA_power':VNA_power, 'IF_bandwidth':IF_bandwidth,
                         'Averages':Averages, 'span': span, 'step' : step_freq}

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
###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###############################################################################
#                                  VNA
###############################################################################

VNA.add_channel('S21',vna_parameter='S21')

VNA.channels.S21.format('dB')
VNA.channels.S21.bandwidth(IF_bandwidth)
VNA.channels.S21.power(VNA_power)
VNA.channels.S21.avg(Averages)
VNA.channels.npts(points_VNA)
VNA.channels.start((center_vec[0]-0.5*span)*1e9)
VNA.channels.stop((center_vec[0]+0.5*span)*1e9)

###############################################################################
#                                  COIL
###############################################################################

I_source.current(0.)

###############################################################################
#                                  COIL TWPA
###############################################################################

I_twpa.current(twpa_current*1.e-3)

###############################################################################
#                                  TWPA
###############################################################################

pump_source.frequency(pump_freq*1.e9)
pump_source.power(pump_power)
pump_source.status(pump_status)

###############################################################################
#                                MW SOURCE
###############################################################################

MW_source.status('off')

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

measure_vs_current(I_vec,center_vec, exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
pump_source.status('off')
I_source.reset()
I_twpa.reset()
