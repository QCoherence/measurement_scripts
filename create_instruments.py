#  # -*- coding: utf-8 -*-
#
#
# ###########################################################
# ##               Physical instruments
# ###########################################################

print ''
print '#######################################'
print '#'
print '#            Import of Physical devices'
print '#'
print '#######################################'
print ''

print '    Import measurement board: ats9360'
try:
   ats9360 = qt.instruments.create('ats9360', 'ATS9360_NPT')
   print '        Succed'
except:
   qt.instruments.remove('ats9360')
   print '        Failed'


print '    Import AWG Tabor'
try:
   Tabor = qt.instruments.create('Tabor', 'Tabor_WX1284C', address = 'TCPIP::192.168.10.51', reset=False)
   print '        Succed'
except:
   qt.instruments.remove('Tabor')
   print '        Failed'


print '    Import RUDAT compensation'
try:
   RUDAT_comp = qt.instruments.create('RUDAT_comp', 'RUDAT8000', address = 'http://192.168.10.10')
   print '        Succed'
except:
   qt.instruments.remove('RUDAT_comp')
   print '        Failed'


print '    Import RUDAT pump and comp'
try:
   RUDAT_pump = qt.instruments.create('RUDAT_pump', 'RUDAT8000', address = 'http://192.168.10.11')
   print '        Succed'
except:
   qt.instruments.remove('RUDAT_pump')
   print '        Failed'


print '    Import RUDAT photon'
try:
   RUDAT_ph = qt.instruments.create('RUDAT_ph', 'RUDAT8000', address = 'http://192.168.10.12')
   print '        Succed'
except:
   qt.instruments.remove('RUDAT_ph')
   print '        Failed'


# print '    Import Vaunix phase shifter 98:'
# try:
#     Phase_1 = qt.instruments.create('Phase_1', 'Vaunix_phase_shifter', serial_number = 22098)
#     print '        Succed'
# except:
#     qt.instruments.remove('Phase_1')
#     print '        Failed'


# print '    Import Vaunix phase shifter 97:'
# try:
#     Phase_2 = qt.instruments.create('Phase_2', 'Vaunix_phase_shifter', serial_number = 22097)
#     print '        Succed'
# except:
#     qt.instruments.remove('Phase_2')
#     print '        Failed'


# print '    Import Vaunix digital attenuator 82:'
# try:
#     Att_JPA = qt.instruments.create('Attenuator_JPA', 'Vaunix_attenuator', serial_number = 22082)
#     print '        Succed'
# except:
#     qt.instruments.remove('Attenuator_JPA')
#     print '        Failed'




print '    Import SMB 100A Clock Master:'
try:
   smb_1 = qt.instruments.create('smb_1', 'SMB100A', address='TCPIP::192.168.10.7', reset=False)
   print '        Succed'
except:
   qt.instruments.remove('smb_1')
   print '        Failed'
# # #
# # #
# # #
print '    Import SMB 100A:'
try:
   smb_2 = qt.instruments.create('smb_2', 'SMB100A', address='TCPIP::192.168.10.4', reset=False)
   print '        Succed'
except:
   qt.instruments.remove('smb_2')
   print '        Failed'
# # #
# # #
# # #
print '    Import SMB 100A TWPA PUMP:'
try:
   smb_3 = qt.instruments.create('smb_3', 'SMB100A', address='TCPIP::192.168.10.3', reset=False)
   print '        Succed'
except:
   qt.instruments.remove('smb_3')
   print '        Failed'
# # #
# # #
# # #

# print '    Import Agilent E8257D TWPA PUMP:'
# try:
#    # smb_3 = qt.instruments.create('smb_3', 'Agilent_E8257D_40GHz', address='TCPIP::192.168.10.6', reset=False)
#    smb_3 = qt.instruments.create('smb_3', 'Agilent_E8257D_40GHz', address='TCPIP::192.168.10.70', reset=False)
#    print '        Succed'
# except:
#    qt.instruments.remove('smb_3')
#    print '        Failed'


####

# print '    Import HP3245A:'
# try:
#     # hp3245 = qt.instruments.create('hp3245', 'HP3245A', address='TCPIP::192.168.10.58::gpib0,17', reset=False)
#     hp3245 = qt.instruments.create('hp3245', 'HP3245A', address='TCPIP::192.168.10.58::gpib0,9', reset=False)
#     hp3245.set_parameter_bounds('current', -50e-3, 50e-3)
#     print '        Succed'
# except:
#     qt.instruments.remove('hp3245')
#     print '        Failed'
#

# print '    Import HP3245A jpa:'
# try:
#     hp3245jpa = qt.instruments.create('hp3245jpa', 'HP3245A', address='TCPIP::192.168.10.58::gpib0,24', reset=False)
#     hp3245jpa.set_parameter_bounds('current', -100e-3, 100e-3)
#     print '        Succed'
# except:
#     qt.instruments.remove('hp3245jpa')
#     print '        Failed'

# print '    Import HP3245A:'
# try:
#     hp3245 = qt.instruments.create('hp3245', 'HP3245A', address='TCPIP::192.168.10.58::gpib0,24', reset=False)
#     hp3245.set_parameter_bounds('current', -50e-3, 50e-3)
#     print '        Succed'
# except:
#     qt.instruments.remove('hp3245')
#     print '        Failed'

print '    Import B2902A:'
try:
    b2902a = qt.instruments.create('b2902a', 'B2902A', address='TCPIP::192.168.10.58::gpib0,23', reset=False)
    b2902a.set_parameter_bounds('current', -50e-3, 50e-3)
    print '        Succed'
except:
    qt.instruments.remove('b2902a')
    print '        Failed'

# print '    Import VNA Anritsu:'
# try:
#     vna = qt.instruments.create('vna', 'MS46522B', address='TCPIP::192.168.10.13', reset=False) #Arpit
#     # vna = qt.instruments.create('vna', 'MS46522B', address='TCPIP::192.168.10.52', reset=False) #Kazi
#     print '        Succed'
# except:
#     qt.instruments.remove('vna')
#     print '        Failed'


######

print '    Import VNA ZNB20:'
try:
    vna = qt.instruments.create('vna znb20', 'ZNB20', address='TCPIP::192.168.10.2', reset=False) #Dorian's VNA
    print '        Succed'
except:
    qt.instruments.remove('vna znb20')
    print '        Failed'


######
######







######
######


# print '    Import Tektronix AFG 3252:'
# try:
#    Tektronix = qt.instruments.create('Tektronix', 'Tektronix_AFG3252', address='TCPIP::192.168.10.23', reset= False)
#    print '        Succed'
# except:
#    qt.instruments.remove('Tektronix')
#    print '        Failed'


#
# print '    Import Highland T560:'
# try:
#    pulser = qt.instruments.create('pulser', 'highland_T560', reset= False)
#    print '        Succed'
# except:
#    qt.instruments.remove('pulser')
#    print '        Failed'
# # # #
# #
# #
# print '    Import Spectrum M3i 4142:'
# try:
#    Spectrum = qt.instruments.create('Spectrum', 'Spectrum_M3i4142filter')
#    print '        Succed'
# except:
#    qt.instruments.remove('Spectrum')
#    print '        Failed'
# #
# # #
# # #

# # #
# print '    Import SMB 100A:'
# try:
#    smb_3 = qt.instruments.create('smb_3', 'SMB100A', address='TCPIP::192.168.10.6', reset=False)
#    print '        Succed'
# except:
#    qt.instruments.remove('smb_3')
#    print '        Failed'
# #
# print '    Import SMB 100A: probe source'
# try:
#    probe_src = qt.instruments.create('probe_src', 'SMB100A', address='TCPIP::10.0.0.50', reset=False)
#    print '        Succed'
# except:
#    qt.instruments.remove('probe_src')
#    print '        Failed'
# 10.0.0.40 for remy, 10.0.0.50 for luca
# # #
# #

#Yury:192.168.0.12
#Luca: 10.0.0.11


# print '    Import HP 83630A:'
# try:
#    smb_3 = qt.instruments.create('smb_3', 'HP83630A', address='TCPIP::192.168.10.58::gpib0,15', reset=False)
#    print '        Succed'
# except:
#    qt.instruments.remove('smb_3')
#    print '        Failed'

# print '    Import VNA MS46522B:'
# try:
#   VNA = qt.instruments.create('VNA', 'MS46522B', address='TCPIP::192.168.10.12', reset=False)
#   print '        Succed'
# except:
#   qt.instruments.remove('VNA')
#   print '        Failed'

# print '    Import VNA ZNB20:'
# try:
#   znb = qt.instruments.create('znb', 'ZNB20', address='TCPIP::192.168.10.9', reset=False)
#   print '        Succed'
# except:
#   qt.instruments.remove('znb')
#   print '        Failed'
# 192.168.0.9 address used by Javier and Nico
# previous :TCPIP::192.168.10.61

# print '    Import VNA ZVL13:'
# try:
#     zvl = qt.instruments.create('zvl', 'ZVL13', address='TCPIP::10.0.0.8', reset=False)
#     print '        Succed'
# except:
#     qt.instruments.remove('zvl')
#     print '        Failed'




# print '    Import Keithley 2400:'
# try:
#    keithley = qt.instruments.create('keithley', 'Keithley_2400', address='TCPIP::10.0.0.10::gpib0,24', reset=False)
#    keithley.set_parameter_bounds('current', -300e-3,300e-3)
#    print '        Succed'
# except:
#    qt.instruments.remove('keithley')
#    print '        Failed'


# #

# Remy: gpib0,9
# Luca: gpib0,17

# print '    Import AWG5014:'
# try:
   # awg5014 = qt.instruments.create('awg5014', 'Tektronix_AWG5014', address='TCPIP::10.0.0.12', reset=False)
   # print '        Succed'
# except:
   # qt.instruments.remove('awg5014')
   # print '        Failed'

# print '    Import LeCroy:'
# try:
   # lecroy = qt.instruments.create('lecroy', 'LeCroy_44Xi', address='TCPIP::10.0.0.15', )
   # print '        Succed'
# except:
   # qt.instruments.remove('lecroy')
   # print '        Failed'

#print ' Import MXA:'
#MXA = qt.instruments.create('MXA', 'Agilent_MXA', address='TCPIP::10.0.0.10::gpib0,18', reset=False)

#print ' Import iMACRT modules:'
#imac1 = qt.instruments.create('imac1', 'iMACRT', host='192.168.1.110',ch_names=['Still_CX2','Still_Ge_2Ohm','1K_Ge_4Ohm'])
# imac2 = qt.instruments.create('imac2', 'iMACRT', host='192.168.1.112',ch_names=['Cold_Plate_RuOx2','MXC_RuOx1','Sample_RuOx_Wolfgang'])
# pid1  = qt.instruments.create('pid1', 'iMACRT',  host='192.168.1.113')






#######################################################
#####              # Virtual instruments
#######################################################

print ''
print '######################################'
print '#'
print '#            Import of virtual devices'
print '#'
print '######################################'
print ''
# #
print '    Import SSB cavity'
try:
   SSB_cavity = qt.instruments.create('SSB_cavity', 'Virtual_SSB' )
   print '        Succed'
except:
   qt.instruments.remove('SSB_cavity')
   print '        Failed'

print '    Import SSB atom'
try:
   SSB_atom = qt.instruments.create('SSB_atom', 'Virtual_SSB' )
   print '        Succed'
except:
   qt.instruments.remove('SSB_atom')
   print '        Failed'
#

print '    Import SSB 3'
try:
   SSB_3 = qt.instruments.create('SSB_3', 'Virtual_SSB' )
   print '        Succed'
except:
   qt.instruments.remove('SSB_3')
   print '        Failed'


print '    Import Pulsing instrument'
try:
   Pulsing_instrument = qt.instruments.create('Pulsing_instrument', 'virtual_pulsing_instrument',
   awg='Tabor', mwsrc1='smb_1', board='ats9360',  ssb1 = 'SSB_cavity',
   mwsrc2= 'smb_2',ssb2='SSB_atom',
   # mwsrc3='smb_3', #!V commented 190302
   # ssb3='SSB_3'    # !V commented 191029
   )
   print '        Succed'
except:
   qt.instruments.remove('Pulsing_instrument')
   print '        Failed'


# print '    Import period'
# Period     = qt.instruments.create('Period', 'virtual_period',  pulser='pulser')
#
# print '    Import microwave pulse'
# Microwave_pulse = qt.instruments.create('Microwave_pulse', 'virtual_microwave_pulse',  pulser='pulser' , ch='A' ,mwsrc='RFsrc', period = 'Period')
#
# print '    Import probe pulse'
# Probe_pulse     = qt.instruments.create('Probe_pulse', 'virtual_probe_pulse',  pulser='pulser', probe_src='probe_src', period = 'Period')
# #
# # # # print '    Import probe pulse 2'
# # # # Probe_pulse_2     = qt.instruments.create('Probe_pulse_2', 'virtual_excitation_pulse',  pulser='pulser', mwsrc='HPsrc', period='Period')
# # #
# print '    Import homodyne-heterodyne detector'
# Detector        = qt.instruments.create('Detector', 'virtual_readout_IQ_multi', spectrum='Spectrum', mwsrc_read_out='LOsrc', pulser = 'pulser')
#
#
#
#
#
# print ''
# print '######################################'
# print '#'
# print '#            Import of qubit experiment'
# print '#'
# print '######################################'
# print ''
#

# import qubit_measurement_proc as QMP
# qm = QMP.qubit_measurement_proc()
#
# print " qubit experiment available under the object \"qm\""


# print ''
# print '######################################'
# print '#'
# print '#           Check for IP conflicts'
# print '#'
# print '######################################'
# print ''
#                                   DOESN'T WORK YET
# ip_list = []
# FLAG_conflict = False
# inst_dict = qt.instruments.get_instruments()
#
# for inst_name in qt.instruments.get_instrument_names():
#     print(inst_name)
#     inst = inst_dict[inst_name]
#     if not ('virtual' in inst.get_tags()):
#         ip = inst._ins._visainstrument.resource_name
#         if ip in ip_list:
#             print('Found an IP conflict at ', ip, '!!')
#         ip_list.append(address)
#
# if not FLAG_conflict:
#     print('No IP conflict found.')
#     print(ip_list)
