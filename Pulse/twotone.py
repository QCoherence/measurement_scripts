from lib.math import fit
import ATS9360.DataTreatment as dt
import numpy as np
import qt
###########################################################
Tabor_loading = 0
Tabor_loading = 1

FIT = False
#FIT = True
###########################################################
#
#
#               Devices
#
#
###########################################################

Tabor           = qt.instruments.get('Tabor')
smb_cavity     = qt.instruments.get('smb_1')
smb_atom        = qt.instruments.get('smb_2')
ats9360        = qt.instruments.get('ats9360')
SSB_cavity      = qt.instruments.get('SSB_cavity')
SSB_atom      = qt.instruments.get('SSB_atom')

Pulsing_instrument = qt.instruments.get('Pulsing_instrument')
###########################################################
SSB_cavity.set_freq_start(4)
SSB_cavity.set_freq_stop(8)
SSB_cavity.set_conversion_loss(6.)
SSB_cavity.set_LO_power(15)
SSB_cavity.set_band_type(+1)
SSB_cavity.set_IF_frequency(0.0)

SSB_atom.set_freq_start(4)
SSB_atom.set_freq_stop(8)
SSB_atom.set_conversion_loss(6.)
SSB_atom.set_LO_power(15)
SSB_atom.set_band_type(-1)
SSB_atom.set_IF_frequency(0.05)

averaging = 6e3
power1 = -0. #in [dB]
#power2 = -0.74
power2 = -1.0
# Frequency [GHz]
f_cav  = 7.027

#StartFrequency [GHz]
# f_min = 4.3
f_min = 6.25

#StopFrequency [GHz]
f_max = 6.35
# f_max = 4.8

#Step of the Sweep [GHz]
#f_step = 0.0002
f_step = 0.0005


freq_vec = np.arange(f_min, f_max + f_step, f_step)
if len(freq_vec) %2 !=0:
        freq_vec = np.arange(f_min, f_max , f_step)

pulse_time = 500.
acq_time = 1000.
delta_t = 200.
t2 = 5e-6
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
    # pulse_time*1e-9, 5.1e-6, 5e-6, delete = 'all')
    # ats9360.set_acquisition_time(acq_time)
qt.mstart()

data_measurement = qt.Data(name='Spectroscopy_mix_2')
data_measurement.add_coordinate('Excitation frequency [GHz]', units = 'GHz')
data_measurement.add_value('S21 ',            units = 'Volt')
data_measurement.add_value('Phase ',            units = 'rad')
data_measurement.add_value('Re ',            units = 'Volt')
data_measurement.add_value('Im ',            units = 'Volt')
data_measurement.create_file()


plot2d_1 = qt.Plot2D(data_measurement,
                  name      = 'S21 ',
                  coorddim  = 0,
                  valdim    = 1,
                  maxtraces = 2)

plot2d_2 = qt.Plot2D(data_measurement,
                    name      = 'Phase ',
                    coorddim  = 0,
                    valdim    = 2,
                    maxtraces = 2)

plot2d_3 = qt.Plot2D(data_measurement,
                  name      = 'Re ',
                  coorddim  = 0,
                  valdim    = 3,
                  maxtraces = 2)

plot2d_4 = qt.Plot2D(data_measurement,
                    name      = 'Im ',
                    coorddim  = 0,
                    valdim    = 4,
                    maxtraces = 2)


board_flag = None
try:
    Pulsing_instrument.prep_twotone(f_cav, freq_vec, averaging, power1, power2, acq_time, pulse_time, delta_t)
    qt.msleep(1)
    smb_atom.restartsweep()
    qt.msleep(1)

    board_flag = True

    Tabor.set_trigger_source('TIM')
    while ats9360.get_completed_acquisition() != 100.:
        print ats9360.get_completed_acquisition(), '%'

        result = ats9360.measurement()
        ((real, rea0), (imag,ima0))= result

        real_a = real - rea0
        imag_a = imag - ima0
        real_a = np.mean(np.reshape(real_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
        imag_a = np.mean(np.reshape(imag_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
        amplitude = np.sqrt(real_a**2+imag_a**2)

        complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
        phase = np.angle(complexe)
        # (real_a, imag_a)= result
        #
        # real_a = np.mean(np.reshape(real_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
        # imag_a = np.mean(np.reshape(imag_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
        # amplitude = np.sqrt(real_a**2+imag_a**2)
        #
        # complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
        # phase = np.angle(complexe)

        qt.msleep(0.1)

        plot2d_1.replace_inline_data(freq_vec, amplitude)
        plot2d_2.replace_inline_data(freq_vec, phase)
        plot2d_3.replace_inline_data(freq_vec, real_a)
        plot2d_4.replace_inline_data(freq_vec, imag_a)

    Tabor.set_trigger_source('EVEN')
    ats9360.measurement_close(transfert_info=False)
    board_flag = False


finally:
    if board_flag:
        ats9360.measurement_close(transfert_info=False)

    data_measurement.add_data_point(freq_vec,amplitude,phase, real_a, imag_a)
    data_measurement.close_file()

    print ats9360.measurement_close(transfert_info=True)
    smb_atom.set_freqsweep('OFF')
    smb_atom.set_gui_update('ON')
    Tabor.set_trigger_source('EVEN')
    if FIT:
        data_fit= qt.Data(name='Spectro_fit')
        data_fit.add_value('parameters ',            units = 'none, none, GHz, Volt')
        data_fit.add_value('errors ',            units = 'none, none, GHz, Volt')
        data_fit.create_file()

        s = fit.Lorentzian()
        signal = real_a
        s.set_data(freq_vec, signal)
        # guess parameters##########################################################
        bg = 0
        area = 1.
        f0 = 6.266
        width = 0.02
        p = [bg, area, f0, width]
        # fitting ##################################################################
        p = s.fit(p)
        values_from_fit = s.func(p)
        print 'params:', s.get_fit_params()
        print 'errors:', s.get_fit_errors()

        data_fit.add_data_point(s.get_fit_params(),s.get_fit_errors())
        plot2d_3.add(freq_vec, values_from_fit)
        data_fit.close_file()


plot2d_1.save_png()
plot2d_2.save_png()
qt.mend()
