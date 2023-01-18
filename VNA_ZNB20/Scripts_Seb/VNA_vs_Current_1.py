# -*- coding: utf-8 -*-
import qt
import numpy as np
import shutil
import glob as glob

ref = True 

###########################################################
#
#
# Sweep and measurement parameters
#
#
###########################################################



#Number of points (int) [Sample]
points = 2000

#Import the frequency/current files 

fnames = glob.glob('windows\\w_1\\f_vec_' + '*')
print fnames 
c_vec = np.array([fnames[k].replace('windows\\w_1\\f_vec_', '') for k in xrange(len(fnames))])
c_vec = np.array([np.float(c_vec[k].replace('.dat', '')) for k in xrange(len(fnames))])

idx_order = np.argsort(c_vec)[::-1]
c_vec = c_vec[idx_order]
fnames = np.array(fnames)[idx_order]


#Detector bandwidth [Hz]
detector_bandwidth = 2# Hz

#Averages [Sample]
averages = 1

#Sweeps
sweeps = averages

#Sparameter
Sparam='S21'


power_vna = -30

#Coil current sweep: start, stop, step, current for reference measurement
# c_start =-5.5e-3 #Ampere
# c_stop  = 8.5e-3
# c_step  = 0.025e-3

# c_ref = 0e-3
# curr_vec = np.arange(c_start,c_stop + c_step, c_step)
curr_vec = c_vec*1e-3

###########################################################
#
#
#               Devices
#
#
###########################################################

znb = qt.instruments.get('znb')
current_source = qt.instruments.get('hp3245a')



###########################################################
#
#
#               ZNB
#
#
###########################################################

znb.initialize_one_tone_spectroscopy(('trace1',),(Sparam,))


znb.set_averages(averages)
znb.set_averagestatus('on')
znb.set_sweeps(sweeps)
znb.set_measBW(detector_bandwidth)
znb.set_points(points)
znb.set_power(power_vna)

znb.averageclear()

###########################################################
#
#
#                      HP3245A
#
#
###########################################################

current_source.set_output_terminal('REAR') #We use the rear ports
current_source.set_mode('dci')
current_source.set_channel('A')
current_source.set_resolution('high')


###########################################################
#
#
#               Experiment
#
#
###########################################################

current_source.on()
qt.msleep(2)
current_source.set_current(0)
qt.msleep(2)

if ref: 
    data_ref = np.loadtxt('reference/ref.dat')
    f_ref = data_ref[:,0]
    S21_ref = data_ref[:,1]
    phase_ref = data_ref[:,2]

for c in xrange(len(curr_vec)): 
    print curr_vec[c]
#We save data
    qt.mstart()
    filename = 'VNA_vs_Current_'+str(curr_vec[c]*1e3)+'_mA' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename
    data = qt.Data(name=filename)

    #We add the coordinate of what is swept
    data.add_coordinate('Current [mA]', units='mA')
    data.add_coordinate('Frequency [GHz]', units='GHz')

    #We add target value that will be read out

    data.add_value('S_21 [dB]', units='dB')
    data.add_value('Phase', units='deg')
    if ref: 
        data.add_value('S_21_corrected [dB]', units='dB')
        data.add_value('Phase_corrected [deg]', units='deg')


    plot2d_1= qt.Plot2D(data, name='last_trace', coorddim=1, valdim=2, maxtraces=2)
    plot2d_2= qt.Plot2D(data, name='last_trace_phase', coorddim=1, valdim=3, maxtraces=2)
    if ref: 
        plot2d_3= qt.Plot2D(data, name='last_trace_corrected', coorddim=1, valdim=4, maxtraces=2)
        plot2d_4= qt.Plot2D(data, name='last_trace_phase_corrected', coorddim=1, valdim=5, maxtraces=2)

    plot3d_1 = qt.Plot3D(data, name='S21_dB', coorddims=(0,1), valdim=2,style='image')
    plot3d_2 = qt.Plot3D(data, name='S21_phase', coorddims=(0,1), valdim=3,style='image')
    plot3d_1.set_palette('bluewhitered')
    plot3d_2.set_palette('bluewhitered')
    if ref:
        plot3d_3 = qt.Plot3D(data, name='S21_dB_normalized', coorddims=(0,1), valdim=4,style='image')
        plot3d_4 = qt.Plot3D(data, name='S21_phase_normalized', coorddims=(0,1), valdim=5,style='image')
        plot3d_3.set_palette('afmhot')
        plot3d_4.set_palette('afmhot')


        #We create a file corresponding to the object data
    data.create_file()
    
    # Importation of the frequency vector 
    freqs = np.array([])
    freq_file = np.loadtxt(fnames[c])
    startfrequency_vec = freq_file[::2]
    stopfrequency_vec = freq_file[1::2]
    for f in xrange(len(startfrequency_vec)):
        freq_tmp = linspace(startfrequency_vec[f],stopfrequency_vec[f],points)
        freqs  = np.concatenate((freqs, freq_tmp))
    
    amp_final = np.array([])
    phase_final = np.array([])
    current_source.set_current(curr_vec[c])
    try:
        for f in xrange(len(startfrequency_vec)):
            print startfrequency_vec[f], stopfrequency_vec[f]
            
            qt.msleep(1)
            znb.set_startfrequency(startfrequency_vec[f]*1e9)
            znb.set_stopfrequency(stopfrequency_vec[f]*1e9)
            qt.msleep(0.1)
            znb.measure()
            amp,phase=znb.get_traces( ('trace1',))[0]
            amp_final = np.concatenate((amp_final, amp))
            phase_final = np.concatenate((phase_final, phase))
        if ref: 
            amp_corr = np.zeros(len(amp_final))
            phase_corr = np.zeros(len(phase_final))
            for k in xrange(len(freqs)):
                index = np.argmin(np.abs(f_ref - freqs[k]))
                amp_corr[k] = amp_final[k] - (S21_ref[index]-40)
                phase_corr[k] = phase_final[k] - phase_ref[index]
            data.add_data_point((curr_vec[c])*np.ones_like(freqs)*1e3,freqs,amp_final,phase_final,amp_corr,phase_corr)
        else: 
            data.add_data_point((curr_vec[c])*np.ones_like(freqs)*1e3,freqs,amp_final,phase_final)
        data.new_block()
    except Exception as error:
        print str(error)
        #We live plot what we record
qt.msleep()
data.close_file()
data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.

plot2d_1.save_png()
plot2d_2.save_png()
plot3d_1.save_png()
plot3d_2.save_png()
plot3d_3.save_png()
plot3d_4.save_png()
current_source.set_current(0)
current_source.off()

znb.set_status('off')
qt.mend()
