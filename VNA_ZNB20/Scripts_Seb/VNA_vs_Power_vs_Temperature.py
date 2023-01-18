# -*- coding: utf-8 -*-
import qt
import numpy as np
import shutil









###########################################################
#
#
# Sweep and measurement parameters
#
#
###########################################################



#Number of points (int) [Sample]
points = 20000

#StartFrequency [Hz]

startfrequency_vec = np.array([2.5])*1e9

stopfrequency_vec = np.array([12])*1e9

#Detector bandwidth [Hz]
detector_bandwidth = 5# Hz

#Averages [Sample]
averages = 1

#Sweeps
sweeps = averages

#Sparameter
Sparam='S21'


#Power Sweep [dBm]: start, stop, step, Power for reference measurement
# P_start = -20
# P_stop  = 0
# P_step  = 10
# P_ref = 0
# Power_vec = arange(P_start,P_stop + P_step, P_step)

Power_vec = np.array([-20])

###############################################
#
#         MMR3 Parameters
#
##############################################


channel_lt = 2

###############################################
#
#         MGC3 Parameters
#
##############################################
#temperature sweep

T_min =25e-3

T_max = 250e-3

T_step = 5e-3
#T_step2 = 100e-3
#T_mid = 500e-3
# Temperature 

# T_vec1 = np.arange(T_min,T_mid+T_step,T_step)
# T_vec2 = np.arange(T_mid+T_step,T_max+T_step2,T_step2)
# T_vec = np.concatenate((T_vec1,T_vec2))
T_vec = np.arange(T_min,T_max+T_step,T_step)
# T_vec = np.concatenate((T_vec_tmp[:-1],T_vec_tmp[::-1]))
w_time = 60*5

P = 5e-3
I = 2e-2
D = 0 
max_Power = 1e-3 

###########################################################
#
#
#               Devices
#
#
###########################################################

znb = qt.instruments.get('znb')

mgc3 = qt.instruments.get('MGC3')

mmr3_LT = qt.instruments.get('MMR3_LT')

###########################################################
#
#
#                      MGC3
#
#
###########################################################
# channel of the MGC3
channel = 1 
# # get the name of the MMR3 at low temperature 
# name = mmr3_lt.get_Head_Name()
# # plug the MGC3 on the MMR3_LT
# mgc3.set_mmr3_Unit(channel,name)
# set the PID 
mgc3.set_P(channel,P)
mgc3.set_I(channel,I)
mgc3.set_D(channel,D)
mgc3.set_max_power(channel,max_Power)
mgc3.set_reg_mode(channel,2)
# initialize the mgc3
mgc3.set_setpoint(channel,0)
mgc3.set_on(channel,1)



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
znb.set_power(P_ref)
znb.set_measBW(detector_bandwidth)
znb.set_points(points)

znb.averageclear()



###########################################################
#
#
#               Experiment
#
#
###########################################################



#We create the object data






 

freqs = np.array([])
for f in xrange(len(startfrequency_vec)):
    freq_tmp = linspace(startfrequency_vec[f],stopfrequency_vec[f],points)/1.0e9
    freqs  = np.concatenate((freqs, freq_tmp))

for t in xrange(len(T_vec)): 
#We save data
    qt.mstart()
    filename = 'VNA_vs_Power_vs_Temperature_'+str(T_vec[t])+'_K' #Filename that will be used to name the data folder. Use script filename.
    file_dir = '' #File directory. It has the form working_directory\file_dir\filename
    data = qt.Data(name=filename)

    #We add the coordinate of what is swept
    data.add_coordinate('Power [dBm]', units='dBm')
    data.add_coordinate('Frequency [GHz]', units='GHz')
    data.add_coordinate('Temperature[K]',units = 'K')

    #We add target value that will be read out

    data.add_value('S_21 [dB]', units='dB')
    data.add_value('Phase', units='deg')

    
    mgc3.set_setpoint(channel,T_vec[t])
        # waiting time before measuring
    qt.msleep(w_time)
       
    T = mmr3_LT.get_Temperature(channel_lt)
    plot2d_1= qt.Plot2D(data, name='last_trace', coorddim=1, valdim=3, maxtraces=2)
    plot2d_2= qt.Plot2D(data, name='last_trace_phase', coorddim=1, valdim=4, maxtraces=2)


    plot3d_1 = qt.Plot3D(data, name='S21_dB', coorddims=(0,1), valdim=3,style='image')
    plot3d_2 = qt.Plot3D(data, name='S21_phase', coorddims=(0,1), valdim=4,style='image')


    plot3d_1.set_palette('bluewhitered')
    plot3d_2.set_palette('bluewhitered')


        #We create a file corresponding to the object data
    data.create_file()
    
    for power in Power_vec:
        amp_final = np.array([])
        phase_final = np.array([])
        try:

    # set the temperature
       
        

         #We save data
            for f in xrange(len(startfrequency_vec)):
            
                znb.set_startfrequency(startfrequency_vec[f])
                znb.set_stopfrequency(stopfrequency_vec[f])
                
                znb.set_power(power)
                qt.msleep(1)
           
                znb.measure()
                
                amp,phase=znb.get_traces( ('trace1',))[0]
                amp_final = np.concatenate((amp_final, amp))
                phase_final = np.concatenate((phase_final, phase))
        except Exception as error:
            print str(error)
        
        data.add_data_point((power)*np.ones_like(freqs),freqs,(T)*np.ones_like(freqs),amp_final,phase_final)
        
        data.new_block()
        #We live plot what we record

    qt.msleep()
    data.close_file()
    data_dir=qt.Data.get_dir(data)           #Where to save the copy of the script.
   
            
  





    plot2d_1.save_png()
    plot2d_2.save_png()

    plot3d_1.save_png()
    plot3d_2.save_png()



znb.set_status('off')
mgc3.set_on(channel,0)
qt.mend()
