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

def measure(center_vec, exp, station):

    meas = qc.Measurement(exp=exp, station=station)
    meas.register_parameter(FSV.center_freq)
    meas.register_parameter(FSV.spectrum,setpoints=[FSV.center_freq])
    meas.register_custom_parameter(name='spectrum_mw_off',paramtype='array',setpoints=[FSV.center_freq])

    with meas.run() as datasaver:

        id=datasaver.dataset.run_id
        qc.load_by_run_spec(captured_run_id=id).add_metadata('parameter_snap',
                                 json.dumps(parameter_snap))

        for idx, center in enumerate(center_vec):

            FSV.center_freq(center*1.e9)

            MW_source.status('off')

            get_s_off = FSV.spectrum.get()

            MW_source.status(src_status)

            get_c = float(FSV.center_freq.get())
            get_s = FSV.spectrum.get()

            sleep(0.01)

            datasaver.add_result((FSV.center_freq, get_c),(FSV.spectrum,get_s),("spectrum_mw_off",get_s_off))

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
description='FSV_CW_vs_CWfreq'
database_name = date+"_"+user+"_"+description


script_dir=os.path.dirname(os.path.abspath("__file__"))
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


qc.initialise_or_create_database_at(data_dir+'\\'+database_name)
qc.config.core.db_location

parameter_snap={}


current = -0.7688 #mA

# Snapshot parameters
parameter_snap['flux']={'current': current}

# TWPA PUMP PARAMETERS
pump_freq    = 5.209                #GHz
pump_power   = -0.28                #dBm
pump_status  = 'off'
twpa_current = 2.7474747            #mA

# Snapshot parameters
parameter_snap['twpa_pump'] = {'freq':pump_freq,'pump_power':pump_power,'pump_status' : pump_status,
                                'current' : twpa_current}

print('\nMeasurement with TWPA {}'.format(pump_status))


# MW SOURCE

src_frequency  =  9.244                 #GHz
# src_power      = np.linspace(-30,10,2) #dBm
src_power = np.array([-30])
src_status     = 'on'

# Snapshot parameters
parameter_snap['MW_source'] = {'freq':src_frequency,'power':src_power[0]}

# Spectral Analyser parameters

FSV_rbw         = 40*1.e6 #Hz
FSV_ref         = -20     #dB
FSV_avg         = 0
FSV_att         = 0       #dB
FSV_npt         = 625
FSV_center      = 3.129   #GHz
FSV_center_span = 1       #GHz
# FSV_cw_vec      = np.arange(FSV_center-0.5*FSV_center_span,FSV_center+0.5*FSV_center_span,FSV_rbw*1.e-9)
FSC_cw_step     = 10*1.e6
FSV_cw_vec      = np.arange(FSV_center-0.5*FSV_center_span,FSV_center+0.5*FSV_center_span,FSC_cw_step*1.e-9)
FSV_span        = 0       #0 span mode

sweep_time_min = FSV_npt / FSV_rbw

FSV_time_sweep  = 15*60/2/len(FSV_cw_vec)
FSV_time_sweep  = max(sweep_time_min,FSV_time_sweep)


if FSV_time_sweep < sweep_time_min :
    raise ValueError("sweeptime to small with respect to the sweep points and rbw")
# Snapshot parameters
parameter_snap['FSV']={'center_freq':FSV_center,'average':FSV_avg,'res_bandwidth':FSV_rbw,
                      'Npoints':FSV_npt,'ref':FSV_ref,'att':FSV_att,'span':FSV_span,'sweeptime':FSV_time_sweep}

for power in src_power :

    if I_source.output()=='on':
        I_source.output('off')

    I_source.source_mode('CURR')
    I_source.range(10e-3)

    I_source.current(current*1.e-3)

    I_source.output('on')


    FSV.res_BW(FSV_rbw)
    FSV.center_freq(FSV_cw_vec[0]*1.e9)
    FSV.averages(FSV_avg)
    FSV.n_points(FSV_npt)
    FSV.span(FSV_span)
    FSV.ref_level(FSV_ref)
    FSV.input_att(FSV_att)
    FSV.sweep_time(FSV_time_sweep)

    FSV.detector('rms')

    parameter_snap['FSV']['Npoints'] = FSV.n_points()

    parameter_snap['MW_source']['power']=power

    print('\ntime estimation for all measurement : {} '
          .format(datetime.timedelta(seconds=2*len(FSV_cw_vec)*FSV_time_sweep)))


    MW_source.frequency(src_frequency*1.e9)
    MW_source.power(power)
    MW_source.status(src_status)

    VNA.rf_off()
    VNA.cont_meas_off()

    # Load experiment
    exp_name = 'FSV_CW_vs_CWfreq'

    sample_name = 'B5_G3_GALV_SQ200_1ST'

    exp=qc.load_or_create_experiment(experiment_name=exp_name,
                              sample_name=sample_name)
    print(parameter_snap)
    measure(center_vec=FSV_cw_vec,exp=exp, station=station)

    # Shutdown devices
    VNA.rf_off()
    VNA.cont_meas_off()
    MW_source.status('off')
    I_source.output('off')
