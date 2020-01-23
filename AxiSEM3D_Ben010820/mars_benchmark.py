#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from obspy.core import Trace, Stats, UTCDateTime
import numpy as np
from scipy.signal import fftconvolve



def plot_single_trace(folder_code, station_name, do_filter, do_convolve, min_period, max_period, gaussian_hw=0, component = 'z'):
    
    """
    folder_code: address of data
    station_name: XX for station XX.KO.RTZ
    do_filter: bandpass filter? (order 4, Butterworth-bandpass)
    do_convolve: gaussian convolution (to smooth out differences in STF shape?)
    min_period: minimum filter period in seconds (in AxiSEM3D, should be mesh period - different definition to SPECFEM)
    max_period: maximum filter period in seconds (should be <100 for accuracy as no gravity)
    """
    plt.figure()

    axisem3d_data_file = '/Users/benfernando/Google Drive/PhD/Data/axisem3d/mars_CTX_benchmark/'+str(folder_code)+'/axisem3d_synthetics.nc'
    axisem3d_trace = load_axisem3d_data(axisem3d_data_file, station_name, component) 
    axisem3d_trace.differentiate()

    if do_filter ==True: 
        axisem3d_trace.filter('bandpass', freqmin=1.0/max_period, freqmax=1.0/min_period)
    if do_convolve==True:
        axisem3d_trace = convolve(axisem3d_trace, gaussian_hw)
    plt.plot(axisem3d_trace.times(), axisem3d_trace.data,label='Syntheics', lw=0.5, color = 'r')
        
    plt.ylabel('Velocity (m/s)')
    plt.xlabel('Time since event (seconds)')
    plt.legend()
    plt.show()  

def deg_to_km(station_lat):
    epicentral_distance = station_lat - 3.2848
    r_planet = 3389.5
    c_planet = 2*np.pi*r_planet
    
    frac_angle = 360/epicentral_distance
    
    distance_km = c_planet/frac_angle
    print(distance_km)
    

def load_axisem3d_data(file,station_code,component):
    
    axisem3d_data = Dataset(file)
    times_a = axisem3d_data.variables['time_points']
    axisem3d_stats = Stats()
    axisem3d_stats.delta = (times_a[1] - times_a[0])
    axisem3d_stats.starttime = UTCDateTime(times_a[0])
    axisem3d_stats.npts = times_a.size
    station_code = station_code+('.KO.RTZ')
    
    if component =='z':
        c_a = axisem3d_data.variables[station_code][:, 2] 
    elif component =='t':
        c_a = axisem3d_data.variables[station_code][:, 1]
    elif component =='r':
        c_a = axisem3d_data.variables[station_code][:, 0] 
    else:
        raise Exception('No component with this name')
    
    axisem3d_trace = Trace(c_a, header=axisem3d_stats)
    axisem3d_data.close()
    return axisem3d_trace

def convolve(trace, stf_half_duration): 
    decay = 1.628
    half_steps = np.ceil(2.5 * stf_half_duration / trace.stats.delta)
    shift = half_steps * trace.stats.delta
    t = -shift + np.arange(half_steps * 2) * trace.stats.delta
    stf = np.exp(-np.power((decay / stf_half_duration * t), 2.)) * decay \
        / (stf_half_duration * np.sqrt(np.pi))
    result = trace.copy()
    result.data = fftconvolve(trace.data, stf, mode='valid')
    result.data /= np.sum(stf)
    return result