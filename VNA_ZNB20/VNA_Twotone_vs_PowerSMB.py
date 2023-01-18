# -*- coding: utf-8 -*-

import qt
import numpy as np
import shutil
from datetime import datetime

tot_start_time = datetime.now()

def anritsu_twotone_trace_vs_smb(cwfreq, vna_params, smb_second_tone_params):
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

    vna = qt.instruments.get('vna znb20') #Anritsu or ZNB20
    vna.initialize_two_tone_spectroscopy(('trace1',),('S21',))
    vna.set_cwfrequency(cwfreq)
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


    [amp, phase] = vna.get_traces( ('trace1',))[0]
    qt.msleep(0.5)

    stop_time = datetime.now()
    probe_src.set_status('off')
    vna.set_status('off')
    qt.mend()

    print "twotone sweep done in: ", (stop_time -start_time).total_seconds(), 's'
    return [amp, phase]

window = 0.5    # [GHz]
freqs_min = [3.] #np.arange(2., 3.5001, window)    # [GHz]

for fq_min in freqs_min:
    filename = 'VNA_Twotone_vs_SMB_Power' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename


    vna_probe_params = {
                    'cwfreq'    : 7.239, #7.2331, #[GHz] #6.637
                    'bandwidth' : 100,  #[Hz]
                    'averages'  : 1,
                    'power'     : -15    #[dBm]
                    }
    smb_params = {
                    'f_min'     : fq_min, #[GHz]
                    'f_max'     : fq_min+window, #[GHz]
                    'f_step'    : 0.5e-3, #[GHz]
                    'power'     : 0    #[dBm]
                    }

    pow_min = -20 #[dBm]
    pow_max = 0   #[dBm]
    pow_step = 5  #[dBm]

    data = qt.Data( name=str(filename) ) #Do not change filename. Include comments as 'filename + str(comments)'
    data.add_coordinate('SMB Power', units='dBm')
    data.add_coordinate('SMB frequency [GHz]', units='GHz')
    data.add_value('S_21 [dB]',   units='dB')
    data.add_value('Phase [deg]', units='deg')
    data.create_file()

    plot2d_1 = qt.Plot2D(data, name='last_VNA_twotone_trace_amp',   coorddim=1, valdim=2, maxtraces=2)
    plot2d_2 = qt.Plot2D(data, name='last_VNA_twotone_trace_phase', coorddim=1, valdim=3, maxtraces=2)
    plot3d_1 = qt.Plot3D(data, name='VNA_twotone_trace_amp_vs_SMB_power',           coorddims=(0,1), valdim=2, style='image')
    plot3d_2 = qt.Plot3D(data, name='VNA_twotone_trace_phase_vs_SMB_power',        coorddims=(0,1), valdim=3, style='image')
    plot3d_1.set_palette('bluewhitered')
    plot3d_2.set_palette('bluewhitered')


    freqs = np.arange(  smb_params['f_min'],
                        smb_params['f_max'] +smb_params['f_step'],
                        smb_params['f_step'])

    pow2_vec = np.arange(   pow_min,
                            pow_max+pow_step,
                            pow_step)

    try:
        for pow2 in pow2_vec:
            smb_params['power'] = pow2
            [amp, phase] = anritsu_twotone_trace_vs_smb(vna_probe_params['cwfreq'], vna_probe_params, smb_params)
            qt.msleep(0.5)
            print "Measurement done"
            data.add_data_point(
                                pow2*np.ones_like(freqs),
                                freqs,
                                amp,
                                phase
                                )
            data.new_block()
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
        plot3d_1.save_png()
        plot3d_2.save_png()


tot_stop_time = datetime.now()
print "all script is done in: ", (tot_stop_time -tot_start_time).total_seconds(), 's'
