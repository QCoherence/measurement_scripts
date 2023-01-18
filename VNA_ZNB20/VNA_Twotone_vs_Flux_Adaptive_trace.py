# -*- coding: utf-8 -*-
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

    vna = qt.instruments.get('vna znb20')   ### 'vna'

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
    print "onetone sweep done in: ", (stop_time -start_time).total_seconds(), 's'
    return [amp, phase]

def anritsu_twotone_trace_vs_smb(vna_params, smb_second_tone_params):
    '''
    using Anritsu as a VNA, and SMB100A as 2nd tone generator
    takes dictionary of VNA Parameters, dict of SMB parameters
    returns list: [amp_ndarray, phase_ndarray]
    '''
    freqs=np.arange( smb_second_tone_params['f_min'],
                     smb_second_tone_params['f_max'] +smb_second_tone_params['f_step'],
                     smb_second_tone_params['f_step'] )
    points = len(freqs)

    #dwell time security time [ms]: to ensure the SMA is not sweeping too fast compared to the VNA capabilities
    DTsecurity = 100 #[ms]
    #dwell time of the frequency sweep [ms]
    dwelltime = 1./vna_params['bandwidth']*1000 +DTsecurity

    vna = qt.instruments.get('vna znb20') #Anritsu
    vna.initialize_two_tone_spectroscopy(('trace1',),('S21',))
    vna.set_cwfrequency(vna_params['cwfreq'])
    vna.set_averages(vna_params['averages'])
    vna.set_averagestatus('on')
    vna.set_power(vna_params['power'])
    # vna.set_port2_power(vna_params['power'])
    vna.set_measBW(vna_params['bandwidth'])
    vna.set_points(points)
    vna.set_trigger('EXT')

    probe_src = qt.instruments.get('smb_2') ##SMB100A
    probe_src.set_power(smb_second_tone_params['power'])
    probe_src.set_freqsweep('on')
    probe_src.set_dwelltime(dwelltime)
    # probe_src.set_sweepmode('single')
    probe_src.set_sweepmode('auto')
    probe_src.set_startfreq(smb_second_tone_params['f_min']-smb_second_tone_params['f_step']) #hack to take into account that the first frequency point of probe_src doesn't send a trigger to the VNA
    probe_src.set_stopfreq(smb_second_tone_params['f_max'])
    probe_src.set_stepfreq(smb_second_tone_params['f_step'])
    probe_src.set_pointsfreq(points+1)

    # print "expected measurement time is:", round(len(points) *vna_params['bandwidth'] *vna_params['averages'] ), "sec"
    print "dwelltime = ", dwelltime, " ms"
    print "expected measurement time is:", round(  1e-3*(dwelltime *len(freqs) ) ), "sec"

    start_time = datetime.now()
    qt.mstart()
    qt.msleep(0.1)

    probe_src.set_status('on')
    probe_src.restartsweep()
    qt.msleep(0.1)

    vna.averageclear()
    vna.measure()
    qt.msleep(0.1)

    probe_src.startsweep()
    qt.msleep(0.1)


    amp, phase = vna.get_traces( ('trace1',))[0]

    stop_time = datetime.now()
    probe_src.set_status('off')
    vna.set_status('off')
    qt.mend()

    print "twotone sweep done in: ", (stop_time -start_time).total_seconds(), 's'
    return [amp, phase]

#######################
filename = 'VNA_Twotone_vs_Flux_Adaptive_trace' #Filename that will be used to name the data folder. Use script filename.
file_dir = '' #File directory. It has the form working_directory\file_dir\filename


cur_start =  -3e-3 #Ampere
cur_stop  =  3e-3
cur_step  =  0.05e-3


window = 0.7    # [GHz]
freqs_min = [6.0] #np.arange(2.5, 3.001, window)    # [GHz]

for fq_min in freqs_min:
    smb_second_tone_params = {
                    'f_min'     : fq_min, #[GHz]
                    'f_max'     : fq_min+window, #[GHz]
                    'f_step'    : 1e-3, #[GHz]
                    'power'     : -0    #[dBm] # 10
                    }

    vna_probe_tone_params = {
                    'cwfreq'    : None, #[Hz] #will be defined automatically
                    'bandwidth' : 50,  #[Hz]
                    'averages'  : 1,
                    'power'     : -15    #[dBm]
                    }

    #4 sec on this sweep [501 points, bw200, av=1]
    vna_scanforresonance_params = { ##less points, better bandwidth ->stable freq (1Mhz resolution is more than enough)
                    'freq_start' : 7.1e9, #[Hz]
                    'freq_stop'  : 7.3e9, #[Hz]
                    'points'     : 501,
                    'bandwidth'  : 100,  #[Hz]
                    'averages'   : 1,
                    'power'      : vna_probe_tone_params['power'] #better always to use same power here
                    }

    ################################################################################

    current_source = qt.instruments.get('b2902a')
    # current_source.set_mode('dci')
    # current_source.set_channel('A')
    # current_source.set_resolution('high')

    full_start_time = datetime.now()

    data = qt.Data( name=str(filename) ) #Do not change filename. Include comments as 'filename + str(comments)'
    data.add_coordinate('current [mA]', units='mA')
    data.add_coordinate('VNA CW Frequency [GHz]', units='GHz')
    data.add_coordinate('SMB frequency [GHz]', units='GHz')
    data.add_value('S_21 [dB]',   units='dB')
    data.add_value('Phase [deg]', units='deg')
    data.create_file()

    plot2d_1 = qt.Plot2D(data, name='last_VNA_twotone_trace_amp',   coorddim=2, valdim=3, maxtraces=2)
    plot2d_2 = qt.Plot2D(data, name='last_VNA_twotone_trace_phase', coorddim=2, valdim=4, maxtraces=2)
    plot3d_1 = qt.Plot3D(data, name='VNA_twotone_trace_amp_vs_flux',           coorddims=(0,2), valdim=3, style='image')
    plot3d_2 = qt.Plot3D(data, name='VNA_twotone_trace_phase_vs_flux',        coorddims=(0,2), valdim=4, style='image')
    plot3d_1.set_palette('bluewhitered')
    plot3d_2.set_palette('bluewhitered')


    count = 0
    try:
        stored_current_value = current_source.get_current()
        # current_source.set_current(cur_start)
        go_to_current( current_source, cur_start)
        current_source.on()
        curr_vec = np.arange(cur_start, cur_stop +cur_step, cur_step)

        for cur in curr_vec:
            # current_source.set_current(cur)
            go_to_current( current_source, cur)
            print 'current=', round(1e3*cur, 4), 'mA  count:', count, '/', len(curr_vec)
            [amp1, phase1] = anritsu_onetone_trace(vna_scanforresonance_params)
            freqs1 = np.linspace(vna_scanforresonance_params['freq_start'],
                                vna_scanforresonance_params['freq_stop'],
                                vna_scanforresonance_params['points'])

            cwfreq = freqs1[ np.argmax(amp1) ]  ###here can be upgraded by fiting the lorentzian #[GHz]
            cwfreq += 0.01e6 # shift freq a bit from the resonance to have bigger derivative
            vna_probe_tone_params['cwfreq'] = cwfreq*1e-9
            print 'cw freq: ', round(cwfreq*1e-9, 4), "GHz"

            print 'current=', round(1e3*cur, 4), 'mA  count:', count, '/', len(curr_vec)
            [amp2, phase2] = anritsu_twotone_trace_vs_smb(vna_probe_tone_params, smb_second_tone_params)
            freqs2 = np.arange(  smb_second_tone_params['f_min'],
                                smb_second_tone_params['f_max'] +smb_second_tone_params['f_step'],
                                smb_second_tone_params['f_step'])

            data.add_data_point( 1e3*cur*np.ones_like(freqs2), cwfreq*np.ones_like(freqs2), freqs2, amp2, phase2)
            data.new_block()
            count +=1

        go_to_current( current_source, stored_current_value)

    except Exception as error:
        print str(error)

    finally:
        data.close_file()
        data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.
        print 'cw freq was: ', round(cwfreq*1e-9, 4), "GHz"
        print 'current=', round(1e3*cur, 4), 'mA  count:', count, '/', len(curr_vec)

        plot2d_1.save_png()
        plot2d_2.save_png()
        plot3d_1.save_png()
        plot3d_2.save_png()


full_stop_time = datetime.now()
print "Script done in: ", (full_stop_time -full_start_time).total_seconds(), 's'

try:
    shutil.copy(file_dir+filename+'.py',data_dir+'\\'+filename+'.py') #Copy of the script
except IOError:
    print 'Error saving the copy of the script'
