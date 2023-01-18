# Script to measure VNA trace vs VNA power
#                            -- Dorian
from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from qcodes.dataset.plotting import plot_dataset,plot_by_id
from qcodes.logger.logger import start_all_logging
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

from qcodes.instrument_drivers.yokogawa.GS200 import GS200

from RS_SMB_100A import SMB100A
from RS_SGS_100A import SGS100A
from HP3245A import HP3245A
from RS_FSQ import RS_FSQ
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
    MW_source=SGS100A('mw_pump','TCPIP0::192.168.10.56::inst0::INSTR')

except KeyError as er:
    SMB100A.close_all()
    MW_source=SGS100A('mw_pump','TCPIP0::192.168.10.56::inst0::INSTR')

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################

def measure_vs_power(power_vec, exp, station):

    VNA.rf_on()
    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(VNA.channels.S21.power)
    meas.register_parameter(VNA.channels.S21.trace_mag_phase,
                            setpoints=[VNA.channels.S21.power])
    meas.write_period = 10

    with meas.run() as datasaver:

        for idx, pow in tqdm(enumerate(power_vec)):

            VNA.channels.S21.power(pow)

            get_v = VNA.channels.S21.trace_mag_phase.get()
            get_p = VNA.channels.S21.power.get()

            datasaver.add_result((VNA.channels.S21.trace_mag_phase, get_v),
                                 (VNA.channels.S21.power,get_p))

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
station.add_component(VNA)
station.add_component(I_source)
station.add_component(MW_source)
# station.add_component(pump_source)
# station.add_component(I_twpa)

station.snapshot()
station.components

# Experiment details
date=datetime.datetime.today().strftime('%Y_%m_%d')
user='DF'
description='VNA_vs_power'
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
# current = -0.694 #mA
current = 0

# Snapshot parameters
parameter_snap['flux']={'current': current}
###############################################################################
#                             VNA PARAMETERS
###############################################################################

# Power sweep
p_start  =  -20.
p_end    =  10.
p_points =  100
p_vec=np.linspace(p_start, p_end, p_points)

# Snapshot parameters
parameter_snap['power_vna']={'p_start':p_start,'p_end':p_end,'npts':p_points}

# Frequency sweep
# start_freq   = 10.3073*1.e9
# end_freq     = 3.09
# center_freq  = 10.
# span         = 10.5
# start_freq   = center_freq - 0.5*span
# end_freq     = center_freq + 0.5*span
start_freq = 7.974+0.7
end_freq  = 8.715+0.7
IF_bandwidth =  100
Averages     = 1
points_VNA = 501

trace_time=points_VNA / IF_bandwidth * Averages

print('\ntime for one trace : {}'.format(datetime.timedelta(seconds=trace_time)))
print('\ntime estimation for all measurement : {} '
      .format(datetime.timedelta(seconds=Averages*p_points*trace_time)))

# Snapshot parameters
parameter_snap['vna'] = {'start_freq':start_freq, 'end_freq':end_freq,
                         'IF_bandwidth':IF_bandwidth, 'Averages':Averages,
                         'points':points_VNA}

###############################################################################
#                             TWPA PUMP PARAMETERS
###############################################################################
#
# pump_freq    = 5.42
# pump_power   = 2.
# pump_status  = 'off'
# # twpa_current = 2.7474747 #mA
# twpa_current =  0.0       #mA

# # Snapshot parameters
# parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
#                                 'current' : twpa_current}
###############################################################################
#
#                          SETTING UP INSTRUMENTS
#
###############################################################################

###############################################################################
#                                  COIL
###############################################################################

# I_source.current(current*1.e-3)

#yokogawa
if I_source.output()=='on':
    I_source.output('off')

I_source.source_mode('CURR')
I_source.range(100e-3)

I_source.current(current*1.e-3)

I_source.output('on')

###############################################################################
#                                  COIL TWPA
###############################################################################

# I_twpa.current(twpa_current*1.e-3)

###############################################################################
#                                  VNA
###############################################################################

VNA.add_channel('S21',vna_parameter='S21')

VNA.channels.S21.format('dB')
VNA.channels.S21.bandwidth(IF_bandwidth)
VNA.channels.S21.power(p_start)
VNA.channels.S21.avg(Averages)
VNA.channels.npts(points_VNA)
VNA.channels.start(start_freq*1e9)
VNA.channels.stop(end_freq*1e9)

###############################################################################
#                                  TWPA
###############################################################################

# pump_source.frequency(pump_freq*1.e9)
# pump_source.power(pump_power)
# pump_source.status(pump_status)

###############################################################################
#                                  SMB
###############################################################################

MW_source.status('off')

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = 'VNA_vs_power'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_vs_power(p_vec, exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
I_source.output('off')
