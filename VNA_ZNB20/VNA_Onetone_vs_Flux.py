import qt
import numpy as np
import shutil
from datetime import datetime


def go_to_current( current_src_instr, cur_target, cur_step=5.0e-6, t_step=0.1 ):
    '''
    Sets current =  cur_target to current_source current_src_instr step by step
    '''
    ##_check_input_##
    current_is_valid = lambda x: abs(x) < 50e-3
    if not current_is_valid(cur_target):
        print "Wrong current to set"
        return False

    ##_set_to_current_mode_##
    if current_src_instr.get_mode() != u'dci':
        current_src_instr.set_mode('dci')

    ##_set_current_step_by_step_##
    cur_now = current_src_instr.get_current()

    ##_in_case_current_is_almost_there__##
    if abs(cur_now - cur_target) < abs(cur_step):
        current_src_instr.set_current(cur_target)

    direction = sign( cur_target -cur_now )

    while abs(cur_now -cur_target) > cur_step:
        cur_now += direction *cur_step
        sleep(t_step)
        current_src_instr.set_current(cur_now)
        print "Curent set to: ", round(1e3*cur_now, 6), " mA"

    current_src_instr.set_current(cur_target)
    print "Curent set to: ", round(1e3*cur_now, 6), " mA"
    return True

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
filename = 'VNA_Onetone_vs_Flux' #Filename that will be used to name the data folder. Use script filename.
file_dir = '' #File directory. It has the form working_directory\file_dir\filename

cur_start =  -3e-3 #Ampere
cur_stop  =  3e-3
cur_step  =  0.05e-3
# current_source = qt.instruments.get('hp3245')
current_source = qt.instruments.get('b2902a')


# vna_params = {
#                 'freq_start' : 4.0e9,  #[Hz]
#                 'freq_stop'  : 8.5e9,  #[Hz]
#                 'points'     : 1001,
#                 'bandwidth'  : 500,  #[Hz]
#                 'averages'   : 1,
#                 'power'      : -30    #[dBm]
#                 }

vna_params = {
                'freq_start' : 7.15e9,  #[Hz]
                'freq_stop'  : 7.3e9,  #[Hz]
                'points'     : 1001,
                'bandwidth'  : 50,  #[Hz]
                'averages'   : 1,
                'power'      : -15    #[dBm]
                }

freqs = np.linspace(vna_params['freq_start'],
                    vna_params['freq_stop'],
                    vna_params['points'])




#############################################

# current_source.set_mode('dci')
# current_source.set_channel('A')
# current_source.set_resolution('high')

full_start_time = datetime.now()

data = qt.Data(name=str(filename)) #Do not change filename. Include comments as 'filename + str(comments)'
data.add_coordinate('current [mA]', units='mA')
data.add_coordinate('Frequency [GHz]', units='GHz')
data.add_value('S_21 [dB]', units='dB')
data.add_value('Phase [deg]', units='deg')
data.create_file()

plot2d_1= qt.Plot2D(data, name='trace_amp',     coorddim=1, valdim=2, maxtraces=2)
plot2d_2= qt.Plot2D(data, name='trace_phase',   coorddim=1, valdim=3, maxtraces=2)
plot3d_1= qt.Plot3D(data, name='S21 vs flux',   coorddim=(0,1), valdim=2)
plot3d_2= qt.Plot3D(data, name='phase vs flux', coorddim=(0,1), valdim=3)


try:
    stored_current_value = 0.0
    stored_current_value = current_source.get_current()
    # current_source.set_current(cur_start)
    go_to_current( current_source, cur_start)
    # current_source.on()
    curr_vec = np.arange(cur_start, cur_stop +cur_step, cur_step)
    for cur in curr_vec:
        # current_source.set_current(cur)
        go_to_current( current_source, cur)
        qt.msleep(0.5)
        [ampdB, phase] = anritsu_onetone_trace(vna_params)
        data.add_data_point( cur*np.ones_like(freqs)*1e3, freqs, ampdB, phase )
        data.new_block()

except Exception as error:
    print str(error)

finally:
    # current_source.set_current( stored_current_value )
    go_to_current( current_source, stored_current_value)
    data.close_file()
    plot2d_1.save_png()
    plot2d_2.save_png()
    plot3d_1.save_png()
    plot3d_2.save_png()
    qt.mend()

    full_stop_time = datetime.now()
    print "Script done in: ", (full_stop_time -full_start_time).total_seconds(), 's'
