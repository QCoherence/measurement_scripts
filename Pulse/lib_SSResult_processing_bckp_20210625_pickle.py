'''
This is a library to support processing, analising and plotting the data
form the single-shot qubit readout experiment (with a postselection).


Vladimir Milchakov
vladimir_ph@protonmail.com
'''



import numpy as np

################################################################################
### My Design ###
my_colors_dict = {  'redberry'      :'#970000',
                    'tamarillo'     :'#8b1212',
                    'venetianred'   :'#770023', ## main
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
                    # 'g_state_mark'  :'#2b488a',
                    'e_state_mark'  :'#fe9393',
                    # 'e_state_mark'  :'#a53030',
                    'meduza_dark'   :'#262626',
                    'gauss_green'   :'#bacc5f',
                    'marker_g_dark' :'b',
                    'marker_e_dark' :'#ff0a0a'

}

dark_scheme_old = {     ### FONT ####
                    'font_family'       : 'Verdana',
                    'legend_fontsize'   : 18,
                    'fontsize'          : 18,

                    ### FIGURE ###
                    'fig_face_color'    :my_colors_dict['meduza_dark'] ,
                    'fig_border_color'  :'r',
                    'bg_color'          :'k',

                    ### TITLE ###
                    'title_color'       :my_colors_dict['meduza_gold'],

                    ### LEGEND ###
                    'legend_color'      :my_colors_dict['meduza_dark'],
                    'legend_text_color' :my_colors_dict['meduza_gold'],
                    'legend_frame_color':my_colors_dict['meduza_gold'],
                    'legend_alpha'      :0.7,
                    'legend_fancy'      : True,

                    ### AXES ####
                    'AXES_COLOR'        :my_colors_dict['meduza_gold'],

                    ### GRID ###
                    'grid_color'        :my_colors_dict['meduza_gold'],
                    'grid_transp'        :0.5,


                    ### SCATTERING BLOBS ###
                    'blob_g'            :my_colors_dict['blob_g'],
                    'blob_e'            :my_colors_dict['blob_e'],
                    'blobs_transp'      :40e-2,
                    'blob_prepulse'     :'g',
                    'point_scatter_size':5,
                    'onplot_mark_size'  :10,

                    ### BLOBS CHARACTERIZATION ###
                    'color_g_mean'      :my_colors_dict['marker_g_dark'],
                    'color_e_mean'      :my_colors_dict['marker_e_dark'],
                    'vector_state_lw'   :4,

                    'color_g_cross'     :my_colors_dict['marker_g_dark'],
                    'color_e_cross'     :my_colors_dict['marker_e_dark'],
                    'lw_cross'          :4,
                    'cadr_frame_part'    :0.1,

                    'color_dist'        :my_colors_dict['deus_ex_gold'],
                    'color_g_vector'    :my_colors_dict['deus_ex_gold'],
                    'color_e_vector'    :my_colors_dict['deus_ex_gold'],
                    'vector_bw_blobs'   :4,

                    'color_void'        :my_colors_dict['deus_ex_gold'],
                    'color_zero'        :my_colors_dict['meduza_gold'],
                    'color_zero_vector' :my_colors_dict['meduza_gold'],
                    'vector_zero_lw'    :4,

                    ### HISTOGRAMS ###
                    'hist_thr_color'        : my_colors_dict['deus_ex_gold'],
                    'hist_thr_alpha'        : 0.7,
                    'hist_thr_linewidth'    : 2.0,
                    'hist_thr_linestyle'    : '--',

                    'hist_mean_alpha'       : 0.7,
                    'hist_mean_linewidth'   : 2.0,
                    'hist_mean_linestyle'   : '--',

                    'hist_hist_g_color'     : my_colors_dict['blob_g'],
                    'hist_hist_e_color'     : my_colors_dict['blob_e'],
                    'hist_hist_g_pre_color' : 'b',
                    'hist_hist_e_pre_color' : 'r',
                    'hist_hist_g_sel_color' : 'b',
                    'hist_hist_e_sel_color' : 'r',

                    'hist_hist_lw'          : 1,

                    'hist_fit_g_color'      : my_colors_dict['g_state_mark'],
                    'hist_fit_e_color'      : my_colors_dict['e_state_mark'],
                    'hist_fit_lw'           : 1,
                    'hist_fit_single_alpha' : 0.3,
                    'hist_fit_second_alpha' : 0.3,
                    'hist_fit_double_alpha' : 0.3,

                    'hist_shade_g_color'    : my_colors_dict['blob_g'],
                    'hist_shade_e_color'    : my_colors_dict['blob_e'],
                    'hist_shade_transp'     : 0.08,
}

dark_scheme = {     ### FONT ####
                    'font_family'       : 'Verdana',
                    'legend_fontsize'   : 12,
                    'fontsize'          : 18,

                    ### FIGURE ###
                    # 'fig_face_color'    :my_colors_dict['meduza_dark'] ,
                    'fig_face_color'    :'k' ,
                    'fig_border_color'  :'r',
                    'bg_color'          :'k',

                    ### TITLE ###
                    'title_color'       :my_colors_dict['deus_ex_gold'],

                    ### LEGEND ###
                    'legend_color'      :my_colors_dict['meduza_dark'],
                    'legend_text_color' :my_colors_dict['deus_ex_gold'],
                    'legend_frame_color':my_colors_dict['deus_ex_gold'],
                    'legend_alpha'      :0.7,
                    'legend_fancy'      : True,

                    ### AXES ####
                    'AXES_COLOR'        :my_colors_dict['deus_ex_gold'],

                    ### GRID ###
                    'grid_color'        :my_colors_dict['deus_ex_gold'],
                    'grid_transp'        :0.5,


                    ### SCATTERING BLOBS ###
                    'blob_g'            :my_colors_dict['blob_g'],
                    'blob_e'            :my_colors_dict['blob_e'],
                    'blobs_transp'      :30e-2,
                    'blob_prepulse'     :'g',
                    'point_scatter_size':5,
                    'onplot_mark_size'  :1,

                    ### BLOBS CHARACTERIZATION ###
                    'color_g_mean'      :my_colors_dict['marker_g_dark'],
                    'color_e_mean'      :my_colors_dict['marker_e_dark'],
                    'vector_state_lw'   :4,

                    'color_g_cross'     :my_colors_dict['marker_g_dark'],
                    'color_e_cross'     :my_colors_dict['marker_e_dark'],
                    'lw_cross'          :4,
                    'cadr_frame_part'    :0.1,

                    'color_dist'        :my_colors_dict['deus_ex_gold'],
                    'color_g_vector'    :my_colors_dict['deus_ex_gold'],
                    'color_e_vector'    :my_colors_dict['deus_ex_gold'],
                    'vector_bw_blobs'   :4,

                    'color_void'        :my_colors_dict['deus_ex_gold'],
                    'color_zero'        :my_colors_dict['deus_ex_gold'],
                    'color_zero_vector' :my_colors_dict['deus_ex_gold'],
                    'vector_zero_lw'    :4,

                    ### HISTOGRAMS ###
                    'hist_thr_color'        : my_colors_dict['deus_ex_gold'],
                    'hist_thr_alpha'        : 0.7,
                    'hist_thr_linewidth'    : 2.0,
                    'hist_thr_linestyle'    : '--',

                    'hist_mean_alpha'       : 0.7,
                    'hist_mean_linewidth'   : 2.0,
                    'hist_mean_linestyle'   : '--',

                    'hist_hist_g_color'     : my_colors_dict['blob_g'],
                    'hist_hist_e_color'     : my_colors_dict['blob_e'],
                    'hist_hist_g_pre_color' : 'b',
                    'hist_hist_e_pre_color' : 'b',
                    'hist_hist_g_sel_color' : 'b',
                    'hist_hist_e_sel_color' : 'r',

                    'hist_hist_lw'          : 3,

                    'hist_fit_g_color'      : my_colors_dict['g_state_mark'],
                    'hist_fit_e_color'      : my_colors_dict['e_state_mark'],
                    'hist_fit_lw'           : 2,
                    'hist_fit_single_alpha' : 0.3,
                    'hist_fit_second_alpha' : 0.3,
                    'hist_fit_double_alpha' : 0.3,

                    'hist_shade_g_color'    : my_colors_dict['blob_g'],
                    'hist_shade_e_color'    : my_colors_dict['blob_e'],
                    'hist_shade_transp'     : 0.15,
}

bright_scheme = {   ### FONT ###
                    'font_family'       : 'DejaVu Sans',
                    'legend_fontsize'   : 16,
                    'fontsize'          : 18,

                    ### FIGURE ###
                    'fig_face_color'    :'white' ,
                    'fig_border_color'  :'r',
                    'bg_color'          :'white',

                    ### TITLE ###
                    'title_color'       :'k',

                    ### LEGEND ###
                    'legend_color'      :'white',
                    'legend_text_color' :'k',
                    'legend_frame_color':'k',
                    'legend_alpha'      : 0.7,
                    'legend_fancy'      : True,

                    ### AXES ####
                    'AXES_COLOR'        :'k',

                    ### GRID ###
                    'grid_color'        :'k',
                    'grid_transp'       :0.5,

                    ### SCATTERING BLOBS ###
                    'blob_g'            :my_colors_dict['blob_g'],
                    'blob_e'            :my_colors_dict['blob_e'],
                    'blobs_transp'      :100e-2,
                    'blob_prepulse'     :'g',
                    'point_scatter_size':1,
                    'onplot_mark_size'  :10,

                    ### BLOBS CHARACTERIZATION ###
                    'color_g_mean'      :my_colors_dict['g_state_mark'],
                    'color_e_mean'      :my_colors_dict['e_state_mark'],
                    'vector_state_lw'   :1,

                    'color_g_cross'     :'k',
                    'color_e_cross'     :'k',
                    'lw_cross'          :1,
                    'cadr_frame_part'    :0.1,

                    'color_dist'        :'k',
                    'color_g_vector'    :'k',
                    'color_e_vector'    :'k',
                    'vector_bw_blobs'   :1,

                    'color_void'        :'k',
                    'color_zero'        :'k',
                    'color_zero_vector' :'k',
                    'vector_zero_lw'    :1,

                    ### HISTOGRAMS ###
                    'hist_thr_color'        : 'grey',
                    'hist_thr_alpha'        : 0.7,
                    'hist_thr_linewidth'    : 2.0,
                    'hist_thr_linestyle'    : '--',

                    'hist_mean_alpha'       : 0.7,
                    'hist_mean_linewidth'   : 2.0,
                    'hist_mean_linestyle'   : '--',

                    'hist_hist_g_color'     : my_colors_dict['blob_g'],
                    'hist_hist_e_color'     : my_colors_dict['blob_e'],
                    'hist_hist_g_pre_color' : 'b',
                    'hist_hist_e_pre_color' : 'r',
                    'hist_hist_g_sel_color' : 'b',
                    'hist_hist_e_sel_color' : 'r',

                    'hist_hist_lw'          : 1,

                    'hist_fit_g_color'      : my_colors_dict['g_state_mark'],
                    'hist_fit_e_color'      : my_colors_dict['e_state_mark'],
                    'hist_fit_lw'           : 1,
                    'hist_fit_single_alpha' : 0.3,
                    'hist_fit_second_alpha' : 0.3,
                    'hist_fit_double_alpha' : 0.3,

                    'hist_shade_g_color'    : my_colors_dict['blob_g'],
                    'hist_shade_e_color'    : my_colors_dict['blob_e'],
                    'hist_shade_transp'     : 0.08,

}




def set_font(filename='Forza-Book.ttf'):
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

    str_adress_name = "fonts/ttf/" + filename

    fpath = os.path.join(rcParams["datapath"], str_adress_name)
    prop = fm.FontProperties(fname=fpath)
    # fname = os.path.split(fpath)[1]

    return prop

################################################################################

################################################################################
### This needs only for fit the hists (maybe future) ###
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

def where_sameside(a_arr, b, ref=0):
    '''
    a_arr = array, b =value_to_compare_with, and ref = reference value
    Returns array of booleans:
    True - on positions where value of both arrays have same side to ref
    False where side is different
    '''
    result_array = np.zeros(len(a_arr))
    for i in range(len(a_arr)):
        result_array[i] = sameside(a_arr[i] ,b, ref=ref)

    return result_array

### Function to put in library as math-function
def crop_data_in_window(x,y, window = [None,None]):
    '''
    This function return only the points which is inside given window
    window is a list = [min_x, max_x]

    '''
    if window is None:
        return [x,y]

    ## check window
    if type(window)!=type([1,2,3])  or  len(window)!=2:
        print 'Error crop_window() - wrong parameter crop_window was given'
        return False

    min_x = window[0]
    max_x = window[1]

    # check values of window
    if min_x is not None   and   max_x is not None:
        if min_x > max_x:
            print 'Error crop_window() - max_x is smaller than min_x'
            return False

    if min_x is not None:
        ind = np.where( min_x > x )
        x = np.delete(x, ind)
        y = np.delete(y, ind)

    if max_x is not None:
        ind = np.where( x > max_x )
        x = np.delete(x, ind)
        y = np.delete(y, ind)

    return [x, y]


################################################################################

################################################################################
### __________math functions__________ ###
### __for work with 2D scattering__ ###
def my_stround(num, digits=3, withminus=False,toright=False):
    '''
    Takes float. Return string. With given number of digits.
    '''
    digits = abs(int(digits))
    dig_remain = digits

    ## check inf
    if num == float('inf'):
        return 'inf'
    if np.isnan(num):
        return 'NaN'


    ### work with first char
    if num >= 0:
        if withminus:
            minus = ' '
            dig_remain = dig_remain -1
        else:
            minus = ''
    else:
        minus = '-'
        dig_remain = dig_remain -1

    num = abs(num)

    ### separate two parts
    left_part = int(num)

    right_part = num - left_part

    dig_remain = dig_remain - len(str(left_part))

    if dig_remain < 1:
        string = minus + str(left_part)
    elif dig_remain ==1:
        if toright:
            string = ' ' + minus + str(left_part)
        else:
             string = minus + str(left_part) + ' '
    else:
        right_part = round(right_part, dig_remain-1)
        string = minus + str( left_part + right_part  )

    if len(string) < digits:
        for i in range(  digits-len(string)  ):
            string = string + '0'

    return string

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

def change_basis_point(x,y, x0, y0, theta):
    '''
    Change the basis of one point.
    takes coordinates of one point and bassis as [x0,y0, theta(grad)]
    return coordinatees in a new basis
    First shift, than rotate. Save shift as if shift was after rotation
    '''
    ### shift the point
    x1 = x -x0
    y1 = y -y0
    #convert theta to radians
    theta = np.radians(theta)
    ### rotate the vector clockwise
    x2 =  x1*np.cos(theta) + y1*np.sin(theta)
    y2 = -x1*np.sin(theta) + y1*np.cos(theta)
    ########

    return [x2,y2]

def change_basis_blobs_inf(x0, y0, theta, *args_datapairs):
    '''
    change basis of all sequence
    takes x0,y0 and theta of a new basis
    AND  few of ndarrays of points in shape [x0_arr, y0_arr], [x1_arr, y1_arr], ...[xn_arr, yn_arr]
    returns few of ndarrays of points in New Basis in shape of list of lists of arrays: [  [x0_arr, y0_arr], [...], ... [xn_arr, yn_arr] ]
    (theta in degrees)
    '''
    result_list = []

    for data_pair in args_datapairs:
        data_x = data_pair[0]
        data_y = data_pair[1]
        if len(data_x) != len(data_y):
            print '___WARNING change_basis_blobs_inf() not the same length of arrays!'

        #for each given sequence - do the basis changing
        data_x_norm = np.ones_like(data_x)  #prepare empty array
        data_y_norm = np.ones_like(data_y)

        # for i in range(len(re_g)):
        for i in range(len(data_x)):
            [ data_x_norm[i], data_y_norm[i] ] = change_basis_point(data_x[i], data_y[i], x0, y0, theta)    #g state

        data_norm = [data_x_norm, data_y_norm]
        result_list.append(data_norm)   #add sequence in a new basis to the list

    return result_list

def centers_two_blobs(re_g, im_g, re_e, im_e):
    '''
    Searching the centers of two blobs on i-q plane
    Takes ndarrays of Re_g, Im_g, Re_e, Im_e
    return coordinates of center list = [c_re_g, c_im_g, c_re_e, c_im_e]
    '''
    c_re_g = np.mean(re_g)
    c_im_g = np.mean(im_g)
    c_re_e = np.mean(re_e)
    c_im_e = np.mean(im_e)

    return [c_re_g, c_im_g, c_re_e, c_im_e ]

def crop_fluctuations(re_g, im_g, re_e, im_e, void_re, void_im, zero_include=True, coeff_shift = 2.0, crop=True):
    '''
    takes re_g, im_g, re_e, im_e data
    finds the main area
    returns values of limits [leftlim, rightlim, toplim, bottomlim]
    coeff_shift - how many std-values shift from mean-value
    '''
    if crop:
        ## for X axis
        re_g_m = np.mean(re_g)     #mean value of g
        re_g_d = np.std(re_g)       #dispersion value of g
        re_e_m = np.mean(re_e)
        re_e_d = np.std(re_e)
        ## for Y axis
        im_g_m = np.mean(im_g)     #mean value of g
        im_g_d = np.std(im_g)       #dispersion value of g
        im_e_m = np.mean(im_e)
        im_e_d = np.std(im_e)
        ### possible X(re) limits
        re1 = re_g_m + re_g_d * coeff_shift
        re2 = re_g_m - re_g_d * coeff_shift
        re3 = re_e_m + re_e_d * coeff_shift
        re4 = re_e_m - re_e_d * coeff_shift
        ### possible Y(im) limits
        im1 = im_g_m + im_g_d * coeff_shift
        im2 = im_g_m - im_g_d * coeff_shift
        im3 = im_e_m + im_e_d * coeff_shift
        im4 = im_e_m - im_e_d * coeff_shift

        leftlim = np.min([ re1,re2,re3,re4])
        rightlim = np.max([ re1,re2,re3,re4])
        toplim = np.max([ im1,im2,im3,im4])
        bottomlim = np.min([ im1,im2,im3,im4 ])

        if zero_include:
            leftlim = np.min([ leftlim, 0, void_re])
            rightlim = np.max([ rightlim, 0, void_re ])
            toplim = np.max([ toplim, 0, void_im ])
            bottomlim = np.min([ bottomlim, 0, void_im ])
    else:
        ## comparing arrays
        leftlim = np.min([ re_e, re_g ])
        rightlim = np.max([ re_e, re_g ])
        toplim = np.max([ im_e, im_g])
        bottomlim = np.min([ im_e, im_g])

        ### comparing floats
        if zero_include:
            leftlim = np.min([ leftlim, 0 ])
            rightlim = np.max([ rightlim, 0 ])
            toplim = np.max([ toplim, 0 ])
            bottomlim = np.min([ bottomlim, 0 ])

    return [leftlim, rightlim, toplim, bottomlim]

### __for histograms__ ###
def array_extender(arr, percent=0):
    '''
    Made for symmetrically extend an np.array
    coef - integer. Equal to pair of elements to add
    if coef=0 - no extension
    '''
    if np.isnan(percent) or np.isinf(percent):
        return arr

    coef = len(arr)*percent/100.0
    coef = int(coef)

    step  = arr[1] -arr[0]
    res = np.arange(arr[0] -step*coef,  arr[-1] +step+step*coef,  step)
    return res

def nbins_autoset(arr1, arr2 ,SIGMAS=1.6, NBINS_IN_NOTABLE_AREA = 64):
    '''
    ####         | notable area  |                  ####
    ####---------&%%$%*&---&^%%$%$------------------####
    Takes TWO arrays of data (for e and g states)
    Calculation reasonable number of bins,
    taking into account that interesting data is only a part of all sequences
    Function uses crop_fluctuations()

    Improvements: extend it to kwargs** for any number of arrays
    '''

    ### take edges of st.deviation
    [leftlim, rightlim, rubbish,rubbish]           = crop_fluctuations(arr1, 0, arr2, 0, 0, 0, zero_include=False, coeff_shift=SIGMAS)
    domain_notable = abs(rightlim - leftlim)
    ### take edges the really minimum and maximum
    [leftlim_edge, rightlim_edge, rubbish,rubbish] = crop_fluctuations(arr1, 0, arr2, 0, 0, 0, crop=False, zero_include=False)
    domain_all = abs(rightlim_edge - leftlim_edge)

    part_notable = domain_all / domain_notable    ### calculate how much is a notable part comparing to all domain
    nbins = int(part_notable * NBINS_IN_NOTABLE_AREA)

    return nbins

### __for calculate fidelity__ ###
def get_count_states(x_g, x_e, threshold):
    '''
    Function to count number of values according to threshold
    Returns dictionary
    n_left_g = number elements x_g less than threshold
    n_left_e = number elements x_e less than threshold
    n_right_g = number elements x_g more than threshold
    n_right_e = number elements x_e more than threshold
    p_left_g -probabilities
    p_left_e
    p_right_g
    p_right_e
    sign_ge - +1 if g less than e; or -1 if g more than e
    p_ge = P to measure e when g was prepared
    '''
    def e_morethan_g(p_left_g, p_left_e, p_right_g, p_right_e):
        '''
        Function for define where is g state and where is e state relative to the threshold
        Takes probabilities of g and e states to be on the left and right parts
        Returns True if |e> > |g>, and False if |g> > |e>
        '''
        if (p_left_g > p_right_g) and (p_left_e < p_right_e):
            return True
        elif (p_left_g < p_right_g) and (p_left_e > p_right_e):
            return False
        elif (p_left_g > p_right_g) and (p_left_e > p_right_e):
            if p_left_g > p_left_e:
                return True
            else:
                return False
        elif (p_left_g < p_right_g) and (p_left_e < p_right_e):
            if p_left_g > p_left_e:
                return True
            else:
                return False

    if ( len(x_g) <1 ) or ( len(x_e) <1 ):
            print 'error get_count_states. No data'
            return None

    #calculate how many g points are less or more than threshold value
    n_left_g  = 0
    n_right_g = 0
    for val in x_g:
        if val < threshold:
            n_left_g  +=1
        else:
            n_right_g +=1
    #calculate how many e points are less or more than threshold value
    n_left_e  = 0
    n_right_e = 0
    for val in x_e:
        if val < threshold:
            n_left_e  +=1
        else:
            n_right_e +=1
    #probabilities of g or e states been bigger or smaller than threshold
    #### DO YOU REALLY NEED PROBABILITIES NOW?

    p_left_g = 1.0*n_left_g / len(x_g)
    p_left_e = 1.0*n_left_e / len(x_e)
    p_right_g = 1.0*n_right_g / len(x_g)
    p_right_e = 1.0*n_right_e / len(x_e)


    ### sign ###
    # check where is e and where is g. Define P_ij
    if e_morethan_g(p_left_g, p_left_e, p_right_g, p_right_e):
        sign = +1
        p_gg = p_left_g
        p_ee = p_right_e
        p_ge = p_right_g  # P to measure e when g was prepared
        p_eg = p_left_e # P to measure g when e was prepared
    else:
        sign = -1
        p_gg = p_right_g
        p_ee = p_left_e
        p_ge = p_left_g # P to measure e when g was prepared
        p_eg = p_right_e # P to measure g when e was prepared

    dict_count = {
    'n_left_g'  :   n_left_g,
    'n_left_e'  :   n_left_e,
    'n_right_g' :   n_right_g,
    'n_right_e' :   n_right_e,
    'p_left_g'  :   p_left_g,
    'p_left_e'  :   p_left_e,
    'p_right_g' :   p_right_g,
    'p_right_e' :   p_right_e,
    'sign_ge'   :   sign,
    'p_gg'      :   p_gg,
    'p_ee'      :   p_ee,
    'p_ge'      :   p_ge,   # P to measure e when g was prepared
    'p_eg'      :   p_eg,   # P to measure g when e was prepared
    }

    return dict_count

def calculate_fidelity_Remy(re_g, im_g, re_e, im_e, re_g_post, im_g_post, re_e_post, im_e_post):
    '''
    Super old function of fidelity calculation
    Takes arrays of raw data
    Returns dict_fidelity
    Calculate fidelity, P(e|g), P(g|e) etc
    Takes arrays of data (re-im) with and without postselection
    returns dictionary with different fidelities
    '''
    Re = re_g
    Im = im_g
    Re_pi = re_e
    Im_pi = im_e
    ### ----
    Re_post = re_g_post
    Im_post = im_g_post
    Re_pi_post = re_e_post
    Im_pi_post = im_e_post

    # C1 and C2 are sequences of complex numbers. one for measured e, one for g. No results of prepulses
    C1 = Re + 1j*Im
    C2 = Re_pi +1j*Im_pi
    theta = -np.angle(np.mean(C1)-np.mean(C2))
    #rotating of the axis - projection the blobs on Re axis
    Re = np.real(C1*np.exp(1j*theta))       # this one for G-state
    Im = np.imag(C1*np.exp(1j*theta))
    Re_pi = np.real(C2*np.exp(1j*theta))    # this one for E-state
    Im_pi = np.imag(C2*np.exp(1j*theta))

    #complex number - same for prepulses. FOR POSTSELECTED data
    C1_post = Re_post + 1j*Im_post
    C2_post = Re_pi_post +1j*Im_pi_post
    #rotating of the axis - projection the blobs on Re axis
    Re_post = np.real(C1_post*np.exp(1j*theta))
    Im_post = np.imag(C1_post*np.exp(1j*theta))
    Re_pi_post = np.real(C2_post*np.exp(1j*theta))
    Im_pi_post = np.imag(C2_post*np.exp(1j*theta))

    re_hist = np.histogram(Re, bins=100,normed=1, density=1)
    re_pi_hist = np.histogram(Re_pi, bins=100, normed=1, density=1)
    im_hist = np.histogram(Im, bins=100, normed=1,density=1)
    im_pi_hist = np.histogram(Im_pi, bins=100,normed=1, density=1)

    re_hist_post = np.histogram(Re_post, bins=100,normed=1, density=1)
    re_pi_hist_post = np.histogram(Re_pi_post, bins=100, normed=1, density=1)
    im_hist_post = np.histogram(Im_post, bins=100, normed=1,density=1)
    im_pi_hist_post = np.histogram(Im_pi_post, bins=100,normed=1, density=1)

    threshold = 0e-3 # here signal is following imag part
    ind1 = np.where(Re_post > threshold)
    ind2 = np.where(Re_pi_post > threshold)

    Re_postselected = np.delete(Re, ind1)
    Re_pi_postselected = np.delete(Re_pi, ind2)
    Im_postselected = np.delete(Im, ind1)
    Im_pi_postselected = np.delete(Im_pi, ind2)

    re_hist_postselected = np.histogram(Re_postselected, bins=100,normed=1, density=1)
    re_pi_hist_postselected = np.histogram(Re_pi_postselected, bins=100, normed=1, density=1)
    im_hist_postselected = np.histogram(Im_postselected, bins=100, normed=1,density=1)
    im_pi_hist_postselected = np.histogram(Im_pi_postselected, bins=100,normed=1, density=1)

    # distance calculation
    distance_blobs = np.sqrt( (np.mean(re_e)-np.mean(re_g))**2 + (np.mean(im_e)-np.mean(im_g))**2 )     #LIQUIDATE IT! !V V !
    d = np.mean(Re)- np.mean(Re_pi)     # same as distance_blobs  redefined

    m_im = np.mean(Im)
    m_im_pi =  np.mean(Im_pi)
    m_re = np.mean(Re)
    m_re_pi =  np.mean(Re_pi)
    std_re = np.std(Re)         #! what we need for quantum efficiency
    std_re_pi = np.std(Re_pi)   #!what we need for quantum efficiency
    std_im = np.std(Im)
    std_im_pi = np.std(Im_pi)

    import fit
    s_re_g = fit.Gaussian()
    s_re_g.set_data(re_hist[1][:-1],re_hist[0])
    p0 = [0, 60e3, m_re, std_re]
    p = s_re_g.fit(p0, fixed=[0])
    re_g_th = s_re_g.func(p)

    s_re_pi_g = fit.Gaussian()
    s_re_pi_g.set_data(re_pi_hist[1][:-1],re_pi_hist[0])
    p0 = [0, 60e3, m_re_pi, std_re_pi]
    p_pi = s_re_pi_g.fit(p0, fixed=[0])
    re_pi_g_th = s_re_pi_g.func(p_pi)

    s_re_dg = fit.DoubleGaussian()
    s_re_dg.set_data(re_hist[1][:-1],re_hist[0])
    p0 = np.hstack((p, [0, p_pi[2], p_pi[3]]))

    p_dg = s_re_dg.fit(p0, fixed=[0])
    re_dg_th = s_re_dg.func(p_dg)

    s_re_pi_dg = fit.DoubleGaussian()
    s_re_pi_dg.set_data(re_pi_hist[1][:-1],re_pi_hist[0])
    p0 = np.hstack((p_pi, [0, p[2], p[3]]))

    p_pi_dg = s_re_pi_dg.fit(p0, fixed=[0])
    re_pi_dg_th = s_re_pi_dg.func(p_pi_dg)

    s = fit.DoubleGaussian()
    # !V Warning error float to integer! (np.linspace)!!!
    vec = np.linspace(np.min( (Re, Re_pi, Im, Im_pi)), np.max((Re, Re_pi, Im, Im_pi)), 1e3 )

    s.set_data(vec, vec)

    re_gfdg = s.func( p_dg)# [:4])
    re_pi_gfdg = s.func(p_pi_dg)#[:4])
    ind = np.argwhere(np.diff(np.sign(re_gfdg - re_pi_gfdg)) != 0)

    s_re_dg_postselected = fit.DoubleGaussian()
    s_re_dg_postselected.set_data(re_hist_postselected[1][:-1],re_hist_postselected[0])
    p0 = np.hstack((p, [0, p_pi[2], p_pi[3]]))
    p_dg = s_re_dg_postselected.fit(p0, fixed=[0])
    re_dg_th_postselected = s_re_dg_postselected.func(p_dg)
    s_re_pi_dg_postselected = fit.DoubleGaussian()
    s_re_pi_dg_postselected.set_data(re_pi_hist_postselected[1][:-1],re_pi_hist_postselected[0])
    p0 = np.hstack((p_pi, [0, p[2], p[3]]))
    p_pi_dg = s_re_pi_dg_postselected.fit(p0, fixed=[0])
    re_pi_dg_th_postselected = s_re_pi_dg_postselected.func(p_pi_dg)

    s = fit.DoubleGaussian()
    vec = np.linspace(np.min( (Re, Re_pi, Im, Im_pi)), np.max((Re, Re_pi, Im, Im_pi)), 1e3 )
    s.set_data(vec, vec)
    re_gfdg_postselected = s.func( p_dg)# [:4])
    re_pi_gfdg_postselected = s.func(p_pi_dg)#[:4])
    s = fit.Gaussian()
    s.set_data(vec, vec)
    R = s.func(p_dg[:4])
    R_pi = s.func(p_pi_dg[:4])


        # threshold definition (Remy_code)
    ind = np.argwhere(np.diff(np.sign(R - R_pi)) != 0)
    if len(ind) == 1:
        threshold = vec[ind]
        val_threshold = re_gfdg[ind]
        #print 'vec',  vec[ind] #!V
    elif len(ind)>1:
        #print 'vec',  vec[ind] #!V
        threshold0 = vec[ind[0]]
        threshold1 = vec[ind[1]]
        if abs(threshold - threshold0)<0.5e-3:
            threshold = threshold0
            val_threshold = re_gfdg[ind[0]]
        elif abs(threshold - threshold1)<0.5e-3:
            threshold = threshold1
            val_threshold = re_gfdg[ind[1]]

    q_b = 0.
    q_a = 0.
    q_b_G = 0
    q_a_G = 0
    q_b_post = 0.
    q_a_post = 0.
    print 'threshold is: ', threshold
    for j in np.arange(len(vec)):
        if vec[j]<threshold:
            q_b_G += R[j]
        else:
            q_a_G += R[j]
    PG_eg = q_b_G/(q_a_G+q_b_G)

    for j in np.arange(len(re_hist[1][:-1])):
        val = re_hist[1][j]
        if  val < threshold:
            q_b += re_hist[0][j]
        else:
            q_a += re_hist[0][j]
    P_e_g = float( q_b)/(q_a+q_b)

    for j in np.arange(len(re_hist_postselected[1][:-1])):
        val = re_hist_postselected[1][j]
        if  val < threshold:
            q_b_post += re_hist_postselected[0][j]
        else:
            q_a_post += re_hist_postselected[0][j]
    P_e_g_post = float( q_b_post)/(q_a_post+q_b_post)

    q_b_pi_G = 0
    q_a_pi_G = 0
    for j in np.arange(len(vec)):
        if vec[j]<threshold:
            q_b_pi_G += R_pi[j]
        else:
            q_a_pi_G += R_pi[j]

    PG_ge = q_a_pi_G/(q_a_pi_G+q_b_pi_G)

    q_b_pi = 0.
    q_a_pi = 0.
    q_b_pi_post = 0.
    q_a_pi_post = 0.
    for j in np.arange(len(re_pi_hist[1][:-1])):
        val = re_pi_hist[1][j]
        if  val < threshold:
            q_b_pi += re_pi_hist[0][j]
        else:
            q_a_pi += re_pi_hist[0][j]
    P_g_e = float(q_a_pi)/(q_a_pi+q_b_pi)

    for j in np.arange(len(re_pi_hist_postselected[1][:-1])):
        val = re_pi_hist_postselected[1][j]
        if  val < threshold:
            q_b_pi_post += re_pi_hist_postselected[0][j]
        else:
            q_a_pi_post += re_pi_hist_postselected[0][j]

    P_g_e_post = float(q_a_pi_post)/(q_a_pi_post+q_b_pi_post)


    print 'P_e_g: ', P_e_g
    print 'P_g_e: ', P_g_e
    F_RO = 1. - P_e_g - P_g_e
    print '_____F_ro old:',F_RO
    F_RO = 1. - 0.5*(P_e_g + P_g_e)       # !V New way of definition by Remy&Olivier
    print '_____F_ro new:',F_RO
    F_g = 1. - P_e_g
    F_e = 1. - P_g_e
    # F_RO_G = 1. - PG_eg - PG_ge
    F_RO_G = 1. - 0.5*(PG_eg + PG_ge)
    print 'PG_eg: ', PG_eg
    print 'PG_ge: ', PG_ge
    F_g_G = 1. - PG_eg
    F_e_G = 1. - PG_ge
    # F_RO_post = 1. - P_e_g_post - P_g_e_post
    F_RO_post = 1. - 0.5*(P_e_g_post + P_g_e_post)             ##!V exchange by new definition by Remy&Olivier
    F_e_P = 1 - P_g_e_post
    F_g_P = 1 - P_e_g_post
    Err_g = 1 - F_e_P - PG_ge
    Err_e = 1 - F_g_P - PG_eg

    result_dict = {'F':F_RO, 'F_g':F_g, 'F_e':F_e, 'F_post':F_RO_post,
    'F_post_g':F_g_P, 'F_post_e':F_e_P, 'F_gaus':1.-PG_eg-PG_ge, 'F_gaus_eg':1.-PG_eg,
    'F_gaus_ge':1.-PG_ge, 'Err_e':Err_e, 'Err_g':Err_g, 'Dist':distance_blobs}

    return result_dict

def get_NonSingleGauss_error(fited_myHist_x_g, fited_myHist_x_e):
    '''
    Difference between data and Single_Gaussian model
    Takes fited_myHist_objects (look in this lib)  for |g> and |e>
    returns dictionary
    '''
    ### (14 Jan 2020) calculate NonGaussian errors
    ### for g and e ## uses class Histogram (see in this lib)
    def get_nonGaus_err(fited_myHist):
        '''
        Return which part of histogram is out of its fit (fit of SingleGaussians).
        1 - if all data inside normal distributions, 0 if all out
        if multiplied on 100 - than it's error of nonGaussian in percent
        '''
        diff_xy = fited_myHist.hist_xy[0] - fited_myHist.gauss_fit[0]
        total_runs = np.sum(fited_myHist.hist_xy[0])
        part_out_of_fit = np.sum(diff_xy) / total_runs
        return part_out_of_fit

    err_non_gauss_g = get_nonGaus_err( fited_myHist_x_g )
    err_non_gauss_e = get_nonGaus_err( fited_myHist_x_e )
    f_non_gauss_g = 1. - err_non_gauss_g
    f_non_gauss_e = 1. - err_non_gauss_e
    f_non_gauss_tot = 1. - 0.5*(err_non_gauss_g + err_non_gauss_e)

    dict_NonSingleGauss ={
    'err_non_gauss_g'  :   err_non_gauss_g,
    'err_non_gauss_e'  :   err_non_gauss_e,
    'f_non_gauss_g'    :   f_non_gauss_g,
    'f_non_gauss_e'    :   f_non_gauss_e,
    'f_non_gauss_tot'  :   f_non_gauss_tot
    }

    return dict_NonSingleGauss

def get_overlap_error_from_errorfunct_old(gauss_p_g, gauss_p_e, threshold, sign_ge):
    '''
    Function to calculate gaussian overlap errors and fidelity
    returns dictionary with errors_overlap and fidelities
    Arguments: gauss_p_g, gauss_p_e, threshold, sign_ge
    gauss_p_g  - parameters of gaussian fit of |g> - state
    gauss_p_e  - parameters of gaussian fit of |e> - state
    threshold  - threshold value
    sign_ge    - if |g> less than |e> it is [+1]. (otherwise [-1] 0

    Looks like the values are wrong 15 JAn 2020.
    Use better get_overlap_error_discret()
    '''
    import scipy

    def errfunc(x, x_c=0, sig=1.0):
        '''
        modification for standard error-function from scipy
        to integrate gaussian form -infinity to x
        And also to take into account sigma and x_center
        '''
        y = scipy.special.erf( (x - x_c)/sig )
        y = 0.5 + 0.5*y
        return y

    ##################################

    [x_center_g, sigma_g] = [ gauss_p_g[0], gauss_p_g[1] ]
    [x_center_e, sigma_e] = [ gauss_p_e[0], gauss_p_e[1] ]

    if sign_ge == +1:
        error_g = 1.0 -errfunc(threshold, x_c=x_center_g, sig=sigma_g)
        error_e =      errfunc(threshold, x_c=x_center_e, sig=sigma_e)

    elif sign_ge == -1:
        error_g =      errfunc(threshold, x_c=x_center_g, sig=sigma_g)
        error_e = 1.0 -errfunc(threshold, x_c=x_center_e, sig=sigma_e)
    else:
        print 'Error. Something wrong with sign_ge. It must be -1 or +1'
        error_g = 0
        error_e = 0

    f_g_over = 1.0 - error_g
    f_e_over = 1.0 - error_e
    f_over = 1.0 - 0.5*( error_g+ error_e )

    dict_overlap = {
        'err_o_g': error_g,
        'err_o_e': error_e,
        'f_o_g'  : f_g_over,
        'f_o_e'  : f_e_over,
        'f_o'  : f_over
    }

    return dict_overlap

def get_overlap_error_discret(fit_xy_g, fit_xy_e, threshold, sign_ge):
    '''
    In this function we take fitted histograms as discret Gaussian functions
    (arrays of X and Y), and work with this model as it were a real data Histograms
    to calculate the errors of readout, taking into account the threshold value

    (optimisation: this code is almost duplicating the functions:  def get_count_states() )
    '''
    ####------##
    def get_count_probab_to_threshold(gauss_fit, threshold):
        '''
        Takes XY-function of Gaussian of one state
        (hist_xy.gaussian_fit -- list with two arrays)
        and threshold
        to calculate the probabilities of errors due to the Gaussians overlap
        Calculate errors and fidelity in a same way,
        as if it were the real data histograms
        returns.... ???
        '''
        Y = gauss_fit[0]
        X = gauss_fit[1]
        ####___e_state________####
        n_left  = 0
        n_right = 0
        for j in range(len(X)):
            if X[j] < threshold:
                n_left  += Y[j]
            else:
                n_right += Y[j]

        total = n_left + n_right
        p_left =  1.0*n_left  / total
        p_right = 1.0*n_right / total

        return  [p_left, p_right]

    ####------##

    [p_left_g, p_right_g] = get_count_probab_to_threshold(fit_xy_g, threshold)
    [p_left_e, p_right_e] = get_count_probab_to_threshold(fit_xy_e, threshold)

    if   sign_ge == 1:
        p_ge = p_left_e
        p_eg = p_right_g
        p_gg = p_left_g
        p_ee = p_right_e
    elif sign_ge == -1:
        p_ge = p_right_e
        p_eg = p_left_g
        p_gg = p_left_e
        p_ee = p_right_g

    f_o_total = 1. - 0.5*(p_ge + p_eg)
    f_g  = 1. - p_ge    #fid of preparation |g> state
    f_e  = 1. - p_eg

    dict_overlap = {
        'err_o_g': p_ge,
        'err_o_e': p_eg,
        'f_o_g'  : f_g,
        'f_o_e'  : f_e,
        'f_o'    : f_o_total
    }

    return dict_overlap

def max_possible_fid(t_read_time, T1 = 3500.):
    '''
    Calculate maximum possible fidelity for given t_read and T1
    Check it. It's might be wrong! (!V)
    '''
    p_ee = np.exp( -t_read_time/T1)
    p_gg = np.exp( -t_read_time/T1)
    p_eg = 1.0 - p_ee
    p_ge = 1.0 - p_gg
    F = 1.0 - 0.5*( p_ge +p_eg )
    return F


###__second gaussian fit___###
def add_SecondGaussian_fit(Hist_x_g, Hist_x_e, PLOT = False):
    '''
    Takes two Histogram objects (see class Histogram in this library)
    Both histograms must be fitted by SingleGaussians before to consist list "gauss_param"
    return list [Hist_x_g, Hist_x_e], with additional parameters:
    Hist_x_e.gauss2_param
    Hist_x_e.gauss2_fit
    Which are the fit parameters list and fit_curve of second gaussian (population of wrong state)
    '''

    ### Maybe use this function as general one... We have almost the same in  class Histogram
    def fit_gauss(x, y, gauss_par0, fixed=[0,2,3], crop_window=[None,None]):
        '''
        Takes data X, Y, list of expected parameters, and, if necessary list of indexes of parameters to fix
        gauss_par0 = [0-expec_min_y, 1-expec_max_y, 2-expec_center_x, 3-expec_std_x]
        Returns list = [gauss_p, y_gausfit], where gauss_p is a list of parameters of fit, y_gausfit - sequence of fit
        function
        Can be used also for cropped fit (setting crop_window=[mix_x,max_x])
        '''

        import fit
        Gauss_full = fit.Gaussian()
        Gauss_full.set_data(x, y)

        if crop_window is not None:
            x_crop, y_crop = crop_data_in_window(x,y, window = crop_window)
            Gauss_crop = fit.Gaussian()
            Gauss_crop.set_data(x_crop, y_crop)
            gauss_p = Gauss_crop.fit(gauss_par0, fixed=fixed)
        else:
            gauss_p = Gauss_full.fit(gauss_par0, fixed=fixed)

        y_gausfit = Gauss_full.func(gauss_p)

        return [gauss_p, y_gausfit]

    #############################################################
    ###____Check_given_Objects___####
    try:
        ### check that histograms exist
        if None in [Hist_x_g.hist, Hist_x_g.hist_xy, Hist_x_e.hist, Hist_x_e.hist_xy]:
            print 'Histogram object is empty'
            return False
        ### check that histograms were fitted
        if None in [Hist_x_g.gauss_fit, Hist_x_g.gauss_param, Hist_x_e.gauss_fit, Hist_x_e.gauss_param]:
            print 'Histogram were not fitted'
            return False
    except:
        print 'Error of SecondGaussian given Histograms doesent have some of parameters'
        return False

    ###________Main_________####
    X = Hist_x_e.hist_xy[1] ## X vector - same for both histograms [mV]
    diff_y_g = Hist_x_g.hist_xy[0] - Hist_x_g.gauss_fit[0]
    diff_y_e = Hist_x_e.hist_xy[0] - Hist_x_e.gauss_fit[0]

    single_ampl_g = Hist_x_g.gauss_param[3]
    x_center_g = Hist_x_g.gauss_param[0]
    std_g = Hist_x_g.gauss_param[2]
    par_g_main_gauss = [0, single_ampl_g, x_center_g, std_g]

    single_ampl_e = Hist_x_g.gauss_param[3]
    x_center_e = Hist_x_e.gauss_param[0]
    std_e = Hist_x_e.gauss_param[2]
    par_e_main_gauss = [0, single_ampl_e, x_center_e, std_e]

    ### depend of sign_eg, which we cant access here (compare just centers)
    ## cut from -inf to center_which_is_smaller, and from center_which_is_bigger to +inf
    if x_center_e > x_center_g:
        crop_window_g = [x_center_e ,None]
        crop_window_e =[None, x_center_g]
    else:
        crop_window_g = [None ,x_center_e]
        crop_window_e =[x_center_g, None]


    ## fit of |e> state populated when we prepared |g>
    # |G>  ## for G second gaussian we take parameters form fit of E-STATE!
    [gauss_p_ge, y_gausfit_ge] = fit_gauss(X, diff_y_g, par_e_main_gauss, crop_window=crop_window_g)

    ## fit of |g> state populated when we prepared |e>
    # |E>  ## for E second gaussian we take parameters form fit of G-STATE!
    [gauss_p_eg, y_gausfit_eg] = fit_gauss(X, diff_y_e, par_g_main_gauss, crop_window=crop_window_e)

    ### to save
    Hist_x_e.gauss2_param = gauss_p_eg
    Hist_x_e.gauss2_fit   = [y_gausfit_eg, X]

    Hist_x_g.gauss2_param = gauss_p_ge
    Hist_x_g.gauss2_fit   = [y_gausfit_ge, X]


    if PLOT:
        ################################################
        ### output
        plt.figure(figsize=[16,8])
        plt.title('Data minus fit and fit of second')

        plt.plot(X, diff_y_g, drawstyle='steps', label='difference |g>', color='b')
        plt.plot(X, y_gausfit_ge, '--', drawstyle='steps', label='fit |g>', color='purple')
        plt.plot(X, diff_y_e, drawstyle='steps', label='difference |e>', color='r')
        plt.plot(X, y_gausfit_eg, '--', drawstyle='steps', label='fit |e>', color='orange')

        plt.xlim(xlim)
        plt.legend()
        x1 = X
        #########################

        ## to comapare
        par_list_g = ssr.hist_x_g.gauss_param
        [ g_center_v, g_sigma_v, fw_at_06, max_y, min_y ] = par_list_g
        par_list_e = ssr.hist_x_e.gauss_param
        [ e_center_v, e_sigma_v, fw_at_06, max_y, min_y ] = par_list_e
        # Data
        y_g = ssr.hist_x_g.hist_xy[0]
        y_e = ssr.hist_x_e.hist_xy[0]
        x1 = ssr.hist_x_e.hist_xy[1]

        #Data plot
        plt.figure(figsize=[16,8])
        plt.title('Data and fit of BOTH Gaussians')
        plt.plot(x1,y_g, drawstyle='steps', label='data g', color='b')
        plt.plot(x1,y_e, drawstyle='steps', label='data e', color='r')
        # Fit
        y_g_fit = ssr.hist_x_g.gauss_fit[0]
        y_e_fit = ssr.hist_x_e.gauss_fit[0]
        #Fit plot
        x2 = ssr.hist_x_e.gauss_fit[1] ##x1==x2
        plt.plot(x2,y_g_fit, label='fit e', color='purple')
        plt.plot(x2,y_e_fit, label='fit e', color='orange')

        x_center_g = ssr.hist_x_g.gauss_param[0]
        x_center_e = ssr.hist_x_e.gauss_param[0]
        plt.axvline(x = ssr.threshold, color='gray')
        plt.axvline(x = x_center_g, color='b')
        plt.axvline(x = x_center_e, color='r')

        # plt.plot(x1, diff_g, label='difference |g>', color='b')
        plt.plot(x1, y_gausfit_ge, label='fit |g>', color='purple')
        # plt.plot(x1, diff_e, label='difference |e>', color='r')
        plt.plot(x1, y_gausfit_eg, label='fit |e>', color='orange')

        plt.xlim(xlim)
        plt.legend()

        ### remain data: data - SingleGaussian - SecondGaussian "NonDoubleGaussian errors"
        diff_g_remain = ssr.hist_x_g.hist_xy[0] - ssr.hist_x_g.gauss_fit[0] -  y_gausfit_ge
        diff_e_remain = ssr.hist_x_e.hist_xy[0] - ssr.hist_x_e.gauss_fit[0] -  y_gausfit_eg

        sum_g_nonDoubleGauss = np.sum(diff_g_remain)
        plt.figure(figsize=[16,8])
        plt.title('Remain points (not in doubleGaussian)')
        plt.plot(x1,diff_g_remain, color='b', label = str( int(np.sum(diff_g_remain)) ) )
        plt.plot(x1,diff_e_remain, color='r', label = str( int(np.sum(diff_e_remain)) ) )
        plt.xlim(xlim)
        plt.legend()

    return [Hist_x_g, Hist_x_e]

################################################################################

################################################################################
class Histogram:
    '''
    A class to containt histograms and it's fit data

    Parameters:
    hist        - histogram itself = tuple: [val_arr, bins_arr]
    hist_xy     - histogram ramake to len(val) = len(bins) [val_arr, x_arr]
    gauss_fit   - also tuple with [val_arr, x_arr] but for fitted curve
    gauss_param - parameters of fit []  #[ center_v, sigma_v, std_v, max_y, min_y ]

    Method: (function to do the fit of itself with SingleGaussian)
    fit( threshold, crop_sign )
        crop_sign - +1 if you need to take part more than threshold
                    -1 otherwise
    '''
    hist        = None
    hist_xy     = None
    ## single gauss fit
    gauss_fit   = None
    gauss_param = None  #[ center_v, sigma_v, std_v, max_y, min_y ]
    ## second gauss fit (transition errors) Can be added by external function
    gauss2_fit  = None
    gauss2_param= None #same as in root fit lib [y_min,  area,  position,  full width at (exp^(-0.5)=0.607)  ]
    nbins = 0
    #########################################

    def __init__(self, x, nbins=100):
        '''
        takes 1D array of data
        '''
        self.hist = np.histogram(x, bins=nbins)
        self.nbins = nbins

        def hist_tuple_to_xy_func(h_tuple):
            '''
            plt.hist automaticly return a tuple (values_array, coordinate_array)
            and they have different lenghtes bacouse of this:   .-.-.-.   :(3 lines, 4 points)
            this function reshape the coordinate array to make possible to match values to cordinates
            ### Thin it out!
            '''
            if h_tuple is None:
                return None
            vals = h_tuple[0]
            cords = h_tuple[1]

            cords_1 = np.zeros_like(cords[:-1])
            for i in range(len(cords_1)):
                cords_1[i] = np.mean([  cords[i], cords[i+1] ])

            return [vals, cords_1]

        self.hist_xy = hist_tuple_to_xy_func(self.hist)

    def fit(self, threshold, crop_sign, do_crop=True):
        '''
        decorator for function fit_gauss
        fit itself by Single Gaussian, setting 'self.gauss_fit' and 'self.gauss_param'
        return True or False
        '''
        def fit_gauss(hist_x_xy, crop_thr=None, crop_sign = +1):
            '''
            Takes histogram-tuple [x, vals]
            fits
            returns histogram-tuple [x, vals_fit] and list of gauss-parameters
            crop_thr: if it is None - than we fit all the data. If it is threshold_value than we do crop
            if crop_sign is positive - than we take points more than threshold
            if crop_sign is negative - than we take points less than threshold
            '''

            def get_only_one_state_histxy(histxy, th=0, sign_ge=+1, state=+1):
                '''
                This function return only the points which is above (below) threshold
                th is threshold value
                sign_ge: {+1 if e>g, -1 otherwise}
                state is:
                for g-state state = -1
                for e-state state = +1
                '''
                x = histxy[1]
                y = histxy[0]

                if sign_ge * state > 0:
                    ind = np.where(x < th)
                elif sign_ge * state < 0:
                    ind = np.where(x > th)
                else:
                    print 'error of input cut_one_state_from_x(). sign_ge and state can be +-1 only'

                x_crop = np.delete(x, ind)
                y_crop = np.delete(y, ind)
                hist_crop = [y_crop, x_crop]

                return hist_crop

            def hwhh_xy(x,y):
                '''
                This function takes x and y sequence
                returns half width at half height
                Works for gaussian type of function (or lorenzian etc.)
                '''
                half_heigh = np.max(y)/2.0
                center_x = x[np.argmax(y)]

                list_x_in = []
                for i in range(len(y)):
                    if y[i] > half_heigh:
                        list_x_in.append(x[i])

                x_max_edge = np.max(list_x_in)
                x_min_edge = np.min(list_x_in)

                hwhh = (x_max_edge - x_min_edge)/2.0

                return hwhh

            #################################################

            ### to crop or not to crop
            if crop_thr is None:
                y = hist_x_xy[0]
                x = hist_x_xy[1]
                x_axis = x
            else:
                if crop_sign == +1:
                    hist_x_xy_crop = get_only_one_state_histxy( hist_x_xy, th=crop_thr, sign_ge=+1, state=crop_sign )
                elif crop_sign == -1:
                    hist_x_xy_crop = get_only_one_state_histxy( hist_x_xy, th=crop_thr, sign_ge=+1, state=crop_sign )
                else:
                    print 'warning in fit_gauss(). crop_sign must be equal to +-1'
                    return None
                y = hist_x_xy_crop[0]
                x = hist_x_xy_crop[1]
                x_axis = hist_x_xy[1]

            if len(x)==0 or len(y)==0:
                print 'empty array'
                return False


            ### make an expectatin
            expec_min_y    = 0
            expec_max_y    = np.max(y)
            expec_center_x = x[np.argmax(y)]
            expec_std_x    = hwhh_xy(x,y)
            gauss_p0 = [expec_min_y, expec_max_y, expec_center_x, expec_std_x]

            ### fit g state by single gaus
            import fit
            gauss = fit.Gaussian()
            gauss.set_data(x, y)
            gauss_p = gauss.fit(gauss_p0, fixed=[0])
            y_gausfit = gauss.func(gauss_p)

            # remake the gaussian again with given parameters, but for all x-axis
            if crop_thr is not None:
                gauss1 = fit.Gaussian()
                gauss1.set_data(x_axis, y)
                y_gausfit = gauss1.func(gauss_p)


            ### here we already know exact centers!
            min_y       = gauss_p[0]
            max_y       = gauss_p[1]
            center_v    = gauss_p[2]
            fw_at_06    = gauss_p[3]

            sigma_v  = fw_at_06/2

            h_x_fit     = [ y_gausfit, x_axis ]
            p_list      = [ center_v, sigma_v, fw_at_06, max_y, min_y ]
            return [h_x_fit, p_list]

        if do_crop:
            fit_gauss_result = fit_gauss( self.hist_xy, crop_thr=threshold, crop_sign=crop_sign )
        else:
            fit_gauss_result = fit_gauss( self.hist_xy)

        if fit_gauss_result is False:
            return False

        [ hist_x_fit, gaus_par_x ] = fit_gauss_result
        self.gauss_fit           = hist_x_fit
        self.gauss_param         = gaus_par_x
        return True


class SSResult:
    '''
    This class is linked with one single-shot measurements.
    Data takes only from file during inizialization.
    Contains re and im parts of measured g and e states and also of two pre-measurements
    '''
    ###---------------------------###
    ###### DATA ######
    ### Raw Data ###
    CONVERT_TOMV=True       #Flag of convertion from [V] to [mV]

    void_re = 0
    void_im = 0
    re_g     = np.array([])
    im_g     = np.array([])
    re_e     = np.array([])
    im_e     = np.array([])
    re_g_pre = np.array([])
    im_g_pre = np.array([])
    re_e_pre = np.array([])
    im_e_pre = np.array([])

    ### Normalised Data ###
    void_x = 0
    void_y = 0
    x_g         = None
    x_e         = None
    x_g_pre     = None
    x_e_pre     = None
    y_g         = None
    y_e         = None
    y_g_pre     = None
    y_e_pre     = None
    ### Save parameters of transformation of data
    THETA = 0       ## angle of rotation to go from re-im to x-y
    SHIFT_X = 0     ## x shift was done after rotation
    SHIFT_Y = 0     ## y shift was done after rotation

    ### Normalised Data after Postselection ###
    x_g_select  = None
    x_e_select  = None
    y_g_select  = None
    y_e_select  = None

    ## Histograms ### (it is all objects of class Histograms)
    hist_x_g         = None
    hist_x_e         = None
    hist_x_g_pre     = None
    hist_x_e_pre     = None
    hist_x_g_select  = None
    hist_x_e_select  = None

    hist_y_g         = None
    hist_y_e         = None
    hist_y_g_pre     = None
    hist_y_e_pre     = None
    hist_y_g_select  = None
    hist_y_e_select  = None

    ###---------------------------###


    ######################################################
    ####  MetaData -----------------##
    ######  ######

    ### Time ###
    datafile = ''
    timestamp = ''

    ### Parameters ###
    paramfile = ''
    # dict_param = {
    # 'freq_read':0, 'power1':0, 't_read':0, 'rudat':0, 'freq_q':0,
    #  'power2':0, 'rudat2':0, 'tpi':0, 'nsigma':0, 'cur':0
    #  }
    dict_param = None
    ################-----------------##
    ######################################################


    ######################################################
    ##### CENTERS, THRESHOLD -----------------##
    ### e-g-State definition ###
    threshold = None
    sign_ge = +1     #COULD BE +-1 depends on e>g or g>e

    ### centers of blobs (in first approximation - np.mean, after taken from gauss fit)
    center_x_g = None
    center_x_e = None
    center_y_g = 0
    center_y_e = 0
    center_x_g_select = None # it is different. I dont know why yet
    center_x_e_select = None
    center_y_g_select = None # it is different. I dont know why yet
    center_y_e_select = None
    sizeblob_x_g = None
    sizeblob_x_e = None
    sizeblob_y_g = None
    sizeblob_y_e = None
    squizingblob_g = None
    squizingblob_e = None
    ### crosses of size of each blolbs
    ## frame_g_reim = [ax,ay,bx,by,cx,cy,dx,dy]
    cross_g_xy = None
    cross_e_xy = None
    cadre_g_xy = None
    cadre_e_xy = None
    '''
    cross = [ax,ay,bx,by,cx,cy,dx,dy]
    cadre = [Ax,Ay,Bx,By,Cx,Cy,Dx,Dy]
                     .c
                     |
                a .--+--. b
                     |
                     .d
       A _____ B
        |     |
        |  +  |
        |_____|
       C       D
    '''


    # ### Back_rotated real centers of blobs, extracted from histograms fits
    center_re_g = None
    center_re_e = None
    center_im_g = None
    center_im_e = None
    ### crosses of size of each blolbs in real raw axes
    ## frame_g_reim = [ax,ay,bx,by,cx,cy,dx,dy]
    cross_g_reim = None
    cross_e_reim = None
    cadre_g_reim = None
    cadre_e_reim = None


    ################-----------------##
    ######################################################

    ######################################################
    ### dimensionless R-axis (like X in [V])#####-------##
    r_g         = None
    r_e         = None
    r_g_pre     = None
    r_e_pre     = None
    r_g_select  = None
    r_e_select  = None

    center_r_g  = None
    center_r_e  = None
    void_r      = None
    void_r      = None
    threshold_r = None
    center_r_g_select = None
    center_r_e_select = None

    ### parameter S = (2/sigma_hist)^2 - 'dimensionless measurement strength'
    S_eff_e = None
    S_eff_g = None
    S_eff_e_selected = None
    S_eff_g_selected = None
    ################-----------------##
    ######################################################


    ######################################################
    ####   Results   ---------------##
    ###  ##########
    ### Count states ###
    dict_count = {
    'n_left_g'  : 0,    'n_left_e'  : 0,
    'n_right_g' : 0,    'n_right_e' : 0,
    'p_left_g'  : 0,    'p_left_e'  : 0,
    'p_right_g' : 0,    'p_right_e' : 0,
    'sign_ge'   : 0,
    'p_gg'      : 0,    'p_ee'      : 0,
    'p_ge'      : 0,    'p_eg'      : 0,
    }
    ### Count states after postselection ###
    dict_count_select = {
    'n_left_g'  : 0,    'n_left_e'  : 0,
    'n_right_g' : 0,    'n_right_e' : 0,
    'p_left_g'  : 0,    'p_left_e'  : 0,
    'p_right_g' : 0,    'p_right_e' : 0,
    'sign_ge'   : 0,
    'p_gg'      : 0,    'p_ee'      : 0,
    'p_ge'      : 0,    'p_eg'      : 0,
    }
    ### Fidelity dictionary ###
    dict_fidelity = None
    ################-----------------##
    ######################################################


    ############################################################################
    ############################################################################
    #### METHODS ###############################################################

    def __init__(self, data=None, datafile=None, paramfile=None, param=None, nbins=None, all_included=True, thr_set_zero=True, shift_to_center=False):

        if not shift_to_center and thr_set_zero:
            print 'thr_set_zero and shift_to_center can not be True simultaniously. '
            print 'WARNING! thr_set_zero was setted as False!'
            thr_set_zero = False

        def get_timestamp(filename):
            '''
            function just to take string of time of measurement from file
            '''
            timestr = ''
            try:
                #opening file
                f = open(filename, "r")
                lines = f.readlines()
                f.close()
            except:
                print 'Error! get_timestamp() can not open the file'
                return None

            timestr = lines[1]
            timestr = timestr[13:-1]

            return timestr

        def get_parameters(filename):
            '''
            Takes file of parameters and extract parameters values. Returns dictionary.
            From file
            '''
            ### opening file
            try:
                f = open(filename, "r")
                lines = f.readlines()
                f.close()
            except:
                print 'Can not read the file'
                return None

            if ( len(lines)== 45 ):      ### new format of parameters file
                print '2nd generation of parameters object'
                par_dict = {'freq_read':0, 'power1':0, 't_read':0, 'rudat':0, 'freq_q':0, 'power2':0, 'rudat2':0, 'tpi':0, 'nsigma':0, 'cur':0}
                NUM_OF_VALUES = 10

                # extract numbers from string one by one
                string = lines[44]
                list_of_values_str = []
                for i in range(NUM_OF_VALUES):
                    ## it is 9 parameters to read
                    cut_end = string.find('\t')
                    str = string[ 0: cut_end ]
                    list_of_values_str.append(float(str))
                    string = string[ cut_end+1 : ]

                #fulfill dictionary and return
                par_dict['freq_read'] = list_of_values_str[0]
                par_dict['power1'] =    list_of_values_str[1]
                par_dict['t_read'] =    list_of_values_str[2]
                par_dict['rudat']  =    list_of_values_str[3]
                par_dict['freq_q'] =    list_of_values_str[4]
                par_dict['power2'] =    list_of_values_str[5]
                par_dict['rudat2'] =    list_of_values_str[6]
                par_dict['tpi']    =    list_of_values_str[7]
                par_dict['nsigma'] =    list_of_values_str[8]
                par_dict['cur']    =    list_of_values_str[9]

                return par_dict


            elif ( len(lines)== 41 ):
                print 'Caution! 1st generation of parameters object'
                par_dict = {'power1':0, 'freq_read':0, 't_read':0, 'rudat':0, 'power2':0, 'freq_q':0, 'tpi':0, 'cur':0, 'nsigma':0, 'rudat2':None}
                NUM_OF_VALUES = 9

                # extract numbers from string one by one
                string = lines[40]
                list_of_values_str = []
                for i in range(NUM_OF_VALUES):
                    ## it is 9 parameters to read
                    cut_end = string.find('\t')
                    str = string[ 0: cut_end ]
                    list_of_values_str.append(float(str))
                    string = string[ cut_end+1 : ]

                #fulfill dictionary and return
                par_dict['power1'] = list_of_values_str[0]
                par_dict['freq_read'] =    list_of_values_str[1]
                par_dict['t_read'] =    list_of_values_str[2]
                par_dict['rudat']  =    list_of_values_str[3]
                par_dict['power2'] =    list_of_values_str[4]
                par_dict['freq_q'] =    list_of_values_str[5]
                par_dict['tpi'] =    list_of_values_str[6]
                par_dict['cur']    =    list_of_values_str[7]
                par_dict['nsigma'] =    list_of_values_str[8]

                return par_dict

            elif ( len(lines)== 49):
                print '3rd generation of parameters object'
                par_dict = {'power1':0, 'freq_read':0, 't_read':0, 'rudat':0, 'power2':0, 'freq_q':0, 'tpi':0, 'cur':0, 'nsigma':0, 'rudat2':None, 'phase1':None}
                NUM_OF_VALUES = 11

                # extract numbers from string one by one
                string = lines[48]
                list_of_values_str = []
                for i in range(NUM_OF_VALUES):
                    ## it is 9 parameters to read
                    cut_end = string.find('\t')
                    str = string[ 0: cut_end ]
                    list_of_values_str.append(float(str))
                    string = string[ cut_end+1 : ]

                #fulfill dictionary and return
                par_dict['freq_read'] = list_of_values_str[0]
                par_dict['power1'] =    list_of_values_str[1]
                par_dict['t_read'] =    list_of_values_str[2]
                par_dict['rudat']  =    list_of_values_str[3]
                par_dict['freq_q'] =    list_of_values_str[4]
                par_dict['power2'] =    list_of_values_str[5]
                par_dict['rudat2'] =    list_of_values_str[6]
                par_dict['tpi']    =    list_of_values_str[7]
                par_dict['nsigma'] =    list_of_values_str[8]
                par_dict['cur']    =    list_of_values_str[9]
                par_dict['phase1']    =    list_of_values_str[10]

                return par_dict

            elif ( len(lines)== 53):
                print '4th generation of parameters object (with t_between)'
                par_dict = {'power1':0, 'freq_read':0, 't_read':0, 't_between':0, 'rudat':0, 'power2':0, 'freq_q':0, 'tpi':0, 'cur':0, 'nsigma':0, 'rudat2':None, 'phase1':None}
                NUM_OF_VALUES = 12

                # extract numbers from string one by one
                string = lines[52]
                list_of_values_str = []
                for i in range(NUM_OF_VALUES):
                    ## it is 9 parameters to read
                    cut_end = string.find('\t')
                    str = string[ 0: cut_end ]
                    list_of_values_str.append(float(str))
                    string = string[ cut_end+1 : ]

                #fulfill dictionary and return
                par_dict['freq_read'] = list_of_values_str[0]
                par_dict['power1'] =    list_of_values_str[1]
                par_dict['t_read'] =    list_of_values_str[2]
                par_dict['t_between'] = list_of_values_str[3]
                par_dict['rudat']  =    list_of_values_str[4]
                par_dict['freq_q'] =    list_of_values_str[5]
                par_dict['power2'] =    list_of_values_str[6]
                par_dict['rudat2'] =    list_of_values_str[7]
                par_dict['tpi']    =    list_of_values_str[8]
                par_dict['nsigma'] =    list_of_values_str[9]
                par_dict['cur']    =    list_of_values_str[10]
                par_dict['phase1']    =    list_of_values_str[11]

                return par_dict



            else:
                print 'Error of loading. Can not recognise the format of parameter file.'
                return None

        def get_paramobject(parameters):
            '''
            Takes file of parameters and extract parameters values. Returns dictionary.
            From object Parameters
            '''
            ### opening file

            # try:
            par_dict = {'freq_read':0, 'power1':0, 't_read':0, 'rudat':0, 'freq_q':0, 'power2':0, 'rudat2':0, 'tpi':0, 'nsigma':0, 'cur':0, 'phase1':0}
            NUM_OF_VALUES = 11

            #fulfill dictionary and return
            try:
                par_dict['freq_read']   = parameters.freq_read
            except:
                print 'cant load freq_read from parameters'
            try:
                par_dict['power1']      = parameters.power1
            except:
                print 'cant load power1 from parameters'
            try:
                par_dict['t_read']      = parameters.t_read
            except:
                print 'cant load t_read from parameters'
            try:
                par_dict['rudat']       = parameters.rudat
            except:
                print 'cant load rudat from parameters'
            try:
                par_dict['freq_q']      = parameters.freq_q
            except:
                print 'cant load freq_q from parameters'
            try:
                par_dict['power2']      = parameters.power2
            except:
                print 'cant load power2 from parameters'
            try:
                par_dict['rudat2']      = parameters.rudat2
            except:
                print 'cant load rudat2 from parameters'
            try:
                par_dict['tpi']         = parameters.tpi
            except:
                print 'cant load tpi from parameters'
            try:
                par_dict['nsigma']      = parameters.nsigma
            except:
                print 'cant load nsigma from parameters'
            try:
                par_dict['cur']         = parameters.current
            except:
                print 'cant load current from parameters'
            try:
                par_dict['phase1']         = parameters.phase1
            except:
                print 'cant load phase1 from parameters'
            try:
                par_dict['t_between']         = parameters.t_between
            except:
                print 'cant load t_between from parameters'

            print 'parameters loaded'

            return par_dict


        ########################################################################
        self.valid = None   ### is object allgood or not
        ###### ZERO ######
        ### Raw Data ###
        self.void_re = 0
        self.void_im = 0
        self.re_g     = np.array([])
        self.im_g     = np.array([])
        self.re_e     = np.array([])
        self.im_e     = np.array([])
        self.re_g_pre = np.array([])
        self.im_g_pre = np.array([])
        self.re_e_pre = np.array([])
        self.im_e_pre = np.array([])

        ### save angle of rotation and shifting the data
        ### to go from raw_basis to normal: use change_basis_point(x,y, SHIFT_X, SHIFT_Y, theta)
        ### to go from normal to raw_basis: use change_basis_point(x,y, -SHIFT_X, -SHIFT_Y, -theta)
        self.THETA = 0
        self.SHIFT_X = 0
        self.SHIFT_Y = 0

        ### Normalised Data ###
        self.void_x = 0
        self.void_y = 0
        self.x_g         = None
        self.x_e         = None
        self.x_g_pre     = None
        self.x_e_pre     = None
        self.y_g         = None
        self.y_e         = None
        self.y_g_p       = None
        self.y_e_pre     = None

        ### Normalised Data after Postselection ###
        self.x_g_select  = None
        self.x_e_select  = None
        self.y_g_select  = None
        self.y_e_select  = None

        ######################################################
        ##### CENTERS, THRESHOLD -----------------##
        ### centers of blobs (in first approximation - np.mean, after taken from gauss fit)
        center_x_g = None
        center_x_e = None
        center_x_g_select = None # it is different. I dont know why yet
        center_x_e_select = None
        sizeblob_x_g = None
        sizeblob_x_e = None
        sizeblob_y_g = None
        sizeblob_y_e = None
        squizingblob_g = None
        squizingblob_e = None
        ### crosses of size of each blolbs
        ## cross_g = [ax,ay,bx,by,cx,cy,dx,dy]
        cross_g_xy = None
        cross_e_xy = None
        cadre_g_xy = None
        cadre_e_xy = None

        # ### for future - need a back rotation #(normalisation)^-1
        center_re_g = None
        center_re_e = None
        center_im_g = None
        center_im_e = None
        ### crosses of size of each blolbs in real raw axes
        ## cross_g = [ax,ay,bx,by,cx,cy,dx,dy]
        cross_g_reim = None
        cross_e_reim = None
        cadre_g_reim = None
        cadre_e_reim = None

        ################-----------------##
        ######################################################

        ### dimensionless R-axis (like X in [V])#####-------##
        self.r_g         = None
        self.r_e         = None
        self.r_g_pre     = None
        self.r_e_pre     = None
        self.r_g_select  = None
        self.r_e_select  = None

        self.center_r_g  = None
        self.center_r_e  = None
        self.void_r      = None
        self.void_r      = None
        self.threshold_r = None

        ## Histograms ### (it is all objects of class Histograms)
        self.hist_x_g         = None
        self.hist_x_e         = None
        self.hist_x_g_pre     = None
        self.hist_x_e_pre     = None
        self.hist_x_g_select  = None
        self.hist_x_e_select  = None

        self.hist_y_g         = None
        self.hist_y_e         = None
        self.hist_y_g_pre     = None
        self.hist_y_e_pre     = None
        self.hist_y_g_select  = None
        self.hist_y_e_select  = None

        self.dict_fidelity = {
        'F'         : 0,
        'F_g'       : 0,
        'F_e'       : 0,
        'F_post'    : 0,
        'F_post_g'  : 0,
        'F_post_e'  : 0,
        'F_gaus'    : 0,
        'F_gaus_eg' : 0,
        'F_gaus_ge' : 0,

        'F_gaus_dscrt'    : 0,
        'F_gaus_eg_dscrt' : 0,
        'F_gaus_ge_dscrt' : 0,
        'F_gaus_aka_remy'    : 0,
        'F_gaus_eg_remy' : 0,
        'F_gaus_ge_remy' : 0,

        'Err_e'     : 0,
        'Err_g'     : 0
        }

        self.dict_count_select = {
        'n_left_g'  : 0,    'n_left_e'  : 0,
        'n_right_g' : 0,    'n_right_e' : 0,
        'p_left_g'  : 0,    'p_left_e'  : 0,
        'p_right_g' : 0,    'p_right_e' : 0,
        'sign_ge'   : 0,
        'p_gg'      : 0,    'p_ee'      : 0,
        'p_ge'      : 0,    'p_eg'      : 0,
        }

        self.dict_count_select = {
        'n_left_g'  : 0,    'n_left_e'  : 0,
        'n_right_g' : 0,    'n_right_e' : 0,
        'p_left_g'  : 0,    'p_left_e'  : 0,
        'p_right_g' : 0,    'p_right_e' : 0,
        'sign_ge'   : 0,
        'p_gg'      : 0,    'p_ee'      : 0,
        'p_ge'      : 0,    'p_eg'      : 0,
        }

        ##############################################

        ### set up metadata
        self.datafile = datafile
        self.paramfile = paramfile
        if datafile is not None:
            self.timestamp = get_timestamp(datafile)

        ##############################################
        ##############################################

        ### set up data measurement
        if datafile is not None:
            self.load_data(datafile)
        elif data is not None:
            self.take_data(data)
        else:
            print 'To load the data you should either give a datafile=... either data= list of numpy.arrays'
            print 'Error of loading data SSResult'

        ### set up parameters
        if paramfile is not None:
            self.dict_param = get_parameters(paramfile)
        elif param is not None:
            self.dict_param = get_paramobject(param)
        else:
            self.dict_param = None
            print 'warning: no parameters is attached to SSResult object'

        ##############################################
        ### ALL THE PROCESSING IS HERE ####
        ##############################################
        if all_included:
            self.valid=True
            ### normalize it
            try:
                ### shift - make histograms symmetrical around zero
                ###
                self.make_norm_data_from_raw(shift=shift_to_center)
            except:
                print '     ___SSResult error during normalisation'
                self.valid=False

            ### find the best threshold and shift the data
            try:
                self.set_best_threshold()
                if thr_set_zero:
                    self.shift_x_to_threshold_be_zero()
            except:
                print '     ___SSResult error during setting threshold'
                self.valid=False

            ### do postselection
            # try:
            if self.make_postselected_data_from_norm() != False:
                ### make histograms
                ## flag - True\False if fit was succeed
                flag1 = self.make_histograms(nbins = nbins)
                flag2 = self.make_histograms_y(nbins = nbins)
                if flag1==False or flag2==False:
                    print 'fit was not ok. Possibly data is creepy'
                    self.valid = False
                    return
            ### make crosses for plot size of real blob on scattering diagram
                self.make_blob_crosses()
            ### calculate fidelity
                self.calculate_fidelity_post()
            else:
                print 'smth went wrong'
            # except:
            #     self.valid=False
            #     print '     ___SSResult error during postselection or hists'

            ## go from x mV to unitless variable r for S extraction
            try:
                self.make_x_dimensionless()
                self.make_unitless_histograms(nbins = nbins)
            except:
                self.valid=False
                print '     ___SSResult error during making unitless histograms'


        print 'Object is created'
        if not self.valid:
            print 'WARNING! Object is invalid'

    ############################################################################

    ### Process data methods ###
    def get_str_date(self):
        if self.timestamp is not None:
            return self.timestamp[20:24] +'_'+ self.timestamp[4:7]+'_'+self.timestamp[8:10]
        return '_'

    def take_data(self, data):
        '''
        Load data from the measurement
        Takes list of numpy.arrays this shape
        data - must be a list of 1D arrays
        [re_g, im_g, re_e, im_e, re_g_post, im_g_post, re_e_post, im_e_post]
        '''
        try:
            if type(data) is not list:
                print 'SSR Error: data must be a list'
                return False
            if len(data) < 4:
                print 'SSR Error: list of data is too short?'
                return False
            if len(data) > 12:
                print 'SSR Error: list of data is too long?'
                return False

            for datum in data:
                if type(datum) is not np.ndarray:
                    print 'data should be a np.array'
                    return False
        except:
            print 'error during checking!'
            print 'Error SSResult take_data()'
            return False

        try:
            ### switch from [Volts] to [mV] if it is aksed
            if self.CONVERT_TOMV == True:
                coef = 1000.0
            else:
                coef = 1.0

            ### [re_g, im_g, re_e, im_e, re_g_post, im_g_post, re_e_post, im_e_post]
            self.re_g     = coef * data[0]
            self.im_g     = coef * data[1]
            self.re_e     = coef * data[2]
            self.im_e     = coef * data[3]
            self.re_g_pre = coef * data[4]
            self.im_g_pre = coef * data[5]
            self.re_e_pre = coef * data[6]
            self.im_e_pre = coef * data[7]
            return True

        except:
            print 'some error of SSResult.take_data()'
            return False

    def load_data(self, datafile):
        '''
        function open file and create data sequences
        '''
        def datatype(file):
            '''
            recognize type of datafile. Work for SingleShot files only
            '''
            try:
                f = open(file, "r")
                lines = f.readlines()
                f.close()
            except:
                print 'Error datatype() - can not open file'
                return 'error'

            if (lines[4]  == '#\tname: Real \n') and (lines[9] == '#\tname: Real-pi\n') and (lines[14] == '#\tname: Imag \n') and (lines[18] == '#\tname: Imag-pi \n'):
                return 'type1' ### old type
            elif (lines[4] == '#\tname: re_g\n') and (lines[7] == '#\tname: im_g\n') and (lines[10] == '#\tname: re_e\n') and (lines[13] == '#\tname: im_e\n'):
                return 'type2' ### new type
            else:
                return 'error'

        try:
            datatype = datatype(datafile)

            if self.CONVERT_TOMV == True:
                coef = 1000.0
            else:
                coef = 1.0

            if datatype == 'type2': ##new data
                raw_data_ss = np.loadtxt(datafile)
                self.re_g     = coef * raw_data_ss[:,0]
                self.im_g     = coef * raw_data_ss[:,1]
                self.re_e     = coef * raw_data_ss[:,2]
                self.im_e     = coef * raw_data_ss[:,3]
                self.re_g_pre = coef * raw_data_ss[:,4]
                self.im_g_pre = coef * raw_data_ss[:,5]
                self.re_e_pre = coef * raw_data_ss[:,6]
                self.im_e_pre = coef * raw_data_ss[:,7]
                print 'data loaded'
                return True
            elif  datatype == 'type1':   ##old data
                raw_data_ss = np.loadtxt(datafile)
                self.re_e     = coef * raw_data_ss[:,0]
                self.re_g     = coef * raw_data_ss[:,1]
                self.im_e     = coef * raw_data_ss[:,2]
                self.im_g     = coef * raw_data_ss[:,3]
                self.re_e_pre = coef * raw_data_ss[:,4]
                self.re_g_pre = coef * raw_data_ss[:,5]
                self.im_e_pre = coef * raw_data_ss[:,6]
                self.im_g_pre = coef * raw_data_ss[:,7]

                print 'data loaded'
                return True
            else:
                print 'ERROR! Can not recognize data type'
                return False

        except:
            print 'Warning load_data() error!'
            print 'can not load file: ', datafile
            return False

    def make_norm_data_from_raw(self, shift=True):
        '''
        Make a normalisation of data on the axis between g_mean and e_mean values
        Write new data as object parameters
        Also make histograms of normalised data
        Returns True if finished
        '''
        ### check if it is data. if not - try to load from file
        if (self.re_g is not None) and (self.im_g is not None) and (self.re_e is not None) and (self.im_e is not None):
            re_g = self.re_g
            im_g = self.im_g
            re_e = self.re_e
            im_e = self.im_e
        else:
            print 'It is no raw data. \n loading...'
            success_load = self.load_data(self.datafile)
            if not success_load:
                print 'load was not successful. Sheck datafile'
                return False
            re_g = self.re_g
            im_g = self.im_g
            re_e = self.re_e
            im_e = self.im_e

        ### ----
        if self.re_g_pre is not None:
            re_g_pre = self.re_g_pre
        if self.im_g_pre is not None:
            im_g_pre = self.im_g_pre
        if self.re_e_pre is not None:
            re_e_pre = self.re_e_pre
        if self.im_e_pre is not None:
            im_e_pre = self.im_e_pre

        ##########______DEFINITION_THE_BASIS________############################
        ### find centers of blobs
        [c_re_g, c_im_g, c_re_e, c_im_e ] = centers_two_blobs(re_g, im_g, re_e, im_e)

        ### find angle 2*alpha (angle between two blolbs according to void-state)
        # angle_between_blobs = angle_three_points(c_re_g,c_im_g, self.void_re,self.void_im, c_re_e,c_im_e)
        ### this should be saved to object?

        ### find distance and theta between this centers
        [dist, theta] = complex_num_relationships(c_re_g,c_im_g,c_re_e,c_im_e)      #extract theta
        if shift:
            threshold_re = np.mean([c_re_g, c_re_e])  #x0
            threshold_im = np.mean([c_im_g, c_im_e])  #y0
        else:
            threshold_re = 0.0
            threshold_im = 0.0

        ######____CHANGING_BASIS_____________####################################
        ### change the basis according to positions of blobs centers
        [ [re_g, im_g], [re_e, im_e] ]                      = change_basis_blobs_inf(threshold_re, threshold_im, theta, [re_g, im_g] , [re_e, im_e] )
        [ [re_g_pre, im_g_pre],  [re_e_pre, im_e_pre] ]     = change_basis_blobs_inf(threshold_re, threshold_im, theta, [re_g_pre, im_g_pre] , [re_e_pre, im_e_pre] )
        # normalize VOID state
        [void_re,void_im]   = change_basis_point(self.void_re, self.void_im, threshold_re, threshold_im, theta)
        ### Calculate shift after rotation
        [x00, y00]          = change_basis_point(0,0, threshold_re,threshold_im, theta)

        ########_____SAVING____________#########################################
        self.THETA   = self.THETA + theta
        self.SHIFT_X = self.SHIFT_X -x00
        self.SHIFT_Y = self.SHIFT_Y -y00
        self.void_x      = void_re
        self.void_y      = void_im
        self.x_g            = re_g
        self.x_e            = re_e
        self.x_g_pre        = re_g_pre
        self.x_e_pre        = re_e_pre
        self.y_g            = im_g
        self.y_e            = im_e
        self.y_g_pre        = im_g_pre
        self.y_e_pre        = im_e_pre

        ### new centers:
        [c_x_g, c_y_g, c_x_e, c_y_e ] = centers_two_blobs(self.x_g, self.y_g, self.x_e, self.y_e)

        self.center_x_g = c_x_g
        self.center_x_e = c_x_e
        print 'new center of blobs: ', self.center_x_g, ' ', self.center_x_e

        print 'data was normalised and saved'
        return True

    def set_best_threshold(self):
        '''
        Find best threshold,
        set it t oobject
        also calculate set self.dict_count values
        returns True if all good
        '''
        ###---
        def get_best_threshold(x_g, x_e, th0, delta0, permiss=1e-4, fragment=40, previous_fid=None):
            '''
            Searching for best value of threshold
            Bruteforce method
            permiss - permissiable value
            '''
            def get_fro_vs_threshold(x_g, x_e, threshold):
                '''
                Simplest function to calculate only f_ro for given threshold value
                Calculate fidelity for given value of THRESHOLD
                Takes 1D arrays of normalized g and e results. ( re_g & re_e )
                return only value of f_ro = 1. - 0.5*(p_ge + p_eg)
                '''
                dict_count = get_count_states(x_g,x_e,threshold)
                if dict_count is not None:
                    p_ge = dict_count['p_ge']
                    p_eg = dict_count['p_eg']
                    f_ro = 1. - 0.5*(p_ge + p_eg)
                    return f_ro
                else:
                    return 0

            # th_min = th0-delta0
            # th_max = th0+delta0
            # step = (th_max - th_min)/fragment
            # thresholds = np.arange(th_min, th_max, step)
            #
            thresholds = np.linspace(th0-delta0, th0+delta0, fragment)


            fids_list = []
            for th in thresholds:
                fid = get_fro_vs_threshold(x_g, x_e, th)
                fids_list.append(fid)

            arg_best = np.argmax(fids_list)
            best_th  = thresholds[ arg_best ]

            if (arg_best > 0):
                left_th  = thresholds[ arg_best -1 ]
            else:
                left_th  = best_th

            if (arg_best < len(thresholds)-1):
                right_th = thresholds[ arg_best +1 ]
            else:
                right_th = best_th

            best_fid  = get_fro_vs_threshold(x_g, x_e, best_th)
            left_fid  = get_fro_vs_threshold(x_g, x_e, left_th)
            right_fid = get_fro_vs_threshold(x_g, x_e, right_th)

            if previous_fid is not None:
                if abs(previous_fid - best_fid) < permiss:
                    return best_th

            # print 'arg best:', arg_best
            # print 'best fidelity: ', best_fid

            if abs(best_fid - left_fid) > permiss  or  abs(best_fid - right_fid) > permiss:
                # recursion here
                # print 'ONE MORE ITTERATION'
                best_th = get_best_threshold(x_g, x_e, best_th, delta0/10, permiss=permiss, previous_fid=best_fid)
            return best_th
        ###---
        ##########______NORMALIZE IF NECESSARY_____#############################
        if (self.x_g is None) or (self.x_e is None):
            success_norm = self.make_norm_data_from_raw()
            if not success_norm:
                print 'can not normalise. error of setting threshold'
                return False

        ##########______THRESHOLD_____##########################################
        ### Find best threshold value ###
        [leftlim, rightlim, rabbish1, rabbish2 ] = crop_fluctuations(self.x_g, [0] , self.x_e, [0], 0, 0 )
        delta = abs(rightlim - leftlim)

        threshold = get_best_threshold(self.x_g, self.x_e, 0, delta, permiss=1e-4)
        # print 'threshold:', threshold

        ##########______SET AND RETURN_____#####################################
        self.threshold = threshold
        self.dict_count = get_count_states(self.x_g,self.x_e, self.threshold)
        self.sign_ge = self.dict_count['sign_ge']

        print 'threshold set'
        return True

    def shift_x_to_threshold_be_zero(self):
        '''
        Search the best threshold value and shift the data on it
        returns threshold value, that was founded and used for shift
        '''
        if (self.x_g is None) or (self.x_e is None):
            success_norm = self.make_norm_data_from_raw()
            success_th = self.set_best_threshold()      #if we load new norm data - we need to redefine a threshold
            if (not success_norm) or (not success_th):
                print 'can not normalise or set threshold. error of shift_x_to_threshold_be_zero'
                return False

        if self.threshold is None:
            success_th = self.set_best_threshold()
            if not success_th:
                print 'can not set threshold. error of shift_x_to_threshold_be_zero'
                return False

        if self.threshold == 0:
            print 'Threshold is already zero'
            return True

        ###  NOW SHIFT THE NORMALIZED DATA FOR THRESHOLD TO BE ZERO ###

        threshold = self.threshold

        def shifter(arr, value):
            '''
            This function just shift a given array on given value
            '''
            new_arr = np.zeros_like(arr)
            for i in range(len(arr)):
                new_arr[i] = arr[i] - value
            return new_arr

        self.x_g = shifter(self.x_g, threshold)
        self.x_e = shifter(self.x_e, threshold)

        if self.x_g_pre is not None:
            self.x_g_pre = shifter(self.x_g_pre, threshold)
        if self.x_e_pre is not None:
            self.x_e_pre = shifter(self.x_e_pre, threshold)

        if self.x_g_select is not None:
            self.x_g_select = shifter(self.x_g_select, threshold)
        if self.x_e_select is not None:
            self.x_e_select = shifter(self.x_e_select, threshold)

        [self.void_x] = shifter([self.void_x], threshold)

        ### ( !V why is it commented 191023 )
        ### ( !V uncommented 191110 works same)
        # ### shift the center of blobs also
        if self.center_x_g is not None:
            [self.center_x_g] = shifter([self.center_x_g], threshold)
        if self.center_x_e is not None:
            [self.center_x_e] = shifter([self.center_x_e], threshold)
        print 'new centers of blobs:', self.center_x_g, self.center_x_e

        ### Kostil: And if the data is shifted we need also to shift histograms if it is exist!
        if (self.hist_x_g is not None) or (self.hist_x_e is not None) or (self.hist_x_g_select is not None)or (self.hist_x_e_select is not None):
            print 'we redo histograms, because of the shift'
            self.make_histograms()

        [self.SHIFT_X] = shifter([self.SHIFT_X], -threshold)

        self.threshold = 0

        print 'x-data shifted on', threshold, '. threshold=0'
        return True

    def make_x_dimensionless(self):
        '''
        Function to switch x from mv to dimensionless parameter
        It is need for calculate measurement strength and quantum efficiency
        https://arxiv.org/abs/1506.08165
        '''
        if self.center_x_g is not None and self.center_x_e is not None:
            c_g = self.center_x_g
            c_e = self.center_x_e
        else:
            print 'cant make dimensionless without centers'

        if c_g == c_e:
            print 'ERROR make_x_dimensionless(): centers have the same value'
            return

        coef = 2/abs( c_g - c_e )
        shift = np.mean([c_g,c_e])

        ###----###
        ### make arrays elements unitless
        self.r_g        = (self.x_g - shift ) * coef
        self.r_e        = (self.x_e - shift ) * coef
        self.r_g_pre    = (self.x_g_pre - shift ) * coef
        self.r_e_pre    = (self.x_e_pre - shift ) * coef
        self.r_g_select = (self.x_g_select - shift ) * coef
        self.r_e_select = (self.x_e_select - shift ) * coef

        self.center_r_g = (self.center_x_g - shift ) * coef
        self.center_r_e = (self.center_x_e - shift ) * coef
        self.center_r_g_select = (self.center_x_g_select - shift ) * coef
        self.center_r_e_select = (self.center_x_e_select - shift ) * coef
        self.void_r     = (self.void_x - shift ) * coef
        self.threshold_r= (self.threshold - shift ) * coef

        return

    def make_postselected_data_from_norm(self):
        '''
        Do the postselection. Threshold usually=0 because we did set_best_threshold_as_zero() before
        also calculate and set dict_count_select
        '''
        if self.threshold is None:
            success_th = self.set_best_threshold()
            if not success_th:
                print 'threshold have not been defined yet'
                return False
        threshold = self.threshold

        if (self.x_g is None) or (self.x_e is None) or (self.x_g_pre is None) or (self.x_e_pre is None):
            success_norm = self.make_norm_data_from_raw()
            success_th = self.set_best_threshold()      #if we load new norm data - we need to redefine a threshold
            if (not success_norm) or (not success_th):
                print 'can not Postselect. error of normalisation or setting threshold'
                return False

        if ( len(self.x_g) != len(self.x_g_pre) ) or ( len(self.x_e) != len(self.x_e_pre) ):
            print 'ERROR make_postselected_data_from_norm(): Size of x_g,x_e,x_g_pre,x_e_pre is not the same  '
            return False

        ### ~~~~~~~~~~~~~~~~~~~~~~~~ ###

        ## Selected data gonna be there
        x_g_selected = np.array([])
        x_e_selected = np.array([])
        y_g_selected = np.array([])
        y_e_selected = np.array([])

        ## Save also data wich we discard (if you need to analize it as well)
        x_g_discarded = np.array([])
        x_e_discarded = np.array([])
        y_g_discarded = np.array([])
        y_e_discarded = np.array([])

        def g_state(val, threshold, sign_ge):
            '''
            small function takes value on x-axes (normalized), threshold value and sign
            return true if value is belongs to |g>-state and False if belongs to |e>.
            '''
            if sign_ge > 0:
                if val > threshold:
                    return False
                else:
                    return True
            else:
                if val > threshold:
                    return True
                else:
                    return False

        ## Working on data with prepared |g>
        for i in range(len(self.x_g)):
            if g_state(self.x_g_pre[i], self.threshold, self.sign_ge):
                x_g_selected = np.append(x_g_selected, self.x_g[i])
                y_g_selected = np.append(y_g_selected, self.y_g[i])
            else:
                x_g_discarded = np.append(x_g_discarded, self.x_g[i])
                y_g_discarded = np.append(y_g_discarded, self.y_g[i])

        ## Working on data with prepared |e>
        for i in range(len(self.x_e)):
            if g_state(self.x_e_pre[i], self.threshold, self.sign_ge):
                x_e_selected = np.append(x_e_selected, self.x_e[i])
                y_e_selected = np.append(y_e_selected, self.y_e[i])
            else:
                x_e_discarded = np.append(x_e_discarded, self.x_e[i])
                y_e_discarded = np.append(y_e_discarded, self.y_e[i])

        #####____SAVE_SELECTED_DATA___######
        self.x_g_select = x_g_selected
        self.x_e_select = x_e_selected
        self.y_g_select = y_g_selected
        self.y_e_select = y_e_selected

        self.x_g_discarded = x_g_discarded
        self.x_e_discarded = x_e_discarded
        self.y_g_discarded = y_g_discarded
        self.y_e_discarded = y_e_discarded

        print '-- before selection --', len(self.x_g)
        print '-- selected --', len(self.x_g_select)
        discarded = len(self.x_g) - len(self.x_g_select)
        print '-- discarded [%] --', 100.0*( 1.0*discarded / len(self.x_g) )

        self.dict_count_select = get_count_states(self.x_g_select, self.x_e_select, self.threshold)
        if self.dict_count_select is None:
            return False

        # return [index_g_wrong, index_e_wrong]  ### could be usefull for delete exact points from raw data also
        ### if you wanna do it -- do it right here, in this function
        ## RIGHT HERE ##

        print 'postselection done'
        return True

    def make_histograms(self, nbins=None):
        '''
        This function in charge of histograms
        of fit the gauss and so on
        return True or False
        '''
        ########################################################################
        ### if no data - load it
        if self.x_g is None or self.x_e is None:
            success_norm = self.make_norm_data_from_raw()
            success_th = self.set_best_threshold()      #if we load new norm data - we need to redefine a threshold
            if (not success_norm) or (not success_th):
                print 'can not normalise or set threshold. error of make_histograms()'
                return False

        ### if no threshold - find one
        if self.threshold is None:
            success_th = self.set_best_threshold()
            if not success_th:
                print 'can not set threshold. error of make_histograms()'
                return False

        ### take only a part for fit
        g_crop_s = -self.sign_ge
        e_crop_s =  self.sign_ge

        ### autoset nbins if not defind ###
        if nbins is None:
            nbins = nbins_autoset(self.x_g, self.x_e)

        ### make preliminary hist to take nbins
        self.hist_x_g = Histogram(self.x_g, nbins = nbins)
        # nbins = self.hist_x_g.hist[1] ##take exact sequence of bins
        nbins = array_extender(self.hist_x_g.hist[1], percent=20 ) ##take exact sequence of bins
        #### !V

        ### making hists and fit for x_g & x_e ###
        self.hist_x_g = Histogram(self.x_g, nbins = nbins)
        self.hist_x_e = Histogram(self.x_e, nbins = nbins)


        ### Fit by single gaussian
        crop_line_for_g =  crop_line_for_e =  self.threshold
        flag1 = self.hist_x_g.fit(crop_line_for_g, g_crop_s)
        flag2 = self.hist_x_e.fit(crop_line_for_e, e_crop_s)
        if flag1==False or flag2==False:
            print 'Error of fiting histograms'
            return False

        ### Fit by single gaussian again (with more precise crops) ## crop_line = center_gauss +- 2sigma_gaussian
        crop_line_for_g =  self.hist_x_g.gauss_param[0] - g_crop_s*self.hist_x_g.gauss_param[2]
        crop_line_for_e =  self.hist_x_e.gauss_param[0] - e_crop_s*self.hist_x_e.gauss_param[2]
        flag1 = self.hist_x_g.fit(crop_line_for_g, g_crop_s)
        flag2 = self.hist_x_e.fit(crop_line_for_e, e_crop_s)
        if flag1==False or flag2==False:
            print 'Error of fiting histograms'
            return False
        print 'Histograms x fited second time'

        ### Fit by second gaussian to see the transitions (DoubleGaussian model)
        [self.hist_x_g, self.hist_x_e] = add_SecondGaussian_fit(self.hist_x_g, self.hist_x_e)

        #####__Extract_values_from_hists__#####
        ### set a new center
        self.center_x_g = self.hist_x_g.gauss_param[0]
        self.center_x_e = self.hist_x_e.gauss_param[0]
        self.sizeblob_x_g = 2*self.hist_x_g.gauss_param[2]
        self.sizeblob_x_e = 2*self.hist_x_e.gauss_param[2]

        ### rotate this center to raw data scale
        [self.center_re_g, self.center_im_g] = change_basis_point(self.center_x_g, self.center_y_g, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)
        [self.center_re_e, self.center_im_e] = change_basis_point(self.center_x_e, self.center_y_e, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)


        #####__Make_hists_for_pre_read__#######
        ### making hists and fit for x_g_pre & x_e_pre ###
        if self.x_g_pre is not None:
            self.hist_x_g_pre = Histogram(self.x_g_pre, nbins = nbins)
        if self.x_e_pre is not None:
            self.hist_x_e_pre = Histogram(self.x_e_pre, nbins = nbins)

        ### making hists and fit for x_g_selected & x_e_selected ###
        if self.x_g_select is not None:
            self.hist_x_g_select = Histogram(self.x_g_select, nbins = nbins)
            self.hist_x_g_select.fit(self.threshold, g_crop_s)
            ### reset a new center
            self.center_x_g_select = self.hist_x_g_select.gauss_param[0]
        if self.x_e_select is not None:
            self.hist_x_e_select = Histogram(self.x_e_select, nbins = nbins)
            self.hist_x_e_select.fit(self.threshold, e_crop_s)
            ### reset a new center
            self.center_x_e_select = self.hist_x_e_select.gauss_param[0]

        ### finish ###
        print 'histograms are made'
        return True

    def make_histograms_y(self, nbins=100):
        ### if no data - load it
        if self.y_g is None or self.y_e is None:
            success_norm = self.make_norm_data_from_raw()
            success_th = self.set_best_threshold()      #if we load new norm data - we need to redefine a threshold
            if (not success_norm) or (not success_th):
                print 'can not normalise or set threshold. error of make_histograms()'
                return False

        # g_crop_s = -self.sign_ge
        # e_crop_s =  self.sign_ge ##here it is meaningless

        if nbins is None:
            nbins = nbins_autoset(self.y_g, self.y_e)

        ### make preliminary hists to take nbins
        self.hist_y_g = Histogram(self.y_g, nbins = nbins)
        # nbins = self.hist_y_g.hist[1] ##take exact sequence of bins
        nbins = array_extender(self.hist_y_g.hist[1], percent=100 ) ##take exact sequence of bins

        ### making hists and fit for x_g & x_e ###
        self.hist_y_g = Histogram(self.y_g, nbins = nbins)
        flag1 = self.hist_y_g.fit(0,0,do_crop=False)
        self.hist_y_e = Histogram(self.y_e, nbins = nbins)
        flag2 = self.hist_y_e.fit(0,0,do_crop=False)

        if flag1==False or flag2==False:
            print 'Error of fiting y histograms'
            return False

        ### set a new center
        self.center_y_g = self.hist_y_g.gauss_param[0]
        self.center_y_e = self.hist_y_e.gauss_param[0]
        self.sizeblob_y_g = 2*self.hist_y_g.gauss_param[2]
        self.sizeblob_y_e = 2*self.hist_y_e.gauss_param[2]

        ## !V
        ### rotate this center to raw data scale
        [self.center_re_g, self.center_im_g] = change_basis_point(self.center_x_g, self.center_y_g, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)
        [self.center_re_e, self.center_im_e] = change_basis_point(self.center_x_e, self.center_y_e, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)

        ### making hists and fit for x_g_pre & x_e_pre ###
        if self.y_g_pre is not None:
            self.hist_y_g_pre = Histogram(self.y_g_pre, nbins = nbins)
        if self.y_e_pre is not None:
            self.hist_y_e_pre = Histogram(self.y_e_pre, nbins = nbins)


        ### make points for rectangle around blobs and rotate its coordinates
        ## example from make_hists()
        # [self.center_re_g, self.center_im_g] = change_basis_point(self.center_x_g,0, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)
        # [self.center_re_e, self.center_im_e] = change_basis_point(self.center_x_e,0, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)

        print 'Y-histograms are maden'
        return True

    def make_unitless_histograms(self, nbins=100):
        '''
        This function in charge of histograms
        of fit the gauss and plot it (remove this part)
        '''
        ########################################################################

        ### if no data - load it
        if (self.r_g is None) or (self.r_e is None) or (self.threshold_r is None):
            print 'can not plot unitless hists'
            return False

        g_crop_s = -self.sign_ge
        e_crop_s =  self.sign_ge

        if nbins is None:
            nbins = nbins_autoset(self.r_g, self.r_e)

        ### make preliminary hist to take nbins
        self.hist_r_g = Histogram(self.r_g, nbins = nbins)
        # nbins = self.hist_r_g.hist[1] ##take exact sequence of bins
        nbins = array_extender(self.hist_r_g.hist[1], percent=20 ) ##take exact sequence of bins

        ### making hists and fit for r_g & r_e ###
        self.hist_r_g = Histogram(self.r_g, nbins = nbins)
        self.hist_r_g.fit(self.threshold_r, g_crop_s)
        self.hist_r_e = Histogram(self.r_e, nbins = nbins)
        self.hist_r_e.fit(self.threshold_r, e_crop_s)

        # ### set a new center
        # self.center_x_g = self.hist_x_g.gauss_param[0]
        # self.center_x_e = self.hist_x_e.gauss_param[0]

        ### making hists and fit for x_g_pre & x_e_pre ###
        if self.r_g_pre is not None:
            self.hist_r_g_pre = Histogram(self.r_g_pre, nbins = nbins)
        if self.r_e_pre is not None:
            self.hist_r_e_pre = Histogram(self.r_e_pre, nbins = nbins)

        ### making hists and fit for x_g_selected & x_e_selected ###
        if self.r_g_select is not None:
            self.hist_r_g_select = Histogram(self.r_g_select, nbins = nbins)
            self.hist_r_g_select.fit(self.threshold_r, g_crop_s)
            # ### reset a new center
            # self.center_r_g_select = self.hist_x_g_select.gauss_param[0]

        if self.r_e_select is not None:
            self.hist_r_e_select = Histogram(self.r_e_select, nbins = nbins)
            self.hist_r_e_select.fit(self.threshold_r, e_crop_s)
            # ### reset a new center
            # self.center_x_e_select = self.hist_x_e_select.gauss_param[0]

        ### Record dimensionless measurement strength
        sig_e = self.hist_r_e.gauss_param[1]
        sig_g = self.hist_r_g.gauss_param[1]
        S_e = (2/sig_e)**2
        S_g = (2/sig_g)**2
        self.S_eff_e = S_e
        self.S_eff_g = S_g

        ### And for data after postselection
        sig_e_sel = self.hist_r_e_select.gauss_param[1]
        sig_g_sel = self.hist_r_g_select.gauss_param[1]
        S_e_sel = (2/sig_e_sel)**2
        S_g_sel = (2/sig_g_sel)**2
        self.S_eff_e_selected = S_e_sel
        self.S_eff_g_selected = S_g_sel

        ### making hists and fit for x_g_pre & x_e_pre ###
        print 'unitless histograms made'
        return True

    def make_blob_crosses(self):
        '''
        Makes a cross shape points around blob in xy_axes and reim_axes for after plot it
        Also calculate squizingblob_g and squizingblob_e
        For work it's necessary to have
        self.center_x_g
        self.center_y_g
        self.center_x_e
        self.center_y_e

                             .c
                             |
                        a .--+--. b
                             |
                             .d
           A _____ B
            |     |
            |  +  |
            |_____|
           C       D

        '''
        def cross_coordinztes_from_center_and_size(center_x, center_y, size_x, size_y):
            '''
            Function takes x_y_center of rectangle, and its sizes A and B
            And convert it to coordinates of its corners (a,b,c,d): [x,y]
            '''
            ax = center_x - size_x/2
            ay = center_y
            bx = center_x + size_x/2
            by = center_y
            cx = center_x
            cy = center_y + size_y/2
            dx = center_x
            dy =center_y - size_y/2

            return [ax,ay,bx,by,cx,cy,dx,dy]

        def cross_to_cadre(coord_cross):
            '''
            Takes [ax,ay,bx,by,cx,cy,dx,dy]  - cross coordinatees
            Returns [Ax,Ay,Bx,By,Cx,Cy,Dx,Dy]  - rectangle coordinates
                                         .c
                                         |
                                    a .--+--. b
                                         |
                                         .d
                       A _____ B
                        |     |
                        |  +  |
                        |_____|
                       C       D

            '''
            [ax,ay,bx,by,cx,cy,dx,dy] = coord_cross
            Ax = ax
            Ay = cy
            Bx = bx
            By = cy
            Cx = ax
            Cy = dy
            Dx = bx
            Dy = dy
            return [Ax,Ay,Bx,By,Cx,Cy,Dx,Dy]

        def change_basis_cross(cross_list, shift_x, shift_y, theta):
            '''
            Change basis using change_basis_point()
            takes list of shape [x0,y0, x1,y1, x2,y2... xN,yN]
            and return it in new basis
            '''
            if len(cross_list) % 2 != 0:
                print 'Error change_basis_cross() - list must consist even number of elements'
                return np.zeros_like(cross_list)

            result_list_reim = []
            for i in np.arange(0, len(cross_list), 2):
                x = cross_list[i]
                y = cross_list[i+1]
                [re,im] = change_basis_point(x,y, shift_x, shift_y, theta)
                result_list_reim.append(re)
                result_list_reim.append(im)

            return result_list_reim

        ##[ax,ay,bx,by,cx,cy,dx,dy]
        self.cross_g_xy = cross_coordinztes_from_center_and_size(self.center_x_g, self.center_y_g, self.sizeblob_x_g, self.sizeblob_y_g)
        self.cross_e_xy = cross_coordinztes_from_center_and_size(self.center_x_e, self.center_y_e, self.sizeblob_x_e, self.sizeblob_y_e)

        ### calculate cadres (angles) positions
        self.cadre_g_xy = cross_to_cadre(self.cross_g_xy)
        self.cadre_e_xy = cross_to_cadre(self.cross_e_xy)

        try:
            ### set cross to raw basis Re-Im
            ##[aRe,aIm,bRe,bIm,cRe,cIm,dRe,dIm]
            self.cross_g_reim = change_basis_cross(self.cross_g_xy, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)
            self.cross_e_reim = change_basis_cross(self.cross_e_xy, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)
            self.cadre_g_reim = change_basis_cross(self.cadre_g_xy, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)
            self.cadre_e_reim = change_basis_cross(self.cadre_e_xy, -self.SHIFT_X, -self.SHIFT_Y, -self.THETA)
        except:
            print 'Error of setting self.cross_g_reim. Probably SHIFT or THETA didnt set'

        print 'crosses around blobs calculated...'

        try:
            ### calculate squizingblob
            self.squizingblob_g = self.sizeblob_y_g / self.sizeblob_x_g
            self.squizingblob_e = self.sizeblob_y_e / self.sizeblob_x_e
        except:
            print 'Error, squizingblob_g(e) was not calculated'

        return True

    def calculate_fidelity_post(self):
        '''
        New version of fidelity calculator.
        Smart threshold by default (no fit, just bruteforce)
        '''
        ####----------------------------------------####
        ### load dictionary with p_ij raw
        if (self.dict_count['p_gg'] ==0) or (self.dict_count['p_ge'] ==0) or (self.dict_count['p_eg'] ==0) or (self.dict_count['p_ee'] ==0):
            print 'Error of calculate_fidelity_post(): no data in dict_count'
            return None
        ### count states from raw data ###
        p_gg = self.dict_count['p_gg']
        p_ge = self.dict_count['p_ge']
        p_eg = self.dict_count['p_eg']
        p_ee = self.dict_count['p_ee']


        ### load dictionary with p_ij selected
        if (self.dict_count_select['p_gg'] ==0) or (self.dict_count_select['p_ge'] ==0) or (self.dict_count_select['p_eg'] ==0) or (self.dict_count_select['p_ee'] ==0):
            print 'Error of calculate_fidelity_post(): no data in dict_count'
            return None
        ### count states with postselection ###
        p_gg_post = self.dict_count_select['p_gg']
        p_ge_post = self.dict_count_select['p_ge']
        p_eg_post = self.dict_count_select['p_eg']
        p_ee_post = self.dict_count_select['p_ee']
        ####----------------------------------------####

        ####----------------------------------------####
        ### calculate fidelities
        f_ro = 1. - 0.5*(p_ge + p_eg)
        f_g  = 1. - p_ge    #fid of preparation |g> state
        f_e  = 1. - p_eg

        f_ro_post = 1. - 0.5*(p_ge_post + p_eg_post)
        f_g_post  = 1. - p_ge_post
        f_e_post  = 1. - p_eg_post
        ####----------------------------------------####

        ####----------------------------------------####
        ##  calculate gaussian overlap (using so called errorfunction)
        ##  this method gives a wrong result maybe
        if self.hist_x_g_select is not None:
            ## use selected data if possible
            g_gaus_par = self.hist_x_g_select.gauss_param
            e_gaus_par = self.hist_x_e_select.gauss_param
        else:
            g_gaus_par = self.hist_x_g.gauss_param
            e_gaus_par = self.hist_x_e.gauss_param
        dict_overlap = get_overlap_error_from_errorfunct_old(g_gaus_par, e_gaus_par, self.threshold, self.sign_ge)
        # ####----------------------------------------####

        ####----------------------------------------####
        ##  calculate gaussian overlap (discret)
        ##  ( processing the single gaussians, extracted from fit as raw data histograms to calculate fidelity)
        dict_overlap_discret = get_overlap_error_discret(self.hist_x_g.gauss_fit, self.hist_x_e.gauss_fit, self.threshold, self.sign_ge)
        ####----------------------------------------####

        ####----------------------------------------####
        ### (14 Jan 2020) calculate NonGaussian errors
        ### for g and e ## uses class Histogram (see in this lib)
        dict_NonSingleGauss = get_NonSingleGauss_error(self.hist_x_g , self.hist_x_e)
        ####----------------------------------------####

        ####----------------------------------------####
        ### (15 Jan 2020) old Remys way of calculation (All in one, takes RAW DATA)
        dict_fidelity_Remy = calculate_fidelity_Remy(self.re_g, self.im_g, self.re_e, self.im_e, self.re_g_pre, self.im_g_pre, self.re_e_pre, self.im_e_pre)
        ####----------------------------------------####

        ####----------------------------------------####
        #####___SAVING_RESULT____#############
        ### error due to read g when prepare e and vice versa
        self.dict_fidelity['F']                     = f_ro
        self.dict_fidelity['F_g']                   = f_g
        self.dict_fidelity['F_e']                   = f_e
        ### error due to read g when prepare e and vice versa (after postselection)
        self.dict_fidelity['F_post']                = f_ro_post
        self.dict_fidelity['F_post_g']              = f_g_post
        self.dict_fidelity['F_post_e']              = f_e_post
        ### Gaussians overlap error (uses error_function)
        self.dict_fidelity['F_gaus' ]               = dict_overlap['f_o']
        self.dict_fidelity['F_gaus_eg']             = dict_overlap['f_o_e']
        self.dict_fidelity['F_gaus_ge']             = dict_overlap['f_o_g']
        ### Gaussians overlap error (uses discret gaussians analisis)
        self.dict_fidelity['F_gaus_dscrt' ]        = dict_overlap_discret['f_o']
        self.dict_fidelity['F_gaus_eg_dscrt']      = dict_overlap_discret['f_o_e']
        self.dict_fidelity['F_gaus_ge_dscrt']      = dict_overlap_discret['f_o_g']
        ### Gaussians overlap error (from Remy's calculation)
        self.dict_fidelity['F_gaus_aka_remy' ]        = dict_fidelity_Remy['F_gaus']
        self.dict_fidelity['F_gaus_eg_remy']      = dict_fidelity_Remy['F_gaus_eg']
        self.dict_fidelity['F_gaus_ge_remy']      = dict_fidelity_Remy['F_gaus_ge']
        ### !V 14 Jan 2020 Error of data out of single gaussians fit (transition or bad pi-pulse errors)
        self.dict_fidelity['F_non_gauss']          = dict_NonSingleGauss['f_non_gauss_tot']
        self.dict_fidelity['F_non_gauss_g']        = dict_NonSingleGauss['f_non_gauss_g']
        self.dict_fidelity['F_non_gauss_e']        = dict_NonSingleGauss['f_non_gauss_e']
        ### Errors Not_Because_of_Overlap
        # p_ge_overlap = dict_overlap['err_o_g']
        # p_eg_overlap = dict_overlap['err_o_e']
        p_ge_overlap = dict_overlap_discret['err_o_g']
        p_eg_overlap = dict_overlap_discret['err_o_e']
        self.dict_fidelity['Err_e']     = p_ge_post - p_ge_overlap
        self.dict_fidelity['Err_g']     = p_eg_post - p_eg_overlap

        ####----------------------------------------####

        ####----------------------------------------####
        #### Return ###
        print 'Fidelity was calculated'
        # return self.dict_fidelity
        return True
        ####----------------------------------------####

    def erase_data(self, data_to_erase, selfrun=False):
        '''
        Function to get free memory.
        Erase the data of object after calculations was done
        parameter data_to_erase:
            'raw' - delete re_g, re_e, im_g, im_e and pre-selections re,im
            'norm'- delete x_g, x_e, y_g, y_e, and pre-selections x,y
            'pre' - delete only results of pre-pulses: re_g_pre, x_g_pre..
            'select' - delete selectde data
        '''
        if data_to_erase == 'raw':
            self.re_g = None
            self.re_e = None
            self.im_g = None
            self.im_e = None
            self.re_g_pre = None
            self.re_e_pre = None
            self.im_g_pre = None
            self.im_e_pre = None
            if not selfrun:
                print '__Raw data erased!'
        elif data_to_erase == 'norm':
            self.x_g = None
            self.x_e = None
            self.y_g = None
            self.y_e = None
            self.x_g_pre = None
            self.x_e_pre = None
            self.y_g_pre = None
            self.y_e_pre = None
            if not selfrun:
                print '__Normed data erased!'
        elif data_to_erase == 'pre':
            self.re_g_pre = None
            self.re_e_pre = None
            self.im_g_pre = None
            self.im_e_pre = None
            self.x_g_pre = None
            self.x_e_pre = None
            self.y_g_pre = None
            self.y_e_pre = None
            if not selfrun:
                print '__Pre-pulse data erased!'
        elif data_to_erase == 'select':
            x_g_select  = None
            x_e_select  = None
            y_g_select  = None
            y_e_select  = None
            if not selfrun:
                print '__Selected data erased!'
        elif data_to_erase == 'all':
            self.erase_data(data_to_erase='raw',   selfrun=True)
            self.erase_data(data_to_erase='norm',  selfrun=True)
            self.erase_data(data_to_erase='select',selfrun=True)
            print 'All data erased!'
        else:
            print '__Nothing erased. Check the parameter'

        return True

    def plot_scatter_two_blob(self, figsize=[15,10],fig_transp=True,cs=None,dark=True,font=None, show=True, norm=False,centers=None, limits=[None,None,None,None],crop=True, zero_on_plot=True, pre_read=False, selected=False, plot_crosses=False, plot_centers=True, plot_cadres=True, NOLEGEND=False, title_str=None, save=False,savepath='',fname='Two_blob',fileformat='.png'):
        '''
        Plots diagramm of scattering for two blobs on the i-q plane
        returns limits of axis (it is used for histograms)
        if want to set the limits dont forget to make 'crop=False'
        figsize - in inches!
        '''
        from matplotlib import pyplot as plt
        ########################################################################
        ###___________STYLE_________________________________________________####
        ########################################################################

        ### set color_scheme (cs)
        if cs is None:
            if dark:
                cs = dark_scheme
            else:
                cs = bright_scheme

        ### set colors of axes
        import matplotlib as mpl
        mpl.rc('axes', edgecolor=cs['AXES_COLOR'], labelcolor=cs['AXES_COLOR'], grid=True)
        mpl.rc('xtick', color=cs['AXES_COLOR'])
        mpl.rc('ytick', color=cs['AXES_COLOR'])
        mpl.rc('grid', color=cs['grid_color'])

        ###____SET CUSTOM FONT ###
        plt.rc('font', family = cs['font_family'])
        plt.rc('font', size   = cs['fontsize'])
        plt.rc('xtick', labelsize =cs['fontsize'])
        plt.rc('ytick', labelsize =cs['fontsize'])

        ### ##############T ###

        ########################################################################


        if selected:
            if norm:
                void_re = self.void_x
                void_im = self.void_y
                re_g     = self.x_g_select
                im_g     = self.y_g_select
                re_e     = self.x_e_select
                im_e     = self.y_e_select
            else:
                print 'Sorry, but this function does not exist now \n try plot it with norm=True, or with selected=False'
                print 'And dont hesitate to add it also'
        else:
            if norm:
                if (self.x_g is None) or (self.x_e is None):
                    self.make_norm_data_from_raw()    ### do renormalization

                void_re = self.void_x
                void_im = self.void_y
                re_g     = self.x_g
                im_g     = self.y_g
                re_e     = self.x_e
                im_e     = self.y_e
                re_g_p = self.x_g_pre
                im_g_p = self.y_g_pre
                re_e_p = self.x_e_pre
                im_e_p = self.y_e_pre
            else:
                if (self.re_g is None) or (self.im_g is None) or (self.re_e is None) or (self.im_e is None):
                    print 'It is no raw data. \n loading...'
                    success_load = self.load_data(self.datafile)
                    if not success_load:
                        print 'load was not successful'
                        return None

                void_re = self.void_re
                void_im = self.void_im
                re_g     = self.re_g
                im_g     = self.im_g
                re_e     = self.re_e
                im_e     = self.im_e
                re_g_p = self.re_g_pre
                im_g_p = self.im_g_pre
                re_e_p = self.re_e_pre
                im_e_p = self.im_e_pre
                if pre_read:
                    re_g_pre = self.re_g_pre
                    im_g_pre = self.im_g_pre
                    re_e_pre = self.re_e_pre
                    im_e_pre = self.im_e_pre

        ### setting centers
        if centers is not None:
            [c_re_g, c_im_g, c_re_e, c_im_e] = centers  ## given manually
        else:
            if not norm:
                if (self.center_re_g is None) or (self.center_re_e is None) or (self.center_im_g is None) or (self.center_im_e is None):
                    [ self.center_re_g, self.center_im_g, self.center_re_e, self.center_im_e] = centers_two_blobs(re_g, im_g, re_e, im_e)
                [c_re_g, c_im_g, c_re_e, c_im_e ] = [ self.center_re_g, self.center_im_g, self.center_re_e, self.center_im_e ]
            else:
                if (self.center_x_g is not None) and (self.center_x_e is not None):
                    [c_re_g, c_im_g, c_re_e, c_im_e ] = [ self.center_x_g, self.center_y_g, self.center_x_e, self.center_y_e  ]
                else:
                    print 'Error: data is not normalised'

        if save:
            if savepath == '':
                savepath='savings\\'

        str_fidelity = ''
        str_params   = ''
        if self.dict_fidelity is not None:
            str_fidelity = 'F_post:'+my_stround(  100*self.dict_fidelity['F_post'],4 )+'% F:'+my_stround(  100*self.dict_fidelity['F'],4 )+'% F_gaus(d):'+my_stround(  100*self.dict_fidelity['F_gaus_dscrt'],4 )+'%'
        if self.dict_param is not None:
            str_params = 'Rdt:'+ my_stround( self.dict_param['rudat'],4 )+'dB; t_read:'+my_stround( 1e9*self.dict_param['t_read'],3 )+'ns'+' Fr:'+my_stround( self.dict_param['freq_read'],6 )+'Ghz'


        ### find angle 2*alpha (angle between two blolbs according to void-state)
        angle_between_blobs = angle_three_points(c_re_g,c_im_g, void_re,void_im, c_re_e,c_im_e)

        ## SETTING BORDERS ### (now it is outside)
        #############################
        def get_cadre_limits():
            '''
            To find a limits of frame
            '''
            ### Choose what do we want to put on a plot
            if plot_cadres:
                if norm:
                    [frame_g, frame_e] = [self.cadre_g_xy, self.cadre_e_xy]
                else:
                    [frame_g, frame_e] = [self.cadre_g_reim, self.cadre_e_reim]
            elif plot_crosses:
                if norm:
                    [frame_g, frame_e] = [self.cross_g_xy, self.cross_e_xy]
                else:
                    [frame_g, frame_e] = [self.cross_g_reim, self.cross_e_reim]
            else:
                return None

            if None in [frame_g, frame_e]:
                return None
            else:
                [gax,gay,gbx,gby,gcx,gcy,gdx,gdy] = frame_g
                [eax,eay,ebx,eby,ecx,ecy,edx,edy] = frame_e


            leftlim   = np.min([gax, gbx, gcx, gdx, eax, ebx, ecx, edx])
            rightlim  = np.max([gax, gbx, gcx, gdx, eax, ebx, ecx, edx])
            toplim    = np.max([gay, gby, gcy, gdy, eay, eby, ecy, edy])
            bottomlim = np.min([gay, gby, gcy, gdy, eay, eby, ecy, edy])

            cadre_limits = [leftlim, rightlim, toplim, bottomlim ]
            return cadre_limits

        if None in limits:
            if crop:
                [leftlim, rightlim, toplim, bottomlim ] = crop_fluctuations(re_g, im_g ,re_e, im_e, void_re=self.void_re, void_im=self.void_im )
                cadre_lim = get_cadre_limits()  ## the frame to be completly on plot
                if cadre_lim is not None:
                    print 'cadre_lim: ', cadre_lim
                    [cadre_left, cadre_right, cadre_top, cadre_bottom ] = cadre_lim

                    leftlim   = np.min([leftlim,   cadre_left])
                    rightlim  = np.max([rightlim,  cadre_right])
                    toplim    = np.max([toplim,    cadre_top])
                    bottomlim = np.min([bottomlim, cadre_bottom])
            else:
                leftlim   = np.min([  0,   np.min([ re_e, re_g ])  ])
                rightlim  = np.max([  0,   np.max([ re_e, re_g ])  ])
                toplim    = np.max([  0,   np.max([ im_e, im_g ])  ])
                bottomlim = np.min([  0,   np.min([ im_e, im_g ])  ])
            autolimits = [leftlim, rightlim, toplim, bottomlim ]

            for i in range(4):
                if limits[i] is None:
                    limits[i] = autolimits[i]
        else:
            print 'Scatter: use only manual limits'

        [leftlim, rightlim, toplim, bottomlim ] = limits
        print 'limits:', limits

        ##############################

        ### calculation of angle and distance between blolb centers
        [dist, theta] = complex_num_relationships(c_re_g,c_im_g,c_re_e,c_im_e)
        str_blob_place = 'Distance:'+ my_stround(dist,4) + '; Theta' +":" + my_stround(theta,2,withminus=True) + 'deg'
        print str_blob_place

        ### vectors of each states from void signal
        [amp_g, ph_g] = complex_num_relationships(void_re, void_im, c_re_g,c_im_g)
        [amp_e, ph_e] = complex_num_relationships(void_re, void_im, c_re_e,c_im_e)

        str_g_place = 'Amp:'+ my_stround(amp_g,5,withminus=True) + '; Phase:'+ my_stround(ph_g,4,withminus=True)+ 'deg'
        str_e_place = 'Amp:'+ my_stround(amp_e,5,withminus=True) + '; Phase:'+ my_stround(ph_e,4,withminus=True)+ 'deg'
        if (self.squizingblob_g is not None) and (self.squizingblob_e is not None):
            str_g_place = str_g_place + '; sqz:' + my_stround(self.squizingblob_g,4,withminus=False)
            str_e_place = str_e_place + '; sqz:' + my_stround(self.squizingblob_e,4,withminus=False)

        amp_relation = my_stround(amp_e/amp_g,4,withminus=True)
        str_blob_place = str_blob_place + '; Ratio amps: '+ amp_relation
        print str_g_place
        print str_e_place
        print 'Ratio amps: '+ amp_relation

        if figsize is None:
            fig = plt.figure(fname, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'])
        else:
            if (type(figsize) != list):
                print 'figsize must be a lsit'
                return False
            else:
                if len(figsize) != 2:
                    print 'figsize list must contain to numbers (x and y size)'
                    return False
            fig = plt.figure(fname, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'], figsize=(figsize[0],figsize[1]))


        ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
        ax.set_facecolor(cs['bg_color'])

        ### setting axes________________###
        if font is not None:
            plt.axis('equal',fontproperties = font)   #same step X and Y        #square axis automatic
        else:
            plt.axis('equal')

        ### !V new 28 Nov 2019 (191128)
        ### check adequat numbers___##
        list_lim = [leftlim, rightlim, toplim, bottomlim]
        print 'list_lim: ', list_lim
        for i in range(len(list_lim)):
            if np.isnan(list_lim[i]) or np.isnan(list_lim[i]):
                list_lim[i] = None
        [leftlim, rightlim, toplim, bottomlim] = list_lim
        print 'list_lim: ', list_lim
        ###_________________________##

        plt.xlim( left = leftlim, right=rightlim )
        plt.ylim( top =  toplim, bottom=bottomlim )
        #############________________#######

        plt.grid(color=cs['grid_color'], alpha= cs['grid_transp'])

        # if title_str is None or title_str=='':
        #     if font is not None:
        #         plt.title(self.timestamp, color=cs['title_color'], fontproperties = font)
        #     else:
        #         plt.title(self.timestamp, color=cs['title_color'])
        # else:
        #     if font is not None:
        #         plt.title(title_str, color=cs['title_color'], fontproperties = font)
        #     else:
        #         plt.title(title_str, color=cs['title_color'])


        if (title_str is None) or (title_str==''):
            title_str = self.timestamp

        if font is not None:
            plt.title(title_str, color=cs['title_color'], fontproperties = font)
        else:
            plt.title(title_str, color=cs['title_color'])


        if self.CONVERT_TOMV:
            lab_units = '[mV]'
        else:
            lab_units = '[V]'


        plt.scatter(re_e, im_e, color=cs['blob_e'], alpha=cs['blobs_transp'], s=cs['point_scatter_size'])
        plt.scatter(re_g, im_g, color=cs['blob_g'], alpha=cs['blobs_transp'], s=cs['point_scatter_size'])

        if pre_read:
            if not norm:
                plt.scatter(re_g_pre, im_g_pre, color=cs['blob_prepulse'], alpha=cs['blobs_transp'], s=cs['point_scatter_size'])

        ### fake plot just for string in legend
        plt.plot([],[], label = str_params, visible=False)
        plt.plot([],[], label = str_fidelity, visible=False)


        ### real plots
        plt.plot([c_re_g, c_re_e], [c_im_g, c_im_e], label=str_blob_place, color=cs['color_dist'], linewidth = cs['vector_bw_blobs'] )              #plot line between blobs centers
        if zero_on_plot:
            plt.plot([void_re,c_re_g], [void_im, c_im_g], color=cs['color_g_vector'], linewidth=cs['vector_state_lw'])        #plot line from VOID to |g> blob
            plt.plot([void_re,c_re_e], [void_im, c_im_e], color=cs['color_e_vector'], linewidth=cs['vector_state_lw'])        #plot line from VOID to |e> blob
            plt.plot([0, void_re], [0, void_im], color=cs['color_zero_vector'], linewidth=cs['vector_zero_lw'])      #plot line form [0,0] to VOID

        plt.plot([ c_re_g ],[ c_im_g ], 'X', markersize=cs['onplot_mark_size'], color=cs['color_g_mean'], label='g-state: '+str_g_place, visible=plot_centers)  #this two needs only for legend color
        plt.plot([ c_re_e ],[ c_im_e ], 'X', markersize=cs['onplot_mark_size'], color=cs['color_e_mean'], label='e-state: '+str_e_place, visible=plot_centers)

        #### PLOT CROSSES OR FRAMES AROUND EACH BLOB TO SHOW REAL SIZE #########
        ###remake it with one pair of plt.plot !V !V

        if plot_crosses:
            def plot_cross(cord_cross, color='k', lw=1):
                if cord_cross is None:
                    return False
                if len(cord_cross) != 8:
                    return False
                ### ----------------------
                [ax,ay,bx,by,cx,cy,dx,dy] = cord_cross
                plt.plot([ax,bx],[ay,by], color=color, lw=lw)
                plt.plot([cx,dx],[cy,dy], color=color, lw=lw)
                return True

            if norm:
                plot_cross(self.cross_g_xy, color=cs['color_g_cross'], lw=cs['lw_cross'])
                plot_cross(self.cross_e_xy, color=cs['color_e_cross'], lw=cs['lw_cross'])
            else:
                plot_cross(self.cross_g_reim, color=cs['color_g_cross'], lw=cs['lw_cross'])
                plot_cross(self.cross_e_reim, color=cs['color_e_cross'], lw=cs['lw_cross'])

        ### cadre frame
        if plot_cadres:
            def plot_cadre(cord_cadre, color='k', lw=1, part=0.1):
                '''
                nice frames with corners
                '''
                if cord_cadre is None:
                    return False
                if len(cord_cadre) != 8:
                    return False
                ### ----------------------
                def plot_cutted_line(x1,x2,y1,y2, part=0.1, color='k', lw=1):
                    if part==1:
                        plt.plot([x1,x2],[y1,y2], color=color, lw=lw)
                        return True

                    distance = np.sqrt( (x2-x1)**2 + (y2-y1)**2  )
                    theta = np.angle((x2+1j*y2) - (x1+1j*y1), deg=False)

                    len1 = part*distance
                    c1x = x1 + len1*np.cos(theta)
                    c1y = y1 + len1*np.sin(theta)

                    len2 = (1.0 - part)*distance
                    c2x = x1 + len2*np.cos(theta)
                    c2y = y1 + len2*np.sin(theta)

                    plt.plot([x1,c1x],[y1,c1y], color=color, lw=lw)
                    plt.plot([c2x,x2],[c2y,y2], color=color, lw=lw)
                    return True

                [ax,ay,bx,by,cx,cy,dx,dy] = cord_cadre
                plot_cutted_line(ax,bx,ay,by, color=color, lw=lw, part=part)
                plot_cutted_line(bx,dx,by,dy, color=color, lw=lw, part=part)
                plot_cutted_line(dx,cx,dy,cy, color=color, lw=lw, part=part)
                plot_cutted_line(cx,ax,cy,ay, color=color, lw=lw, part=part)
                return True

            if norm:
                plot_cadre(self.cadre_g_xy, color=cs['color_g_cross'], lw=cs['lw_cross'], part=cs['cadr_frame_part'])
                plot_cadre(self.cadre_e_xy, color=cs['color_e_cross'], lw=cs['lw_cross'], part=cs['cadr_frame_part'])
            else:
                plot_cadre(self.cadre_g_reim, color=cs['color_g_cross'], lw=cs['lw_cross'], part=cs['cadr_frame_part'])
                plot_cadre(self.cadre_e_reim, color=cs['color_e_cross'], lw=cs['lw_cross'], part=cs['cadr_frame_part'])


        ########################################################################

        if zero_on_plot:
            zero_label = 'Void zero: Re:'+ my_stround(void_re,5,withminus=True)+ '; Im:'+ my_stround(void_im,5,withminus=True) + '; 2*alpha='+ my_stround(angle_between_blobs,3,withminus=True)+ u"\u00b0"
            plt.plot([void_re],[void_im],'+', label=zero_label, color=cs['color_void'], markersize=cs['onplot_mark_size'] )      #coordinats of no signal VOID (global)
            plt.plot([0],[0],'+', color=cs['color_zero'], markersize=cs['onplot_mark_size'] )   #coordinats of 0 V

        # if font is not None:
        #     leg = plt.legend(fancybox=True, framealpha=cs['legend_alpha'], loc='lower left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'], prop=font)
        # else:
        #     leg = plt.legend(fancybox=True, framealpha=cs['legend_alpha'], loc='lower left', facecolor=cs['legend_color'],edgecolor=cs['legend_frame_color'])
        #
        # for text in leg.get_texts():        #set color to legend text
        #     plt.setp(text, size = fontsize)
        #     plt.setp(text, color = cs['legend_text_color'])
        #
        #
        # if font is not None:
        #     for label in ax.get_xticklabels():  #set font to each xtick
        #         label.set_fontproperties(font)
        #     for label in ax.get_yticklabels():  #set font to each xtick
        #         label.set_fontproperties(font)


        if font is not None:
            plt.title(  title_str, fontproperties = font, color=cs['title_color'] )
            plt.xlabel('Re '+lab_units, fontproperties = font)
            plt.ylabel('Im '+lab_units, fontproperties = font)
            if not NOLEGEND:
                leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'], prop=font)
            for label in ax.get_xticklabels():  #set font to each xtick
                label.set_fontproperties(font)
            for label in ax.get_yticklabels():  #set font to each xtick
                label.set_fontproperties(font)
        else:
            plt.title(title_str, color=cs['title_color'])
            plt.xlabel('Re '+lab_units)
            plt.ylabel('Im '+lab_units)
            if not NOLEGEND:
                leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'])
                for text in leg.get_texts():        #set color to legend text
                    plt.setp(text, color = cs['legend_text_color'])
                    plt.setp(text, size =  cs['legend_fontsize'])






        if save:
            import os

            if not os.path.exists(savepath):
                os.makedirs(savepath)
            full_fname = savepath +'\\'+ fname + fileformat
            plt.savefig(full_fname, transparent = fig_transp, facecolor=cs['fig_face_color'], edgecolor=cs['fig_border_color'], fontproperties = font)

        mpl.style.use('default')

        if show:
            plt.show()
            return [fig, ax]
        else:
            plt.close()
            return True

    def plot_hists(self, regime='raw_and_selected', dark=True, log=True, figsize=[15,10], lw=1, fig_transp=False, title_str='', font=None, show=True, limits=[None,None],y_limits=[None,None], save=False, savepath='', fname='Hists', fileformat='.png', SHOW_SIZE=True, SHOW_FIT=True, NOLEGEND=False):
        '''
        function of plot histograms of object is it exists
        have different regimes:
        regime = 'raw_data' - plot hists of data with fit(if it is)
        regime = 'raw_data_and_pre' - same, but with results of prepulse
        regime = 'selected' - plot postselected data with fit(if it is)
        regime = 'raw_and_selected' compare between raw data and postselected (no fit)
        '''
        from matplotlib import pyplot as plt
        ###############################################
        ### all design here _________________________##
        ###############################################

        ### STYLE
        if dark:
            cs = dark_scheme
        else:
            cs = bright_scheme

        import matplotlib as mpl
        mpl.rc('axes',  edgecolor=cs['AXES_COLOR'], labelcolor=cs['AXES_COLOR'], grid=True)
        mpl.rc('xtick', color=cs['AXES_COLOR'])
        mpl.rc('ytick', color=cs['AXES_COLOR'])
        mpl.rc('grid',  color=cs['grid_color'])

        ###____SET CUSTOM FONT ###
        plt.rc('font', family = cs['font_family'])
        plt.rc('font', size   = cs['fontsize'])
        plt.rc('xtick', labelsize =cs['fontsize'])
        plt.rc('ytick', labelsize =cs['fontsize'])

        ###############################################
        ### all data plot here ______________________##
        ###############################################
        if figsize is None:
            fig, ax = plt.subplots(1, 1, sharey=True, tight_layout=True, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'])
        else:
            if (type(figsize) != list):
                print 'figsize must be a lsit'
                return False
            else:
                if len(figsize) != 2:
                    print 'figsize list must contain to numbers (x and y size)'
                    return False
            fig, ax = plt.subplots(1, 1, figsize=(figsize[0],figsize[1]), sharey=True, tight_layout=True, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'])

        ############################################
        ### fake plot just for string in legend_####
        str_fidelity = ''
        str_params   = ''
        if self.dict_fidelity is not None:
            str_fidelity = 'F_post:'+my_stround(  100*self.dict_fidelity['F_post'],4 )+'% F:'+my_stround(  100*self.dict_fidelity['F'],4 )+'% F_gaus(d):'+my_stround(  100*self.dict_fidelity['F_gaus_dscrt'],4 )+'%'
        if self.dict_param is not None:
            str_params = 'Rdt:'+ my_stround( self.dict_param['rudat'],4 )+'dB; t_read:'+my_stround( 1e9*self.dict_param['t_read'],3 )+'ns'+' Fr:'+my_stround( self.dict_param['freq_read'],6 )+'Ghz'
        plt.plot([],[], label = str_params, visible=False)
        plt.plot([],[], label = str_fidelity, visible=False)
        ############################################


        maxval = 1 ##this variable we use for define plt.ylim()

        if self.threshold is not None:
            plt.axvline(x=self.threshold, alpha=cs['hist_thr_alpha'], c=cs['hist_thr_color'], lw=cs['hist_thr_linewidth'], ls=cs['hist_thr_linestyle'], label='Threshold')

        if regime == 'raw_data':
            print 'regime: raw_data'

            #### plot vertical lines of centers
            if (self.center_x_g is not None) and (self.center_x_e is not None):
                plt.axvline(x=self.center_x_g, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_x_e, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])

            #### plot x_g, x_e hists ####
            if (self.hist_x_g is not None) and (self.hist_x_e is not None):
                #### plot raw data step_histograms
                if (self.hist_x_g.hist_xy is not None) and (self.hist_x_e.hist_xy is not None):
                    hist_g   = self.hist_x_g.hist_xy
                    hist_e   = self.hist_x_e.hist_xy
                    maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                    plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_color'], label='Read g-state')
                    plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_color'], label='Read e-state')

                #### plot fit hists ####
                if SHOW_FIT:
                    ### fit by SingleGaussian
                    if (self.hist_x_g.gauss_fit is not None) and (self.hist_x_e.gauss_fit is not None):
                        hist_g  = self.hist_x_g.gauss_fit
                        hist_e  = self.hist_x_e.gauss_fit
                        plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state', alpha=cs['hist_fit_single_alpha'])
                        plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state', alpha=cs['hist_fit_single_alpha'])

                    ### fit by SecondGaussian & by DoubleGaussian
                    if (self.hist_x_g.gauss2_fit is not None) and (self.hist_x_e.gauss2_fit is not None):
                        ### fit by SecondGaussian
                        hist_g  = self.hist_x_g.gauss2_fit
                        hist_e  = self.hist_x_e.gauss2_fit
                        plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state second', alpha=cs['hist_fit_second_alpha'])
                        plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state second', alpha=cs['hist_fit_second_alpha'])

                        ### fit by DoubleGaussian
                        X = self.hist_x_g.gauss_fit[1]
                        Y_g_sum = self.hist_x_g.gauss_fit[0] + self.hist_x_g.gauss2_fit[0]
                        Y_e_sum = self.hist_x_e.gauss_fit[0] + self.hist_x_e.gauss2_fit[0]
                        plt.plot(X, Y_g_sum, lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state DoubleGauss', alpha=cs['hist_fit_double_alpha'])
                        plt.plot(X, Y_e_sum, lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state DoubleGauss', alpha=cs['hist_fit_double_alpha'])





        elif regime == 'raw_data_and_pre':
            print 'regime: raw_data_and_pre'
            #### plot vertical lines of centers
            if (self.center_x_g is not None) and (self.center_x_e is not None):
                plt.axvline(x=self.center_x_g, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_x_e, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])

            #### plot PREPULSE hists ####
            if (self.hist_x_g_pre is not None) and (self.hist_x_e_pre is not None):
                hist_g  = self.hist_x_g_pre.hist_xy
                hist_e  = self.hist_x_e_pre.hist_xy
                # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_pre_color'], label='Prepulse g-state')
                plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_pre_color'], label='Prepulse e-state')


            #### plot x_g, x_e hists ####
            if (self.hist_x_g is not None) and (self.hist_x_e is not None):
                if (self.hist_x_g.hist_xy is not None) and (self.hist_x_e.hist_xy is not None):
                    hist_g   = self.hist_x_g.hist_xy
                    hist_e   = self.hist_x_e.hist_xy
                    maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                    plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_color'], label='Read g-state')
                    plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_color'], label='Read e-state')


                #### plot fit hists ####
                if SHOW_FIT:
                    ### fit by SingleGaussian
                    if (self.hist_x_g.gauss_fit is not None) and (self.hist_x_e.gauss_fit is not None):
                        hist_g  = self.hist_x_g.gauss_fit
                        hist_e  = self.hist_x_e.gauss_fit
                        plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state', alpha=cs['hist_fit_single_alpha'])
                        plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state', alpha=cs['hist_fit_single_alpha'])

                    ### fit by SecondGaussian & by DoubleGaussian
                    if (self.hist_x_g.gauss2_fit is not None) and (self.hist_x_e.gauss2_fit is not None):
                        ### fit by SecondGaussian
                        hist_g  = self.hist_x_g.gauss2_fit
                        hist_e  = self.hist_x_e.gauss2_fit
                        plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state second', alpha=cs['hist_fit_second_alpha'])
                        plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state second', alpha=cs['hist_fit_second_alpha'])

                        ### fit by DoubleGaussian
                        X = self.hist_x_g.gauss_fit[1]
                        Y_g_sum = self.hist_x_g.gauss_fit[0] + self.hist_x_g.gauss2_fit[0]
                        Y_e_sum = self.hist_x_e.gauss_fit[0] + self.hist_x_e.gauss2_fit[0]
                        plt.plot(X, Y_g_sum, lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state DoubleGauss', alpha=cs['hist_fit_double_alpha'])
                        plt.plot(X, Y_e_sum, lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state DoubleGauss', alpha=cs['hist_fit_double_alpha'])


        elif regime=='selected':
            print 'regime: selected'
            #### plot vertical lines of centers
            if (self.center_x_g_select is not None) and (self.center_x_e_select is not None):
                plt.axvline(x=self.center_x_g_select, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_x_e_select, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])


            #### plot x_g, x_e hists  SELECTED ####
            if (self.hist_x_g_select is not None) and (self.hist_x_e_select is not None):
                if (self.hist_x_g_select.hist_xy is not None) and (self.hist_x_e_select.hist_xy is not None):
                    hist_g   = self.hist_x_g_select.hist_xy
                    hist_e   = self.hist_x_e_select.hist_xy
                    maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                    plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_sel_color'], label='Selected g-state')
                    plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_sel_color'], label='Selected e-state')


                #### plot fit hists ####
                if SHOW_FIT:
                    #### fit of selected
                    if (self.hist_x_g_select.gauss_fit is not None) and (self.hist_x_e_select.gauss_fit is not None):
                        hist_g  = self.hist_x_g_select.gauss_fit
                        hist_e  = self.hist_x_e_select.gauss_fit
                        # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                        plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state selected', alpha=cs['hist_fit_single_alpha'])
                        plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state selected', alpha=cs['hist_fit_single_alpha'])


        elif regime=='raw_and_selected':
            print 'regime==raw_and_selected'
            #### plot vertical lines of centers
            if (self.center_x_g_select is not None) and (self.center_x_e_select is not None):
                plt.axvline(x=self.center_x_g_select, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_x_e_select, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])


            #### plot x_g, x_e hists  SELECTED ####
            if (self.hist_x_g_select is not None) and (self.hist_x_e_select is not None):
                if (self.hist_x_g_select.hist_xy is not None) and (self.hist_x_e_select.hist_xy is not None):
                    hist_g   = self.hist_x_g_select.hist_xy
                    hist_e   = self.hist_x_e_select.hist_xy
                    maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                    plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_sel_color'], label='Selected g-state')
                    plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_sel_color'], label='Selected e-state')


            #### plot x_g, x_e hists ####
            if (self.hist_x_g is not None) and (self.hist_x_e is not None):
                if (self.hist_x_g.hist_xy is not None) and (self.hist_x_e.hist_xy is not None):
                    hist_g   = self.hist_x_g.hist_xy
                    hist_e   = self.hist_x_e.hist_xy
                    maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                    plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_color'], label='Read g-state')
                    plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_color'], label='Read e-state')

            #### plot fit hists ####
            if SHOW_FIT:
                #### fit of selected
                if (self.hist_x_g_select.gauss_fit is not None) and (self.hist_x_e_select.gauss_fit is not None):
                    hist_g  = self.hist_x_g_select.gauss_fit
                    hist_e  = self.hist_x_e_select.gauss_fit
                    # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                    plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_hist_g_sel_color'], label='Fit g-state selected', alpha=cs['hist_fit_single_alpha'])
                    plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_hist_e_sel_color'], label='Fit e-state selected', alpha=cs['hist_fit_single_alpha'])

                ### fit by SingleGaussian
                if (self.hist_x_g.gauss_fit is not None) and (self.hist_x_e.gauss_fit is not None):
                    hist_g  = self.hist_x_g.gauss_fit
                    hist_e  = self.hist_x_e.gauss_fit
                    plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state', alpha=cs['hist_fit_single_alpha'])
                    plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state', alpha=cs['hist_fit_single_alpha'])

                ### fit by SecondGaussian & by DoubleGaussian
                if (self.hist_x_g.gauss2_fit is not None) and (self.hist_x_e.gauss2_fit is not None):
                    ### fit by SecondGaussian
                    hist_g  = self.hist_x_g.gauss2_fit
                    hist_e  = self.hist_x_e.gauss2_fit
                    plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state second', alpha=cs['hist_fit_second_alpha'])
                    plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state second', alpha=cs['hist_fit_second_alpha'])

                    ### fit by DoubleGaussian
                    X = self.hist_x_g.gauss_fit[1]
                    Y_g_sum = self.hist_x_g.gauss_fit[0] + self.hist_x_g.gauss2_fit[0]
                    Y_e_sum = self.hist_x_e.gauss_fit[0] + self.hist_x_e.gauss2_fit[0]
                    plt.plot(X, Y_g_sum, lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state DoubleGauss', alpha=cs['hist_fit_double_alpha'])
                    plt.plot(X, Y_e_sum, lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state DoubleGauss', alpha=cs['hist_fit_double_alpha'])





        else:
            print 'plot_hist: wrong value for regime!'

        ### to plot the borders of std
        if SHOW_SIZE:
            if (self.sizeblob_x_g is not None) and (self.sizeblob_x_e is not None):
                x_g_left =  self.center_x_g - self.sizeblob_x_g/2
                x_g_right = self.center_x_g + self.sizeblob_x_g/2
                x_e_left =  self.center_x_e - self.sizeblob_x_e/2
                x_e_right = self.center_x_e + self.sizeblob_x_e/2
                if log:
                    y_max = maxval*1.5
                else:
                    y_max = maxval*1.1
                plt.fill_between([x_g_left, x_g_right], 0, y_max, color=cs['hist_shade_g_color'], alpha=cs['hist_shade_transp']  )
                plt.fill_between([x_e_left, x_e_right], 0, y_max, color=cs['hist_shade_e_color'], alpha=cs['hist_shade_transp']  )

        ###############################################


        ###############################################
        ### all work with axes here _________________##
        ###############################################
        ax.set_facecolor(cs['bg_color'])
        plt.grid(color=cs['grid_color'], alpha= cs['grid_transp'])

        [leftlim, rightlim] = limits

        if leftlim is None:
            leftlim = np.min([ np.min(hist_g[1]), np.min(hist_e[1]) ])
        if rightlim is None:
            rightlim = np.max([ np.max(hist_g[1]), np.max(hist_e[1]) ])
        plt.xlim(leftlim,rightlim)

        ###__choose_limits_###
        if y_limits[0] is not None:
            y_min = y_limits[0]
        else:
            y_min = 1

        if y_limits[1] is not None:
            y_max =  y_limits[1]
        else:
            if log:
                y_max = maxval*1.5
            else:
                y_max = maxval*1.1

        plt.ylim(ymin = y_min, ymax = y_max)
        #####______________####

        ### axis_scale_#
        if log:
            plt.yscale('log')
        else:
            plt.yscale('linear')
        ###__________###

        if title_str is '':
            title_str = self.timestamp

        if self.CONVERT_TOMV:
            lab_units = '[mV]'
        else:
            lab_units = '[V]'

        if font is not None:
            plt.title(  title_str, fontproperties = font, color=cs['title_color'] )
            plt.xlabel( lab_units, fontproperties = font )
            plt.ylabel( 'Counts',  fontproperties = font )
            if not NOLEGEND:
                leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'], prop=font)
                for text in leg.get_texts():        #set color to legend text
                    plt.setp(text, size = cs['legend_fontsize'])
                    plt.setp(text, color = cs['legend_text_color'])

            for label in ax.get_xticklabels():  #set font to each xtick
                label.set_fontproperties(font)
            for label in ax.get_yticklabels():  #set font to each xtick
                label.set_fontproperties(font)



        else:
            plt.title(title_str, color=cs['title_color'])
            plt.xlabel(lab_units)
            plt.ylabel('Counts')
            if not NOLEGEND:
                leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'])
                for text in leg.get_texts():        #set color to legend text
                    plt.setp(text, color = cs['legend_text_color'])
                    plt.setp(text, size =  cs['legend_fontsize'])
            # plt.setp(text, size = cs['legend_fontsize'])



        if save:
            if savepath == '':
                savepath='savings\\'
            import os
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            full_fname = savepath +'\\'+ fname + fileformat
            if fig_transp:
                plt.savefig(full_fname, transparent = True)
            else:
                plt.savefig(full_fname,facecolor=cs['fig_face_color'], edgecolor=cs['fig_border_color'])

        mpl.style.use('default')

        if show:
            plt.show()
            return fig
        else:
            plt.close()
            return True

    def plot_hists_y(self, dark=True, log=True, figsize=[15,10], lw=1, fig_transp=False, title_str='', font=None, show=True, limits=[None,None],y_limits=[None,None], save=False, savepath='', fname='Hists_Y', fileformat='.png', SHOW_SIZE=True):
        '''
        function of plot histograms of object is it exists
        have different regimes:
        regime = 'raw_data' - plot hists of data with fit(if it is)

        '''
        from matplotlib import pyplot as plt
        ###############################################
        ### all design here _________________________##
        ###############################################

        ### STYLE
        if dark:
            cs = dark_scheme
        else:
            cs = bright_scheme

        import matplotlib as mpl
        mpl.rc('axes',  edgecolor=cs['AXES_COLOR'], labelcolor=cs['AXES_COLOR'], grid=True)
        mpl.rc('xtick', color=cs['AXES_COLOR'])
        mpl.rc('ytick', color=cs['AXES_COLOR'])
        mpl.rc('grid',  color=cs['grid_color'])
        ### font default
        plt.rc('font', family = cs['font_family'])
        plt.rc('font', size   = cs['fontsize'])
        plt.rc('xtick', labelsize =cs['fontsize'])
        plt.rc('ytick', labelsize =cs['fontsize'])

        ###############################################
        ### all data plot here ______________________##
        ###############################################
        if figsize is None:
            fig, ax = plt.subplots(1, 1, sharey=True, tight_layout=True, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'])
        else:
            if (type(figsize) != list):
                print 'figsize must be a lsit'
                return False
            else:
                if len(figsize) != 2:
                    print 'figsize list must contain to numbers (x and y size)'
                    return False
            fig, ax = plt.subplots(1, 1, figsize=(figsize[0],figsize[1]), sharey=True, tight_layout=True, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'])


        maxval = 1 ##this variable we use for define plt.ylim()

        # if self.threshold is not None:
        #     plt.axvline(x=self.threshold, alpha=cs['hist_thr_alpha'], c=cs['hist_thr_color'], lw=cs['hist_thr_linewidth'], ls=cs['hist_thr_linestyle'], label='Threshold')

        if (self.center_y_g is not None) and (self.center_y_e is not None):
            plt.axvline(x=self.center_y_g, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
            plt.axvline(x=self.center_y_e, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])

        # if (self.sizeblob_y_g is not None) and (self.sizeblob_y_e is not None):
        #     plt.axvline(x=self.center_y_g - self.sizeblob_y_g/2, alpha=th_alpha/2, c=color_g_mean, lw=th_width, ls=th_linestyle)
        #     plt.axvline(x=self.center_y_g + self.sizeblob_y_g/2, alpha=th_alpha/2, c=color_g_mean, lw=th_width, ls=th_linestyle)
        #     plt.axvline(x=self.center_y_e - self.sizeblob_y_e/2, alpha=th_alpha/2, c=color_e_mean, lw=th_width, ls=th_linestyle)
        #     plt.axvline(x=self.center_y_e + self.sizeblob_y_e/2, alpha=th_alpha/2, c=color_e_mean, lw=th_width, ls=th_linestyle)

        if SHOW_SIZE:
            if (self.sizeblob_y_g is not None) and (self.sizeblob_y_e is not None):
                x_g_left =  self.center_y_g - self.sizeblob_y_g/2
                x_g_right = self.center_y_g + self.sizeblob_y_g/2
                x_e_left =  self.center_y_e - self.sizeblob_y_e/2
                x_e_right = self.center_y_e + self.sizeblob_y_e/2
                if log:
                    y_max = maxval*1.5
                else:
                    y_max = maxval*1.1
                plt.fill_between([x_g_left, x_g_right], 0, y_max, color=cs['hist_shade_g_color'], alpha=cs['hist_shade_transp']  )
                plt.fill_between([x_e_left, x_e_right], 0, y_max, color=cs['hist_shade_e_color'], alpha=cs['hist_shade_transp']  )


        #### plot x_g, x_e hists ####
        if (self.hist_y_g.hist_xy is not None) and (self.hist_y_e.hist_xy is not None):
            hist_g   = self.hist_y_g.hist_xy
            hist_e   = self.hist_y_e.hist_xy
            maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
            plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_color'], label='Read g-state')
            plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_color'], label='Read e-state')


        #### plot fit hists ####
        if (self.hist_y_g.gauss_fit is not None) and (self.hist_y_e.gauss_fit is not None):
            hist_g  = self.hist_y_g.gauss_fit
            hist_e  = self.hist_y_e.gauss_fit
            # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
            plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state', alpha=cs['hist_fit_single_alpha'])
            plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state', alpha=cs['hist_fit_single_alpha'])


        ###############################################


        ###############################################
        ### all work with axes here _________________##
        ###############################################
        ax.set_facecolor(cs['bg_color'])
        plt.grid(color=cs['grid_color'], alpha= cs['grid_transp'])

        [leftlim, rightlim] = limits
        if leftlim is None:
            leftlim = np.min([ np.min(hist_g[1]), np.min(hist_e[1]) ])
        if rightlim is None:
            rightlim = np.max([ np.max(hist_g[1]), np.max(hist_e[1]) ])
        plt.xlim(leftlim,rightlim)

        ###__choose_limits_###
        if y_limits[0] is not None:
            y_min = y_limits[0]
        else:
            y_min = 1

        if y_limits[1] is not None:
            y_max =  y_limits[1]
        else:
            if log:
                y_max = maxval*1.5
            else:
                y_max = maxval*1.1

        plt.ylim(ymin = y_min, ymax = y_max)
        #####______________####

        if log:
            plt.yscale('log')
        else:
            plt.yscale('linear')


        if title_str is '':
            title_str = self.timestamp

        if self.CONVERT_TOMV:
            lab_units = '[mV]'
        else:
            lab_units = '[V]'

        if font is not None:
            plt.title(  title_str, fontproperties = font, color=cs['title_color'] )
            plt.xlabel( lab_units, fontproperties = font )
            plt.ylabel( 'Counts',  fontproperties = font )
            leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'], prop=font)
            for label in ax.get_xticklabels():  #set font to each xtick
                label.set_fontproperties(font)
            for label in ax.get_yticklabels():  #set font to each xtick
                label.set_fontproperties(font)
        else:
            plt.title(title_str, color=cs['title_color'])
            plt.xlabel(lab_units)
            plt.ylabel('Counts')
            leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'])
            plt.setp(text, size = cs['legend_fontsize'])

        for text in leg.get_texts():        #set color to legend text
            plt.setp(text, color = cs['legend_text_color'])
            plt.setp(text, size =  cs['legend_fontsize'])


        if save:
            if savepath == '':
                savepath='savings\\'
            import os
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            full_fname = savepath +'\\'+ fname + fileformat
            if fig_transp:
                plt.savefig(full_fname, transparent = True)
            else:
                plt.savefig(full_fname,facecolor=cs['fig_face_color'], edgecolor=cs['fig_border_color'])

        mpl.style.use('default')

        if show:
            plt.show()
            return fig
        else:
            plt.close()
            return True

    def plot_hists_unitless(self, regime='raw_and_selected', dark=True, log=True, figsize=[15,10], lw=1, fig_transp=False, title_str='', font=None, show=True, limits=[None,None],y_limits=[None,None], save=False, savepath='', fname='Hists_unitless', fileformat='.png'):
        '''
        function of plot histograms of object is it exists
        have different regimes:
        regime = 'raw_data' - plot hists of data with fit(if it is)
        regime = 'raw_data_and_pre' - same, but with results of prepulse
        regime = 'selected' - plot postselected data with fit(if it is)
        regime = 'raw_and_selected' compare between raw data and postselected (no fit)
        '''
        from matplotlib import pyplot as plt
        ###############################################
        ### all design here _________________________##
        ###############################################

        ### STYLE
        if dark:
            cs = dark_scheme
        else:
            cs = bright_scheme

        import matplotlib as mpl
        mpl.rc('axes',  edgecolor=cs['AXES_COLOR'], labelcolor=cs['AXES_COLOR'], grid=True)
        mpl.rc('xtick', color=cs['AXES_COLOR'])
        mpl.rc('ytick', color=cs['AXES_COLOR'])
        mpl.rc('grid',  color=cs['grid_color'])

        ### font default
        plt.rc('font', family = cs['font_family'])
        plt.rc('font', size   = cs['fontsize'])
        plt.rc('xtick', labelsize =cs['fontsize'])
        plt.rc('ytick', labelsize =cs['fontsize'])

        ###############################################
        ### all data plot here ______________________##
        ###############################################
        if figsize is None:
            fig, ax = plt.subplots(1, 1, sharey=True, tight_layout=True, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'])
        else:
            if (type(figsize) != list):
                print 'figsize must be a lsit'
                return False
            else:
                if len(figsize) != 2:
                    print 'figsize list must contain to numbers (x and y size)'
                    return False
            fig, ax = plt.subplots(1, 1, figsize=(figsize[0],figsize[1]), sharey=True, tight_layout=True, facecolor=cs['fig_face_color'], edgecolor = cs['fig_border_color'])

        ############################################
        ### fake plot just for string in legend_####
        str_fidelity = ''
        str_params   = ''
        if self.dict_fidelity is not None:
            str_fidelity = 'F_post:'+my_stround(  100*self.dict_fidelity['F_post'],4 )+'% F:'+my_stround(  100*self.dict_fidelity['F'],4 )+'% F_gaus(d):'+my_stround(  100*self.dict_fidelity['F_gaus_dscrt'],4 )+'%'
        if self.dict_param is not None:
            str_params = 'Rdt:'+ my_stround( self.dict_param['rudat'],4 )+'dB; t_read:'+my_stround( 1e9*self.dict_param['t_read'],3 )+'ns'+' Fr:'+my_stround( self.dict_param['freq_read'],6 )+'Ghz'
        plt.plot([],[], label = str_params, visible=False)
        plt.plot([],[], label = str_fidelity, visible=False)
        ############################################

        maxval = 1 ##this variable we use for define plt.ylim()

        if self.threshold_r is not None:
            plt.axvline(x=self.threshold_r, alpha=cs['hist_thr_alpha'], c=cs['hist_thr_color'], lw=cs['hist_thr_linewidth'], ls=cs['hist_thr_linestyle'], label='Threshold')


        S_e = self.S_eff_e
        S_g = self.S_eff_g
        str_S_e = '; Se='+ str( round(S_e,2) )
        str_S_g = '; Sg='+ str( round(S_g,2) )

        S_e_selected = self.S_eff_e_selected
        S_g_selected = self.S_eff_g_selected
        str_S_e_selected = '; Se_sel='+ str( round(S_e_selected,2) )
        str_S_g_selected = '; Sg_sel='+ str( round(S_g_selected,2) )

        if regime == 'raw_data':
            print 'regime: raw_data (unitless)'
            if (self.center_r_g is not None) and (self.center_r_e is not None):
                plt.axvline(x=self.center_r_g, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_r_e, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])

            #### plot r_g, r_e hists ####
            if (self.hist_r_g.hist_xy is not None) and (self.hist_r_e.hist_xy is not None):
                hist_g   = self.hist_r_g.hist_xy
                hist_e   = self.hist_r_e.hist_xy
                maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_color'], label='Read g-state'+str_S_g)
                plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_color'], label='Read e-state'+str_S_e)


            #### plot fit hists ####
            if (self.hist_r_g.gauss_fit is not None) and (self.hist_r_e.gauss_fit is not None):
                hist_g  = self.hist_r_g.gauss_fit
                hist_e  = self.hist_r_e.gauss_fit
                # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state', alpha=cs['hist_fit_single_alpha'])
                plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state', alpha=cs['hist_fit_single_alpha'])


        elif regime == 'raw_data_and_pre':
            print 'regime: raw_data_and_pre (unitless)'
            if (self.center_r_g is not None) and (self.center_r_e is not None):
                plt.axvline(x=self.center_r_g, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_r_e, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])

            #### plot PREPULSE hists ####
            if (self.hist_r_g_pre is not None) and (self.hist_r_e_pre is not None):
                hist_g  = self.hist_r_g_pre.hist_xy
                hist_e  = self.hist_r_e_pre.hist_xy
                # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_pre_color'], label='Prepulse g-state')
                plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_pre_color'], label='Prepulse e-state')


            #### plot r_g, r_e hists ####
            if (self.hist_r_g.hist_xy is not None) and (self.hist_r_e.hist_xy is not None):
                hist_g   = self.hist_r_g.hist_xy
                hist_e   = self.hist_r_e.hist_xy
                maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_color'], label='Read g-state')
                plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_color'], label='Read e-state')


            #### plot fit hists ####
            if (self.hist_r_g.gauss_fit is not None) and (self.hist_r_e.gauss_fit is not None):
                hist_g  = self.hist_r_g.gauss_fit
                hist_e  = self.hist_r_e.gauss_fit
                # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state', alpha=cs['hist_fit_single_alpha'])
                plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state', alpha=cs['hist_fit_single_alpha'])



        elif regime=='selected':
            print 'regime: selected (unitless)'
            if (self.center_r_g_select is not None) and (self.center_r_e_select is not None):
                plt.axvline(x=self.center_r_g_select, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_r_e_select, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])


            print 'regime: selected'
            #### plot r_g, r_e hists  SELECTED ####
            if (self.hist_r_g_select.hist_xy is not None) and (self.hist_r_e_select.hist_xy is not None):
                hist_g   = self.hist_r_g_select.hist_xy
                hist_e   = self.hist_r_e_select.hist_xy
                maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_sel_color'], label='Selected g-state'+str_S_g_selected)
                plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_sel_color'], label='Selected e-state'+str_S_e_selected)


            #### plot fit hists ####
            if (self.hist_r_g_select.gauss_fit is not None) and (self.hist_r_e_select.gauss_fit is not None):
                hist_g  = self.hist_r_g_select.gauss_fit
                hist_e  = self.hist_r_e_select.gauss_fit
                # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state selected', alpha=cs['hist_fit_single_alpha'])
                plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state selected', alpha=cs['hist_fit_single_alpha'])



        elif regime=='raw_and_selected':
            print 'regime: raw_and_selected (unitless)'
            if (self.center_r_g_select is not None) and (self.center_r_e_select is not None):
                plt.axvline(x=self.center_r_g_select, alpha=cs['hist_mean_alpha'], c=cs['color_g_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])
                plt.axvline(x=self.center_r_e_select, alpha=cs['hist_mean_alpha'], c=cs['color_e_mean'], lw=cs['hist_mean_linewidth'], ls=cs['hist_mean_linestyle'])

            #### plot r_g, r_e hists  SELECTED ####
            if (self.hist_r_g_select.hist_xy is not None) and (self.hist_r_e_select.hist_xy is not None):
                hist_g   = self.hist_r_g_select.hist_xy
                hist_e   = self.hist_r_e_select.hist_xy
                maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_sel_color'], label='Selected g-state'+str_S_g_selected)
                plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_sel_color'], label='Selected e-state'+str_S_e_selected)


            #### plot r_g, r_e hists ####
            if (self.hist_r_g.hist_xy is not None) and (self.hist_r_e.hist_xy is not None):
                hist_g   = self.hist_r_g.hist_xy
                hist_e   = self.hist_r_e.hist_xy
                maxval = np.max([ maxval, np.max(hist_g[0]), np.max(hist_e[0]) ])
                plt.plot(hist_g[1], hist_g[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_g_color'], label='Read g-state'+str_S_g)
                plt.plot(hist_e[1], hist_e[0], drawstyle='steps', lw=cs['hist_hist_lw'], color=cs['hist_hist_e_color'], label='Read e-state'+str_S_e)



            #### plot fit hists ####
            ## selected
            if (self.hist_r_g_select.gauss_fit is not None) and (self.hist_r_e_select.gauss_fit is not None):
                hist_g  = self.hist_r_g_select.gauss_fit
                hist_e  = self.hist_r_e_select.gauss_fit
                # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state selected', alpha=cs['hist_fit_single_alpha'])
                plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state selected', alpha=cs['hist_fit_single_alpha'])

            ### raw
            if (self.hist_r_g.gauss_fit is not None) and (self.hist_r_e.gauss_fit is not None):
                hist_g  = self.hist_r_g.gauss_fit
                hist_e  = self.hist_r_e.gauss_fit
                # maxval = np.max([ maxval, np.max(hist_g_fit[0]), np.max(hist_e_fit[0]) ])
                plt.plot(hist_g[1], hist_g[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_g_color'], label='Fit g-state', alpha=cs['hist_fit_single_alpha'])
                plt.plot(hist_e[1], hist_e[0], lw=cs['hist_fit_lw'], color=cs['hist_fit_e_color'], label='Fit e-state', alpha=cs['hist_fit_single_alpha'])


        else:
            print 'plot_hist: wrong value for regime!'

        ###############################################


        ###############################################
        ### all work with axes here _________________##
        ###############################################
        ax.set_facecolor(cs['bg_color'])
        plt.grid(color=cs['grid_color'], alpha= cs['grid_transp'])

        [leftlim, rightlim] = limits
        if leftlim is None:
            leftlim = np.min([ np.min(hist_g[1]), np.min(hist_e[1]) ])
        if rightlim is None:
            rightlim = np.max([ np.max(hist_g[1]), np.max(hist_e[1]) ])
        plt.xlim(leftlim,rightlim)

        ###__choose_limits_###
        if y_limits[0] is not None:
            y_min = y_limits[0]
        else:
            y_min = 1

        if y_limits[1] is not None:
            y_max =  y_limits[1]
        else:
            if log:
                y_max = maxval*1.5
            else:
                y_max = maxval*1.1

        plt.ylim(ymin = y_min, ymax = y_max)
        #####______________####


        if log:
            plt.yscale('log')
        else:
            plt.yscale('linear')


        if title_str is '':
            title_str = self.timestamp

        lab_units = '[unitless]'

        if font is not None:
            plt.title(  title_str, fontproperties = font, color=cs['title_color'] )
            plt.xlabel( lab_units, fontproperties = font )
            plt.ylabel( 'Counts',  fontproperties = font )
            leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'], prop=font)

            for label in ax.get_xticklabels():  #set font to each xtick
                label.set_fontproperties(font)
            for label in ax.get_yticklabels():  #set font to each xtick
                label.set_fontproperties(font)
        else:
            plt.title(title_str, color=cs['title_color'])
            plt.xlabel(lab_units)
            plt.ylabel('Counts')
            leg = plt.legend(fancybox=cs['legend_fancy'], framealpha=cs['legend_alpha'], loc='upper left', facecolor=cs['legend_color'], edgecolor=cs['legend_frame_color'])
            # plt.setp(text, size = cs['legend_fontsize'])

        for text in leg.get_texts():        #set color to legend text
            plt.setp(text, color = cs['legend_text_color'])
            plt.setp(text, size =  cs['legend_fontsize'])

        if save:
            if savepath == '':
                savepath='savings\\'
            import os
            if not os.path.exists(savepath):
                os.makedirs(savepath)
            full_fname = savepath +'\\'+ fname + fileformat
            if fig_transp:
                plt.savefig(full_fname, transparent = True)
            else:
                plt.savefig( full_fname,facecolor=cs['fig_face_color'], edgecolor=cs['fig_border_color'] )

        mpl.style.use('default')

        if show:
            plt.show()
            return fig
        else:
            plt.close()
            return True

    def plot_f_vs_threshold(self, xmin=None, xmax=None, ymin=None, ymax=None):
        '''
        function to show fidelity versus threshold
        '''
        from matplotlib import pyplot as plt

        def get_fro_vs_threshold(x_g, x_e, threshold):
            '''
            Simplest function to calculate only f_ro for given threshold value
            Calculate fidelity for given value of THRESHOLD
            Takes 1D arrays of normalized g and e results. ( re_g & re_e )
            return only value of f_ro = 1. - 0.5*(p_ge + p_eg)
            '''
            dict_count = get_count_states(x_g,x_e,threshold)
            p_ge = dict_count['p_ge']
            p_eg = dict_count['p_eg']
            f_ro = 1. - 0.5*(p_ge + p_eg)
            return f_ro

        if (self.x_g is None) or (self.x_e is None):
            self.make_norm_data_from_raw()
        x_g = self.x_g
        x_e = self.x_e

        nop = 200.
        [leftlim, rightlim, rabbish1, rabbish2 ] = crop_fluctuations(self.x_g, [0] , self.x_e, [0], 0, 0 )
        thr_vector = np.linspace(leftlim, rightlim, nop)

        fid_vector = []
        for thr in thr_vector:
            fid_vector.append( get_fro_vs_threshold(x_g, x_e, thr) )

        pic = plt.figure()

        if self.CONVERT_TOMV:
            lab_units = '[mV]'
        else:
            lab_units = '[V]'

        plt.plot(thr_vector, fid_vector, '.')
        plt.xlabel('threshold '+lab_units)
        plt.ylabel('Fidelity')


        ##postselected
        if (self.x_g_select is not None ) and (self.x_e_select is not None):
            fid_post_vector = []
            for thr in thr_vector:
                fid_post_vector.append( get_fro_vs_threshold(self.x_g_select, self.x_e_select, thr) )
            plt.plot(thr_vector, fid_post_vector, '.')

        return pic

################################################################################
