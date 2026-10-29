## new version JKskirt

import os
import sys
from importlib import reload

import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":
    
    GFE_DIR = '/home/yuchang/JKsKIRT/'
    sys.path.append(GFE_DIR)
    import JKsKIRT as gskirt

    from rur import uri, uhmi
    SioverSil = 0.163 

    nout = 78

    repo = '/storage8/NCdustfix/NCdustfix2/'
    path_in_repo = 'snapshots'
    mode = 'nc'

    boxrad = 10

    snap = uri.RamsesSnapshot(repo=repo, 
                            path_in_repo=path_in_repo, 
                            iout=nout, 
                            mode=mode, 
                            longint=False)

    gals_tot, pid = uhmi.HaloMaker.load(snap, 
                                        galaxy=True,
                                        load_parts=True,
                                        double_precision=True,
                                        extend=True)
    gals_tot.sort(order='m')
    gals_tot = np.flip(gals_tot)
    mlow = 9.5
    mupp = 12
    # mask = np.isin(gals_tot['id'],[3,6,34,18,79,23,21,33,30,35,4,11,17,1,74])
    mask = np.isin(gals_tot['id'],[3])
    gals = gals_tot[mask]
    print(gals['m'])

    for id in gals['id']:
        gal = gals[gals['id']==id]
        snap.clear()
        snap = uri.RamsesSnapshot(repo=repo, 
                                path_in_repo=path_in_repo, 
                                iout=nout, 
                                mode=mode)

        boxtokpc = 1/snap.unit['kpc']
        snap.set_box_halo(gal, 
                        use_halo_radius=False, 
                        radius=10/boxtokpc)

        star = snap.get_part(pname='star')
        cell = snap.get_cell()
        snap.clear()
        
        p_mC_small = cell['d1']*cell['m','Msun']
        p_mC_large = cell['d2']*cell['m','Msun']
        p_mSil_small = cell['d3']*cell['m','Msun']/SioverSil
        p_mSil_large = cell['d4']*cell['m','Msun']/SioverSil

        p_m_H = cell['m','Msun']
        sfe_s = np.full_like(star['m','Msun'], 0.025) # Follwing SKIRT-COLIBRE pipeline
        cnd_s = np.full_like(star['m','Msun'], 320) # Follwing SKIRT-COLIBRE pipeline

        repo_par = '/storage8/yuchang/obscured_2/'
        fname_par = 'parameter_setting_new_include_spitzer'

        try:
            par = reload(sys.modules[fname_par])
        except:
            pass

        sys.path.append(repo_par)
        par = __import__(fname_par)

        par.repo = f'/storage1/yuchang/Attenuation/gal_{nout:04d}/{gals['id']:04d}/'

        par.add_pah = False
        p_mPAHneu = []
        p_mPAHion = []

        ###########################################################################
        if par.add_pah == True:

            X = (star['x','kpc'][star['age','Gyr']<=0.03]).reshape(-1,1)         # sample recently formed stars
            Y = (star['y','kpc'][star['age','Gyr']<=0.03]).reshape(-1,1)         #
            Z = (star['z','kpc'][star['age','Gyr']<=0.03]).reshape(-1,1)
            XSET = np.hstack((X,Y,Z))

            Xc = cell['x','kpc'].reshape(-1,1)                                   # sampele cells                  
            Yc = cell['y','kpc'].reshape(-1,1)
            Zc = cell['z','kpc'].reshape(-1,1)
            XcSET = np.hstack((Xc,Yc,Zc))

            X_grid = XcSET + 0.                                                  # cell positions
            X_compare = XSET + 0.                                                # star positions        

            from sklearn.neighbors import NearestNeighbors
            nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(X_grid) # fit the cell positions
            distances, indices = nbrs.kneighbors(X_compare)                      # find the nearest cell for each star

            cell_shape = cell['x','kpc'].shape

            pahf_ion = np.zeros(len(XcSET), dtype=float)
            pahf_neu = np.zeros(len(XcSET), dtype=float)

            ordinary = np.setdiff1d(np.arange(len(XcSET)), indices.flatten())

            pahf_ion[indices] = 0.5
            pahf_ion[ordinary] = 0.5
            pahf_neu[indices] = 0.5
            pahf_neu[ordinary] = 0.5

            pahf_ion = pahf_ion.reshape(cell_shape)
            pahf_neu = pahf_neu.reshape(cell_shape)

            def find_qpah(Z, Z_th):
                return ((15.1 * (Z > Z_th)) + (15.1 * (Z/Z_th)**2.6 * (Z <= Z_th)))/3.69
            metal_z = cell['metal'] / 0.01345
            q_pah = find_qpah(metal_z, Z_th=0.625) * 0.01
            CS = cell['d1'] * cell['m','Msun']
            CL = cell['d2'] * cell['m','Msun']
            SiS = cell['d3']/0.163 * cell['m','Msun']
            SiL = cell['d4']/0.163 * cell['m','Msun']
            total = CS + CL + SiS + SiL
            p_mC_small = CS - total* q_pah / (1 + CL/CS)
            p_mC_large = CL - total* q_pah / (1 + CS/CL)

            p_mPAHneu = pahf_neu * total * q_pah
            p_mPAHion = pahf_ion * total * q_pah

        ###########################################################################


        print('Total photon packet Number = 10^{%s}'%(np.round(np.log10(par.N_phot),2)),end='\n\n')
        print('Redshift of the target = %s'%(par.z_red))
        print('Distance to the target = %s (>0 only when z_red = 0)'%(par.inst_dist),end='\n\n')
        print('Field-of-View (X-direction) = %s %s'%(par.fov_X,par.fov_unit))
        print('Field-of-View (Y-direction) = %s %s'%(par.fov_Y,par.fov_unit),end='\n\n')
        print('Using on-the-fly-dust info = %s'%(par.on_the_fly_dust),end='\n\n')
        print('The file will be saved in %s/%s'%(par.repo,par.repo_output),end='\n\n')

        gskirt.utils.execute_SKIRT.make_INSKI(
                                                boxtokpc=boxtokpc,
                                                x_s=star['x'],y_s=star['y'],z_s=star['z'], # position
                                                vx_s=star['vx','km/s'],vy_s=star['vy','km/s'],vz_s=star['vz','km/s'], # velocity
                                                m_s=star['m','Msun'],age_s=star['age','Gyr'],metal_s=star['metal'], # stellar population
                                                # m0_s=star['m0','Msun'],rho0_s=star['rho0','H/cc'],sfe_s=sfe_s, # young stellar population
                                                m0_s=star['m0','Msun'],rho0_s=cnd_s,sfe_s=sfe_s, # young stellar population

                                                x_c=cell['x'],y_c=cell['y'],z_c=cell['z'],
                                                vx_c=cell['vx','km/s'],vy_c=cell['vy','km/s'],vz_c=cell['vz','km/s'],
                                                lvl_c=cell['level'],
                                                m_c=p_m_H,
                                                T_c=cell['T','K'], metal_c=cell['metal'],
                                                param=par,
                                                pos_ctr=[gal['x'],gal['y'],gal['z']],
                                                vel_ctr=[gal['vx'],gal['vy'],gal['vz']],

                                                mC_small=p_mC_small,
                                                mC_large=p_mC_large,
                                                mSil_small=p_mSil_small,
                                                mSil_large=p_mSil_large,

                                                mPAHneu=p_mPAHneu,
                                                mPAHion=p_mPAHion
                                                )
