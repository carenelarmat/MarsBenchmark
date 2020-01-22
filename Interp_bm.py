#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:33:22 2019

This code cannot do any quality estimate on the polynomial fit. The user needs
to identify the best way to split the model before running the script and enter
the discontinuities by repeating the radius 

Comment January 2020: This script needs to be changed to mimick the subroutine
    AxiSEM, discontinuities of order 0 and 1 should be identified by a repeating radius. 
    This is different from AxiSEM subroutine which can identify either (1) repeated 
     radius indicative of discontinuities of order 0, (2) gradient jump. 
@author: carene
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#name of file and name of columns 
#fname = 'EH45TcoldCrust1rq_Reg2.bm'
fname = '2019_BENCHMARK/AxiSEM_SEISshallow_2Hz_erf/inputs/external_model.bm'
#radius(m),density(kg/m^3),Vpv(m/s),Vsv(m/s),Q-kappa,Q-mu,Vph(m/s),Vsh(m/s),eta
columns=('radius','rho','vpv','vsv','qkappa','qmu','vph','vsh','eta')

mod = np.loadtxt(fname,skiprows=5)

model = pd.DataFrame(data=mod,columns=columns)

plt.figure()
plt.plot(model['vpv'].values/1000.0,model['radius'].values/1000.0,label='vp')
plt.plot(model['vsv'].values/1000.0,model['radius'].values/1000.0,label='vs')
plt.plot(model['rho'].values/1000.0,model['radius'].values/1000.0,label='rho')
#plt.plot(model2['vpv'].values/1000.0,model2['radius'].values/1000.0,'--',color='blue',label='vp')
#plt.plot(model2['vsv'].values/1000.0,model2['radius'].values/1000.0,'--',color='orange',label='vs')
#plt.plot(model2['rho'].values/1000.0,model2['radius'].values/1000.0,'--',color='green',label='rho')
plt.legend()
plt.ylabel('radius (km)')
plt.xlabel('v in km/s; rho in g/cm3')

plt.ylim([3390-20,3390])

#Find where radius is repeated - discontinuities order 0 and 1 
rad=model['radius'].values
#discontinuities of order 0 are identified by a repeated radius 
ind_discs_0 = np.where(np.diff(rad)==0)[0]
#discontinuties of order 1 are identified by a "jump", i.e. variation over a certain threshold - AxiSEM is 0.1 km/s
ind_discs_1_p = np.where(np.abs(np.diff(model['vpv']))>100)[0]
ind_discs_1_s = np.where(np.abs(np.diff(model['vsv']))>100)[0]
ind_discs_1_r = np.where(np.abs(np.diff(model['rho']))>100)[0]
#ind_discs = np.unique(np.concatenate((ind_discs_0,ind_discs_1_p,ind_discs_1_s,ind_discs_1_r)))
ind_discs=ind_discs_0
discontinuities = rad[-1]-rad[ind_discs]
#
#
#Segments the model
segments_rad = np.split(rad,ind_discs)
segments_depth = rad[-1]-segments_rad
segments_vp=np.split(model['vpv'],ind_discs)
segments_vs=np.split(model['vsv'],ind_discs)
segments_rho=np.split(model['rho'],ind_discs)
segments_qkappa=np.split(model['qkappa'],ind_discs)
segments_qmu=np.split(model['qmu'],ind_discs)

def search_ind(d):
#Search indices of depth
    ind_d = -1
    for i,t in enumerate(discontinuities):
#        if (d>=t[1] and d<t[0]): 
        if (d<t):
            ind_d=i+1
    return ind_d
    
    
fout=open('External_Model.xyz','w')
bb = 0 # km
ee = 18 # km
dres = 4.0/1000.0 # sampling in km 
dd = np.linspace(bb,ee,int((ee-bb)/dres))*1000.0
for id in dd:
    ind_d = search_ind(id)
    x = segments_depth[ind_d][::-1]
    y = segments_vp[ind_d][::-1]
    vp = np.interp(id,x,y)
    y = segments_vs[ind_d][::-1]
    vs = np.interp(id,x,y)
    y = segments_rho[ind_d][::-1]
    rho = np.interp(id,x,y)
    y = segments_qkappa[ind_d][::-1]
    qk = np.interp(id,x,y)
    y = segments_qmu[ind_d][::-1]
    qm = np.interp(id,x,y)

    fout.write('0 0 '+str(-2700-id)+' '+str(vp)+' '+str(vs)+' '+str(rho)+' '+str(qk)+' '+str(qm)+'\n')
fout.close()

#Figure BM - xyz 
SEM = np.loadtxt('External_Model.xyz')

plt.figure()
plt.plot(model['vpv'].values/1000.0,-(model['radius'].values[-1]-model['radius'].values)/1000.0,label='vp BM')
plt.plot(model['vsv'].values/1000.0,-(model['radius'].values[-1]-model['radius'].values)/1000.0,label='vs BM')
plt.plot(model['rho'].values/1000.0,-(model['radius'].values[-1]-model['radius'].values)/1000.0,label='rho BM')
plt.plot(SEM[:,3]/1000.0,(SEM[:,2]+2700)/1000.0,'--',label='vp xyz')
plt.plot(SEM[:,4]/1000.0,(SEM[:,2]+2700)/1000.0,'--',label='vs xyz')
plt.plot(SEM[:,5]/1000.0,(SEM[:,2]+2700)/1000.0,'--',label='rho xyz')

plt.legend()
plt.ylabel('radius (km)')
plt.xlabel('v in km/s; rho in g/cm3')

plt.ylim([-ee,bb])
