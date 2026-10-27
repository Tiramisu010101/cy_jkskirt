import numpy as np
#import rur
#from rur import uri, drawer, utool, uhmi, sci

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

kpc = 3.0857e21
msun = 1.989e33
Lsun = 3.826e33

k_boltzmann = k_b = 1.38064852*1e-23 ## m^2 kg s^-2 K^-1
m_H = 1.6735575*1e-27 ## kg 

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def rotation(array1, array2, theta, type='rad'):
    if type == 'deg':
        theta *= np.pi/ 180
    new_array1 = np.cos(theta) * array1 - np.sin(theta) * array2
    new_array2 = np.sin(theta) * array1 + np.cos(theta) * array2
    return new_array1, new_array2

def Ang_Rot( 
            M,
            X,Y,Z,
            VX,VY,VZ,
            age,
            R_upp,R_low=0,
            A_upp=8,
            mass_weight=True,
            par_mode='median',
            Param=True
            ):
    
    ######### rotation ###########

    if Param == True:
        ang_x = (Y*VZ - Z*VY)
        ang_y = (Z*VX - X*VZ)
        ang_z = (X*VY - Y*VX)
        if mass_weight==True:
            ang_x *= M
            ang_y *= M
            ang_z *= M
        
        rotsort = (R_low<np.sqrt(np.square(X)+np.square(Y)+np.square(Z)))*\
                  (np.sqrt(np.square(X)+np.square(Y)+np.square(Z))<R_upp)*\
                  (age<A_upp)
        
        if par_mode == 'median' or par_mode == 'Median' or par_mode == 'MEDIAN':
            param = [np.median(ang_x[rotsort]),np.median(ang_y[rotsort]),np.median(ang_z[rotsort])]
        elif par_mode == 'mean' or par_mode == 'Mean' or par_mode == 'MEAN':
            param = [np.mean(ang_x[rotsort]),np.mean(ang_y[rotsort]),np.mean(ang_z[rotsort])]
        else:
            print('Please choose "mean" or "median".')
        
    else:
        param = Param

    a, b, c = param[0], param[1], param[2]
    ab = np.sqrt(np.square(a)+np.square(b))
    
    Tht_xy = -1 * np.arctan2(a,b)
    Tht_yz = -1 * np.arctan2(ab,c)
    
    y_mid,x_new = rotation(Y,X,Tht_xy)
    z_new,y_new = rotation(Z,y_mid,Tht_yz)

    vy_mid,vx_new = rotation(VY,VX,Tht_xy)
    vz_new,vy_new = rotation(VZ,vy_mid,Tht_yz)

    return  x_new, y_new, z_new,\
            vx_new,vy_new,vz_new, param


#!!!!!!!

def make_input(
           boxtokpc,
           x_s,
           y_s,
           z_s,
           vx_s,
           vy_s,
           vz_s,
           m_s,
           m0_s,
           age_s,
           metal_s,
           cnd_s,
           sfe_s,

           x_c,
           y_c,
           z_c,
           lvl_c,
           vx_c,
           vy_c,
           vz_c,
           m_c,
           T_c,
           metal_c,

           pos_ctr,
           vel_ctr,
                
           dx_dirt=[],
    
           l_simbox=1,

           # gal rotation
           rotating_gal=True,
           R_upp=8,
           R_low=2,
           A_upp=8,
           mass_weight=True,
           par_mode='median',

           # Stellar population
           sig_s = 10, #[km/s]

           # Old population
           old_fbase = './',
           old_fname = 'part_old.txt',

           # Young star selection criteria
           add_young=False,

           young_fbase = './',
           young_fname = 'part_young.txt',

           Age_Cut = 0.01, #[Myr]
           SED_type_o='BC03',
           SED_type_y='mappings',

           # Using additional columns?
           import_velocity='true',
           import_dispersion='false',

           # Gas cells 
           gas_fbase = './',
           gas_fname = 'gas_cell.txt',

           fact_dx = 1,
           sig_c = 5, #[km/s]
    
           metal_dependent_dust = True,
           Zsun = 0.0134,
           mtd_mod = 'Li2019',

           import_velocity_gas='true',
           import_dispersion_gas='false',

           cell_medium=False,

           dx_s_o = 50, #[pc]
           dx_s_y = 50, #[pc]
           adaptive_smoothing=False,
           n_targ_nbr=5,
           n_job_smoothing=32,
    
           on_the_fly_dust=False,
           add_pah='false',
           mC_small = [],
           mC_large = [],
           mSil_small = [],
           mSil_large = [],
           mPAHneu = [],
           mPAHion = [],

           torrey_fdust=0.14
           ):
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    if adaptive_smoothing == True:
        from sklearn.neighbors import NearestNeighbors

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    x_s = (x_s - pos_ctr[0]) * boxtokpc
    y_s = (y_s - pos_ctr[1]) * boxtokpc
    z_s = (z_s - pos_ctr[2]) * boxtokpc
    
    vx_s -= vel_ctr[0]
    vy_s -= vel_ctr[1]
    vz_s -= vel_ctr[2]
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    x_c = (x_c - pos_ctr[0]) * boxtokpc
    y_c = (y_c - pos_ctr[1]) * boxtokpc
    z_c = (z_c - pos_ctr[2]) * boxtokpc
    
    vx_c -= vel_ctr[0]
    vy_c -= vel_ctr[1]
    vz_c -= vel_ctr[2]
    
    if len(dx_dirt) == 0:
        dx_c = l_simbox / (2**lvl_c) * boxtokpc
    else:
        dx_c = dx_dirt

    print("done -- basic setting")
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if rotating_gal == True:
        x_s, y_s, z_s, vx_s, vy_s, vz_s, par_rot =  Ang_Rot( 
                                                            M=m_s,
                                                            X=x_s,Y=y_s,Z=z_s,
                                                            VX=vx_s,VY=vy_s,VZ=vz_s,
                                                            age=age_s,
                                                            R_upp=R_upp,R_low=R_low,
                                                            A_upp=A_upp,
                                                            mass_weight=mass_weight,
                                                            par_mode=par_mode,
                                                            Param=True
                                                            )               
        x_c, y_c, z_c, vx_c, vy_c, vz_c, par_rot =  Ang_Rot( 
                                                            M=m_c,
                                                            X=x_c,Y=y_c,Z=z_c,
                                                            VX=vx_c,VY=vy_c,VZ=vz_c,
                                                            age=x_c,
                                                            R_upp=R_upp,R_low=R_low,
                                                            A_upp=A_upp,
                                                            mass_weight=mass_weight,
                                                            par_mode=par_mode,
                                                            Param=par_rot
                                                            )    
        
        print("done -- galaxy rotation")
        
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    if adaptive_smoothing == True:    
        print("start -- calculating distance to the Nth-nearest neighbor (N=%s)"%(n_targ_nbr))
        X = (x_s).reshape(-1,1)
        Y = (y_s).reshape(-1,1)
        Z = (z_s).reshape(-1,1)
        XSET = np.hstack((X,Y,Z))
        nbrs = NearestNeighbors(n_neighbors=n_targ_nbr+1, algorithm='auto',n_jobs=n_job_smoothing).fit(XSET)
        distances, indices = nbrs.kneighbors(XSET)
        dx_adaptive = distances[:,n_targ_nbr]*1e3 #kpc to pc
        print("done -- calculating distance to the Nth-nearest neighbor (N=%s)"%(n_targ_nbr))
        
    if on_the_fly_dust in [False,'false'] and metal_dependent_dust in [True,'true']:
        print("start -- calculating metallicity dependent Dust-to-Gas ratio")
        if mtd_mod == 'Li2019':
            log_metal_c = np.log10(metal_c/Zsun)
            DGR = 10**(2.445*log_metal_c - 2.029)
            m_c *= DGR
            metal_c = np.ones(len(m_c))
        elif mtd_mod == 'Torrey':
            rho_gas = m_c/(dx_c)**3 # Msun/kpc^3
            ind = (np.log10(T_c) < 6 + 0.25 * np.log10(rho_gas / (1e10 * 0.677**2)))
            new_m_c = np.zeros(len(m_c))
            # DGR = 0.14 * metal_c # f_{dust} = 0.14 # kapoor et al. 2021 best fraction of the metallic gas locked up in dust, cell의 metal이 gas phase만 포함하고 있음 정의대로라면 gas + dust phase로 해야함.
            new_m_c[ind] = m_c[ind] * metal_c[ind] * torrey_fdust
            m_c = new_m_c
            metal_c = np.ones(len(m_c))
        elif mtd_mod == 'RR14':

            # -------------------------------------------------
            # Remy-Ruyer et al. (2014)
            # metallicity-dependent dust-to-gas ratio
            #
            # x = log10(Z / Zsun)
            #
            # log10(G/D) = 2.21 - x          (high-Z)
            #              0.96 - 3.10*x     (low-Z)
            #
            # transition:
            # 12 + log(O/H) = 8.10
            # assuming solar 12 + log(O/H) = 8.69
            # -> log10(Z/Zsun) = -0.59
            # -------------------------------------------------

            Zrel = metal_c / Zsun

            # avoid log10(0) or negative metallicities
            valid = Zrel > 0.0

            DGR = np.zeros(len(m_c))

            log_Zrel = np.zeros(len(m_c))
            log_Zrel[valid] = np.log10(Zrel[valid])

            highZ = valid & (log_Zrel > -0.59)
            lowZ  = valid & (log_Zrel <= -0.59)

            # Gas-to-dust ratio
            log_GDR = np.zeros(len(m_c))

            log_GDR[highZ] = 2.21 - log_Zrel[highZ]
            log_GDR[lowZ]  = 0.96 - 3.10 * log_Zrel[lowZ]

            # Convert G/D -> D/G
            DGR[valid] = 10**(-log_GDR[valid])

            dust_mask = valid

            new_m_c = np.zeros(len(m_c))
            new_m_c[dust_mask] = m_c[dust_mask] * DGR[dust_mask]

            m_c = new_m_c
            metal_c = np.ones(len(m_c))
        print("done -- calculating metallicity dependent Dust-to-Gas ratio")
           
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!! For old stellar population
    
    if SED_type_o in ['Toddlers','toddlers','TODDLERS']:
        #!!! linear regression for the parameter space. 
        #!!! If you want to apply your model, try.

        x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
        dx_s_ind = 3 
        age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 4, 5, 6, 7, 8

        old_arr_len = 9
        if import_velocity == 'true':
            old_arr_len += 3
            vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
            age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 7, 8, 9, 10, 11

        if import_dispersion == 'true':
            old_arr_len += 1
            sig_s_ind = 7
            age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 8, 9, 10, 11, 12

        #!!!!!

        sort = (Age_Cut>abs(age_s))
        old_arr = np.empty((len(x_s[sort]), old_arr_len))

        old_arr[:,x_s_ind] = x_s[sort]
        old_arr[:,y_s_ind] = y_s[sort]
        old_arr[:,z_s_ind] = z_s[sort]
        old_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_o
        if import_velocity == 'true':
            old_arr[:,vx_s_ind] = vx_s[sort]
            old_arr[:,vy_s_ind] = vy_s[sort]
            old_arr[:,vz_s_ind] = vz_s[sort]
        if import_dispersion == 'true':
            old_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
        old_arr[:,age_s_ind] = age_s[sort]
        old_arr[:,metal_s_ind] = metal_s[sort]
        old_arr[:,sfe_s_ind] = sfe_s[sort]
        old_arr[:,cnd_s_ind] = cnd_s[sort]
        old_arr[:,m_s_ind] = m0_s[sort]

        header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
        header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
        header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
        header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
        if import_velocity == 'true':
            header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
            header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
            header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
        if import_dispersion == 'true':
            header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
        header += "Column %s: age (Gyr)\n" %(age_s_ind+1)
        header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
        header += "Column %s: star formation efficiency (1)\n" %(sfe_s_ind+1)
        header += "Column %s: Cloud number density (1/cm3)\n" %(cnd_s_ind+1)
        header += "Column %s: mass (Msun)\n" %(m_s_ind+1)

        np.savetxt(
            old_fbase+old_fname,
            old_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
    
    else:
        x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
        dx_s_ind = 3 
        m_s_ind, metal_s_ind, age_s_ind = 4, 5, 6

        old_arr_len = 7
        if import_velocity == 'true':
            old_arr_len += 3
            vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
            m_s_ind, metal_s_ind, age_s_ind = 7, 8, 9

        if import_dispersion == 'true':
            old_arr_len += 1
            sig_s_ind = 7
            m_s_ind, metal_s_ind, age_s_ind = 8, 9, 10

        # if add_young == True:
        #     sort = (Age_Cut<=abs(age_s))
        # else:
        #     sort = (0<abs(age_s))
        sort = (Age_Cut<=abs(age_s)) 

        old_arr = np.empty((len(x_s[sort]), old_arr_len))

        old_arr[:,x_s_ind] = x_s[sort]
        old_arr[:,y_s_ind] = y_s[sort]
        old_arr[:,z_s_ind] = z_s[sort]
        if adaptive_smoothing==True:
            old_arr[:,dx_s_ind] = dx_adaptive[sort]
        else:
            old_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_o
        if import_velocity == 'true':
            old_arr[:,vx_s_ind] = vx_s[sort]
            old_arr[:,vy_s_ind] = vy_s[sort]
            old_arr[:,vz_s_ind] = vz_s[sort]
        if import_dispersion == 'true':
            old_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
        old_arr[:,m_s_ind] = m0_s[sort]
        old_arr[:,metal_s_ind] = metal_s[sort]
        old_arr[:,age_s_ind] = age_s[sort]

        header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
        header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
        header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
        header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
        if import_velocity == 'true':
            header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
            header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
            header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
        if import_dispersion == 'true':
            header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
        header += "Column %s: mass (Msun)\n" %(m_s_ind+1)
        header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
        header += "Column %s: age (Gyr)\n" %(age_s_ind+1)

        np.savetxt(
            old_fbase+old_fname,
            old_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)

    print("done -- writing old population")
    #!!! For young stellar population
    if add_young == True:
        if SED_type_y == 'BC03':
            sort = (Age_Cut>age_s)
            young_arr = np.empty((len(x_s[sort]), old_arr_len))

            young_arr[:,x_s_ind] = x_s[sort]
            young_arr[:,y_s_ind] = y_s[sort]
            young_arr[:,z_s_ind] = z_s[sort]
            young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s
            if adaptive_smoothing==True:
                young_arr[:,dx_s_ind] = dx_adaptive[sort]
            else:
                young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_y
        
            if import_velocity == 'true':
                young_arr[:,vx_s_ind] = vx_s[sort]
                young_arr[:,vy_s_ind] = vy_s[sort]
                young_arr[:,vz_s_ind] = vz_s[sort]
            if import_dispersion == 'true':
                young_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
            young_arr[:,m_s_ind] = m0_s[sort]
            young_arr[:,metal_s_ind] = metal_s[sort]
            young_arr[:,age_s_ind] = age_s[sort]

            header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
            header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
            header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
            header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
            if import_velocity == 'true':
                header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
                header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
                header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
            if import_dispersion == 'true':
                header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
            header += "Column %s: mass (Msun)\n" %(m_s_ind+1)
            header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
            header += "Column %s: age (Gyr)\n" %(age_s_ind+1)

            np.savetxt(
                young_fbase+young_fname,
                young_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
            
            
        elif SED_type_y == 'mappings':
            #!!! linear regression for the parameter space. 
            #!!! If you want to apply your model, try.
            a_prs, b_prs, c_prs = 0.4, 10, -8.86
            a_cpt, b_cpt, c_cpt = 0.25, 10, 6.5
            t_clr = 0.003 #[Gyr]
            
            prs_s = 10**(a_prs*(age_s-b_prs)+c_prs)
            cpt_s = a_cpt*(age_s-b_cpt)+c_cpt
            fpdr_s = np.exp(-age_s/t_clr)
            
            #!!!!!
            
            x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
            dx_s_ind = 3 
            sfr_s_ind, metal_s_ind, cpt_s_ind, prs_s_ind, fpdr_s_ind = 4, 5, 6, 7, 8

            young_arr_len = 9
            if import_velocity == 'true':
                young_arr_len += 3
                vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
                sfr_s_ind, metal_s_ind, cpt_s_ind, prs_s_ind, fpdr_s_ind = 7, 8, 9, 10, 11

            if import_dispersion == 'true':
                young_arr_len += 1
                sig_s_ind = 7
                sfr_s_ind, metal_s_ind, cpt_s_ind, prs_s_ind, fpdr_s_ind = 8, 9, 10, 11, 12
            
            #!!!!!
            
            sort = (Age_Cut>age_s)
            young_arr = np.empty((len(x_s[sort]), young_arr_len))

            young_arr[:,x_s_ind] = x_s[sort]
            young_arr[:,y_s_ind] = y_s[sort]
            young_arr[:,z_s_ind] = z_s[sort]
            young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_y
            if import_velocity == 'true':
                young_arr[:,vx_s_ind] = vx_s[sort]
                young_arr[:,vy_s_ind] = vy_s[sort]
                young_arr[:,vz_s_ind] = vz_s[sort]
            if import_dispersion == 'true':
                young_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
            young_arr[:,sfr_s_ind] = m0_s[sort]/(age_s[sort]*1e9)
            young_arr[:,metal_s_ind] = metal_s[sort]
            young_arr[:,cpt_s_ind] = cpt_s[sort]
            young_arr[:,prs_s_ind] = prs_s[sort]
            young_arr[:,fpdr_s_ind] = fpdr_s[sort]

            header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
            header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
            header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
            header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
            if import_velocity == 'true':
                header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
                header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
                header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
            if import_dispersion == 'true':
                header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
            header += "Column %s: star formation rate (Msun/yr)\n" %(sfr_s_ind+1)
            header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
            header += "Column %s: compactness (1)\n" %(cpt_s_ind+1)
            header += "Column %s: pressure (Pa)\n" %(prs_s_ind+1)
            header += "Column %s: covering factor (1)\n" %(fpdr_s_ind+1)

            np.savetxt(
                young_fbase+young_fname,
                young_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
    
        elif SED_type_y in ['Toddlers','toddlers','TODDLERS']:
            #!!! linear regression for the parameter space. 
            #!!! If you want to apply your model, try.
            
            x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
            dx_s_ind = 3 
            # age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 4, 5, 6, 7, 8
            metal_s_ind, sfe_s_ind, cnd_s_ind, sfr_s_ind = 4,5,6,7
            young_arr_len = 8
            if import_velocity == 'true':
                young_arr_len += 3
                vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
                age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 7, 8, 9, 10, 11
    
            if import_dispersion == 'true':
                young_arr_len += 1
                sig_s_ind = 7
                age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 8, 9, 10, 11, 12
            
            #!!!!!
            
            sort = (Age_Cut>age_s)
            young_arr = np.empty((len(x_s[sort]), young_arr_len))

            young_arr[:,x_s_ind] = x_s[sort]
            young_arr[:,y_s_ind] = y_s[sort]
            young_arr[:,z_s_ind] = z_s[sort]
            young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_y
            if import_velocity == 'true':
                young_arr[:,vx_s_ind] = vx_s[sort]
                young_arr[:,vy_s_ind] = vy_s[sort]
                young_arr[:,vz_s_ind] = vz_s[sort]
            if import_dispersion == 'true':
                young_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
            # young_arr[:,age_s_ind] = age_s[sort]
            young_arr[:,metal_s_ind] = metal_s[sort]
            young_arr[:,sfe_s_ind] = sfe_s[sort]
            young_arr[:,cnd_s_ind] = cnd_s[sort]
            # young_arr[:,m_s_ind] = m0_s[sort]
            # young_arr[:,sfr_s_ind] = sfr_s[sort]
            young_arr[:,sfr_s_ind] = m0_s[sort]/(30*1e6) # 편의를 위해 30으로 고정했습니다.
            header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
            header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
            header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
            header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
            if import_velocity == 'true':
                header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
                header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
                header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
            if import_dispersion == 'true':
                header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
            # header += "Column %s: age (Gyr)\n" %(age_s_ind+1)
            header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
            header += "Column %s: star formation efficiency (1)\n" %(sfe_s_ind+1)
            header += "Column %s: cloud number density (1/cm3)\n" %(cnd_s_ind+1)
            header += "Column %s: star formation rate (Msun/yr)\n"%(sfr_s_ind+1)
            # header += "Column %s: mass (Msun)\n" %(m_s_ind+1)

            np.savetxt(
                young_fbase+young_fname,
                young_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
    
        print("done -- writing young population")
    
    #!!! For gas cells
    
    if cell_medium == False:
        x_c_ind, y_c_ind, z_c_ind = 0, 1, 2
        dx_c_ind = 3 
        m_c_ind, metal_c_ind, T_c_ind = 4, 5, 6

        gas_arr_len = 7
        if import_velocity_gas == 'true':
            gas_arr_len += 3
            vx_c_ind, vy_c_ind, vz_c_ind = 7, 8, 9

        if import_dispersion_gas == 'true':
            gas_arr_len += 1
            sig_c_ind = 10

        gas_arr = np.empty((len(x_c), gas_arr_len))

        gas_arr[:,x_c_ind] = x_c
        gas_arr[:,y_c_ind] = y_c
        gas_arr[:,z_c_ind] = z_c
        gas_arr[:,dx_c_ind] = dx_c *fact_dx
        if import_velocity_gas == 'true':
            gas_arr[:,vx_c_ind] = vx_c
            gas_arr[:,vy_c_ind] = vy_c
            gas_arr[:,vz_c_ind] = vz_c
        if import_dispersion_gas == 'true':
            gas_arr[:,sig_c_ind] = np.ones(len(x_c))*sig_c
        gas_arr[:,m_c_ind] = m_c
        gas_arr[:,metal_c_ind] = metal_c
        gas_arr[:,T_c_ind] = T_c

        header = "Column %s: position x (kpc)\n" %(x_c_ind+1)
        header += "Column %s: position y (kpc)\n" %(y_c_ind+1)
        header += "Column %s: position z (kpc)\n" %(z_c_ind+1)
        header += "Column %s: smoothing length (kpc)\n" %(dx_c_ind+1)
        header += "Column %s: mass (Msun)\n" %(m_c_ind+1)
        header += "Column %s: metallicity (1)\n" %(metal_c_ind+1)
        header += "Column %s: Temperature (K)\n" %(T_c_ind+1)
        if import_velocity_gas == 'true':
            header += "Column %s: velocity x (km/s)\n" %(vx_c_ind+1)
            header += "Column %s: velocity y (km/s)\n" %(vy_c_ind+1)
            header += "Column %s: velocity z (km/s)\n" %(vz_c_ind+1)
        if import_dispersion_gas == 'true':
            header += "Column %s: velocity dispersion (km/s)\n" %(sig_c_ind+1)

        np.savetxt(
            gas_fbase+gas_fname,
            gas_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
    
    elif cell_medium == True:
        x_min_ind,x_max_ind = 0, 3
        y_min_ind,y_max_ind = 1, 4
        z_min_ind,z_max_ind = 2, 5
        m_c_ind, metal_c_ind, T_c_ind = 6, 7, 8

        gas_arr_len = T_c_ind+1
        if import_velocity_gas == 'true' or import_velocity_gas == True:
            vx_c_ind, vy_c_ind, vz_c_ind = gas_arr_len, gas_arr_len+1, gas_arr_len+2
            gas_arr_len += 3

        if import_dispersion_gas == 'true' or import_dispersion_gas == True:
            sig_c_ind = gas_arr_len
            gas_arr_len += 1
        
        if on_the_fly_dust == 'true' or on_the_fly_dust == True:
            mCs_c_ind, mCl_c_ind, mSils_c_ind, mSill_c_ind = gas_arr_len, gas_arr_len+1, gas_arr_len+2, gas_arr_len+3
            gas_arr_len += 4
            if add_pah == 'true' or add_pah == True:
                mPn_ind, mPi_ind = gas_arr_len, gas_arr_len+1
                gas_arr_len += 2
            
        gas_arr = np.empty((len(x_c), gas_arr_len))

        gas_arr[:,x_min_ind] = x_c-0.5*dx_c
        gas_arr[:,x_max_ind] = x_c+0.5*dx_c
        gas_arr[:,y_min_ind] = y_c-0.5*dx_c
        gas_arr[:,y_max_ind] = y_c+0.5*dx_c
        gas_arr[:,z_min_ind] = z_c-0.5*dx_c
        gas_arr[:,z_max_ind] = z_c+0.5*dx_c
        gas_arr[:,m_c_ind] = m_c/(1e3*dx_c)**3
        gas_arr[:,metal_c_ind] = metal_c
        gas_arr[:,T_c_ind] = T_c
        if import_velocity_gas == 'true' or import_velocity_gas == True:
            gas_arr[:,vx_c_ind] = vx_c
            gas_arr[:,vy_c_ind] = vy_c
            gas_arr[:,vz_c_ind] = vz_c
        if import_dispersion_gas == 'true' or import_dispersion_gas == True:
            gas_arr[:,sig_c_ind] = np.ones(len(x_c))*sig_c
        if on_the_fly_dust == 'true' or on_the_fly_dust == True:
            gas_arr[:,mCs_c_ind] = mC_small/(1e3*dx_c)**3
            gas_arr[:,mCl_c_ind] = mC_large/(1e3*dx_c)**3
            gas_arr[:,mSils_c_ind] = mSil_small/(1e3*dx_c)**3
            gas_arr[:,mSill_c_ind] = mSil_large/(1e3*dx_c)**3
            if add_pah == 'true' or add_pah == True:
                gas_arr[:,mPn_ind] = mPAHneu/(1e3*dx_c)**3
                gas_arr[:,mPi_ind] = mPAHion/(1e3*dx_c)**3

        header = "Column %s: x-min (kpc)\n" %(x_min_ind+1)
        header += "Column %s: y-min (kpc)\n" %(y_min_ind+1)   
        header += "Column %s: z-min (kpc)\n" %(z_min_ind+1)
        header += "Column %s: x-max (kpc)\n" %(x_max_ind+1)
        header += "Column %s: y-max (kpc)\n" %(y_max_ind+1)
        header += "Column %s: z-max (kpc)\n" %(z_max_ind+1)
        header += "Column %s: mass volume density (Msun/pc3)\n" %(m_c_ind+1)
        header += "Column %s: metallicity (1)\n" %(metal_c_ind+1)
        header += "Column %s: temperature (K)\n" %(T_c_ind+1)
        if import_velocity_gas == 'true' or import_velocity_gas == True:
            header += "Column %s: velocity x (km/s)\n" %(vx_c_ind+1)
            header += "Column %s: velocity y (km/s)\n" %(vy_c_ind+1)
            header += "Column %s: velocity z (km/s)\n" %(vz_c_ind+1)
        if import_dispersion_gas == 'true' or import_dispersion_gas == True:
            header += "Column %s: velocity dispersion (km/s)\n" %(sig_c_ind+1)
        if on_the_fly_dust == 'true' or on_the_fly_dust == True:
            header += "Column %s: small carbonaceous density (Msun/pc3)\n" %(mCs_c_ind+1)
            header += "Column %s: large carbonaceous density (Msun/pc3)\n" %(mCl_c_ind+1)
            header += "Column %s: small silicates density (Msun/pc3)\n" %(mSils_c_ind+1)
            header += "Column %s: large silicates density (Msun/pc3)\n" %(mSill_c_ind+1)
        if add_pah == 'true' or add_pah == True:
            header += "Column %s: pah neutral density (Msun/pc3)\n" %(mPn_ind+1)
            header += "Column %s: pah ionized density (Msun/pc3)\n" %(mPi_ind+1)

        np.savetxt(
            gas_fbase+gas_fname,
            gas_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
        
    print("done -- writing gas cells")
    
    return









def make_input0(
                boxtokpc,
                x_s,
                y_s,
                z_s,
                vx_s,
                vy_s,
                vz_s,
                m_s,
                m0_s,
                age_s,
                metal_s,
                cnd_s,
                sfe_s,

                pos_ctr,
                vel_ctr,
                        
                dx_dirt=[],
            
                l_simbox=1,

                # gal rotation
                rotating_gal=True,
                R_upp=8,
                R_low=2,
                A_upp=8,
                mass_weight=True,
                par_mode='median',

                # Stellar population
                sig_s = 10, #[km/s]

                # Old population
                old_fbase = './',
                old_fname = 'part_old.txt',

                # Young star selection criteria
                add_young=False,

                young_fbase = './',
                young_fname = 'part_young.txt',

                Age_Cut = 0.01, #[Myr]
                SED_type_o='BC03',
                SED_type_y='mappings',

                # Using additional columns?
                import_velocity='true',
                import_dispersion='false',

                dx_s_o = 50, #[pc]
                dx_s_y = 50, #[pc]
                adaptive_smoothing=False,
                n_targ_nbr=5,
                n_job_smoothing=32,
                ):
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    if adaptive_smoothing == True:
        from sklearn.neighbors import NearestNeighbors

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    x_s = (x_s - pos_ctr[0]) * boxtokpc
    y_s = (y_s - pos_ctr[1]) * boxtokpc
    z_s = (z_s - pos_ctr[2]) * boxtokpc
    
    vx_s -= vel_ctr[0]
    vy_s -= vel_ctr[1]
    vz_s -= vel_ctr[2]
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    print("done -- basic setting")
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if rotating_gal == True:
        x_s, y_s, z_s, vx_s, vy_s, vz_s, par_rot =  Ang_Rot( 
                                                            M=m_s,
                                                            X=x_s,Y=y_s,Z=z_s,
                                                            VX=vx_s,VY=vy_s,VZ=vz_s,
                                                            age=age_s,
                                                            R_upp=R_upp,R_low=R_low,
                                                            A_upp=A_upp,
                                                            mass_weight=mass_weight,
                                                            par_mode=par_mode,
                                                            Param=True
                                                            )               

        print("done -- galaxy rotation")
        
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    if adaptive_smoothing == True:    
        print("start -- calculating distance to the Nth-nearest neighbor (N=%s)"%(n_targ_nbr))
        X = (x_s).reshape(-1,1)
        Y = (y_s).reshape(-1,1)
        Z = (z_s).reshape(-1,1)
        XSET = np.hstack((X,Y,Z))
        nbrs = NearestNeighbors(n_neighbors=n_targ_nbr+1, algorithm='auto',n_jobs=n_job_smoothing).fit(XSET)
        distances, indices = nbrs.kneighbors(XSET)
        dx_adaptive = distances[:,n_targ_nbr]*1e3 #kpc to pc
        print("done -- calculating distance to the Nth-nearest neighbor (N=%s)"%(n_targ_nbr))
        
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!! For old stellar population
    
    if SED_type_o in ['Toddlers','toddlers','TODDLERS']:
        #!!! linear regression for the parameter space. 
        #!!! If you want to apply your model, try.

        x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
        dx_s_ind = 3 
        age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 4, 5, 6, 7, 8

        old_arr_len = 9
        if import_velocity == 'true':
            old_arr_len += 3
            vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
            age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 7, 8, 9, 10, 11

        if import_dispersion == 'true':
            old_arr_len += 1
            sig_s_ind = 7
            age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 8, 9, 10, 11, 12

        #!!!!!

        sort = (Age_Cut>abs(age_s))
        old_arr = np.empty((len(x_s[sort]), old_arr_len))

        old_arr[:,x_s_ind] = x_s[sort]
        old_arr[:,y_s_ind] = y_s[sort]
        old_arr[:,z_s_ind] = z_s[sort]
        old_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_o
        if import_velocity == 'true':
            old_arr[:,vx_s_ind] = vx_s[sort]
            old_arr[:,vy_s_ind] = vy_s[sort]
            old_arr[:,vz_s_ind] = vz_s[sort]
        if import_dispersion == 'true':
            old_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
        old_arr[:,age_s_ind] = age_s[sort]
        old_arr[:,metal_s_ind] = metal_s[sort]
        old_arr[:,sfe_s_ind] = sfe_s[sort]
        old_arr[:,cnd_s_ind] = cnd_s[sort]
        old_arr[:,m_s_ind] = m0_s[sort]

        header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
        header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
        header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
        header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
        if import_velocity == 'true':
            header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
            header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
            header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
        if import_dispersion == 'true':
            header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
        header += "Column %s: age (Gyr)\n" %(age_s_ind+1)
        header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
        header += "Column %s: star formation efficiency (1)\n" %(sfe_s_ind+1)
        header += "Column %s: Cloud number density (1/cm3)\n" %(cnd_s_ind+1)
        header += "Column %s: mass (Msun)\n" %(m_s_ind+1)

        np.savetxt(
            old_fbase+old_fname,
            old_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
    
    else:
        x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
        dx_s_ind = 3 
        m_s_ind, metal_s_ind, age_s_ind = 4, 5, 6

        old_arr_len = 7
        if import_velocity == 'true':
            old_arr_len += 3
            vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
            m_s_ind, metal_s_ind, age_s_ind = 7, 8, 9

        if import_dispersion == 'true':
            old_arr_len += 1
            sig_s_ind = 7
            m_s_ind, metal_s_ind, age_s_ind = 8, 9, 10

        if add_young == True:
            sort = (Age_Cut<=abs(age_s))
        else:
            sort = (0<abs(age_s))

        old_arr = np.empty((len(x_s[sort]), old_arr_len))

        old_arr[:,x_s_ind] = x_s[sort]
        old_arr[:,y_s_ind] = y_s[sort]
        old_arr[:,z_s_ind] = z_s[sort]
        if adaptive_smoothing==True:
            old_arr[:,dx_s_ind] = dx_adaptive[sort]
        else:
            old_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_o
        if import_velocity == 'true':
            old_arr[:,vx_s_ind] = vx_s[sort]
            old_arr[:,vy_s_ind] = vy_s[sort]
            old_arr[:,vz_s_ind] = vz_s[sort]
        if import_dispersion == 'true':
            old_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
        old_arr[:,m_s_ind] = m0_s[sort]
        old_arr[:,metal_s_ind] = metal_s[sort]
        old_arr[:,age_s_ind] = age_s[sort]

        header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
        header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
        header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
        header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
        if import_velocity == 'true':
            header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
            header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
            header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
        if import_dispersion == 'true':
            header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
        header += "Column %s: mass (Msun)\n" %(m_s_ind+1)
        header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
        header += "Column %s: age (Gyr)\n" %(age_s_ind+1)

        np.savetxt(
            old_fbase+old_fname,
            old_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)

    print("done -- writing old population")
    #!!! For young stellar population
    if add_young == True:
        if SED_type_y == 'BC03':
            sort = (Age_Cut>age_s)
            young_arr = np.empty((len(x_s[sort]), old_arr_len))

            young_arr[:,x_s_ind] = x_s[sort]
            young_arr[:,y_s_ind] = y_s[sort]
            young_arr[:,z_s_ind] = z_s[sort]
            young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s
            if adaptive_smoothing==True:
                young_arr[:,dx_s_ind] = dx_adaptive[sort]
            else:
                young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_y
        
            if import_velocity == 'true':
                young_arr[:,vx_s_ind] = vx_s[sort]
                young_arr[:,vy_s_ind] = vy_s[sort]
                young_arr[:,vz_s_ind] = vz_s[sort]
            if import_dispersion == 'true':
                young_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
            young_arr[:,m_s_ind] = m0_s[sort]
            young_arr[:,metal_s_ind] = metal_s[sort]
            young_arr[:,age_s_ind] = age_s[sort]

            header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
            header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
            header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
            header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
            if import_velocity == 'true':
                header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
                header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
                header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
            if import_dispersion == 'true':
                header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
            header += "Column %s: mass (Msun)\n" %(m_s_ind+1)
            header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
            header += "Column %s: age (Gyr)\n" %(age_s_ind+1)

            np.savetxt(
                young_fbase+young_fname,
                young_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
            
            
        elif SED_type_y == 'mappings':
            #!!! linear regression for the parameter space. 
            #!!! If you want to apply your model, try.
            a_prs, b_prs, c_prs = 0.4, 10, -8.86
            a_cpt, b_cpt, c_cpt = 0.25, 10, 6.5
            t_clr = 0.003 #[Gyr]
            
            prs_s = 10**(a_prs*(age_s-b_prs)+c_prs)
            cpt_s = a_cpt*(age_s-b_cpt)+c_cpt
            fpdr_s = np.exp(-age_s/t_clr)
            
            #!!!!!
            
            x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
            dx_s_ind = 3 
            sfr_s_ind, metal_s_ind, cpt_s_ind, prs_s_ind, fpdr_s_ind = 4, 5, 6, 7, 8

            young_arr_len = 9
            if import_velocity == 'true':
                young_arr_len += 3
                vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
                sfr_s_ind, metal_s_ind, cpt_s_ind, prs_s_ind, fpdr_s_ind = 7, 8, 9, 10, 11

            if import_dispersion == 'true':
                young_arr_len += 1
                sig_s_ind = 7
                sfr_s_ind, metal_s_ind, cpt_s_ind, prs_s_ind, fpdr_s_ind = 8, 9, 10, 11, 12
            
            #!!!!!
            
            sort = (Age_Cut>age_s)
            young_arr = np.empty((len(x_s[sort]), young_arr_len))

            young_arr[:,x_s_ind] = x_s[sort]
            young_arr[:,y_s_ind] = y_s[sort]
            young_arr[:,z_s_ind] = z_s[sort]
            young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_y
            if import_velocity == 'true':
                young_arr[:,vx_s_ind] = vx_s[sort]
                young_arr[:,vy_s_ind] = vy_s[sort]
                young_arr[:,vz_s_ind] = vz_s[sort]
            if import_dispersion == 'true':
                young_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
            young_arr[:,sfr_s_ind] = m0_s[sort]/(age_s[sort]*1e9)
            young_arr[:,metal_s_ind] = metal_s[sort]
            young_arr[:,cpt_s_ind] = cpt_s[sort]
            young_arr[:,prs_s_ind] = prs_s[sort]
            young_arr[:,fpdr_s_ind] = fpdr_s[sort]

            header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
            header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
            header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
            header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
            if import_velocity == 'true':
                header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
                header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
                header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
            if import_dispersion == 'true':
                header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
            header += "Column %s: star formation rate (Msun/yr)\n" %(sfr_s_ind+1)
            header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
            header += "Column %s: compactness (1)\n" %(cpt_s_ind+1)
            header += "Column %s: pressure (Pa)\n" %(prs_s_ind+1)
            header += "Column %s: covering factor (1)\n" %(fpdr_s_ind+1)

            np.savetxt(
                young_fbase+young_fname,
                young_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
    
        elif SED_type_y in ['Toddlers','toddlers','TODDLERS']:
            #!!! linear regression for the parameter space. 
            #!!! If you want to apply your model, try.
            
            x_s_ind, y_s_ind, z_s_ind = 0, 1, 2
            dx_s_ind = 3 
            age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 4, 5, 6, 7, 8

            young_arr_len = 9
            if import_velocity == 'true':
                young_arr_len += 3
                vx_s_ind, vy_s_ind, vz_s_ind = 4, 5, 6
                age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 7, 8, 9, 10, 11

            if import_dispersion == 'true':
                young_arr_len += 1
                sig_s_ind = 7
                age_s_ind, metal_s_ind, sfe_s_ind, cnd_s_ind, m_s_ind = 8, 9, 10, 11, 12
            
            #!!!!!
            
            sort = (Age_Cut>age_s)
            young_arr = np.empty((len(x_s[sort]), young_arr_len))

            young_arr[:,x_s_ind] = x_s[sort]
            young_arr[:,y_s_ind] = y_s[sort]
            young_arr[:,z_s_ind] = z_s[sort]
            young_arr[:,dx_s_ind] = np.ones(len(x_s[sort]))*dx_s_y
            if import_velocity == 'true':
                young_arr[:,vx_s_ind] = vx_s[sort]
                young_arr[:,vy_s_ind] = vy_s[sort]
                young_arr[:,vz_s_ind] = vz_s[sort]
            if import_dispersion == 'true':
                young_arr[:,sig_s_ind] = np.ones(len(x_s[sort]))*sig_s
            young_arr[:,age_s_ind] = age_s[sort]
            young_arr[:,metal_s_ind] = metal_s[sort]
            young_arr[:,sfe_s_ind] = sfe_s[sort]
            young_arr[:,cnd_s_ind] = cnd_s[sort]
            young_arr[:,m_s_ind] = m0_s[sort]

            header = "Column %s: position x (kpc)\n" %(x_s_ind+1)
            header += "Column %s: position y (kpc)\n" %(y_s_ind+1)
            header += "Column %s: position z (kpc)\n" %(z_s_ind+1)
            header += "Column %s: smoothing length (pc)\n" %(dx_s_ind+1)
            if import_velocity == 'true':
                header += "Column %s: velocity x (km/s)\n" %(vx_s_ind+1)
                header += "Column %s: velocity y (km/s)\n" %(vy_s_ind+1)
                header += "Column %s: velocity z (km/s)\n" %(vz_s_ind+1)
            if import_dispersion == 'true':
                header += "Column %s: velocity dispersion (km/s)\n" %(sig_s_ind+1)
            header += "Column %s: age (Gyr)\n" %(age_s_ind+1)
            header += "Column %s: metallicity (1)\n" %(metal_s_ind+1)
            header += "Column %s: star formation efficiency (1)\n" %(sfe_s_ind+1)
            header += "Column %s: Cloud number density (1/cm3)\n" %(cnd_s_ind+1)
            header += "Column %s: mass (Msun)\n" %(m_s_ind+1)

            np.savetxt(
                young_fbase+young_fname,
                young_arr, delimiter=' ', newline='\n', header=header, footer='', comments='# ', encoding=None)
    
        print("done -- writing young population")
    
        
    print("done -- writing gas cells")
    
    return


