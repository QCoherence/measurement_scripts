###########################################################
#
#
#               Imports
#
#
###########################################################
from lib.math import fit
import math
import ATS9360.DataTreatment as dt
import numpy as np
from numpy import array
import qt
import datetime
from datetime import date
import time
import sys
import matplotlib.pyplot as plt
import gc


###########################################################
#
#
#               Devices
#
#
###########################################################

## AWG
Tabor           = qt.instruments.get('Tabor')

## Board of acquisition
ats9360        = qt.instruments.get('ats9360')

## real microwave sources
smb_cavity     = qt.instruments.get('smb_1')
smb_atom        = qt.instruments.get('smb_2')
smb_twpa       = qt.instruments.get('smb_3')

## Virtual devices
SSB_cavity      = qt.instruments.get('SSB_cavity')
SSB_atom      = qt.instruments.get('SSB_atom')
# SSB_atom2     = qt.instruments.get('SSB_atom2')

## Digital attenuators (step=0.25 dB)
Rudat = qt.instruments.get('RUDAT_ph')
Rudat_2 = qt.instruments.get('RUDAT_comp')
Rudat_3 = qt.instruments.get('RUDAT_pump')
# Att_JPA = qt.instruments.get('Attenuator_JPA')

## Current sources HP
# Cur_qub = qt.instruments.get('hp3245')
Cur_qub = qt.instruments.get('b2902a')
Cur_jpa =  qt.instruments.get('hp3245jpa')


## Main Virtual device for pulse shaping
Pulsing_instrument = qt.instruments.get('Pulsing_instrument')


###################################
####_____SETUP__DEVICES____########
###################################
smb_cavity.set_power(18)
# smb_cavity.set_power(18.12) #when JPA is ON
smb_cavity.set_gui_update('ON')
smb_cavity.set_status('off')
qt.msleep(0.1)

# smb_atom.set_power(15)
smb_atom.set_power( 5)       #new ssb w8ch03 (before 15dBm was crazy)
smb_atom.set_gui_update('ON')
qt.msleep(0.1)

SSB_cavity.set_freq_start(4)
SSB_cavity.set_freq_stop(8)
SSB_cavity.set_conversion_loss(6.)
SSB_cavity.set_LO_power(15)
SSB_cavity.set_band_type(-1)
SSB_cavity.set_IF_frequency(0.0)
qt.msleep(0.1)

# SSB_atom.set_freq_start(4)    #old ssb for 2017-2020
# SSB_atom.set_freq_stop(8.)    #old ssb for 2017-2020
SSB_atom.set_freq_start(0.5)    #new ssb for w8ch03
SSB_atom.set_freq_stop( 5.0)    #new ssb for w8ch03
SSB_atom.set_conversion_loss(6.)
# SSB_atom.set_LO_power(15)     #new ssb w8ch03 (before 15dBm was crazy)
SSB_atom.set_LO_power( 5)
SSB_atom.set_band_type(-1)
SSB_atom.set_IF_frequency(0.05)
qt.msleep(0.1)

###########################################################
#
#               Global constants
#
###########################################################
# AWG_OFFSET = -0.060
AWG_OFFSET = 0.0

### position of blob from get_fidelity, if 50Ohm on output
VOID_RE = 0.0
VOID_IM = 0.0
# VOID_RE = -0.0002371347
# VOID_IM = -0.0005649796

VOID_RE_MV = 1e3*VOID_RE
VOID_IM_MV = 1e3*VOID_IM


my_colors_dict = {  'redberry'      :'#970000',
                    'tamarillo'     :'#8b1212',
                    'venetianred'   :'#770023',
                    'monarch'       :'#850731',
                    'toledo'        :'#40001b',
                    'shipgrey'      :'#423B4B',
                    'charde'        :'#20202c',
                    'woodsmoke'     :'#171719',
                    'mediumpurple'  :'#795FD7',
                    'curciousblue'  :'#2f99e2',
                    'electric'      :'#795fd7',
                    'deus_ex_gold'  :'#eda723',
                    'meduza'        :'#b5895b',
                    'meduza_gold'   :'#B5965B',
                    'blob_g'        :'#546ea9',
                    'blob_e'        :'#fd6e6e',
                    'blob_post'     :'#1b346e',
                    'g_state_mark'  :'#849cd4',
                    'e_state_mark'  :'#fe9393'

}


def get_same_ampl_freq_vs_rudat(rudat):
    '''
    Uses data from 23 June 2021 for sample w8ch03 conditional transmission vs rudat
    '''
    freq_amp_crossection_vs_rudat = {
                        30.0 	 : 7.37 ,
                        29.5 	 : 7.37 ,
                        29.0 	 : 7.36975 ,
                        28.5 	 : 7.36975 ,
                        28.0 	 : 7.36975 ,
                        27.5 	 : 7.36975 ,
                        27.0 	 : 7.36975 ,
                        26.5 	 : 7.36975 ,
                        26.0 	 : 7.36975 ,
                        25.5 	 : 7.36975 ,
                        25.0 	 : 7.36975 ,
                        24.5 	 : 7.3695 ,
                        24.0 	 : 7.3695 ,
                        23.5 	 : 7.3695 ,
                        23.0 	 : 7.3695 ,
                        22.5 	 : 7.3695 ,
                        22.0 	 : 7.3695 ,
                        21.5 	 : 7.36925 ,
                        21.0 	 : 7.36925 ,
                        20.5 	 : 7.36925 ,
                        20.0 	 : 7.36925 ,
                        19.5 	 : 7.36925 ,
                        19.0 	 : 7.369 ,
                        18.5 	 : 7.369 ,
                        18.0 	 : 7.369 ,
                        17.5 	 : 7.36875 ,
                        17.0 	 : 7.36875 ,
                        16.5 	 : 7.3685 ,
                        16.0 	 : 7.3685 ,
                        15.5 	 : 7.36825 ,
                        15.0 	 : 7.368 ,
                        14.5 	 : 7.36775 ,
                        14.0 	 : 7.3675 ,
                        13.5 	 : 7.36725 ,
                        13.0 	 : 7.367 ,
                        12.5 	 : 7.36675 ,
                        12.0 	 : 7.3665 ,
                        11.5 	 : 7.36625 ,
                        11.0 	 : 7.36575 ,
                        10.5 	 : 7.36525 ,
                        10.0 	 : 7.36475 ,
                        9.5 	 : 7.36425 ,
                        9.0 	 : 7.3635 ,
                        8.5 	 : 7.363 ,
                        8.0 	 : 7.36225 ,
                        7.5 	 : 7.361 ,
                        7.0 	 : 7.36 ,
                        6.5 	 : 7.359 ,
                        6.0 	 : 7.358 ,
                        5.5 	 : 7.35725 ,
                        5.0 	 : 7.3565 ,
                        4.5 	 : 7.3555 ,
                        4.0 	 : 7.3545 ,
                        3.5 	 : 7.3535 ,
                        3.0 	 : 7.3525 ,
                        2.5 	 : 7.3515 ,
                        2.0 	 : 7.3505 ,
                        1.5 	 : 7.34975 ,
                        1.0 	 : 7.35
    }

    ## check limits:
    if 1.0 <=rudat <=30.0:
        pass
    else:
        "get_same_ampl_freq_vs_rudat Rudat out of limits. Rudat < 1dB is not in database"
        return None

    ## check if we have it in database
    if rudat not in freq_amp_crossection_vs_rudat.keys():
        ## take a meanvalue
        smaller = get_same_ampl_freq_vs_rudat( round(rudat-0.25, 1) )
        bigger  = get_same_ampl_freq_vs_rudat( round(rudat+0.25, 1) )
        return round( np.mean([smaller, bigger]), 5)


    return round( freq_amp_crossection_vs_rudat[rudat], 5 )


###########################################################
#
#               Handmade functions
#
###########################################################
def taketime():
	'''
	returns date and time now as a short string
	'''
	import datetime
	s = str(datetime.datetime.now())
	s = s[2]+s[3]+s[5]+s[6]+s[8]+s[9]+'_'+s[11]+s[12]+s[14]+s[15]+s[17]+s[18]
	return s

def take_dt_str(date=True, time=True, slash=False):
    import datetime
    s1 = ''
    s = str(datetime.datetime.now())

    if date:
        s1 =s1 + s[0] + s[1] +s[2]+s[3]+s[5]+s[6]+s[8]+s[9]
    if slash:
        s1 = s1 + '\\'
    if time:
        s1 = s1 + s[11]+s[12]+s[14]+s[15]+s[17]+s[18]

    return s1

def test_color(color1, color2):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
    ax.set_facecolor(color1)

    plt.grid(axis = 'both', color=color2, alpha= 0.5)
    plt.plot([0.1],[0.1],'+', color=color2)
    plt.show()

def complex_num_relationships(re1,im1,re2,im2):
    '''
    return distance and angle between two complex numbers
    tekes re and im of both numbers
    '''
    c1 = re1 + 1j*im1
    c2 = re2 + 1j*im2
    theta = np.angle(c2-c1, deg=True)
    distance = np.sqrt( (re2-re1)**2 + (im2-im1)**2  )

    return [distance, theta]

def angle_three_points(x1,y1,x2,y2,x3,y3):
    '''
    Find an angle between three points.
    Takes 6 coordinats <ABC
    return angle in grad
    '''

    [dist, theta12] = complex_num_relationships(x2,y2,x1,y1)
    if theta12 < 0:
        theta12 = 360 + theta12
    [dist, theta23] = complex_num_relationships(x3,y3,x2,y2)
    if theta23 < 0:
        theta23 = 360 + theta23

    angle = theta23 - theta12 - 180

     # to be always in range [-360:360]
    if angle> 0:
        angle = angle % 360
    else:
        angle = -angle % 360
        angle = -angle

    return angle

def where_sameside(a_arr, b, ref=0):
    '''
    a_arr = array, b =value_to_compare_with, and ref = reference value
    Returns array of booleans:
    True - on positions where value of both arrays have same side to ref
    False where side is different
    '''
    def sameside(a,b, ref=0):
        '''
        if ref = 0
        return True if a and b has a same sign
        for different ref return True if a and b on the one side from ref
        '''
        if (a == ref) or (b==ref):
            return True
        a_sign = a > ref
        b_sign = b > ref
        if a_sign == b_sign:
            return True
        else:
            return False

    result_array = np.zeros(len(a_arr))
    for i in range(len(a_arr)):
        result_array[i] = sameside(a_arr[i] ,b, ref=ref)

    return result_array

def ingap(value, min_value, max_value):
    if value > max_value:
        return False
    if value < min_value:
        return False
    return True

def closest_even(x):
    '''
    Function to find the closest even number to x
    x should be more than 1.0
    '''
    if abs(x) < 1.0:
        print 'error: closest_even() - abs(x) must be more than 1.0'
    if x < 0:
        sign = -1
    else:
        sign = 1
    x = abs(x)

    # if rounds to even - simple case
    if ( round(x) %2 == 0):
        result = round(x)
        return result*sign
    # round(x) is not even:
    #two even candidats:
    a1 = round(x)+1
    a2 = round(x)-1
    r1 = abs(a1-x)
    r2 = abs(a2-x)
    if (r1 < r2):
        result = a1
    else:
        result = a2
    return result*sign

def get_datetime(arg='datetime'):
    '''
    function take arguments 'date', 'time', and 'datetime'
    returns simple string with date and time
    '''
    t = datetime.datetime.now()
    year = str(t.year)

    if t.month > 9:
        month = str(t.month)
    else:
        month = '0' + str(t.month)

    if t.day > 9:
        day = str(t.day)
    else:
        day = '0' + str(t.day)

    if t.hour > 9:
        hour = str(t.hour)
    else:
        hour = '0' + str(t.hour)

    if t.minute > 9:
        minute = str(t.minute)
    else:
        minute = '0' + str(t.minute)

    if t.second > 9:
        second = str(t.second)
    else:
        second = '0' + str(t.second)

    time = hour + minute + second
    date = year + month + day

    if arg == 'time':
        return time

    if arg == 'date':
        return date

    if arg == 'datetime':
        return date+time

def check_rudat_value(value):
    if value < 0:
        return False
    if value > 30:
        return False

    return True

def go_to_current( current_src_instr, cur_target, cur_step=1.0e-4, t_step=0.1 ):
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

def save_data(data, coordinats = ['x'], values=['y'], name='noname', filepath=None, set_file=True, log_file=True):
    '''
    saves data using qt-lab
    data must be given as list of the lists like [list_of_x, list_of_y], with same lenght
    coordinats and values must be given as lists of strings. And number of coordinates + values must be equal to number of lists of data
    returns qt.data object

    Example:
    list_x = [1,2,...n]
    list_y = [1,4,...n]
    list_z = [1,4,...n]
    save_data( [list_x, list_y, list_z], coordinats=['x', 'y'], values=['z'] )
    '''
    if (type(data) != type([1,2,3,4])) and (type(data) != type( np.zeros(1) )):
        print 'data with type list of lists is expected. Was given', type(data)
        return False
    if len(data) < 1:
        print 'Looks like there is no data here'
        return False
    if  type(data[0]) != type([1,2,3,4]) and (type(data[0]) != type( np.zeros(1) )):
        print 'data with type list of lists is expected. Was given list of', type(data[0])
        return False
    if len(data) != len(coordinats) + len(values):
        print 'length of data sequence is not the same as coordinats + values'
        return False
    if  len(data[0]) < 1:
        print 'Looks like there is no data here'
        return False
    for dat_list in data:
        if len(dat_list) != len(data[0]):
            print 'ERROR of save_data(): data lists has not same length'
            return False

    data_measurement = qt.Data(name=name)

    for cord in coordinats:
        data_measurement.add_coordinate(cord)
    for value in values:
        data_measurement.add_value(value)

    data_measurement.create_file(filepath=filepath, settings_file=set_file, logging_file=log_file)

    data_ar = array(data)
    data_ar = np.transpose(data_ar)
    data_measurement.add_data_point(data_ar)
    data_measurement.close_file()

    print 'data saved'
    return data_measurement

def set_font(filename='Orbitron_Regular.ttf'):
    '''
    Takes the name of file.ttf
    File must be in folder of
    Python27\Lib\site-packages\matplotlib\mpl-data\fonts\ttf
    return prop
    wich could be use as in an example:
    ax.set_title('This is a special font: {}'.format(fname), fontproperties=prop)
    fontproperties = set_font('Forza-Book.ttf')
    '''
    ## special font from ttf
    ###+===============================######
    import os
    from matplotlib import font_manager as fm, rcParams

    # str_adress_name = "fonts/ttf/" + filename
    str_adress_name = "fonts\\ttf\\" + filename

    fpath = os.path.join(rcParams["datapath"], str_adress_name)
    prop = fm.FontProperties(fname=fpath)
    # fname = os.path.split(fpath)[1]

    return prop

def estimate_nb_oscillations(vec):      # ADDED on 06/23/2021
    '''
    Function to estimate roughly number of oscillations for vec - data like exp_decay_sinus or other
    Takes vec - np.array of data
    Return integer number of oscillations
    ...
    Calculates it by finding medium number as max - min and counts how much time the curve crossected this value
    '''
    nom_cross = 0
    background = (vec.max() + vec.min())/2.
    for i in np.arange(3, len(vec)):
        #s[i] positive sign or not
        s0 = vec[i-3] > background
        s1 = vec[i-2] > background
        s2 = vec[i-1] > background
        s3 = vec[i]   > background
        if (s0==s1 and s2==s3 and s1!=s3):
            nom_cross = nom_cross +1
    nb_expected_oscillation = nom_cross/2

    return nb_expected_oscillation

def set_qub_cur(cur):
    # def current_valid(cur, maxcur=50e-3):
    #     if abs(cur) < maxcur:
    #         return True
    #     else:
    #         print('Error of setting current. Current must be not more than:', maxcur, '[A]')
    #         return False
    #
    # if not current_valid(cur):
    #     return False
    #
    # try:
    #     Cur_jpa.set_resolution('high')
    #     qt.msleep(0.2)
    #     Cur_jpa.set_output_terminal('FRONT')
    #     qt.msleep(0.2)
    #
    #     Cur_jpa.set_channel('B')
    #     qt.msleep(0.5)
    #     Cur_jpa.set_mode('dci')
    #     qt.msleep(0.5)
    #
    #     Cur_jpa.set_current(cur)
    #     qt.msleep(1)
    #
    #     return True
    # except:
    #     return False
    try:
        go_to_current(Cur_qub, cur)
        return True
    except:
        print "\n cant set current!! \n "
        return False

def get_qub_cur():
    # try:
    #     Cur_jpa.set_channel('B')
    #     qt.msleep(0.5)
    #     Cur_jpa.set_mode('dci')
    #     qt.msleep(0.5)
    #     cur_qub = Cur_jpa.get_current()
    #     qt.msleep(1)
    #     return cur_qub
    # except:
    #     return None
    ###### simplify
    try:
        return Cur_qub.get_current()
    except:
        print "\n Warning! cant get current! \n"
        return None

def set_jpa_cur(cur):
    print "NO CURRENT SOURSE ANYMORE"
    return False

    def current_valid(cur, maxcur=50e-3):
        if abs(cur) < maxcur:
            return True
        else:
            print('Error of setting current. Current must be not more than:', maxcur, '[A]')
            return False

    if not current_valid(cur):
        return False

    try:
        Cur_jpa.set_resolution('high')
        qt.msleep(0.2)
        Cur_jpa.set_output_terminal('FRONT')
        qt.msleep(0.2)

        Cur_jpa.set_channel('A')
        qt.msleep(0.5)
        Cur_jpa.set_mode('dci')
        qt.msleep(0.5)

        Cur_jpa.set_current(cur)
        qt.msleep(1)

        return True
    except:
        return False

def get_jpa_cur():
    try:
        Cur_jpa.set_channel('A')
        qt.msleep(0.5)
        Cur_jpa.set_mode('dci')
        qt.msleep(0.5)
        cur_jpa = Cur_jpa.get_current()
        qt.msleep(1)
        return cur_jpa
    except:
        return False

def smb_cavity_on(comment=True):
    try:
        smb_cavity.set_status('on')
        if comment:
            print('smb_cavity status on')
        qt.msleep(0.2)
        return True
    except:
        return False

def smb_cavity_off(comment=True, pause=None):
    try:
        smb_cavity.set_status('off')
        if pause == None:
            if comment:
                print('smb_cavity status off')
        else:
            if comment:
                print('smb_cavity status off, waiting {}s ...'.format(abs(pause)))
            qt.msleep(abs(pause))
        return True
    except:
        return False

def smb_atom_on(comment=True):
    try:
        smb_atom.set_status('on')
        if comment:
            print('smb_atom status on')
        qt.msleep(0.2)
        return True
    except:
        return False

def smb_atom_off(comment=True, pause=None):
    try:
        smb_atom.set_status('off')
        if pause == None:
            if comment:
                print('smb_atom status off')
        else:
            if comment:
                print('smb_atom status off, waiting {}s ...'.format(abs(pause)))
            qt.msleep(abs(pause))
        return True
    except:
        return False

def smb_twpa_on(comment=True):
    try:
        smb_twpa.set_status('on')
        if comment:
            print('smb_twpa status on')
        qt.msleep(0.2)
        return True
    except:
        return False

def smb_twpa_off(comment=True, pause=None):
    try:
        smb_twpa.set_status('off')
        if pause == None:
            if comment:
                print('smb_twpa status off')
        else:
            if comment:
                print('smb_twpa status off, waiting {}s ...'.format(abs(pause)))
            qt.msleep(abs(pause))
        return True
    except:
        return False

def all_smb_on(comment=True):
    # print "\n \n \n (!) FUNCTION ALL_SMB_ON() DISABLED \n\n\n"
    smb_cavity_on(comment=comment)
    smb_atom_on(comment=comment)
    if TWPA_ON:
        smb_twpa_on(comment=comment)
        print "TWPA_ON"
    else:
        print "TWPA_ON == False. NO PUMP"
    qt.msleep(2.0) # warming up devices
    return

def all_smb_off(comment=True,  pause=None):
    # pass
    # print "\n \n \n (!) FUNCTION ALL_SMB_OFF() DISABLED \n\n\n"
    smb_cavity_off(comment=comment, pause=pause)
    smb_atom_off(comment=comment,   pause=pause)
    smb_twpa_off(comment=comment,   pause=pause)
    return

class Stopclock:
    time_start = None
    time_stop = None
    time_interval = None

    def __init__(self):
        import datetime
        self.start()

    def start(self):
        self.time_start = datetime.datetime.now()

    def stop(self):
        self.time_stop = datetime.datetime.now()
        self.time_interval = self.time_stop - self.time_start
        return self.time_interval

    def display(self):
        print 'Start:\t\t', self.time_start
        print 'Stop:\t\t', self.time_stop
        print 'Interval:\t', self.time_interval


###########################################################
#
#               Class of parameters
#
###########################################################

class SetOfParam(object):
    '''
    Data keeper class
    every object is a set_of_parameters for different kind of measurements

    '''
    #readout tone
    freq_read = 0 #GHz
    rudat = 0
    power1 = -0.0
    t_read = 0 #duration of readout pulse # in sec
    t_between = 0 ## time between pre-pulse and readout. [uses only for singleshot] [is =0 -- no pre-pulse]

    #qubit 0-1 tone
    freq_q = 0  #GHz
    rudat2 = 0
    power2 = 0
    tpi = 0 # in sec
    nsigma = 0

    #other
    jpa_att = 0
    current = 0
    phase1 = 0
    phase2 = 0
    def __init__(self):
        print 'param created'
        self.get_jpa_att()
        # self.set_params_tim()

    def __repr__(self):
        self._compare_assign('rudat2', Rudat_2.get_attenuation())
        self._compare_assign('rudat', Rudat.get_attenuation())
        # self._compare_assign('phase1', Phase_1.get_phase_shift())
        # self._compare_assign('phase2', Phase_2.get_phase_shift())
        self._compare_assign('current', get_qub_cur())
        smb_status = smb_cavity.get_status()

        if self.current == None:
            print "Attention. Costil. Current to zero"
            self.current = 0.0


        text = 'freq_read = {}GHz \npower1    = {} \nt_read    = {}ns \nt_between = {}ns\nrudat     = {}dB\n\n'.format(self.freq_read, self.power1,
        1e9*self.t_read, 1e9*self.t_between, self.rudat)
        text += 'phase1    = {}deg \n\n'.format(self.phase1)
        text += 'freq_q    = {}GHz \npower2    = {}\nrudat2    = {}\ntpi       = {}ns\nnsigma    = {}\n'.format(self.freq_q, self.power2, self.rudat2, self.tpi*1e9, self.nsigma)
        text += 'phase2    = {}deg\n\n'.format(self.phase2)
        text += 'current   = {}mA\n'.format(self.current*1e3)
        text += 'jpa_att   = {}dB\n'.format(self.jpa_att)
        text += 'smb_cavity status = {}'.format(smb_status)

        return text

    def __str__(self):
        return self.__repr__()

    def __setattr__(self, name_attr, val_attr):
        previous_val = getattr(self, name_attr)
        object.__setattr__(self, name_attr, val_attr)
        if previous_val == 0:
            return False
        if previous_val == val_attr:
            print '{} was not changed from {}'.format(name_attr, previous_val)
        else:
            print '{} was changed from {} to {}'.format(name_attr, previous_val, val_attr)

    def _compare_assign(self, name, val):
        if getattr(self, name) != val:
            self.__setattr__(name, val)


    def set_params_forRS(self):
        ### NON Gaussian
        print 'set_params_forRS():'
        print 'NON gaussian pi-pulse!'
        #================== JPA ===============#
        self.freq_q = 6.2985
        self.set_rudat2(11)
        self.tpi = 30e-9
        self.power2 = -0.09
        self.nsigma = 0

        ###___Parameters of Readout tone___########################
        # param0.freq_read = 7.029    #best by distance blobs
        self.freq_read = 7.028    #from onetone
        self.set_rudat(28)
        self.power1 = -0.0
        self.t_read = 500e-9 #duration of readout pulse

        ###___Put correct values of rudats and current_source___###
        # param0.current = Cur_qub.get_current()
        self.set_phase1(65)
        self.set_phase2(0)
        #----------------------------------------------------------
        self.save()

    def set_params_sym(self):
        ### NON Gaussian
        print 'NON gaussian pi-pulse!'
        #================== JPA ===============#
        self.freq_q = 6.2986
        self.set_rudat2(7.75)
        self.tpi = 30e-9
        self.power2 = -0.09
        self.nsigma = 1.8

        ###___Parameters of Readout tone___########################
        self.freq_read = 7.022    #from onetone
        self.set_rudat(17)
        self.power1 = -0.0
        self.t_read = 200e-9 #duration of readout pulse
        self.t_between = 1000e-9

        ###___Put correct values of rudats and current_source___###
        # param0.current = Cur_qub.get_current()
        self.set_phase1(10)
        self.set_phase2(0)
        #----------------------------------------------------------
        self.save()

    def set_params_tim(self):
        ### NON Gaussian
        print 'NON gaussian pi-pulse!'
        #================== JPA ===============#
        self.freq_q = 6.314
        self.set_rudat2(7.75)
        self.tpi = 46e-9
        self.power2 = -0.09
        self.nsigma = 3.0

        ###___Parameters of Readout tone___########################
        self.freq_read = 7.021    #from onetone
        self.set_rudat(18)
        self.power1 = -0.0
        self.t_read = 165e-9 #duration of readout pulse
        self.t_between = 400e-9

        ###___Put correct values of rudats and current_source___###
        # param0.current = Cur_qub.get_current()
        self.set_jpa_att(11.4)
        self.current = get_qub_cur()
        self.set_phase1(30)
        self.set_phase2(0)


    def get_string(self):
        name = ' p1='+str(round(self.power1,2))+';fr='+str(round(self.freq_read,3))+';tr='+str(round(self.t_read*1e9,0))
        name = name + 't_btw='+str(1e9*self.t_between)
        name = name +';Rd='+str(round(self.rudat,2))+';p2='+str(round(self.power2,2))
        name = name +  ';fq='+str(round(self.freq_q,3))+';pi='+str(round(self.tpi*1e9))+';cur'+str(round(self.current,5))+'sig='+str(round(self.nsigma,1))
        name = name + ';rud2='+str(self.rudat2)
        return name

    def save(self, name='parameters '):
        data_parameters = qt.Data(name=name+taketime())
        data_parameters.add_value('freq_read',     units='GHz')
        data_parameters.add_value('power1',    units='V')
        data_parameters.add_value('t_read',    units='ns')
        data_parameters.add_value('t_between',    units='ns')
        data_parameters.add_value('rudat',     units='dB')
        data_parameters.add_value('freq_q',     units='GHz')
        data_parameters.add_value('power2',     units='V')
        data_parameters.add_value('rudat2',     units='dB')
        data_parameters.add_value('tpi',     units='ns')
        data_parameters.add_value('nsigma',     units='none')
        data_parameters.add_value('cur',     units='A')
        data_parameters.add_value('phase1',     units='deg')
        data_parameters.add_value('jpa_att',     units='dB')
        data_parameters.create_file()

        if self.current == None:
            self.current = 0.0
            print "attention. Costil. current saved as zero"
        data_parameters.add_data_point(self.freq_read, self.power1, self.t_read, self.t_between, self.rudat, self.freq_q, self.power2, self.rudat2, self.tpi, self.nsigma, self.current, self.phase1, self.jpa_att)
        data_parameters.close_file()
        print 'parameters saved'
        return data_parameters

    def get_jpa_att(self):
        return 0 #!!
        jpa_att = Att_JPA.get_attenuation()
        value = int(((jpa_att-11)*120) / 6)
        if value%2 != 0:
            self.jpa_att = jpa_att + 0.05
        else:
            self.jpa_att = jpa_att

    def set_jpa_att(self, att):
        Att_JPA.set_attenuation(att)
        self.jpa_att = Att_JPA.get_attenuation()
        return True

    def set_rudat(self, att):
        Rudat.set_attenuation(att)
        self.rudat = Rudat.get_attenuation()
        return True

    def set_rudat2(self, att):
        Rudat_2.set_attenuation(att)
        self.rudat2 = Rudat_2.get_attenuation()
        return True

    def set_phase1(self, phase):
        return None ##!V
        try:
            Phase_1.set_phase_shift(phase)
            self.phase1 = Phase_1.get_phase_shift()
            return True
        except:
            print('Error set_phase1(): can not set the Phase2')
            return False

    def set_phase2(self, phase):
        try:
            Phase_2.set_phase_shift(phase)
            self.phase2 = Phase_2.get_phase_shift()
            return True
        except:
            print('Error set_phase2(): can not set the Phase2')
            return False

###########################################################
#
#               Measurment functions
#
###########################################################

def get_vna_trace(fr_start=7.074, fr_stop=7.075, nop=1001, power=0, bw=100, av=1, fname=None, memory=None):
    '''
    __Get single trace form VNA__
    fr_start, fr_stop - frequences in GHz
    nop - nomber of points in trace
    power - power of mw source VNA in [dBm]
    bw - bandwidth
    av - number of averaging. (if < 2 -- no averaging)
    fname - name of file and folder
    memory - vna_trace [freqs, amps, phases], data to subtract from new trace
    fr_start=7.0267, fr_stop=7.0269,
    '''

    #fr_start=7.025, fr_stop=7.03, nop=501

    fr_start = fr_start*1e9
    fr_stop = fr_stop*1e9

    if 'vna' in globals():  ## same as if it is connected (var is exists)
        vna.set_sweeptype('LIN')     #Linear frequency sweep
        vna.set_trigger('IMM')       #Immediate trigger. The vna measures the second trace immediately after the first one.
        vna.set_startfrequency(fr_start)
        vna.set_stopfrequency(fr_stop)
        vna.set_port1_power(power)
        vna.set_port2_power(power)
        vna.set_measBW(bw)
        vna.set_points(nop)
        if av > 1:
            vna.set_averages(av)
            vna.set_averagestatus('on')
        else:
            vna.set_averages(1)
            vna.set_averagestatus('off')
        vna.create_traces(('1',),('S21',))
        vna.set_status('on')

        if fname is None:
            fname = 'VNA_trace'
        ####---------------------------------####
        qt.mstart()

        #We create the object data
        data = qt.Data(name=fname) #Do not change filename. Include comments as 'filename + str(comments)'
        data.add_coordinate('Frequency [GHz]', units='GHz')
        data.add_value('S_21 [dB]', units='dB')
        data.add_value('Phase [deg]', units='deg')
        data.create_file()

        #We live plot what we record
        plot2d_1= qt.Plot2D(data, name='_dB', coorddim=0, valdim=1, maxtraces=2)
        plot2d_2= qt.Plot2D(data, name='_phase', coorddim=0, valdim=2, maxtraces=2)

        ####---------------------------------####


        try:
            vna.averageclear()
            vna.measure()
            qt.msleep(0.1)
            # print 'here start'
            ampdB, phase = vna.get_traces(('1',))[0]
            # print 'here finish'
            qt.msleep(0.1)

            ###_minus_memory__if_given_######
            freqs = linspace(fr_start, fr_stop, nop) / 1.0e9
            if memory is not None:
                if False in (memory[0] == freqs) :
                    print 'Erorr VNA_trace: memory trace has different freqs'
                    return False
                amps_zero  = memory[1]
                phase_zero = memory[2]
                ### minus memory trace
                ampdB = ampdB - amps_zero
                phase = phase - phase_zero
            ###_________________________######

            data.add_data_point(freqs,ampdB,phase)

        except Exception as error:
            print str(error)
            return False

        finally:
            qt.msleep()
            data.close_file()

            plot2d_1.save_png()
            plot2d_2.save_png()

            vna.set_status('off')
            qt.mend()

            print 'return [freqs, ampdB, phase]'
            return [freqs, ampdB, phase]

    else:
        print 'WARNING! VNA IS NOT CONECTED TO QTLAB!'

def get_onetone_fread(f_min_cav=6.5, f_max_cav=7.5, tl = 1, graph = True, averaging = 0.5e3, nop=300, awg_offset=AWG_OFFSET, returnALL=False):
    '''
    One tone spectroscopy
    if not returnALL - return only freq of maximum amplitude
    if returnALL - return [list_of_freq, list of amplitude, list of phase, list_of_fit]
    tl=1 - means Tabor Loading. Necessary if it's a new pulse sequence for AWG
    '''
    smb_cavity_on()
    # all_smb_on()
    Tabor_loading = tl
    SSB_cavity.set_band_type(+1)
    #only this is important. (no singlesideband == 0 freq) /180711 V
    power = -0. #in [dB]
    pulse_time = 1000.
    delta_t = 200.
    acq_time = pulse_time+delta_t+300.
    t_rise = None

    f_step_cav = round( abs(f_max_cav - f_min_cav)/nop,  6 ) ##[GHz]
    freq_vec = np.arange(f_min_cav, f_max_cav + f_step_cav, f_step_cav)
    if len(freq_vec) %2 !=0:
            freq_vec = np.arange(f_min_cav, f_max_cav , f_step_cav)
    if nop != len(freq_vec):
        print "nop changed from ", nop, "to ", len(freq_vec)
        nop = len(freq_vec)

    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################
    if Tabor_loading:
        Pulsing_instrument.set_trigger_time(100)
        Pulsing_instrument.write_onetone_pulsessequence( pulse_time*1e-9, t1_start=0.2e-6, m1_start=0.1e-6, delete = 'all', t_rise=t_rise)
        # ats9360.set_acquisition_time(acq_time)
        Tabor.set_ch1_offset(awg_offset)

    qt.mstart()

    data_measurement = qt.Data(name='onetone')
    data_measurement.add_coordinate('Read-out frequency [GHz]', units = 'GHz')
    data_measurement.add_value('Amplitude [mV]',            units = 'mV')
    data_measurement.add_value('Phase ',            units = 'rad')
    data_measurement.add_value('Phase unwrapped',            units = 'rad')
    data_measurement.create_file()

    if graph:
        plot2d_1 = qt.Plot2D(data_measurement,
                          name      = 'S21 onetone',
                          coorddim  = 0,
                          valdim    = 1,
                          maxtraces = 2)

        # plot2d_2 = qt.Plot2D(data_measurement,
        #                     name      = 'Phase ',
        #                     coorddim  = 0,
        #                     valdim    = 2,
        #                     maxtraces = 2)

    board_flag = None
    try:
        Pulsing_instrument.prep_onetone(freq_vec, averaging, power, acq_time, pulse_time, delta_t)
        qt.msleep(1)
        # smb_cavity.startsweep()
        smb_cavity.set_gui_update('ON')
        smb_cavity.set_freqsweep('ON')
        smb_cavity.restartsweep()

        qt.msleep(1)

        board_flag = True

        Tabor.set_trigger_source('TIM')
        print 'do the measurement onetone...'
        while ats9360.get_completed_acquisition() != 100.:
            #if COMMENTS:
                #print ats9360.get_completed_acquisition()

            result = ats9360.measurement()
            ((real, rea0), (imag,ima0))= result

            real_a = real - rea0
            imag_a = imag - ima0
            ### convert to mV ###
            real_a = 1e3*real_a
            imag_a = 1e3*imag_a


            real_a = np.mean(np.reshape(real_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
            imag_a = np.mean(np.reshape(imag_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)

            amplitude = np.sqrt(real_a**2+imag_a**2)
            complexe = (real_a + 1j*imag_a )*np.exp(1j*freq_vec*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase = np.angle(complexe)
            phase_unwrap = np.unwrap(phase)
            qt.msleep(0.1)

            if graph:
                plot2d_1.replace_inline_data(freq_vec, amplitude)
                #plot2d_2.replace_inline_data(freq_vec, phase)
            # plot2d_3.replace_inline_data(freq_vec, phase_unwrap)

        Tabor.set_trigger_source('EVEN')
        ats9360.measurement_close(transfert_info=False)
        board_flag = False


    finally:
        if board_flag:
            ats9360.measurement_close(transfert_info=False)

        data_measurement.add_data_point(freq_vec,amplitude,phase, phase_unwrap)
        data_measurement.close_file()

        if COMMENTS:
            print ats9360.measurement_close(transfert_info=True)
        Tabor.set_trigger_source('EVEN')
        #set back this parameter
        SSB_cavity.set_band_type(-1)

    data_fit= qt.Data(name='Spectro_fit')
    data_fit.add_value('parameters ',            units = 'none, none, GHz, Volt')
    data_fit.add_value('errors ',            units = 'none, none, GHz, Volt')
    data_fit.create_file()

    s = fit.Lorentzian()
    s.set_data(freq_vec, amplitude**2)
    # guess parameters##########################################################
    bg = 0
    area = 1.
    #f0 = 7.17
    f0 = freq_vec[argmax(amplitude)]
    print 'f0 was', f0
    width = 0.04
    p = [bg, area, f0, width]
    # fitting ##################################################################
    p = s.fit(p)
    values_from_fit = s.func(p)
    if COMMENTS:
        print 'params:', s.get_fit_params()
        print 'errors:', s.get_fit_errors()

    data_fit.add_data_point(s.get_fit_params(),s.get_fit_errors())
    data_fit.close_file()

    if graph:
        plot2d_1.add(freq_vec, np.sqrt(values_from_fit))

        plot2d_1.save_png()
        #plot2d_2.save_png()

    qt.mend()
    p = s.get_fit_params()

    print 'freq= ', p[2]
    print 'width=', p[3]
    f0 = p[2]
    #f0 = p[2] + p[3]/2  #center freq - half of width of peak
    print 'f0=   ', f0

    # smb_cavity_off()
    all_smb_off()
    if returnALL:
        ### [freq_vec,  amplitude, phase, values_from_fit, extracted fit parameters]
        list_all = [freq_vec,  amplitude, phase, values_from_fit, p]
        return list_all
    else:
        if abs( np.mean(amplitude)-np.max(amplitude) )  <  3*np.std(amplitude):
            '_____onetone didnt find peak'
            return None

        if (f0 < f_min_cav) or (f0 > f_max_cav):
                return None

        return f0

def get_onetone_vs_flux(f_min_cav=6.0, f_max_cav=7.4, f_step_cav=0.0035, averaging=1e3, tl=1, current_min=-30.0e-3, current_max=30.0e-3, current_step=5.0e-3, current_src=Cur_qub):
    '''
    tl=1 - means Tabor Loading. Necessary if it's a new pulse sequence for AWG
    '''
    # smb_cavity_on()
    all_smb_on()

    current_vec = np.arange(current_min, current_max+current_step, current_step)
    Tabor_loading = tl

    power = -0.
    freq_vec = np.arange(f_min_cav, f_max_cav + f_step_cav, f_step_cav)
    if len(freq_vec) %2 !=0:
            freq_vec = np.arange(f_min_cav, f_max_cav , f_step_cav)

    pulse_time = 600.
    delta_t = 200.
    acq_time = pulse_time + delta_t + 300.

    t_rise =None

    if Tabor_loading:
        Pulsing_instrument.set_trigger_time(100)
        Pulsing_instrument.write_onetone_pulsessequence( pulse_time*1e-9, t1_start=0.2e-6, m1_start=0.1e-6, delete = 'all',t_rise =t_rise )

    qt.mstart()
    # qt.msleep(1)
    data_measurement = qt.Data(name='Onetone_Spectroscopy_vs_flux')
    data_measurement.add_coordinate('Read-out frequency [GHz]', units = 'GHz')
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

    fres = np.zeros(len(current_vec))
    f0_err =  np.zeros(len(current_vec))
    data_fit= qt.Data(name='Spectro_fit')
    data_fit.add_coordinate('Current', units = 'uA')
    data_fit.add_value('f_cav ',            units = ' GHz')
    data_fit.add_value('f_cav_error ',            units = 'GHz')
    data_fit.create_file()

    s = fit.S21dB_pic_amplitude()

    # guess parameters##########################################################
    Qi = 1e3
    Qext = 1e3
    f0 = 6.95
    background = 0.
    p0 = [Qi, Qext, f0, background]
    i = 0

    for c in current_vec:
        # Cur_qub.set_current(c)
        # set_qub_cur(c)
        go_to_current(current_src, c)
        qt.msleep(0.1)


        board_flag = None
        try:
            Pulsing_instrument.prep_onetone(freq_vec, averaging, power, acq_time, pulse_time, delta_t)
            qt.msleep(1)
            board_flag = True
            smb_cavity.restartsweep()
            qt.msleep(1)


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
            Tabor.set_trigger_source('EVEN')

        s.set_data(freq_vec, amplitude)
        if i>0:
            p0 = p
        p = s.fit(p0)
        print 'params:', s.get_fit_params()
        print 'errors:', s.get_fit_errors()
        fres[i] = p[2]
        f0_err[i] = s.get_fit_errors()[2]

        i += 1
        data_fit.add_data_point(c, p[2], s.get_fit_errors()[2])

    data_measurement.close_file()
    plot3d_1.save_png()
    qt.mend()

    # smb_cavity_off()
    all_smb_off()
    data_fit.close_file()

def get_twotone3D(f_min=2., f_max=2.5, nop=300, averaging=0.5e3, fcav_min=6.5, fcav_max=7.5, fcav_step=5.0e-3):
    '''
    Repeats twotone measurements while varying freq_read
    '''
    qt.mstart()

    data_measurement = qt.Data(name='Twotone_3D')
    data_measurement.add_coordinate('2nd tone freq [GHz]', units = 'GHz')
    data_measurement.add_coordinate('1st tone freq [GHz]', units = 'GHz')
    data_measurement.add_value('S21 ',            units = 'Volt')
    data_measurement.add_value('Phase ',            units = 'rad')
    data_measurement.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'S21 ',
                      coorddim  = (0,1),
                      valdim    = 2)
    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'Phase ',
                      coorddim  = (0,1),
                      valdim    = 3)

    fcav_list = []
    freq_arr_list = []
    ampl_arr_list = []
    phase_arr_list = []

    Tabor_loading = True
    try:
        for freq_cav in np.arange(fcav_min, fcav_max, fcav_step):
            qt.msleep(0.1)

            # [freq_vec, amplitude, phase] = get_twotone_fqub(f_cav, Return_fq_only=False, f_min=f_min, f_max=f_max, Tabor_loading=Tabor_loading, graph=graph, averaging=averaging)
            [freq_vec, amplitude, phase] = get_twotone_fqub(freq_cav, Return_fq_only=False, nop=nop, f_min=f_min, f_max=f_max, Tabor_loading=Tabor_loading, graph=False, averaging=averaging)
            Tabor_loading = False

            data_measurement.add_data_point(freq_vec, freq_cav*np.ones_like(freq_vec), amplitude, phase)
            data_measurement.new_block()

            fcav_list.append(freq_cav)
            freq_arr_list.append( freq_vec )
            ampl_arr_list.append( amplitude )
            phase_arr_list.append( phase )
    finally:
        data_measurement.close_file()
        plot3d_1.save_png()
        plot3d_2.save_png()
        qt.mend()
        # smb_cavity_off()
        all_smb_off()

    print fcav_list, freq_arr_list, ampl_arr_list, phase_arr_list

    return [fcav_list, freq_arr_list, ampl_arr_list, phase_arr_list]

def get_onetone_vs_jpa_flux(f_min_cav=6.8, f_max_cav=7.0, f_step_cav=0.0035, averaging=1e3, tl=1, current_min=0.0e-3, current_max=0.7e-3, current_step=0.1e-3):
    get_onetone_vs_flux(f_min_cav, f_max_cav, f_step_cav, averaging, tl, current_min, current_max, current_step, current_src=Cur_jpa)
    return

def do_onetone_vs_rudat(f_min_cav=6.8,f_max_cav=7.5, rudat_vec=np.arange(0,30,5), tl=1, graph=True, averaging=1000, nop=400, awg_offset=AWG_OFFSET):
    '''
    Make a 3D plot of onetone spectroscopy changing Rudat (power of readout signal)
    '''
    # rudat_vec = np.arange(rudat_start, rudat_stop, rudat_step)
    rudat_stored = Rudat.get_attenuation()

    # smb_cavity_on()
    all_smb_on()

    Tabor_loading = tl
    SSB_cavity.set_band_type(+1) #only this is important. (no singlesideband == 0 freq) /180711 V
    power = -0. #in [dB]
    pulse_time = 500.
    delta_t = 200.
    acq_time = pulse_time+delta_t+300.
    t_rise = None

    f_step_cav = round( abs(f_max_cav - f_min_cav)/nop,  6 ) ##[GHz]
    freq_vec = np.arange(f_min_cav, f_max_cav + f_step_cav, f_step_cav)
    if len(freq_vec) %2 !=0:
            freq_vec = np.arange(f_min_cav, f_max_cav , f_step_cav)
    if nop != len(freq_vec):
        print "nop changed from ", nop, "to ", len(freq_vec)
        nop = len(freq_vec)

    if Tabor_loading:
        Pulsing_instrument.set_trigger_time(100)
        Pulsing_instrument.write_onetone_pulsessequence( pulse_time*1e-9, t1_start=0.2e-6, m1_start=0.1e-6, delete = 'all', t_rise=t_rise)
        # ats9360.set_acquisition_time(acq_time)
        Tabor.set_ch1_offset(awg_offset)

    qt.mstart()

    data_measurement = qt.Data(name='onetone_vs_rudat')
    data_measurement.add_coordinate('Rudat', units = 'dB')
    data_measurement.add_coordinate('Read-out frequency [GHz]', units = 'GHz')
    data_measurement.add_value('Amplitude [mV]',            units = 'mV')
    data_measurement.add_value('Phase ',            units = 'rad')
    data_measurement.add_value('Phase unwrapped',            units = 'rad')
    data_measurement.create_file()

    plot2d_1 = qt.Plot2D(
                    data_measurement,
                    name      = 'onetone_amp_last_trace',
                    coorddim  = 1,
                    valdim    = 2,
                    maxtraces = 2
                    )
    plot3d_1 = qt.Plot3D(
                    data_measurement,
                    name='onetone_vs_rudat_amp',
                    coorddims=(0,1),
                    valdim=2,
                    style='image'
                    )
    plot3d_2 = qt.Plot3D(
                    data_measurement,
                    name='onetone_vs_rudat_phase_unwraped',
                    coorddims=(0,1),
                    valdim=4,
                    style='image'
                    )
    plot3d_1.set_palette('bluewhitered')
    plot3d_2.set_palette('bluewhitered')


    try:
        board_flag = None
        for atten in rudat_vec:
            amplitude    = np.ones_like(freq_vec)
            phase        = np.ones_like(freq_vec)
            phase_unwrap = np.ones_like(freq_vec)
            try:
                Rudat.set_attenuation(atten)
                print "Rudat set:", atten, "dB"
                qt.msleep(0.5)
                Pulsing_instrument.prep_onetone(freq_vec, averaging, power, acq_time, pulse_time, delta_t)
                qt.msleep(1)
                # smb_cavity.startsweep()
                smb_cavity.set_freqsweep('ON')
                smb_cavity.restartsweep()
                qt.msleep(1)
                board_flag = True
                Tabor.set_trigger_source('TIM')
                print 'do the measurement onetone...'

                while ats9360.get_completed_acquisition() != 100.:
                    result = ats9360.measurement()
                    ((real, rea0), (imag,ima0))= result
                    real_a = real - rea0
                    imag_a = imag - ima0

                    ### convert to mV ###
                    real_a = 1e3*real_a
                    imag_a = 1e3*imag_a

                    real_a = np.mean(np.reshape(real_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
                    imag_a = np.mean(np.reshape(imag_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)

                    amplitude = np.sqrt(real_a**2+imag_a**2)
                    complexe = (real_a + 1j*imag_a )*np.exp(1j*freq_vec*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)

                    phase = np.angle(complexe)
                    phase_unwrap = np.unwrap(phase)
                    qt.msleep(0.1)

                    plot2d_1.replace_inline_data(freq_vec, amplitude)
                    #plot2d_2.replace_inline_data(freq_vec, phase)
                    # plot2d_3.replace_inline_data(freq_vec, phase_unwrap)

                Tabor.set_trigger_source('EVEN')
                ats9360.measurement_close(transfert_info=False)
                board_flag = False
            finally:
                atten_got = Rudat.get_attenuation()
                qt.msleep(0.5)
                data_measurement.add_data_point(atten_got*np.ones_like(freq_vec), freq_vec, amplitude, phase, phase_unwrap)
                data_measurement.new_block()
                if board_flag:
                    ats9360.measurement_close(transfert_info=False)

    finally:
        Tabor.set_trigger_source('EVEN')
        SSB_cavity.set_band_type(-1) #set back this parameter
        Rudat.set_attenuation( rudat_stored )

        plot2d_1.save_png()
        plot3d_1.save_png()
        plot3d_2.save_png()

        data_measurement.close_file()

    return True

def get_twotone_fqub(f_cav, f_min=2.8, f_max=3.0, nop = 200, Tabor_loading = 1, graph = True, averaging = 1e3, awg_offset=AWG_OFFSET, Return_fq_only=True):
    ###########################################################
    SSB_cavity.set_band_type(+1)
    # smb_cavity_on()
    # smb_atom_on()
    all_smb_on()

    pow2 = 7        ### ADDED on 20211126

    power1 = -0. #in [dB]
    power2 = -0.  ### -4.0 CHANGED on 26/10/2021
    #threshold = 0.0001
    #f_step = 0.0001

    f_step = round( abs(f_max - f_min)/nop,  6 ) ##[GHz]

    freq_vec = np.arange(f_min, f_max + f_step, f_step)
    if len(freq_vec) %2 !=0:
            freq_vec = np.arange(f_min, f_max , f_step)

    if nop != len(freq_vec):
        print "nop changed from ", nop, "to ", len(freq_vec)
        nop = len(freq_vec)

    pulse_time = 1000. #readout pulse duration [ns]   ### 500. CHANGED on 26/10/2021
    delta_t = 200.
    acq_time = pulse_time + delta_t + 300.   ### acq_time = 1000. CHANGE on 26/10/2021
    # t2 = 5e-6
    t2 = 18.e-6    ### 0.1e-6   # pi-pulse duration [s]   CHANGED on 27/10/2021
    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################

    if Tabor_loading:
        # Pulsing_instrument.set_trigger_time(50) ## changed 05 Mar 2021
        Pulsing_instrument.set_trigger_time(20) ### (10) CHANGED on 26/10/2021
        Pulsing_instrument.write_twotone_pulsessequence( temp_1=pulse_time*1e-9, t1_start= t2 + 0.1e-6, temp_2=t2 , m1_start= t2 , delete = 'all')    ### CHANGED on 30/11/2021
        # Pulsing_instrument.write_twotone_pulsessequence( temp_1=t2 + pulse_time*1e-9, t1_start= 0.1e-6, temp_2=t2 , m1_start= t2 , delete = 'all') # both tones sent simultaneously during t2
        # pulse_time*1e-9, 5.1e-6, 5e-6, delete = 'all')
        # ats9360.set_acquisition_time(acq_time)
        Tabor.set_ch1_offset(awg_offset)
    qt.mstart()

    data_measurement = qt.Data(name='twotone')
    data_measurement.add_coordinate('Excitation frequency [GHz]', units = 'GHz')
    data_measurement.add_value('S21 ',            units = 'Volt')
    data_measurement.add_value('Phase ',            units = 'rad')
    data_measurement.add_value('Re ',            units = 'Volt')
    data_measurement.add_value('Im ',            units = 'Volt')
    data_measurement.create_file()

    if graph:
        plot2d_1 = qt.Plot2D(data_measurement,
                          name      = 'twotone S21 ',
                          coorddim  = 0,
                          valdim    = 1,
                          maxtraces = 2)

        plot2d_2 = qt.Plot2D(data_measurement,
                            name      = 'twotone  Phase ',
                            coorddim  = 0,
                            valdim    = 2,
                            maxtraces = 2)

        # plot2d_3 = qt.Plot2D(data_measurement,
        #                   name      = 'twotone  Re ',
        #                   coorddim  = 0,
        #                   valdim    = 3,
        #                   maxtraces = 2)
        #
        # plot2d_4 = qt.Plot2D(data_measurement,
        #                     name      = 'twotone  Im ',
        #                     coorddim  = 0,
        #                     valdim    = 4,
        #                     maxtraces = 2)

    board_flag = None
    try:
        Pulsing_instrument.prep_twotone(f_cav, freq_vec, averaging, power1, power2, acq_time, pulse_time, delta_t)

        smb_atom.set_power(pow2)        ### ADDED on 20211126

        qt.msleep(1)
        smb_atom.restartsweep()
        qt.msleep(1)

        board_flag = True

        Tabor.set_trigger_source('TIM')
        print 'measure twotone...'
        while ats9360.get_completed_acquisition() != 100.:
            #print ats9360.get_completed_acquisition(), '%'

            result = ats9360.measurement()
            ((real, rea0), (imag,ima0))= result

            real_a = real - rea0
            imag_a = imag - ima0
            real_a = np.mean(np.reshape(real_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
            imag_a = np.mean(np.reshape(imag_a, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) ), axis = 1)
            amplitude = np.sqrt(real_a**2+imag_a**2)

            complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase = np.angle(complexe)
            #print 'hey! i am here!'

            qt.msleep(0.1)

            if graph:
                plot2d_1.replace_inline_data(freq_vec, amplitude)
                plot2d_2.replace_inline_data(freq_vec, phase)
                # plot2d_3.replace_inline_data(freq_vec, real_a)
                # plot2d_4.replace_inline_data(freq_vec, imag_a)

        Tabor.set_trigger_source('EVEN')
        ats9360.measurement_close(transfert_info=False)
        board_flag = False

    finally:
        if board_flag:
            ats9360.measurement_close(transfert_info=False)

        data_measurement.add_data_point(freq_vec, amplitude, phase, real_a, imag_a)
        data_measurement.close_file()

        print ats9360.measurement_close(transfert_info=True)
        smb_atom.set_freqsweep('OFF')
        smb_atom.set_gui_update('ON')
        smb_cavity.set_gui_update('ON')
        Tabor.set_trigger_source('EVEN')

        #turn back this parameter
        SSB_cavity.set_band_type(-1)

        data_fit= qt.Data(name='twotone_fit')
        data_fit.add_value('parameters ',            units = 'none, none, GHz, Volt')
        data_fit.add_value('errors ',            units = 'none, none, GHz, Volt')
        data_fit.create_file()

        s = fit.Lorentzian()
        signal = amplitude
        s.set_data(freq_vec, signal)
        # guess parameters##########################################################
        bg = 0
        area = 1.
        f0 = freq_vec[argmin(signal)]
        width = 0.02
        p = [bg, area, f0, width]
        # fitting ##################################################################
        p = s.fit(p)
        values_from_fit = s.func(p)
        print 'params:', s.get_fit_params()
        print 'errors:', s.get_fit_errors()

        data_fit.add_data_point(s.get_fit_params(),s.get_fit_errors())
        if graph:
            plot2d_1.add(freq_vec, values_from_fit)
        data_fit.close_file()

    if graph:
        plot2d_1.save_png()
        plot2d_2.save_png()
    qt.mend()

    p = s.get_fit_params()
    f0 = p[2]

    # smb_cavity_off()
    all_smb_off()
    #work if the peak is down!
    # if abs( np.mean(amplitude)-np.min(amplitude) )  <  3*np.std(amplitude):
    #     '_____twotone didnt find peak'
    #     return None

    # if (f0<f_min) or (f0>f_max):    # if fitted frequency is outside of measured window
    #     print "Fitted resonance ", f0, "is outside of freq window"
    #     return None

    if Return_fq_only:
        print 'Return_fq_only'
        return f0
    else:
        print 'retrun data'
        return [freq_vec, amplitude, phase]

def get_twotone_vs_current(cur_min, cur_max, cur_step, f_cav, f_min=2.1, f_max=2.4, nop=200, Tabor_loading = 1, graph = True, averaging = 5e3, use_res_fit = False):
    '''
    For search for sweet spot
    If use_res_fit then we set fread by using a polynomial fit (which has to be done manually on a onetone vs flux measurement)
    '''
    qt.mstart()

    fit_params = [ 0.008008, -0.015369, -0.020198, 0.045192, 0.020394, -0.044318, -0.007903, 7.192717 ]
    fread_shift = 5e-3

    data_measurement = qt.Data(name='Twotone_Spectroscopy_vs_flux')
    data_measurement.add_coordinate('2nd tone freq [GHz]', units = 'GHz')
    data_measurement.add_coordinate('Current [uA]', units = 'mA')
    data_measurement.add_value('S21 ',            units = 'Volt')
    data_measurement.add_value('Phase ',            units = 'rad')
    data_measurement.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'S21 ',
                      coorddim  = (0,1),
                      valdim    = 2)
    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'Phase ',
                      coorddim  = (0,1),
                      valdim    = 3)

    cur_list = []
    freq_arr_list = []
    ampl_arr_list = []
    phase_arr_list = []
    try:
        for curcur in np.arange(cur_min, cur_max, cur_step):
            set_qub_cur(curcur)
            qt.msleep(0.1)

            if use_res_fit:
                curcur_mA = curcur*1e3
                f_cav = np.polyval(fit_params, curcur_mA)
                # fcav += fread_shift
                print("Cavity-like polariton is at " + str(f_cav) + "GHz at " + str(curcur_mA) + "mA")

            # [freq_vec, amplitude, phase] = get_twotone_fqub(f_cav, Return_fq_only=False, f_min=f_min, f_max=f_max, Tabor_loading=Tabor_loading, graph=graph, averaging=averaging)
            [freq_vec, amplitude, phase] = get_twotone_fqub(f_cav, Return_fq_only=False, nop=nop, f_min=f_min, f_max=f_max, Tabor_loading=Tabor_loading, graph=graph, averaging=averaging)

            data_measurement.add_data_point(freq_vec, 1e3*curcur*np.ones_like(freq_vec), amplitude, phase)
            data_measurement.new_block()

            cur_list.append(curcur)
            freq_arr_list.append( freq_vec )
            ampl_arr_list.append( amplitude )
            phase_arr_list.append( phase )
    finally:
        data_measurement.close_file()
        plot3d_1.save_png()
        plot3d_2.save_png()
        qt.mend()
        # smb_cavity_off()
        all_smb_off()

    print cur_list, freq_arr_list, ampl_arr_list, phase_arr_list

    return [cur_list, freq_arr_list, ampl_arr_list, phase_arr_list]

def get_rabi_pi(parameters, power2, tl = 1, averaging=500, nom_expect = 0, window = 1200, nop=400.0, graph=True, awg_offset=AWG_OFFSET, Return_tpi_only=True, Return_trabi=False):
    '''
    Return time of pi-pulse in seconds: tpi = 30e-9
    takes object of parameters class and power2
    '''
    # smb_cavity_on()
    all_smb_on()

    pow2 = 7        ### ADDED on 20211126

    qt.msleep(0.1)
    FIT = True
    print 'power smb atom-1:', smb_atom.get_power()

    try:
        Tabor_loading = tl
        GausSigma = parameters.nsigma
        tr_start = 0e-9
        tr_stop = window*1e-9
        tr_step = round( abs(tr_stop - tr_start)/nop,  9 ) ##[s]
        power1 = parameters.power1
        #power2 = parameters.power2
        f_atom = parameters.freq_q
        f_cav = parameters.freq_read
        t_meas = parameters.t_read

    except:
        print 'WARNING: (rabi) one of parameters is not defined!'
        return None

    try:
        delta_t = 200
        acq_time = t_meas*1e9 + delta_t + 300.
        t_wait = 0e-9
        T_vec = np.arange(tr_start, tr_stop, tr_step)
        if nop != len(T_vec):
            print "nop changed from ", nop, "to ", len(T_vec)
            nop = len(T_vec)
        nb_sequences = len(T_vec)
        t_rise = None
    except:
        print 'WARNING: (rabi) problem of setting'
        return None

    ###########################################################
    try:
        mw = 2
        Pulsing_instrument.set_routing_awg({'secondtone_channel':4})

        if Tabor_loading:
            if COMMENTS:
                print 'Tabor loading'
            Pulsing_instrument.set_trigger_time(100.)
            if GausSigma < 0:
                GausSigma = 0
                print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
            if GausSigma > 5:
                GausSigma = 5
                print 'Warning_Fidelity: Gaussigma was >5, changed to 5'
            if GausSigma > 0:
                    if COMMENTS:
                        print 'gaussian form!'
            #gaussian pulse
            Pulsing_instrument.write_Rabi_pulsessequence(tr_stop, tr_step, tr_start, t_meas,
                t_wait=t_wait, delta_m1_start=0.1e-6, phi=0, delete='all', t_rise =t_rise, nsigma=GausSigma)
            Tabor.set_ch1_offset(awg_offset)
        qt.mstart()
    except:
        print 'WARNING: (rabi) problem of Tabor loading'
        return None

    parameters.save(name='parameters_Rabi')

    data_measurement = qt.Data(name='Rabi_')
    data_measurement.add_coordinate('excitation time [ns]', units = 'ns')
    data_measurement.add_value('S21 [mV]',            units = 'mV')
    data_measurement.add_value('Phase [rad]',            units = 'rad')
    data_measurement.add_value('Re [mV]',            units = 'mV')
    data_measurement.add_value('Im [mV]',            units = 'mV')
    data_measurement.add_value('Dist [mV]',            units = 'mV')
    data_measurement.create_file()



    try:
        if graph:
            plot2d_5 = qt.Plot2D(data_measurement,
                              name      = 'Rabi distance',
                              coorddim  = 0,
                              valdim    = 5)
            plot2d_3 = qt.Plot2D(data_measurement,
                              name      = 'Re rabi',
                              coorddim  = 0,
                              valdim    = 3,
                              maxtraces = 2)
            plot2d_4 = qt.Plot2D(data_measurement,
                                name      = 'Im rabi',
                                coorddim  = 0,
                                valdim    = 4,
                                maxtraces = 2)
        if FIT:
            data_fit = qt.Data(name='Rabi_OSC_fit')
            data_fit.add_value('parameters ',            units = 'rad, rad, GHz*2pi, rad, ns')
            data_fit.add_value('errors ',            units = 'rad, rad, GHz*2pi, rad, ns')
            data_fit.create_file()

    except:
        print 'WARNING: (rabi) problem with plot the graph'

    try:

        Pulsing_instrument.prep_rabi(f_cav, f_atom, averaging, nb_sequences,
            power1, power2, acq_time, t_meas*1e9, delta_t, mw =mw)

        smb_atom.set_power(pow2)        ### ADDED on 20211126

        if COMMENTS:
            print 'Rabi_sequence was prepared'
        qt.msleep(2.1)
        Tabor.set_trigger_source('TIM')
        cycle_counter = 0

        while Pulsing_instrument.get_acquisition_completed() !=100.:
            #print  Pulsing_instrument.get_acquisition_completed(), '%' #!V
            result = Pulsing_instrument.measurement()
            ((real_a, rea0), (imag_a, ima0))= result
            real_a -= rea0
            imag_a -= ima0 #deduction of background V?

            ### convert to mV ###
            real_a = 1e3*real_a
            imag_a = 1e3*imag_a

            ### processing ###
            amplitude = np.sqrt(real_a**2+imag_a**2)
            complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase = np.angle(complexe)

            # ############# NORM ############### (not used here)
            # covMat = np.cov(real_a, imag_a)
            # eigenValue, eigenVector = np.linalg.eig(covMat)
            # norm_a = eigenVector[0,0]*imag_a + eigenVector[0,1]*real_a  ##ok 0 : +8

            qt.msleep(0.1)

            # Real part used for nom_expect now
            if FIT:
                ######### AMPL #################### # CHANGED on 06/23/2021
                s = fit.ExponentialDecaySine()
                signal = amplitude
                s.set_data(T_vec*1e9, signal)
                # guess parameters##############################################
                background = (signal.max() + signal.min() )/2.
                osc_amp = (signal.max() - signal.min() )/2.
                # nb_expected_oscillation = 10.
                # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
                nb_expected_oscillation = estimate_nb_oscillations(signal)
                pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
                # pulsation = 2*np.pi*qub_detuning          # CHANGED on 06/23/2021
                phio = 0.
                decaytime = 1000.
                p0 = [background, osc_amp, pulsation, phio, decaytime]
                # fitting ######################################################
                p = s.fit(p0)
                p[4] = abs(p[4]) ## no negative T2
                p_err = s.get_fit_errors()
                values_from_fit = s.func(p)
                amp_values_from_fit = values_from_fit
                amp_p = p
                amp_p_err = p_err

                ############ COMPUTE DIST (from fit) ###############
                # dist_a = np.sqrt(  (real_a-real_a[0])**2 + (imag_a-imag_a[0])**2  )
                id_ref = np.argmin(amp_values_from_fit)                 # CHANGED on 06/23/2021
                dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )

                ####   DISTANCE!############################################################
                # guess parameters##########################################################
                phio = 0.
                decaytime = 1000.
                s = fit.ExponentialDecaySine()
                s.set_data(T_vec*1e9, dist_a)
                background_dist = sum(dist_a)/len(dist_a)
                osc_dist = (dist_a.max() - dist_a.min() )/2.

                #autosearch of nom_expect
                if nom_expect == 0:
                    #!V 180824 automaticaly counts Rabi-pulses
                    # nom_cross = 0
                    # for i in np.arange(3, len(dist_a)):
                    #     #s[i] positive sign or not
                    #     s0 = dist_a[i-3] > background_dist
                    #     s1 = dist_a[i-2] > background_dist
                    #     s2 = dist_a[i-1] > background_dist
                    #     s3 = dist_a[i]   > background_dist
                    #     if (s0==s1 and s2==s3 and s1!=s3):
                    #         nom_cross = nom_cross +1
                    # nb_expected_oscillation = nom_cross/2
                    nb_expected_oscillation = estimate_nb_oscillations(dist_a)      # CHANGED on 06/23/2021
                    pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation

                p0 = [background_dist, osc_dist, pulsation, phio, decaytime]
                # fitting ##################
                p = s.fit(p0)
                dist_values_from_fit = s.func(p)
                tpi_dist = np.pi/p[2]
                error_dist = s.get_fit_errors()
                trabi = p[-1]*1e-9 # decay time in ns

                if graph:
                    # plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
                    # plot2d_2.replace_inline_data(T_vec*1e9, phase)
                    #plot2d_3.replace_inline_data(T_vec*1e9, real_a)
                    #plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
                    plot2d_5.replace_inline_data_y2(T_vec*1e9, dist_a, dist_values_from_fit )
                    plot2d_5.set_plottitle('Fq: '+str(parameters.freq_q)+'GHz; ' +'rdt2: '+str(parameters.rudat2)+'dB;  ' +'pwr2: '+str( round(power2,2) )  +'; nsig: '+str(parameters.nsigma) +';  ->   T_pi= '+str( round(tpi_dist, 4) )+' ns;  ' + 'T_Rabi= '+str( round(p[4],2) )+' ns')
            # ####### END OF FIT###########################################################

            else:
                ############ COMPUTE DIST (from raw data) ###############
                # dist_a = np.sqrt(  (real_a-real_a[0])**2 + (imag_a-imag_a[0])**2  )     # CHANGED on 06/23/2021
                id_ref = np.argmin(amplitude)
                dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )

            if graph:
                # plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
                # plot2d_2.replace_inline_data(T_vec*1e9, phase)
                #plot2d_3.replace_inline_data(T_vec*1e9, real_a)
                #plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
                plot2d_5.replace_inline_data(T_vec*1e9, dist_a)

        Tabor.set_trigger_source('EVEN')
        if Pulsing_instrument.get_board_flag():
            Pulsing_instrument.measurement_close(transfert_info=False)

    except:
        print 'WARNING: (rabi) An error ocurred:'
        e = sys.exc_info()[1]
        print e.args[0]
    finally:
        if Pulsing_instrument.get_board_flag():
            Pulsing_instrument.measurement_close(transfert_info=False)

        data_measurement.add_data_point(T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a)
        data_measurement.close_file()
        if COMMENTS:
            print Pulsing_instrument.measurement_close(transfert_info=True)
        else:
            Pulsing_instrument.measurement_close(transfert_info=True)

        Tabor.set_trigger_source('EVEN')

    if FIT:
        if graph:         # CHANGED on 06/23/2021
            # plot2d_1.add(T_vec*1e9, am_values_from_fit)
            # plot2d_2.add(T_vec*1e9, ph_values_from_fit)
            # plot2d_3.add(T_vec*1e9, re_values_from_fit)
            # plot2d_4.add(T_vec*1e9, im_values_from_fit)
            plot2d_5.add(T_vec*1e9, dist_values_from_fit)
        data_fit.add_data_point( s.get_fit_params(), s.get_fit_errors())
        data_fit.close_file()


    if graph:
        # plot2d_1.save_png()
        # plot2d_2.save_png()
        plot2d_3.save_png()
        plot2d_4.save_png()
        plot2d_5.save_png()

    # this is empirical...
    if COMMENTS:
        print 'distance=', round(np.sqrt((real_a[9]-real_a[0])**2 + (imag_a[9]-imag_a[0])**2)*1e3, 2), T_vec[9]*1e9

    qt.mend()

    # smb_cavity_off()
    all_smb_off()
    if Return_tpi_only:     #in most cases
        tpi = tpi_dist*1e-9
        if Return_trabi:
            return tpi, trabi
        return tpi
    else:
        return [1e9*T_vec, amplitude, phase, real_a, imag_a, dist_a]

def get_rabi_shevrones(parameters, averaging=0.5e3, fr_vec = np.arange(2.0, 3.0, 2e-3), window = 4000, nop=20.0, tl=1, awg_offset=AWG_OFFSET):
    '''
    Return time of pi-pulse in seconds: tpi = 30e-9
    takes object of parameters class and power2
    '''
    try:
        Tabor_loading = tl
        GausSigma = parameters.nsigma
        tr_start = 0e-9
        tr_stop = window*1e-9
        tr_step = round( abs(tr_stop - tr_start)/nop,  9 ) ##[s]
        power1 = parameters.power1
        power2 = parameters.power2
        f_atom = parameters.freq_q
        f_cav = parameters.freq_read
        t_meas = parameters.t_read
    except:
        print 'WARNING: (rabi-shevrones) one of parameters is not defined!'
        return None

    try:
        delta_t = 200
        acq_time = t_meas*1e9 + delta_t + 300.
        t_wait = 0e-9
        T_vec = np.arange(tr_start, tr_stop, tr_step)
        if nop != len(T_vec):
            print "nop changed from ", nop, "to ", len(T_vec)
            nop = len(T_vec)
        nb_sequences = len(T_vec)
        t_rise = None
    except:
        print 'WARNING: (rabi-shevrones) problem of setting'
        return None

    ###########################################################
    # smb_cavity_on()
    all_smb_on()
    qt.msleep(0.1)

    try:
        mw = 2
        Pulsing_instrument.set_routing_awg({'secondtone_channel':4})

        if Tabor_loading:
            print 'Tabor loading'
            Pulsing_instrument.set_trigger_time(100.)
            Pulsing_instrument.write_Rabi_pulsessequence(tr_stop, tr_step, tr_start, t_meas,
                t_wait=t_wait, delta_m1_start=0.1e-6, phi=0, delete='all', t_rise =t_rise, nsigma=GausSigma)
            Tabor.set_ch1_offset(awg_offset)

    except:
        print 'WARNING: (rabi) problem of Tabor loading'
        return None

    parameters.save(name='parameters_Rabi-shevron')

    data_measurement = qt.Data(name='Rabi_shevron')
    data_measurement.add_coordinate('Frequency pump',       units = 'GHz')
    data_measurement.add_coordinate('excitation time [ns]', units = 'ns')
    data_measurement.add_value('S21 [mV]',           units = 'mV')
    data_measurement.add_value('Phase [rad]',        units = 'rad')
    data_measurement.add_value('Re [mV]',            units = 'mV')
    data_measurement.add_value('Im [mV]',            units = 'mV')
    data_measurement.add_value('Dist [mV]',          units = 'mV')
    data_measurement.create_file()


    # plot2d_1 = qt.Plot2D(data_measurement,
    #                 name      = 'Re rabi',
    #                 coorddim  = 1,
    #                 valdim    = 2,
    #                 maxtraces = 2)
    # plot2d_2 = qt.Plot2D(data_measurement,
    #                 name      = 'Im rabi',
    #                 coorddim  = 1,
    #                 valdim    = 3,
    #                 maxtraces = 2)
    plot2d_3 = qt.Plot2D(data_measurement,
                    name      = 'Re rabi',
                    coorddim  = 1,
                    valdim    = 4,
                    maxtraces = 2)
    plot2d_4 = qt.Plot2D(data_measurement,
                    name      = 'Im rabi',
                    coorddim  = 1,
                    valdim    = 5,
                    maxtraces = 2)
    plot2d_5 = qt.Plot2D(data_measurement,
                    name      = 'Rabi distance',
                    coorddim  = 1,
                    valdim    = 6,
                    maxtraces = 2)

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'Rabi distance colorplot',
                      coorddim  = (0,1),
                      valdim    = 6)

    start_shevrones_time = datetime.datetime.now()

    for f_atom in fr_vec:
        start_loop_time = datetime.datetime.now()

        print 'f_atom is: ', round(f_atom, 3)

        try:
            qt.mstart()
            Pulsing_instrument.prep_rabi(f_cav, f_atom, averaging, nb_sequences,
                power1, power2, acq_time, t_meas*1e9, delta_t, mw =mw)
            qt.msleep(2.1)
            Tabor.set_trigger_source('TIM')
            cycle_counter = 0
            while Pulsing_instrument.get_acquisition_completed() !=100.:
                result = Pulsing_instrument.measurement()
                ((real_a, rea0), (imag_a, ima0))= result
                real_a -= rea0
                imag_a -= ima0 #deduction of background V?

                ### convert to mV ###
                real_a = 1e3*real_a
                imag_a = 1e3*imag_a

                ### processing ###
                amplitude = np.sqrt(real_a**2+imag_a**2)
                complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
                phase = np.angle(complexe)
                dist_a = np.sqrt(  (real_a-real_a[0])**2 + (imag_a-imag_a[0])**2  )

                qt.msleep(0.1)

                # plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
                # plot2d_2.replace_inline_data(T_vec*1e9, phase)
                # plot2d_3.replace_inline_data(T_vec*1e9, real_a)
                # plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
                plot2d_5.replace_inline_data(T_vec*1e9, dist_a)

            Tabor.set_trigger_source('EVEN')
            if Pulsing_instrument.get_board_flag():
                Pulsing_instrument.measurement_close(transfert_info=False)

        except:
            print 'WARNING: (rabi-shevrones) An error ocurred:'
            e = sys.exc_info()[1]
            print e.args[0]

        finally:
            if Pulsing_instrument.get_board_flag():
                Pulsing_instrument.measurement_close(transfert_info=False)
            Pulsing_instrument.measurement_close(transfert_info=True)
            Tabor.set_trigger_source('EVEN')
            data_measurement.add_data_point(f_atom*np.ones_like(T_vec), T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a)
            data_measurement.new_block()

        stop_loop_time = datetime.datetime.now()
        print "loop done in: ", stop_loop_time - start_loop_time

    print 'all cycle is done'
    data_measurement.close_file()

    # plot2d_1.save_png()
    # plot2d_2.save_png()
    plot2d_3.save_png()
    plot2d_4.save_png()
    plot2d_5.save_png()
    plot3d_1.save_png()

    qt.mend()
    # smb_cavity_off()
    all_smb_off()

    # stop_shevrones_time = datetime.datetime.now()
    # delta_time = stop_shevrones_time - start_shevrones_time
    # print "Total time: ", delta_time
    print "Total time: ", datetime.datetime.now() - start_shevrones_time

    return [T_vec, amplitude, phase, real_a, imag_a, dist_a]

def get_twotone_vs_rudat2(parameters, rudat2_vec, f_min=2.1, f_max=2.5, av=1e3,  nop=300, awg_offset=AWG_OFFSET):
    initial_rudat2 = parameters.rudat2

    data_measurement = qt.Data(name='Twotone_vs_rudatQ')
    data_measurement.add_coordinate('Rudat2 [dB]', units = 'dB')
    data_measurement.add_coordinate('Frequency pump',       units = 'GHz')
    data_measurement.add_value('S21 [mV]',           units = 'mV')
    data_measurement.add_value('Phase [rad]',        units = 'rad')
    data_measurement.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'Twotone vs RudatQ S21 colorplot',
                      coorddim  = (0,1),
                      valdim    = 2)
    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'Twotone vs RudatQ Phase colorplot',
                      coorddim  = (0,1),
                      valdim    = 3)

    try:
        tl = 1

        for i in range(len( rudat2_vec ) ):
            parameters.set_rudat2(rudat2_vec[i])
            res = get_twotone_fqub(parameters.freq_read, f_min=f_min, f_max=f_max, nop=nop, Tabor_loading = tl, graph = True, averaging = av, awg_offset=awg_offset, Return_fq_only=False)
            # return res
            [freq_vec, amplitude, phase] = res
            dist_arr = np.zeros(( len(rudat2_vec), len(freq_vec) ))
            dist_arr[i] = amplitude
            tl = 0
            data_measurement.add_data_point(rudat2_vec[i]*np.ones_like(freq_vec), freq_vec, amplitude, phase)
            data_measurement.new_block()
            # plot3d_1.replace_inline_data(T_vec*1e9, dist_a)

    finally:
        parameters.set_rudat2(initial_rudat2)
        plot3d_1.save_png()
        plot3d_2.save_png()
        data_measurement.close_file()

    # try:
    # plt.figure()
    # plt.pcolor( rudat2_vec, freq_vec, np.transpose(dist_arr) )
    # plt.show()
    # # except:
    #     print 'error of plotting !!'


    print( ' return [ freq_vec, dist_arr]' )
    return [ freq_vec, dist_arr]

def get_rabi_pi_bench(parameters, power2, tl=1, averaging=500, N_pi=60, start_Pi=0, step_Pi=0.5, awg_offset=AWG_OFFSET ):
    '''
    Return time of pi-pulse in seconds: tpi = 30e-9
    takes object of parameters class and power2
    '''
    # smb_cavity_on()
    all_smb_on()

    qt.msleep(0.1)
    print 'power smb atom-1:', smb_atom.get_power()

    try:
        Tabor_loading = tl
        GausSigma = parameters.nsigma
        power1 = parameters.power1
        #power2 = parameters.power2
        f_atom = parameters.freq_q
        f_cav = parameters.freq_read
        t_meas = parameters.t_read
        tpi = parameters.tpi

        N_vec = np.arange(start_Pi, N_pi, step_Pi) #0pi, 1pi, 2pi ...
        nop = len(N_vec)
        if nop > 400:
            print "Too long vector"
            return None

        tr_step = tpi *step_Pi
        T_vec = N_vec * tr_step
        tr_start = T_vec[0]
        tr_stop = T_vec[-1]


    except:
        print 'WARNING: (rabi) one of parameters is not defined!'
        return None

    try:
        delta_t = 200
        acq_time = t_meas*1e9 + delta_t + 300.
        t_wait = 0e-9

        if nop != len(T_vec):
            print "nop changed from ", nop, "to ", len(T_vec)
            nop = len(T_vec)
        nb_sequences = len(T_vec)
        t_rise = None
    except:
        print 'WARNING: (rabi) problem of setting'
        return None

    ###########################################################
    try:
        mw = 2
        Pulsing_instrument.set_routing_awg({'secondtone_channel':4})

        if Tabor_loading:
            if COMMENTS:
                print 'Tabor loading'
            Pulsing_instrument.set_trigger_time(100.)
            if GausSigma < 0:
                GausSigma = 0
                print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
            if GausSigma > 5:
                GausSigma = 5
                print 'Warning_Fidelity: Gaussigma was >5, changed to 5'
            if GausSigma > 0:
                    if COMMENTS:
                        print 'gaussian form!'
            #gaussian pulse
            Pulsing_instrument.write_Rabi_pulsessequence(tr_stop, tr_step, tr_start, t_meas,
                t_wait=t_wait, delta_m1_start=0.1e-6, phi=0, delete='all', t_rise =t_rise, nsigma=GausSigma)
            Tabor.set_ch1_offset(awg_offset)
        qt.mstart()
    except:
        print 'WARNING: (rabi) problem of Tabor loading'
        return None

    parameters.save(name='parameters_Rabi')

    data_measurement = qt.Data(name='Rabi_')
    data_measurement.add_coordinate('Num of pi', units = '#')
    data_measurement.add_coordinate('excitation time [ns]', units = 'ns')
    data_measurement.add_value('S21 [mV]',            units = 'mV')
    data_measurement.add_value('Phase [rad]',            units = 'rad')
    data_measurement.add_value('Re [mV]',            units = 'mV')
    data_measurement.add_value('Im [mV]',            units = 'mV')
    data_measurement.add_value('Dist [mV]',            units = 'mV')
    data_measurement.create_file()



    try:
        plot2d_3 = qt.Plot2D(data_measurement,
                          name      = 'Bench Re rabi',
                          coorddim  = 0,
                          valdim    = 4)
        plot2d_3.set_style('steps')

        plot2d_4 = qt.Plot2D(data_measurement,
                            name      = 'Bench Im rabi',
                            coorddim  = 0,
                            valdim    = 5)
        plot2d_4.set_style('steps')

        plot2d_5 = qt.Plot2D(data_measurement,
                          name      = 'Bench Rabi distance',
                          coorddim  = 0,
                          valdim    = 6)
        plot2d_5.set_style('steps')


    except:
        print 'WARNING: (rabi) problem with plot the graph'

    try:

        Pulsing_instrument.prep_rabi(f_cav, f_atom, averaging, nb_sequences,
            power1, power2, acq_time, t_meas*1e9, delta_t, mw =mw)

        if COMMENTS:
            print 'Rabi_sequence was prepared'
        qt.msleep(2.1)
        Tabor.set_trigger_source('TIM')
        cycle_counter = 0

        while Pulsing_instrument.get_acquisition_completed() !=100.:
            #print  Pulsing_instrument.get_acquisition_completed(), '%' #!V
            result = Pulsing_instrument.measurement()
            ((real_a, rea0), (imag_a, ima0))= result
            real_a -= rea0
            imag_a -= ima0 #deduction of background V?

            ### convert to mV ###
            real_a = 1e3*real_a
            imag_a = 1e3*imag_a

            ### processing ###
            amplitude = np.sqrt(real_a**2+imag_a**2)
            complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase = np.angle(complexe)
            dist_a = np.sqrt(  (real_a-real_a[0])**2 + (imag_a-imag_a[0])**2  )

            qt.msleep(0.1)


            plot2d_3.replace_inline_data(N_vec, real_a)
            plot2d_4.replace_inline_data(N_vec, imag_a)
            plot2d_5.replace_inline_data(N_vec, dist_a)

        Tabor.set_trigger_source('EVEN')
        if Pulsing_instrument.get_board_flag():
            Pulsing_instrument.measurement_close(transfert_info=False)

    except:
        print 'WARNING: (rabi) An error ocurred:'
        e = sys.exc_info()[1]
        print e.args[0]
    finally:
        data_measurement.add_data_point( N_vec, T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a )
        data_measurement.close_file()


        if Pulsing_instrument.get_board_flag():
            Pulsing_instrument.measurement_close(transfert_info=False)

        if COMMENTS:
            print Pulsing_instrument.measurement_close(transfert_info=True)
        else:
            Pulsing_instrument.measurement_close(transfert_info=True)

        Tabor.set_trigger_source('EVEN')


        plot2d_3.save_png()
        plot2d_4.save_png()
        plot2d_5.save_png()

    # this is empirical...
    if COMMENTS:
        print 'distance=', round(np.sqrt((real_a[9]-real_a[0])**2 + (imag_a[9]-imag_a[0])**2)*1e3, 2), T_vec[9]*1e9

    qt.mend()

    # smb_cavity_off()
    all_smb_off()
    return [N_vec, 1e9*T_vec, amplitude, phase, real_a, imag_a, dist_a]

def get_rabi_pi_bench_colorplot(parameters, tl=1, av=500, N_pi=60, start_Pi=0, step_Pi=0.5, power2_vec=np.arange(-0.0, -0.5, -0.1)):
    data_measurement = qt.Data(name='Rabi_Benchmark_vs_power2')
    data_measurement.add_coordinate('power2', units = 'V')
    data_measurement.add_coordinate('N_pi', units = 'num')
    data_measurement.add_value('Re',            units = 'Volt')
    data_measurement.add_value('Im',            units = 'Volt')
    data_measurement.add_value('Dist',          units = 'Volt')
    data_measurement.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'Re Rabi bench 3D',
                      coorddim  = (1,0),
                      valdim    = 2)

    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'Im Rabi bench 3D',
                      coorddim  = (1,0),
                      valdim    = 3)

    plot3d_3 = qt.Plot3D(data_measurement,
                      name      = 'Dist Rabi bench 3D',
                      coorddim  = (1,0),
                      valdim    = 4)

    for power2 in power2_vec:
        data = get_rabi_pi_bench(parameters, power2, tl=tl, N_pi=N_pi, start_Pi=start_Pi, step_Pi=step_Pi, averaging=av)
        # tl = 0 ## not sure we can do it

        N_vec = data[0]
        Re = data[4]
        Im = data[5]
        Dist = data[6]
        data_measurement.add_data_point( power2*np.ones_like(N_vec), N_vec, Re, Im, Dist)
        data_measurement.new_block()

    plot3d_1.save_png()
    plot3d_2.save_png()
    plot3d_3.save_png()
    data_measurement.close_file()



def get_ramsey_df_backup_20210622(parameters, qub_detuning=0.0, tl =1, averaging = 3e3, window=4000, nop = 200,  graph=True, awg_offset=AWG_OFFSET, Return_all_data=False, Return_extracted_values=True):
    '''
    takes parameters
    makes ramsey measurement
    return delta frequency in Ghz
    (use ONLY non-gaussian pi-pulse calibration)
    '''
    # smb_cavity_on()
    all_smb_on()

    if qub_detuning != 0.0:
        fq_init = parameters.freq_q
        parameters.freq_q = fq_init + 1e-3*qub_detuning

    if COMMENTS:
        print 'Ramsey, freq-q=', parameters.freq_q
    #returns frequency diference to f_q
    df=0
    FIT = True
    try:
        Tabor_loading = tl
        power1 = parameters.power1
        power2 = parameters.power2
        f_atom = parameters.freq_q
        f_cav = parameters.freq_read
        t_meas = parameters.t_read
        tpi = parameters.tpi
        GausSigma = parameters.nsigma
        if GausSigma !=0:
            print 'Ramsey: pi pulse is gaussian'
    except:
        print 'WARNING: (ramsey) one of parameters is not defined!'
        return None

    #t_pi_o2 = 1e-9 * math.floor(tpi/2) # we define the excitation time for a pi over 2 pulse on the qubit
    t_pi_o2 = 1e-9*int( 1e9*tpi/2 ) #should be in sec
    if COMMENTS:
        print 't_pi_o2: ', t_pi_o2
    delta_t = 200 # not to touch for now
    acq_time = t_meas*1e9 + delta_t + 300. # not to touch for now

    # We define the time vector of the Ramsey measurement:
    if (window > 100) and (window<20000):
        tr_stop = window*1e-9
        tr_step = round( tr_stop/nop,  9 ) ##[s]
    else:
        tr_stop = 1e-6 # in s
        tr_step = 5e-9 # in s
    tr_start = 0e-6 # in s
    T_vec = np.arange(tr_start, tr_stop, tr_step)
    if nop != len(T_vec):
        print "nop changed from ", nop, "to ", len(T_vec)
        nop = len(T_vec)

    nb_sequences = len(T_vec) # we define the number of sequences to acquire for the board.

    t_wait = 0e-9
    t_rise = None
    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################

    if Tabor_loading:
        # here we write in the AWG memory if the condition Tabor_loading is True
        if COMMENTS:
            print 'Tabor loading...'

        if GausSigma < 0:
            GausSigma = 0
            print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
        if GausSigma > 5:
            GausSigma = 5
            print 'Warning_Fidelity: Gaussigma was >5, changed to 5'

        Pulsing_instrument.set_trigger_time(100.)
        Pulsing_instrument.write_Ramsey_pulsessequence(t_pi_o2, tr_stop, tr_step,
                tr_start, t_meas, t_wait=t_wait, delete='all', t_rise =t_rise, nsigma=GausSigma )
        Tabor.set_ch1_offset(awg_offset)


    qt.mstart()

    parameters.save(name='parameters_Ramsey')

    data_measurement = qt.Data(name='Ramsey')
    data_measurement.add_coordinate('waiting time [ns]', units = 'ns')
    data_measurement.add_value('S21 [mV]',            units = 'mV')
    data_measurement.add_value('Phase [rad]',            units = 'rad')
    data_measurement.add_value('Re [mV]',            units = 'mV')
    data_measurement.add_value('Im [mV]',            units = 'mV')
    data_measurement.add_value('Dist [mV]',            units = 'mV')
    data_measurement.create_file()

    if graph:
        # plot2d_1 = qt.Plot2D(data_measurement,
        #                   name      = 'S21 ramsey',
        #                   coorddim  = 0,
        #                   valdim    = 1,
        #                   maxtraces = 2)
        # plot2d_2 = qt.Plot2D(data_measurement,
        #                     name      = 'Phase ramsey',
        #                     coorddim  = 0,
        #                     valdim    = 2,
        #                     maxtraces = 2)
        plot2d_3 = qt.Plot2D(data_measurement,
                          name      = 'Re ramsey',
                          coorddim  = 0,
                          valdim    = 3,
                          maxtraces = 2)
        plot2d_4 = qt.Plot2D(data_measurement,
                            name      = 'Im ramsey',
                            coorddim  = 0,
                            valdim    = 4,
                            maxtraces = 2)
        plot2d_5 = qt.Plot2D(data_measurement,
                            name      = 'Ramsey distance',
                            coorddim  = 0,
                            valdim    = 5,
                            maxtraces = 2)

    if FIT:
        data_fit = qt.Data(name='Ramsey_OSC_fit')
        data_fit.add_value('parameters ',            units = 'rad, rad, GHz*2pi, rad, ns')
        data_fit.add_value('errors ',            units = 'rad, rad, GHz*2pi, rad, ns')
        data_fit.create_file()

    # try:
    Pulsing_instrument.prep_rabi(f_cav, f_atom, averaging, nb_sequences,
        power1, power2, acq_time, t_meas*1e9, delta_t) #rabi.. ?
    # Pulsing_instrument.prep_ramsey(f_cav, f_atom, averaging, nb_sequences, power1, power2)
    qt.msleep(3)
    Tabor.set_trigger_source('TIM')
    while Pulsing_instrument.get_acquisition_completed() != 100.:
        #print  Pulsing_instrument.get_acquisition_completed(), '%'

        result = Pulsing_instrument.measurement()
        ((real_a, rea0), (imag_a, ima0))= result
        real_a -= rea0
        imag_a -= ima0

        ### convert to mV ###
        real_a = 1e3*real_a
        imag_a = 1e3*imag_a

        amplitude = np.sqrt(real_a**2+imag_a**2)

        complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
        phase = np.angle(complexe)
        dist_a = np.sqrt(  (real_a-real_a[0])**2 + (imag_a-imag_a[0])**2  )

        qt.msleep(0.1)
        if graph:
            # plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
            # plot2d_2.replace_inline_data(T_vec*1e9, phase)
            plot2d_3.replace_inline_data(T_vec*1e9, real_a)
            plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
            plot2d_5.replace_inline_data(T_vec*1e9, dist_a)

        if FIT:
            ######### REAL ####################
            s = fit.ExponentialDecaySine()
            signal = real_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters##########################################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            nb_expected_oscillation = 4.
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            phio = 0.
            decaytime = 1000.
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting ##################################################################
            p = s.fit(p0)
            values_from_fit = s.func(p)
            if graph:
                plot2d_3.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_3.set_plottitle('T2= '+ str(round(p[4],2)) +' ns'+',   Freq_detun= '+ str(round( p[2]/2/np.pi*1e3, 5 ))+' MHz,   Probe_Freq='+str(round( 1e3*f_atom, 1 ))+'MHz'  )
            ######### IMAG ####################
            s = fit.ExponentialDecaySine()
            signal = imag_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters##########################################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            nb_expected_oscillation = 10.
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            phio = 0.
            decaytime = 1000.
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting ##################################################################
            p = s.fit(p0)
            values_from_fit = s.func(p)
            if graph:
                plot2d_4.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                # plot2d_4.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
                plot2d_4.set_plottitle('T2= '+ str(round(p[4],2)) +' ns'+',   Freq_detun= '+ str(round( p[2]/2/np.pi*1e3,5 ))+' MHz,   Probe_Freq='+str(round( 1e3*f_atom ))+'MHz'  )
            ######### AMPL ####################
            # s = fit.ExponentialDecaySine()
            # signal = amplitude
            # s.set_data(T_vec*1e9, signal)
            # # guess parameters##########################################################
            # background = (signal.max() + signal.min() )/2.
            # osc_amp = (signal.max() - signal.min() )/2.
            # nb_expected_oscillation = 10.
            # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            # # print pulsation/2/np.pi
            # phio = 0.
            # decaytime = 1000.
            # p0 = [background, osc_amp, pulsation, phio, decaytime]
            # # fitting ##################################################################
            # p = s.fit(p0)
            # values_from_fit = s.func(p)
            # # print 'params:', s.get_fit_params()
            # # print 'errors:', s.get_fit_errors()
            # if graph:
            #     plot2d_1.replace_inline_data_y2(T_vec*1e9, amplitude, values_from_fit )
            #     plot2d_1.add(T_vec*1e9, values_from_fit)
            #     plot2d_1.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
            ######### DIST ####################
            s = fit.ExponentialDecaySine()
            signal = dist_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters##########################################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            nb_expected_oscillation = 10.
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            phio = 0.
            decaytime = 1000.
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting ##################################################################
            p = s.fit(p0)
            values_from_fit = s.func(p)
            if graph:
                plot2d_5.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                # plot2d_5.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
                plot2d_5.set_plottitle('T2= '+ str(round(p[4],2)) +' ns'+',   Freq_detun= '+ str(round( p[2]/2/np.pi*1e3,5 ))+' MHz,   Probe_Freq='+str(round( 1e3*f_atom ))+'MHz'  )
            # result!
            df = p[2]/2/np.pi
            #print df*1e3

    Tabor.set_trigger_source('EVEN')
    if Pulsing_instrument.get_board_flag():
        Pulsing_instrument.measurement_close(transfert_info=False)

    #df = p[2]/2/np.pi*1e3
    #df = p[2]/2/np.pi
    print df*1e3

    # finally:
    if Pulsing_instrument.get_board_flag():
        Pulsing_instrument.measurement_close(transfert_info=False)

    data_measurement.add_data_point(T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a)
    data_measurement.close_file()

    #print Pulsing_instrument.measurement_close(transfert_info=True)
    Pulsing_instrument.measurement_close(transfert_info=True)
    Tabor.set_trigger_source('EVEN')

    if FIT:
        if graph:
            plot2d_5.add(T_vec*1e9, values_from_fit)
        data_fit.add_data_point( s.get_fit_params(), s.get_fit_errors())
        data_fit.close_file()

    if graph:
        # plot2d_1.save_png()
        # plot2d_2.save_png()
        plot2d_3.save_png()
        plot2d_4.save_png()
        plot2d_5.save_png()
    qt.mend()

    df_mhz = df*1e3
    if COMMENTS:
        print 'delta f = ', "%.8f" %df, 'GHz'
        print 'delta_f = ', "%.4f" %df_mhz, 'MHz'

    # smb_cavity_off()
    all_smb_off()

    if qub_detuning != 0.0:
        parameters.freq_q = fq_init

    T2 = round(p[4],2)

    if not Return_all_data:
        return (df, T2)
    else:
        return [T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a]

def get_ramsey_df(parameters, qub_detuning=5.0, tl =1, av=3e3, window=4000, nop = 200,  graph=True, awg_offset=AWG_OFFSET, Return_all_data=False, Return_extracted_values=True, note=''):
    '''
    takes parameters
    makes ramsey measurement
    return delta frequency in Ghz
    (use ONLY non-gaussian pi-pulse calibration)
    '''
    all_smb_on()

    if qub_detuning != 0.0:
        fq_init = parameters.freq_q
        parameters.freq_q = fq_init + 1e-3*qub_detuning

    if COMMENTS:
        print 'Ramsey, freq-q=', parameters.freq_q
    #returns frequency diference to f_q
    df=0
    FIT = True
    try:
        Tabor_loading = tl
        power1 = parameters.power1
        power2 = parameters.power2
        f_atom = parameters.freq_q
        f_cav = parameters.freq_read
        t_meas = parameters.t_read
        tpi = parameters.tpi
        GausSigma = parameters.nsigma
        if GausSigma !=0:
            print 'Ramsey: pi pulse is gaussian'
    except:
        print 'WARNING: (ramsey) one of parameters is not defined!'
        return None

    #t_pi_o2 = 1e-9 * math.floor(tpi/2) # we define the excitation time for a pi over 2 pulse on the qubit
    t_pi_o2 = 1e-9*int( 1e9*tpi/2 ) #should be in sec
    if COMMENTS:
        print 't_pi_o2: ', t_pi_o2
    delta_t = 200 # not to touch for now
    acq_time = t_meas*1e9 + delta_t + 300. # not to touch for now

    # We define the time vector of the Ramsey measurement:
    if (window > 100) and (window<20000):
        tr_stop = window*1e-9
        tr_step = round( tr_stop/nop,  9 ) ##[s]
    else:
        print "\n Error of setting window. Window changed to window=1000 ns nop=200"
        tr_stop = 1e-6 # in s
        tr_step = 5e-9 # in s

    tr_start = 0e-6 # in s
    T_vec = np.arange(tr_start, tr_stop, tr_step)
    if nop != len(T_vec):
        print "nop changed from ", nop, "to ", len(T_vec)
        nop = len(T_vec)

    nb_sequences = len(T_vec) # we define the number of sequences to acquire for the board.

    t_wait = 0e-9
    t_rise = None
    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################

    if Tabor_loading:
        # here we write in the AWG memory if the condition Tabor_loading is True
        if COMMENTS:
            print 'Tabor loading...'

        if GausSigma < 0:
            GausSigma = 0
            print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
        if GausSigma > 5:
            GausSigma = 5
            print 'Warning_Fidelity: Gaussigma was >5, changed to 5'

        Pulsing_instrument.set_trigger_time(100.)
        Pulsing_instrument.write_Ramsey_pulsessequence(t_pi_o2, tr_stop, tr_step,
                tr_start, t_meas, t_wait=t_wait, delete='all', t_rise =t_rise, nsigma=GausSigma )
        Tabor.set_ch1_offset(awg_offset)


    qt.mstart()

    if type(note) != str:
        note = ''
        print 'note variable must has a string type!'
    elif note != ''  and  note[0] != '_':
        note = '_'+note
    label = '_bg_df=' +str(round(qub_detuning*1e3, 1)) +'MHz; av='+str(av) +note

    parameters.save(name='parameters_Ramsey'+label)

    data_measurement = qt.Data(name='Ramsey'+label)
    data_measurement.add_coordinate('waiting time [ns]',    units = 'ns')
    data_measurement.add_value('Ramsy S21 [mV]',            units = 'mV')
    data_measurement.add_value('Ramsy Phase [rad]',         units = 'rad')
    data_measurement.add_value('Ramsy Re [mV]',             units = 'mV')
    data_measurement.add_value('Ramsy Im [mV]',             units = 'mV')
    data_measurement.add_value('Ramsy Dist [mV]',           units = 'mV')
    data_measurement.add_value('Ramsy Norm',                units = 'mV')
    data_measurement.create_file()

    if FIT:
        data_fit = qt.Data(name='Ramsey_fit'+label)
        data_fit.add_coordinate('Source (1-re, 2-im, 3-amp, 4-phase, 5-dist)', units = 'name')
        data_fit.add_value('T2 ',        units = 'ns')
        data_fit.add_value('df ',        units = 'MHz')
        data_fit.add_value('T2_error',        units = 'arb. units')
        data_fit.add_value('df_error',        units = 'arb. units')
        data_fit.create_file()

    if graph:
        plot2d_1 = qt.Plot2D(data_measurement,
                          name      = 'Ramsey S21 ',
                          coorddim  = 0,
                          valdim    = 1,
                          maxtraces = 2)
        plot2d_2 = qt.Plot2D(data_measurement,
                            name      = 'Ramsey Phase ',
                            coorddim  = 0,
                            valdim    = 2,
                            maxtraces = 2)
        plot2d_3 = qt.Plot2D(data_measurement,
                          name      = 'Ramsey Re ',
                          coorddim  = 0,
                          valdim    = 3,
                          maxtraces = 2)
        plot2d_4 = qt.Plot2D(data_measurement,
                            name      = 'Ramsey Im ',
                            coorddim  = 0,
                            valdim    = 4,
                            maxtraces = 2)
        plot2d_5 = qt.Plot2D(data_measurement,
                            name      = 'Ramsey distance',
                            coorddim  = 0,
                            valdim    = 5)
        plot2d_6 = qt.Plot2D(data_measurement,
                            name      = 'Ramsey norm',
                            coorddim  = 0,
                            valdim    = 6)


    Pulsing_instrument.prep_rabi(f_cav, f_atom, av, nb_sequences,
        power1, power2, acq_time, t_meas*1e9, delta_t) #rabi.. ?
    # Pulsing_instrument.prep_ramsey(f_cav, f_atom, av, nb_sequences, power1, power2)
    ## (!) Very strange. Check it with oscilloscope
    qt.msleep(3)
    Tabor.set_trigger_source('TIM')


    while Pulsing_instrument.get_acquisition_completed() != 100.:
        #print  Pulsing_instrument.get_acquisition_completed(), '%'

        result = Pulsing_instrument.measurement()
        ((real_a, rea0), (imag_a, ima0))= result
        real_a -= rea0
        imag_a -= ima0

        ### convert to mV ###
        real_a = 1e3*real_a
        imag_a = 1e3*imag_a

        amplitude = np.sqrt(real_a**2+imag_a**2)
        complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
        phase = np.angle(complexe)
        # dist_a = np.sqrt(  (real_a-real_a[0])**2 + (imag_a-imag_a[0])**2  )     # CHANGED on 06/23/2021

        ######### COMPUTE NORM ##########
        covMat = np.cov(real_a, imag_a)
        eigenValue, eigenVector = np.linalg.eig(covMat)
        norm_a = eigenVector[0,0]*imag_a + eigenVector[0,1]*real_a  ##ok 0 : +8


        qt.msleep(0.1)

        ##------------------------------------##
        ####________FIT CURVES___###############
        ##------------------------------------##
        if FIT:
            ######### REAL ####################
            s = fit.ExponentialDecaySine()
            signal = real_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            nb_expected_oscillation = estimate_nb_oscillations(signal)
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            # pulsation = 2*np.pi*qub_detuning          # CHANGED on 06/23/2021
            phio = 0.
            decaytime = 1000.
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting #####################################################
            p = s.fit(p0)
            p[4] = abs(p[4]) ## no negative T2
            p_err = s.get_fit_errors()
            values_from_fit = s.func(p)
            if graph:
                plot2d_3.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                # plot2d_3.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
                plot2d_3.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
            re_values_from_fit = values_from_fit
            re_p = p
            re_p_err = p_err

            ######### IMAG ####################
            s = fit.ExponentialDecaySine()
            signal = imag_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            # nb_expected_oscillation = 10.
            # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            nb_expected_oscillation = estimate_nb_oscillations(signal)
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            # pulsation = 2*np.pi*qub_detuning          # CHANGED on 06/23/2021
            phio = 0.
            decaytime = 1000.
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting #####################################################
            p = s.fit(p0)
            p[4] = abs(p[4]) ## no negative T2
            p_err = s.get_fit_errors()
            values_from_fit = s.func(p)
            if graph:
                plot2d_4.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_4.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
            im_values_from_fit = values_from_fit
            im_p = p
            im_p_err = p_err


            ######### AMPL ####################
            s = fit.ExponentialDecaySine()
            signal = amplitude
            s.set_data(T_vec*1e9, signal)
            # guess parameters##############################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            # nb_expected_oscillation = 10.
            # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            nb_expected_oscillation = estimate_nb_oscillations(signal)
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            # pulsation = 2*np.pi*qub_detuning          # CHANGED on 06/23/2021
            phio = 0.
            decaytime = 1000.
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting ######################################################
            p = s.fit(p0)
            p[4] = abs(p[4]) ## no negative T2
            p_err = s.get_fit_errors()
            values_from_fit = s.func(p)
            if graph:
                plot2d_1.replace_inline_data_y2(T_vec*1e9, amplitude, values_from_fit )
                # plot2d_1.add(T_vec*1e9, values_from_fit)
                # plot2d_1.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
                plot2d_1.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
            amp_values_from_fit = values_from_fit
            amp_p = p
            amp_p_err = p_err

            ######### PHASE ####################
            s = fit.ExponentialDecaySine()
            signal = phase
            s.set_data(T_vec*1e9, signal)
            # guess parameters##############################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            # nb_expected_oscillation = 10.
            # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            nb_expected_oscillation = estimate_nb_oscillations(signal)
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            # pulsation = 2*np.pi*qub_detuning          # CHANGED on 06/23/2021
            phio = 0.
            decaytime = 1000.
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting ######################################################
            p = s.fit(p0)
            p[4] = abs(p[4]) ## no negative T2
            p_err = s.get_fit_errors()
            values_from_fit = s.func(p)
            if graph:
                plot2d_2.replace_inline_data_y2(T_vec*1e9, phase, values_from_fit )
                # plot2d_2.add(T_vec*1e9, values_from_fit)
                # plot2d_2.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
                plot2d_2.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
            ph_values_from_fit = values_from_fit
            ph_p = p
            ph_p_err = p_err

            ###### COMPUTE DIST (from fit) #######      # CHANGED on 06/23/2021
            id_ref = np.argmin(amp_values_from_fit)
            dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )

            ######### DIST ####################
            s = fit.ExponentialDecaySine()
            signal = dist_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters##########################################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            # nb_expected_oscillation = 10.
            # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            nb_expected_oscillation = estimate_nb_oscillations(signal)
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            # pulsation = 2*np.pi*qub_detuning          # CHANGED on 06/23/2021
            phio = 0.
            decaytime = 1000. #ns
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting ##################################################################
            p = s.fit(p0)
            p[4] = abs(p[4]) ## no negative T2
            p_err = s.get_fit_errors()
            values_from_fit = s.func(p)
            if graph:
                plot2d_5.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                # plot2d_5.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
                plot2d_5.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
            # result!
            df = p[2]/2/np.pi
            dist_values_from_fit = values_from_fit
            dist_p = p
            dist_p_err = p_err

            ######### NORM ####################
            s = fit.ExponentialDecaySine()
            signal = norm_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters##########################################################
            background = (signal.max() + signal.min() )/2.
            osc_amp = (signal.max() - signal.min() )/2.
            nb_expected_oscillation = estimate_nb_oscillations(signal)
            pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
            # pulsation = 2*np.pi*qub_detuning          # CHANGED on 06/23/2021
            phio = 0.
            decaytime = 1000. #ns
            p0 = [background, osc_amp, pulsation, phio, decaytime]
            # fitting ##################################################################
            p = s.fit(p0)
            p[4] = abs(p[4]) ## no negative T2
            p_err = s.get_fit_errors()
            values_from_fit = s.func(p)
            if graph:
                plot2d_6.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_6.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
            # result!
            df = p[2]/2/np.pi
            norm_values_from_fit = values_from_fit
            norm_p = p
            norm_p_err = p_err
        else:
            ###### COMPUTE DIST (from raw data) #####      # CHANGED on 06/23/2021
            id_ref = np.argmin(amplitude)
            dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )

        if graph:
            plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
            plot2d_2.replace_inline_data(T_vec*1e9, phase)
            plot2d_3.replace_inline_data(T_vec*1e9, real_a)
            plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
            plot2d_5.replace_inline_data(T_vec*1e9, dist_a)
            plot2d_6.replace_inline_data(T_vec*1e9, norm_a)


    data_measurement.add_data_point(T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a)
    data_measurement.close_file()

    Tabor.set_trigger_source('EVEN')
    if Pulsing_instrument.get_board_flag():
        Pulsing_instrument.measurement_close(transfert_info=False)

    if Pulsing_instrument.get_board_flag():
        Pulsing_instrument.measurement_close(transfert_info=False)

    Pulsing_instrument.measurement_close(transfert_info=True)
    Tabor.set_trigger_source('EVEN')

    if FIT:
        data_fit.add_data_point(1.0, re_p[4],   re_p[2]/2/np.pi,   re_p_err[4],   re_p_err[2] ) #re
        data_fit.add_data_point(2.0, im_p[4],   im_p[2]/2/np.pi,   im_p_err[4],   im_p_err[2] ) #im
        data_fit.add_data_point(3.0, amp_p[4],  amp_p[2]/2/np.pi,  amp_p_err[4],  amp_p_err[2] ) #amo
        data_fit.add_data_point(4.0, ph_p[4],   ph_p[2]/2/np.pi,   ph_p_err[4],   ph_p_err[2] ) #ph
        data_fit.add_data_point(5.0, dist_p[4], dist_p[2]/2/np.pi, dist_p_err[4], dist_p_err[2] ) #Dist
        data_fit.add_data_point(6.0, norm_p[4], norm_p[2]/2/np.pi, norm_p_err[4], norm_p_err[2] ) #Norm

        if graph:
            plot2d_1.add(T_vec*1e9, amp_values_from_fit)
            plot2d_2.add(T_vec*1e9, ph_values_from_fit)
            plot2d_3.add(T_vec*1e9, re_values_from_fit)
            plot2d_4.add(T_vec*1e9, im_values_from_fit)
            plot2d_5.add(T_vec*1e9, dist_values_from_fit)
            plot2d_6.add(T_vec*1e9, norm_values_from_fit)
        # data_fit.add_data_point( s.get_fit_params(), s.get_fit_errors())
        data_fit.close_file()

    if graph:
        plot2d_1.save_png()
        plot2d_2.save_png()
        plot2d_3.save_png()
        plot2d_4.save_png()
        plot2d_5.save_png()
        plot2d_6.save_png()

    qt.mend()
    all_smb_off()

    ## choosing the best fit (by the biggest amplitude of signal between re and im)
    print "amp of Re osc:", abs(round(re_p[1], 2)), ' [mV]'
    print "amp of Im osc:", abs(round(im_p[1], 2)), ' [mV]'
    print "amp of Dist osc:", abs(round(dist_p[1], 2)), '[mV]'
    print "amp of Norm osc:", abs(round(norm_p[1], 2)), '[mV]'

    # if abs(re_p[1]) > abs(im_p[1]):
    #     print "best is Re"
    #     best_p = re_p
    #     best_p_err = re_p_err
    # else:
    #     print "best is Im"
    #     best_p = im_p
    #     best_p_err = im_p_err
    # if abs(norm_p[1]) > abs(best_p[1]):
    #     print "No! Now best is Norm (covariation) -- of course..."
    #     best_p = norm_p
    #     best_p_err = norm_p_err

    best_p = dist_p
    best_p_err = dist_p_err

    print 'T2=: ', int(best_p[4]), 'ns +-', int(best_p_err[4]), 'ns'
    print 'df=: ', round(1e3*best_p[2]/2/np.pi, 5), 'MHz +-', round(1e3*best_p_err[2]/2/np.pi, 5), 'MHz'

    print "\n"
    #####    What to return?    #####
    if Return_all_data and Return_extracted_values:
        result_list = [best_p[4], best_p_err[4], best_p[2]/2/np.pi*1e3,  best_p_err[2]/2/np.pi*1e3]
        data_list = [T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a]
        return (result_list, data_list)

    elif Return_extracted_values:
        result_list = [best_p[4], best_p_err[4], best_p[2]/2/np.pi*1e3,  best_p_err[2]/2/np.pi*1e3]
        return result_list

    elif Return_all_data:
        data_list = [T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a]
        return data_list

    else:
        return None



def get_ramsey_df_list(parameters, amount=10, qub_detuning=1.0, av=3e3, window=5000, awg_offset=AWG_OFFSET, comnt='', tl=True):
    data_t2_list = qt.Data(name='____T2_list'+comnt)
    data_t2_list.add_value(     'T2',  units = 'ns')
    data_t2_list.add_value(     'd_freq',  units = 'MHz')
    data_t2_list.create_file()

    t2t2 = []
    dfdf = []
    for i in range(amount):
        print('___iteration:', i, '_over:', amount,'___')
        qt.msleep(0.5)
        (df, t2) = get_ramsey_df(parameters, qub_detuning=qub_detuning, window=window, av=av, awg_offset=awg_offset, tl=tl)
        df = 1e3*df
        dfdf.append(df)
        t2t2.append(t2)
        tl = False
        data_t2_list.add_data_point(t2, df)
    data_t2_list.close_file()

    t2_mean = np.mean(t2t2)
    t2_std = np.std(t2t2)
    if COMMENTS:
        print 'T2 is ', round(t2_mean), '+-', round(t2_std)
    df_mean = np.mean(dfdf)
    df_std = np.std(dfdf)
    if COMMENTS:
        print 'delta_freq is ', round(df_mean,4), '+-', round(df_std,4)

    return (t2t2, dfdf)

def get_ramsey_stark_wt2(parameters, pump, qub_detuning=5e-3, tl=1, av=3e3, graph=True, window=4e3, nop=200, note='', awg_offset=AWG_OFFSET, Return_all_data=False, Return_extracted_values=True):
    '''
    Do the ramsey measurement with pumping on readout tone
    between two pi/2 pulses
    Used for extracting number of photons in cavity
    pump = [0.0; 1.0]
    ! Not work with gaussian-pulses (don't know why)
    '''
    # smb_cavity_on()
    all_smb_on()

    Tabor_loading = tl
    power1 = parameters.power1
    power2 = parameters.power2
    f_atom = parameters.freq_q + qub_detuning
    f_cav = parameters.freq_read
    t_meas = parameters.t_read
    tpi = parameters.tpi
    amplitude_photon = pump
    GausSigma = parameters.nsigma
    if GausSigma !=0:
        print 'Warning! get_ramsey_stark_wt2'
        print 'pi pulse is gaussian! Change it to square one'
    if round(tpi*1e9) % 2 != 0:
        print 'tpi is not even. Use even number for tpi'

    # check type of note
    if type(note) != str:
        note = ''
        print 'note variable must has a string type!'
    elif note != ''  and  note[0] != '_':
        note = '_'+note
    label = 'p=' +str(pump) +'_bg_df=' +str(round(qub_detuning*1e3, 1)) +'MHz; av='+str(av) +note


    if t_meas < 500e-9:
        print "ATEENTION! ATTENTION! ATTENTION! \n \nREADOUT TIME is only ", str(int(1e9*t_meas)), "[ns]. Increase param.t_read for ramsey stark \n \n "

    t_pi_o2 = tpi/2
    delta_t = 200
    acq_time = t_meas*1e9 + delta_t + 300.
    # We define the time vector of the Ramsey measurement:
    tr_start = 0e-6 # in s
    if (window > 100) and (window<10000):
        nop = 200.0
        tr_stop = window*1e-9
        tr_step = round( tr_stop/nop,  9 ) ##[s]
    else:
        print 'Warning:get_ramsey_stark_wt2\n window and nop was automaticly changed'
        tr_stop = 1000e-9 # in s
        tr_step = 5e-9 # in s
    #####
    T_vec = np.arange(tr_start, tr_stop, tr_step)
    if nop != len(T_vec):
            print "nop changed from ", nop, "to ", len(T_vec)
            nop = len(T_vec)
    nb_sequences = len(T_vec) # we define the number of sequences to acquire for the board.
    t_wait = 0e-9
    t_rise = None
    ###########################################################
    #
    #
    #               Save parameters
    #
    #
    ###########################################################
    parameters.save(name='parameters_RamseyStark')
    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################
    if Tabor_loading:
        if COMMENTS:
            print 'Tabor loading... (Ramsey_stark)'
        Pulsing_instrument.set_trigger_time(100.)
        Pulsing_instrument.write_Ramsey_Starckshift_pulsessequence(t_pi_o2, tr_stop, tr_step,
                            tr_start, amplitude_photon, t_meas, t_protect=0, delete='all')
        Tabor.set_ch1_offset(awg_offset)
        if COMMENTS:
            print 'Tabor loading successful (Ramsey_stark)'

    qt.mstart()

    data_measurement = qt.Data(name='Ramsey_stark_' +label)
    data_measurement.add_coordinate('waiting time [ns]', units = 'ns')
    data_measurement.add_value('Ram_star S21'  ,         units = 'mV')
    data_measurement.add_value('Ram_star Phase',         units = 'rad')
    data_measurement.add_value('Ram_star Re'   ,         units = 'mV')
    data_measurement.add_value('Ram_star Im'   ,         units = 'mV')
    data_measurement.add_value('Ram_star Dist',         units = 'mV')
    data_measurement.add_value('Ram_star Norm',         units = 'mV')
    data_measurement.create_file()

    data_fit = qt.Data(name='Ramsey_stark_OSC_fit_'+label)
    data_fit.add_coordinate('Source (1-re, 2-im, 3-amp, 4-phase, 5-dist)', units = 'name')
    data_fit.add_value('T2 ',        units = 'ns')
    data_fit.add_value('df ',        units = 'MHz')
    data_fit.add_value('T2_error',        units = 'arb. units')
    data_fit.add_value('df_error',        units = 'arb. units')
    data_fit.create_file()

    if graph:
        plot2d_1 = qt.Plot2D(data_measurement,
                          name      = 'Ram_star S21 ',
                          coorddim  = 0,
                          valdim    = 1,
                          maxtraces = 2)
        plot2d_2 = qt.Plot2D(data_measurement,
                            name      = 'Ram_star Phase ',
                            coorddim  = 0,
                            valdim    = 2,
                            maxtraces = 2)
        plot2d_3 = qt.Plot2D(data_measurement,
                          name      = 'Ram_star Re ',
                          coorddim  = 0,
                          valdim    = 3,
                          maxtraces = 2)
        plot2d_4 = qt.Plot2D(data_measurement,
                            name      = 'Ram_star Im ',
                            coorddim  = 0,
                            valdim    = 4,
                            maxtraces = 2)
        plot2d_5 = qt.Plot2D(data_measurement,
                            name      = 'Ram_star distance',
                            coorddim  = 0,
                            valdim    = 5)
        plot2d_6 = qt.Plot2D(data_measurement,
                            name      = 'Ram_star norm',
                            coorddim  = 0,
                            valdim    = 6)

    board_flag = None
    Pulsing_instrument.prep_rabi(f_cav, f_atom, av, nb_sequences,
        power1, power2, acq_time, t_meas*1e9, delta_t)  ###Same procedure for rabi and ramsey

    qt.msleep(2)
    board_flag = True
    Tabor.set_trigger_source('TIM')

    while Pulsing_instrument.get_acquisition_completed() != 100.:
        result = Pulsing_instrument.measurement()
        ((real_a, rea0), (imag_a, ima0))= result
        real_a -= rea0
        imag_a -= ima0

        ### convert to mV ###
        real_a = 1e3*real_a
        imag_a = 1e3*imag_a

        amplitude = np.sqrt(real_a**2+imag_a**2)
        complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
        phase = np.angle(complexe)

        # id_ref = np.argmin(amplitude)                     # CHANGED on 06/23/2021
        # dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )
        #
        # covMat = np.cov(real_a, imag_a)
        # eigenValue, eigenVector = np.linalg.eig(covMat)
        # norm_a = eigenVector[0,0]*imag_a + eigenVector[0,1]*real_a  ##ok 0 : +8

        qt.msleep(0.1)
        # if graph:
        #     plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
        #     plot2d_2.replace_inline_data(T_vec*1e9, phase)
        #     plot2d_3.replace_inline_data(T_vec*1e9, real_a)
        #     plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
        #     plot2d_5.replace_inline_data(T_vec*1e9, dist_a)
        #     plot2d_6.replace_inline_data(T_vec*1e9, norm_a)

        ##------------------------------------##
        ####________FIT CURVES___###############
        ##------------------------------------##

        ######### REAL ####################
        s = fit.ExponentialDecaySine()
        signal = real_a
        s.set_data(T_vec*1e9, signal)
        # guess parameters#############################################
        background = (signal.max() + signal.min() )/2.
        osc_amp = (signal.max() - signal.min() )/2.
        # nb_expected_oscillation = 4.
        # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        # pulsation = 2*np.pi*qub_detuning
        nb_expected_oscillation = estimate_nb_oscillations(signal)      # CHANGED on 06/23/2021
        pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        phio = 0.
        decaytime = 1000.
        p0 = [background, osc_amp, pulsation, phio, decaytime]
        # fitting #####################################################
        p = s.fit(p0)
        p[4] = abs(p[4]) ## no negative T2
        p_err = s.get_fit_errors()
        values_from_fit = s.func(p)
        if graph:
            plot2d_3.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
            # plot2d_3.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
            plot2d_3.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
        re_values_from_fit = values_from_fit
        re_p = p
        re_p_err = p_err

        ######### IMAG ####################
        s = fit.ExponentialDecaySine()
        signal = imag_a
        s.set_data(T_vec*1e9, signal)
        # guess parameters#############################################
        background = (signal.max() + signal.min() )/2.
        osc_amp = (signal.max() - signal.min() )/2.
        # nb_expected_oscillation = 10.
        # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        # pulsation = 2*np.pi*qub_detuning
        nb_expected_oscillation = estimate_nb_oscillations(signal)      # CHANGED on 06/23/2021
        pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        phio = 0.
        decaytime = 1000.
        p0 = [background, osc_amp, pulsation, phio, decaytime]
        # fitting #####################################################
        p = s.fit(p0)
        p[4] = abs(p[4]) ## no negative T2
        p_err = s.get_fit_errors()
        values_from_fit = s.func(p)
        if graph:
            plot2d_4.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
            plot2d_4.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
        im_values_from_fit = values_from_fit
        im_p = p
        im_p_err = p_err


        ######### AMPL ####################
        s = fit.ExponentialDecaySine()
        signal = amplitude
        s.set_data(T_vec*1e9, signal)
        # guess parameters##############################################
        background = (signal.max() + signal.min() )/2.
        osc_amp = (signal.max() - signal.min() )/2.
        # nb_expected_oscillation = 10.
        # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        # pulsation = 2*np.pi*qub_detuning
        nb_expected_oscillation = estimate_nb_oscillations(signal)      # CHANGED on 06/23/2021
        pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        phio = 0.
        decaytime = 1000.
        p0 = [background, osc_amp, pulsation, phio, decaytime]
        # fitting ######################################################
        p = s.fit(p0)
        p[4] = abs(p[4]) ## no negative T2
        p_err = s.get_fit_errors()
        values_from_fit = s.func(p)
        if graph:
            plot2d_1.replace_inline_data_y2(T_vec*1e9, amplitude, values_from_fit )
            # plot2d_1.add(T_vec*1e9, values_from_fit)
            # plot2d_1.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
            plot2d_1.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
        amp_values_from_fit = values_from_fit
        amp_p = p
        amp_p_err = p_err

        ######### PHASE ####################
        s = fit.ExponentialDecaySine()
        signal = phase
        s.set_data(T_vec*1e9, signal)
        # guess parameters##############################################
        background = (signal.max() + signal.min() )/2.
        osc_amp = (signal.max() - signal.min() )/2.
        # nb_expected_oscillation = 10.
        # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        # pulsation = 2*np.pi*qub_detuning
        nb_expected_oscillation = estimate_nb_oscillations(signal)      # CHANGED on 06/23/2021
        pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        phio = 0.
        decaytime = 1000.
        p0 = [background, osc_amp, pulsation, phio, decaytime]
        # fitting ######################################################
        p = s.fit(p0)
        p[4] = abs(p[4]) ## no negative T2
        p_err = s.get_fit_errors()
        values_from_fit = s.func(p)
        if graph:
            plot2d_2.replace_inline_data_y2(T_vec*1e9, phase, values_from_fit )
            # plot2d_2.add(T_vec*1e9, values_from_fit)
            # plot2d_2.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
            plot2d_2.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
        ph_values_from_fit = values_from_fit
        ph_p = p
        ph_p_err = p_err


        ########### COMPUTE DIST AND NORM ############# CHANGED on 06/23/2021

        id_ref = np.argmin(amp_values_from_fit)
        dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )

        covMat = np.cov(real_a, imag_a)
        eigenValue, eigenVector = np.linalg.eig(covMat)
        norm_a = eigenVector[0,0]*imag_a + eigenVector[0,1]*real_a  ##ok 0 : +8


        ######### DIST ####################
        s = fit.ExponentialDecaySine()
        signal = dist_a
        s.set_data(T_vec*1e9, signal)
        # guess parameters##########################################################
        background = (signal.max() + signal.min() )/2.
        osc_amp = (signal.max() - signal.min() )/2.
        # nb_expected_oscillation = 10.
        # pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        # pulsation = 2*np.pi*qub_detuning
        nb_expected_oscillation = estimate_nb_oscillations(signal)      # CHANGED on 06/23/2021
        pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        phio = 0.
        decaytime = 1000. #ns
        p0 = [background, osc_amp, pulsation, phio, decaytime]
        # fitting ##################################################################
        p = s.fit(p0)
        p[4] = abs(p[4]) ## no negative T2
        p_err = s.get_fit_errors()
        values_from_fit = s.func(p)
        if graph:
            plot2d_5.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
            # plot2d_5.set_plottitle('T2= '+ str(p[4])+' ns'+', Freq= '+str(p[2]/2/np.pi*1e3)+' MHz')
            plot2d_5.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
        # result!
        df = p[2]/2/np.pi
        dist_values_from_fit = values_from_fit
        dist_p = p
        dist_p_err = p_err

        ######### NORM ####################
        s = fit.ExponentialDecaySine()
        signal = norm_a
        s.set_data(T_vec*1e9, signal)
        # guess parameters##########################################################
        background = (signal.max() + signal.min() )/2.
        osc_amp = (signal.max() - signal.min() )/2.
        # pulsation = 2*np.pi*qub_detuning
        nb_expected_oscillation = estimate_nb_oscillations(signal)      # CHANGED on 06/23/2021
        pulsation = 2*np.pi/(tr_stop*1e9)*nb_expected_oscillation
        phio = 0.
        decaytime = 1000. #ns
        p0 = [background, osc_amp, pulsation, phio, decaytime]
        # fitting ##################################################################
        p = s.fit(p0)
        p[4] = abs(p[4]) ## no negative T2
        p_err = s.get_fit_errors()
        values_from_fit = s.func(p)
        if graph:
            plot2d_6.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
            plot2d_6.set_plottitle('T2= '+ str(int(p[4]))+'ns'+', Freq= '+str(round(p[2]/2/np.pi*1e3, 5))+'MHz')
        # result!
        df = p[2]/2/np.pi
        norm_values_from_fit = values_from_fit
        norm_p = p
        norm_p_err = p_err

        if graph:
            plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
            plot2d_2.replace_inline_data(T_vec*1e9, phase)
            plot2d_3.replace_inline_data(T_vec*1e9, real_a)
            plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
            plot2d_5.replace_inline_data(T_vec*1e9, dist_a)
            plot2d_6.replace_inline_data(T_vec*1e9, norm_a)

    data_fit.add_data_point(1.0, re_p[4],   re_p[2]/2/np.pi,   re_p_err[4],   re_p_err[2] ) #re
    data_fit.add_data_point(2.0, im_p[4],   im_p[2]/2/np.pi,   im_p_err[4],   im_p_err[2] ) #im
    data_fit.add_data_point(3.0, amp_p[4],  amp_p[2]/2/np.pi,  amp_p_err[4],  amp_p_err[2] ) #amo
    data_fit.add_data_point(4.0, ph_p[4],   ph_p[2]/2/np.pi,   ph_p_err[4],   ph_p_err[2] ) #ph
    data_fit.add_data_point(5.0, dist_p[4], dist_p[2]/2/np.pi, dist_p_err[4], dist_p_err[2] ) #Dist
    data_fit.add_data_point(6.0, norm_p[4], norm_p[2]/2/np.pi, norm_p_err[4], norm_p_err[2] ) #Norm

    Tabor.set_trigger_source('EVEN')
    if Pulsing_instrument.get_board_flag():
        Pulsing_instrument.measurement_close(transfert_info=False)
    Pulsing_instrument.measurement_close(transfert_info=True)
    Tabor.set_trigger_source('EVEN')

    data_measurement.add_data_point(T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a)
    data_measurement.close_file()

    data_fit.close_file()

    if graph:
        plot2d_1.add(T_vec*1e9, amp_values_from_fit)
        plot2d_2.add(T_vec*1e9, ph_values_from_fit)
        plot2d_3.add(T_vec*1e9, re_values_from_fit)
        plot2d_4.add(T_vec*1e9, im_values_from_fit)
        plot2d_5.add(T_vec*1e9, dist_values_from_fit)
        plot2d_6.add(T_vec*1e9, norm_values_from_fit)
        plot2d_1.save_png()
        plot2d_2.save_png()
        plot2d_3.save_png()
        plot2d_4.save_png()
        plot2d_5.save_png()
        plot2d_6.save_png()

    qt.mend()
    all_smb_off()

    ## choosing the best fit (by the biggest amplitude of signal between re and im)
    print "amp of Re osc:", abs(round(re_p[1], 2)), ' [mV]'
    print "amp of Im osc:", abs(round(im_p[1], 2)), ' [mV]'
    print "amp of Dist osc:", abs(round(dist_p[1], 2)), '[mV]'
    print "amp of Norm osc:", abs(round(norm_p[1], 2)), '[mV]'

    # if abs(re_p[1]) > abs(im_p[1]):
    #     print "best is Re"
    #     best_p = re_p
    #     best_p_err = re_p_err
    # else:
    #     print "best is Im"
    #     best_p = im_p
    #     best_p_err = im_p_err
    # if abs(norm_p[1]) > abs(best_p[1]):
    #     print "No! Now best is Norm (covariation) -- of course..."
    #     best_p = norm_p
    #     best_p_err = norm_p_err

    best_p = dist_p
    best_p_err = dist_p_err

    print 'T2=: ', int(best_p[4]), 'ns +-', int(best_p_err[4]), 'ns'
    print 'df=: ', round(1e3*best_p[2]/2/np.pi, 5), 'MHz +-', round(1e3*best_p_err[2]/2/np.pi, 5), 'MHz'


    print "\n"
    #####    What to return?    #####
    if Return_all_data and Return_extracted_values:
        result_list = [best_p[4], best_p_err[4], best_p[2]/2/np.pi*1e3,  best_p_err[2]/2/np.pi*1e3]
        data_list = [T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a]
        return (result_list, data_list)

    elif Return_extracted_values:
        result_list = [best_p[4], best_p_err[4], best_p[2]/2/np.pi*1e3,  best_p_err[2]/2/np.pi*1e3]
        return result_list

    elif Return_all_data:
        data_list = [T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a]
        return data_list

    else:
        return None

def get_relax_time(parameters, tl = 1, averaging=3e3, graph=True):
    '''
    Measure the relaxation time after pi-pulses
    returns t1 in nanoseconds
    '''
    # smb_cavity_on()
    all_smb_on()

    if COMMENTS:
        print 'relaxation time measurment'
    try:
        Tabor_loading = tl
        GausSigma = parameters.nsigma
        #tr_start = 0e-9
        #tr_stop = window*1e-9
        #tr_step = tr_stop/400.
        power1 = parameters.power1
        power2 = parameters.power2
        f_atom = parameters.freq_q
        f_cav = parameters.freq_read
        t_meas = parameters.t_read
        t_pi = parameters.tpi
    except:
        print 'WARNING: (relax) one of parameters is not defined!'
        return None

    delta_t = 200.
    acq_time = t_meas*1e9 + delta_t + 300.
    T_vec = np.logspace(-9., -4.046, 140)         # -4.7, 140)
    #T_vec = np.arange(tr_start, tr_stop, tr_step) #from rabi
    before = 10
    t_prev = np.linspace(-T_vec[-1]/5., 0, before)
    t_rise= None
    tau = None
    signal_str = 'real'
    if (GausSigma != 0) and COMMENTS:
        print 'Gaussain relaxation!'
    #####################EXPERIMENT##################
    if Tabor_loading:
        Pulsing_instrument.set_trigger_time(100.)
        # Pulsing_instrument.write_Relaxation_pulsessequence2(t_pi, T_vec, t_meas, delete='all', before=before, t_rise=t_rise, nsigma=GausSigma)
        Pulsing_instrument.write_Relaxation_pulsessequence_prepulse_test(t_pi, T_vec, t_meas, delete='all', before=before, t_rise=t_rise, nsigma=GausSigma)  # TEST!!! 26/04/22: was "write_Relaxation_pulsessequence2"

    T_vec = np.append(t_prev, T_vec)
    nb_sequences = len(T_vec)
    qt.mstart()

    data_measurement = qt.Data(name='Relaxation')
    data_measurement.add_coordinate('excitation time [ns]', units = 'ns')
    data_measurement.add_value('S21 [mV]',            units = 'mV')
    data_measurement.add_value('Phase [rad]',            units = 'rad')
    data_measurement.add_value('Re [mV]',            units = 'mV')
    data_measurement.add_value('Im [mV]',            units = 'mV')
    data_measurement.add_value('Distance [mV]',            units = 'mV')
    data_measurement.create_file()

    if graph:
        # plot2d_3 = qt.Plot2D(data_measurement,
        #                   name      = 'Re ',
        #                   coorddim  = 0,
        #                   valdim    = 3,
        #                   maxtraces = 2)
        # plot2d_4 = qt.Plot2D(data_measurement,
        #                     name      = 'Im ',
        #                     coorddim  = 0,
        #                     valdim    = 4,
        #                     maxtraces = 2)
        plot2d_5  = qt.Plot2D(data_measurement,
                            name      = 'Relaxation_dist',
                            coorddim  = 0,
                            valdim    = 5,
                            maxtraces = 2)

    data_fit = qt.Data(name='T1_fit')
    data_fit.add_value('parameters ',            units = 'rad, rad, -GHz, .. ')
    data_fit.add_value('perrors ',            units = 'rad, rad, -GHz, ..')
    data_fit.create_file()

    board_flag = None


    try:
        Pulsing_instrument.prep_relaxation(f_cav, f_atom, averaging, nb_sequences,
            power1, power2, acq_time, t_meas*1e9, delta_t)
        qt.msleep(2.)

        board_flag = True

        Tabor.set_trigger_source('TIM')
        while ats9360.get_completed_acquisition() != 100.:
            #print ats9360.get_completed_acquisition(), '%'

            result = ats9360.measurement()
            ((real_a, rea0), (imag_a, ima0))= result
            real_a -= np.mean(rea0)
            imag_a -= np.mean(ima0)
            ### convert to mV ###
            real_a = 1e3*real_a
            imag_a = 1e3*imag_a

            amplitude = np.sqrt(real_a**2+imag_a**2)

            complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase = np.angle(complexe)
            # phase_renormed = np.log( phase[-10:-1].mean() - phase)
            # phase_renormed = np.log(phase_renormed)
            r0 = np.mean(real_a[:before])
            im0 = np.mean(imag_a[:before])
            distance = np.sqrt((real_a-r0)**2+(imag_a-im0)**2)
            qt.msleep(0.1)

            if graph:
                plot2d_5.replace_inline_data(T_vec*1e9, distance)

            s = fit.Exponential()
            signal = real_a
            a0 = np.mean(signal[:before])
            amp = a0 - signal
            s.set_data(T_vec[before:]*1e9, amp[before:] )
            # guess parameters##########################################################
            a = 0.
            b = np.max(amp*1e-3) ##because amp is in [mV], but formula is for [V]
            c = 0.
            d = 1./2e3
            p0 = [a, b, c, d]

            # fitting ##################################################################
            p = s.fit(p0, fixed = [0, 2])
            values_from_fit = s.func(p)
            values_from_fit= np.append( a0+np.zeros(before),  a0 - values_from_fit)
            # if graph:
            #     plot2d_3.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit)
            #     plot2d_3.set_plottitle('T1= '+ str(1/p[3])+' ns')

            signal = imag_a
            a0 = np.mean(signal[:before])
            amp = a0 - signal
            s.set_data(T_vec[before:]*1e9, amp[before:] )
            # guess parameters##########################################################
            a = 0.
            b = np.max(amp*1e-3)
            c = 0.
            d = 1./2e3
            p0 = [a, b, c, d]

            # fitting ##################################################################
            p = s.fit(p0, fixed = [0, 2])
            values_from_fit = s.func(p)
            values_from_fit= np.append( a0+np.zeros(before),  a0 - values_from_fit)
            # if graph:
            #     plot2d_4.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit)
            #     plot2d_4.set_plottitle('T1= '+ str(1/p[3])+' ns')

            s = fit.Exponential()
            signal = distance
            a0 = 0.
            amp = a0 + signal
            s.set_data(T_vec[before:]*1e9, amp[before:] )
            # guess parameters##########################################################
            a = 0.
            b = np.max(amp)
            c = 0.
            d = 1./2e3
            p0 = [a, b, c, d]

            # fitting ##################################################################
            p = s.fit(p0, fixed = [0])
            values_from_fit = s.func(p)
            values_from_fit= np.append( a0 + np.zeros(before),  a0 + values_from_fit)
            if graph:
                plot2d_5.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit)
                plot2d_5.set_plottitle('T1= '+ str( round(1/p[3],1) )+' ns')


        Tabor.set_trigger_source('EVEN')
        ats9360.measurement_close(transfert_info=False)
        board_flag = False

    finally:
        if board_flag:
            ats9360.measurement_close(transfert_info=False)

        data_measurement.add_data_point(T_vec*1e9, amplitude, phase, real_a, imag_a, distance)
        data_measurement.close_file()
        print ats9360.measurement_close(transfert_info=True)
        Tabor.set_trigger_source('EVEN')

    data_fit.add_data_point(s.get_fit_params(), s.get_fit_errors() )
    data_fit.close_file()
    if graph:
        plot2d_5.set_plottitle('T1= '+ str( round(1/p[3],1) )+' ns')
        # plot2d_3.save_png()
        # plot2d_4.save_png()
        plot2d_5.save_png()
    qt.mend()

    time_relax = (1.0/p[3])*1e-9

    # smb_cavity_off()
    all_smb_off()
    return time_relax

def get_relax_list(parameters, averaging=3e3, graph=True, amount=1, comnt=''):
    '''
    call get_relax_time() amount of times, makes averaging and
    returns mean value and std
    '''

    start_time = datetime.datetime.now()
    print 'Relax_list started at:', start_time, '\n'

    if amount<0:
        print 'warning: relax_list() :amount <0'
        return None

    #create data file
    data_t1_list = qt.Data(name='____T1_list'+comnt)
    data_t1_list.add_coordinate('current',  units = 'mA')
    data_t1_list.add_coordinate('F_read',   units ='GHz')
    data_t1_list.add_coordinate('F_qubit',  units = 'GHz')
    data_t1_list.add_coordinate('tpi',      units = 'ns')
    data_t1_list.add_coordinate('power2',   units = 'V')
    data_t1_list.add_value(     'T1',  units = 'ns')
    data_t1_list.create_file()

    t1t1 = []
    tl_flag = 1
    for i in range(amount):
        print('___iteration:', i, '_over:', amount,'___')
        qt.msleep(0.5)
        t1 = get_relax_time(parameters, graph = graph, averaging = averaging, tl = tl_flag)
        tl_flag = 0
        if t1 is not None:
            t1t1.append(t1)
            data_t1_list.add_data_point(parameters.current, parameters.freq_read, parameters.freq_q, parameters.tpi, parameters.power2, t1)


    data_t1_list.close_file()
    t1_mean = np.mean(t1t1)
    t1_std = np.std(t1t1)
    if COMMENTS:
        print 't1 is ', t1_mean, '+-', t1_std

    stop_time = datetime.datetime.now()
    print '\n Relax_list finished at:', stop_time,'\n','       time:', stop_time - start_time

    return [t1_mean, t1_std]

def get_dephasing_list(parameters, av=2e3, graph=True, amount=1, comnt='', window=4000, tl=1):
    '''
    call  get_ramsey_df() amount of times, makes averaging and
    returns mean value and std
    '''

    start_time = datetime.datetime.now()
    print 'Dephasing_list started at:', start_time, '\n'

    if amount<0:
        print 'warning: relax_list() :amount <0'
        return None

    #create data file
    data_t2_list = qt.Data(name='____T2_list'+comnt)
    data_t2_list.add_coordinate('current',  units = 'mA')
    data_t2_list.add_coordinate('F_read',   units ='GHz')
    data_t2_list.add_coordinate('F_qubit',  units = 'GHz')
    data_t2_list.add_coordinate('tpi',      units = 'ns')
    data_t2_list.add_coordinate('power2',   units = 'V')
    data_t2_list.add_value(     'T2',  units = 'ns')
    data_t2_list.add_value(     'T2_error',  units = 'ns')
    data_t2_list.add_value(     'Freq_q_shift',  units = 'MHz')
    data_t2_list.add_value(     'Freq_error',  units = 'MHz')
    data_t2_list.create_file()

    t2_list = []
    t2_err_list = []
    fq_list = []
    fq_err_list =[]
    tl_flag = tl
    for i in range(amount):
        qt.msleep(0.5)
        [t2, t2_err, fq, fq_err] = get_ramsey_stark_wt2(parameters, pump=0.0, graph=graph, av=av, tl=tl_flag, window=window)
        tl_flag = 0
        if t2 is not None:
            t2_list.append(t2)
            t2_err_list.append(t2_err)
            fq_list.append(fq)
            fq_err_list.append(fq_err)
            data_t2_list.add_data_point(parameters.current, parameters.freq_read, parameters.freq_q, parameters.tpi, parameters.power2, t2, t2_err, fq, fq_err)


    data_t2_list.close_file()
    t2_mean = np.mean(t2_list)
    t2_std = np.std(t2_list)
    if COMMENTS:
        print 't2 is ', t2_mean, '+-', t2_std

    stop_time = datetime.datetime.now()
    print '\n Relax_list finished at:', stop_time,'\n','       time:', stop_time - start_time

    return [t2_mean, t2_std]

def get_rabi_list(parameters, averaging=2e3, graph=True, window=3000, amount=1, comnt=''):
    '''
    call get_rabi_pi() amount of times, makes averaging and
    returns mean value and std
    '''

    start_time = datetime.datetime.now()
    print 'Rabi_list started at:', start_time, '\n'

    if amount<0:
        print 'warning: rabi_list() :amount <0'
        return None

    #create data file
    data_trabi_list = qt.Data(name='____T_Rabi_list'+comnt)
    data_trabi_list.add_coordinate('current',  units = 'mA')
    data_trabi_list.add_coordinate('F_read',   units ='GHz')
    data_trabi_list.add_coordinate('F_qubit',  units = 'GHz')
    data_trabi_list.add_coordinate('tpi',      units = 'ns')
    data_trabi_list.add_coordinate('power2',   units = 'V')
    data_trabi_list.add_value(     'Tpi exp.',  units = 'ns')
    data_trabi_list.add_value(     'Trabi',  units = 'ns')
    data_trabi_list.create_file()

    trabi_arr = []
    tl_flag = 1
    for i in range(amount):
        print('___iteration:', i, '_over:', amount,'___')
        qt.msleep(0.5)
        tpi, trabi = get_rabi_pi(parameters, parameters.power2, graph = graph, window=window, averaging = averaging, tl = tl_flag, Return_trabi=True)
        tl_flag = 0
        if trabi is not None:
            trabi_arr.append(trabi)
            data_trabi_list.add_data_point(parameters.current, parameters.freq_read, parameters.freq_q, parameters.tpi, parameters.power2, tpi, trabi)


    data_trabi_list.close_file()
    trabi_mean = np.mean(trabi_arr)
    trabi_std = np.std(trabi_arr)
    if COMMENTS:
        print 't_rabi is ', trabi_mean, '+-', trabi_std

    stop_time = datetime.datetime.now()
    print '\n Rabi_list finished at:', stop_time,'\n','       time:', stop_time - start_time

    return [trabi_mean, trabi_std]

def get_dblob(parameters, span=0.1, av = 1e3, nop = 200, tl = 1, graph=True, awg_offset=AWG_OFFSET, Return_all_data=False, Return_best_freq=True, comnt=''):
    '''
    Makes sweep s21/ph vs readout frequences, returns optimal freq_read
    transmission(f_min, f_max, averaging = 1e3, nop = 100, Tabor_loading = 1)
    - now just maximum of d-blobs (how to fit it?)
    [just repeat in small spot with more av]
    '''
    #### checking that JPA is off, or switch it off if not
    #jpa_onoff(0)
    # smb_cavity_on()
    all_smb_on()

    try:
        Tabor_loading = tl
        power1 = parameters.power1
        power2 = parameters.power2
        freq_q = parameters.freq_q
        freq_cav = parameters.freq_read
        # tpi = 1e-9 * parameters.tpi
        tpi = parameters.tpi
        GausSigma = parameters.nsigma
        t_read = parameters.t_read
        f_min = parameters.freq_read - span/2
        f_max = parameters.freq_read + span/2
    except:
        print 'W@RNING: (dblob) one of parameters is not defined!'
        return None
    #start
    f_step = round( abs(f_max - f_min)/nop,  6 ) ##[GHz]
    if COMMENTS:
        print 'Dblob, f_read=', parameters.freq_read
        print('fstep=', f_step)

    freq_vec = np.arange(f_min, f_max + f_step, f_step)
    if len(freq_vec) %2 !=0:
            freq_vec = np.arange(f_min, f_max , f_step)

    if nop != len(freq_vec):
        print "nop changed from ", nop, "to ", len(freq_vec)
        nop = len(freq_vec)

    delta_t = 0.2e-6
    acq_time =  t_read*1e9 + delta_t*1e9 + 300.
    t_rise = None
    # 10e-9
    tau = None
    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################
    if Tabor_loading:
        if COMMENTS:
            print 'Tabor loading'
        Pulsing_instrument.set_trigger_time(100.)

        if GausSigma < 0:
            GausSigma = 0
            print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
        if GausSigma > 5:
            GausSigma = 5
            print 'Warning_Fidelity: Gaussigma was >5, changed to 5'
        if GausSigma > 0:
                if COMMENTS:
                    print 'gaussian form!'

        Pulsing_instrument.set_trigger_time(100.)
        Pulsing_instrument.write_twotone_pulsessequence_withpi(temp_1=t_read,
            t1_start= tpi + 0.1e-6, temp_2=tpi , m1_start= tpi,  delete = 'all', t_rise=t_rise, nsigma=GausSigma)
        Tabor.set_ch1_offset(awg_offset)

    # Pulsing_instrument.write_twotone_pulsessequence( 500e-9, 100e-9 + tpi, tpi, delete = 'all')
    qt.mstart()

    if comnt != '':
        comnt = '_' +comnt

    data_measurement = qt.Data(name='Cavity_shift'+str(comnt) )
    data_measurement.add_coordinate('R.O. frequency [GHz]', units = 'GHz')
    data_measurement.add_value('S21 [mV]',            units = 'mV')
    data_measurement.add_value('Phase ',              units = 'rad')
    data_measurement.add_value('Re [mV]',             units = 'mV')
    data_measurement.add_value('Im [mV]',             units = 'mV')
    data_measurement.add_value('S21 pi [mV]',         units = 'mV')
    data_measurement.add_value('Phase pi',            units = 'rad')
    data_measurement.add_value('Re pi [mV]',          units = 'mV')
    data_measurement.add_value('Im pi [mV]',          units = 'mV')
    data_measurement.add_value('D blobs [mV]',        units = 'mV')

    data_measurement.create_file()
    if graph:
        plot2d_1 = qt.Plot2D(data_measurement,
                          name      = 'S21 ',
                          coorddim  = 0,
                          valdim    = 1,
                          maxtraces = 2)
        #
        plot2d_2 = qt.Plot2D(data_measurement,
                            name      = 'Phase ',
                            coorddim  = 0,
                            valdim    = 2,
                            maxtraces = 2)
        #
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

        plot2d_5 = qt.Plot2D(data_measurement,
                            name      = 'd blobs ',
                            coorddim  = 0,
                            valdim    = 9,
                            maxtraces = 2)
    # With Pi-Pulse:
    board_flag = None
    #d_dict = {}
    try:
        # Pulsing_instrument.prep_conditional_transmission(freq_vec, averaging,
        #             power1, f_cw=freq_q, power2=power2, acq_time=acq_time, pulse_time=t_read*1e9, delta_t=delta_t )
        Pulsing_instrument.prep_conditional_transmission(freq_vec, av,
                    power1, f_cw=freq_q, power2=power2, acq_time=acq_time, pulse_time=t_read*1e9, delta_t=delta_t, tau=tau )

        qt.msleep(2)
        # smb_atom.set_freqsweep('OFF')
        smb_cavity.restartsweep()
        qt.msleep(1)

        board_flag = True
        Tabor.set_trigger_source('TIM')
        while ats9360.get_completed_acquisition() != 100.:
            #print  ats9360.get_completed_acquisition(), '%'
            result = ats9360.measurement()
            # (real, imag)= result
            ((real, rea0), (imag,ima0))= result

            real = real - np.mean(rea0)
            imag = imag - np.mean(ima0)

            ### convert to mV ###
            real = 1e3*real
            imag = 1e3*imag

            real = np.reshape(real, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) )
            imag = np.reshape(imag, (len(freq_vec), Pulsing_instrument.get_pulsenumber_averaging()) )
            real_a = real[:, :Pulsing_instrument.get_pulsenumber_averaging()/2]
            imag_a = imag[:, :Pulsing_instrument.get_pulsenumber_averaging()/2]
            real_a = np.mean(real_a, axis = 1)
            imag_a = np.mean(imag_a, axis = 1)
            real_a_pi = real[:, Pulsing_instrument.get_pulsenumber_averaging()/2:]
            imag_a_pi = imag[:, Pulsing_instrument.get_pulsenumber_averaging()/2:]
            real_a_pi = np.mean(real_a_pi, axis = 1)
            imag_a_pi = np.mean(imag_a_pi, axis = 1)

            d_blobs = np.sqrt((real_a-real_a_pi)**2+(imag_a-imag_a_pi)**2)

            amplitude = np.sqrt(real_a**2+imag_a**2)
            complexe = (real_a + 1j*imag_a )*np.exp(1j*freq_vec*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase = np.angle(complexe)

            amplitude_pi = np.sqrt(real_a_pi**2+imag_a_pi**2)
            complexe_pi = (real_a_pi + 1j*imag_a_pi )*np.exp(1j*freq_vec*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
            phase_pi = np.angle(complexe_pi)
            qt.msleep(0.1)
            #
            if graph:
                plot2d_1.replace_inline_data_y2(freq_vec, amplitude, amplitude_pi)
                plot2d_2.replace_inline_data_y2(freq_vec, phase, phase_pi)
                plot2d_3.replace_inline_data_y2(freq_vec, real_a, real_a_pi)
                plot2d_4.replace_inline_data_y2(freq_vec, imag_a, imag_a_pi)
                plot2d_5.replace_inline_data(freq_vec, d_blobs)

        Tabor.set_trigger_source('EVEN')
        ats9360.measurement_close(transfert_info=False)
        board_flag = False
    finally:
        if board_flag:
            ats9360.measurement_close(transfert_info=False)

        data_measurement.add_data_point(freq_vec,amplitude,phase, real_a, imag_a, amplitude_pi, phase_pi, real_a_pi, imag_a_pi, d_blobs)
        if graph:
            plot2d_1.add(freq_vec, amplitude_pi)
            plot2d_2.add(freq_vec, phase_pi)
            plot2d_3.add(freq_vec, real_a_pi)
            plot2d_4.add(freq_vec, imag_a_pi)

        #print ats9360.measurement_close(transfert_info=True)
        # smb_cavity.set_freqsweep('OFF')
        # smb_cavity.set_gui_update('ON')
        Tabor.set_trigger_source('EVEN')

    #return max[d_blobs]
    data_measurement.close_file()
    if graph:
        plot2d_1.save_png()
        plot2d_2.save_png()
        plot2d_3.save_png()
        plot2d_4.save_png()
        plot2d_5.save_png()

    #jpa_onoff(1)

    qt.mend()
    # Searching for maximum:
    best_dblob = np.max(d_blobs)
    best_freq = freq_vec[np.argmax(d_blobs)]
    result = {'best_freq':best_freq,'best_dblob':best_dblob}
    print result
    # # no doesent work (peak is too wide - std -is not noize)
    # #maybe take a 10% part of data...
    # if abs( np.mean(d_blobs)-np.max(d_blobs) )  <  3*np.std(d_blobs):
    #     print '_____dBlob didnt find peak'
    #     return None

    all_smb_off()

    # Return_all_data=False, Return_best_freq=True
    if Return_all_data and Return_best_freq:
        data_list = [freq_vec, amplitude, phase, real_a, imag_a, amplitude_pi, phase_pi, real_a_pi, imag_a_pi, d_blobs]
        return (best_freq, data_list)

    elif Return_best_freq:
        return best_freq

    elif Return_all_data:
        data_list = [freq_vec, amplitude, phase, real_a, imag_a, amplitude_pi, phase_pi, real_a_pi, imag_a_pi, d_blobs]
        return data_list

    else:
        return None

def get_dblob_vs_rudat(parameters, att_vec, span=0.1, nop = 200, av = 2e3, Follow_peak_shift=True):
    '''
    runs get_dblob() in loop, plot 3D-colorplot, save data. Returns True.
    '''
    data_measurement = qt.Data(name='___Distance_blobs_vs_Rudat___')
    data_measurement.add_coordinate('Att on read [dB]', units = 'dB') #0
    data_measurement.add_coordinate('R.O. frequency [GHz]', units = 'GHz') #1
    data_measurement.add_value('S21 ',            units = 'Volt') #2
    data_measurement.add_value('Phase ',            units = 'rad') #3
    data_measurement.add_value('Re ',            units = 'Volt') #4
    data_measurement.add_value('Im ',            units = 'Volt') #5
    data_measurement.add_value('S21 pi',            units = 'Volt') #6
    data_measurement.add_value('Phase pi',            units = 'rad') #7
    data_measurement.add_value('Re pi',            units = 'Volt') #8
    data_measurement.add_value('Im pi',            units = 'Volt') #9
    data_measurement.add_value('D blobs',            units = 'Volt') #10
    data_measurement.add_value('D Ampl',            units = 'Volt') #difference of Ampl after pi-pulse and no pi-pulse
    data_measurement.add_value('D Phase',            units = 'Volt') #difference of Phase after pi-pulse and no pi-pulse
    data_measurement.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'Distance blobs',
                      coorddim  = (1,0),
                      valdim    = 10)
    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'Amplitude diff',
                      coorddim  = (1,0),
                      valdim    = 11)
    plot3d_3 = qt.Plot3D(data_measurement,
                      name      = 'Phase diff',
                      coorddim  = (1,0),
                      valdim    = 12)

    initial_rudat = parameters.rudat
    initial_freq_read = parameters.freq_read

    center_freq_read = parameters.freq_read
    tl_flag = 1
    for att in att_vec:
        parameters.set_rudat(att)
        ( center_freq_read, data ) = get_dblob(parameters, span=span, av=av, nop=nop, tl=tl_flag, Return_best_freq=True, Return_all_data=True, comnt='Rudat='+str(round(att,2))+'dB' )
        [freq_vec, amplitude, phase, real_a, imag_a, amplitude_pi, phase_pi, real_a_pi, imag_a_pi, d_blobs] = data
        ampl_diff  = abs( amplitude_pi -amplitude )
        phase_diff = abs( phase_pi -phase )
        data_measurement.add_data_point( att*np.ones_like(freq_vec), freq_vec, amplitude, phase, real_a, imag_a, amplitude_pi, phase_pi, real_a_pi, imag_a_pi, d_blobs, ampl_diff, phase_diff  )
        data_measurement.new_block()
        tl_flag = 0
        parameters.freq_read = center_freq_read

    parameters.set_rudat(initial_rudat)
    parameters.freq_read = initial_freq_read
    data_measurement.close_file()
    plot3d_1.save_png()
    plot3d_2.save_png()
    plot3d_3.save_png()
    return True

def make_weightfunc(parameters, averaging=400, awg_offset=AWG_OFFSET, t_between=300e-9, t_tail=200e-9, ats_trigger_delay=None, TRIGGER_TIME=200, DELTA_M1_START=100e-9, t1_1start=100e-9, ):
    '''
    New weight functions maker. 2019 Oct 30 V
    '''
    power       = parameters.power1
    power2      = parameters.power2
    freq_cav    = parameters.t_read
    t_read      = parameters.t_read
    SIGMA       = parameters.nsigma     ### is SIGMA > 0 -- pi-pulse will be gaussian
    tpi         = parameters.tpi

    #############################

    ### it is in function arguments now
    # t1_1start = 100e-9       ### ???
    # t_between = 300e-9       ### time between end of 1st readout and start of pi-pulse for second readout
    # t_tail = 200e-9          ### how much time to record after readout pulse is finished

    if t_between < t_tail:
        print 'warning! t_between < t_tail. It will be an overlap of aquisition. Make time_between_pulses(t_between) more than time_datataking_after_each_pulse(t_tail)'
        print 'but nevetheless function can continue to go'

    ## initial_delay - delay time in ns beween zero of Tabor sequence and start of acquisition. Depends of length of the wires must be positive (Warning:no checking), 175 by qtlab
    if ats_trigger_delay == None:
        initial_delay = ats9360.get_trigger_delay() # initial_delay = 175 ### usual one
        qt.msleep(0.1)
    else:
        initial_delay = ats_trigger_delay

    print 'ats trigger initial_delay is: ', initial_delay

    ###############------------------######################
    # #### CONSTANTS HERE #####
    # # TRIGGER_TIME        = 200       ### WTF IS THIS?
    # # DELTA_M1_START      = 100e-9    ### WTF IS THIS?
    # # AQUISITION_TIME     = 800
    # AQUISITION_TIME     = 1e9*(t_read + t_tail)
    #
    # if AQUISITION_TIME < 256e-9:
    #     print('Warning: acquisition time was less than 256ns\nChange acquisition time from {}ns to 256ns'.format(AQUISITION_TIME))
    #     AQUISITION_TIME = 256e-9
    # # return AQUISITION_TIME
    ###############------------------######################
    ## CHANGED V 2021-06-29
    AQUISITION_TIME     = t_read + t_tail
    if AQUISITION_TIME < 256:
        print('Warning: acquisition time was less than 256ns\nChange acquisition time from {}ns to 256ns'.format(AQUISITION_TIME))
        AQUISITION_TIME = 256
    # return AQUISITION_TIME
    ###############------------------######################

    print "\nAQUISITION_TIME = ", AQUISITION_TIME

    # t1_1start           = 100e-9    ### WTF? If I try to change it nothing change. If it is 0 - pulses inverted. Mistery stuff.. It doesent work properly

    t2_start = t1_1start + t_read + t_between
    t1_2start = t2_start + tpi

    amplitude2 = 2 * 10**((power2)/10.)

    param_str = 'between:' + str(int(1e9*t_between)) + ';tail:' + str(int(1e9*t_tail)) + ';read:' + str(int(1e9*t_read)) + ';\nav:' + str(int(averaging)) + ';t1_1start:' + str(int(1e9*t1_1start))
    ###########################################################

    ### create data file
    data_measurement = qt.Data(name='time_plot')
    data_measurement.add_coordinate('time ',         units = 'us')
    data_measurement.add_value('V (t) ',             units = 'Volt')
    data_measurement.add_value('V std',              units = 'Volt')
    data_measurement.add_value('V2 (t) ',            units = 'Volt')
    data_measurement.add_value('V2 std',             units = 'Volt')
    data_measurement.add_value('Amp (t) ',           units = 'Volt')
    data_measurement.create_file()

    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################

    ### With Pi-pulse
    ### Preparation AWG and board
    Tabor.set_ch1_offset(awg_offset) ### !V add 191029
    board_flag = None
    Pulsing_instrument.set_trigger_time(TRIGGER_TIME)


    Pulsing_instrument.write_IQ_alwayspi_several_RO(tpi, t_read, t_read, t2_start=t2_start ,
            t1_1start=t1_1start, t1_2start=t1_2start, delta_m1_start=DELTA_M1_START, delete=False,  nsigma=SIGMA)       #now gauss
    ####  HERE AQUISITION TIME IS ALREADY AUTOMATICALLY CHANGED.
    ##### write_IQ_alwayspi_several_RO  ----- this command change ats board parameters!

    ### Preparation AWG and board  AGAIN. MAYBE ITS NOT PROPER WAY BUT OK FOR NOW
    ats9360.set_trigger_delay(initial_delay)
    qt.msleep(0.1)
    ats9360.set_acquisition_time(AQUISITION_TIME)
    qt.msleep(0.1)

    qt.msleep(0.1)
    print '__aquisition time now: ', ats9360.get_acquisition_time()
    qt.msleep(0.1)

    ################################################################################
    ### start
    qt.mstart()

    try:
        Pulsing_instrument.prep_timing(freq_cav, averaging, power) ## here error 'trying to set to small value 2e-7'
        qt.msleep(2)
        Tabor.set_ch4_output('ON')
        qt.msleep(0.1)
        Tabor.set_ch4_amplitude(amplitude2)
        qt.msleep(0.1)
        print 'Tabor ch4 output: ', Tabor.get_ch4_output()
        print 'Tabor ch4 ampl:   ', Tabor.get_ch4_amplitude()
        board_flag = True
        Tabor.set_trigger_source('TIM')
        qt.msleep(0.1)

        while ats9360.get_completed_acquisition() != 100.:
            print 'percentage done:' + str(ats9360.get_completed_acquisition())+'%'
            result = ats9360.measurement()

            ((vg_re, vg_re_std), (vg_im, vg_im_std)) = result

            t_vector_board = np.arange(len(vg_im))/ats9360.get_samplerate()*1e3

            qt.msleep(0.1)
            amp = np.sqrt((vg_re-vg_re[-1])**2+(vg_im-vg_im[-1])**2)

        Tabor.set_trigger_source('EVEN')
        ats9360.measurement_close(transfert_info=False)
        board_flag = False



    finally:
        if board_flag:
            ats9360.measurement_close(transfert_info=False)
        print ats9360.measurement_close(transfert_info=True)

        data_measurement.add_data_point(t_vector_board, vg_re, vg_re_std, vg_im, vg_im_std, amp)

    ################################################################################

    Tabor.set_trigger_source('EVEN')
    data_measurement.new_block()
    ats9360.set_trigger_delay( initial_delay + ( t_read + t_between + tpi )*1e9 )
    board_flag = None

    try:
        Pulsing_instrument.prep_timing( freq_cav, averaging, power)
        qt.msleep(2)
        Tabor.set_ch4_output('ON')
        Tabor.set_ch4_amplitude(amplitude2)
        print 'here', Tabor.get_ch4_output(), Tabor.get_ch4_amplitude()

        board_flag = True
        Tabor.set_trigger_source('TIM')

        while ats9360.get_completed_acquisition() != 100.:
            print 'percentage done:' + str(ats9360.get_completed_acquisition())+'%'

            result = ats9360.measurement()

            ((ve_re, ve_re_std), (ve_im, ve_im_std)) = result

            qt.msleep(0.1)
            amp = np.sqrt((ve_re-ve_re[-1])**2+(ve_im-ve_im[-1])**2)

        Tabor.set_trigger_source('EVEN')
        ats9360.measurement_close(transfert_info=False)
        board_flag = False


    finally:
        qt.msleep(0.2)
        if board_flag:
            ats9360.measurement_close(transfert_info=False)
        data_measurement.add_data_point(t_vector_board, ve_re, ve_re_std, ve_im, ve_im_std, amp)

        print ats9360.measurement_close(transfert_info=True)


    Tabor.set_trigger_source('EVEN')
    data_measurement.close_file()
    ats9360.set_trigger_delay(initial_delay)
    qt.mend()

    distance = np.sqrt( (ve_re - vg_re)**2 + (ve_im - vg_im)**2 )

    def normalized_function(func):
        '''
        Normalize any 1D function on 1. To make on [0,1]
        '''
        import numpy as np

        max = np.max(func) ## --> 1.0
        min = np.min(func) ## --> 0.0
        delta = max - min

        norm_func = func.copy()

        ##shift to the bottom
        norm_func = norm_func - min

        norm_func = norm_func / delta


        return norm_func

    weightfunction = normalized_function(distance)


    ### Plot my graphics ##################################

    plt.figure()
    plt.plot(t_vector_board, vg_re*1e3, label='vg_re', color='b')
    plt.plot(t_vector_board, vg_im*1e3, label='vg_im', color='darkblue')
    plt.plot(t_vector_board, ve_re*1e3, label='ve_re', color='r')
    plt.plot(t_vector_board, ve_im*1e3, label='ve_im', color='darkred')
    plt.legend()
    plt.grid()
    plt.title('Recorded voltages and weight')
    plt.xlabel('Time [ns]')
    # plt.xlabel('aquised points [-]')
    plt.ylabel('Voltage [mV]')

    plt.twinx()
    # plt.plot(t_vector_board, distance*1e3, label='distance', color='green', lw=0.5)
    # plt.ylabel('Distance [mV]')
    plt.plot(t_vector_board, weightfunction, label='weight', color='green', lw=0.5)
    plt.ylabel('Weight [n.u.]')
    plt.legend()
    [x_text, y_text] = [0,0]
    plt.text(x_text,y_text,param_str)

    save_graph= True
    if save_graph:
        import os
        filepath_pic = 'D:\\Data\\' +take_dt_str(date=True,time=True, slash=True)+  'weightfunc_pic'
        if not os.path.exists(filepath_pic):
            os.makedirs(filepath_pic)
        full_fname = filepath_pic +'\\'+ 'voltages_vs_time' + '.png'
        plt.savefig(full_fname)

    plt.close()

    return weightfunction

def do_single_shot_meas(parameters, av, counts, tl=1, use_weight=False,weightfunc=None,awg_offset=AWG_OFFSET, t_pre=None, switch_off_smb_after=True):
    '''
    Doing a single shot measurement. Returning raw data [re_g, im_g, re_e, im_e, re_g_post, im_g_post, re_e_post, im_e_post]
    '''
    if counts > 2e4:
        print 'too much value for counts can produce ATS-board crash memory. use averages'

    ### real_num_of_meas = counts * (av/2) ## dont ask me why. Ask Remy...
    ### realy it is no averaging doing anyway

    #######PARAMETERS###########################################################
    # function for check validity of GausSigma
    def check_nsigma(value):
        if value < 0:
            value = 0
            print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
        if value > 5:
            value = 5
            print 'Warning_Fidelity: Gaussigma was >5, changed to 5'
        return value
    ###_____variables_from_param____###
    try:
        freq_read = parameters.freq_read
        power1 = parameters.power1
        t_read = parameters.t_read
        t_between = parameters.t_between #in seconds ~300e-9

        freq_q = parameters.freq_q
        power2 = parameters.power2
        tpi = parameters.tpi
        GausSigma = parameters.nsigma
    except:
        print 'WARNING: (Fidelity) one of parameters is not defined!'


    ### Check t_between for valid ####
    # t_between = 300e-9  ##it is inside parameters now
    if t_between < 0:
        print 'Error do_single_shot_meas(): t_between < 0'
        return False
    if t_between > 20e-6:
        print 'Error do_single_shot_meas(): t_between > 10us'
        return False

        ##### IMPLEMENT IT LATER #### (possibility to not use pre-pulse)
    # NO_PRE = False
    # if t_between == 0:
    #     print '____No Pre_pulse regime (t_between == 0)'
    #     NO_PRE = True

    ###################################
    ###_____intrinisic_variables____###

    ### t1_1
    if t_pre is not None:
        t1_1 = t_pre
    else:
        t1_1 = t_read

    ### t1_2
    t1_2 = t_read


    ## this I don't know and just keep it
    t_rise = None  #error if it is not None... wtf...
    tau = 50 #in ns ### !V tau (looks like it change nothing anyway)


    t1_1start = 100e-9      ### better keep it constant
    t_protect = 0.
    delta_m1_start = 100e-9

    ### this i need to undertand
    delta_t = 250.          ### is it equal to 't_tail in weight?'

    # tpi - duration of pi pulse
    # t2_start - tone_2_start time of starting of pi-pulse (we guess)
    # t1_1start  - start of first readout pulse
    # t1_2start - start of second readout pulse

    t2_start = t1_1start + t1_1 + t_between
    t1_2start = t2_start + tpi
    acq_time = (t1_2start + t1_2)*1e9 + delta_t + 300.

### CAreful here !V 191030
    # t_tail = 200e-9
    # acq_time = (t_read + t_tail)*1e9
    # acq_time = 384


    #####                                                                               #    |-\___
    #diff_PdB=-0 - means that readout pulse is simple, but if you change it pulse become ___|      \_
    diff_PdB=-0
    #####

    ############################################################################


    Pulsing_instrument.set_routing_awg({'secondtone_channel':4})
    if tl:
        t1 = datetime.datetime.now()
        print 'Single-shot Tabor loading...'
        Pulsing_instrument.set_trigger_time(200.)
        GausSigma = check_nsigma(GausSigma)

        Pulsing_instrument.write_IQpi_several_RO_bifurcationshape(tpi, t1_1, t1_2, duty_cycle=0.05, diff_PdB=diff_PdB, t2_start=t2_start ,
                t1_1start=t1_1start, t1_2start=t1_2start, t_rise= t_rise, delta_m1_start=delta_m1_start, delete=True, nsigma=GausSigma)
        Tabor.set_ch1_offset(awg_offset)
        t2 = datetime.datetime.now()
        print "___time Tabor loading: ", t2-t1

    board_flag = None

    qt.msleep(0.1)
    print '__aquisition time before start: ', ats9360.get_acquisition_time()
    qt.msleep(0.1)

    qt.mstart()
    all_smb_on()

    t1 = datetime.datetime.now()
    print "srr measurement started (don't interrupt)"

    try:
        real_a = []
        imag_a = []
        real_b = []
        imag_b = []

        if not use_weight:
            print 'no weightfunction'
            Pulsing_instrument.prep_IQ_2_sevRO(counts, av, freq_read, power1,
                    freq_q, power2, acq_time, t1_1*1e9 - t_protect, 0.,
                    t1_2*1e9 - t_protect, t1_2start*1e9 -t1_1start*1e9, delta_t, tau=tau)
        else:
            if weightfunc is None:
                print 'make the weightfunction'
                graph_weight = True
                weightfunc = make_weightfunc(parameters, graph=graph_weight)

            Pulsing_instrument.prep_IQ_2_sevRO(counts, av, freq_read, power1,
                    freq_q, power2, acq_time, t1_1*1e9 - t_protect, 0.,
                    t1_2*1e9 - t_protect, t1_2start*1e9 -t1_1start*1e9, delta_t,  weightfunc=weightfunc, wf=1)

        qt.msleep(2)
        board_flag = True
        Tabor.set_trigger_source('TIM')

        qt.msleep(0.1)
        print '__aquisition time during measurement: ', ats9360.get_acquisition_time()
        qt.msleep(0.1)

        while ats9360.get_completed_acquisition() != 100.:
            result = ats9360.measurement()      #result we obtain from the board
            if use_weight:
                ((real, real2), (imag, imag2)) = result
                real_a = np.append(real_a, real )
                imag_a = np.append(imag_a, imag )
                real_b = np.append(real_b, real2 )
                imag_b = np.append(imag_b, imag2 )
            else:
                ((real, real2, re0), (imag, imag2, im0)) = result
                real_a = np.append(real_a, real - np.mean(re0))
                imag_a = np.append(imag_a, imag - np.mean(im0))
                real_b = np.append(real_b, real2 - np.mean(re0))
                imag_b = np.append(imag_b, imag2 - np.mean(im0))
            qt.msleep(0.1)

        Tabor.set_trigger_source('EVEN')
        try:
            ats9360.measurement_close(transfert_info=False)
            board_flag = False
        except:
            qt.msleep(2.)
            ats9360.measurement_close(transfert_info=False)
            board_flag = False
    finally:
        if board_flag:
            try:
                ats9360.measurement_close(transfert_info=False)
                Tabor.set_trigger_source('EVEN')
            except:
                qt.msleep(2.)
                ats9360.measurement_close(transfert_info=False)
                Tabor.set_trigger_source('EVEN')

    qt.mend()
    if switch_off_smb_after:
        all_smb_off()
    t2 = datetime.datetime.now()
    print "srr measurement finished"
    print "___time measurement ssr:",  t2-t1

    qt.msleep(0.1)
    print '__aquisition after measurement: ', ats9360.get_acquisition_time()
    qt.msleep(0.1)


    re_e = real_b[::2]              # Re-part of reaout AFTER PI-pulse
    re_g = real_b[1::2]             # Re-part of readout the g-state
    im_e = imag_b[::2]              # Im-part of reaout AFTER PI-pulse
    im_g = imag_b[1::2]             # Im-part of readout the g-state
    re_e_post = real_a[::2]       # Re-part of presel reaoudt BEFORE PI-pulse   ## CHANGED on 11/06/2021
    re_g_post = real_a[1::2]      # Re-part of presel the g-state               ## CHANGED on 11/06/2021
    im_e_post = imag_a[::2]       # Im-part of presel reaoudt BEFORE PI-pulse   ## CHANGED on 11/06/2021
    im_g_post = imag_a[1::2]      # Im-part of presel the g-state               ## CHANGED on 11/06/2021

    return [re_g, im_g, re_e, im_e, re_g_post, im_g_post, re_e_post, im_e_post]

def get_fidelity(parameters,av=4,counts=5e3,tl=1, weightfunc=None, DOWEIGHT=False, nbins=200, awg_offset=AWG_OFFSET, title='', t_pre=None, switch_off_smb_after=True):
    '''
    Version 28 10 2019
    weightfunc - given weightfunction, if measured already
    prepweight - if True, weightfunction will be created (make it a part of the object SSR)
    t_pre -  time duration of the pre_pulse. if None - equal to t_readout in parameters-object

    add it
    t_between=200e-9, awg_offset=AWG_OFFSET,
    no_pre=False,use_weight=False,weightfunc=None,
    title='Raw data SingleShot' === fname='1_SingleShot',
    before av=2, counts=1e4

    '''
    # smb_cavity_on()
    # all_smb_on()  # it all in do_single_shot !

    if parameters.t_between < 50e-9:
        print '\n\n_____(!)_parameters.t_between is less than 50ns____' #it's not good, i've checked

    if parameters.t_between > 2*parameters.t_read:
        print '\n\n_____(!)_parameters.t_between is more than 2 t_read____' #it's not good, i've checked

    script_stopclock = Stopclock()

    if counts > 40e3:
        print "\n (!) Attention get_fidelity() number of counts is too big and can produce an Alazar error. To increase the statistics use more averages av. It does not make any averages actually, just make more points \n \n "

    ### collect the data
    if DOWEIGHT is True:
        weight_stopclock = Stopclock()
        weightfunc = make_weightfunc(parameters, awg_offset=awg_offset)
        print '____Time weightgunc preparation:', weight_stopclock.stop()

        res_list = do_single_shot_meas(parameters, av, counts, tl=tl,  use_weight=True, weightfunc=weightfunc,  awg_offset=awg_offset, t_pre=t_pre, switch_off_smb_after=switch_off_smb_after )
        str_weight = '_wgt_'



    elif weightfunc is not None:
        res_list = do_single_shot_meas(parameters, av, counts, tl=tl,  use_weight=True, weightfunc=weightfunc,  awg_offset=awg_offset, t_pre=t_pre)
        str_weight = '_wgt_'

    else:
        res_list = do_single_shot_meas(parameters, av, counts, tl=tl, awg_offset=awg_offset,  t_pre=t_pre )
        str_weight = ''

    ############################################################################
    ### PROCESSING ####
    processing_stopclock = Stopclock()

    from lib_SSResult_processing import SSResult   ### !V 20200224 update
    ssr = SSResult( data = res_list, param=parameters, nbins=nbins )
    ssr.weightfunc = weightfunc     # not accurate but ok for now for save it

    str_fid_post = "_F={:03.1f}%".format(ssr.dict_fidelity['F_post']*100)

    print '____Time ssr processing :', processing_stopclock.stop()


    ############################################################################

    # datetime = take_dt_str(date=True,time=True, slash=True)
    title +=str_fid_post
    timestr = take_dt_str(date=False,time=True, slash=False)
    datasave_stopclock = Stopclock()

    ### save parameters ###
    parameters.save(name='parameters_Fidelity'+str_weight)

    ### save the data and keep folderadress
    data_measurement = save_data(res_list, coordinats = [], values=['re_g','im_g','re_e','im_e','re_g_preselect','im_g_preselect','re_e_preselect','im_e_preselect'], name='SingleShot'+title+str_weight)
    datapath = data_measurement.get_filepath()
    datafname = data_measurement.get_filename()
    datafolder = datapath[ 0 : len(datapath)-len(datafname) ]

    ### save object with processed data ###
    filepath_ssr = datafolder
    ssr.datafile = datapath #save path to raw datafile
    ssr.autosafe()
    # datafname = datafname[0:-4] # removing ".dat" in the end of the name
    # ssr.save_ssr_as_object(filepath_ssr +datafname)

    print '____Time ssr datasaving :', datasave_stopclock.stop()

    ### make and save pictures
    filepath_pic = datafolder
    ssr.plot_scatter_two_blob(save=True, show=False, savepath=filepath_pic, fname=timestr+'_Blobs', zero_on_plot=True, title_str=title, limits=[None,None,None,None])
    ssr.plot_hists(regime='raw_data_and_pre', log=True,show=False,  save=True, savepath=filepath_pic, fname=timestr+'_Hists_log')
    # ssr.plot_hists(regime='raw_data_and_pre', log=False,show=False, save=True, savepath=filepath_pic, fname=timestr+'_Hists')
    ssr.plot_hists_unitless(regime='raw_data_and_pre',log=False,show=False, save=True, savepath=filepath_pic, fname=timestr+'_ul_hists')
    ssr.plot_hists(regime='raw_and_selected', log=True,show=False,  save=True, savepath=filepath_pic, fname=timestr+'_Hists_post_log') # added on June 3rd 2021 for debugging

    ############################################################################

    ### print result in terminal and return object
    print '\n'
    print '    F = ', ssr.dict_fidelity['F']
    print 'Fpost = ', ssr.dict_fidelity['F_post']


    gc.collect()
    # all_smb_off()
    print "TOTAL TIME of get_fidelity()", script_stopclock.stop()

    return ssr

def do_QNDness_meas(parameters, av, counts, t_dwell=None, tl=1, use_weight=False,weightfunc=None,awg_offset=AWG_OFFSET, t_pre=None, switch_off_smb_after=True):
    '''
    Doing a QNDness measurement. Returning raw data [re_g_post, im_g_post, re_e_post, im_e_post, re1_g, im1_g, re1_e, im1_e, re2_g, im2_g, re2_e, im2_e]
    We send pre-pulse, then pi-pulse, then 1st read-out pulse, then 2nd read-out pulse.
    t_dwell (s) is the waiting time time 1st and 2nd read-out pulses, set to parameters.t_between by default.
    '''
    if counts > 2e4:
        print 'too much value for counts can produce ATS-board crash memory. use averages'

    #######PARAMETERS###########################################################
    # function for check validity of GausSigma
    def check_nsigma(value):
        if value < 0:
            value = 0
            print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
        if value > 5:
            value = 5
            print 'Warning_Fidelity: Gaussigma was >5, changed to 5'
        return value
    ###_____variables_from_param____###
    try:
        freq_read = parameters.freq_read
        power1 = parameters.power1
        t_read = parameters.t_read
        t_between = parameters.t_between #in seconds ~300e-9

        freq_q = parameters.freq_q
        power2 = parameters.power2
        tpi = parameters.tpi
        GausSigma = parameters.nsigma
    except:
        print 'WARNING: (Fidelity) one of parameters is not defined!'


    ### Check t_between for valid ####

    if t_between < 0:
        print 'Error do_single_shot_meas(): t_between < 0'
        return False
    if t_between > 20e-6:
        print 'Error do_single_shot_meas(): t_between > 10us'
        return False

    if t_dwell == None:
        t_dwell = t_between

    ###################################
    ###_____intrinisic_variables____###

    ### t1_1
    if t_pre is not None:
        t1_1 = t_pre
    else:
        t1_1 = t_read

    ### t1_2 and t1_3
    t1_2 = t_read
    t1_3 = t_read


    t_rise = None  # probably the duration of transient when a read-out pulse is applied (only used for safety checks)
    tau = None       # [ns] time constant used in the weight function

    t1_1start = 100e-9      ### better keep it constant
    t_protect = 0.
    delta_m1_start = 100e-9

    ### this i need to undertand
    delta_t = 250.          ### is it equal to 't_tail in weight?'

    # tpi - duration of pi pulse
    # t2_start - tone_2_start time of starting of pi-pulse (we guess)
    # t1_1start - start of pre-pulse
    # t1_2start - start of first readout pulse
    # t1_3start - start of second readout pulse

    t2_start = t1_1start + t1_1 + t_between
    t1_2start = t2_start + tpi
    t1_3start = t1_2start + t1_2 + t_dwell
    acq_time = (t1_3start + t1_3)*1e9 + delta_t + 300.

    #####                                                                               #    |-\___
    #diff_PdB=-0 - means that readout pulse is simple, but if you change it pulse become ___|      \_
    diff_PdB=-0
    #####


    Pulsing_instrument.set_routing_awg({'secondtone_channel':4})
    if tl:
        t_begin = datetime.datetime.now()
        print 'Single-shot Tabor loading...'
        Pulsing_instrument.set_trigger_time(200.)
        GausSigma = check_nsigma(GausSigma)

        Pulsing_instrument.write_QNDness_several(tpi, t1_1, t1_2, t1_3, duty_cycle=0.05, diff_PdB=diff_PdB, t2_start=t2_start ,
                t1_1start=t1_1start, t1_2start=t1_2start, t1_3start=t1_3start, t_rise= t_rise, delta_m1_start=delta_m1_start, delete=True, nsigma=GausSigma)
        Tabor.set_ch1_offset(awg_offset)
        t_end = datetime.datetime.now()
        print "___time Tabor loading: ", t_end-t_begin

    board_flag = None

    qt.msleep(0.1)
    print '__aquisition time before start: ', ats9360.get_acquisition_time()
    qt.msleep(0.1)

    qt.mstart()
    all_smb_on()

    t_begin = datetime.datetime.now()
    print "QNDness measurement started (don't interrupt)"

    try:
        real_a = [] # pre-pulse
        imag_a = []
        real_b = [] # 1st read-out pulse
        imag_b = []
        real_c = [] # 2nd read-out pulse
        imag_c = []

        if not use_weight:
            print 'no weightfunction'
            Pulsing_instrument.prep_QNDness_sevRO(counts, av, freq_read, power1,
                    freq_q, power2, acq_time, t1_1*1e9 - t_protect, 0.,
                    t1_2*1e9 - t_protect, t1_2start*1e9 - t1_1start*1e9,
                    t1_3*1e9 - t_protect, t1_3start*1e9 - t1_1start*1e9, delta_t, tau=tau)
        else:
            if weightfunc is None:
                print 'make the weightfunction'
                graph_weight = True
                weightfunc = make_weightfunc(parameters, graph=graph_weight)

            Pulsing_instrument.prep_QNDness_sevRO(counts, av, freq_read, power1,
                    freq_q, power2, acq_time, t1_1*1e9 - t_protect, 0.,
                    t1_2*1e9 - t_protect, t1_2start*1e9 -t1_1start*1e9,
                    t1_3*1e9 - t_protect, t1_3start*1e9 - t1_1start*1e9, delta_t,  weightfunc=weightfunc, wf=1)

        qt.msleep(2)
        board_flag = True
        Tabor.set_trigger_source('TIM')

        qt.msleep(0.1)
        print '__aquisition time during measurement: ', ats9360.get_acquisition_time()
        qt.msleep(0.1)

        while ats9360.get_completed_acquisition() != 100.:
            result = ats9360.measurement()      #result we obtain from the board
            if use_weight:
                ((real, real2, real3), (imag, imag2, imag3)) = result
                real_a = np.append(real_a, real )
                imag_a = np.append(imag_a, imag )
                real_b = np.append(real_b, real2 )
                imag_b = np.append(imag_b, imag2 )
                real_c = np.append(real_c, real3 )
                imag_c = np.append(imag_c, imag3 )
            else:
                ((real, real2, real3, re0), (imag, imag2, imag3, im0)) = result
                real_a = np.append(real_a, real - np.mean(re0))
                imag_a = np.append(imag_a, imag - np.mean(im0))
                real_b = np.append(real_b, real2 - np.mean(re0))
                imag_b = np.append(imag_b, imag2 - np.mean(im0))
                real_c = np.append(real_c, real3 - np.mean(re0))
                imag_c = np.append(imag_c, imag3 - np.mean(im0))
            qt.msleep(0.1)

        Tabor.set_trigger_source('EVEN')
        try:
            ats9360.measurement_close(transfert_info=False)
            board_flag = False
        except:
            qt.msleep(2.)
            ats9360.measurement_close(transfert_info=False)
            board_flag = False
    finally:
        if board_flag:
            try:
                ats9360.measurement_close(transfert_info=False)
                Tabor.set_trigger_source('EVEN')
            except:
                qt.msleep(2.)
                ats9360.measurement_close(transfert_info=False)
                Tabor.set_trigger_source('EVEN')

    qt.mend()
    if switch_off_smb_after:
        all_smb_off()
    t_end = datetime.datetime.now()
    print "srr measurement finished"
    print "___time measurement ssr:",  t_end-t_begin

    qt.msleep(0.1)
    print '__aquisition after measurement: ', ats9360.get_acquisition_time()
    qt.msleep(0.1)

    re_e_post = real_a[::2]       # Re-part of presel reaoudt BEFORE PI-pulse
    re_g_post = real_a[1::2]      # Re-part of presel the g-state
    im_e_post = imag_a[::2]       # Im-part of presel reaoudt BEFORE PI-pulse
    im_g_post = imag_a[1::2]      # Im-part of presel the g-state
    re1_e = real_b[::2]              # Re-part of 1st reaout AFTER PI-pulse
    re1_g = real_b[1::2]             # Re-part of 1st readout the g-state
    im1_e = imag_b[::2]              # Im-part of 1st reaout AFTER PI-pulse
    im1_g = imag_b[1::2]             # Im-part of 1st readout the g-state
    re2_e = real_c[::2]              # Re-part of 2nd reaout AFTER PI-pulse
    re2_g = real_c[1::2]             # Re-part of 2nd readout the g-state
    im2_e = imag_c[::2]              # Im-part of 2nd reaout AFTER PI-pulse
    im2_g = imag_c[1::2]             # Im-part of 2nd readout the g-state


    return [re_g_post, im_g_post, re_e_post, im_e_post, re1_g, im1_g, re1_e, im1_e, re2_g, im2_g, re2_e, im2_e]

def get_QNDness(parameters,av=4,counts=5e3,t_dwell=None,tl=1, weightfunc=None, DOWEIGHT=False, nbins=200, awg_offset=AWG_OFFSET, title='', t_pre=None, switch_off_smb_after=True):
    '''
    Version 07 07 2021
    weightfunc - given weightfunction, if measured already
    prepweight - if True, weightfunction will be created (make it a part of the object SSR)
    t_pre -  time duration of the pre_pulse. if None - equal to t_readout in parameters-object

    add it
    t_between=200e-9, awg_offset=AWG_OFFSET,
    no_pre=False,use_weight=False,weightfunc=None,
    title='Raw data SingleShot' === fname='1_SingleShot',
    before av=2, counts=1e4

    '''

    if parameters.t_between < 50e-9:
        print '\n\n_____(!)_parameters.t_between is less than 50ns____' #it's not good, i've checked

    if parameters.t_between > 2*parameters.t_read:
        print '\n\n_____(!)_parameters.t_between is more than 2 t_read____' #it's not good, i've checked

    script_stopclock = Stopclock()

    if counts > 40e3:
        print "\n (!) Attention get_QNDness() number of counts is too big and can produce an Alazar error. To increase the statistics use more averages av. It does not make any averages actually, just make more points \n \n "

    ### collect the data
    if DOWEIGHT is True:
        weight_stopclock = Stopclock()
        weightfunc = make_weightfunc(parameters, awg_offset=awg_offset)
        print '____Time weightgunc preparation:', weight_stopclock.stop()

        res_list = do_QNDness_meas(parameters, av, counts, t_dwell=t_dwell, tl=tl,  use_weight=True, weightfunc=weightfunc,  awg_offset=awg_offset, t_pre=t_pre, switch_off_smb_after=switch_off_smb_after )
        str_weight = '_wgt_'



    elif weightfunc is not None:
        res_list = do_QNDness_meas(parameters, av, counts, t_dwell=t_dwell, tl=tl,  use_weight=True, weightfunc=weightfunc,  awg_offset=awg_offset, t_pre=t_pre)
        str_weight = '_wgt_'

    else:
        res_list = do_QNDness_meas(parameters, av, counts, t_dwell=t_dwell, tl=tl, awg_offset=awg_offset,  t_pre=t_pre )
        str_weight = ''

    ############################################################################
    ### PROCESSING ####
    processing_stopclock = Stopclock()

    from lib_SSResult_processing import QNDnessResult

    qndness_res = QNDnessResult( data = res_list, param=parameters, nbins=nbins, use_ro2=False )
    qndness_res.weightfunc = weightfunc     # not accurate but ok for now for save it

    p_gg = qndness_res.dict_corr['p_gg']     # half of the measurements are g-state and the other are g-state
    p_ee = qndness_res.dict_corr['p_ee']
    p_ge = qndness_res.dict_corr['p_ge']
    p_eg = qndness_res.dict_corr['p_eg']

    hist_probas = [p_gg, p_ee, p_ge, p_eg]
    label_list = ['p_gg={:.2f}%'.format(p_gg*100.), 'p_ee={:.2f}%'.format(p_ee*100.),
                'p_ge={:.2f}%'.format(p_ge*100.), 'p_eg={:.2f}%'.format(p_eg*100.)]

    qnd = (p_gg+p_ee)/2.

    fig, ax = plt.subplots()
    ax.bar(np.arange(4), hist_probas)
    if t_dwell==None:
        t_dwell = parameters.t_between
    ax.set_title('Correlations histogram between 1st and 2nd readout\n time between readouts={:d}ns/ rudat={:d}dB'.format(int(t_dwell*1e9), int(parameters.rudat)))
    ax.set_xticks(np.arange(4))
    ax.set_xticklabels(label_list)
    plt.grid()

    str_fid_post = "_QND={:03.1f}%".format(qnd*100)

    print '____Time QNDness processing :', processing_stopclock.stop()


    ############################################################################

    # # datetime = take_dt_str(date=True,time=True, slash=True)
    # title +=str_fid_post
    timestr = take_dt_str(date=False,time=True, slash=False)
    datasave_stopclock = Stopclock()

    ### save parameters ###
    parameters.save(name='parameters_QNDness_probas'+str_weight)

    ### save the data and keep folderadress
    data_measurement = save_data(res_list, coordinats = [], values=['re_g_preselect','im_g_preselect','re_e_preselect','im_e_preselect','re1_g','im1_g','re1_e','im1_e','re2_g','im2_g','re2_e','im2_e'], name='QNDness_probas'+title+str_weight)
    datapath = data_measurement.get_filepath()
    datafname = data_measurement.get_filename()
    datafolder = datapath[ 0 : len(datapath)-len(datafname) ]

    ### save histogram
    plt.savefig(datafolder+'Correlation_Histo.png')
    plt.close()

    ### save object with processed data ###
    filepath_QNDness = datafolder
    qndness_res.datafile = datapath #save path to raw datafile
    qndness_res.autosafe()
    # datafname = datafname[0:-4] # removing ".dat" in the end of the name
    # ssr.save_ssr_as_object(filepath_QNDness +datafname)

    print '____Time QNDness datasaving :', datasave_stopclock.stop()

    # ### make and save pictures
    # filepath_pic = datafolder
    # ssr.plot_scatter_two_blob(save=True, show=False, savepath=filepath_pic, fname=timestr+'_Blobs', zero_on_plot=True, title_str=title, limits=[None,None,None,None])
    # ssr.plot_hists(regime='raw_data_and_pre', log=True,show=False,  save=True, savepath=filepath_pic, fname=timestr+'_Hists_log')
    # # ssr.plot_hists(regime='raw_data_and_pre', log=False,show=False, save=True, savepath=filepath_pic, fname=timestr+'_Hists')
    # ssr.plot_hists_unitless(regime='raw_data_and_pre',log=False,show=False, save=True, savepath=filepath_pic, fname=timestr+'_ul_hists')
    # ssr.plot_hists(regime='raw_and_selected', log=True,show=False,  save=True, savepath=filepath_pic, fname=timestr+'_Hists_post_log') # added on June 3rd 2021 for debugging

    #########################################################################

    ### print result in terminal and return object
    print '\n'
    print '    QND = ', qnd


    gc.collect()
    print "TOTAL TIME of get_QNDness()", script_stopclock.stop()

    return qndness_res

def do_single_shot_pio2_meas(parameters, av, counts, t_dwell=None, tl=1, use_weight=False,weightfunc=None,awg_offset=AWG_OFFSET, t_pre=None, switch_off_smb_after=True):
    '''
    Doing a single shot measurement with pi/2-pulse. Sequence is: pre-pulse, pi/2-pulse, 1st readout, 2nd readout.
    Returning raw data [re_post, im_post, re1, im1, re2, im2]
    We send pre-pulse, then pi-pulse, then 1st read-out pulse, then 2nd read-out pulse.
    t_dwell (s) is the waiting time time 1st and 2nd read-out pulses, set to parameters.t_between by default.
    '''
    if counts > 2e4:
        print 'too much value for counts can produce ATS-board crash memory. use averages'

    #######PARAMETERS###########################################################
    # function for check validity of GausSigma
    def check_nsigma(value):
        if value < 0:
            value = 0
            print 'Warning_Fidelity: Gaussigma was <0, changed to 0'
        if value > 5:
            value = 5
            print 'Warning_Fidelity: Gaussigma was >5, changed to 5'
        return value
    ###_____variables_from_param____###
    try:
        freq_read = parameters.freq_read
        power1 = parameters.power1
        t_read = parameters.t_read
        t_between = parameters.t_between # in seconds

        freq_q = parameters.freq_q
        power2 = parameters.power2
        tpio2 = np.round(parameters.tpi/2, 9) # in seconds, rounded to the ns
        GausSigma = parameters.nsigma
    except:
        print 'WARNING: (Fidelity) one of parameters is not defined!'


    ### Check t_between for valid ####

    if t_between < 0:
        print 'Error do_single_shot_meas(): t_between < 0'
        return False
    if t_between > 20e-6:
        print 'Error do_single_shot_meas(): t_between > 10us'
        return False

    if t_dwell == None:
        t_dwell = t_between

    ###################################
    ###_____intrinisic_variables____###

    ### t1_1
    if t_pre is not None:
        t1_1 = t_pre
    else:
        t1_1 = t_read

    ### t1_2 and t1_3
    t1_2 = t_read
    t1_3 = t_read


    t_rise = None  # probably the duration of transient when a read-out pulse is applied (only used for safety checks)
    tau = None       # [ns] time constant used in the weight function

    t1_1start = 100e-9      ### better keep it constant
    t_protect = 0.
    delta_m1_start = 100e-9

    ### this i need to undertand
    delta_t = 250.          ### is it equal to 't_tail in weight?'

    # tpi - duration of pi pulse
    # t2_start - tone_2_start time of starting of pi-pulse (we guess)
    # t1_1start - start of pre-pulse
    # t1_2start - start of first readout pulse
    # t1_3start - start of second readout pulse

    t2_start = t1_1start + t1_1 + t_between
    t1_2start = t2_start + tpio2
    t1_3start = t1_2start + t1_2 + t_dwell
    acq_time = (t1_3start + t1_3)*1e9 + delta_t + 300.

    #####                                                                               #    |-\___
    #diff_PdB=-0 - means that readout pulse is simple, but if you change it pulse become ___|      \_
    diff_PdB=-0
    #####


    Pulsing_instrument.set_routing_awg({'secondtone_channel':4})
    if tl:
        t_begin = datetime.datetime.now()
        print 'Single-shot Tabor loading...'
        Pulsing_instrument.set_trigger_time(200.)
        GausSigma = check_nsigma(GausSigma)

        Pulsing_instrument.write_QNDness_withpi(tpio2, t1_1, t1_2, t1_3, duty_cycle=0.05, diff_PdB=diff_PdB, t2_start=t2_start ,
                t1_1start=t1_1start, t1_2start=t1_2start, t1_3start=t1_3start, t_rise= t_rise, delta_m1_start=delta_m1_start, delete=True, nsigma=GausSigma)
        Tabor.set_ch1_offset(awg_offset)
        t_end = datetime.datetime.now()
        print "___time Tabor loading: ", t_end-t_begin

    board_flag = None

    qt.msleep(0.1)
    print '__aquisition time before start: ', ats9360.get_acquisition_time()
    qt.msleep(0.1)

    qt.mstart()
    all_smb_on()

    t_begin = datetime.datetime.now()
    print "QNDness measurement started (don't interrupt)"

    try:
        real_a = [] # pre-pulse
        imag_a = []
        real_b = [] # 1st read-out pulse
        imag_b = []
        real_c = [] # 2nd read-out pulse
        imag_c = []

        if not use_weight:
            print 'no weightfunction'
            Pulsing_instrument.prep_QNDness_sevRO(counts, av, freq_read, power1,
                    freq_q, power2, acq_time, t1_1*1e9 - t_protect, 0.,
                    t1_2*1e9 - t_protect, t1_2start*1e9 - t1_1start*1e9,
                    t1_3*1e9 - t_protect, t1_3start*1e9 - t1_1start*1e9, delta_t, tau=tau)
        else:
            if weightfunc is None:
                print 'make the weightfunction'
                graph_weight = True
                weightfunc = make_weightfunc(parameters, graph=graph_weight)

            Pulsing_instrument.prep_QNDness_withpi(counts, av, freq_read, power1,
                    freq_q, power2, acq_time, t1_1*1e9 - t_protect, 0.,
                    t1_2*1e9 - t_protect, t1_2start*1e9 -t1_1start*1e9,
                    t1_3*1e9 - t_protect, t1_3start*1e9 - t1_1start*1e9, delta_t,  weightfunc=weightfunc, wf=1)

        qt.msleep(2)
        board_flag = True
        Tabor.set_trigger_source('TIM')

        qt.msleep(0.1)
        print '__aquisition time during measurement: ', ats9360.get_acquisition_time()
        qt.msleep(0.1)

        while ats9360.get_completed_acquisition() != 100.:
            result = ats9360.measurement()      #result we obtain from the board
            if use_weight:
                ((real, real2, real3), (imag, imag2, imag3)) = result
                real_a = np.append(real_a, real )
                imag_a = np.append(imag_a, imag )
                real_b = np.append(real_b, real2 )
                imag_b = np.append(imag_b, imag2 )
                real_c = np.append(real_c, real3 )
                imag_c = np.append(imag_c, imag3 )
            else:
                ((real, real2, real3, re0), (imag, imag2, imag3, im0)) = result
                real_a = np.append(real_a, real - np.mean(re0))
                imag_a = np.append(imag_a, imag - np.mean(im0))
                real_b = np.append(real_b, real2 - np.mean(re0))
                imag_b = np.append(imag_b, imag2 - np.mean(im0))
                real_c = np.append(real_c, real3 - np.mean(re0))
                imag_c = np.append(imag_c, imag3 - np.mean(im0))
            qt.msleep(0.1)

        Tabor.set_trigger_source('EVEN')
        try:
            ats9360.measurement_close(transfert_info=False)
            board_flag = False
        except:
            qt.msleep(2.)
            ats9360.measurement_close(transfert_info=False)
            board_flag = False
    finally:
        if board_flag:
            try:
                ats9360.measurement_close(transfert_info=False)
                Tabor.set_trigger_source('EVEN')
            except:
                qt.msleep(2.)
                ats9360.measurement_close(transfert_info=False)
                Tabor.set_trigger_source('EVEN')

    qt.mend()
    if switch_off_smb_after:
        all_smb_off()
    t_end = datetime.datetime.now()
    print "srr measurement finished"
    print "___time measurement ssr:",  t_end-t_begin

    qt.msleep(0.1)
    print '__aquisition after measurement: ', ats9360.get_acquisition_time()
    qt.msleep(0.1)

    re_post = real_a          # Re-part of presel reaoudt BEFORE PI/2-pulse
    im_post = imag_a          # Im-part of presel reaoudt BEFORE PI/2-pulse
    re1 = real_b              # Re-part of 1st reaout AFTER PI/2-pulse
    im1 = imag_b              # Im-part of 1st reaout AFTER PI/2-pulse
    re2 = real_c              # Re-part of 2nd reaout AFTER PI/2-pulse
    im2 = imag_c              # Im-part of 2nd reaout AFTER PI/2-pulse


    return [re_post, im_post, re1, im1, re2, im2]

def get_fidelity_pio2pulse(parameters,av=4,counts=5e3,t_dwell=None,tl=1, weightfunc=None, DOWEIGHT=False, nbins=200, awg_offset=AWG_OFFSET, title='', t_pre=None, switch_off_smb_after=True):
    '''
    Version 12 07 2021
    weightfunc - given weightfunction, if measured already
    prepweight - if True, weightfunction will be created (make it a part of the object SSR)
    t_pre -  time duration of the pre_pulse. if None - equal to t_readout in parameters-object

    add it
    t_between=200e-9, awg_offset=AWG_OFFSET,
    no_pre=False,use_weight=False,weightfunc=None,
    title='Raw data SingleShot' === fname='1_SingleShot',
    before av=2, counts=1e4

    '''

    if parameters.t_between < 50e-9:
        print '\n\n_____(!)_parameters.t_between is less than 50ns____' #it's not good, i've checked

    if parameters.t_between > 2*parameters.t_read:
        print '\n\n_____(!)_parameters.t_between is more than 2 t_read____' #it's not good, i've checked

    script_stopclock = Stopclock()

    if counts > 40e3:
        print "\n (!) Attention get_fidelity_pio2pulse() number of counts is too big and can produce an Alazar error. To increase the statistics use more averages av. It does not make any averages actually, just make more points \n \n "

    ### collect the data
    if DOWEIGHT is True:
        weight_stopclock = Stopclock()
        weightfunc = make_weightfunc(parameters, awg_offset=awg_offset)
        print '____Time weightgunc preparation:', weight_stopclock.stop()

        res_list = do_single_shot_pio2_meas(parameters, av, counts, t_dwell=t_dwell, tl=tl,  use_weight=True, weightfunc=weightfunc,  awg_offset=awg_offset, t_pre=t_pre, switch_off_smb_after=switch_off_smb_after )
        str_weight = '_wgt_'



    elif weightfunc is not None:
        res_list = do_single_shot_pio2_meas(parameters, av, counts, t_dwell=t_dwell, tl=tl,  use_weight=True, weightfunc=weightfunc,  awg_offset=awg_offset, t_pre=t_pre)
        str_weight = '_wgt_'

    else:
        res_list = do_single_shot_pio2_meas(parameters, av, counts, t_dwell=t_dwell, tl=tl, awg_offset=awg_offset,  t_pre=t_pre )
        str_weight = ''

    # ############################################################################
    # ### PROCESSING ####
    # processing_stopclock = Stopclock()
    #
    # ssr_ref = get_fidelity(parameters, av=4, counts=5e3)
    #
    # ext_data = [ssr_ref.re_g, ssr_ref.im_g, ssr_ref.re_e, ssr_ref.im_e]
    # ext_threshold = ssr_ref.threshold
    #
    # from lib_SSResult_processing import SSResult_pio2
    # ssr = SSResult_pio2( data = res_list[2:], param=parameters, nbins=nbins, ext_data=ext_data, ext_threshold=ext_threshold )
    # ssr.weightfunc = weightfunc     # not accurate but ok for now for save it
    #
    # str_fid_post = "_F={:03.1f}%".format(ssr.dict_fidelity['F_post']*100)
    #
    # print '____Time ssr processing :', processing_stopclock.stop()


    ############################################################################

    # # datetime = take_dt_str(date=True,time=True, slash=True)
    # title +=str_fid_post
    timestr = take_dt_str(date=False,time=True, slash=False)
    datasave_stopclock = Stopclock()

    ### save parameters ###
    parameters.save(name='parameters_Fidelity_pio2'+str_weight)

    ### save the data and keep folderadress
    data_measurement = save_data(res_list, coordinats = [], values=['re_preselect','im_preselect','re1','im1','re2','im2'], name='Singleshot_pio2'+title+str_weight)
    datapath = data_measurement.get_filepath()
    datafname = data_measurement.get_filename()
    datafolder = datapath[ 0 : len(datapath)-len(datafname) ]

    # ### save object with processed data ###
    # filepath_ssr = datafolder
    # ssr.datafile = datapath #save path to raw datafile
    # ssr.autosafe()
    # # datafname = datafname[0:-4] # removing ".dat" in the end of the name
    # # ssr.save_ssr_as_object(filepath_ssr +datafname)
    #
    # print '____Time ssr datasaving :', datasave_stopclock.stop()

    # ### make and save pictures
    # filepath_pic = datafolder
    # ssr.plot_scatter_two_blob(save=True, show=False, savepath=filepath_pic, fname=timestr+'_Blobs', zero_on_plot=True, title_str=title, limits=[None,None,None,None])
    # ssr.plot_hists(regime='raw_data_and_pre', log=True,show=False,  save=True, savepath=filepath_pic, fname=timestr+'_Hists_log')
    # # ssr.plot_hists(regime='raw_data_and_pre', log=False,show=False, save=True, savepath=filepath_pic, fname=timestr+'_Hists')
    # ssr.plot_hists_unitless(regime='raw_data_and_pre',log=False,show=False, save=True, savepath=filepath_pic, fname=timestr+'_ul_hists')
    # ssr.plot_hists(regime='raw_and_selected', log=True,show=False,  save=True, savepath=filepath_pic, fname=timestr+'_Hists_post_log') # added on June 3rd 2021 for debugging

    # #########################################################################
    #
    # ### print result in terminal and return object
    # print '\n'
    # print '    F = ', ssr.dict_fidelity['F']
    # print 'Fpost = ', ssr.dict_fidelity['F_post']

    gc.collect()
    print "TOTAL TIME of get_fidelity_pio2pulse()", script_stopclock.stop()

    return 0

def get_echo_time(parameters, tl =1, av=1e3, t_wait_stop=2000, nop=200, graph=True, awg_offset=AWG_OFFSET, Return_all_data=False, Return_extracted_values=True, note=''):
    '''
    Measure the echo coherence time
    returns t2_echo in nanoseconds
    '''
    all_smb_on()

    if COMMENTS:
        print 'Echo coherence time measurement'
    FIT = True
    try:
        Tabor_loading = tl
        power1 = parameters.power1
        power2 = parameters.power2
        f_atom = parameters.freq_q
        f_cav = parameters.freq_read
        t_meas = parameters.t_read
        tpi = parameters.tpi
        GausSigma = parameters.nsigma
        if GausSigma !=0:
            print 'Echo: pi and pi/2 pulses are gaussians'
    except:
        print 'WARNING: (echo) one of parameters is not defined!'
        return None

    t_pi_o2 = round( tpi/2, 9 ) # [s]
    if COMMENTS:
        print 't_pi_o2: ', t_pi_o2
    delta_t = 200 # not to touch for now
    acq_time = t_meas*1e9 + delta_t + 300. # not to touch for now

    # We define the time vector of the Ramsey measurement:
    if (t_wait_stop > 100) and (2*t_wait_stop<20000):
        tr_stop = t_wait_stop*1e-9
        tr_step = round( tr_stop/nop,  9 ) # [s]
    else:
        print "\n Error of setting window. Window changed to window=1000 ns nop=200"
        tr_stop = 1e-6 # [s]
        tr_step = 5e-9 # [s]

    tr_start = 0e-9 # [s]
    T_vec = np.arange(tr_start, 2*tr_stop, 2*tr_step)
    if nop != len(T_vec):
        print "nop changed from ", nop, "to ", len(T_vec)
        nop = len(T_vec)

    nb_sequences = len(T_vec) # we define the number of sequences to acquire for the board.

    t_wait = 0e-9
    t_rise = None
    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################

    if Tabor_loading:
        # here we write in the AWG memory if the condition Tabor_loading is True
        if COMMENTS:
            print 'Tabor loading...'

        if GausSigma < 0:
            GausSigma = 0
            print 'Warning_Echo: Gaussigma was <0, changed to 0'
        if GausSigma > 5:
            GausSigma = 5
            print 'Warning_Echo: Gaussigma was >5, changed to 5'

        Pulsing_instrument.set_trigger_time(100.)
        Pulsing_instrument.write_Echo_pulsessequence(t_pi_o2,
                tr_start, tr_step, tr_stop, t_meas=t_meas, delete='all')
        Tabor.set_ch1_offset(awg_offset)


    qt.mstart()

    if type(note) != str:
        note = ''
        print 'note variable must be a string!'
    elif note != ''  and  note[0] != '_':
        note = '_'+note
    label = '_av='+str(av) +note

    parameters.save(name='parameters_Echo'+label)

    data_measurement = qt.Data(name='Echo'+label)
    data_measurement.add_coordinate('waiting time [ns]',    units = 'ns')
    data_measurement.add_value('Echo S21 [mV]',            units = 'mV')
    data_measurement.add_value('Echo Phase [rad]',         units = 'rad')
    data_measurement.add_value('Echo Re [mV]',             units = 'mV')
    data_measurement.add_value('Echo Im [mV]',             units = 'mV')
    data_measurement.add_value('Echo Dist [mV]',           units = 'mV')
    data_measurement.add_value('Echo Norm',                units = 'mV')
    data_measurement.create_file()

    if FIT:
        data_fit = qt.Data(name='Echo_fit'+label)
        data_fit.add_coordinate('Source (1-re, 2-im, 3-amp, 4-phase, 5-dist)', units = 'name')
        data_fit.add_value('T2_echo ',        units = 'ns')
        data_fit.add_value('T2_echo_error',        units = 'arb. units')
        data_fit.create_file()

    if graph:
        plot2d_1 = qt.Plot2D(data_measurement,
                          name      = 'Echo S21 ',
                          coorddim  = 0,
                          valdim    = 1,
                          maxtraces = 2)
        plot2d_2 = qt.Plot2D(data_measurement,
                            name      = 'Echo Phase ',
                            coorddim  = 0,
                            valdim    = 2,
                            maxtraces = 2)
        plot2d_3 = qt.Plot2D(data_measurement,
                          name      = 'Echo Re ',
                          coorddim  = 0,
                          valdim    = 3,
                          maxtraces = 2)
        plot2d_4 = qt.Plot2D(data_measurement,
                            name      = 'Echo Im ',
                            coorddim  = 0,
                            valdim    = 4,
                            maxtraces = 2)
        plot2d_5 = qt.Plot2D(data_measurement,
                            name      = 'Echo distance',
                            coorddim  = 0,
                            valdim    = 5)
        plot2d_6 = qt.Plot2D(data_measurement,
                            name      = 'Echo norm',
                            coorddim  = 0,
                            valdim    = 6)

    # try:
    Pulsing_instrument.prep_echo(f_cav, f_atom, av, nb_sequences,
        power1, power2, acq_time, t_meas*1e9, delta_t)

    qt.msleep(2)

    Tabor.set_trigger_source('TIM')
    while Pulsing_instrument.get_acquisition_completed() != 100.:
        #print  Pulsing_instrument.get_acquisition_completed(), '%'

        result = Pulsing_instrument.measurement()
        ((real_a, rea0), (imag_a, ima0))= result
        real_a -= rea0
        imag_a -= ima0

        ### convert to mV ###
        real_a = 1e3*real_a
        imag_a = 1e3*imag_a

        amplitude = np.sqrt(real_a**2+imag_a**2)
        complexe = (real_a + 1j*imag_a )*np.exp(1j*f_cav*Pulsing_instrument.get_electrical_phase_delay()*2*np.pi)
        phase = np.angle(complexe)
        # dist_a = np.sqrt(  (real_a-real_a[0])**2 + (imag_a-imag_a[0])**2  )     # CHANGED on 06/23/2021



        ######### COMPUTE NORM ##########
        covMat = np.cov(real_a, imag_a)
        eigenValue, eigenVector = np.linalg.eig(covMat)
        norm_a = eigenVector[0,0]*imag_a + eigenVector[0,1]*real_a  ##ok 0 : +8

        qt.msleep(0.1)

        ##------------------------------------##
        ####________FIT CURVES___###############
        ##------------------------------------##
        if FIT:
            ######### REAL ####################
            s = fit.Exponential()
            signal = real_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            amp_exp = np.max(amplitude*1e-3) ##because amp is in [mV], but formula is for [V]
            center = 0.
            decay = 1./2e3
            p0 = [background, amp_exp, center, decay]
            p = s.fit(p0, fixed = [0, 2])
            p_err = s.get_fit_errors()
            p[3] = abs(p[3]) ## no negative T2_echo
            values_from_fit = s.func(p)
            if graph:
                plot2d_3.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_3.set_plottitle('T2_echo= '+ str(int(1./p[3]))+'ns')
            re_values_from_fit = values_from_fit
            re_p = p
            re_p_err = p_err

            ######### IMAG ####################
            s = fit.Exponential()
            signal = imag_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            amp_exp = np.max(amplitude*1e-3) ##because amp is in [mV], but formula is for [V]
            center = 0.
            decay = 1./2e3
            p0 = [background, amp_exp, center, decay]
            p = s.fit(p0, fixed = [0, 2])
            p_err = s.get_fit_errors()
            p[3] = abs(p[3]) ## no negative T2_echo
            values_from_fit = s.func(p)
            if graph:
                plot2d_4.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_4.set_plottitle('T2_echo= '+ str(int(1./p[3]))+'ns')
            im_values_from_fit = values_from_fit
            im_p = p
            im_p_err = p_err

            ######### AMPL ####################
            s = fit.Exponential()
            signal = amplitude
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            amp_exp = np.max(amplitude*1e-3) ##because amp is in [mV], but formula is for [V]
            center = 0.
            decay = 1./2e3
            p0 = [background, amp_exp, center, decay]
            p = s.fit(p0, fixed = [0, 2])
            p_err = s.get_fit_errors()
            p[3] = abs(p[3]) ## no negative T2_echo
            values_from_fit = s.func(p)
            if graph:
                plot2d_1.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_1.set_plottitle('T2_echo= '+ str(int(1./p[3]))+'ns')
            amp_values_from_fit = values_from_fit
            amp_p = p
            amp_p_err = p_err

            ######### PHASE ####################
            s = fit.Exponential()
            signal = phase
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            amp_exp = np.max(amplitude*1e-3) ##because amp is in [mV], but formula is for [V]
            center = 0.
            decay = 1./2e3
            p0 = [background, amp_exp, center, decay]
            p = s.fit(p0, fixed = [0, 2])
            p_err = s.get_fit_errors()
            p[3] = abs(p[3]) ## no negative T2_echo
            values_from_fit = s.func(p)
            if graph:
                plot2d_2.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_2.set_plottitle('T2_echo= '+ str(int(1./p[3]))+'ns')
            ph_values_from_fit = values_from_fit
            ph_p = p
            ph_p_err = p_err

            ###### COMPUTE DIST (from fit) #######      # CHANGED on 06/23/2021
            id_ref = np.argmin(amp_values_from_fit)
            dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )

            ######### PHASE ####################
            s = fit.Exponential()
            signal = dist_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            amp_exp = np.max(amplitude*1e-3) ##because amp is in [mV], but formula is for [V]
            center = 0.
            decay = 1./2e3
            p0 = [background, amp_exp, center, decay]
            p = s.fit(p0, fixed = [0, 2])
            p_err = s.get_fit_errors()
            p[3] = abs(p[3]) ## no negative T2_echo
            values_from_fit = s.func(p)
            if graph:
                plot2d_5.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_5.set_plottitle('T2_echo= '+ str(int(1./p[3]))+'ns')
            dist_values_from_fit = values_from_fit
            dist_p = p
            dist_p_err = p_err

            ######### PHASE ####################
            s = fit.Exponential()
            signal = norm_a
            s.set_data(T_vec*1e9, signal)
            # guess parameters#############################################
            background = (signal.max() + signal.min() )/2.
            amp_exp = np.max(amplitude*1e-3) ##because amp is in [mV], but formula is for [V]
            center = 0.
            decay = 1./2e3
            p0 = [background, amp_exp, center, decay]
            p = s.fit(p0, fixed = [0, 2])
            p_err = s.get_fit_errors()
            p[3] = abs(p[3]) ## no negative T2_echo
            values_from_fit = s.func(p)
            if graph:
                plot2d_6.replace_inline_data_y2(T_vec*1e9, signal, values_from_fit )
                plot2d_6.set_plottitle('T2_echo= '+ str(int(1./p[3]))+'ns')
            norm_values_from_fit = values_from_fit
            norm_p = p
            norm_p_err = p_err

        else:
            ###### COMPUTE DIST (from raw data) #####      # CHANGED on 06/23/2021
            id_ref = np.argmin(amplitude)
            dist_a = np.sqrt(  (real_a -real_a[id_ref])**2 + (imag_a -imag_a[id_ref])**2  )

        if graph:
            plot2d_1.replace_inline_data(T_vec*1e9, amplitude)
            plot2d_2.replace_inline_data(T_vec*1e9, phase)
            plot2d_3.replace_inline_data(T_vec*1e9, real_a)
            plot2d_4.replace_inline_data(T_vec*1e9, imag_a)
            plot2d_5.replace_inline_data(T_vec*1e9, dist_a)
            plot2d_6.replace_inline_data(T_vec*1e9, norm_a)

    # finally:
    if Pulsing_instrument.get_board_flag():
        Pulsing_instrument.measurement_close(transfert_info=False)

    data_measurement.add_data_point(T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a)
    data_measurement.close_file()
    print Pulsing_instrument.measurement_close(transfert_info=True)
    Tabor.set_trigger_source('EVEN')

    if FIT:
        data_fit.add_data_point(1.0, 1./re_p[3],   re_p_err[3]/(re_p[3])**2 ) #re
        data_fit.add_data_point(2.0, 1./im_p[3],   im_p_err[3]/(im_p[3])**2 ) #im
        data_fit.add_data_point(3.0, 1./amp_p[3],  amp_p_err[3]/(amp_p[3])**2 ) #amp
        data_fit.add_data_point(4.0, 1./ph_p[3],   ph_p_err[3]/(ph_p[3])**2 ) #ph
        data_fit.add_data_point(5.0, 1./dist_p[3], dist_p_err[3]/(dist_p[3])**2 ) #Dist
        data_fit.add_data_point(6.0, 1./norm_p[3], norm_p_err[3]/(norm_p[3])**2 ) #Norm

        if graph:
            plot2d_1.add(T_vec*1e9, amp_values_from_fit)
            plot2d_2.add(T_vec*1e9, ph_values_from_fit)
            plot2d_3.add(T_vec*1e9, re_values_from_fit)
            plot2d_4.add(T_vec*1e9, im_values_from_fit)
            plot2d_5.add(T_vec*1e9, dist_values_from_fit)
            plot2d_6.add(T_vec*1e9, norm_values_from_fit)
        data_fit.close_file()

    if graph:
        plot2d_1.save_png()
        plot2d_2.save_png()
        plot2d_3.save_png()
        plot2d_4.save_png()
        plot2d_5.save_png()
        plot2d_6.save_png()

    qt.mend()
    all_smb_off()

    ## choosing the best fit (by the biggest amplitude of signal between re and im)
    print "amp of Re exp:", abs(round(re_p[1], 2)), ' [mV]'
    print "amp of Im exp:", abs(round(im_p[1], 2)), ' [mV]'
    print "amp of Dist exp:", abs(round(dist_p[1], 2)), '[mV]'
    print "amp of Norm exp:", abs(round(norm_p[1], 2)), '[mV]'

    best_p = dist_p
    best_p_err = dist_p_err

    print 'T2_echo=: ', int(1./best_p[3]), 'ns +-', int(best_p_err[3]/(best_p[3])**2), 'ns'

    print "\n"
    #####    What to return?    #####
    if Return_all_data and Return_extracted_values:
        result_list = [best_p[3], best_p_err[3]/(best_p[3])**2]
        data_list = [T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a]
        return (result_list, data_list)

    elif Return_extracted_values:
        result_list = [best_p[3], best_p_err[3]/(best_p[3])**2]
        return result_list

    elif Return_all_data:
        data_list = [T_vec*1e9, amplitude, phase, real_a, imag_a, dist_a, norm_a]
        return data_list

    else:
        return None


# def load_ssr_by_pickle(filepath, protokol=2):
def load_ssr_by_pickle(filepath):
    try:
        ## For all versions of Python (2., 3.)
        try:
            import cPickle as pickle
        except ModuleNotFoundError:
            import pickle
        protokol =  pickle.HIGHEST_PROTOCOL
        print "Pickle highest protokol:", protokol
        print "(and we use protokol = 2)"
    except:
        print "Warning! Can't import pickle. Probably it is not installed. It is used for save\load objects of ssr"

    # with open(filepath, 'wb') as output:
    #     pickle.dump(ssr, output, protokol)
    with open(filepath, 'rb') as input:
        ssr = pickle.load(input)
    return ssr

def do_traject_measure(parameters, n_of_files=5, t_read_us=50, averaging=2, with_pio2=False, pause=0, title='', do_get_fidelity_check=True, main_data_folder = 'F:\\Data\\', only_pi=False):
    '''
    New function to measure QNDness
    n_of_files - how many files to record. Each file can contain few trajectories.
    t_read_us - duration of trajectory in microseconds [us]
    averaging -  number of trajectories saved in a single data file (must be even number)
    with_pio2 - to do or not to do 3rd trajectory with pi/2 pulse before trajectory measurement
    pause - [seconds]  just a pause between each couple of trajectories to cooldown the system. Can be None.
    do_get_fidelity_check - to do or not to do get_fidelity measurement before and after trajectory (to check that setup is stable and data is consistant)
    '''

    ## checking averaging value: EVEN INTEGER
    averaging = int(averaging)
    if averaging % 2 != 0:
        averaging +=1
        print("averaging changed to ", averaging, "because it must be an even number")

    if do_get_fidelity_check:
        SSR_fid = get_fidelity(parameters)

    start_time1 = datetime.datetime.now()
    print ' started at:', start_time1, '\n'

    ###   adress of files   ###
    QND_folder = main_data_folder +take_dt_str(date=True, time=True, slash=True)+'___QNDness_meas_'+'dur='+str(t_read_us)+'us_Ntrj='+str(averaging*n_of_files)+title+'\\'
    print 'folder_adress:  ', QND_folder

    ####   parameters   ###
    try:
        freq_cav = parameters.freq_read
        power1 = parameters.power1
        power2 = parameters.power2
        t2 = parameters.tpi
        nsigma = parameters.nsigma
    except:
        print 'WARNING: (Fidelity) one of parameters is not defined!'

    t_read = 1e-6*t_read_us ### convert t_read to seconds ###
    t1 = t_read #from function argument
    t1_1 = 0e-9     #?for first readout in measurment (g)
    t1_2 = t1       #?for second readout in measurment (g or e)
    delta_t = 200.
    t1_1start = 0.1e-6
    t_between = 300e-9
    t2_start = t1_1start + t1_1 + t_between
    t1_2start = t2_start + t2
    t_protect = 0.
    delay_initial = 100.
    # acq_time = 2600.
    acq_time = (t1_1start+t1)*1e9+200
    print 'acq_time', acq_time
    delta_m1_start = 0.1e-6
    trigger_time = 300 + t1*1e9/10.

    trigger_delay_init = ats9360.get_trigger_delay()
    ats9360.set_trigger_delay(delay_initial)

    ###########################################################
    #
    #
    #               Experiment
    #
    #
    ###########################################################

    qt.mstart()
    start_time1 = datetime.datetime.now()

    num_seria = 2 #for label

    if only_pi == False:
        list_type_trj = ['no', 'pi']
    else:
        list_type_trj = ['pi']

    trigger_delay_list = [delay_initial + (t1_1+t_between+t2)*1e9, delay_initial + (t1_1+t_between+t2)*1e9]
    if with_pio2:
        num_seria += 1
        list_type_trj += ['pio2']
        trigger_delay_list += [delay_initial + (t1_1+t_between+t2/2.)*1e9]


    num = 0
    for type_trj, trigger_delay in zip(list_type_trj, trigger_delay_list):
        Tabor.set_trigger_source('EVEN')
        Pulsing_instrument.set_trigger_time(trigger_time)
        Pulsing_instrument.write_IQ_alwayspi_several_RO(t2, t1_1, t1_2, t2_start=t2_start ,
                t1_1start=t1_1start, t1_2start=t1_2start, delta_m1_start=delta_m1_start, delete=False, nsigma=nsigma)
        ats9360.set_acquisition_time(acq_time)
        ats9360.set_trigger_delay(trigger_delay)
        board_flag = None

        num += 1
        indx_file = 0
        for traj_n in range(n_of_files):
            print '{}/{} type {} pulse. Traj N: {} over {}'.format(num, num_seria, type_trj, traj_n, n_of_files-1)

            try:
                # smb_cavity_on()
                all_smb_on()
                time_meas_start = datetime.datetime.now()
                Pulsing_instrument.prep_timing(freq_cav, averaging, power1, average_type='test')
                qt.msleep(2)

                if type_trj != 'no':
                    Tabor.set_ch4_output('ON')
                    amplitude2 = 10**((power2)/10.)
                    Tabor.set_ch4_amplitude(2*amplitude2)

                board_flag = True
                Tabor.set_trigger_source('TIM')
                while ats9360.get_completed_acquisition() != 100.:
                    result = ats9360.measurement()
                    (I, Q) = result
                    qt.msleep(0.1)

                t_vec = np.arange(len(I[0,:]))/ats9360.get_samplerate()*1e3

                Tabor.set_trigger_source('EVEN')
                ats9360.measurement_close(transfert_info=False)
                board_flag = False
                time_meas_stop = datetime.datetime.now()

            except:
                print("\n\n   ERROR DURING TRJECTORY MEASURE "+title+"  \n\n")

            finally:
                if board_flag:
                    ats9360.measurement_close(transfert_info=False)
                print ats9360.measurement_close(transfert_info=True)

                # data = (t_vec, I, Q, type_trj, traj_n)

                # smb_cavity_off(pause=pause)
                if pause > 0:
                    all_smb_off(pause=pause)


                ### We save file here ###
                flag_file = False
                if indx_file == n_of_files-1:
                    flag_file = True
                sys.stdout.write('\n')
                start_saving = datetime.datetime.now()
                # for t_vec, I, Q, type_trj, traj_n in listData:
                sys.stdout.write('\rSaving of type {} pulse, traject number {}'.format(type_trj, traj_n))
                traj_name_file = 'traj_{}_{}_{}'.format(type_trj, traj_n, take_dt_str(time=True, date=False, slash=False))
                data_measurement = qt.Data(name='Projected_trajectories')
                # data_measurement.add_coordinate('time ',         units = 'ns')  ## V 20210618 no point to save time if it's linear with 1ns step always  ##economy 1/3 of memory!
                data_measurement.add_value('I_{}(t) '.format(type_trj),         units = 'Volt')
                data_measurement.add_value('Q_{}(t) '.format(type_trj),         units = 'Volt')
                data_measurement.add_comment('Tvec is from ' +str(t_vec[0]) +'ns to ' +str(t_vec[-1]) +'ns with step ' +str(t_vec[1]-t_vec[0])+'ns' )
                data_measurement.create_file(filepath=QND_folder+'Data\\'+ traj_name_file+'.dat', logging_file=flag_file, settings_file=flag_file)
                for i in np.arange(len(I[:,0])):
                    # data_measurement.add_data_point(t_vec, I[i,:], Q[i,:])
                    data_measurement.add_data_point(I[i,:], Q[i,:]) ## V 20210618 no point to save time if it's linear with 1ns step always  ##economy 1/3 of memory!
                    data_measurement.new_block()
                data_measurement.close_file()
                indx_file += 1
                stop_saving = datetime.datetime.now()
                print '\ntime of measurement', time_meas_stop - time_meas_start, '\n'
                print 'time of saving', stop_saving - start_saving


                gc.collect()
            ########################################

        gc.collect()

    sys.stdout.write('\n')
    ats9360.set_trigger_delay(trigger_delay_init)
    ###########################################################
    #
    #
    #               PROCESSING THE DATA
    #
    #
    ###########################################################
    gc.collect()

    # smb_cavity_on()
    all_smb_on()

    if do_get_fidelity_check:
        SSR_fid = get_fidelity(parameters)

    stop_time1 = datetime.datetime.now()
    print '\n finished at:', stop_time1, '\n'
    print '\n Total time :', stop_time1 - start_time1, '\n'
    return True

def do_traj_vs_rudat(parameters, rdt_vector, n_of_files=100, t_read_us=1000, with_pio2=True, pause=1.0):
    initial_rudat = param0.rudat
    for rdt in rdt_vector:
        param0.set_rudat(rdt)
        do_traject_measure(parameters, n_of_files=n_of_files, t_read_us=t_read_us, averaging=2, with_pio2=with_pio2, pause=pause, title='_rdt='+str(rdt))
    param0.set_rudat(initial_rudat)
    return


###########################################################
#
#               SEARCHING FUNCTIONS
#
###########################################################
def set_spectr(param, polmin=6.8, polmax=7.1, graph=True, averaging=1e3):
    if COMMENTS:
        print 'onetone spectroscopy...'
    cav = get_onetone_fread(f_min_cav=polmin, f_max_cav=polmax,
                            averaging=averaging, graph=graph)
    if cav is None:
        print 'warning: set_spectr(): Onetone cannot find peak!'
        return None
    cav = get_onetone_fread(f_min_cav= cav-0.2, f_max_cav= cav+0.2,
                            graph=graph, averaging = averaging)
    if cav is None:
        print 'warning: set_spectr(): Onetone cannot find peak!'
        return None
    param.freq_read = round(cav,4)

    qub = None
    if COMMENTS:
        print 'twotone spectroscopy...'
    qub = get_twotone_fqub(param.freq_read, averaging=2*averaging, graph=graph)
    if qub is None:
        print 'warning: set_spectr(): Twotone cannot find peak!'
        return False
    param.freq_q = round(qub,4)

    return True

def set_prec_freq_read(param, graph=True, averaging=1.5e3):
    '''
    set to given param object precise readout_pulse
    use get_dblob() for do it
    needs a calibrated pi-pulse
    '''
    # set freq of readout
    f_read = get_dblob(param, nop=200, averaging = averaging, graph=graph)
    if f_read is not None:
        param.freq_read = np.round(f_read,5)
        return True

    return False

#need tests
def set_prec_freq_q(param, graph=True, averaging=2e3):
        '''
        set to given param object precise qubit tone frequency
        uses get_ramsey_df() for do it
        needs a calibrated pi-pulse
        '''
        df_1 = abs(get_ramsey_df(param, graph=graph, averaging=averaging, window=4000))
        if df_1 is None:
            return False

        #if qub_tone is already good enough
        if df_1 < 0.1e-3:
            return True

        param.freq_q = param.freq_q + df_1

        df_2 = abs(get_ramsey_df(param, graph=graph, averaging=averaging, window=4000, tl=0))
        if df_2 is None:
            return False

        #if qub_tone is already good enough
        if df_2 < 0.1e-3:
            return True

        if df_2 > df_1: #if + is wrong direction
            param.freq_q = param.freq_q - df_2
            df_2 = abs(get_ramsey_df(param, graph=graph, averaging=averaging, window=4000, tl=0))
            return True
        else:
            print 'Something go wrong. Ramsey! Calibrate it by yourself'
            return False

        return False

# Need a test
def find_sweetspot(cur_start, cur_stop, cur_step, fq_min=6.0, fq_max=6.35, freq_read=None, averaging=1e3):
    '''
    returns [sweet_cur, freq_q, freq_read]
    make twotone vs current in given range
    takes freq_read for probe, if not - find it everytime
    fq_min, fq_max - frequency of qubit range
    '''
    if (abs(cur_start) > 100e-3) or (abs(cur_start) > 100e-3) or (abs(cur_start) > 100e-3):
        print 'W@rning! __too big current'
        return None

    curs = []
    freqs_q = []
    freqs_r = []

    if COMMENTS:
        print 'start twotone vs flux'

    tl_flag = 1
    for i in np.arange(cur_start,cur_stop,cur_step):

        # Cur_qub.set_current(i)
        set_qub_cur(i)
        qt.msleep(0.5)
        curs.append(i)
        if COMMENTS:
            print '___current: ', i

        if freq_read is not None:
            fr = freq_read
            fq = get_twotone_fqub(freq_read, tl = tl_flag, f_min=fq_min, f_max=fq_max, averaging=averaging)
        else:
            fr = get_onetone_fread()
            if fr is not None:
                freqs_r.append(fr)
                fq = get_twotone_fqub(freq_read, tl = tl_flag, f_min=fq_min, f_max=fq_max, averaging=averaging)
            else:
                freqs_r.append(0)
                freqs_q.sppend(0)
        tl_flag = 0

    index = np.argmax(freqs_q)
    sweet_cur = curs[index]
    freq_q_sweet = freqs_q[index]
    freq_read_sweet = freqs_r[index]

    if COMMENTS:
        print 'max freq is:', np.max(freqs_q)
        print 'on sweet current:', sweet_cur

    return [sweet_cur, freq_q_sweet, freq_read_sweet]

def find_pwr2(parameters, tpi_wanted, precision = 1, max_iteration = 5, averaging=2e3, tl=1, graph = False, pwr2=None, tpi=None, window=400):
    '''
    looking for power2 ==x corresponded to T-pi = tpi_wanted ==y
    using Secant method. returns power2.
    tpi_wanted in seconds, inside transforms to nanoseconds and back
    precision in percent
    return power2
    '''
    #precision given in nanoseconds - convering to nanoseconds
    # precision_sec = precision*1e-9
    precision_percent = precision*1e-2

    if precision<0 or precision>50:
        print 'precision should be in [0,50]'
        return None
    if (tpi_wanted < 10*1e-9) or (tpi_wanted > 100*1e-9):
        print 'tpi is not in range 10-100ns'
        return None
    if tpi is not None:
        if (tpi < 10*1e-9) or (tpi > 100*1e-9):
            print 'tpi is not in range 10-100ns'
            return None
    if parameters.power2 > 0:
        parameters.power2 = -0.0
        print 'power2 had wrong sign. Changed to -0.0'

    #y1,y2,y3 in nanoseconds inside the function!
    if (pwr2 is not None) and (tpi is not None):
        x1 = pwr2
        y1 = tpi
    else:
        x1 = parameters.power2
        if COMMENTS:
            print 'power2:',x1,'start Rabi...'
        y1 = get_rabi_pi(parameters, x1, averaging = averaging, tl = tl,
                    graph=graph, window=window)
        if y1 is None:
            return None
    if COMMENTS:
        print 'x1=',x1,'y1=',y1

    #check if it is already successful
    if (  (math.fabs(tpi_wanted-y1)/tpi_wanted) < precision_percent  ):
        print '__found power2: ', x1
        return x1

    x2 = parameters.power2*1.1 - 0.3
    if COMMENTS:
        print 'power2:',x2,'start Rabi...'
    y2 = get_rabi_pi(parameters, x2, averaging = averaging, tl=0,
                    graph=graph, window=window)
    if y2 is None:
        return None
    if COMMENTS:
        print 'x2=',x2,'y2=',y2

    #check if it is already successful
    if (  (math.fabs(tpi_wanted-y2)/tpi_wanted) < precision_percent  ):
        print '__found power2: ', x2
        return x2

    for i in range(max_iteration):
        x3 = (x2-x1)/(y2-y1)*(tpi_wanted-y1)+x1
        if COMMENTS:
            print 'try power2=', x3, '...'
            print 'itteration: ', i
        last = False
        if x3 < -10:
            print 'WARNING: rabi power2 more than -10. Bad regime'
            last = True
            x3 = -10.0
        elif x3 >0:
            print 'WARNING: rabi power2 less than 0. Bad regime'
            last = True
            x3 = -0.0
        if COMMENTS:
            print 'power2:', x3

        y3 = get_rabi_pi(parameters, x3, tl=0, averaging=1.62*averaging,
                        graph=graph, window=window)
        if y3 is None:
            return None
        if COMMENTS:
            print  'Fnd_pwr: iter:', i, ' x3=', x3, ' tpi=', y3

        #if (math.fabs(tpi_wanted-y3) < precision_sec) and (math.fabs(tpi_wanted-y2)):

        if (  (math.fabs(tpi_wanted-y3)/tpi_wanted) < precision_percent  ):
            print '__found power2: ', x3
            return x3
        x1 = x2
        x2 = x3
        y1 = y2
        y2 = y3
        if last == True:
            print 'value on the edge returned'
            return x3

    print  'Warning! [power2,Tpi] is not precise enough! \n', 'power2=',x3,'tpi=',y3
    return x3

def get_closest_tpi(params, graph = False, averaging = 2e3, onlyBigger=True, onlyEven=True):
    '''
    Function check tpi on given pwr2 and find closest even tpi
    With returned tpi one could run find_pwr2(param, tpi) to find pwr2
    Use function 'closest_even()'
    Improve: if closest even too small for achive?
    returns [tpi_wanted, tpi_raw]
    '''

    print 'Searching for closest tpi'

    tpi_raw = get_rabi_pi(params, params.power2, graph=graph, averaging = averaging)
    if tpi_raw is None:
        return None

    if COMMENTS:
        print 'tpi_raw is',tpi_raw

    if onlyEven:
        tpi_wanted = 1e-9*round(closest_even(tpi_raw*1e9))
    else:
        tpi_wanted = 1e-9*round(tpi_raw*1e9)

    if onlyBigger:  #only bigger than raw used for not go out of range during 'find_pwr2()'
        if tpi_wanted < tpi_raw:
            tpi_wanted = tpi_wanted + 2e-9

    if COMMENTS:
        print 'after closest_even()', tpi_wanted
    return [tpi_wanted, tpi_raw]

def set_tpi(params, wanted_tpi, precision=1, graph = False, averaging = 2e3, raw_tpi=None, pwr2=None, window=400):
    '''
    just run find_pwr2 and set tpi and pwr2 values
    Enter param-object, wanted tpi in sec, precision in %

    '''
    pwr2 = find_pwr2(params, wanted_tpi, graph=graph, tpi = raw_tpi, pwr2 = pwr2,
                        averaging = averaging, precision = precision, tl=0, window=window) #precision in %
    params.tpi = wanted_tpi
    params.power2 = pwr2
    return True

def set_closest_tpi(params, pwr2=-0.1, graph=False, averaging=2e3, onlyBigger=True, onlyEven=True, precision=1):
    '''
    1) Find closest tpi, save data_parameters
    2) run find_pwr2() with this parameters
    '''
    closest_tpi = get_closest_tpi(params, graph = graph, averaging = averaging,
                                    onlyBigger=onlyBigger, onlyEven=onlyEven)
    if closest_tpi is None:
        print '__________bad rabi!'
        return None
    qt.msleep(0.5)
    wanted_tpi = closest_tpi[0]
    raw_tpi = closest_tpi[1]
    print 'wanted tpi is: ', wanted_tpi #must be in seconds
    pwr2 = find_pwr2(params, wanted_tpi, graph=graph, tpi = raw_tpi, pwr2 = pwr2,
                        averaging = averaging, precision = precision, tl=0) #precision in %
    print 'param set:'
    print 'tpi = ', wanted_tpi
    print 'pwr2= ', pwr2
    params.tpi = wanted_tpi
    params.power2 = pwr2
    return True

def find_best_fid_vs_tread(param, nb_max_iter=3, av=4, counts=0.5e4, DOWEIGHT=False, nbins=200):
    '''
    This would be smarter to do iterative. Maybe even using scypy.optimizer right inside (but with added limits of course)
    Or at least by Newton linear approximations
    '''
    tread_vec = np.array([30, 100, 200, 500, 1000])*1e-9
    tread_init = param.t_read
    # smb_cavity_on()
    all_smb_on()

    nb_iter = 1
    fid_list = []
    for tread in tread_vec:
        param.t_read = tread
        SSR = get_fidelity(param, av=av, counts=counts, DOWEIGHT=DOWEIGHT, nbins=nbins, title='_______find_best_iter{}'.format(nb_iter), switch_off_smb_after=False)
        fid_list.append(SSR.dict_fidelity['F'])

    ind_max_fid = np.argmax(fid_list)
    max_fid = fid_list[ind_max_fid]
    tread_max_fid = tread_vec[ind_max_fid]
    print 'iter={} ---- fid list : {}'.format(nb_iter, fid_list)
    print 'max_fid={} ---- max_tread={}'.format(max_fid, tread_max_fid)

    nb_iter = 2
    while nb_iter <= nb_max_iter:
        tread_vec = np.array([0.75, 0.85, 0.95, 1.05, 1.15, 1.25])*tread_max_fid

        fid_list = []
        for tread in tread_vec:
            param.t_read = tread
            SSR = get_fidelity(param, av=av, counts=counts, DOWEIGHT=DOWEIGHT, nbins=nbins, title='_find_best_iter{}'.format(nb_iter))
            fid_list.append(SSR.dict_fidelity['F'])

        tread_vec = tread_vec.tolist()
        tread_vec.append(tread_max_fid)
        fid_list.append(max_fid)

        ind_max_fid = np.argmax(fid_list)
        max_fid = fid_list[ind_max_fid]
        #if we did not find a better tread than before
        if tread_max_fid == tread_vec[ind_max_fid]:
            # smb_cavity_off()
            all_smb_off()
            param.t_read = tread_init
            print 'return {}'.format(tread_max_fid)
            return tread_max_fid

        tread_max_fid = tread_vec[ind_max_fid]
        print 'iter={} ---- fid list : {}'.format(nb_iter, fid_list)
        print 'max_fid={} ---- max_tread={}'.format(max_fid, tread_max_fid)
        nb_iter += 1


    # smb_cavity_off()
    all_smb_off()
    param.t_read = tread_init
    print 'return {}'.format(tread_max_fid)
    return tread_max_fid


###########################################################
#
#               INVESTIGATE FUNCTIONS
#
###########################################################
##############___FIDELITY___#################
def fid_vs_tpi(param, tpi_vector=np.arange(0e-9,200e-9, 50e-9)):
    init_tpi = param.tpi

    data_measurement = qt.Data(name='____Fidelity_vs_tpi(not_calib)')
    data_measurement.add_coordinate('Excitation time [ns]', units = 'ns')
    data_measurement.add_value('F [%]'  ,         units = '%')
    data_measurement.add_value('F_post [%]',         units = '%')
    data_measurement.create_file()
    plot2d_1 = qt.Plot2D(data_measurement,
                      name      = 'F_',
                      coorddim  = 0,
                      valdim    = 1)
    plot2d_2 = qt.Plot2D(data_measurement,
                      name      = 'F_post_vs_tpi',
                      coorddim  = 0,
                      valdim    = 2)

    ssr_list = []
    for tpi in tpi_vector:
        param0.tpi = tpi
        ssr = get_fidelity(param0, title='vary_tpi='+str(int(1e9*param.tpi))+'ns', switch_off_smb_after=False )

        ssr_list.append(ssr)
        F       = ssr.dict_fidelity["F"]
        F_post  = ssr.dict_fidelity["F_post"]
        data_measurement.add_data_point( 1e9*tpi,  100*F,  100*F_post )

    param0.tpi = init_tpi
    all_smb_off()
    plot2d_1.save_png()
    plot2d_2.save_png()
    data_measurement.close_file()
    return ssr_list

def fid_vs_power2(param, power2_vector=np.arange(-0.0, -1.0, -0.1), tl=1):
    init_power2 = param.power2

    data_measurement = qt.Data(name='____Fidelity_vs_power2')
    data_measurement.add_coordinate('Excitation Amplitude modulator [V]', units = 'V')
    data_measurement.add_value('F [%]'  ,         units = '%')
    data_measurement.add_value('F_post [%]',         units = '%')
    data_measurement.create_file()

    plot2d_1 = qt.Plot2D(data_measurement,
                      name      = 'F_vs_power2',
                      coorddim  = 0,
                      valdim    = 1)
    plot2d_2 = qt.Plot2D(data_measurement,
                      name      = 'F_post_vs_power2',
                      coorddim  = 0,
                      valdim    = 2)

    ssr_list = []

    for power2 in power2_vector:
        param0.power2 = power2
        ssr = get_fidelity(param0, title='vary_power='+str(round(power2, 3))+'V', tl=tl, switch_off_smb_after=False )
        tl = 0

        ssr_list.append(ssr)
        F       = ssr.dict_fidelity["F"]
        F_post  = ssr.dict_fidelity["F_post"]
        data_measurement.add_data_point( power2,  F,  F_post )

    param0.power2 = init_power2
    plot2d_1.save_png()
    plot2d_2.save_png()
    all_smb_off()
    data_measurement.close_file()

    return ssr_list

def fid_vs_nsigma(param,nsigma,tpi=32e-9):
    '''
    return fidelity data_parameters
    with given nsigma(gaussian form of pi-pulse)
    and time of pi-pulse (32ns by default)
    '''
    if nsigma < 0:
        print 'error fid_vs_nsigma: nsigma < 0!'
        return False
    if nsigma > 5:
        print 'warning fid_vs_nsigma: nsigma>5'
        return False
    #tpi = param.tpi
    param.nsigma = nsigma

    pwr = find_pwr2(param, tpi)
    param.power2 = pwr
    real_tpi = get_rabi_pi(param, param.power2)
    fid = get_fidelity(param, switch_off_smb_after=False)

    res = [pwr, real_tpi, nsigma, fid]
    return res

def fid_vs_AWG_Offset(param, awg_offset_v, tl=1):
    '''
    Vary AWG offset. Measure get_fidelity()
    Plot F and F_post vs awg offset
    '''
    data_measurement = qt.Data(name='____Fidelity_vs_AWG_OFFSET')
    data_measurement.add_coordinate('AWG_OFFSET', units = 'V')
    data_measurement.add_value('F [%]'  ,         units = '%')
    data_measurement.add_value('F_post [%]',         units = '%')
    data_measurement.create_file()

    plot2d_1 = qt.Plot2D(data_measurement,
                      name      = 'F__vs_awg_offset',
                      coorddim  = 0,
                      valdim    = 1)
    plot2d_2 = qt.Plot2D(data_measurement,
                      name      = 'F_post_vs_awg_offset',
                      coorddim  = 0,
                      valdim    = 2)

    ssr_list = []
    for awg_off in awg_offset_v:
        ssr = get_fidelity(param, awg_offset=awg_off, switch_off_smb_after=False)
        # tl=0 # probably not possible

        ssr_list.append(ssr)
        F       = ssr.dict_fidelity["F"]
        F_post  = ssr.dict_fidelity["F_post"]
        data_measurement.add_data_point( awg_off,  100*F,  100*F_post )

    plot2d_1.save_png()
    plot2d_2.save_png()
    data_measurement.close_file()
    return ssr_list



###___fidelity_vs_timeOfReadPulse___###
def fid_vs_tread(param, tt_start=50e-9, tt_stop=510e-9, tt_step=50e-9, av=4, counts=5e3, t_vector=None, graph=False,  DOWEIGHT = False,  relax=False, label=''):
    '''
    Function for make measurments of fidelity (using or not weight functions)
    versus time of readout pulses
    Plot the graph of error f_ro, f_gauss and f_e, f_g
    Saves fidelity-data in folder 'Fidelity_vs_time'
    '''
    if t_vector is None:
        t_vector = np.arange(tt_start, tt_stop, tt_step)
    else:
        if (tt_start < 1e-9) or (tt_step < 1e-9) or (tt_stop < 1e-9):
            print '__!_fid_vs_tread:too small time value: shold be at least 1e-9'
            return False
        if (tt_stop > 1e-3) or (tt_step > 1e-3):
            print 'Error: fid_vs_tread: t_read should bi in sec'
            return False

    start_time = datetime.datetime.now()
    print '_______started at:', start_time, '\n'

    rdt_str = str( param.rudat )
    data_fidelity_time = qt.Data(name='______Fidelity_vs_time_rdt='+rdt_str+str(label))
    data_fidelity_time.add_coordinate('time ',         units = 'ns')
    data_fidelity_time.add_value('F_ro',         units = '')
    data_fidelity_time.add_value('F_g',         units = '')
    data_fidelity_time.add_value('F_e',         units = '')
    data_fidelity_time.add_value('F_post',         units = '')
    data_fidelity_time.add_value('F_post_g',         units = '')
    data_fidelity_time.add_value('F_post_e',         units = '')
    data_fidelity_time.add_value('F_gaus',         units = '')
    data_fidelity_time.add_value('F_gaus_eg',         units = '')
    data_fidelity_time.add_value('F_gaus_ge',         units = '')
    data_fidelity_time.add_value('Err_e',         units = '')
    data_fidelity_time.add_value('Err_g',         units = '')
    data_fidelity_time.create_file()

    plot2d_fid_post = qt.Plot2D(data_fidelity_time,
                      name      = 'fidelity vs t_read ',
                      coorddim  = 0,
                      valdim    = 4)

    T1_before = 0
    T1_after = 0
    previons_t_read = param.t_read
    if relax:
        T1_before = get_relax_time(param)
        print 'T1 before=', T1_before*1e6, 'us'


    tt = []
    ff = []
    e_ro = []
    e_g = []
    e_e = []
    e_gaus = []
    for i in t_vector:
        qt.msleep(0.2)
        i = round(1e9*i)*1e-9
        print('___t_read=', i)
        qt.msleep(1)
        try:
            print 'im ok 1'
            qt.msleep(0.4)
            param.t_read = i
            ssr = get_fidelity(param, counts=counts, av=av, DOWEIGHT=DOWEIGHT,  title='t_read= '+str(int(i*1e9)), switch_off_smb_after=False )
            qt.msleep(0.4)
            fid = ssr.dict_fidelity
            fid_post = fid['F_post']
        except:
            print '_______Error was at t_read=', param.t_read, 'ns'
            fid_post = 0
        print 't_read:', i, 'fid_post:', fid_post
        tt.append(i)
        ff.append(fid_post)
        data_fidelity_time.add_data_point(i, fid['F'], fid['F_g'], fid['F_e'], fid['F_post'],
            fid['F_post_g'], fid['F_post_e'], fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'], fid['Err_e'], fid['Err_g'])
        plot2d_fid_post.replace_inline_data(t_vector*1e9, ff)

    qt.msleep(0.1)
    data_fidelity_time.close_file()
    plot2d_fid_post.save_png()
    qt.msleep(0.1)
    param.t_read = previons_t_read

    if relax:
        T1_after = 0
        T1_after = get_relax_time(param)
        print 'T1 before=', T1_before*1e6, 'us'
        print 'T1 after=', T1_after*1e6, 'us'
        print 'T1 difference', (T1_before - T1_after)*1e6, 'us'

    stop_time = datetime.datetime.now()
    print '\n _______finished at:', stop_time,'\n','       time:', stop_time - start_time

    if graph:
        try:
            plt.figure()
            plt.plot(tt, e_ro_post, '.', color='b', label='error_postselected')
            plt.plot(tt, e_g_post, '.', color='r', label='error_excited')
            plt.plot(tt, e_e_post, '.', color='g', label='error_ground')
            plt.plot(tt, e_gaus, '.', color='k', label='gaussian overlap')

            theory_relax1 = []
            theory_relax2 = []
            theory_time = []
            if relax:
                try:
                    for i in np.arange(tt_start, tt_stop, tt_step/10):
                        theory_time.append(i)
                        theory_relax1.append( 1-np.exp(-i/T1_before) )
                        theory_relax2.append( 1-np.exp(-i/T1_after) )
                    plt.plot(theory_time, theory_relax1, color='y', label='relaxation, t1='+str(round(1e6*T1_before))+'us' )
                    plt.plot(theory_time, theory_relax2, color='orange', label='relaxation, t1='+str(round(1e6*T1_after))+'us')
                except:
                    print 'error during plotting relaxation'

            plt.grid()
            plt.yscale('log')
            plt.xlabel('time, sec')
            plt.legend(loc='best')
            plt.title(param.get_string())
            print 'graph was plotted'
            print 'problem of lenght!!!!'
            print 'tt_____________=', len(tt)
            print 'e_ro=___________',len(e_ro)
            plt.figure()
            plt.plot(tt, e_ro, '.', color='b', label='error_postselected')
            plt.plot(tt, e_g, '.', color='r', label='error_excited')
            plt.plot(tt, e_e, '.', color='g', label='error_ground')
            plt.plot(tt, e_gaus, '.', color='k', label='gaussian overlap')

            theory_relax1 = []
            theory_relax2 = []
            theory_time = []
            if relax:
                try:
                    for i in np.arange(tt_start, tt_stop, tt_step/10):
                        theory_time.append(i)
                        theory_relax1.append( 1-np.exp(-i/T1_before) )
                        theory_relax2.append( 1-np.exp(-i/T1_after) )
                    plt.plot(theory_time, theory_relax1, color='y', label='relaxation, t1='+str(round(1e6*T1_before))+'us' )
                    plt.plot(theory_time, theory_relax2, color='orange', label='relaxation, t1='+str(round(1e6*T1_after))+'us')
                except:
                    print 'error during plotting relaxation'

            plt.grid()
            plt.yscale('log')
            plt.xlabel('time, sec')
            plt.legend(loc='best')
            plt.title(param.get_string())
            print 'graph was plotted'

            plt.show()

        except:
            'Error: fid_vs_tread: Cant plot graph'
        finally:
            return [tt, ff, T1_before, T1_after]

    return [tt, ff, T1_before, T1_after]

def fid_vs_rudat(param, rudat_v, av=2,counts=1e4, DOWEIGHT = False, title='', verify_optimal_freq_read=False):
    '''
    Function for make measurments of fidelity (using or not weight functions)
    versus time of readout pulses
    Plot the graph of error f_ro, f_gauss and f_e, f_g
    Saves fidelity-data in folder 'Fidelity_vs_time'
    '''
    start_time = datetime.datetime.now()
    print '_______started at:', start_time, '\n'

    tread_str = str( param.t_read*1e9 )
    data_fidelity_time = qt.Data(name='______Fid_vs_rudat_tread='+tread_str+title)
    data_fidelity_time.add_coordinate('rudat ',         units = 'dB')
    data_fidelity_time.add_value('F_ro',         units = '')
    data_fidelity_time.add_value('F_g',         units = '')
    data_fidelity_time.add_value('F_e',         units = '')
    data_fidelity_time.add_value('F_post',         units = '')
    data_fidelity_time.add_value('F_post_g',         units = '')
    data_fidelity_time.add_value('F_post_e',         units = '')
    data_fidelity_time.add_value('F_gaus',         units = '')
    data_fidelity_time.add_value('F_gaus_eg',         units = '')
    data_fidelity_time.add_value('F_gaus_ge',         units = '')
    data_fidelity_time.add_value('Err_e',         units = '')
    data_fidelity_time.add_value('Err_g',         units = '')
    data_fidelity_time.create_file()

    plot2d_fid_post = qt.Plot2D(data_fidelity_time,
                      name      = 'fidelity vs rudat ',
                      coorddim  = 0,
                      valdim    = 4)

    previons_rdt = param.rudat

    rr = []
    ff = []
    e_ro = []
    e_g = []
    e_e = []
    e_gaus = []
    tl = 1
    freq_read_init = param.freq_read ##(useful if verify_optimal_freq_read==True)
    for i in rudat_v:
        qt.msleep(0.2)
        print('___rudat=', i)
        qt.msleep(1)
        try:
            print 'im ok 1'
            param.set_rudat(i)
            qt.msleep(1.0)
            if verify_optimal_freq_read:
                param.freq_read = get_dblob(param0)
                tl = 1
            ssr = get_fidelity(param, tl=tl, counts=counts, av=av, DOWEIGHT=DOWEIGHT,  title='_rudat='+str(i)+title, switch_off_smb_after=False )
            qt.msleep(0.4)
            tl = 0
            fid = ssr.dict_fidelity
            fid_post = fid['F_post']
        except:
            print '_______Error was at t_read=', param.t_read, 'ns'
            fid_post = 0
        finally:
            param.freq_read = freq_read_init
        print 't_read:', i, 'fid_post:', fid_post
        rr.append(i)
        ff.append(fid_post)
        data_fidelity_time.add_data_point(i, fid['F'], fid['F_g'], fid['F_e'], fid['F_post'],
            fid['F_post_g'], fid['F_post_e'], fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'], fid['Err_e'], fid['Err_g'])
        plot2d_fid_post.replace_inline_data(rudat_v, ff)

    qt.msleep(0.1)
    data_fidelity_time.close_file()
    plot2d_fid_post.save_png()
    qt.msleep(0.1)
    param.set_rudat(previons_rdt)

    stop_time = datetime.datetime.now()
    print '\n _______finished at:', stop_time,'\n','       time:', stop_time - start_time

    gc.collect()

    return [rr, ff]

def fid_vs_freq_read(param, freq_vec, title='', tl=1):
    '''
    Function for make measurments of fidelity (using or not weight functions)
    versus time of readout pulses
    Plot the graph of error f_ro, f_gauss and f_e, f_g
    Saves fidelity-data in folder 'Fidelity_vs_time'
    '''
    start_time = datetime.datetime.now()
    print '_______started at:', start_time, '\n'

    data_fidelity_time = qt.Data(name='______Fidelity_vs_freq'+title)
    data_fidelity_time.add_coordinate('Freq_read [GHz]',         units = 'GHz')
    data_fidelity_time.add_value('F_ro',         units = '')
    data_fidelity_time.add_value('F_g',         units = '')
    data_fidelity_time.add_value('F_e',         units = '')
    data_fidelity_time.add_value('F_post',         units = '')
    data_fidelity_time.add_value('F_post_g',         units = '')
    data_fidelity_time.add_value('F_post_e',         units = '')
    data_fidelity_time.add_value('F_gaus',         units = '')
    data_fidelity_time.add_value('F_gaus_eg',         units = '')
    data_fidelity_time.add_value('F_gaus_ge',         units = '')
    data_fidelity_time.add_value('Err_e',         units = '')
    data_fidelity_time.add_value('Err_g',         units = '')
    data_fidelity_time.create_file()

    plot2d_fid_post = qt.Plot2D(data_fidelity_time,
                      name      = 'fidelity vs freq_read ',
                      coorddim  = 0,
                      valdim    = 4)

    previons_freq = param.freq_read

    rr = []
    ff = []
    e_ro = []
    e_g = []
    e_e = []
    e_gaus = []
    for i in freq_vec:
        qt.msleep(0.2)
        print('___freq=', i)
        qt.msleep(0.1)
        # try:
        print 'im ok 1'
        param.freq_read = i
        qt.msleep(0.1)
        str_freq = str( 1e-3*(int(i*1e3)) )
        ssr = get_fidelity(param, tl=tl, title='_fr_read= '+str_freq, switch_off_smb_after=False)
        tl = 0 #This is ok. No need of reloading tabor if frequency changed. I checked. (it has nothing to do with AWG) (Vladimir)
        qt.msleep(0.1)
        fid = ssr.dict_fidelity
        fid_post = fid['F_post']
        # except:
            # print '_______Error was at t_read=', param.t_read, 'ns'
            # fid_post = 0
        print 't_read:', i, 'fid_post:', fid_post
        rr.append(i)
        ff.append(fid_post)
        data_fidelity_time.add_data_point(i, fid['F'], fid['F_g'], fid['F_e'], fid['F_post'],
            fid['F_post_g'], fid['F_post_e'], fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'], fid['Err_e'], fid['Err_g'])
        plot2d_fid_post.replace_inline_data(freq_vec, ff)

    qt.msleep(0.1)
    data_fidelity_time.close_file()
    plot2d_fid_post.save_png()
    qt.msleep(0.1)
    param.freq_read = previons_freq

    stop_time = datetime.datetime.now()
    print '\n _______finished at:', stop_time,'\n','       time:', stop_time - start_time

    return [rr, ff]

def fid_vs_tbetween(param, tb_vector=np.arange(0.0e-9, 200e-9, 10e-9), av=4, counts=20e3, graph=False,  DOWEIGHT = False):
    '''
    Function for make measurments of fidelity (using or not weight functions)
    versus time of readout pulses
    Plot the graph of error f_ro, f_gauss and f_e, f_g
    Saves fidelity-data in folder 'Fidelity_vs_time'
    '''
    for t in tb_vector:
        if t > 10000e-9:
            print "tb_vector must be given in seconds! In range (0; 10000e-9 ) sec"
            return False
    ### To prevent reaching the limits of the Alazar
    # if tb_stop+2*param0.t_read > 5e-6:
    #     print 'tb_stop was too long and was set to 5us - 2*t_read'
    #     tt_stop = 5.e-6 - 2*param0.t_read
    # if tb_start < param.tpi:
    #     tb_start = param.tpi
    #     print 'tb_start was too low and was set to t_pi'
    # if tb_vector is None:
    #     tb_vector = np.arange(tb_start, tb_stop, tb_step)
    # else:
    #     if (tb_start < 1e-9) or (tb_step < 1e-9) or (tb_stop < 1e-9):
    #         print '__!_fid_vs_tbetween:too small time value: shold be at least 1e-9'
    #         return False
    #     if (tb_stop > 1e-3) or (tb_step > 1e-3):
    #         print 'Error: fid_vs_tread: t_between should be in sec'
    #         return False

    start_time = datetime.datetime.now()
    print '_______started at:', start_time, '\n'

    data_fidelity_time = qt.Data(name='______Fidelity_vs_tbetween')
    data_fidelity_time.add_coordinate('t_between ',         units = 'ns')
    data_fidelity_time.add_value('F_ro',         units = '')
    data_fidelity_time.add_value('F_g',         units = '')
    data_fidelity_time.add_value('F_e',         units = '')
    data_fidelity_time.add_value('F_post',         units = '')
    data_fidelity_time.add_value('F_post_g',         units = '')
    data_fidelity_time.add_value('F_post_e',         units = '')
    data_fidelity_time.add_value('F_gaus',         units = '')
    data_fidelity_time.add_value('F_gaus_eg',         units = '')
    data_fidelity_time.add_value('F_gaus_ge',         units = '')
    data_fidelity_time.add_value('Err_e',         units = '')
    data_fidelity_time.add_value('Err_g',         units = '')
    data_fidelity_time.create_file()

    plot2d_fid_post = qt.Plot2D(data_fidelity_time,
                      name      = 'fidelity vs t_between ',
                      coorddim  = 0,
                      valdim    = 4)

    previons_t_between = param.t_between

    tt = []
    ff = []
    e_ro = []
    e_g = []
    e_e = []
    e_gaus = []
    for i in tb_vector:
        qt.msleep(0.2)
        i = round(1e9*i)*1e-9
        print('___t_between=', i)
        qt.msleep(1)
        try:
            print 'im ok 1'
            qt.msleep(0.4)
            param.t_between = i
            ssr = get_fidelity(param, counts=counts, av=av, DOWEIGHT=DOWEIGHT,  title='t_read= '+str(int(i*1e9)), switch_off_smb_after=False)
            qt.msleep(0.4)
            fid = ssr.dict_fidelity
            fid_post = fid['F_post']
        except:
            print '_______Error was at t_between=', param.t_read, 'ns'
            fid_post = 0
        print 't_between:', i, 'fid_post:', fid_post
        tt.append(i)
        ff.append(fid_post)
        data_fidelity_time.add_data_point(i*1e9, fid['F'], fid['F_g'], fid['F_e'], fid['F_post'],
            fid['F_post_g'], fid['F_post_e'], fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'], fid['Err_e'], fid['Err_g'])
        plot2d_fid_post.replace_inline_data(tb_vector*1e9, ff)

    qt.msleep(0.1)
    data_fidelity_time.close_file()
    plot2d_fid_post.save_png()
    qt.msleep(0.1)
    param.t_between = previons_t_between

    stop_time = datetime.datetime.now()
    print '\n _______finished at:', stop_time,'\n','       time:', stop_time - start_time

    return [tt, ff]

def fid_vs_phase1(param, ph_start=0, ph_stop=30, ph_step=10, av=2,counts=1e4, ph_vector=None, graph=False,  DOWEIGHT = False):
    '''
    Function for make measurments of fidelity (using or not weight functions)
    versus time of readout pulses
    Plot the graph of error f_ro, f_gauss and f_e, f_g
    Saves fidelity-data in folder '______Fidelity_vs_phase1'
    '''
    if ph_vector is None:
        ph_vector = np.arange(ph_start, ph_stop, ph_step)

    start_time = datetime.datetime.now()
    print '_______started at:', start_time, '\n'

    data_fidelity_phase = qt.Data(name='______Fidelity_vs_phase1')
    data_fidelity_phase.add_coordinate('Phase1 ',         units = 'deg')
    data_fidelity_phase.add_value('F_ro',         units = '')
    data_fidelity_phase.add_value('F_g',         units = '')
    data_fidelity_phase.add_value('F_e',         units = '')
    data_fidelity_phase.add_value('F_post',         units = '')
    data_fidelity_phase.add_value('F_post_g',         units = '')
    data_fidelity_phase.add_value('F_post_e',         units = '')
    data_fidelity_phase.add_value('F_gaus',         units = '')
    data_fidelity_phase.add_value('F_gaus_eg',         units = '')
    data_fidelity_phase.add_value('F_gaus_ge',         units = '')
    data_fidelity_phase.add_value('Err_e',         units = '')
    data_fidelity_phase.add_value('Err_g',         units = '')
    data_fidelity_phase.create_file()

    previons_phase1 = param.phase1

    ph = []
    ff = []
    for i in ph_vector:
        print('___phase=', i)
        qt.msleep(1)
        # try:
        print 'im ok 1'
        qt.msleep(0.5)
        param.set_phase1(i)
        ssr = get_fidelity(param, counts=counts, av=av, DOWEIGHT=DOWEIGHT,  title= 'Phase='+str(int(i)), switch_off_smb_after=False )
        fid = ssr.dict_fidelity
        fid_post = fid['F_post']
        # except:
        #     print '_______Error was at phase=', param.phase1, 'ns'
        #     fid_post = 0
        print 'phase:', i, 'fid_post:', fid_post
        ph.append(i)
        ff.append(fid_post)
        data_fidelity_phase.add_data_point(i, fid['F'], fid['F_g'], fid['F_e'], fid['F_post'],
            fid['F_post_g'], fid['F_post_e'], fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'], fid['Err_e'], fid['Err_g'])

    data_fidelity_phase.close_file()
    param.set_phase1(previons_phase1)

    stop_time = datetime.datetime.now()
    print '\n _______finished at:', stop_time,'\n','       time:', stop_time - start_time

    if graph:
        plt.figure()
        plt.plot(ph, ff, '.', color='b', label='fid_postselected')
        plt.grid()
        plt.yscale('log')
        plt.xlabel('time, sec')
        plt.ylabel('Fidelity post')
        plt.legend(loc='best')
        plt.title(param.get_string())
        print 'graph was plotted'

    return [ph, ff]

def fid_vs_jpa_gain(v_vec):
    ssr_list = []
    flag_tl = 1
    for v in v_vec:
        Cur_jpa.set_channel('B')
        Cur_jpa.set_voltage(v)
        qt.msleep(1)
        ssr = get_fidelity(param0, tl=flag_tl, title='JPA_att_v='+str(round(v, 4)), switch_off_smb_after=False)
        flag_tl = 0
        ssr_list.append(ssr)

    return ssr_list

def fid_vs_rudat2(parameters, rudat2_vec, rabi_av=1e3,  rabi_graph=True, rabi_window=3000, rabi_nop=400.0, rabi_awg_offset=AWG_OFFSET,
        fid_av=4, fid_counts=5e3, fid_weightfunc=None, fid_DOWEIGHT=False, fid_nbins=200, fid_awg_offset=AWG_OFFSET, fid_title='', fid_t_pre=None):   # parameters for Rabi then parameters for single SingleShot
    '''
    Measures fidelity vs. rudat_2
    pi-pulse has to be re-calibrated every iteration with a Rabi measurement
    takes object of parameters class and rudat2 vector and all parameters for Rabit and Single Shot readout
    '''
    initial_rudat2 = parameters.rudat2
    initial_tpi = parameters.tpi


    start_time1 = datetime.datetime.now()
    print ' started at:', start_time1, '\n'

    data_measurement = qt.Data(name='______Fidelity_vs_rudatQ')
    data_measurement.add_coordinate('Rudat2 [dB]', units = 'dB')
    data_measurement.add_value('Tpi',       units = 's')
    data_measurement.add_value('Fidelity [%]',           units = '%')
    data_measurement.add_value('Fidelity_post [%]',           units = '%')
    data_measurement.create_file()

    plot2d_1 = qt.Plot2D(data_measurement,
                      name      = 'Fidelity vs RudatQ plot',
                      coorddim  = 0,
                      valdim    = 2)

    try:
        fid_arr = []    #np.zeros(( len(rudat2_vec) ))
        fid_post_arr = []   #np.zeros(( len(rudat2_vec) ))
        for i in range(len( rudat2_vec ) ):
            parameters.set_rudat2(rudat2_vec[i])
            new_tpi = get_rabi_pi(parameters, 0., tl = 1, averaging=rabi_av, nom_expect = 0, window = rabi_window, nop=rabi_nop, graph=rabi_graph, awg_offset=rabi_awg_offset, Return_tpi_only=True, Return_trabi=False)
            parameters.tpi = new_tpi
            ssr = get_fidelity(parameters,av=fid_av,counts=fid_counts, tl=1, weightfunc=fid_weightfunc, DOWEIGHT=fid_DOWEIGHT, nbins=fid_nbins, awg_offset=fid_awg_offset, title=fid_title, t_pre=fid_t_pre, switch_off_smb_after=False)
            fid = ssr.dict_fidelity['F']
            fid_post = ssr.dict_fidelity['F_post']
            fid_arr.append(fid)
            fid_post_arr.append(fid_post)
            data_measurement.add_data_point(rudat2_vec[i], new_tpi, fid, fid_post)
            # data_measurement.new_block()
            plot2d_1.replace_inline_data(rudat2_vec, fid_arr)

    finally:
        parameters.set_rudat2(initial_rudat2)
        parameters.tpi = initial_tpi
        plot2d_1.save_png()
        qt.mend()
        data_measurement.close_file()

    stop_time1 = datetime.datetime.now()
    print '\n finished at:', stop_time1,'\n','       time:',
    print 'time of measurement', stop_time1 - start_time1

    print( ' return [ rudat2_vec, fid_arr, fid_post_arr]' )
    return [ rudat2_vec, fid_arr, fid_post_arr]


def fid_vs_tread_and_rudat_on_optimal_freq_read(param, rudat_v, tread_v, ss_av=2, ss_counts=1e4, DOWEIGHT = False, title='', dblobs_span=0.1, dblobs_nop = 200, dblobs_av = 1e3, label=''):
    '''
    Function for make measurments of fidelity (using or not weight functions)
    versus time and attenuation of readout pulses
    Computes the best readout frequencies for each power value beforehand to optimize all 3 parameters at once
    '''
    start_time = datetime.datetime.now()
    print '_______started at:', start_time, '\n'

    data_fidelity_RO_params = qt.Data(name='______Fidelity_vs_readout_parameters'+label)
    # data_fidelity_RO_params.add_coordinate('timestamp',         units = 'time')
    data_fidelity_RO_params.add_coordinate('tread ',         units = 'ns')
    data_fidelity_RO_params.add_coordinate('rudat ',         units = 'ns')
    data_fidelity_RO_params.add_coordinate('fread ',         units = 'ns')
    data_fidelity_RO_params.add_value('F_ro',         units = '')
    data_fidelity_RO_params.add_value('F_g',         units = '')
    data_fidelity_RO_params.add_value('F_e',         units = '')
    data_fidelity_RO_params.add_value('F_post',         units = '')
    data_fidelity_RO_params.add_value('F_post_g',         units = '')
    data_fidelity_RO_params.add_value('F_post_e',         units = '')
    data_fidelity_RO_params.add_value('F_gaus',         units = '')
    data_fidelity_RO_params.add_value('F_gaus_eg',         units = '')
    data_fidelity_RO_params.add_value('F_gaus_ge',         units = '')
    data_fidelity_RO_params.add_value('Err_e',         units = '')
    data_fidelity_RO_params.add_value('Err_g',         units = '')
    data_fidelity_RO_params.create_file()

    plot3d_fid_post = qt.Plot3D(data_fidelity_RO_params,
                      name      = 'fidelity vs t_read, rudat ',
                      coorddim  = (0, 1),
                      valdim    = 6)

    ## save parameters we want to change
    previous_fread = param.freq_read
    previons_tread = param.t_read
    previous_rudat = param.rudat

    fread_v = []
    dblob_tl_flag = 1
    print "Mapping optimal frequency vs rudat"
    for rud in rudat_v:
        param.set_rudat(rud)
        fread_best = get_dblob(param, span=dblobs_span, av = dblobs_av, nop = dblobs_nop, tl=dblob_tl_flag, graph=True, all_data_return=False, comnt='rdt='+str(rud))
        dblob_tl_flag = 0
        fread_v.append(fread_best)

    print 'f_read optimized as a function of rudat for t_read = ', previons_tread

    # Measure fid while varying t_read and rudat (with optimized f_read)
    best_timestamp = 0.0
    best_F_post = 0.0
    for tt in tread_v:
        for i in range(len(rudat_v)):
            fread = fread_v[i]
            tt_ns = round(1e9*tt)*1e-9
            param.t_read = tt
            rud = rudat_v[i]
            param.set_rudat(rud)
            param.freq_read = fread
            print('___t_read=', tt_ns)

            try:
                qt.msleep(0.2)
                print 'Start Single-Shot measurement'
                title_str = 't_read= '+str(1e9*tt_ns)+', rudat= '+str(rud)+', f_read= '+str(round(fread, 3))
                ssr = get_fidelity(param, counts=ss_counts, av=ss_av, DOWEIGHT=DOWEIGHT,  title=title_str, switch_off_smb_after=False )
                qt.msleep(0.2)
                fid = ssr.dict_fidelity
                fid_post = fid['F_post']
                timestamp = take_dt_str(date=False,time=True, slash=False)
                del ssr
                gc.collect()
            except:
                print '_______Error was at '+title_str
                fid_post = 0

            print 'At ', title_str, ' -> fid_post= ', fid_post
            data_fidelity_RO_params.add_data_point( 1e9*tt_ns, rud, fread, fid['F'], fid['F_g'], fid['F_e'], fid['F_post'],
                fid['F_post_g'], fid['F_post_e'], fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'], fid['Err_e'], fid['Err_g'])
            if fid['F_post'] > best_F_post:
                best_F_post = fid['F_post']
                best_timestamp = timestamp

        ###################
        data_fidelity_RO_params.new_block()

    qt.msleep(0.1)
    data_fidelity_RO_params.close_file()
    plot3d_fid_post.save_png()
    qt.msleep(0.1)

    param.freq_read = previous_fread
    param.t_read = previons_tread

    stop_time = datetime.datetime.now()
    print '\n _______finished at:', stop_time,'\n','       time:', stop_time - start_time
    print "\n best result is ", round( 100*best_F_post, 3 ), "%"
    print "reached at ", best_timestamp, "\n\n"
    return [rudat_v, tread_v, fread_v, fid_post ]

def fid_vs_TRF(param, t_vec, r_vec, f_vec, ss_counts=10e3, ss_av=4, label=''):
    '''
    Vary three parameters of measurement.
    T - t_read
    R - rudat1
    F - freq_read
    Tabor is loading for only change of t_read, which economy quite a lot of time.
    '''
    start_time = datetime.datetime.now()
    print '_______started at:', start_time, '\n'

    ##########################
    if label != '':
        label = '_'+label

    data_fidelity_TRF_params = qt.Data(name='__(!)______Fidelity_vs_3D_param_T_R_F___'+label)
    data_fidelity_TRF_params.add_coordinate('T_read ',         units = 'ns')
    data_fidelity_TRF_params.add_coordinate('Rudat ',         units = 'dB')
    data_fidelity_TRF_params.add_coordinate('F_read ',         units = 'GHz')
    data_fidelity_TRF_params.add_value('F_ro',         units = '')
    data_fidelity_TRF_params.add_value('F_g',         units = '')
    data_fidelity_TRF_params.add_value('F_e',         units = '')
    data_fidelity_TRF_params.add_value('F_post',         units = '')
    data_fidelity_TRF_params.add_value('F_post_g',         units = '')
    data_fidelity_TRF_params.add_value('F_post_e',         units = '')
    data_fidelity_TRF_params.add_value('F_gaus',         units = '')
    data_fidelity_TRF_params.add_value('F_gaus_eg',         units = '')
    data_fidelity_TRF_params.add_value('F_gaus_ge',         units = '')
    data_fidelity_TRF_params.add_value('Err_e',         units = '')
    data_fidelity_TRF_params.add_value('Err_g',         units = '')
    data_fidelity_TRF_params.create_file()
    #
    # data_fidelity_TR = qt.Data(name='______Fidelity_vs_2D_param_T_R___'+label)
    # data_fidelity_TR.add_coordinate('T_read ',         units = 'ns')
    # data_fidelity_TR.add_coordinate('Rudat ',         units = 'dB')
    # data_fidelity_TR.add_value('F_ro',         units = '')
    # data_fidelity_TR.add_value('F_g',         units = '')
    # data_fidelity_TR.add_value('F_e',         units = '')
    # data_fidelity_TR.add_value('F_post',         units = '')
    # data_fidelity_TR.add_value('F_post_g',         units = '')
    # data_fidelity_TR.add_value('F_post_e',         units = '')
    # data_fidelity_TR.add_value('F_gaus',         units = '')
    # data_fidelity_TR.add_value('F_gaus_eg',         units = '')
    # data_fidelity_TR.add_value('F_gaus_ge',         units = '')
    # data_fidelity_TR.add_value('Err_e',         units = '')
    # data_fidelity_TR.add_value('Err_g',         units = '')
    # data_fidelity_TR.create_file()
    #
    # data_fidelity_RF = qt.Data(name='______Fidelity_vs_2D_param_R_F___'+label)
    # data_fidelity_RF.add_coordinate('Rudat ',         units = 'dB')
    # data_fidelity_RF.add_coordinate('F_read ',         units = 'GHz')
    # data_fidelity_RF.add_value('F_ro',         units = '')
    # data_fidelity_RF.add_value('F_g',         units = '')
    # data_fidelity_RF.add_value('F_e',         units = '')
    # data_fidelity_RF.add_value('F_post',         units = '')
    # data_fidelity_RF.add_value('F_post_g',         units = '')
    # data_fidelity_RF.add_value('F_post_e',         units = '')
    # data_fidelity_RF.add_value('F_gaus',         units = '')
    # data_fidelity_RF.add_value('F_gaus_eg',         units = '')
    # data_fidelity_RF.add_value('F_gaus_ge',         units = '')
    # data_fidelity_RF.add_value('Err_e',         units = '')
    # data_fidelity_RF.add_value('Err_g',         units = '')
    # data_fidelity_RF.create_file()
    #
    # data_fidelity_FT = qt.Data(name='______Fidelity_vs_2D_param_F_T___'+label)
    # data_fidelity_FT.add_coordinate('F_read ',         units = 'GHz')
    # data_fidelity_FT.add_coordinate('T_read ',         units = 'ns')
    # data_fidelity_FT.add_value('F_ro',         units = '')
    # data_fidelity_FT.add_value('F_g',         units = '')
    # data_fidelity_FT.add_value('F_e',         units = '')
    # data_fidelity_FT.add_value('F_post',         units = '')
    # data_fidelity_FT.add_value('F_post_g',         units = '')
    # data_fidelity_FT.add_value('F_post_e',         units = '')
    # data_fidelity_FT.add_value('F_gaus',         units = '')
    # data_fidelity_FT.add_value('F_gaus_eg',         units = '')
    # data_fidelity_FT.add_value('F_gaus_ge',         units = '')
    # data_fidelity_FT.add_value('Err_e',         units = '')
    # data_fidelity_FT.add_value('Err_g',         units = '')
    # data_fidelity_FT.create_file()

    # plot3d_Fp_TR = qt.Plot3D(data_fidelity_TR_params,
    #                   name      = 'fidelity vs t_read, rudat',
    #                   coorddim  = (0, 1),
    #                   valdim    = 5)
    # plot3d_Fp_RF = qt.Plot3D(data_fidelity_RF,
    #                   name      = 'fidelity vs rudat, freq_read',
    #                   coorddim  = (0, 1),
    #                   valdim    = 5)
    # plot3d_Fp_TF = qt.Plot3D(data_fidelity_FT,
    #                   name      = 'fidelity vs t_read, freq_read',
    #                   coorddim  = (0, 1),
    #                   valdim    = 5)
    ##########################

    previous_fread = param.freq_read
    previons_tread = param.t_read
    previous_rudat = param.rudat

    best_F_post = 0
    best_timestamp = ''
    best_params={}

    ### Begin ###
    for t_read in t_vec:
        tl = 1
        t_read = round(1e9*t_read)*1e-9
        param.t_read = t_read
        for rud in r_vec:
            param.set_rudat( rud )
            for freq_read in f_vec:
                fid = {}
                title_str = 'T='+str(int(1e9*t_read))+'; R='+str(rud)+'; F='+str(round(freq_read, 3))
                try:
                    param.freq_read = freq_read
                    qt.msleep(0.2)
                    print '\n', title_str, '\n'

                    ssr = get_fidelity(param, counts=ss_counts, av=ss_av,  title=title_str, switch_off_smb_after=False )

                    timestamp = take_dt_str(date=False,time=True, slash=False)
                    fid = ssr.dict_fidelity
                    qt.msleep(0.2)
                except:
                    print '_______Error was at T=', t_read, 'R=', rud, 'F=', freq_read
                    qt.msleep(0.2)
                    continue  ## skip the rest, nothing to save, go to the next itteration
                finally:
                    gc.collect() ##clean RAM

                ###

                data_fidelity_TRF_params.add_data_point( 1e9*t_read, rud, freq_read,
                                fid['F'], fid['F_g'], fid['F_e'],
                                fid['F_post'], fid['F_post_g'], fid['F_post_e'],
                                fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'],
                                fid['Err_e'], fid['Err_g'])

                # data_fidelity_TR_params.add_data_point( 1e9*t_read, rud,
                #                 fid['F'], fid['F_g'], fid['F_e'],
                #                 fid['F_post'], fid['F_post_g'], fid['F_post_e'],
                #                 fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'],
                #                 fid['Err_e'], fid['Err_g'])
                #
                # data_fidelity_RF_params.add_data_point( rud, freq_read,
                #                 fid['F'], fid['F_g'], fid['F_e'],
                #                 fid['F_post'], fid['F_post_g'], fid['F_post_e'],
                #                 fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'],
                #                 fid['Err_e'], fid['Err_g'])
                #
                # data_fidelity_FT_params.add_data_point( freq_read, 1e9*t_read,
                #                 fid['F'], fid['F_g'], fid['F_e'],
                #                 fid['F_post'], fid['F_post_g'], fid['F_post_e'],
                #                 fid['F_gaus'], fid['F_gaus_eg'], fid['F_gaus_ge'],
                #                 fid['Err_e'], fid['Err_g'])

                if fid['F_post'] > best_F_post:
                    best_F_post = fid['F_post']
                    best_params = {"t_read":t_read, "rud":rud, "freq_read":freq_read}
                    best_timestamp = timestamp

            #### __ loop of Freq finished __
            # data_fidelity_TRF_params.new_block()

        #### __ loop of Rudat finished __
        # data_fidelity_TRF_params.new_block()

    #### End ####
    # plot3d_Fp_TR.save_png()
    # plot3d_Fp_RF.save_png()
    # plot3d_Fp_TF.save_png()
    data_fidelity_TRF_params.close_file()
    # data_fidelity_TR_params.close_file()
    # data_fidelity_RF_params.close_file()
    # data_fidelity_FT_params.close_file()

    param.freq_read = previous_fread
    param.t_read    = previons_tread
    param.set_rudat(previous_rudat)
    all_smb_off()

    stop_time = datetime.datetime.now()
    print '\n _______finished at:', stop_time,'\n','       TOTAL TIME:', stop_time - start_time
    print "\nBest result is ", round( 100*best_F_post, 3 ), "% reached at ", best_timestamp, "\n with parameters: \n", best_params
    return


###########################################################

##############___T1(Relaxation)___###########
####___t1 on given current___###
def t1_from_cur(current, graph = False, f_min_cav = 6.6, f_max_cav = 7.15, numt1meas = 10, rudat_close=30, rudat_open=10, precRabi=False, precFreqs=True, t1_averaging=1e3):
    '''
    make all spectroscopy for measure T1 for given current
    returns t1 as array of 10(numt1meas) times measured t1 (used for statistic)
    change the param_t1! Use param_t1 for measurments!
    ! function use rudat_2 on the qubit line!
    '''
    #check value
    if check_rudat_value(rudat_open)==False or check_rudat_value(rudat_close)==False:
        print 'rudat value is out of range'
        rudat_open = 0
        rudat_close = 30
    rudat_before = Rudat_2.get_attenuation()

    #set up parameters
    param_t1 = SetOfParam()
    param_t1.t_read = 500e-9
    param_t1.power1 = -0.0
    param_t1.nsigma = 0
    param_t1.rudat = Rudat.get_attenuation()
    param_t1.currentrent = current
    #set current
    qt.msleep(1)

    # Cur_qub.set_current(current)
    set_qub_cur(current)
    qt.msleep(1)

    #print time of start
    start_time = datetime.datetime.now()
    print ' started at:', start_time, '\n'
    print 't1_vs_cur = ', current


    #########do the onetone and twotone spectroscopy:########
    Rudat_2.set_attenuation(rudat_close)
    qt.msleep(0.5)
    if COMMENTS:
        print 'Rudat_2 =', rudat_close, 'dB'
        print 'onetone spectroscopy'
    qt.msleep(1)

    ###___set f_read and f_qub by spectroscopy___###
    set_spectr(param_t1)
    param_t1.show()

    #######find a pi-pulse by Rabi########
    Rudat_2.set_attenuation(rudat_open)
    qt.msleep(0.5)
    Rudat_2.set_attenuation(rudat_open)
    qt.msleep(0.5)
    if COMMENTS:
        print 'Rudat_2 = ', rudat_open, '- start rabi'

    pwr2 = -0.5
    param_t1.power2 = pwr2
    #precRabi - means do the iteration finding best power2 for exactly pi-pulse
    if precRabi:
        closest_tpi = get_closest_tpi(param_t1, onlyEven=precFreqs, onlyBigger=False, graph = graph, averaging = 2e3)
        if closest_tpi is None:
            print '__________bad rabi!'
            return None
        qt.msleep(0.5)
        wanted_tpi = closest_tpi[0]
        raw_tpi = closest_tpi[1]
        print 'wanted tpi is: ', wanted_tpi #must be in seconds
        pwr2 = find_pwr2(param_t1, wanted_tpi, graph=graph, tpi = raw_tpi, pwr2 = pwr2,
                            averaging = 2e3, precision = 0.5) #precision in %
        qt.msleep(0.5)
    else:
        closest_tpi = get_closest_tpi(param_t1, graph = graph,
                                        onlyBigger=False, onlyEven=precFreqs, #if prec freq=>ramey=>need even tpi
                                         averaging = 2e3)
        if closest_tpi is None:
            print '__________bad rabi!'
            return None
        wanted_tpi = closest_tpi[0]

    if pwr2 is None:
        print 'bad power2'
        return None
    param_t1.tpi = wanted_tpi
    param_t1.power2 = pwr2

    ######___do ramsey and dblob___#######
    set_prec_freq_read(param_t1)
    #set_prec_freq_q(param_t1) #doesent work now

    ######___make a relaxation (by function)___######
    [mean_t1, std_t1] = get_relax_list(param_t1, graph=graph, averaging=t1_averaging, amount=numt1meas, comnt='cur='+str(param_t1.current))

    stop_time = datetime.datetime.now()
    print '\n __t1_from_cur() finished at:', stop_time,'\n','       time:', stop_time - start_time

    result = [mean_t1, std_t1, current, param_t1.freq_read, param_t1.freq_q, param_t1.tpi, param_t1.power2]
    Rudat_2.set_attenuation(rudat_before)
    return result

####___t1 versus flux___###
def t1_vs_flux(cur_vec, numt1meas = 10, graph = False, f_min_cav=6.8, f_max_cav=7.2, rudat_close=30,rudat_open=10, precRabi=False, precFreqs=True):
    '''
    Measure T1 time versus current_max
    Use t1_from_cur(), call it with different current and save the data
    returns [curents, cav_freqs, q_freqs, t_pi, power2's, arrays of T1's ]
    '''
    start_time = datetime.datetime.now()
    print ' started at:', start_time, '\n'

    data_t1_flux = qt.Data(name='______t1_vs_flux')

    data_t1_flux.add_coordinate('current',  units = 'mA')
    data_t1_flux.add_coordinate('F_read',   units ='GHz')
    data_t1_flux.add_coordinate('F_qubit',  units = 'GHz')
    data_t1_flux.add_coordinate('tpi',      units = 'ns')
    data_t1_flux.add_coordinate('power2',   units = 'V')
    data_t1_flux.add_value(     'T1_mean',  units = 'ns')
    data_t1_flux.add_value(     'T1_std',   units = 'ns')
    data_t1_flux.create_file()
    qt.msleep(1)
    #========================measurment---------
    if max(cur_vec) > 100e-3:
        print 't1_vs_flux ERROR: current more than 100 mA!'
        return None

    curcur = []
    tt = []
    ter = []
    cavcav = []
    qq = []
    pipi = []
    p2p2 = []
    try:
        for i in cur_vec:
            print '=========CURRENT = ',i,' ============'

            result = t1_from_cur(i, graph = graph, numt1meas = numt1meas,
                                f_min_cav=f_min_cav, f_max_cav=f_max_cav, rudat_close=rudat_close, rudat_open=rudat_open,
                                precRabi=precRabi, precFreqs=precFreqs)
            #result = [t1_array, current, freq_read, freq_q, tpi, power2]

            if result is None:
                print 'No result: __________on current= ', i, 'mA'
                continue    #go to  next current

            curcur.append(result[2])
            cavcav.append(result[3])
            qq.append(result[4])
            pipi.append(result[5])
            # p2p2.append(1e9*result[5]) #!V
            p2p2.append(result[6]) #!V
            tt.append(result[0])
            ter.append(result[1])

            data_t1_flux.add_data_point(result[2], result[3], result[4], result[5], result[6], result[0], result[1])
            print 'data saved'
    ##=============================end of measurment=--
    except:
        print '!_________ERROR DURING T1_VS_FLUX_____!'

    finally:
        data_t1_flux.close_file()

        stop_time = datetime.datetime.now()
        print '\n finished at:', stop_time,'\n','       time:', stop_time - start_time
        print '\n return  0-cur, 1-fr, 2-fq, 3-tpi, 4-pwr2, 5-t1_meas, 6-t1_std '

        return [curcur, cavcav, qq, pipi, p2p2, tt, ter]

def t1_vs_flux_usedata(numt1meas = 10, graph = True, rudat_open=8):
    '''
    Was made for measure only t1 by knowing spectro and rabi parameters vs current
    call relaxation
    return [t1t1, param7.current, param7.freq_read, param7.freq_q, param7.tpi, param7.power2]
    '''
    #open file
    filename = '183849_data_t1.dat'
    data = np.loadtxt(filename)

    #create new data file
    data_t1_flux = qt.Data(name='______t1_vs_flux')

    data_t1_flux.add_coordinate('current',  units = 'mA')
    data_t1_flux.add_coordinate('F_read',   units ='GHz')
    data_t1_flux.add_coordinate('F_qubit',  units = 'GHz')
    data_t1_flux.add_coordinate('tpi',      units = 'ns')
    data_t1_flux.add_coordinate('power2',   units = 'V')
    data_t1_flux.add_value(     'T1_mean',  units = 'ns')
    data_t1_flux.add_value(     'T1_std',   units = 'ns')

    data_t1_flux.create_file()

    #========================measurment---------
    Rudat_2.set_attenuation(rudat_open)
    qt.msleep(0.5)
    print 'rudat is: ', Rudat_2.get_attenuation(), 'dB'

    for i in range(len(data)):
        print '=========CURRENT = ',i,' ============'
        #result = t1_from_cur(i, graph = graph, numt1meas = numt1meas)
        param7 = SetOfParam()
        param7.t_read=500e-9
        param7.rudat = Rudat.get_attenuation()
        current = data[i][0]
        param7.current = current
        param7.freq_read = data[i][1]
        param7.freq_q = data[i][2]
        param7.tpi = data[i][3]
        param7.power2 = data[i][4]
        param7.show()
        # do t1
        qt.msleep(1)
        # Cur_qub.set_current(current)
        set_qub_cur(current)
        qt.msleep(2)
        # print 'current=', Cur_qub.get_current(), 'A'
        # qt.msleep(1)

        # make a relaxation1
        t1t1 = []

        t1 = get_relax_time(param7, graph = graph, averaging = 2e3)
        if t1 is not None:
            t1t1.append(t1)
        for i in range(numt1meas - 1):
            qt.msleep(0.5)
            t1 = get_relax_time(param7, graph = graph, averaging = 2e3, Tabor_loading = 0)
            if t1 is not None:
                t1t1.append(t1)


        param7.t1 = np.mean(t1t1)
        print 't1 is ', np.mean(t1t1), '+-', np.std(t1t1)
        #result = [t1_array, current, freq_read, freq_q, tpi, power2]
        result = [t1t1, param7.current, param7.freq_read, param7.freq_q, param7.tpi, param7.power2]

        # finish saving
        if result is None:
            print 'No result: __________on current= ', i, 'mA'
            continue    #go to  next current

        if t1 is not None:
            tt.append(t1t1)
            t1_mean = np.mean(t1t1)
            t1_std = np.std(t1t1)
        else:
            tt.append(0)
            t1_mean = 0
            t1_std = 0
            print 'None returned by t1_from_cur, cur = ', i

        data_t1_flux.add_data_point(result[1], result[2], result[3], result[4], result[5], t1_mean, t1_std)
        print 'data saved'
    #=============================end of measurment=--
    data_t1_flux.close_file()
    stop_time = datetime.datetime.now()
    print '\n __t1_from_cur finished at:', stop_time,'\n','       time:', stop_time - start_time
    print '\n return  0-cur, 1-t1, 2-fr, 3-fq, 4-tpi, 5-power2 '
    return result

def t1_vs_int_flux(cur_span, cur_step, curs_centers=[2.5e-3], numt1meas = 2000, graph = False):
    '''
    Searching the sweetspots and measure t1
    takes: cur_span, cur_step - float, range around each flux and step by current
    takes: curs_centers - list of currents - expected sweetspots
    use t1_from_cur()
    use find_sweetspot()
    '''
    if curs_centers is None:
        curs_centers = []

    flux_ind = []
    cur = []
    freq_q = []


    for n in range(len(curs_centers)):
        if COMMENTS:
            print 'num of flux: ', n

        cur_min = curs_centers[n]-cur_span
        cur_max = curs_centers[n]+cur_span
        if COMMENTS:
            print 'cur min', cur_min,
            print 'cur max', cur_max
            print 'cur step', cur_step
            print 'run find_sweetspot()'
        sweet_params = find_sweetspot(cur_min, cur_max, cur_step)
        sweet_cur = sweet_params[0]
        if COMMENTS:
            print 'current of sweetspot = ', sweet_cur
###########################################################

##############___Ramsey_stark_n_photons__###########
def ramsey_stark_from_freq_read(parameters, pump=1.00, start_fr=7.01,stop_fr=7.06,step_fr=0.005, qub_detuning = 5e-3,  sweet_t_vec=False, tl=1, av=3e3, graph=True, window=1000, nop=200, note=''):
    '''
    Do the measurement ramsey_stark
    for list of freq_read on constant pump
    save the data and plot the graphs
    shift_vs_detuning, T2_vs_detuning
    step in Ghz
    cav_detuning in Ghz
    3 hours - 50 points
    '''
    Tabor_loading = tl
    start_time1 = datetime.datetime.now()
    print ' started at:', start_time1, '\n'
    pump = abs(pump)
    if pump > 1.0:
        print 'pump must be between 0 and 1'
        return False

    #save the value
    freq_read0 = parameters.freq_read
    freq_q0 = parameters.freq_q

    if sweet_t_vec:
        T_vec = np.array([7.0238, 7.0278, 7.0318, 7.0328, 7.0338, 7.0348, 7.0358, 7.0398, 7.0438])
    else:
        T_vec = np.arange(start_fr, stop_fr, step_fr)

    #Qubit frequency a bit above real value (for see oscillations)

    #---saving parameters----
    parameters.save(name='parameters_RamseyStark_from_FR')

    #------data file-------
    data_measurement = qt.Data(name='____Qubit_Shift_vs_Cav_Detun__pump='+str(pump) + note)
    data_measurement.add_coordinate('freq_read',         units = 'us')
    data_measurement.add_value('T2',         units = 'ns')
    data_measurement.add_value('T2_error',         units = 'ns')
    data_measurement.add_value('qubit_shift',         units = 'MHz')
    data_measurement.add_value('qubit_shift_error',         units = 'MHz')
    data_measurement.create_file()

    plot2d_T2 = qt.Plot2D(data_measurement,
                      name      = 'T2 vs freq_read ',
                      coorddim  = 0,
                      valdim    = 1)

    #create arrays:
    ar_fr = []
    ar_t2 = []
    ar_qshift = []

#    try:
    for fr in T_vec:
        parameters.freq_read = fr

        res = get_ramsey_stark_wt2(parameters, pump, tl=tl, qub_detuning=qub_detuning, av=av, graph=graph, window=window, nop=nop, note='_'+str(fr)+'GHz')
        tl = 0
        if res is not None:
            data_measurement.add_data_point(fr, res[0], res[1], res[2], res[3])
            ar_fr.append(fr)
            ar_t2.append(res[0])
            ar_qshift.append(res[2])
            plot2d_T2.replace_inline_data(T_vec, ar_t2)

        else:
            data_measurement.add_data_point(fr, 0, 0, 0, 0)

        #optional
        if res is not None:
            [t2, t2_err, df, df_err] = res
            print 'cav_shift=', fr - freq_read0
            print 'df=  ', df, ' t2=  ', t2,' terr=', t2_err

#    except:
#        print 'error in cicle of ramsey_stark_from_freq_read()'
    #finally:
    data_measurement.close_file()
    plot2d_T2.save_png()
    #set the value back
    parameters.freq_read = freq_read0
    parameters.freq_q = freq_q0
    print '_____return [ar_fr, ar_t2, ar_qshift]'


    stop_time1 = datetime.datetime.now()
    print '\n finished at:', stop_time1,'\n','       time:',
    print 'time of measurement', stop_time1 - start_time1

    return [ar_fr, ar_t2, ar_qshift]

def ramsey_stark_vs_fr_seria(parameters, pump_vector):
    '''
    For make a seria of ramsey-stark measurement with different pump
    Also measure fidelity (with same amplitude) to know the distance
    '''
    time_array = []
    for pump in pump_vector:
        time_array.append(datetime.datetime.now())
        get_fidelity_cor_ampl(parameters, pump)
        ramsey_stark_from_freq_read(parameters, pump)
        qt.msleep(10)

def ramsey_stark_vs_pump(parameters, pump_vector, graph=True):
    '''
    seria of Ramsey_Stark versus pump on constant freq_read
    '''
    data_measurement = qt.Data(name='____RamseyStark_vs_pump')
    data_measurement.add_coordinate('pump',         units = 'part')
    data_measurement.add_value('T2',         units = 'ns')
    data_measurement.add_value('T2_error',         units = 'ns')
    data_measurement.add_value('qubit_shift',         units = 'MHz')
    data_measurement.add_value('qubit_shift_error',         units = 'MHz')
    data_measurement.create_file()

    time_array = []
    list_t2 = []
    list_t2_err = []
    list_fr = []
    list_fr_err = []

    for pump in pump_vector:
        print 'current pump is: ', pump
        notification = 'seria; pump='+str(round(pump,3))+';fr='+str(round(parameters.freq_read,4))
        time_array.append(datetime.datetime.now())

        [t2, t2_err, f_shift, f_shift_err] = get_ramsey_stark_wt2(parameters, pump, note=notification)
        data_measurement.add_data_point(pump, t2, t2_err, f_shift, f_shift_err)
        list_t2.append(t2)
        list_fr.append(f_shift)

    if graph:
        plt.figure()
        plt.plot(pump_vector, list_t2, '.')
        # plt.errorbar(pump_vector, list_t2, yerr=list_t2_err)
        plt.xlabel('pump')
        plt.ylabel('T2, ns')
        plt.show()

    data_measurement.close_file()

    print 'the end. Press ctrl-c'
    return [list_t2, list_fr, time_array]

def ramsey_stark_vs_t_read(parameters, t_read_vector, pump=0.2):
    result = []
    for t_read in t_read_vector:
        parameters.t_read = t_read
        print('t_read= ', param0.t_read)
        res = get_ramsey_stark_wt2(parameters, pump, tl=1, graph=True, window=1000)
        result.append(res)
    return result

def ramsey_stark_vs_rudat(parameters, rudat_vector, pump=0.2):
    result = []
    save_rudat = Rudat.get_attenuation()
    qt.msleep(1)

    for rudat in rudat_vector:
        Rudat.set_attenuation(rudat)
        qt.msleep(1)
        parameters.rudat = rudat
        print('rudat_before= ', param0.rudat)
        res = get_ramsey_stark_wt2(parameters, pump, tl=1, graph=True, window=1000)
        result.append(res)

    Rudat.set_attenuation(save_rudat)
    qt.msleep(1)
    return result

def ramsey_stark_vs_awg_offset(parameters, offset_vector, pump=0, graph=True):
    '''
    Measure Ramsey versus offset of awg to calibrate the offset on mixer
    '''
    data_measurement = qt.Data(name='____RamseyStark_vs_AWG_offset')
    data_measurement.add_coordinate('awg_offset',         units = 'Volts')
    data_measurement.add_value('T2',         units = 'ns')
    data_measurement.add_value('T2_error',         units = 'ns')
    data_measurement.add_value('qubit_shift',         units = 'MHz')
    data_measurement.add_value('qubit_shift_error',         units = 'MHz')
    data_measurement.create_file()

    list_offset = []
    list_t2 = []
    list_t2_err = []
    list_fr = []
    list_fr_err = []

    for awg_offset in offset_vector:
        print 'awg_offset is: ', awg_offset
        notification = 'calibrating awg_offset =' + str(awg_offset)
        t_load = True
        for i in range(10):
            [t2, t2_err, f_shift, f_shift_err] = get_ramsey_stark_wt2(parameters, awg_offset=awg_offset, pump=0, note=notification, av=10e3, window=8000, tl=t_load)
            t_load = False
            data_measurement.add_data_point(awg_offset, t2, t2_err, f_shift, f_shift_err)
            list_offset.append(awg_offset)
            list_t2.append(t2)
            list_t2_err.append(t2_err)


    if graph:
        plt.figure()
        plt.plot(offset_vector, list_t2, '.')
        plt.errorbar(pump_vector, list_t2, yerr=list_t2_err)
        plt.xlabel('pump')
        plt.ylabel('T2, ns')
        plt.show()

    print 'the end. Press ctrl-c'
    data_measurement.close_file()
    return [list_t2, list_fr]

def do_ramsey_stark_fringes(parameters, freq_read_vector, pump=1.0, qub_detuning=5e-3, av=3e3, window=800, nop=200, graph=True, awg_offset=AWG_OFFSET, tl=1, title='', t2_limit_ns=20e3):
    '''
    Vary Freq READOUT, measuring ramsey-stark to calibrate N-photons
    '''
    if title != '':
        title = str(title)
        titile = '_'+title

    pump = abs(pump)
    if pump > 1.0:
        print 'pump must be between 0 and 1'
        return False

    qt.msleep(0.1)
    parameters.save(name='RamseyStark_fringes-parameters')
    time_start = taketime()

    data_measurement = qt.Data(name='___RamseyStark_fringes'+title)
    data_measurement.add_coordinate('Frequency of readout [GHz]', units = 'Ghz')
    data_measurement.add_coordinate('delay time between pi/2 pulses [ns]', units = 'ns')
    data_measurement.add_value('Amplitude ',    units = 'Volt')
    data_measurement.add_value('Phase ',        units = 'rad')
    data_measurement.add_value('Re ',           units = 'Volt')
    data_measurement.add_value('Im ',           units = 'Volt')
    data_measurement.add_value('Dist ',         units = 'Volt')
    data_measurement.add_value('Norm ',         units = 'Volt')
    data_measurement.create_file()

    data_extracted = qt.Data(name='___RamseyStark_vs_Fr_Read_extr_val'+title)
    data_extracted.add_coordinate('Frequency of readout [GHz]', units = 'Ghz')
    data_extracted.add_value('T2 [ns]',          units = 'ns')
    data_extracted.add_value('T2_err',      units = 'ns (or arb units)')
    data_extracted.add_value('dfr_Q [MHz]',       units = 'MHz')
    data_extracted.add_value('dfr_Q_err',   units = 'MHz (or arb units)')
    data_extracted.add_value('Gamma [MHz]',       units = 'rate MHz')
    data_extracted.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'RamseyStark fringes (dist)',
                      coorddim  = (0,1),
                      valdim    = 6)
    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'RamseyStark fringes (Re)',
                      coorddim  = (0,1),
                      valdim    = 4)
    plot3d_3 = qt.Plot3D(data_measurement,
                      name      = 'RamseyStark fringes (Im)',
                      coorddim  = (0,1),
                      valdim    = 5)
    plot3d_4 = qt.Plot3D(data_measurement,
                      name      = 'RamseyStark fringes (norm)',
                      coorddim  = (0,1),
                      valdim    = 7)

    plot2d_1 = qt.Plot2D(data_extracted, name=' T2', coorddim=0, valdim=1)
    plot2d_2 = qt.Plot2D(data_extracted, name=' df', coorddim=0, valdim=3)
    plot2d_3 = qt.Plot2D(data_extracted, name=' Gamma', coorddim=0, valdim=5)

    freq_read_old = parameters.freq_read

    for freq_read in freq_read_vector:
        parameters.freq_read = freq_read
        qt.msleep(1.0)

        (values, data) = get_ramsey_stark_wt2(parameters, pump, qub_detuning=qub_detuning, av=av, window=window,
                        nop=nop, Return_all_data=True, Return_extracted_values=True, graph=graph, awg_offset=awg_offset, tl=tl, note='fr_r='+str(round(freq_read,4)))

        tl=0

        [t2, t2_err, df, df_err] = values
        if t2 > t2_limit_ns:
            t2 = -1.0  #just to filter bad extraction
        gamma = 1e3 *(1.0 /t2)  #t2 in ns, convert it to freq [GHz], than gamma converts in [MHz]
        data_extracted.add_data_point(freq_read, t2, t2_err, df, df_err, gamma)
        [time_vec, amplitude, phase, real_a, imag_a, dist_a, norm_a] = data
        data_measurement.add_data_point( parameters.freq_read *np.ones_like(time_vec), time_vec, amplitude, phase, real_a, imag_a, dist_a, norm_a )
        data_measurement.new_block()

    qt.mend()
    data_measurement.close_file()
    data_extracted.close_file()
    plot3d_1.save_png()
    plot3d_2.save_png()
    plot3d_3.save_png()
    plot3d_4.save_png()
    plot2d_1.save_png()
    plot2d_2.save_png()
    plot2d_3.save_png()

    parameters.freq_read = freq_read_old

    time_stop = taketime()
    print 'started at: ', time_start
    print 'stoped at:', time_stop, 'for N-freq:', len(time_vec)
    return

###########################################################

##############___Rabi shevrons__Ramsey fringes__###########
def do_rabi_shevrones(parameters, freq_q_vector, averaging=1e3, window=2000, nop=400, graph=True, awg_offset=AWG_OFFSET, tl=1):
    '''
    function for do the shevrones Rabi
    function can only collect data in file (no plotting)
    '''
    # qt.msleep(0.1)
    qt.mstart()
    parameters.save(name='Rabi-chevrons-parameters')
    time_start = taketime()

    data_measurement = qt.Data(name='___Rabi_chevrons')
    data_measurement.add_coordinate('Frequency of qubit tone [GHz]', units = 'Ghz')
    data_measurement.add_coordinate('excitation time [ns]', units = 'ns')
    data_measurement.add_value('Amplitude ',    units = 'Volt')
    data_measurement.add_value('Phase ',        units = 'rad')
    data_measurement.add_value('Re ',           units = 'Volt')
    data_measurement.add_value('Im ',           units = 'Volt')
    data_measurement.add_value('Dist ',         units = 'Volt')
    data_measurement.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'Rabi shevrons (dist)',
                      coorddim  = (0,1),
                      valdim    = 6)
    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'Rabi shevrons (Re)',
                      coorddim  = (0,1),
                      valdim    = 4)
    plot3d_3 = qt.Plot3D(data_measurement,
                      name      = 'Rabi shevrons (Im)',
                      coorddim  = (0,1),
                      valdim    = 5)

    freq_qubit_old = parameters.freq_q

    for freq_qubit in freq_q_vector:

        parameters.freq_q = freq_qubit

        result = get_rabi_pi(parameters, parameters.power2, Return_tpi_only=False, averaging=averaging, window=window, nop=nop, graph=graph, awg_offset=awg_offset, tl=tl)
        tl=0

        [time_vec, amplitude, phase, real_a, imag_a, dist_a] = result
        data_measurement.add_data_point( parameters.freq_q *np.ones_like(time_vec), time_vec, amplitude, phase, real_a, imag_a, dist_a )
        data_measurement.new_block()

    qt.mend()
    data_measurement.close_file()
    plot3d_1.save_png()
    plot3d_2.save_png()
    plot3d_3.save_png()

    parameters.freq_q = freq_qubit_old

    time_stop = taketime()
    print 'started at: ', time_start
    print 'stoped at:', time_stop, 'for N-freq:', len(time_vec)
    return

def do_ramsey_fringes(parameters, freq_q_vector, av=1e3, window=1000, nop=400, graph=True, awg_offset=AWG_OFFSET, tl=1):
    '''
    Vary Freq qubit, measuring ramsey to make Ramsey fringes
    '''

    qt.msleep(0.1)
    parameters.save(name='Ramsey_fringes-parameters')
    time_start = taketime()

    data_measurement = qt.Data(name='___Ramsey_fringes')
    data_measurement.add_coordinate('Frequency of qubit tone [GHz]', units = 'Ghz')
    data_measurement.add_coordinate('delay time between pi/2 pulses [ns]', units = 'ns')
    data_measurement.add_value('Amplitude ',    units = 'Volt')
    data_measurement.add_value('Phase ',        units = 'rad')
    data_measurement.add_value('Re ',           units = 'Volt')
    data_measurement.add_value('Im ',           units = 'Volt')
    data_measurement.add_value('Dist ',         units = 'Volt')
    data_measurement.create_file()

    plot3d_1 = qt.Plot3D(data_measurement,
                      name      = 'Ramsey fringes (dist)',
                      coorddim  = (0,1),
                      valdim    = 6)
    plot3d_2 = qt.Plot3D(data_measurement,
                      name      = 'Ramsey fringes (Re)',
                      coorddim  = (0,1),
                      valdim    = 4)
    plot3d_3 = qt.Plot3D(data_measurement,
                      name      = 'Ramsey fringes (Im)',
                      coorddim  = (0,1),
                      valdim    = 5)

    freq_qubit_old = parameters.freq_q

    for freq_qubit in freq_q_vector:
        parameters.freq_q = freq_qubit

        result = get_ramsey_df_backup_20210622(parameters, qub_detuning=0.0, Return_all_data=True, averaging=av, window=window, nop=nop, graph=graph, awg_offset=awg_offset, tl=tl)
        tl=0

        [time_vec, amplitude, phase, real_a, imag_a, dist_a] = result
        data_measurement.add_data_point( parameters.freq_q *np.ones_like(time_vec), time_vec, amplitude, phase, real_a, imag_a, dist_a )
        data_measurement.new_block()

    qt.mend()
    data_measurement.close_file()
    plot3d_1.save_png()
    plot3d_2.save_png()
    plot3d_3.save_png()

    parameters.freq_q = freq_qubit_old

    time_stop = taketime()
    print 'started at: ', time_start
    print 'stoped at:', time_stop, 'for N-freq:', len(time_vec)
    return

def rabi_ramsey():
    freq_q_vec = np.arange(6.27, 6.32, 0.125e-3)
    time1 = do_rabi_shevrones(param0, freq_q_vec, averaging=2e3)
    time2 = do_ramsey_fringes(param0, freq_q_vec, averaging=2e3)

    return [time1, time2]

###########################################################

##### Onetone versus Rudat (power of readout) ###
def onetone_vs_rudat(rdt_vec, f_min_cav=6.8, f_max_cav=7.2, averaging = 0.5e3, nop=200,awg_offset=AWG_OFFSET):
    '''
    Make simple onetone spectroscopy using function get_onetone_fread
    versus power of readout signal (by changing rudat attenuation)
    '''
    import matplotlib.gridspec as gridspec

    remember_rudat = Rudat.get_attenuation()
    qt.msleep(0.4)


    tl =1
    # try:
    rdt_list = []
    results_list = []
    for rdt in rdt_vec:
        print '\n____Rudat attenuation ', rdt, ' dB'
        if not check_rudat_value(rdt):
            empty_list = [ [0],  [0], [0], [0], [0,0,0,0,0]]
            results_list.append(empty_list)
            continue # go to next step immidiately
        Rudat.set_attenuation(rdt)
        qt.msleep(0.4)

        # fr = get_onetone_fread( f_min_cav=f_min_cav, f_max_cav=f_max_cav, averaging = averaging, nop=nop)
        result_onetone = get_onetone_fread(returnALL=True, tl=tl, f_min_cav=f_min_cav, f_max_cav=f_max_cav, averaging = averaging, nop=nop)
        # try:
        #     freq_vec = result_onetone[0]
        #     amplitude = result_onetone[1]
        #     phase = result_onetone[2]
        # except:
        #     print 'error of read result_onetone'
        #
        # try:
        #     values_from_fit = result_onetone[3]
        #     fit_params = result_onetone[4]  ### fit params = [bg, area, f0, width]
        # except:
        #     values_from_fit = [0]
        #     fit_params = [0,0,0,0,0]
        #     print 'error of read fit parameters from result_onetone'

        rdt_list.append(rdt)
        results_list.append(result_onetone)
        tl = 0


    number_of_plots = len(results_list)
    plt.figure(figsize=[12,3*number_of_plots])
    gs = gridspec.GridSpec(number_of_plots, 1)

    axes_list = []
    for i in range(number_of_plots):
        res = results_list[i]
        freq = res[4][2]  ## take frequency from fit
        title = 'Rdt='+ str(rdt_list[i]) +'dB; Fr='+ str( round(freq, 4) ) +'GHz'
        ax = plt.subplot(gs[i])
        ax.plot(res[0], 1e3*res[1], color='r')

        # ### make it work fit data
        # try:        ## try to plo fit
        #     ax.plot(res[0], 1e3*res[3], color='#B5965B', ls='--')
        # except:
        #     print 'fit didnt plotted for #', i

        ax.set_ylabel('Amp [mV]')
        ax.grid()
        ax.axvline(x=freq, alpha=0.5, c='#B5965B', lw=1, ls='--')
        ax.set_title(title)
        # erase axis if it is not the last one
        if i < number_of_plots-1: ## if not last iteration
            # ax.get_xaxis().set_visible(False)   ## erase all xaxis
            ax.xaxis.set_ticklabels([])         ## erase text xaxis
        else:
            ax.set_xlabel('Frequency [GHz]')

        axes_list.append(ax)

    date_time_string = take_dt_str(date=True,time=True, slash=True)
    picname = 'D:\\Data\\' + date_time_string+'onetone_vs_rdt' +'.png'
    plt.savefig(picname)
    plt.close()


    # except:
    #     print 'some error in onetone_vs_rudat'
    # finally:
    Rudat.set_attenuation(remember_rudat)
    qt.msleep(0.4)
    print 'returned [rdt_list, fr_list]'
    return [rdt_list, results_list]

#### Ramsey_vs_flux ####

# def get_ramsey_vs_flux(parameters, currents, freq_shift=1e-3, window=1000):
#
#     freq_q_initial = parameters.freq_q
#     parameters.freq_q = parameters.freq_q + freq_shift
#
#     data_measurement = qt.Data(name='Ramsey_vs_flux')
#     data_measurement.add_coordinate('current [uA]', units = 'uA')
#     data_measurement.add_value('Detuning [MHz]',            units = 'MHz')
#     data_measurement.create_file()
#
#
#     plot2d_3 = qt.Plot2D(data_measurement,
#                       name      = 'Detuning vs flux',
#                       coorddim  = 0,
#                       valdim    = 1,
#                       maxtraces = 2)
#     cur_list = []
#     df_list = []
#     Tabor_flag = 1
#     for i in currents:
#         print 'currents:', currents
#         set_qub_cur(i)
#         df = get_ramsey_df(parameters, tl=Tabor_flag, window=window) #if 'stop pressed during measurement - this string cancelles'
#
#         Tabor_flag = 0
#         df_list.append(df*1e3) ### in [MHz]
#         cur_list.append(i*1e6) ### in [uA]
#
#         plot2d_3.replace_inline_data(np.array(cur_list), df_list)
#
#     data_measurement.add_data_point(np.array(cur_list), df_list)
#     plot2d_3.save_png()
#
#
#     data_measurement.close_file()
#     parameters.freq_q = freq_q_initial
#     return [cur_list, df_list]

def get_ramsey_vs_flux(parameters, currents, freq_shift=1e-3, window=1000):

    freq_q_initial = parameters.freq_q
    parameters.freq_q = parameters.freq_q + freq_shift

    data_measurement = qt.Data(name='Ramsey_vs_flux')
    data_measurement.add_coordinate('current [uA]', units = 'uA')
    data_measurement.add_value('Detuning [MHz]',            units = 'MHz')
    data_measurement.create_file()

    try:
        plot2d_3 = qt.Plot2D(data_measurement,
                          name      = 'Detuning vs flux',
                          coorddim  = 0,
                          valdim    = 1,
                          maxtraces = 2)
        cur_list = []
        df_list = []
        Tabor_flag = 1
        for i in currents:
            try:
                set_qub_cur(i)
                df = None
                df = get_ramsey_df(parameters, tl=Tabor_flag, window=window) #if 'stop pressed during measurement - this string cancelles'
                if df is None:
                    print 'Loop interrupted \n(probably "stop"-button pressed)'
                    break

                Tabor_flag = 0
                df_list.append(df*1e3) ### in [MHz]
                cur_list.append(i*1e6) ### in [uA]

                plot2d_3.replace_inline_data(np.array(cur_list), df_list)
            except:
                print 'Error during measurement. Loop interrupted'
                break

        data_measurement.add_data_point(np.array(cur_list), df_list)
        plot2d_3.save_png()

    finally:
        data_measurement.close_file()
        parameters.freq_q = freq_q_initial
        return [cur_list, df_list]

def get_vna_trace_jpa_gain(label):
    # smb_cavity_off()
    all_smb_off()
    memory = get_vna_trace(fr_start=6.0, fr_stop=8.0, bw=500, nop=501, fname='memory_'+label)
    qt.msleep(0.2)

    # smb_cavity_on()
    all_smb_on()
    gain = get_vna_trace(fr_start=6.0, fr_stop=8.0, bw=500, nop=501, fname='gain_'+label, memory=memory)
    qt.msleep(0.1)

    [freq, amp, ph] = gain
    max = np.max(amp)
    print 'MAXIMUM IS:', max

    return max

def give_ramsey_stark_result(file):
        data = np.loadtxt(file)
        fr = data[:,0]
        T2 = data[:,1]

        plt.plot(fr, abs(1/T2))
        plt.xlabel('freq_read (GHz)')
        plt.ylabel('Gamma')
        plt.show()

        return fr, T2



####################################################

def check_att(v, mem):
    set_att_v(v)
    res = get_vna_trace(memory=mem, fname='vatt='+str(v))
    qt.msleep(0.5)
    return res

def vna_vs_att(v_att_vec, mem):
    res_list =[]
    max_list =[]
    for v in v_att_vec:
         s = check_att(v, mem)
         res_list.append(s)
         max_list.append( np.max(s[1]) )

    plt.plot(v_att_vec, max_list)

def try_ats_as_oscilloscop(pulse_time=500, samplerate=1000, delta_t=0):
    import ATS9360.DataTreatment as dt

    qt.mstart()

    ats9360.set_acquisition_time(pulse_time)
    # processus = dt.HomodyneRealImag_raw(pulse_time*1e-9, samplerate*1e6, delta_t*1e-9)
    processus = dt.Raw()

    ats9360.measurement_initialization(processor=processus)
    while ats9360.get_completed_acquisition() != 100.:
        result = ats9360.measurement()      #result we obtain from the board

    print(result)

    try:
        ats9360.measurement_close(transfert_info=False)
        board_flag = False
    except:
        qt.msleep(2.)
        ats9360.measurement_close(transfert_info=False)
    return True


################################################################################
################################################################################
#
#
#               _MAIN_
#
#
################################################################################

COMMENTS = True
Tabor.set_ch1_offset(AWG_OFFSET)

def script_measure(parameters):

    try:
        AWG_OFFSET = 0.0
        Tabor.set_ch1_offset(AWG_OFFSET)
        first = 1
        for i in range(1000):
            get_ramsey_df(parameters, qub_detuning=2, tl=first, averaging=3e3, window=2000, graph=True, awg_offset=AWG_OFFSET)
            first = 0
        # for rudat in [10,20,30]:
        #     parameters.set_rudat(rudat)
        #     do_traject_measure(param0, n_of_files=100, t_read=500e-9, averaging=150, pause=1, with_pio2=True, title="pio2_500ns_rudat={}".format(parameters.rudat))
        #
        # for rudat in [6,8,10,12]:
        #     parameters.set_rudat(rudat)
        #     do_traject_measure(param0, n_of_files=25, t_read=100000e-9, averaging=4, pause=1, title="_100us_rudat={}".format(parameters.rudat))
        #
        #     # do_traject_measure(param0, n_of_files=5, t_read=1000000e-9, averaging=2, pause=5, title="_1000us_rudat={}".format(parameters.rudat))

    finally:
        # smb_cavity_off()
        all_smb_off()

def give_params_w8ch03_1():
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(0.0) #excluded
    param.freq_q = 2.52385
    param.tpi = 212e-9
    param.power2 = -0.0 #-4.0
    param.nsigma = 0


    ###___Parameters of Readout tone___########################
    param.set_rudat(12)
    param.freq_read = 7.40    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 1200e-9 #duration of readout pulse
    param.t_between = 1000e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_20210601():
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(6.50) #0.25)
    param.freq_q = 2.47576
    param.tpi = 142e-9 #110e-9
    param.power2 = -0.08 #-0.00
    param.nsigma = 0


    ###___Parameters of Readout tone___########################
    param.set_rudat(14)
    param.freq_read = 7.3685    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 900e-9 #duration of readout pulse
    param.t_between = 1000e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_20210604():
    '''
    Precise qubit freq after current shift
    nsigma = 1.8 - gaussian pi-pulse
    '''
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(6.50) #0.25)
    param.freq_q = 2.475712
    param.tpi = 174e-9 #140e-9 #110e-9
    param.power2 = -0.00
    param.nsigma = 1.8


    ###___Parameters of Readout tone___########################
    param.set_rudat(14)
    param.freq_read = 7.3685    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 900e-9 #duration of readout pulse
    param.t_between = 1000e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_20210614():
    '''
    Precise qubit freq after current shift
    nsigma = 1.8 - gaussian pi-pulse
    '''
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(6.5) #0.25)
    param.freq_q = 2.47579936 #2.475797
    param.tpi = 140e-9 #140e-9 #110e-9
    param.power2 = -0.17 # only amplical, no Rudat2
    param.nsigma = 0.0


    ###___Parameters of Readout tone___########################
    param.set_rudat(6.0)
    param.freq_read = 7.355    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 150e-9 #duration of readout pulse
    param.t_between = 300e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param




def give_params_w8ch03_20210617_nogaus():
    '''
    Precise qubit freq after current shift
    nsigma = 1.8 - gaussian pi-pulse
    '''
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(6.5) #0.25)
    param.freq_q = 2.47579936 #2.475797
    param.tpi = 118e-9 #140e-9 #110e-9
    param.power2 = -0.11 # only amplical, no Rudat2
    param.nsigma = 0.0


    ###___Parameters of Readout tone___########################
    param.set_rudat(6.0)
    param.freq_read = 7.355    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 150e-9 #duration of readout pulse
    param.t_between = 150e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_20210622_best_fidelity993():
    '''
    Precise qubit freq after current shift
    nsigma = 1.8 - gaussian pi-pulse
    '''
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(0.0)  #disconnected at all
    param.freq_q = 2.47579936 #2.475797
    param.tpi = 118e-9 #140e-9 #110e-9
    param.power2 = -0.11 # only amplical, no Rudat2
    param.nsigma = 0.0


    ###___Parameters of Readout tone___########################
    param.set_rudat(1.0)
    param.freq_read = 7.3440    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 150e-9 #duration of readout pulse
    param.t_between = 150e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_20210622_best_fidelity993_almost():
    '''
    Precise qubit freq after current shift
    nsigma = 1.8 - gaussian pi-pulse
    '''
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(0.0)  #disconnected at all
    param.freq_q = 2.47579936 #2.475797
    param.tpi = 118e-9 #140e-9 #110e-9
    param.power2 = -0.11 # only amplical, no Rudat2
    param.nsigma = 0.0


    ###___Parameters of Readout tone___########################
    param.set_rudat(15.0)
    param.freq_read = 7.3440    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 150e-9 #duration of readout pulse
    param.t_between = 150e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param


def give_params_w8ch03_20210617_gaus():
    '''
    Precise qubit freq after current shift
    nsigma = 1.8 - gaussian pi-pulse
    '''
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(6.5) #0.25)
    param.freq_q = 2.47579936 #2.475797
    param.tpi = 126e-9 #140e-9 #110e-9
    param.power2 = -0.03 # only amplical, no Rudat2
    param.nsigma = 2.0


    ###___Parameters of Readout tone___########################
    param.set_rudat(6.0)
    param.freq_read = 7.355    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 150e-9 #duration of readout pulse
    param.t_between = 150e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_20210618_RSTARK():
    '''
    Precise qubit freq after current shift
    nsigma = 1.8 - gaussian pi-pulse
    '''
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(6.5) #0.25)
    param.freq_q = 2.47579936 #2.475797
    param.tpi = 118e-9 #140e-9 #110e-9
    param.power2 = -0.11 # only amplical, no Rudat2
    param.nsigma = 0.0


    ###___Parameters of Readout tone___########################
    param.set_rudat(30.0)
    param.freq_read = 7.362    #from set_prec_freq_read()
    param.power1 = -0.0
    param.t_read = 1000e-9 #duration of readout pulse
    param.t_between = 150e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param



def give_params_w8ch03_0phi0(pol = 'u'):
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(5.0) #excluded
    param.freq_q = 2.521437
    param.tpi = 254e-9
    param.power2 = -0.0 #-4.0
    param.nsigma = 0

    ###___Parameters of Readout tone___########################
    param.set_rudat(10)
    if pol == 'u':
        param.freq_read = 7.402    #from set_prec_freq_read()
    elif pol == 'l':
        param.freq_read = 6.944
    else:
        print 'No polariton identified. Parameters set for upper pol. by default.'
        param.freq_read = 7.402
    param.power1 = -0.0
    param.t_read = 1500e-9 #duration of readout pulse
    param.t_between = 1000e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_2phi0(pol = 'u'):
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(5.0) #excluded
    param.freq_q = 2.524117
    param.tpi = 254e-9
    param.power2 = -0.0 #-4.0
    param.nsigma = 0

    ###___Parameters of Readout tone___########################
    param.set_rudat(10)
    if pol == 'u':
        param.freq_read = 7.373    #from set_prec_freq_read()
    elif pol == 'l':
        param.freq_read = 6.882
    else:
        print 'No polariton identified. Parameters set for upper pol. by default.'
        param.freq_read = 7.373
    param.power1 = -0.0
    param.t_read = 1500e-9 #duration of readout pulse
    param.t_between = 1000e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_4phi0(pol = 'u'):
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(5.0) #excluded
    param.freq_q = 2.52335
    param.tpi = 260e-9
    param.power2 = -0.0 #-4.0
    param.nsigma = 0

    ###___Parameters of Readout tone___########################
    param.set_rudat(10)
    if pol == 'u':
        param.freq_read = 7.324    #from set_prec_freq_read()
    elif pol == 'l':
        param.freq_read = 6.723
    else:
        print 'No polariton identified. Parameters set for upper pol. by default.'
        param.freq_read = 7.324
    param.power1 = -0.0
    param.t_read = 1500e-9 #duration of readout pulse
    param.t_between = 1000e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param

def give_params_w8ch03_6phi0(pol = 'u'):
    ###___Parameters of Qubit tone___########################
    param = SetOfParam()
    param.set_rudat2(5.0) #excluded
    param.freq_q = 2.52175
    param.tpi = 272e-9
    param.power2 = -0.0 #
    param.nsigma = 0

    ###___Parameters of Readout tone___########################
    param.set_rudat(10)
    if pol == 'u':
        param.freq_read = 7.283    #from set_prec_freq_read()
    elif pol == 'l':
        param.freq_read = 6.389
    else:
        print 'No polariton identified. Parameters set for upper pol. by default.'
        param.freq_read = 7.283
    param.power1 = -0.0
    param.t_read = 1800e-9 #duration of readout pulse
    param.t_between = 1000e-9

    ###___Put correct values of rudats and current_source___###
    param.current = get_qub_cur()
    param.set_phase1(0)
    # param.phase1 = Phase_1.get_phase_shift()

    #----------------------------------------------------------
    return param


def get_sweetspot(param, cur_min=13.5e-3, cur_max=13.61e-3, cur_step=0.5e-3, f_min=2.5, f_max=2.55, averaging = 1e3):
    cur_arr = np.arange(cur_min, cur_max, cur_step)
    freq_arr = np.zeros(len(cur_arr))
    i = 0
    tl_flag = 1
    while i < len(cur_arr):
        set_qub_cur(cur_arr[i])
        f_res = get_twotone_fqub(f_cav=param.freq_read, f_min=f_min, f_max=f_max, averaging=averaging, Tabor_loading=tl_flag)
        tl_flag = 0
        if f_res:
            freq_arr[i] = f_res
            i = i+1
        else:
            cur_arr = np.delete(cur_arr, i)
            freq_arr = np.delete(freq_arr, i)

    print 'currents: ', cur_arr
    print 'resonances: ', freq_arr

    if len(freq_arr>0):
        sweetspot_freq = np.amax(freq_arr)
        max_i = np.where(freq_arr == sweetspot_freq)[0]
        sweetspot_cur = cur_arr[max_i]
        print 'sweestpot found is at ', sweetspot_cur, 'with resonance at ', sweetspot_freq
        return sweetspot_cur
    else:
        print 'no resonance was fitted in the given range'
        return None

#-------------START--------------------------------------
start_time = datetime.datetime.now()
print ' started at:', start_time, '\n'

################################################################################
################################################################################

# param0 = give_params_w8ch03_1()
# param0 = give_params_w8ch03_20210617_gaus()

# param0 = give_params_w8ch03_20210617_nogaus()
param0 = give_params_w8ch03_20210622_best_fidelity993_almost()
# param0 = give_params_w8ch03_20210618_RSTARK() # reduced Rudat
#
all_smb_off()
param0.set_rudat(10)
param0.set_rudat2(10)
param0.freq_read = 7.195
param0.freq_q = 1.45622
# param0.tpi = 80e-9
param0.t_read = 1.5e-6
#
#
TWPA_ON = True
print(param0)




set_qub_cur(-0.15e-3)
window = 0.3
for f_init in np.arange(1., 5.2001, window):
    get_twotone_fqub(param0.freq_read, f_min=f_init, f_max=f_init+window, nop=500, averaging=3e3)


window = 0.3
# rdt2_vec = np.arange(30, -0.001, -5)
for f_init in np.arange(1., 5.2001, window):
    # get_onetone_vs_flux(f_min_cav=f_init, f_max_cav=f_init+window, f_step_cav=1.5e-3, current_min=-1.e-3, current_max=1.e-3, current_step=0.1e-3)
    # get_twotone_vs_rudat2(param0, rdt2_vec, f_min=f_init, f_max=f_init+window, av=2e3, nop=300)
    # get_twotone_fqub(param0.freq_read, f_min=f_init, f_max=f_init+window, nop=500, averaging=3e3)
    get_twotone_vs_current(-1.2e-3, 1.2e-3, 0.1e-3, param0.freq_read, f_min=f_init, f_max=f_init+window, nop=400, averaging=2e3, use_res_fit=True)

set_qub_cur(0.)

# get_twotone_vs_current(-1.e-3, 1.e-3, 0.05e-3, 7.235, f_min=1.2, f_max=1.54, nop=400, averaging=1e3)
#
# get_twotone_vs_current(-1.e-3, 1.e-3, 0.05e-3, 7.235, f_min=1.9, f_max=2.2, nop=400, averaging=1e3)
#
# get_twotone_vs_current(-1.e-3, 1.e-3, 0.05e-3, 7.235, f_min=2.9, f_max=3.22, nop=400, averaging=1e3)
#
# get_twotone_vs_current(-1.e-3, 1.e-3, 0.05e-3, 7.235, f_min=3., f_max=3.3, nop=400, averaging=1e3)
#
# get_twotone_vs_current(-0.5e-3, 0.5e-3, 0.05e-3, 7.237, f_min=3., f_max=3.2, nop=400, averaging=1e3)
#
# set_qub_cur(-0.2e-3)


# rdt2_vec = np.arange(30., -0.001, -5.)
# window = 0.3

# for f_init in np.arange(2., 3.8001, window):
    # get_twotone_vs_rudat2(param0, rdt2_vec, f_min=f_init, f_max=f_init+window)
    # get_onetone_fread(f_min_cav=f_init, f_max_cav=f_init+window, averaging=1e3)
    # get_onetone_vs_flux(f_min_cav=f_init, f_max_cav=f_init+window, f_step_cav=1.e-3, current_min=-1.e-3, current_max=1.e-3, current_step=0.1e-3)
    # get_twotone_vs_current(-1.e-3, 1.e-3, 0.1e-3, 7.23, f_min=f_init, f_max=f_init+window, nop=400, averaging=1e3)
    # get_twotone_fqub(param0.freq_read, f_min=f_init, f_max=f_init+window, nop=500, averaging=1e3)

# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.0, f_max=2.1, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.1, f_max=2.2, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.2, f_max=2.3, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.3, f_max=2.4, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.4, f_max=2.5, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.5, f_max=2.6, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.6, f_max=2.7, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.7, f_max=2.8, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.8, f_max=2.9, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=2.9, f_max=3.0, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.0, f_max=3.1, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.1, f_max=3.2, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.2, f_max=3.3, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.3, f_max=3.4, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.4, f_max=3.5, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.5, f_max=3.6, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.6, f_max=3.7, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.7, f_max=3.8, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.8, f_max=3.9, nop=300)
# get_twotone3D(fcav_min=7.1, fcav_max=7.3, fcav_step=1e-3, f_min=3.9, f_max=4.0, nop=300)
#


# get_onetone_vs_flux(f_min_cav=7.15, f_max_cav=7.28, f_step_cav=1e-3, current_min=-10e-3, current_max=10e-3, current_step=0.1e-3)



# param0.set_rudat(10)
# param0.freq_read = 7.28
#
# param0.set_rudat2(20)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=1.5, f_max=2.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=2.5, f_max=3.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=3.5, f_max=4.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=4.5, f_max=5.5, nop=400, averaging=3e3)
#
# param0.set_rudat2(10)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=1.5, f_max=2.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=2.5, f_max=3.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=3.5, f_max=4.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=4.5, f_max=5.5, nop=400, averaging=3e3)
#
# param0.set_rudat2(0)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=1.5, f_max=2.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=2.5, f_max=3.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=3.5, f_max=4.5, nop=400, averaging=3e3)
# get_twotone_vs_current(-0.6e-3, 0.2e-3, 5.4e-6, param0.freq_read, f_min=4.5, f_max=5.5, nop=400, averaging=3e3)
#
# set_qub_cur(-0.3e-3)
#
# set_qub_cur(-0.13e-3)

# cur_vec = [-0.13e-3, -0.6e-3]
# rdt_vec = np.arange(30, -0.1, -5)
#
# for cur in cur_vec:
#     set_qub_cur(cur)
#     for rdt in rdt_vec:
#         param0.set_rudat(rdt)
#         for i in range(20):
#             get_onetone_fread(8, 8.1)
#
#
# param0.set_rudat(15)
# set_qub_cur(-0.13e-3)
# f_q_vec = [1.71, 1.73, 1.91]
#
# smb_atom.set_freqsweep('off')
# for f_q in f_q_vec:
#     smb_atom.set_frequency(f_q)
#
#     for i in range(20):
#         smb_atom.set_status('on')
#         qt.msleep(0.2)
#         get_onetone_fread(8, 8.1)
#         smb_atom.set_status('off')
#         qt.msleep(0.2)



# set_qub_cur(-0.6e-3)
# f_q_vec = [1.37, 1.46, 1.6]
#
# smb_atom.set_freqsweep('off')
# for f_q in f_q_vec:
#     smb_atom.set_frequency(f_q)
#
#     for i in range(20):
#         smb_atom.set_status('on')
#         qt.msleep(0.2)
#         get_onetone_fread(8, 8.1)
#         smb_atom.set_status('off')
#         qt.msleep(0.2)



# param0.freq_read = 7.285
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=2., f_max=2.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=2.5, f_max=3., nop=500, averaging=3e3)
# param0.freq_read = 6.65
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=2., f_max=2.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=2.5, f_max=3., nop=500, averaging=3e3)

# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=3., f_max=3.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=3.5, f_max=4., nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=4., f_max=4.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.05e-3, 7.281, f_min=4.5, f_max=5., nop=500, averaging=3e3)
#
# param0.freq_read = 7.252
# get_twotone_fqub(param0.freq_read, f_min=2.7, f_max=2.75, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.65, f_max=2.7, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.75, f_max=2.8, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.6, f_max=2.65, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.8, f_max=2.85, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.55, f_max=2.6, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.85, f_max=2.9, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.5, f_max=2.55, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.9, f_max=2.95, nop=500, averaging=3e3)
# qt.msleep(2*60)
# get_twotone_fqub(param0.freq_read, f_min=2.95, f_max=3., nop=500, averaging=3e3)
# all_smb_off()
# param0.freq_read = 6.65
# get_twotone_fqub(param0.freq_read, f_min=1., f_max=1.5, nop=500, averaging=3e3)
# get_twotone_fqub(param0.freq_read, f_min=1.5, f_max=2., nop=500, averaging=3e3)
# get_twotone_fqub(param0.freq_read, f_min=2., f_max=2.5, nop=500, averaging=3e3)
# get_twotone_fqub(param0.freq_read, f_min=2.5, f_max=3., nop=500, averaging=3e3)
# get_twotone_fqub(param0.freq_read, f_min=3., f_max=3.5, nop=500, averaging=3e3)
# get_twotone_fqub(param0.freq_read, f_min=3.5, f_max=4., nop=500, averaging=3e3)
# get_twotone_fqub(param0.freq_read, f_min=4., f_max=4.5, nop=500, averaging=3e3)
# get_twotone_fqub(param0.freq_read, f_min=4.5, f_max=5., nop=500, averaging=3e3)
#
# param0.freq_read = 7.285
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=1., f_max=1.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=1.5, f_max=2., nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=2., f_max=2.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=2.5, f_max=3., nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=3., f_max=3.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=3.5, f_max=4., nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=4., f_max=4.5, nop=500, averaging=3e3)
# get_twotone_vs_current(-0.7e-3, 0.1e-3, 0.1e-3, param0.freq_read, f_min=4.5, f_max=5., nop=500, averaging=3e3)

# param0.freq_q = 2.9609
# set_qub_cur(-2.4e-3)
#
# get_rabi_shevrones(param0, fr_vec=np.arange(2.94, 3.02001, 0.0005), nop=500, window=2000)
#
# get_rabi_shevrones(param0, fr_vec=np.arange(2.72, 2.80001, 0.0005), nop=500, window=2000)
# #
# get_rabi_shevrones(param0, fr_vec=np.arange(4.0, 4.2, 0.002), nop=500, window=2000)
#
# get_rabi_shevrones(param0, fr_vec=np.arange(4.2, 4.4, 0.002), nop=500, window=2000)

# get_rabi_shevrones(param0, fr_vec=np.arange(3.2, 3.4, 0.002), nop=500, window=2000)
#
# get_rabi_shevrones(param0, fr_vec=np.arange(3.4, 3.6, 0.002), nop=500, window=2000)
#
# get_rabi_shevrones(param0, fr_vec=np.arange(3.6, 3.8, 0.002), nop=500, window=2000)

# get_relax_list(param0, amount=1000, averaging=3e3)
# param0.freq_q = 2.959 - 5e-3
# get_dephasing_list(param0, amount=500)

# param0.freq_q = 2.945
# param0.tpi = 256e-9
# set_qub_cur(-0.2e-3)
#
# get_relax_list(param0, amount=200, averaging=3e3)
# param0.freq_q = 2.945 - 5e-3
# get_dephasing_list(param0, amount=200)
#
# param0.freq_q = 2.8092
# param0.tpi = 82e-9
# set_qub_cur(-0.e-3)
#
# get_relax_list(param0, amount=200, averaging=3e3)
# param0.freq_q = 2.7883 - 5e-3
# get_dephasing_list(param0, amount=200)

# t_read_list = [10,30,50,100,130,150,200,300,500,700,1000,1500]
# f_read_list = np.arange(7.335, 7.3501, 0.001)
# rudat_list = np.arange(0, 22.1, 1)

# param0.set_rudat(10)
# qt.msleep(60*60*2)
# fid_vs_tread(param0, tt_start=30e-9,  tt_stop=120e-9, tt_step=5e-9, graph=True,  DOWEIGHT = False, label='short,noW')
# fid_vs_tread(param0, tt_start=100e-9, tt_stop=1200e-9, tt_step=50e-9, graph=True,  DOWEIGHT = False, label='long,noW')
# fid_vs_tread(param0, tt_start=30e-9,  tt_stop=120e-9, tt_step=5e-9, graph=True, DOWEIGHT = True,  label='short,WEIG')
# fid_vs_tread(param0, tt_start=100e-9, tt_stop=1200e-9, tt_step=50e-9, graph=True,  DOWEIGHT = True,  label='long,WEIG')

#  param0.freq_read = get_same_ampl_freq_vs_rudat(param0.rudat)  # if want same amplitude |g> and |e> use this

# rudat_vec = [1, 7, 14, 20]
# n_repetitions = 100

# rdt = 20.0
# param0.set_rudat(rdt)
# param0.freq_read = get_same_ampl_freq_vs_rudat(param0.rudat)
# do_traject_measure(param0, t_read_us=300, n_of_files=100, pause=0, title='manual_rdt20_tread300_pause0', do_get_fidelity_check=False,    only_pi=False  )

# #==============================================#
################################################
###--------- FINISH---------------------------------------

stop_time = datetime.datetime.now()
print 'time of measurement', stop_time - start_time
