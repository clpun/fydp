import sys
import numpy as np
import math
import time
import os
from enum import Enum
from csv import reader

sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']
class classifier_type(Enum):
    temporal_working_memory = 1
class Twm_stage(Enum):
    normal = 1
    encoding = 2
twm_dvs_lut = {}
twm_stage = Twm_stage.normal
twm_timer = 0.0
twm_timeout = 5.0
twm_encodingtime = 2.8
twm_stage1_vars = {}
twm_stage2_vars = {}

def load_decision_values(input_type, filename):
    if(input_type == classifier_type.temporal_working_memory):
        with open(filename, 'rU') as csv_file:
            data_reader = reader(csv_file)
            dvs1to2 = []
            dvs2to3 = []
            dvs1to3 = []
            first_row = True
            for row in data_reader:
                if first_row:
                    first_row = False
                    continue
                if int(row[6]) == 1:
                    if int(row[2]) == 1 and int(row[3]) == 2:
                        dvs1to2.append(tuple(row))
                    elif int(row[2]) == 2 and int(row[3]) == 3:
                        dvs2to3.append(tuple(row))
                    elif int(row[2]) == 1 and int(row[3]) == 3:
                        dvs1to3.append(tuple(row))
        twm_dvs_lut['dvs1to2'] = []
        twm_dvs_lut['dvs2to3'] = []
        twm_dvs_lut['dvs1to3'] = []
        twm_dvs_lut['dvs1to2'] = np.rec.array(dvs1to2,
                                     dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4'), ('DV', '<f8'), ('increase','<u1'), ('accepted','<u1')])
        twm_dvs_lut['dvs2to3'] = np.rec.array(dvs2to3,
                                     dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4'), ('DV', '<f8'), ('increase','<u1'), ('accepted','<u1')])
        twm_dvs_lut['dvs1to3'] = np.rec.array(dvs1to3,
                                     dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4'), ('DV', '<f8'), ('increase','<u1'), ('accepted','<u1')])
        # remove_field_name(twm_dvs_lut['dvs1to2'],'accepted')
        # remove_field_name(twm_dvs_lut['dvs2to3'],'accepted')
        # remove_field_name(twm_dvs_lut['dvs1to3'],'accepted')
        # remove_field_name(twm_dvs_lut['dvs1to2'],'C1')
        # remove_field_name(twm_dvs_lut['dvs2to3'],'C1')
        # remove_field_name(twm_dvs_lut['dvs1to3'],'C1')
        # remove_field_name(twm_dvs_lut['dvs1to2'],'C2')
        # remove_field_name(twm_dvs_lut['dvs2to3'],'C2')
        # remove_field_name(twm_dvs_lut['dvs1to3'],'C2')
        print "Successfully import user's decision values = " + str(twm_dvs_lut)

def remove_field_name(array, name):
    names = list(array.dtype.names)
    if name in names:
        names.remove(name)
    return array[names]

# Temporal Working Memory Classifier
def twm_classifier(ffts_tminus1,ffts_t):
    global twm_stage1_vars
    global twm_stage2_vars
    global twm_stage
    global twm_timer
    # print "twm time.time = " + str(time.time()) + " stage = " + str(twm_stage)
    if twm_stage == Twm_stage.normal:
        if(check_dvs(classifier_type.temporal_working_memory,ffts_tminus1,ffts_t,'dvs1to2')):
            # for sensor in sensor_names:
            #     twm_stage1_vars[sensor] = {}
            #     twm_stage2_vars[sensor] = {}
            #     for ii in range(0,len(ffts_tminus1)-1):
            #         twm_stage1_vars[sensor][str(ii)] = ffts_tminus1[sensor][str(ii)]
            #         twm_stage2_vars[sensor][str(ii)] = ffts_t[sensor][str(ii)]
            twm_stage = Twm_stage.encoding
            twm_timer = time.time()
            print "twm encode = " + str(twm_timer)
    elif twm_stage == Twm_stage.encoding:
        if(time.time() - twm_timer > twm_timeout):
            print "twm timeout"
            twm_stage = Twm_stage.normal
        elif(check_dvs(classifier_type.temporal_working_memory,ffts_tminus1,ffts_t,'dvs2to3') and
            check_dvs(classifier_type.temporal_working_memory,ffts_tminus1,ffts_t,'dvs1to3')):
            if(time.time() - twm_timer > twm_encodingtime):
                return True
            print "twm control before encoding time"
            twm_stage = Twm_stage.normal
    return False

def check_dvs(input_type, ffts_tminus1, ffts_t, condition):
    if input_type == classifier_type.temporal_working_memory:
        pos = 0
        neg = 0
        if condition == 'dvs1to2':
            for ii in twm_dvs_lut[condition]:
                satisfy = False
                channel = ii[0]
                frequency = str(ii[1])
                dv = float(ii[4])
                increase = int(ii[5])
                if(increase == 1):
                    # check if greater than
                    if(ffts_t[channel][frequency] > dv):
                        satisfy = True
                elif(increase == 0):
                    # check if smaller than
                    if(ffts_t[channel][frequency] < dv):
                        satisfy = True
                else:
                    print "Error reading decision values = " + str(ii)
                if satisfy:
                    pos += 1
                else:
                    neg += 1
            if (float(pos-neg)/float(pos+neg)) > 0.75:
                # print "pos = " + str(pos)
                # print "neg = " + str(neg)
                return True
            else:
                return False
        elif condition == 'dvs2to3':
            for ii in twm_dvs_lut[condition]:
                satisfy = False
                channel = ii[0]
                frequency = str(ii[1])
                dv = float(ii[4])
                increase = int(ii[5])
                if(increase == 1):
                    # check if greater than
                    if(ffts_t[channel][frequency] > dv):
                        satisfy = True
                elif(increase == 0):
                    # check if smaller than
                    if(ffts_t[channel][frequency] < dv):
                        satisfy = True
                else:
                    print "Error reading decision values = " + str(ii)
                if satisfy:
                    pos += 1
                else:
                    neg += 1
            if (float(pos-neg)/float(pos+neg)) > 0.75:
                # print "pos = " + str(pos)
                # print "neg = " + str(neg)
                return True
            else:
                return False
        elif condition == 'dvs1to3':
            for ii in twm_dvs_lut[condition]:
                satisfy = False
                channel = ii[0]
                frequency = str(ii[1])
                dv = float(ii[4])
                increase = int(ii[5])
                if(increase == 1):
                    # check if greater than
                    if(ffts_t[channel][frequency] > dv):
                        satisfy = True
                elif(increase == 0):
                    # check if smaller than
                    if(ffts_t[channel][frequency] < dv):
                        satisfy = True
                else:
                    print "Error reading decision values = " + str(ii)
                if satisfy:
                    pos += 1
                else:
                    neg += 1
            if (float(pos-neg)/float(pos+neg)) > 0.75:
                # print "pos = " + str(pos)
                # print "neg = " + str(neg)
                return True
            else:
                return False
        else:
            print "Cannot check decision values of condition = " + str(condition)
            return False
    else:
        print "No decision values for input type = " + str(input_type)
        return False