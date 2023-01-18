import qt
import numpy as np
import shutil
from datetime import datetime

def znb_onetone_trace(params):
    '''
    using ZNB20 as a VNA
    takes dictionary of VNA Parameters
    returns list: [amp_ndarray, phase_ndarray]
    '''
    start_time = datetime.now()
    freqs = linspace(params['freq_start'],
                     params['freq_stop'],
                     params['points'] ) /1.0e9

    vna = qt.instruments.get('vna znb20')

    #this block takes only 0.023 seconds
    vna.set_sweeptype('LIN')     #Linear frequency sweep
    vna.set_trigger('IMM')       #Immediate trigger. The vna measures the second trace immediately after the first one.
    vna.set_startfrequency(params['freq_start'])
    vna.set_stopfrequency(params['freq_stop'])
    vna.set_averages(params['averages'])
    vna.set_averagestatus('on')
    vna.set_power(params['power'])
    # vna.set_port2_power(params['power'])
    vna.set_measBW(params['bandwidth'])
    vna.set_points(params['points'])
    vna.create_traces(('trace1',),('S21',))
    vna.set_status('on')
    vna.averageclear()

    qt.mstart()
    vna.measure()
    qt.msleep(0.1)
    [amp, phase] = vna.get_traces( ('trace1',))[0]
    stop_time = datetime.now()
    print "sweep done in: ", (stop_time -start_time).total_seconds(), 's'
    return [amp, phase]

############################################
filename = 'VNA_Onetone_vs_PowerProbe' #Filename that will be used to name the data folder. Use script filename.
file_dir = '' #File directory. It has the form working_directory\file_dir\filename


vna_power_start =  -30.0
vna_power_stop  =   0.0
vna_power_step  =   5.
vna_power_vec = np.arange(vna_power_start, vna_power_stop, vna_power_step)


vna_parameters = {
                'freq_start' : 6.5e9,  #[Hz]
                'freq_stop'  : 6.8e9,  #[Hz]
                'points'     : 1001,
                'bandwidth'  : 10,  #[Hz]
                'averages'   : 1,
                'power'      : None    #[dBm]
                }

freqs = np.linspace(vna_parameters['freq_start'],
                    vna_parameters['freq_stop'],
                    vna_parameters['points'])

data = qt.Data( name=str(filename) )
data.add_coordinate('VNA power [dBm]', units='dBm')
data.add_coordinate('VNA Frequency [GHz]', units='GHz')
data.add_value('S_21 [dB]',   units='dB')
data.add_value('Phase [deg]', units='deg')
data.create_file()

plot2d_1 = qt.Plot2D(data, name='last_VNA_onetone_trace_amp',   coorddim=1, valdim=2, maxtraces=2)
plot2d_2 = qt.Plot2D(data, name='last_VNA_onetone_trace_phase', coorddim=1, valdim=3, maxtraces=2)
plot3d_1 = qt.Plot3D(data, name='VNA_onetone_trace_vs_PowerProbe_amp',   coorddims=(0,1), valdim=2, style='image')
plot3d_2 = qt.Plot3D(data, name='VNA_onetone_trace_vs_PowerProbe_phase', coorddims=(0,1), valdim=3, style='image')
plot3d_1.set_palette('bluewhitered')
plot3d_2.set_palette('bluewhitered')

try:
    for power in vna_power_vec:
        vna_parameters['power'] = power
        [amp, phase] = znb_onetone_trace(vna_parameters)
        data.add_data_point( power*np.ones_like(freqs), freqs, amp, phase)
        data.new_block()

except Exception as error:
    print str(error)

finally:
    data.close_file()
    data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.
    try:
        shutil.copy( file_dir +filename +'.py', data_dir +'\\' +filename +'.py' ) #Copy of the script
    except IOError:
        print 'Error saving the copy of the script'

    plot2d_1.save_png()
    plot2d_2.save_png()
    plot3d_1.save_png()
    plot3d_2.save_png()
