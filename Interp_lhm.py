#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 21:41:43 2019

@author: carene
"""
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

def interp_modele(depth,key):
    ind = np.where(modele['depth']<=depth)[0][-1]
    db = modele['depth'][ind]
    de = modele['depth'][ind+1]
    vb = modele[key].values[ind]
    ve = modele[key].values[ind+1]
    v = vb #+ (depth-db)/(de-db)*(ve-vb)
    return v 

modele=pd.DataFrame(np.loadtxt('SEIS1_BM_resampled.dat',skiprows=3),columns=['depth','rho','vp','vs','Qp','Qs'])
plt.figure()
plt.plot(modele['vp'],3389.5-modele['depth']*1000.0,label='vp')
plt.plot(modele['vs'],3389.5-modele['depth']*1000.0,label='vs')
plt.plot(modele['rho'],3389.5-modele['depth']*1000.0,label='rho')
plt.legend()
plt.ylabel('radius (km)')
plt.xlabel('v in km/s; rho in g/cm3')

plt.ylim([3390-20,3390])    


dout = open('SEIS1_BM_v2.xyz','w')
depth = np.linspace(0,18,int(18/0.004))
for d in depth:
    vp = interp_modele(d,'vp')*1000.0
    vs = interp_modele(d,'vs')*1000.0
    rho = interp_modele(d,'rho')*1000.0
    qp = interp_modele(d,'Qp')
    qs = interp_modele(d,'Qs')
    dout.write('0 0 '+str(-2700-d*1000.0)+' '+str(vp)+' '+str(vs)+' '+str(rho)+' '+str(qp)+' '+str(qs)+'\n')

dout.close()

