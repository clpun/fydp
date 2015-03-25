import sys
import numpy as np
import math
import time
import os
from enum import Enum
from csv import reader
from scipy.stats import norm

sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']
class classifier_type(Enum):
    temporal_working_memory = 1
class Twm_stage(Enum):
    normal = 1
    encoding = 2
twm_mean_dvs_lut = {}
twm_minmax_dvs_lut = {}
twm_stage = Twm_stage.normal
twm_timer = 0.0
twm_timeout = 5.0
twm_encodingtime = 2.8
twm_stage1_vars = {}
twm_stage2_vars = {}

def load_minmax_decision_values(input_type, filename):
    global twm_minmax_dvs_lut
    if(input_type == classifier_type.temporal_working_memory):
        with open(filename, 'rU') as csv_file:
            data_reader = reader(csv_file)
            dvs_minmax = []
            first_row = True
            for row in data_reader:
                if first_row:
                    first_row = False
                    continue
                dvs_minmax.append(tuple(row))
        twm_minmax_dvs_lut = np.rec.array(dvs_minmax,
                                dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4'), ('DV', '<f8')])
        print "Successfully import user's min max twm decision values = " + str(twm_minmax_dvs_lut)

def load_mean_decision_values(input_type, filename):
    global twm_mean_dvs_lut
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
        twm_mean_dvs_lut['dvs1to2'] = []
        twm_mean_dvs_lut['dvs2to3'] = []
        twm_mean_dvs_lut['dvs1to3'] = []
        twm_mean_dvs_lut['dvs1to2'] = np.rec.array(dvs1to2,
                                     dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4'), ('DV', '<f8'), ('increase','<u1'), ('accepted','<u1')])
        twm_mean_dvs_lut['dvs2to3'] = np.rec.array(dvs2to3,
                                     dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4'), ('DV', '<f8'), ('increase','<u1'), ('accepted','<u1')])
        twm_mean_dvs_lut['dvs1to3'] = np.rec.array(dvs1to3,
                                     dtype=[('CH', '|S8'), ('frequency', '<i4'), ('C1', '<i4'), ('C2', '<i4'), ('DV', '<f8'), ('increase','<u1'), ('accepted','<u1')])
        # remove_field_name(twm_mean_dvs_lut['dvs1to2'],'accepted')
        # remove_field_name(twm_mean_dvs_lut['dvs2to3'],'accepted')
        # remove_field_name(twm_mean_dvs_lut['dvs1to3'],'accepted')
        # remove_field_name(twm_mean_dvs_lut['dvs1to2'],'C1')
        # remove_field_name(twm_mean_dvs_lut['dvs2to3'],'C1')
        # remove_field_name(twm_mean_dvs_lut['dvs1to3'],'C1')
        # remove_field_name(twm_mean_dvs_lut['dvs1to2'],'C2')
        # remove_field_name(twm_mean_dvs_lut['dvs2to3'],'C2')
        # remove_field_name(twm_mean_dvs_lut['dvs1to3'],'C2')
        print "Successfully import user's twm mean decision values = " + str(twm_mean_dvs_lut)

def remove_field_name(array, name):
    names = list(array.dtype.names)
    if name in names:
        names.remove(name)
    return array[names]

# Temporal Working Memory Mean Classifier
def twm_mean_classifier(ffts_t,ffts_circbufferindex):
    global twm_stage1_vars
    global twm_stage2_vars
    global twm_stage
    global twm_timer
    # print "twm time.time = " + str(time.time()) + " stage = " + str(twm_stage)
    if twm_stage == Twm_stage.normal:
        if(check_mean_dvs(classifier_type.temporal_working_memory,ffts_t,ffts_circbufferindex,'dvs1to2')):
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
        elif(check_mean_dvs(classifier_type.temporal_working_memory,ffts_t,ffts_circbufferindex,'dvs2to3') and
            check_mean_dvs(classifier_type.temporal_working_memory,ffts_t,ffts_circbufferindex,'dvs1to3')):
            if(time.time() - twm_timer > twm_encodingtime):
                return True
            print "twm control before encoding time"
            twm_stage = Twm_stage.normal
    return False

'''
    This function should be called once. Right after the Encoding Session is done
'''
# Temporal Working Memory Min Max Classifier
def twm_minmax_classifier(ffts_t,ffts_circbufferindex,control_lbound,control_ubound,encoding_lbound,encoding_ubound):
    if(check_minmax_dvs(classifier_type.temporal_working_memory,ffts_t,ffts_circbufferindex,control_lbound,control_ubound,encoding_lbound,encoding_ubound)):
        return True
    else:
        return False

def check_minmax_dvs(input_type,ffts_t,ffts_circbufferindex,control_lbound,control_ubound,encoding_lbound,encoding_ubound):
    if(input_type == classifier_type.temporal_working_memory):
        pos = 0
        neg = 0
        for ii in twm_minmax_dvs_lut:
            satisfy = False
            channel = ii[0]
            frequency = int(ii[1])
            dscale = float(ii[4])
            control_minmaxdiff = check_minmaxdiff(ffts_t,ffts_circbufferindex,channel,frequency,control_lbound,control_ubound)
            encoding_minmaxdiff = check_minmaxdiff(ffts_t,ffts_circbufferindex,channel,frequency,encoding_lbound,encoding_ubound)
            control_std = check_std(ffts_t,ffts_circbufferindex,channel,frequency,control_lbound,control_ubound)
            encoding_std = check_std(ffts_t,ffts_circbufferindex,channel,frequency,encoding_lbound,encoding_ubound)
            # print "ii = " + str(ii)
            # print "control_std = " + str(control_std)
            # print "encoding_std = " + str(encoding_std)
            #if(control_minmaxdiff/encoding_minmaxdiff >= dscale):
            #    satisfy = True
            if(control_std/encoding_std >= 1):
                 satisfy = True
            if(satisfy):
                print str(ii) + " : +"
                pos += 1
            else:
                print str(ii) + " : -"
                neg += 1
        print "pos = " + str(pos)
        print "neg = " + str(neg)
        if (float(pos)/float(pos+neg)) > 0.70:
            return True
        else:
            return False
    else:
        print "No decision values for input type = " + str(input_type)
        return False

def check_mean_dvs(input_type, ffts_t, ffts_circbufferindex, condition):
    if input_type == classifier_type.temporal_working_memory:
        pos = 0
        neg = 0
        if condition == 'dvs1to2':
            for ii in twm_mean_dvs_lut[condition]:
                satisfy = False
                channel = ii[0]
                frequency = int(ii[1])
                dv = float(ii[4])
                increase = int(ii[5])
                if(increase == 1):
                    # check if greater than
                    if(ffts_t[channel][frequency][ffts_circbufferindex] > dv):
                        satisfy = True
                elif(increase == 0):
                    # check if smaller than
                    if(ffts_t[channel][frequency][ffts_circbufferindex] < dv):
                        satisfy = True
                else:
                    print "Error reading increase values = " + str(ii)
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
            for ii in twm_mean_dvs_lut[condition]:
                satisfy = False
                channel = ii[0]
                frequency = int(ii[1])
                dv = float(ii[4])
                increase = int(ii[5])
                if(increase == 1):
                    # check if greater than
                    if(ffts_t[channel][frequency][ffts_circbufferindex] > dv):
                        satisfy = True
                elif(increase == 0):
                    # check if smaller than
                    if(ffts_t[channel][frequency][ffts_circbufferindex] < dv):
                        satisfy = True
                else:
                    print "Error reading increase values = " + str(ii)
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
            for ii in twm_mean_dvs_lut[condition]:
                satisfy = False
                channel = ii[0]
                frequency = int(ii[1])
                dv = float(ii[4])
                increase = int(ii[5])
                if(increase == 1):
                    # check if greater than
                    if(ffts_t[channel][frequency][ffts_circbufferindex] > dv):
                        satisfy = True
                elif(increase == 0):
                    # check if smaller than
                    if(ffts_t[channel][frequency][ffts_circbufferindex] < dv):
                        satisfy = True
                else:
                    print "Error reading increase values = " + str(ii)
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

'''
    Assume the circular buffer of size n with values denoted by indices 0, 1, 2, n [0 1 2 n]
    with n is the most recent entry (ffts_circbufferindex)
    Suppose we want to know the difference of the minimum and maximum values of the buffer
    from index 0 to index 2
    lbound = 0
    ubound = 2
'''
def check_minmaxdiff(ffts_t, ffts_circbufferindex, channel, frequency, lbound, ubound):
    target_buffer = ffts_t[channel][frequency]
    bsize = len(target_buffer)
    if(lbound>=bsize or lbound<0 or ubound>=bsize or lbound<0 or lbound>=ubound):
        raise Exception('Unbound parameters for check_minmaxdiff')
        return 10000000.0
    lbound_rel_index = adjust_bufferindexoffset(lbound,ffts_circbufferindex,bsize)
    ubound_rel_index = adjust_bufferindexoffset(ubound,ffts_circbufferindex,bsize)
    min_val = target_buffer[lbound_rel_index]
    max_val = target_buffer[lbound_rel_index]

    terminate = False
    ii = lbound_rel_index
    while (not terminate):
        ii = inc_circbufferindex(ii,bsize)
        if(target_buffer[ii]<min_val):
            min_val = target_buffer[ii]
        if(target_buffer[ii]>max_val):
            max_val = target_buffer[ii]
        if(ii==ubound_rel_index):
            terminate = True
    return (max_val-min_val)

'''
    Assume the circular buffer of size n with values denoted by indices 0, 1, 2, n [0 1 2 n]
    with n is the most recent entry (ffts_circbufferindex)
    Suppose we want to know the std of the buffer
    from index 0 to index 2
    lbound = 0
    ubound = 2
'''
def check_std(ffts_t, ffts_circbufferindex, channel, frequency, lbound, ubound):
    target_buffer = ffts_t[channel][frequency]
    bsize = len(target_buffer)
    if(lbound>=bsize or lbound<0 or ubound>=bsize or lbound<0 or lbound>=ubound):
        raise Exception('Unbound parameters for check_minmaxdiff')
        return 10000000.0
    lbound_rel_index = adjust_bufferindexoffset(lbound,ffts_circbufferindex,bsize)
    ubound_rel_index = adjust_bufferindexoffset(ubound,ffts_circbufferindex,bsize)
    data = []

    terminate = False
    ii = dec_circbufferindex(lbound_rel_index,bsize)
    while (not terminate):
        ii = inc_circbufferindex(ii,bsize)
        data.append(target_buffer[ii])
        if(ii==ubound_rel_index):
            terminate = True
    # print "data = " + str(data)
    mu, std = norm.fit(np.array(data))
    return (std)

'''
    Using the model where the last element of the circular buffer is the most recent one
    Convert index to the relative index in the circular buffer
    e.g. [0 1 2 n], circbufferindex = 2, index = 0 (oldest entry)
    return rel_index
'''
def adjust_bufferindexoffset(index, circbufferindex, bsize):
    if(circbufferindex>bsize or index<0 or index>=bsize):
        raise Exception('Unbound parameters for adjust_bufferindexoffset')
    rel_index = index-(bsize-1-circbufferindex)
    if rel_index < 0:
        return (rel_index+bsize)
    else:
        return rel_index

def inc_circbufferindex(index, bsize):
    new_index = index + 1
    if(new_index==bsize):
        new_index = 0
    return new_index

def dec_circbufferindex(index, bsize):
    new_index = index - 1
    if(new_index<0):
        new_index = bsize - 1
    return new_index