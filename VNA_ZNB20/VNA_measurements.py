# -*- coding: utf-8 -*-
import qt
import numpy as np
import shutil
from datetime import datetime

smb_1.set_status('off')
smb_2.set_status('off')

current_source = qt.instruments.get('hp3245')
rudat_qubit = qt.instruments.get('RUDAT_comp')

rudat_qubit.set_attenuation(0)

## Default parameters

# Onetone
params_ot = {
                'freq_start' : 8.e9,  #[Hz]
                'freq_stop'  : 8.1e9,  #[Hz]
                'points'     : 501,            ### 501
                'bandwidth'  : 5,         ### 500   #[Hz]
                'averages'   : 64,
                'power'      : -30    #[dBm]
                }

# Onetone vs flux
params_ot_vs_flux = {
                'freq_start' : 7.9e9,  #[Hz]
                'freq_stop'  : 8.1e9,  #[Hz]
                'points'     : 501,
                'bandwidth'  : 5,  #[Hz]
                'averages'   : 16,
                'power'      : -30,    #[dBm]
                'cur_start'  : -1.0e-3,   #[Ampere]
                'cur_stop'   : 1.0e-3,    #[Ampere]
                'cur_step'   : 0.01e-3    #[Ampere]
                }

# Twotones
vna_probe_params = {
                'cwfreq'    : 8.04, #[GHz]
                'bandwidth' : 5,  #[Hz]
                'averages'  : 128,
                'power'     : -30    #[dBm]
                }
smb_params = {
                'f_min'     : 1.6, #[GHz]
                'f_max'     : 1.9, #[GHz]
                'f_step'    : 0.3e-3, #[GHz]
                'power'     : 0    #[dBm]
                }

# Twotones vs flux
smb_second_tone_params = {
                'f_min'     : 1.3, #[GHz]
                'f_max'     : 1.9, #[GHz]
                'f_step'    : 2.e-3, #[GHz]
                'power'     : 0,    #[dBm]
                'cur_start' : -0.7e-3,   #[Ampere]
                'cur_stop'  : 0.3e-3,     #[Ampere]
                'cur_step'  : 0.005e-3    #[Ampere]
                }
vna_probe_tone_params = {
                'cwfreq'    : None, #8.0365, #[GHz] # if None, will be defined automatically
                'bandwidth' : 5,  #[Hz]
                'averages'  : 128,
                'power'     : -30    #[dBm]
                }
# (4s for this sweep [501 points, bw200, av=1])
vna_scanforresonance_params = { ##less points, better bandwidth ->stable freq (1Mhz resolution is more than enough)
                'freq_start' : 8.035e9, #[Hz]
                'freq_stop'  : 8.07e9, #[Hz]
                'points'     : 501,
                'bandwidth'  : 10,  #[Hz]
                'averages'   : 1,
                'power'      : vna_probe_tone_params['power'] #better always to use same power here
                }

# Onetone vs time
ot_vs_time_params = {
                'bandwidth' : 1,  #[Hz]
                'averages'  : 1,
                'power'     : -30,   #[dBm]
                'time_nop'  : 1001,
                ## for 2D plot
                'cwfreq'    : 8.0556 #[GHz]
                }
ot_vs_time3D_params = {
                'bandwidth' : 5,  #[Hz]
                'averages'  : 1,
                'power'     : -30,   #[dBm]
                'points'    : 201,
                'time_nop'  : 10,
                ## for 3D plot
                'freq_start' : 8.035e9,  #[Hz]
                'freq_stop'  : 8.075e9  #[Hz]
                }


# Twotone 3D
params_tt3D_vna = { # takes 17.2s per onetone, using these nop=101, averaging=8 and BW=5
                'freq_start': 8.01e9, #[Hz]
                'freq_stop' : 8.07e9, #[Hz]
                'points'    : 201,
                'bandwidth' : 5,  #[Hz]
                'averages'  : 64,
                'power'     : -30    #[dBm]
                }
params_tt3D_smb = {
                'f_min'     : 1.8, #[GHz]
                'f_max'     : 2., #[GHz]
                'f_step'    : 1.e-3, #[GHz]
                'power'     : 0    #[dBm]
                }


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

def onetone_save(params=params_ot):
    filename = 'VNA_Onetone_trace' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    freqs = np.linspace(params['freq_start'],
                        params['freq_stop'],
                        params['points'])

    # [amp, phase] = znb_onetone_trace(params_dict)


    data = qt.Data(name=str(filename))
    data.add_coordinate('VNA Frequency [GHz]', units='GHz')
    data.add_value('S_21 [dB]',   units='dB')
    data.add_value('Phase [rad]', units='rad')
    data.add_value('Phase unwrapped',            units = 'deg')
    data.create_file()

    plot2d_1= qt.Plot2D(data, name='VNA_onetone_trace_amp', coorddim=0, valdim=1, maxtraces=2)
    plot2d_2= qt.Plot2D(data, name='VNA_onetone_trace_phase_unwraped', coorddim=0, valdim=3, maxtraces=2)

    try:
        [amp, phase] = znb_onetone_trace(params)
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

def onetone_vs_flux_save(params=params_ot_vs_flux):
    filename = 'VNA_Onetone_vs_Flux' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    cur_start =  params['cur_start'] #Ampere
    cur_stop  =  params['cur_stop']
    cur_step  =  params['cur_step']
    # current_source = qt.instruments.get('hp3245') ##for Qubit source
    current_source = qt.instruments.get('hp3245') ## for TWPA source

    freqs = np.linspace(params['freq_start'],
                        params['freq_stop'],
                        params['points'])

    #############################################

    current_source.set_mode('dci')
    current_source.set_channel('A')
    current_source.set_resolution('high')

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
        current_source.on()
        curr_vec = np.arange(cur_start, cur_stop +cur_step, cur_step)
        for cur in curr_vec:
            # current_source.set_current(cur)
            go_to_current( current_source, cur)
            qt.msleep(0.5)
            [ampdB, phase] = znb_onetone_trace(params)
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

def znb_twotone_trace_vs_smb(vna_params, smb_second_tone_params):
    '''
    using ZNB20 as a VNA, and SMB100A as 2nd tone generator
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

    vna = qt.instruments.get('vna znb20') # ZNB20
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
    probe_src.set_sweepmode('single')
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


    [amp, phase] = vna.get_traces( ('trace1',))[0]
    qt.msleep(0.5)

    stop_time = datetime.now()
    probe_src.set_status('off')
    vna.set_status('off')
    qt.mend()

    print "twotone sweep done in: ", (stop_time -start_time).total_seconds(), 's'
    return [amp, phase]

def twotone_save(vna_probe_params=vna_probe_params, smb_params=smb_params):
    tot_start_time = datetime.now()

    #######################
    filename = 'VNA_Twotone_trace' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    data = qt.Data(name=str(filename))
    data.add_coordinate('VNA Frequency [GHz]', units='GHz')
    data.add_coordinate('SMB frequency [GHz]', units='GHz')
    data.add_value('S_21 [dB]', units='dB')
    data.add_value('Phase [deg]', units='deg')
    data.create_file()

    plot2d_1 = qt.Plot2D(data, name='VNA_twotone_trace_amp',   coorddim=1, valdim=2, maxtraces=2)
    plot2d_2 = qt.Plot2D(data, name='VNA_twotone_trace_phase', coorddim=1, valdim=3, maxtraces=2)


    freqs = np.arange(  smb_params['f_min'],
                        smb_params['f_max'] +smb_params['f_step'],
                        smb_params['f_step'])

    try:
        [amp, phase] = znb_twotone_trace_vs_smb(vna_probe_params, smb_params)
        qt.msleep(0.5)
        print "Measurement done"
        data.add_data_point(
                            vna_probe_params['cwfreq']*np.ones_like(freqs),
                            freqs,
                            amp,
                            phase
                            )
        print "Data point added"

    except Exception as error:
        print str(error)
    finally:

        data.close_file()
        print "Data file closed"
        data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.
        try:
            shutil.copy(file_dir+filename+'.py',data_dir+'\\'+filename+'.py') #Copy of the script
        except IOError:
            print 'Error saving the copy of the script'

        plot2d_1.save_png()
        plot2d_2.save_png()

        tot_stop_time = datetime.now()
        print "all script is done in: ", (tot_stop_time -tot_start_time).total_seconds(), 's'

def twotone_vs_flux_save(smb_second_tone_params=smb_second_tone_params, vna_probe_tone_params=vna_probe_tone_params, vna_scanforresonance_params=vna_scanforresonance_params, shift=1.0e6):
    filename = 'VNA_Twotone_vs_Flux_Adaptive_trace' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    cur_start =  smb_second_tone_params['cur_start'] #Ampere
    cur_stop  =  smb_second_tone_params['cur_stop']
    cur_step  =  smb_second_tone_params['cur_step']

    current_source = qt.instruments.get('hp3245')
    current_source.set_mode('dci')
    current_source.set_channel('A')
    current_source.set_resolution('high')

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
            if not vna_probe_tone_params['cwfreq']:
                [amp1, phase1] = znb_onetone_trace(vna_scanforresonance_params)
                freqs1 = np.linspace(vna_scanforresonance_params['freq_start'],
                                    vna_scanforresonance_params['freq_stop'],
                                    vna_scanforresonance_params['points'])

                cwfreq = freqs1[ np.argmax(amp1) ]  ###here can be upgraded by fitting the lorentzian #[GHz]
                cwfreq += shift # shift freq a bit from the resonance to have bigger derivative
                vna_probe_tone_params['cwfreq'] = cwfreq*1e-9
            print 'cw freq: ', round(vna_probe_tone_params['cwfreq'], 4), "GHz"

            print 'current=', round(1e3*cur, 4), 'mA  count:', count, '/', len(curr_vec)
            [amp2, phase2] = znb_twotone_trace_vs_smb(vna_probe_tone_params, smb_second_tone_params)
            freqs2 = np.arange(  smb_second_tone_params['f_min'],
                                smb_second_tone_params['f_max'] +smb_second_tone_params['f_step'],
                                smb_second_tone_params['f_step'])

            data.add_data_point( 1e3*cur*np.ones_like(freqs2), vna_probe_tone_params['cwfreq']*np.ones_like(freqs2), freqs2, amp2, phase2)
            data.new_block()
            count +=1

        go_to_current( current_source, stored_current_value)

    except Exception as error:
        print str(error)

    finally:
        data.close_file()
        data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.
        print 'cw freq was: ', round(vna_probe_tone_params['cwfreq']*1e-9, 4), "GHz"
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

def twotone3D_save(vna_params=params_tt3D_vna, smb_params=params_tt3D_smb):
    filename = 'VNA_Twotone3D' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    freqs_tone1 = np.linspace(vna_params['freq_start'],
                        vna_params['freq_stop'],
                        vna_params['points'])

    freqs_tone2 = np.arange(  smb_params['f_min'],
                        smb_params['f_max'] +smb_params['f_step'],
                        smb_params['f_step'])

    #dwell time security time [ms]: to ensure the SMA is not sweeping too fast compared to the VNA capabilities
    DTsecurity = 100 #[ms]
    #dwell time of the frequency sweep [ms]
    dwelltime = 1./vna_params['bandwidth']*1000 +DTsecurity

    #############################################

    probe_src = qt.instruments.get('smb_2') ##SMB100A
    probe_src.set_power(smb_second_tone_params['power'])
    probe_src.set_freqsweep('off')
    probe_src.set_dwelltime(dwelltime)
    probe_src.set_status('off')

    full_start_time = datetime.now()

    data = qt.Data(name=str(filename)) #Do not change filename. Include comments as 'filename + str(comments)'
    data.add_coordinate('SMB Frequency [GHz]', units='GHz')
    data.add_coordinate('VNA Frequency [GHz]', units='GHz')
    data.add_value('S_21 [dB]', units='dB')
    data.add_value('Phase [deg]', units='rad')
    data.add_value('Phase unwrapped', units = 'deg')
    data.create_file()

    plot2d_1= qt.Plot2D(data, name='trace_amp',     coorddim=1, valdim=2, maxtraces=2)
    plot2d_2= qt.Plot2D(data, name='trace_phase',   coorddim=1, valdim=3, maxtraces=2)
    plot3d_1= qt.Plot3D(data, name='S21',   coorddim=(0,1), valdim=2)
    plot3d_2= qt.Plot3D(data, name='phase', coorddim=(0,1), valdim=4)

    probe_src.set_status('on')

    try:
        for f_q in freqs_tone2:
            probe_src.set_frequency(f_q*1e9)
            qt.msleep(0.5)
            [ampdB, phase] = znb_onetone_trace(vna_params)
            phase_unwrap = np.unwrap(phase)
            data.add_data_point( f_q*np.ones_like(freqs_tone1), freqs_tone1, ampdB, phase, phase_unwrap )
            data.new_block()

    except Exception as error:
        print str(error)

    finally:
        data.close_file()
        plot2d_1.save_png()
        plot2d_2.save_png()
        plot3d_1.save_png()
        plot3d_2.save_png()
        qt.mend()

        probe_src.set_status('off')
        full_stop_time = datetime.now()
        print "Script done in: ", (full_stop_time -full_start_time).total_seconds(), 's'

def onetone_vs_time2D_save(params=ot_vs_time_params):
    def measure_ot_vs_time2D(vna_params=params):
        '''
        using ZNB20 as a VNA
        takes dictionary of VNA Parameters
        returns list: [time_ndarray, amp_ndarray, phase_ndarray]
        '''
        points = params['time_nop']
        time = np.arange(points)

        #dwell time security time [ms]: to ensure the SMA is not sweeping too fast compared to the VNA capabilities
        DTsecurity = 100 #[ms]
        #dwell time of the frequency sweep [ms]
        dwelltime = 1./vna_params['bandwidth']*1000 +DTsecurity

        vna = qt.instruments.get('vna znb20') # ZNB20
        vna.initialize_two_tone_spectroscopy(('trace1',),('S21',))
        vna.set_cwfrequency(vna_params['cwfreq'])
        vna.set_averages(vna_params['averages'])
        vna.set_averagestatus('on')
        vna.set_power(vna_params['power'])
        # vna.set_port2_power(vna_params['power'])
        vna.set_measBW(vna_params['bandwidth'])
        vna.set_points(points)
        vna.set_trigger('IMM')

        vna.set_status('on')
        vna.averageclear()

        # print "expected measurement time is:", round(len(points) *vna_params['bandwidth'] *vna_params['averages'] ), "sec"
        print "dwelltime = ", dwelltime, " ms"
        print "expected measurement time is:", round(  1e-3*(dwelltime *points ) ), "sec"

        start_time = datetime.now()
        qt.mstart()
        qt.msleep(0.1)

        vna.averageclear()
        vna.measure()
        qt.msleep(0.1)

        [amp, phase] = vna.get_traces( ('trace1',))[0]
        qt.msleep(0.5)

        stop_time = datetime.now()
        vna.set_status('off')
        qt.mend()

        print "onetone sweep done in: ", (stop_time -start_time).total_seconds(), 's'
        real_time = time*(stop_time -start_time).total_seconds()*1.0/points

        return [real_time, amp, phase]

    freq = params['cwfreq']
    filename = 'VNA_Onetone_vs_time_trace_at{:.1f}GHz'.format(freq) #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    data = qt.Data(name=str(filename))
    data.add_coordinate('Time [s]', units='s')
    data.add_value('S_21 [dB]',   units='dB')
    data.add_value('Phase [rad]', units='rad')
    data.add_value('Phase unwrapped',            units = 'deg')
    data.create_file()

    plot2d_1= qt.Plot2D(data, name='VNA_onetone_trace_amp_at{:.1f}GHz'.format(freq), coorddim=0, valdim=1, maxtraces=2)
    plot2d_2= qt.Plot2D(data, name='VNA_onetone_trace_phase_unwraped_at{:.1f}GHz'.format(freq), coorddim=0, valdim=3, maxtraces=2)

    try:
        [time, amp, phase] = measure_ot_vs_time2D(params)
        phase_unwrap = np.unwrap(phase)

        data.add_data_point( time, amp, phase, phase_unwrap)

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

def onetone_vs_time3D_save(params=ot_vs_time3D_params):
    filename = 'VNA_Onetone_vs_time_trace_{:.1f}-{:.1f}GHz'.format(params['freq_start']/1e9, params['freq_stop']/1e9) #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    freqs = np.linspace(params['freq_start'],
                        params['freq_stop'],
                        params['points'])
    point_vec = np.arange(params['time_nop'])
    time_vec = np.zeros(len(point_vec))

    data = qt.Data(name=str(filename))
    data.add_coordinate('Time [s]', units='s')
    data.add_coordinate('VNA Frequency [GHz]', units='GHz')
    data.add_value('S_21 [dB]',   units='dB')
    data.add_value('Phase [rad]', units='rad')
    data.add_value('Phase unwrapped',            units = 'deg')
    data.create_file()

    plot2d_1= qt.Plot2D(data, name='trace_amp',     coorddim=1, valdim=2, maxtraces=2)
    plot2d_2= qt.Plot2D(data, name='trace_phase',   coorddim=1, valdim=4, maxtraces=2)
    plot3d_1= qt.Plot3D(data, name='S21 vs time',   coorddim=(0,1), valdim=2)
    plot3d_2= qt.Plot3D(data, name='phase vs time', coorddim=(0,1), valdim=4)

    full_start_time = datetime.now()
    try:
        for point in point_vec:
            qt.msleep(0.5)
            [ampdB, phase] = znb_onetone_trace(params)
            phase_unwrap = np.unwrap(phase)
            time = (datetime.now()-full_start_time).total_seconds()
            data.add_data_point( time*np.ones_like(freqs), freqs, ampdB, phase, phase_unwrap )
            data.new_block()

    except Exception as error:
        print str(error)

    finally:
        data.close_file()
        plot2d_1.save_png()
        plot2d_2.save_png()
        plot3d_1.save_png()
        plot3d_2.save_png()
        qt.mend()

        full_stop_time = datetime.now()
        print "Script done in: ", (full_stop_time -full_start_time).total_seconds(), 's'



#########          ##########
#########   MAIN   ##########
#########          ##########

# # Onetone_vs_flux vs polariton
# params_ot_vs_flux['freq_start'] = 7.9e9
# params_ot_vs_flux['freq_stop'] = 8.1e9
# onetone_vs_flux_save()
# params_ot_vs_flux['freq_start'] = 7.14e9
# params_ot_vs_flux['freq_stop'] = 7.18e9
# onetone_vs_flux_save()


# # Twotone vs time
# current_source = qt.instruments.get('hp3245')
# go_to_current(current_source, 0.e-3)
# f_start_vec = np.arange(1., 5., 0.5)
#
# for f_start in f_start_vec:
#     f_end = f_start + 0.5
#     smb_params['f_min'] = f_start
#     smb_params['f_max'] = f_end
#
#     n = 20
#     for i in range(n):
#         twotone_save()


## Twotones vs power

# fread_vec = [7.166, 8.0563]
# pow_vec = np.arange(-20, 0.01, 5)
# f_start_vec = np.arange(1., 5., 0.5)
#
# for fread in fread_vec:
#     vna_probe_params['cwfreq'] = fread
#     for pow in pow_vec:
#         smb_params['power'] = pow
#         for f_start in f_start_vec:
#             f_end = f_start + 0.5
#             smb_params['f_min'] = f_start
#             smb_params['f_max'] = f_end
#             print(vna_probe_params)
#             print(smb_params)
#             twotone_save()

# fmin_list = np.arange(1.5, 5., 0.5)
#
# for f_start in fmin_list:
#     f_end = f_start + 0.5
#     params_tt3D_smb['f_min'] = f_start
#     params_tt3D_smb['f_max'] = f_end
#
#     twotone3D_save()

# onetone_vs_time2D_save()
# onetone_vs_time3D_save()
#
# chi = -14e6   # [Hz]
#
# twotone_vs_flux_save(shift=chi)



# go_to_current(current_source, -0.6e-3)
#
# pow2_vec = np.arange(-15, 0.001, 5.)
# rdt_vec = np.arange(30, -0.001, -5)
#
# freq_vec = [1.36e9, 1.6e9]
#
# smb_2.set_status('on')
#
# for freq in freq_vec:
#     smb_2.set_frequency(freq)
#     smb_2.set_power(-20)
#
#     for rdt in rdt_vec: # power of SMB is always -20dBm
#         rudat_qubit.set_attenuation(rdt)
#         for i in range(20):
#             onetone_save()
#
#     for pow2 in pow2_vec:   # Rudat attenuation is always 0dB
#         smb_2.set_power(pow2)
#         for i in range(20):
#             onetone_save()
#
# smb_2.set_power(0)
# rudat_qubit.set_attenuation(0)
#
# for freq in freq_vec:
#     smb_2.set_frequency(freq)
#     onetone_vs_flux_save()
#
# smb_2.set_status('off')
#
# go_to_current(current_source, -0.6e-3)
# twotone3D_save()


# go_to_current(current_source, -0.13e-3)
# pow_vec = np.arange(-80, -29, 10)
#
# for pow in pow_vec:
#     params_ot['power'] = pow
#
#     n = 20
#     for i in range(n):
#         onetone_save()
