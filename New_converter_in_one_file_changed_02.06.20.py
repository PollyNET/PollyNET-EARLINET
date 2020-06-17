import os
import netCDF4
import numpy as np
import os, fnmatch
import xarray as xray
import math
from netCDF4 import Dataset


import sys
print(sys.argv[0]) # prints python_script.py
print(sys.argv[1]) # prints var1
#print sys.argv[2] # prints var2


exec(sys.argv[1])    



# import lidarconfig_arielle as ld
# import lidarconfig_default_polly as ld


# import lidarconfig_lacros as ld


for name in fnmatch.filter(os.listdir(path=ld.RAW_PATH), '*.nc'):
    print(name)

    print(os.path.getsize(ld.RAW_PATH + name))

    if os.path.getsize(
            ld.RAW_PATH + name) < ld.FILE_SIZE_RESTRICTION:  ###Checking if the file size small enough to ignore the file
        print(name + "  " + "Input file is too small")
        continue

    print(name)
    # dt.depol(name)
    r = Dataset(ld.RAW_PATH + name)  ### opening raw file


    def depol():  # here put name
        # for name in os.listdir(path=ld.RAW_PATH):
        print("name for depol", name)
        print("doing depol")

        calib = []  # list for number of depol
        depol_angle = []  # concrete time for calib
        depol_angle_plus = []  # +45
        depol_angle_minus = []  # -45
        # r = Dataset(ld.RAW_PATH + name)  # raw file

        for i in range(r.dimensions['time'].size):
            if str(r.variables['depol_cal_angle'][i]) == 'nan':  # comment 15.10.2019, if nan in cal_angle_measur
                break
            if int(r.variables['depol_cal_angle'][i]) != ld.CAL_ANGLE_MEASUREMENT:
                calib.append(i)  # defining calib
        zero_shot = []
        # print(calib)

        if len(calib) != 0:
            print('DEPOL')
            for i in range(len(calib)):
                for j in range(r.dimensions['channel'].size):
                    if r.variables['measurement_shots'][i, j] == 0:
                        continue

            d = Dataset(ld.NEW_PATH + 'depol' + "_" + name, 'w')  # new file
            d.createDimension('channels', ld.NUM_CAL_CHANNELS)
            depol_angle = r.variables['depol_cal_angle'][calib[0]:calib[-1]]  # defining depol

            #####values for +/- depol
            # print(calib)
            for i in range(len(calib)):
                while depol_angle[i] == depol_angle[i + 1]:
                    depol_angle_plus.append(calib[i])
                    i = i + 1
                else:
                    depol_angle_plus.append(calib[i])
                    depol_angle_minus = calib[i + 1:-1]
                    break
            first_channel = []

            if len(depol_angle_minus) > len(depol_angle_plus):
                diff = len(depol_angle_minus) - len(depol_angle_plus)
                for i in range(diff):
                    del depol_angle_minus[-i]
            elif len(depol_angle_plus) > len(depol_angle_minus):
                diff = len(depol_angle_plus) - len(depol_angle_minus)
                for i in range(diff):
                    del depol_angle_plus[-i]

            del depol_angle_plus[-1]  # del first and last depol time
            del depol_angle_plus[0]
            del depol_angle_minus[-1]
            del depol_angle_minus[0]
            # if len(depol_angle_plus) != len(depol_angle_minus):

            print("depol_plus", depol_angle_plus, "depol_min", depol_angle_minus)
            d.createDimension('time', len(depol_angle_plus))
            cal_set = set(ld.CAL_CHANNEL)
            result = set(ld.CAL_CHANNEL) ^ set(ld.CHAN_NC_POS)  # finding channels needed for depol
            print(cal_set)

            ### equling the number of +/- depol calib

            ### reopening for transpose, creating raw_data
            def raw_data():
                r_old = xray.open_dataset(ld.RAW_PATH + name)
                r_old1 = r_old['raw_signal'].transpose('time', 'channel', 'height')
                raw_signal_array = np.zeros((r.dimensions["time"].size, r.dimensions['channel'].size,
                                             r.dimensions["height"].size))  # creating numpy array from raw file
                raw_signal_array[:][:][:] = r_old1[:, :, :]  # creating numpy array from raw file
                # if r.dimensions['channel'].size != len(ld.CHANNEL_ID):  # cheking for more channels
                #   raw_signal_array = np.delete(raw_signal_array, (12), 1)#del them
                raw_signal_array = np.delete(raw_signal_array, list(result), 1)  # deleting channels useless for depol
                arrays = []

                raw_signal_array_plus = raw_signal_array[depol_angle_plus[0]:depol_angle_plus[-1] + 1, :, :]
                list_initial = []
                for i in cal_set:
                    list_initial.append("plus" + str(i))
                # print(list_initial)

                raw_signal_array_minus = raw_signal_array[depol_angle_minus[0]:depol_angle_minus[-1] + 1, :, :]
                for i in cal_set:
                    list_initial.append("minus" + str(i))
                print("list_initial", list_initial)

                plus_list = []
                print(ld.NUM_CAL_CHANNELS / 2)
                for j in range(int(ld.NUM_CAL_CHANNELS / 2)):
                    plus_list.append(raw_signal_array_plus[:, j, :])
                print(plus_list[0][:, 250])
                print(plus_list[1][:, 250])

                for j in range(int(ld.NUM_CAL_CHANNELS / 2)):
                    plus_list.append(raw_signal_array_minus[:, j, :])
                print(plus_list[2][:, 250])
                print(plus_list[3][:, 250])

                array_full = np.zeros(
                    (raw_signal_array_plus.shape[0], ld.NUM_CAL_CHANNELS, r.dimensions['height'].size))
                print(array_full.shape)

               
                list_index = []
                print(list_initial)
                for i in ld.STR_CHANNEL:
                    list_index.append(list_initial.index(i))
                

                # for a in sorted(ld.STR_CHANNEL.values()):
                #   print(a)
                for i in range(raw_signal_array_plus.shape[0]):

                    for j in range(0, len(ld.CAL_CHANNEL)):

                        for k in range(r.dimensions['height'].size):
                            array_full[i, j, k] = plus_list[list_index[j]][i, k]

                

                d.createDimension('points', r.dimensions['height'].size)
                d.createVariable('Raw_Lidar_Data', float, ('time', 'channels', 'points'), zlib=True)
                
                d.variables['Raw_Lidar_Data'][:, :, :] = array_full[:, :, :]  # writing netcdf
                # print("minus", raw_signal_array_minus[:, :, 250])
                return list_index

            list_in = []
            list_in = raw_data()

            ### same for laser shots

            def laser_shots():
                laser_shots_array = np.zeros((r.dimensions["time"].size, r.dimensions['channel'].size))
                laser_shots_array[:][:] = r.variables["measurement_shots"][:][:]
                # if r.dimensions['channel'].size != len(ld.CHANNEL_ID):
                #   laser_shots_array = np.delete(laser_shots_array, (12), 1)
                laser_shots_array = np.delete(laser_shots_array, list(result), 1)

                laser_shots_array_minus = laser_shots_array[depol_angle_minus[0]:depol_angle_minus[-1] + 1][:]
                # laser_shots_array_minus = np.flip(laser_shots_array_minus,1)
                laser_shots_array_plus = laser_shots_array[depol_angle_plus[0]:depol_angle_plus[-1] + 1][:]
                # laser_shots_array_plus = np.flip(laser_shots_array_plus,1)

                plus_laser_list = []
                print(ld.NUM_CAL_CHANNELS / 2)
                for j in range(int(ld.NUM_CAL_CHANNELS / 2)):
                    plus_laser_list.append(laser_shots_array_plus[:, j])

                for j in range(int(ld.NUM_CAL_CHANNELS / 2)):
                    plus_laser_list.append(laser_shots_array_minus[:, j])

                array_full_laser = np.zeros((laser_shots_array_plus.shape[0], ld.NUM_CAL_CHANNELS))
                #                print(array_full.shape)

                for i in range(laser_shots_array_plus.shape[0]):

                    for j in range(0, len(ld.CAL_CHANNEL)):
                        array_full_laser[i, j] = plus_laser_list[list_in[j]][i]

                # laser_shots_array_minus = np.insert(laser_shots_array_minus, (0,1), laser_shots_array_plus, 1)
                d.createVariable('Laser_Shots', np.int32, ('time', 'channels'), zlib=True)
                d.variables['Laser_Shots'][:, :] = array_full_laser

            laser_shots()

            def start_stop_time():
                start_time = []
                for i in range(len(depol_angle_plus)):
                    start_time.append((r.variables['measurement_time'][depol_angle_plus[i], 1] -
                                       r.variables['measurement_time'][depol_angle_plus[0], 1]))  # writing start time

                stop_time = []
                for i in range(len(depol_angle_minus)):
                    stop_time.append(
                        r.variables['measurement_time'][depol_angle_minus[i], 1] - r.variables['measurement_time'][
                            depol_angle_plus[0], 1])
                del stop_time[0]
                stop_time.append(stop_time[-1] + r.variables['measurement_time'][depol_angle_minus[-1], 1] -
                                 r.variables['measurement_time'][depol_angle_minus[-2], 1])  # writing stop time

                d.createDimension('nb_of_time_scales', ld.NB_OF_TIME_SCALES)
                d.createVariable('Raw_Data_Start_Time', np.int32, ('time', 'nb_of_time_scales'))
                d.createVariable('Raw_Data_Stop_Time', np.int32, ('time', 'nb_of_time_scales'))
                d.variables['Raw_Data_Start_Time'][:] = start_time[:]
                d.variables['Raw_Data_Stop_Time'][:] = stop_time[:]

            start_stop_time()

            ##### creating ID stuff
            def time_ID():
                hour_start = int(r.variables['measurement_time'][depol_angle_plus[0], 1] / 3600)
                min_start = int((r.variables['measurement_time'][depol_angle_plus[0], 1] - hour_start * 3600) / 60)
                sec_start = int(
                    r.variables['measurement_time'][depol_angle_plus[0], 1] - hour_start * 3600 - min_start * 60)

                hour_start = str(hour_start)
                min_start = str(min_start)
                sec_start = str(sec_start)

                if len(str(hour_start)) < 2:
                    hour_start = '0' + hour_start

                if len(str(min_start)) < 2:
                    min_start = '0' + min_start

                if len(str(sec_start)) < 2:
                    sec_start = '0' + sec_start

                hour_stop = int(r.variables['measurement_time'][depol_angle_minus[-1], 1] / 3600)
                min_stop = int((r.variables['measurement_time'][depol_angle_minus[-1], 1] - hour_stop * 3600) / 60)
                sec_stop = int(
                    r.variables['measurement_time'][depol_angle_minus[-1], 1] - hour_stop * 3600 - min_stop * 60)

                hour_stop = str(hour_stop)
                min_stop = str(min_stop)
                sec_stop = str(sec_stop)

                if len(str(hour_stop)) < 2:
                    hour_stop = '0' + hour_stop

                if len(str(min_stop)) < 2:
                    min_stop = '0' + min_stop

                if len(str(sec_stop)) < 2:
                    sec_stop = '0' + sec_stop

                d.Measurement_ID = str(r.variables['measurement_time'][1, 0]) + 'lei' + str(hour_start) + str(min_start)
                d.RawData_Start_Date = str(r.variables['measurement_time'][1, 0])
                d.RawData_Start_Time_UT = hour_start + min_start + sec_start
                d.RawData_Stop_Time_UT = hour_stop + min_stop + sec_stop
                d.Comment = ""

            time_ID()

            def create_variables():

                d.createVariable('ID_Range', np.int32, ('channels'))
                d.variables['ID_Range'][:] = ld.RANGE_ID[0:d.dimensions['channels'].size]

                d.createVariable('Background_High', float, 'channels', )
                d.variables['Background_High'][:] = ld.BG_LAST[0:d.dimensions['channels'].size]

                d.createVariable('Background_Low', float, 'channels', )
                d.variables['Background_Low'][:] = ld.BG_FIRST[0:d.dimensions['channels'].size]

                d.createVariable('channel_ID', np.int32, 'channels', )
                d.variables['channel_ID'][:] = ld.CAL_CHANNEL_SCC_ID

                d.createVariable('id_timescale', np.int32, 'channels')
                d.variables['id_timescale'][:] = ld.ID_timescale

                d.createVariable('Background_Mode', np.int32, 'channels')
                d.variables['Background_Mode'][:] = ld.BACKGROUND_MODE

                d.createVariable('Laser_Pointing_Angle_of_Profiles', np.int32, ('time', 'nb_of_time_scales'))
                d.variables['Laser_Pointing_Angle_of_Profiles'][:] = ld.LASER_POINTING_ANGLE_of_PROFILES

                d.createVariable('LR_Input', np.int32, 'channels')
                d.variables['LR_Input'][:] = ld.LR_INPUT

                d.createVariable('Raw_Data_Range_Resolution', float, 'channels')
                d.variables['Raw_Data_Range_Resolution'][:] = ld.RAW_DATA_RANGE_RESOLUTION

                d.createVariable('Molecular_Calc', np.int32)
                d.variables['Molecular_Calc'][:] = ld.MOLECULAR_CALC

                d.createVariable('Pressure_at_Lidar_Station', float)
                d.variables['Pressure_at_Lidar_Station'][:] = ld.GROUND_PRES

                d.createVariable('Pol_Calib_Range_Max', float, 'channels')
                d.variables['Pol_Calib_Range_Max'][:] = ld.CALIB_RANGE_MAX

                d.createVariable('Pol_Calib_Range_Min', float, 'channels')
                d.variables['Pol_Calib_Range_Min'][:] = ld.CALIB_RANGE_MIN

                d.createVariable('Temperature_at_Lidar_Station', float)
                d.variables['Temperature_at_Lidar_Station'][:] = ld.GROUND_TEMP

                d.createVariable('channel_string_ID', str, 'channels')
                for i in range(ld.NUM_CAL_CHANNELS):
                    d.variables['channel_string_ID'][i] = ld.CAL_CHANNEL_SCC_ID_STR[i]

                d.createDimension('scan_angles', ld.NB_OF_SCAN_ANGLES)

                d.createVariable('Laser_Pointing_Angle', float, 'scan_angles')
                d.variables['Laser_Pointing_Angle'][:] = ld.LASER_POINTING_ANGLE

                return 1

            create_variables()
            # depol()
            d.close()
        # r.close()


    depol()

    # calling depol program put name here

    number_hours = ld.FILE_DIVISION  # this value can be taken from config, here it is just hour cutting
    start = 0  # initial values for start and end time for every one-hour files
    end = ld.FILE_DIVISION

    ####### this block counting the number of zero shots and if all of them empty - file is ignored

    zero_shot = []
    for i in range(r.dimensions['time'].size):
        for j in range(r.dimensions['channel'].size):
            if r.variables['measurement_shots'][i, j] == 0:
                zero_shot.append(i)
    if all(zero_shot) == 0:
        print("All laser shots empty!")
        continue
    #######

    ####### this block shows number of divisions of one files, e.g number of one-hour files, also this for cycle makes snall files from residues
    number_of_cycles = math.ceil(r.dimensions['time'].size / number_hours)
    print("Number of cycles in one file:", number_of_cycles)

    for hour in range(number_of_cycles):
        res = r.dimensions['time'].size - end
        print("Residue:", res)
        if res < 0:
            #break                                                      ### now no small files, only 2 hours
            number_hours = number_hours - np.abs(res)
            end = r.dimensions['time'].size
        time = []  # defining time dimension
        hour_start = int(r.variables['measurement_time'][start, 1] / 3600)
        min_start = int((r.variables['measurement_time'][start, 1] - hour_start * 3600) / 60)

        d = Dataset(
            ld.NEW_PATH_SCC + str(r.variables['measurement_time'][1, 0]) + ld.STATION_ID + str(hour_start) + str(
                min_start) + '.nc', 'w')  # creating new file

        #############

        ###### defining time var from number of one-hour cycle
        for sec in range(number_hours):
            time.append(sec)

        calib = []  # list for depol time

        # print(r)
        d.createDimension('points', r.dimensions['height'].size)  ## creating points dimension
        d.createDimension('channels', len(ld.CHANNEL_ID))  ## creating channels dimension
        if 'depol_cal_angle' not in globals():
            print("wert")
        ##### cycle for detecting calibration periods to cut them out.
        for i in range(start, end):
            if 'depol_cal_angle' in globals():
                if int(r.variables['depol_cal_angle'][i]) > ld.CAL_ANGLE_MEASUREMENT:
                    calib.append(i)
        print("Depol:", len(calib))
        print(calib)

        #####

        ##### redefining calib indecies because of time shifting and one hour cutting
        if len(calib) != 0:  # shift for calib, because one hour cutting with shift

            # for i in range(720/ld.FILE_DIVISION):

            if calib[0] < 120:
                shift = 0
            elif calib[0] < 240:
                shift = 120
            elif calib[0] < 360:
                shift = 240
            elif calib[0] < 480:
                shift = 360
            elif calib[0] < 600:
                shift = 480
            else:
                shift = 600

            for i in range(len(calib)):
                calib[i] = calib[i] - shift


        #####

        ##### creating and defining variable Laser Shots
        def laser_shots():
            laser_shots_array = np.zeros((number_hours, r.dimensions["channel"].size))
            laser_shots_array[:, :] = r.variables["measurement_shots"][start:end, :]
            if r.dimensions['channel'].size != len(ld.CHANNEL_ID):  # cheking for more channels
                laser_shots_array = np.delete(laser_shots_array, (12), 1)  # del them
            print((calib))
            print(laser_shots_array.shape)
            laser_shots_array = np.delete(laser_shots_array, (calib), 0)
            print(laser_shots_array.shape)
            print("Start:", start, "End:", end)

            #### block for redefining zero laser shots, according to this new array without calibration period
            zero_shot1 = []
            for i in range(laser_shots_array.shape[0]):
                for j in range(len(ld.CHANNEL_ID)):
                    if laser_shots_array[i, j] == 0:
                        zero_shot1.append(i)
            print("Set of zero shots:", (set(zero_shot1)))
            ####
            laser_shots_array = np.delete(laser_shots_array, (zero_shot1), 0)  #### deleting these zero laser shots

            print("Length of calib:", len(calib))
            print("Shape of laser shots array:", laser_shots_array.shape)

            d.createDimension('time', len(time) - len(calib) - len(
                set(zero_shot1)))  ### creating time dimension without calibration period and zeto laser shots
            d.createVariable('Laser_Shots', np.int32, ('time', 'channels'), zlib=True)

            d.variables['Laser_Shots'][:, :] = laser_shots_array[:, :]
            return list(set(zero_shot1))  #### returning zero list laser shots for time variable


        shots = []
        shots = laser_shots()

        print("Zero shots:", shots)


        #### creating and defining raw_signal variable
        def raw_signal():

            r_old = xray.open_dataset(ld.RAW_PATH + name)
            raw_signal_array = np.zeros((number_hours, r.dimensions["channel"].size,
                                         r.dimensions["height"].size))  ### coping netcdf array to numpy array

            r_old1 = r_old['raw_signal'].transpose('time', 'channel', 'height')  #### transpose initial array
            raw_signal_array[:, :, :] = r_old1[start:end, :, :]

            if r.dimensions['channel'].size != len(ld.CHANNEL_ID):  # cheking for more channels
                raw_signal_array = np.delete(raw_signal_array, (12), 1)  # del them

            raw_signal_array = np.delete(raw_signal_array, (calib), 0)  ### deleting calibration period
            print("Shape of raw signal array:", raw_signal_array.shape)

            raw_signal_array = np.delete(raw_signal_array, (shots), 0)
            d.createVariable('Raw_Lidar_Data', float, ('time', 'channels', 'points'), zlib=True)
            d.variables['Raw_Lidar_Data'][:, :, :] = raw_signal_array[:, :, :]

            return 1


        raw_signal()


        #### creating stop and start times by making list with 30 interval

        def gap_correction():
            measur_time = []
            for i in range(0, max(len(time) - 1, 1)):
                measur_time.append(
                    (r.variables['measurement_time'][i + 1, 1] - (r.variables['measurement_time'][i, 1])))

            j = 0
            list_measer_start_time = [0]
            list_measer_stop_time = [int(np.mean(measur_time))]
            for k in range(0, len(time) - 1):
                j1 = j + int(np.mean(measur_time))
                j = j1
                list_measer_start_time.append(j)
                list_measer_stop_time.append(j + int(np.mean(measur_time)))
            d.createDimension('nb_of_time_scales', ld.NB_OF_TIME_SCALES)
            d.createVariable('Raw_Data_Start_Time', np.int32, ('time', 'nb_of_time_scales'))
            d.createVariable('Raw_Data_Stop_Time', np.int32, ('time', 'nb_of_time_scales'))

            start_time = np.zeros((len(list_measer_start_time)))
            stop_time = np.zeros((len(list_measer_stop_time)))
            start_time[:] = list_measer_start_time[:]
            stop_time[:] = list_measer_stop_time[:]

            start_time = np.delete(start_time, (calib))
            stop_time = np.delete(stop_time, (calib))

            start_time = np.delete(start_time, (shots))
            stop_time = np.delete(stop_time, (shots))

            d.variables['Raw_Data_Start_Time'][:] = start_time[:]
            d.variables['Raw_Data_Stop_Time'][:] = stop_time[:]

            return 1


        gap_correction()


        #### creating variables which values are taken from config file
        def create_variables():

            d.createVariable('ID_Range', np.int32, ('channels'))
            d.variables['ID_Range'][:] = ld.RANGE_ID

            d.createVariable('Background_High', float, 'channels', )
            d.variables['Background_High'][:] = ld.BG_LAST

            d.createVariable('Background_Low', float, 'channels', )
            d.variables['Background_Low'][:] = ld.BG_FIRST

            d.createVariable('channel_ID', np.int32, 'channels', )
            d.variables['channel_ID'][:] = ld.CHANNEL_ID

            d.createVariable('id_timescale', np.int32, 'channels')
            d.variables['id_timescale'][:] = ld.ID_timescale

            d.createVariable('Background_Mode', np.int32, 'channels')
            d.variables['Background_Mode'][:] = ld.BACKGROUND_MODE

            d.createVariable('Laser_Pointing_Angle_of_Profiles', np.int32, ('time', 'nb_of_time_scales'))
            d.variables['Laser_Pointing_Angle_of_Profiles'][:] = ld.LASER_POINTING_ANGLE_of_PROFILES

            d.createVariable('LR_Input', np.int32, 'channels')
            d.variables['LR_Input'][:] = ld.LR_INPUT

            d.createVariable('First_Signal_Rangebin', np.int32, 'channels')
            d.variables['First_Signal_Rangebin'][:] = ld.FIRST_VALID_BIN

            d.createVariable('Raw_Data_Range_Resolution', float, 'channels')
            d.variables['Raw_Data_Range_Resolution'][:] = ld.RAW_DATA_RANGE_RESOLUTION

            d.createVariable('Molecular_Calc', np.int32)
            d.variables['Molecular_Calc'][:] = ld.MOLECULAR_CALC

            d.createVariable('Pressure_at_Lidar_Station', float)
            d.variables['Pressure_at_Lidar_Station'][:] = ld.GROUND_PRES

            d.createVariable('Temperature_at_Lidar_Station', float)
            d.variables['Temperature_at_Lidar_Station'][:] = ld.GROUND_TEMP

            d.createVariable('channel_string_ID', str, 'channels')
            for i in range(d.dimensions['channels'].size):
                d.variables['channel_string_ID'][i] = ld.CHANNEL_ID_STR[i]

            d.createDimension('scan_angles', ld.NB_OF_SCAN_ANGLES)

            d.createVariable('Laser_Pointing_Angle', float, 'scan_angles')
            d.variables['Laser_Pointing_Angle'][:] = ld.LASER_POINTING_ANGLE

            return 1


        create_variables()


        #### creating ID stuff
        def time_ID():
            hour_start = int(r.variables['measurement_time'][start, 1] / 3600)
            min_start = int((r.variables['measurement_time'][start, 1] - hour_start * 3600) / 60)
            sec_start = int(r.variables['measurement_time'][start, 1] - hour_start * 3600 - min_start * 60)

            hour_start = str(hour_start)
            min_start = str(min_start)
            sec_start = str(sec_start)

            if len(str(hour_start)) < 2:
                hour_start = '0' + hour_start

            if len(str(min_start)) < 2:
                min_start = '0' + min_start

            if len(str(sec_start)) < 2:
                sec_start = '0' + sec_start
            hour_stop = int(r.variables['measurement_time'][end - 1, 1] / 3600)
            min_stop = int((r.variables['measurement_time'][end - 1, 1] - hour_stop * 3600) / 60)
            sec_stop = int(
                r.variables['measurement_time'][end - 1, 1] - hour_stop * 3600 - min_stop * 60)

            hour_stop = str(hour_stop)
            min_stop = str(min_stop)
            sec_stop = str(sec_stop)

            if len(str(hour_stop)) < 2:
                hour_stop = '0' + hour_stop

            if len(str(min_stop)) < 2:
                min_stop = '0' + min_stop

            if len(str(sec_stop)) < 2:
                sec_stop = '0' + sec_stop

            d.Measurement_ID = str(r.variables['measurement_time'][1, 0]) + ld.STATION_ID + str(hour_start) + str(
                min_start)
            d.RawData_Start_Date = str(r.variables['measurement_time'][1, 0])
            d.RawData_Start_Time_UT = hour_start + min_start + sec_start
            d.RawData_Stop_Time_UT = hour_stop + min_stop + sec_stop
            d.Comment = ""


        time_ID()
        start = start + number_hours
        end = end + number_hours

        d.close()



