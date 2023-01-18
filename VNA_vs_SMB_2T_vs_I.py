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
import os
import sys

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
    MW_source=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')

except KeyError as er:
    SMB100A.close_all()
    MW_source=SMB100A('mw_pump','TCPIP0::192.168.10.6::inst0::INSTR')



# ###############################################################################
# #
# #                   FUNCTION USED FOR LIVE PLOTTING
# #
# ###############################################################################
#

# def live_plotter(x_vec,y_data,line,vertline, identifier='', pause_time=0.1):
#     global fig,ax
#
#     if line==[]:
#         # this is the call to matplotlib that allows dynamic plotting
#         plt.ion()
#         fig = plt.figure(figsize=(13,6))
#         ax = fig.add_subplot(111)
#         # create a variable for the line so we can later update it
#         line, = ax.plot(x_vec,y_data,'-')
#         #update plot label/title
#         plt.ylabel(r'$\arg(S_{21})$')
#         plt.xlabel(r'VNA frequency')
#         plt.title(identifier)
#         plt.show()
#
#     # after the figure, axis, and line are created, we only need to update the y-data
#     line.set_ydata(y_data)
#     ax.axvline(vertline,color='red')
#     # adjust limits if new data goes beyond bounds
#     if np.min(y_data)<=line.axes.get_ylim()[0] or np.max(y_data)>=line.axes.get_ylim()[1]:
#         plt.ylim([np.min(y_data)-np.std(y_data),np.max(y_data)+np.std(y_data)])
#     # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
#     plt.pause(pause_time)
#
#     # return line so we can update it again in the next iteration
#     return line

###############################################################################
#
#                   FUNCTION USED TO RUN THE MEASUREMENT
#
###############################################################################
def measure_2T_vs_I(current_vec,cw_freq_vec,exp,station):

    VNA.rf_on()
    MW_source.status('on')
    MW_source.restartsweep()

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(MW_source.freq_vec)
    meas.register_parameter(I_source.current)
    meas.register_parameter(VNA.channels.S21.cw_frequency,
                            setpoints=[I_source.current])
    meas.register_parameter(VNA.channels.S21.point_fixed_frequency_mag_phase_trace,
                            setpoints=[I_source.current])

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec( captured_run_id=id).add_metadata('parameter_snap',
                             json.dumps(parameter_snap))

        # cw_freq_vec = np.zeros(len(current_vec))

        for i,cur in enumerate(current_vec):

            VNA.channels.S21.cw_frequency(cw_freq_vec[i]*1.e9)
            I_source.current(cur)
            MW_source.restartsweep()
            MW_source.start_sweep()

            # for freq in freqs:
            #     sleep(dwelltime*1.e-3)

            # Save data

            get_i    = I_source.current.get()
            get_v_cw = VNA.channels.S21.point_fixed_frequency_mag_phase_trace.get(initiate=True)
            get_f    = MW_source.freq_vec.get()
            get_cw   = VNA.channels.S21.cw_frequency.get()

            datasaver.add_result((VNA.channels.S21.point_fixed_frequency_mag_phase_trace, get_v_cw),
                                 (MW_source.freq_vec, get_f),(I_source.current, get_i),
                                 (VNA.channels.S21.cw_frequency,get_cw))

            # get_v = VNA.channels.S21.point_fixed_frequency_mag_phase_trace.get(initiate=False)

            # VNA.channels.S21.initialize_two_tone_spectroscopy()

            # MW_source.status('off')
            # sleep(0.1)

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
user='DF'
date=datetime.datetime.today().strftime('%Y_%m_%d')
description='2T_VNA_vs_SMB_vs_I'
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
I_file = np.loadtxt('current_fit_mode3_3.dat')

N_split  = 10
I_vec    = I_file[::N_split]
I_start  =  I_vec[0]
I_end    =  I_vec [-1]
points_I = len([I_vec])
I_step   = (I_end - I_start)/points_I

# Snapshot parameters
parameter_snap['flux']={'I_start':I_start,'I_end':I_end,'I_step':I_step}

###############################################################################
#                             VNA PARAMETERS
###############################################################################

# Parameters for when the VNA is used as CW

cw_freq_vec        = np.loadtxt('fr_fit_mode3_3.dat')[::N_split]   #Hz
cw_averages        = 1
sweeps             = cw_averages
detector_power     = -10          #dB
detector_bandwidth = 100           #Hz

# Snapshot parameters
parameter_snap['vna'] = {'cw_freq':'sweep', 'power':detector_power,
                         'IF_bandwidth':detector_bandwidth, 'Averages':cw_averages}

###############################################################################
#                        SPECTROSCOPY TONE PARAMETERS
###############################################################################
f_min         = 2.0*1.e9                              #Hz
f_max         = 4*1.e9                              #Hz
f_step        = 1*1.e6                             #Hz
freqs         = np.arange(f_min,f_max+f_step,f_step)   #Hz

power = -10

# Dwell time security time [ms]: to ensure the SMA is not sweeping too fast
# compared to the VNA capabilities

DTsecurity=100

# Dwell time of the frequency sweep [ms]
dwelltime=1./detector_bandwidth*1000+DTsecurity

if dwelltime<5:
    dwelltime=5

N_points     = int(round((f_max - f_min)/f_step))

parameter_snap['mw_source'] = {'start_freq':f_min, 'stop_freq':f_max,
                               'step_freq':f_step, 'N_points':N_points,
                              'power':power}

trace_time = N_points*(1*dwelltime*1.e-3)

print('time for one trace : {} s'.format(trace_time))
print('total time : {} h'.format(trace_time*len(I_vec)/3600.))

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

VNA.channels.S21.initialize_two_tone_spectroscopy()

VNA.channels.S21.cw_frequency(cw_freq_vec[0]*1.e9)
VNA.channels.S21.avg(cw_averages)
VNA.channels.S21.power(detector_power)
VNA.channels.S21.bandwidth(detector_bandwidth)
VNA.channels.S21.npts(N_points)

###############################################################################
#                                 MW SOURCE
###############################################################################

MW_source.power(power)
MW_source.sourcemode('sweep')
MW_source.dwell_time(dwelltime*1.e-3)
MW_source.sweepmode('single')
MW_source.spacing_freq('LIN')
MW_source.freq_start(f_min-f_step) # Hack to take into account that the first
                                   # frequency point of MW_source doesn't send
                                   # a trigger to the VNA
MW_source.freq_stop(f_max)
MW_source.freq_step(f_step)
MW_source.freq_points(N_points+1)
MW_source.set_gui_update('on')

if I_source.output()=='on':
    I_source.output('off')

I_source.source_mode('CURR')
I_source.range(10e-3)

I_source.current(I_vec[0])

I_source.output('on')

###############################################################################
#
#                              MEASUREMENT
#
###############################################################################

# Load experiment
exp_name = '2T_VNA_vs_SMB_vs_P'

sample_name = 'B5_G3_GALV_SQ200_1ST'

exp=qc.load_or_create_experiment(experiment_name=exp_name,
                          sample_name=sample_name)

measure_2T_vs_I(I_vec,cw_freq_vec,exp=exp, station=station)

# Shutdown devices
VNA.rf_off()
VNA.cont_meas_off()
MW_source.status('off')
I_source.reset()
