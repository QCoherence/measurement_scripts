# -*- coding: utf-8 -*-

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

window = 0.1    # [GHz]
freqs_min = np.arange(1., 6.001, window)    # [GHz]

for fq_min in freqs_min:
    ############################################
    filename = 'VNA_Twotone_3D' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename

    vna_params = {
                    'freq_start' : 7.2e9,  #[Hz]
                    'freq_stop'  : 7.3e9,  #[Hz]
                    'points'     : 501,
                    'bandwidth'  : 20,  #[Hz]
                    'averages'   : 1,
                    'power'      : -15    #[dBm]
                    }

    smb_params = {
                    'f_min'     : fq_min, #1.5, #[GHz]
                    'f_max'     : fq_min+window, #1.6, #[GHz]
                    'f_step'    : 0.5e-3, #[GHz]
                    'power'     : 10    #[dBm]
                    }

    freqs = np.linspace(vna_params['freq_start'],
                        vna_params['freq_stop'],
                        vna_params['points'])

    freq_q_vec = np.arange(smb_params['f_min'],
                            smb_params['f_max'] +smb_params['f_step'],
                            smb_params['f_step'])

    #############################################

    full_start_time = datetime.now()


    probe_src = qt.instruments.get('smb_2') ##SMB100A
    probe_src.set_power(smb_params['power'])
    probe_src.set_freqsweep('off')

    data = qt.Data(name=str(filename)) #Do not change filename. Include comments as 'filename + str(comments)'
    data.add_coordinate('Qubit frequency [GHz]', units='GHz')
    data.add_coordinate('Readout frequency [GHz]', units='GHz')
    data.add_value('S_21 [dB]', units='dB')
    data.add_value('Phase [deg]', units='deg')
    data.create_file()

    plot2d_1= qt.Plot2D(data, name='trace_amp',     coorddim=1, valdim=2, maxtraces=2)
    plot2d_2= qt.Plot2D(data, name='trace_phase',   coorddim=1, valdim=3, maxtraces=2)
    plot3d_1= qt.Plot3D(data, name='S21 vs qubit freq, readout freq',   coorddim=(0,1), valdim=2)
    plot3d_2= qt.Plot3D(data, name='Phase vs qubit freq, readout freq', coorddim=(0,1), valdim=3)


    try:
        for freq_q in freq_q_vec:
            probe_src.set_frequency(freq_q*1e9)
            probe_src.set_status('on')
            probe_src.restartsweep()
            qt.msleep(0.5)
            [ampdB, phase] = anritsu_onetone_trace(vna_params)
            data.add_data_point( freq_q*np.ones_like(freqs), freqs*1e-9, ampdB, phase )
            data.new_block()

            probe_src.set_status('off')

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














# SLOW VERSION

#
#
# tot_start_time = datetime.now()
#
# def anritsu_twotone_trace_vs_smb(cwfreq, vna_params, smb_second_tone_params):
#     '''
#     using Anritsu as a VNA, and SMB100A as 2nd tone generator
#     takes dictionary of VNA Parameters, dict of SMB parameters
#     returns list: [amp_ndarray, phase_ndarray]
#     '''
#     freqs=np.arange( smb_second_tone_params['f_min'],
#                      smb_second_tone_params['f_max'] +smb_second_tone_params['f_step'],
#                      smb_second_tone_params['f_step'] )
#     points = len(freqs)
#
#     #dwell time security time [ms]: to ensure the SMA is not sweeping too fast compared to the VNA capabilities
#     DTsecurity = 100 #[ms]
#     #dwell time of the frequency sweep [ms]
#     dwelltime = 1./vna_params['bandwidth']*1000 +DTsecurity
#
#     vna = qt.instruments.get('vna znb20') #Anritsu or ZNB20
#     vna.initialize_two_tone_spectroscopy(('trace1',),('S21',))
#     vna.set_cwfrequency(cwfreq)
#     vna.set_averages(vna_params['averages'])
#     vna.set_averagestatus('on')
#     vna.set_power(vna_params['power'])
#     # vna.set_port2_power(vna_params['power'])
#     vna.set_measBW(vna_params['bandwidth'])
#     vna.set_points(points)
#     vna.set_trigger('EXT')
#
#     probe_src = qt.instruments.get('smb_2') ##SMB100A
#     probe_src.set_power(smb_second_tone_params['power'])
#     probe_src.set_freqsweep('on')
#     probe_src.set_dwelltime(dwelltime)
#     # probe_src.set_sweepmode('single')
#     probe_src.set_sweepmode('auto')
#     probe_src.set_startfreq(smb_second_tone_params['f_min']-smb_second_tone_params['f_step']) #hack to take into account that the first frequency point of probe_src doesn't send a trigger to the VNA
#     probe_src.set_stopfreq(smb_second_tone_params['f_max'])
#     probe_src.set_stepfreq(smb_second_tone_params['f_step'])
#     probe_src.set_pointsfreq(points+1)
#
#     # print "expected measurement time is:", round(len(points) *vna_params['bandwidth'] *vna_params['averages'] ), "sec"
#     print "dwelltime = ", dwelltime, " ms"
#     print "expected measurement time is:", round(  1e-3*(dwelltime *len(freqs) ) ), "sec"
#
#     start_time = datetime.now()
#     qt.mstart()
#     qt.msleep(0.1)
#
#     probe_src.set_status('on')
#     probe_src.restartsweep()
#     qt.msleep(0.1)
#
#     vna.averageclear()
#     vna.measure()
#     qt.msleep(0.1)
#
#     probe_src.startsweep()
#     qt.msleep(0.1)
#
#
#     [amp, phase] = vna.get_traces( ('trace1',))[0]
#     qt.msleep(0.5)
#
#     stop_time = datetime.now()
#     probe_src.set_status('off')
#     vna.set_status('off')
#     qt.mend()
#
#     print "twotone sweep done in: ", (stop_time -start_time).total_seconds(), 's'
#     return [amp, phase]
#
# window = 0.1    # [GHz]
# freqs_min = np.arange(2.92, 2.98, window)    # [GHz]
#
# # for fq_min in freqs_min:
# #######################
# filename = 'VNA_Twotone_trace' #Filename that will be used to name the data folder. Use script filename.
# file_dir = '' #File directory. It has the form working_directory\file_dir\filename
#
#
# vna_params = {
#                 'freq_start' : 7.23,  #[Hz]
#                 'freq_stop'  : 7.25,  #[Hz]
#                 'freq_step'  : 5e-3,     #[Hz]
#                 'points'     : 101, # for the onetone spectroscopy
#                 'bandwidth'  : 1000,  #[Hz]
#                 'averages'   : 1,
#                 'power'      : -15    #[dBm]
#                 }
# smb_params = {
#                 'f_min'     : 1.5, #fq_min, #[GHz]
#                 'f_max'     : 1.6, #fq_min+window, #[GHz]
#                 'f_step'    : 0.5e-3, #[GHz]
#                 'power'     : 0    #[dBm]
#                 }
#
# data = qt.Data( name=str(filename) ) #Do not change filename. Include comments as 'filename + str(comments)'
# data.add_coordinate('VNA Readout Frequency [GHz]', units='GHz')
# data.add_coordinate('SMB frequency [GHz]', units='GHz')
# data.add_value('S_21 [dB]',   units='dB')
# data.add_value('Phase [deg]', units='deg')
# data.create_file()
#
# plot2d_1 = qt.Plot2D(data, name='last_VNA_twotone_trace_amp',   coorddim=1, valdim=2, maxtraces=2)
# plot2d_2 = qt.Plot2D(data, name='last_VNA_twotone_trace_phase', coorddim=1, valdim=3, maxtraces=2)
# plot3d_1 = qt.Plot3D(data, name='VNA_twotone_trace_amp_vs_readout_freq',           coorddims=(0,1), valdim=2, style='image')
# plot3d_2 = qt.Plot3D(data, name='VNA_twotone_trace_phase_vs_readout_freq',        coorddims=(0,1), valdim=3, style='image')
# plot3d_1.set_palette('bluewhitered')
# plot3d_2.set_palette('bluewhitered')
#
#
# freqs = np.arange(  smb_params['f_min'],
#                     smb_params['f_max'] +smb_params['f_step'],
#                     smb_params['f_step'])
#
# freqs_readout = np.linspace(    vna_params['freq_start'],
#                                 vna_params['freq_stop'],
#                                 vna_params['points'])
#
# try:
#     for cwfreq in freqs_readout:
#         [amp, phase] = anritsu_twotone_trace_vs_smb(cwfreq, vna_params, smb_params)
#         qt.msleep(0.5)
#         print "Measurement done"
#         data.add_data_point(
#                             cwfreq*np.ones_like(freqs),
#                             freqs,
#                             amp,
#                             phase
#                             )
#         data.new_block()
#         print "Data point added"
#
# except Exception as error:
#     print str(error)
# finally:
#
#     data.close_file()
#     print "Data file closed"
#     data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.
#     try:
#         shutil.copy(file_dir+filename+'.py',data_dir+'\\'+filename+'.py') #Copy of the script
#     except IOError:
#         print 'Error saving the copy of the script'
#
#     plot2d_1.save_png()
#     plot2d_2.save_png()
#     plot3d_1.save_png()
#     plot3d_2.save_png()
#
#
# tot_stop_time = datetime.now()
# print "all script is done in: ", (tot_stop_time -tot_start_time).total_seconds(), 's'
