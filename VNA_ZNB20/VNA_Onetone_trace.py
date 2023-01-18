import qt
import numpy as np
import shutil
from datetime import datetime

def anritsu_onetone_trace(params):
    '''
    using Anritsu as a VNA
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
    vna.set_measBW(params['bandwidth'])
    vna.set_points(params['points'])
    vna.create_traces(('trace1',),('S21',))
    vna.set_status('on')
    vna.averageclear()

    qt.mstart()
    vna.measure()
    qt.msleep(0.1)
    [amp, phase] = vna.get_traces( ('trace1',))[0]
    vna.set_status('off')
    stop_time = datetime.now()
    print "sweep done in: ", (stop_time -start_time).total_seconds(), 's'
    return [amp, phase]

############################################
filename = 'VNA_Onetone_trace' #Filename that will be used to name the data folder. Use script filename.
file_dir = '' #File directory. It has the form working_directory\file_dir\filename


params_dict = {
                'freq_start' : 7.15e9,  #[Hz]
                'freq_stop'  : 7.3e9,  #[Hz]
                'points'     : 1001,            ### 501
                'bandwidth'  : 1e2,         ### 500   #[Hz]
                'averages'   : 1,
                'power'      : -15    #[dBm]
                }

freqs = np.linspace(params_dict['freq_start'],
                    params_dict['freq_stop'],
                    params_dict['points'])

# [amp, phase] = anritsu_onetone_trace(params_dict)


data = qt.Data(name=str(filename))
data.add_coordinate('VNA Frequency [GHz]', units='GHz')
data.add_value('S_21 [dB]',   units='dB')
data.add_value('Phase [rad]', units='rad')
data.add_value('Phase unwrapped',            units = 'deg')
data.create_file()

plot2d_1= qt.Plot2D(data, name='VNA_onetone_trace_amp', coorddim=0, valdim=1, maxtraces=2)
plot2d_2= qt.Plot2D(data, name='VNA_onetone_trace_phase_unwraped', coorddim=0, valdim=3, maxtraces=2)

try:
    [amp, phase] = anritsu_onetone_trace(params_dict)
    phase_unwrap = np.unwrap(phase)

    data.add_data_point( freqs, amp, phase, phase_unwrap)

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
