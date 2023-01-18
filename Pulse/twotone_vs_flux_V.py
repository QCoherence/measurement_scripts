from lib.math import fit
import ATS9360.DataTreatment as dt
import numpy as np
import qt
import matplotlib.pyplot as plt
###########################################################
FIT = False
Tabor_loading = 1
###########################################################
#
#
#               Devices
#
#
###########################################################

Tabor           = qt.instruments.get('Tabor')
smb_cavity     = qt.instruments.get('smb_1')
ats9360        = qt.instruments.get('ats9360')
SSB_cavity      = qt.instruments.get('SSB_cavity')

Pulsing_instrument = qt.instruments.get('Pulsing_instrument')
current_source = qt.instruments.get('hp3245')

current_min =  0.340e-3 # in A
current_max =  0.350e-3 # in A +
current_step = 0.010e-3 # in A
# c_ref = 0e-6 # in A
current_vec = np.arange(current_min, current_max+current_step, current_step)

###########################################################

f_cav    = 7.40
f_min_q  = 2.35
f_max_q  = 2.40
f_step_q = 0.1e-3

averaging = 2e3
power1 = -0.0 #in [dB]
power2 = -4.0

freq_vec = np.arange(f_min_q, f_max_q + f_step_q, f_step_q)

if len(freq_vec) %2 !=0:
        freq_vec = np.arange(f_min_q, f_max_q , f_step_q)

pulse_time = 600.
delta_t = 200.
acq_time = pulse_time + delta_t + 300.
t2 = 5e-6
t_rise =None
###########################################################

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



current_source.set_mode('dci')
current_source.set_channel('A')
current_source.set_resolution('high')

SSB_cavity.set_freq_start(4)
SSB_cavity.set_freq_stop(8)
SSB_cavity.set_conversion_loss(6.)
SSB_cavity.set_LO_power(5)
SSB_cavity.set_band_type(-1)
SSB_cavity.set_IF_frequency(0.0)


###########################################################
#
#
#               Experiment
#
#
###########################################################

if Tabor_loading:
    Pulsing_instrument.set_trigger_time(50)
    Pulsing_instrument.write_twotone_pulsessequence( temp_1=pulse_time*1e-9, t1_start= t2 + 0.1e-6, temp_2=t2 , m1_start= t2 , delete = 'all')

qt.mstart()
data_measurement = qt.Data(name='Twotone_Spectroscopy_vs_flux')
data_measurement.add_coordinate('Qubit frequency [GHz]', units = 'GHz')
data_measurement.add_coordinate('Current [uA]', units = 'uA')
data_measurement.add_value('S21 ',            units = 'Volt')
data_measurement.add_value('Phase ',            units = 'rad')
data_measurement.add_value('S21 normed',            units = 'Volt')
data_measurement.add_value('Phase normed',            units = 'rad')
data_measurement.add_value('Phase unwrap',            units = 'rad')

data_measurement.create_file()

plot3d_1 = qt.Plot3D(data_measurement,
                  name      = 'S21 ',
                  coorddim  = (0,1),
                  valdim    = 2)


plot2d_1 = qt.Plot2D(data_measurement,
                  name      = 'S21 cut',
                  coorddim  = 0,
                  valdim    = 2,
                  maxtraces = 2)


i = 0
for c in current_vec:
    # current_source.set_current(c)
    go_to_current(current_source, c)
    qt.msleep(0.1)

    board_flag = None

    try:
        Pulsing_instrument.prep_twotone(f_cav, freq_vec, averaging, power1, power2, acq_time, pulse_time, delta_t)
        qt.msleep(1)
        smb_atom.restartsweep()
        qt.msleep(1)
        board_flag = True

        Tabor.set_trigger_source('TIM')
        while ats9360.get_completed_acquisition() != 100.:

            result = ats9360.measurement()
            ((real, rea0), (imag,ima0))= result

            real_a = real - rea0
            imag_a = imag - ima0
            real_a = np.mean(np.reshape(real_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
            imag_a = np.mean(np.reshape(imag_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
            amplitude = np.sqrt(real_a**2+imag_a**2)

            complexe = (real_a + 1j*imag_a )*np.exp(1j*freq_vec*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase = np.angle(complexe)

            phase_unwrap = np.unwrap(phase)
            if i == 0:
                a0 = amplitude
                ph0 = phase
            amp_normed = amplitude - a0
            phase_normed = np.unwrap(phase - ph0)
            qt.msleep(0.1)


        Tabor.set_trigger_source('EVEN')
        ats9360.measurement_close(transfert_info=False)
        board_flag = False


    finally:
        if board_flag:
            ats9360.measurement_close(transfert_info=False)

        data_measurement.add_data_point(freq_vec,1e6*c*np.ones_like(freq_vec), amplitude, phase, amp_normed,
                phase_normed, phase_unwrap)
        data_measurement.new_block()



        print ats9360.measurement_close(transfert_info=True)
        # smb_cavity.set_freqsweep('OFF')
        # smb_cavity.set_gui_update('ON')
        Tabor.set_trigger_source('EVEN')

data_measurement.close_file()
plot3d_1.save_png()

qt.mend()
