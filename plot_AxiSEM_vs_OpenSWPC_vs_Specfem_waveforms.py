import obspy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import fftconvolve
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

#---------------------------------------------------------------------------
# filter parameters
#---------------------------------------------------------------------------
freqmin = 1./5.
freqmax = 2.0
corners = 8
zerophase = False

#----------------------------------------------------------------------------
# if convolution is desired
#----------------------------------------------------------------------------
def convolve(trace, stf_half_duration, ftype='gaussian',plot=False):

    half_steps = np.ceil(2.5 * stf_half_duration / trace.stats.delta)
    shift = half_steps * trace.stats.delta
    t = -shift + np.arange(half_steps * 2) * trace.stats.delta

    if ftype=='gaussian':
        #decay = 1.628
        decay = 3.5
        stf = np.exp(-np.power((decay / stf_half_duration * t), 2.)) * decay \
            / (stf_half_duration * np.sqrt(np.pi))

    elif ftype=='kupper':
        c1 = (3.*np.pi)/(8.*stf_half_duration)
        c2 = np.pi/(2.*stf_half_duration)
        stf = c1*np.sin(c2*t)**3
        inds = np.where(t > (2.*stf_half_duration))
        stf[inds] = 0.0
        inds = np.where(t < 0)
        stf[inds] = 0.0

    if plot:
        plt.plot(t,stf)
        plt.show()

    result = trace.copy()
    result.data = fftconvolve(trace.data, stf, mode='valid')
    result.data /= np.sum(stf)
    return result

#---------------------------------------------------------------------------
# setup axes to plot velocity seismograms between 1 - 5 km distance
#---------------------------------------------------------------------------
#fig,axes = plt.subplots(nrows=10,figsize=[14,14])
fig,axes = plt.subplots(nrows=5,ncols=1,figsize=[12,12])
#axes = axes.ravel(order='F')

#---------------------------------------------------------------------------
# plot seismograms
#---------------------------------------------------------------------------
for i in range(0,5):

    #AxiSEM-----------------------------------------------------------------
    st = obspy.read("./AxiSEM_SEIS_BM_v2/sac_seismograms/{}km_Vz.sac".format(i+1)) #sac seismograms are in velocity
    tr = st[0]
    tr = convolve(tr,stf_half_duration = 0.5,ftype='kupper')
    tr.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=corners,zerophase=zerophase)
    time = np.linspace(0,tr.stats.npts*tr.stats.delta,tr.stats.npts)
    axes[i].plot(time+1.,tr.data,color='C0',label='AxiSEM')

    #OpenSWPC--------------------------------------------------------------
    st = obspy.read("./Benchmark_KO_20191030/Vz_m:s/{}km_Vz.sac".format(i+1))
    tr = st[0]
    tr.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=corners,zerophase=zerophase)
    time = np.linspace(0,tr.stats.npts*tr.stats.delta,tr.stats.npts)
    axes[i].plot(time,tr.data,color='C1',label='OpenSWPC')

    #Specfem---------------------------------------------------------------
    #st = obspy.read("./SEM_RESULT_TOMOBM_KUPP/D{:02d}.KO.FXZ.semv.sac".format(i+1))
    st = obspy.read("./SEM_RESULT_TOMO2/D{:02d}.KO.FXZ.semv.sac".format(i+1))
    tr = st[0]
    tr.filter('bandpass',freqmin=freqmin,freqmax=freqmax,corners=corners,zerophase=zerophase)
    time = np.linspace(0,tr.stats.npts*tr.stats.delta,tr.stats.npts)
    axes[i].plot(time,tr.data,color='C2',label='Specfem3D')

    #Axis Params-----------------------------------------------------------
    #axes[i].set_xlim([0,100])
    axes[i].set_xlim([0,50])
    axes[i].set_ylabel('vel. (m/s)')
    axes[i].legend(loc='upper right')
    axes[i].set_title('dist {} km'.format(i+1))

#axes[0].set_title('AxiSEM vs OpenSWPC, bandpass {} - {} Hz'.format(freqmin,freqmax))
#axes[0].legend()
axes[-1].set_xlabel('time (s)')
axes[4].set_xlabel('time (s)')
plt.tight_layout()
#plt.savefig('AxiSEM_vs_OpenSWPC_waveforms.png')
#plt.suptitle('Bandpass 0.2 - 2.0 Hz',fontsize=14)
plt.savefig('AxiSEM_vs_OpenSWPC_vs_Specfem_waveforms.pdf',transparent=True)
