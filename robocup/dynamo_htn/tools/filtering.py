# -*- Mode: Python; indent-tabs-mode: nil; py-indent-offset: 4; tab-width: 4 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
import math

def MovingAverage(cur_data, buffer_pointer, buffer_sum, ring_buffer):
    """returns moving averaged data.  Moving average length is specified with
    ring buffer length.
    Usage: out, index, buf_sum, buf = MovingAverage(cur_val, index, buf_sum, buf)
    where cur_data:list with n element
          ring_buffer: m length list of n element list
    written by kaminaga"""
    buflen = len(ring_buffer)
    dim    = len(cur_data)

    if( len(ring_buffer[0])!=dim ):
        print "dimension error"

    new_buffer_sum = range(dim)
    filt_data      = range(dim)

    #import pdb; pdb.set_trace()
    for i in range(dim):
        new_buffer_sum[i] = buffer_sum[i] + cur_data[i] - ring_buffer[buffer_pointer][i]
        filt_data[i]      = new_buffer_sum[i] / buflen

    new_ring_buffer = list(ring_buffer)
    new_ring_buffer[buffer_pointer] = cur_data
    new_buffer_pointer = buffer_pointer + 1
    if(new_buffer_pointer>=buflen):
        new_buffer_pointer = 0

    return (filt_data, new_buffer_pointer, new_buffer_sum, new_ring_buffer)

def InitializeMovingAverage(cur_data, ring_buffer):
    """returns operable parameters for MovingAverage.
    Usage: index, buf_sum, buf = InitializeMovingAverage(cur_val, buf)
    where cur_data:list with n element
          ring_buffer: m length list of n element list
    written by kaminaga"""
    index = 0
    dims = len(cur_data)
    buflen = len(ring_buffer)
    buf_sum = []
    for i in range(dims):
        buf_sum.append(0)
    
    for i in range(dims):
        buf_sum[i] = cur_data[i]*buflen
    for i in range(buflen):
        ring_buffer[i] = cur_data

    return (index, buf_sum, ring_buffer) 

def ReturnSaturatedChange(newvalue, oldvalue, limit):
    """ Return saturated new value
    if | new - old | > limit, return saturated newvalue
    witten by minakata 2008.04.23
    """
    if newvalue - oldvalue > limit: # increasing
        return oldvalue + limit
    elif oldvalue - newvalue > limit: # decreasing
        return oldvalue - limit
    return newvalue                 # |newvalue - oldvalue| < limit
