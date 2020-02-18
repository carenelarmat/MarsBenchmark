import numpy as np
import matplotlib.pyplot as plt

#read specfem model
specfem_model = 'SEM_RESULT_TOMO2/SEIS1_BM_v2.xyz'
f = np.loadtxt(specfem_model,skiprows=4)
x = f[:,0]
y = f[:,1]
z = f[:,2]
vp = f[:,3]
vs = f[:,4]
rho = f[:,5]
qk = f[:,6]
qm = f[:,7]

#read a bm mars model (for structure below the specfem model)
bm_mars_model = 'AxiSEM_SEISshallow_2Hz_erf/inputs/external_model.bm'
g = np.loadtxt(bm_mars_model,skiprows=5)
bm_rad = g[:,0]
bm_rho = g[:,1]
bm_vp = g[:,2]
bm_vs = g[:,3]
bm_qk = g[:,4]
bm_qm = g[:,5]

#convert depth to radius
z -= np.max(z)
rad = np.max(bm_rad) + z
print 'the maximum depth/minimum radius of the specfem model is {}/{}'.format(-1*np.min(z),np.min(rad))
#plt.plot(vs,rad)
#plt.show()

#write new bm modelfile
out = open('SEIS_BM_v2.bm','w')
out.write('NAME SEIS_BM_v2\n')
out.write('ANELASTIC T\n')
out.write('ANISOTROPIC T\n')
out.write('UNITS m\n')
out.write('COLUMNS radius rho vpv vsv qka qmu vph vsh eta\n')

#write model below specfem structure (radius increases!)
for i in range(0,len(bm_rad)):
    if bm_rad[i] < np.min(rad):
        out.write('{:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} 1.00000\n'.format(
                   bm_rad[i],bm_rho[i],bm_vp[i],bm_vs[i],bm_qk[i],bm_qm[i],bm_vp[i],bm_vs[i]))
#write top of model
for i in range(0,len(rad)):
    rad_here = rad[::-1][i]
    rho_here = rho[::-1][i]
    vp_here = vp[::-1][i]
    vs_here = vs[::-1][i]
    qm_here = qm[::-1][i]
    qk_here = qk[::-1][i]
    out.write('{:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} 1.00000\n'.format(
                rad_here,rho_here,vp_here,vs_here,qm_here,qk_here,vp_here,vs_here))
    

