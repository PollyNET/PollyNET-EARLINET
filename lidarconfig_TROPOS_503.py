# Constants do not change at all. They are consistent over runs of the
# application and the plattform and the environment.

RAW_PATH= '//home/polly_crew/scc_convert/input_pxt_tropos/'

NEW_PATH= '//home/polly_crew/scc_access/depol_pxt_tropos/'
NEW_PATH_SCC= '//home/polly_crew/scc_access/pxt_tropos/'

from PyQt5 import QtGui

# Build chan-0 to chan_7 channames
CHANNEL_NAMES = {chan_id: "chan_%s" % chan_id for chan_id in range(12)}  # 12 instead of nine
CHANNEL_ID = [1388,1389,1390,1391,1392,1393,1394,1395,1396, 1397,1398,1399] #arielle developer scc
#pxt_tropos config: 355g, 355s, 387, 407, 532, 532s, 607, 1064, 532nf, 607nf, 355nf, 387nf



CHANNEL_ID_STR = [   #pxt_tropos developer scc
    'PXT_TROPOS_1', #355g
    'PXT_TROPOS_2', #355s
    'PXT_TROPOS_3', #387
    'PXT_TROPOS_4', #407
    'PXT_TROPOS_5', #532
    'PXT_TROPOS_6', #532s
    'PXT_TROPOS_7', #607
    'PXT_TROPOS_8', #1064
    'PXT_TROPOS_9', # 532nf
    'PXT_TROPOS_10', # 607nf
    'PXT_TROPOS_11', # 355 nf
    'PXT_TROPOS_12',]  # 387 nf

RANGE_ID = [1, 1, 1, 1, 1, 1, 1, 1, 0,  0, 0, 0] # 8 far range, 4 near range

BG_FIRST    = [0,    0,    0,    0,    0,    0,    0,    0,   0,  0,    0,   0 ]
BG_LAST     = [240,  240, 240,  240,  240,  240,  240,  240, 240,  240,  240, 240]

#OVL_ID      = ['',   '',  '_532', '_532s', '_607', '_1064', '', '', '']
#CHAN_NC_POS = [0,1,2,3,4,5,6,7,2]

OVL_ID = [
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '', 
    '',
    '',
    '']
CHAN_NC_POS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

#DOUBLE_CHAN = 2
NUM_DOUBLE_CHANNELS = 0

#depolcalibration settings
NUM_CAL_CHANNELS = 8
CAL_CHANNEL_SCC_ID =    [1400,1401,1402,1403,1404,1405,1406,1407] #scc developer version: 355g+45, 355s+45, 532g+45, 532s+45, 355g-45, 532g-45, 355s-45, 532s+45
CAL_CHANNEL_SCC_ID_STR =  ['PXT_TROPOS_13', 'PXT_TROPOS_14', 'PXT_TROPOS_15', 'PXT_TROPOS_16', 'PXT_TROPOS_17', 'PXT_TROPOS_18', 'PXT_TROPOS_18', 'PXT_TROPOS_20'] #scc test version: 532s+45, 532s-45, 532+45, 532-45


CAL_CHANNEL        =  [0,   1,   4,  5,  0,  4, 1, 5] #532s = channel 5, 532 = channel 4
CAL_IDX_RANGE      =  [0,   0,   0,   0,  1,   1,   1,   1] # 0 = first calibration # position, 1 = second calibration position
STR_CHANNEL = ["plus0", "plus1", "plus4", "plus5","minus0", "minus1", "minus4", "minus5"]
# calibration range for depol in ??METERS??
CALIB_RANGE_MIN = 1000
CALIB_RANGE_MAX = 3000

# rounded value of the variable 'depol_cal_angle' in case of normal measurement
CAL_ANGLE_MEASUREMENT = 999 # in case of arielle normally:0

LIGHT_SPEED = 3E8

NB_OF_TIME_SCALES = 1
NB_OF_SCAN_ANGLES = 1


GROUND_PRES = 1000.  # hPa
GROUND_TEMP = 15.  # degC

FIRST_VALID_BIN = 251

SCC_RAW_FILENAME_BODY = 'le_TROPOS'

SONDE_HEADER_STR = 'hPa'
SONDE_BOTTOM_STR = 'Station'



NC_FILL_INT = -2147483647
NC_FILL_FOAT = 9.9692099683868690e+36


STATION_ID = 'lei'

FILE_SIZE_RESTRICTION = 400000   #file size less than which files are ignored
FILE_DIVISION = 240  #how the file is devided, 720 = 6 hours, so 120 - one hour division
MOLECULAR_CALC = 2
 #0-standard atmosphere, 1 radio soudning, 2 - model data --> 2 standard
RAW_DATA_RANGE_RESOLUTION = 7.5
LASER_POINTING_ANGLE = 5
LASER_POINTING_ANGLE_of_PROFILES = 0
ID_timescale = 0
BACKGROUND_MODE = 0
LR_INPUT = 1
