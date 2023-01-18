# -*- coding: utf-8 -*-
import qt
import numpy as np
import shutil


filename = 'VNA_vs_VNA_power_standard' #We save the name of the script for the folder name
file_dir = '' #File directory. It has the form working_directory\file_dir\filename
ref = True

#We create the object data
data = qt.Data(name=str(filename))


#Saving a copy of the script
data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.

try:
    shutil.copy(file_dir+filename+'.py',data_dir+'\\'+filename+'.py') #Copy of the script
except IOError:
    print 'Error saving the copy of the script'

###########################################################
#
#
# Sweep and measurement parameters
#
#
###########################################################


#Number of points (int) [Sample]
points = 1000
startfrequency = 7.2e9
#StopFrequency [Hz]
stopfrequency =7.4e9

#Detector bandwidth [Hz]
detector_bandwidth = [10.]# Hz
# detector_bandwidth = np.array([2,2, 4, 10, 100, 100, 100, 100, 100])

#Averages [Sample]
averages = 1

#Sweeps
sweeps = averages

#Sparameter
Sparam='S21'

#Coil current
# I_ref=-0.21385e-3
# I_ref=-1.156e-3
# I_ref=-0.85e-3
# I_ref=-29.7169e-3
# I_ref=-28.75e-3
# I_ref= 0e-3
I_ref = -0.3e-3

#Power Sweep [dBm]: start, stop, step, Power for reference measurement
P_start = -30
P_stop  = 0.
P_step  = 5
P_ref = 0
Power_vec = arange(P_start,P_stop + P_step, P_step)
# Power_vec = np.ones(100)*-10

################################################
#
#            Gate Voltage Parameters
#
################################################


#Reference gate voltage
Vg_ref = 0

###########################################################
#
#
#               Devices
#
#
###########################################################

current_source = qt.instruments.get('hp3245')
znb = qt.instruments.get('vna znb20')
#Vg_source = qt.instruments.get('hp3245a_2')
#probe_src = qt.instruments.get('probe_src')

############################################################
#
#
#       SMB100A
#
#
############################################################

#probe_src.set_status('off')


###########################################################
#
#
#               HP3245A_2 (Voltage source)
#
#
###########################################################

# Vg_source.set_mode('dcv')
# Vg_source.set_channel('A')
# Vg_source.set_resolution('high')

###########################################################
#
#
#               ZNB
#
#
###########################################################

znb.initialize_one_tone_spectroscopy(('trace1',),(Sparam,))

znb.set_startfrequency(startfrequency)
znb.set_stopfrequency(stopfrequency)
znb.set_averages(averages)
znb.set_averagestatus('on')
znb.set_sweeps(sweeps)
znb.set_power(P_ref)
if len(detector_bandwidth) ==1:
    znb.set_measBW(detector_bandwidth)
znb.set_points(points)




###########################################################
#
#
#           HP8245A
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

qt.mstart()

#We create the object data
data = qt.Data(name=str(filename)+'_20dBm')

#We add the coordinate of what is swept
data.add_coordinate('Power [dBm]', units='dBm')
data.add_coordinate('Frequency [GHz]', units='GHz')

#We add target value that will be read out

data.add_value('S_21 [dB]', units='dB')
data.add_value('Phase', units='deg')
if ref:
    data.add_value('S_21_corrected [dB]', units='dB')
    data.add_value('Phase_corrected [deg]', units='deg')

#We live plot what we record

plot2d_1= qt.Plot2D(data, name='last_trace', coorddim=1, valdim=2, maxtraces=2)
plot2d_2= qt.Plot2D(data, name='last_trace_phase', coorddim=1, valdim=3, maxtraces=2)
if ref:
    plot2d_3= qt.Plot2D(data, name='last_trace_corrected', coorddim=1, valdim=4, maxtraces=2)
    plot2d_4= qt.Plot2D(data, name='last_trace_phase_corrected', coorddim=1, valdim=5, maxtraces=2)



plot3d_1 = qt.Plot3D(data, name='S21_dB', coorddims=(0,1), valdim=2,style='image')
plot3d_2 = qt.Plot3D(data, name='S21_phas', coorddims=(0,1), valdim=3,style='image')
if ref:
    plot3d_3 = qt.Plot3D(data, name='S21_dB_normalized', coorddims=(0,1), valdim=4,style='image')
    plot3d_4 = qt.Plot3D(data, name='S21_phase_normalized', coorddims=(0,1), valdim=5,style='image')
plot3d_1.set_palette('bluewhitered')
plot3d_2.set_palette('bluewhitered')
plot3d_3.set_palette('bluewhitered')
plot3d_4.set_palette('bluewhitered')

#We create a file corresponding to the object data
data.create_file()

# Vg_source.on()
# current_source.on()
qt.msleep(1)
current_source.set_current(I_ref)
# Vg_source.set_voltage(Vg_ref)
# znb.set_power(P_ref)

# znb.measure()
if ref:
    data_ref = np.loadtxt('reference/ref.dat')
    f_ref = data_ref[:,0]
    S21_ref = data_ref[:,1]
    phase_ref = data_ref[:,2]

freqs=linspace(startfrequency,stopfrequency,points)/1.0e9
try:
    for p in xrange(len(Power_vec)):
        if len(detector_bandwidth) !=1:
            znb.set_measBW(detector_bandwidth[p])
        znb.set_power(Power_vec[p])
        qt.msleep(1)
        znb.averageclear()
        znb.measure()
        amp,phase=znb.get_traces( ('trace1',))[0]
        if ref:
            amp_corr = np.zeros(len(amp))
            phase_corr = np.zeros(len(phase))
            for k in xrange(len(freqs)):
                index = np.argmin(np.abs(f_ref - freqs[k]))
                amp_corr[k] = amp[k] - (S21_ref[index]-40)
                phase_corr[k] = phase[k] - phase_ref[index]
            data.add_data_point((Power_vec[p])*np.ones_like(freqs),freqs,amp,phase,amp_corr,phase_corr)
        else:
            data.add_data_point((Power_vec[p])*np.ones_like(freqs),freqs,amp,phase)

        data.new_block()
except Exception as error:
    print str(error)
finally:
    qt.msleep()
    data.close_file()



    plot3d_1.save_png()
    plot3d_2.save_png()
    plot3d_3.save_png()
    plot3d_4.save_png()


    current_source.set_current(0)
    current_source.off()
    # Vg_source.set_voltage(0)
    # Vg_source.off()
    znb.set_status('off')
    qt.mend()
