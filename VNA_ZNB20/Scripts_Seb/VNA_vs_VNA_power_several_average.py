# -*- coding: utf-8 -*-
import qt
import numpy as np
import shutil


filename = 'VNA_vs_VNA_power_standard' #We save the name of the script for the folder name
file_dir = '' #File directory. It has the form working_directory\file_dir\filename

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
points = 250

#StartFrequency [Hz]
startfrequency =2.5e9
#StopFrequency [Hz]
stopfrequency =3e9

#Detector bandwidth [Hz]
detector_bandwidth_vec = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]) # Hz

#Averages [Sample]
averages_vec = np.array([15,12,8,5,2,1,1,1,1,1,1,1,1,1,1])

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
I_ref= 0e-3

#Power Sweep [mW]: start, stop, step, Power for reference measurement
P_start = -30
P_stop =  0
P_point = 15
# [mW]
p_start = 10**(P_start/10)
p_stop  = 10**(P_stop/10)


# Power_vec = 10*np.log10(np.linspace(p_start,p_stop,P_point))

Power_vec = np.linspace(P_start,P_stop,P_point)

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

current_source = qt.instruments.get('hp3245a')
znb = qt.instruments.get('znb')
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
znb.set_averagestatus('on')
# znb.set_power(P_ref)

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
data.add_value('S_21_normalized [dB]', units='dB')
data.add_value('Phase_normalized', units='deg')

#We live plot what we record

plot2d_1= qt.Plot2D(data, name='last_trace', coorddim=1, valdim=2, maxtraces=2)
plot2d_2= qt.Plot2D(data, name='last_trace_phase', coorddim=1, valdim=3, maxtraces=2)


plot3d_1 = qt.Plot3D(data, name='S21_dB', coorddims=(0,1), valdim=2,style='image')
plot3d_2 = qt.Plot3D(data, name='S21_phase', coorddims=(0,1), valdim=3,style='image')
plot3d_3 = qt.Plot3D(data, name='S21_dB_normalized', coorddims=(0,1), valdim=4,style='image')
plot3d_4 = qt.Plot3D(data, name='S21_phase_normalized', coorddims=(0,1), valdim=5,style='image')
plot3d_1.set_palette('bluewhitered')
plot3d_2.set_palette('bluewhitered')
plot3d_3.set_palette('bluewhitered')
plot3d_4.set_palette('bluewhitered')

#We create a file corresponding to the object data
data.create_file()

# Vg_source.on()
current_source.on()
qt.msleep(1)
current_source.set_current(I_ref)
# Vg_source.set_voltage(Vg_ref)
# znb.set_power(P_ref)

# znb.measure()
# ref_amp,ref_phase=znb.get_traces( ('trace1',))[0]
ref_amp,ref_phase=[0,0]

freqs=linspace(startfrequency,stopfrequency,points)/1.0e9
try:
    for p in xrange(len(Power_vec)):
        znb.set_measBW(detector_bandwidth_vec[p])
        znb.set_power(Power_vec[p])
        znb.set_averages(averages_vec[p])
        znb.set_sweeps(averages_vec[p])
        qt.msleep(1)
        znb.averageclear()
        znb.measure()
        amp,phase=znb.get_traces( ('trace1',))[0]
        amp_norm=amp - ref_amp
        phase_norm=phase - ref_phase 
        #We save data
        data.add_data_point((Power_vec[p])*np.ones_like(freqs),freqs,amp,phase,amp_norm,phase_norm)
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
