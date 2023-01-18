# -*- coding: utf-8 -*-
import qt
import numpy as np
import shutil
from datetime import datetime, timedelta

filename = 'VNA_vs_Time_standard' #We save the name of the script for the folder name
file_dir = 'StandardScripts/' #File directory. It has the form working_directory\file_dir\filename
ref = True   

###########################################################
#
#
# Sweep and measurement parameters
#
#
###########################################################


#Number of points (int) [Sample]
points = 750

#StartFrequency [Hz]
startfrequency =5.75e9

#StopFrequency [Hz]
stopfrequency =  5.95e9

#Power [dBm]
detector_power = -30# dBm

#Detector bandwidth [Hz]
detector_bandwidth = 1# Hz


#Averages [Sample]
averages = 1

#Sweeps
sweeps = averages

#Duration of the measurement [seconds]
meas_time=3600*15

#Sparameter
Sparam='S21'

###############################################
#
#         Coil Current Parameters
#
##############################################

#Reference coil current
c_ref =2.7284e-3


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


znb = qt.instruments.get('znb')
current_source = qt.instruments.get('hp3245a')
# Vg_source = qt.instruments.get('hp3245a_2')
# probe_src = qt.instruments.get('probe_src')

############################################################
#
#
#       SMB100A
#
#
############################################################

# probe_src.set_status('off')


###########################################################
#
#
#               znb
#
#
###########################################################

znb.initialize_one_tone_spectroscopy(('trace1',),(Sparam,))


znb.set_startfrequency(startfrequency)
znb.set_stopfrequency(stopfrequency)
znb.set_averages(averages)
znb.set_averagestatus('on')
znb.set_sweeps(sweeps)
znb.set_power(detector_power)
znb.set_measBW(detector_bandwidth)
znb.set_points(points)

###########################################################
#
#
#                      HP3245A 1 & 2
#
#
###########################################################

# Vg_source.set_mode('dcv')
# Vg_source.set_channel('A')
# Vg_source.set_resolution('high')

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
data = qt.Data(name=filename)

#We add the coordinate of what is sweeped
data.add_coordinate('Time elapsed [s]', units='s')
data.add_coordinate('Frequency [GHz]', units='GHz')

#We add the value that will be read out

data.add_value('S_21 [dB]', units='dB')
data.add_value('Phase [deg]', units='deg')
if ref:
    data.add_value('S_21_corrected', units='dB')
    data.add_value('Phase_corrected', units='rad')


#We live plot what we record


plot2d_1= qt.Plot2D(data, name='last_trace', coorddim=1, valdim=2, maxtraces=2)
plot2d_2= qt.Plot2D(data, name='last_trace_phase', coorddim=1, valdim=3, maxtraces=2)

if ref: 
    plot2d_3= qt.Plot2D(data, name='last_trace_corrected', coorddim=1, valdim=4, maxtraces=2)
    plot2d_4= qt.Plot2D(data, name='last_trace_phase_corrected', coorddim=1, valdim=5, maxtraces=2)


plot3d_1 = qt.Plot3D(data, name='S21_dB', coorddims=(0,1), valdim=2,style='image')
plot3d_2 = qt.Plot3D(data, name='S21_phaqe', coorddims=(0,1), valdim=3,style='image')
plot3d_1.set_palette('bluewhitered')
plot3d_2.set_palette('bluewhitered')

if ref:
    plot3d_3 = qt.Plot3D(data, name='S21_dB_normalized', coorddims=(0,1), valdim=4,style='image')
    plot3d_4 = qt.Plot3D(data, name='S21_phase_normalized', coorddims=(0,1), valdim=5,style='image')
    plot3d_3.set_palette('afmhot')
    plot3d_4.set_palette('afmhot')


#We create a file corresponding to the object data
data.create_file()



current_source.on()
qt.msleep(1)
current_source.set_current(c_ref)

# Vg_source.on()
qt.msleep(0.1)
# Vg_source.set_voltage(Vg_ref)

znb.set_averages(averages)
freqs=linspace(startfrequency,stopfrequency,points)/1.0e9

meas_start=datetime.now()
delta_now=datetime.now()-meas_start
delta_meas=timedelta(seconds=meas_time)

if ref: 
    data_ref = np.loadtxt('reference/ref.dat')
    f_ref = data_ref[:,0]
    S21_ref = data_ref[:,1]
    phase_ref = data_ref[:,2]


try:
    while delta_now < delta_meas:

        znb.averageclear()
        znb.measure()
        qt.msleep(0.1)
        
        delta_now=datetime.now()-meas_start
        amp,phase=znb.get_traces( ('trace1',))[0]
        qt.msleep(0.1)
        #We save data
        
        if ref: 
            amp_corr = np.zeros(len(amp))
            phase_corr = np.zeros(len(phase))
            for k in xrange(len(freqs)):
                index = np.argmin(np.abs(f_ref - freqs[k]))
                amp_corr[k] = amp[k] - (S21_ref[index]-40)
                phase_corr[k] = phase[k] - phase_ref[index]

            data.add_data_point(delta_now.seconds*np.ones_like(freqs),freqs,amp,phase,amp_corr,phase_corr)
        else: 
            data.add_data_point(delta_now.seconds*np.ones_like(freqs),freqs,amp,phase)
        
        
        
        
        
        data.new_block()

except Exception as error:
    print str(error)
finally:
    qt.msleep()
    data.close_file()
    data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.
    try:
        shutil.copy(file_dir+filename+'.py',data_dir+'\\'+filename+'.py') #Copy of the script
    except IOError:
        print 'Error saving the copy of the script'

    plot3d_1.save_png()
    plot3d_2.save_png()

    
    # Vg_source.set_voltage(0)
    # Vg_source.off()
    current_source.set_current(0)
    current_source.off()
    znb.set_status('off')
    qt.mend()
