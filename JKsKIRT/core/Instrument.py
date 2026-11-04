import numpy as np
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Instrument System
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def Inst_System(
                wfile,

                def_wv_grid,
               includeGALEX,
               includejohnson,
               includespitzer,
               includeSDSS,
               include2MASS,
               includeWISE,
               includeHERSCHEL,
               CustomFilterList,

               inst_dist_unit,
               inst_dist,

               inc_default,
               azm_default,
               roll_default,

               inc_min,
               inc_max,
               inc_del,

               azm_min,
               azm_max,
               azm_del,

               recordComponents,
               recordPolarization,
               recordStatistics,
               numScatteringLevels,

               #@@@!!! fullInstrument
               fov_unit,
               fov_X,
               fov_Y,

               pscale_X,
               pscale_Y,

               centre_X,
               centre_Y,

               #@@@!!! SEDInstrument
               save_1d_sed,
               aperture_unit,
               aperture_min,
               aperture_max,
               aper_del,

               inst_sed_grid_type,
               inst_sed_grid_unit,
               inst_sed_min_wv,
               inst_sed_max_wv,
               inst_sed_N_wv,

               indent,
               indent_base,

               inst_sed_min_wv_sub = 0.4,
               inst_sed_max_wv_sub = 0.7,
               inst_sed_N_wv_sub = 3001,

               inst_2d_sed_on=False,
               inst_2d_sed_unit='micron',
               inst_2d_sed_type = 'log',
               inst_2d_sed_min_wv = 0.09,
               inst_2d_sed_max_wv = 1000,
               inst_2d_sed_N_wv = 100,
               inst_2d_sed_min_wv_sub = 0.4,
               inst_2d_sed_max_wv_sub = 0.7,
               inst_2d_sed_N_wv_sub = 200,
               inst_2d_sed_repo='./',
               inst_2d_sed_fname='inst_2d_sed.txt',
               inst_2d_sed_relHW=0,
               visual = False,
               inst_1d_sed_only=False,
               los_angles=None
                ):


    N_idt = indent_base
    sed_only = inst_1d_sed_only in [True, 'true']

    print((N_idt)*indent+'<instrumentSystem type="InstrumentSystem">',file=wfile)
    print((N_idt+1)*indent+'<InstrumentSystem>',file=wfile)
    print((N_idt+2)*indent+'<defaultWavelengthGrid type="WavelengthGrid">',file=wfile)

    if sed_only:
        print((N_idt+3)*indent+'<LogWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(inst_sed_min_wv,inst_sed_grid_unit,inst_sed_max_wv,inst_sed_grid_unit,inst_sed_N_wv),file=wfile)
    elif def_wv_grid == 'pre-defined':
        print((N_idt+3)*indent+'<PredefinedBandWavelengthGrid includeGALEX="%s" includejohnson="%s" includespitzer="%s" includeSDSS="%s" include2MASS="%s" includeWISE="%s" includeHERSCHEL="%s"/>'%(includeGALEX,includejohnson,includespitzer,includeSDSS,include2MASS,includeWISE,includeHERSCHEL),file=wfile)

    print((N_idt+2)*indent+'</defaultWavelengthGrid>',file=wfile)
    print((N_idt+2)*indent+'<instruments type="Instrument">',file=wfile)

    #!!!

    if los_angles is None:
        if inc_min != inc_max:
            inc_space = np.linspace(inc_min,inc_max,int((inc_max-inc_min)/inc_del+1)).astype(np.int32)
        else:
            inc_space = np.array([inc_min]).astype(np.int32)

        if inc_default == 'kapoor':
            inc_space = np.array([0,26,37,46,53,60,66,73,90]).astype(np.int32)

        if azm_min != azm_max:
            azm_space = np.linspace(azm_min,azm_max,int((azm_max-azm_min)/azm_del+1)).astype(np.int32)
        else:
            azm_space = np.array([azm_min]).astype(np.int32)

        directions = [(inc, azm) for inc in inc_space for azm in azm_space]
    else:
        directions = np.asarray(los_angles, dtype=float)
        if directions.ndim != 2 or directions.shape[1] != 2 or len(directions) == 0:
            raise ValueError("los_angles must be a nonempty (N, 2) array of inclination/azimuth in degrees")
        if not np.all(np.isfinite(directions)) or np.any((directions[:, 0] < 0) | (directions[:, 0] > 180)):
            raise ValueError("LOS angles must be finite, with inclination in [0, 180]")

    if save_1d_sed == True:
        if aperture_min != aperture_max:
            aptr_space = np.linspace(aperture_min,aperture_max,int((aperture_max-aperture_min)/aper_del+1)).astype(np.int32)
        else:
            aptr_space = np.array([aperture_min]).astype(np.int32)

    #!!!

    Npix_X = int(fov_X/pscale_X)
    Npix_Y = int(fov_Y/pscale_Y)

    for los_id, (inc_i, azm_j) in enumerate(directions):
        if los_angles is None:
            fname_ij = f'rot_{int(inc_i):03d}_{int(azm_j):03d}'
        else:
            fname_ij = f'los_{los_id:03d}'
        fname_ij_visual = fname_ij+"_visual"
        fname_ij_visual2 = fname_ij+"_visual2"
        fname_ij_visual4 = fname_ij+"_visual4"
        fname_ij_visual6 = fname_ij+"_visual6"
        fname_ij_visual8 = fname_ij+"_visual8"
        fname_ij_visual10 = fname_ij+"_visual10"
        fname_ij_visual24 = fname_ij+"_visual24"



        if not sed_only:
            if len(CustomFilterList) == 0:
                print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,Npix_X,centre_X,fov_unit,fov_Y,fov_unit,Npix_Y,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                if visual == True or visual == 'true':
                    print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij_visual,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,1031,centre_X,fov_unit,fov_Y,fov_unit,1031,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                    print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij_visual2,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,515,centre_X,fov_unit,fov_Y,fov_unit,515,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                    print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij_visual4,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,257,centre_X,fov_unit,fov_Y,fov_unit,257,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                    print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij_visual6,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,171,centre_X,fov_unit,fov_Y,fov_unit,171,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                    print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij_visual8,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,128,centre_X,fov_unit,fov_Y,fov_unit,128,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                    print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij_visual10,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,103,centre_X,fov_unit,fov_Y,fov_unit,103,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                    print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s"/>'%(fname_ij_visual24,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,42,centre_X,fov_unit,fov_Y,fov_unit,42,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)

            else:
                print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s">'%(fname_ij,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,Npix_X,centre_X,fov_unit,fov_Y,fov_unit,Npix_Y,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                print((N_idt+4)*indent+'<wavelengthGrid type="WavelengthGrid">',file=wfile)
                print((N_idt+5)*indent+'<ConfigurableBandWavelengthGrid>',file=wfile)
                print((N_idt+6)*indent+'<bands type="Band">',file=wfile)

                #includeGALEX,  includejohnson, includeSDSS,  include2MASS,    includeWISE, includeHERSCHEL,
                if includeGALEX in [True,'true']:
                    print((N_idt+7)*indent+'<BroadBand bandName="GALEX_GALEX_FUV"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="GALEX_GALEX_NUV"/>',file=wfile)
                if includeSDSS in [True,'true']:
                    print((N_idt+7)*indent+'<BroadBand bandName="SLOAN_SDSS_U"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="SLOAN_SDSS_G"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="SLOAN_SDSS_R"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="SLOAN_SDSS_I"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="SLOAN_SDSS_Z"/>',file=wfile)

                if includejohnson in [True,'true']:
                    print((N_idt+7)*indent+'<BroadBand bandName="GENERIC_JOHNSON_U"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="GENERIC_JOHNSON_B"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="GENERIC_JOHNSON_V"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="GENERIC_JOHNSON_J"/>',file=wfile)
                if includespitzer in [True,'true']:
                    print((N_idt+7)*indent+'<BroadBand bandName="SPITZER_IRAC_I1"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="SPITZER_IRAC_I2"/>',file=wfile)

                if include2MASS in [True,'true']:
                    print((N_idt+7)*indent+'<BroadBand bandName="2MASS_2MASS_J"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="2MASS_2MASS_H"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="2MASS_2MASS_KS"/>',file=wfile)
                if includeWISE in [True,'true']:
                    print((N_idt+7)*indent+'<BroadBand bandName="WISE_WISE_W1"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="WISE_WISE_W2"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="WISE_WISE_W3"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="WISE_WISE_W4"/>',file=wfile)
                if includeHERSCHEL in [True,'true']:
                    print((N_idt+7)*indent+'<BroadBand bandName="HERSCHEL_PACS_70"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="HERSCHEL_PACS_100"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="HERSCHEL_PACS_160"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="HERSCHEL_SPIRE_250"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="HERSCHEL_SPIRE_350"/>',file=wfile)
                    print((N_idt+7)*indent+'<BroadBand bandName="HERSCHEL_SPIRE_500"/>',file=wfile)

                cfl = 0
                while cfl < len(CustomFilterList):
                    print((N_idt+7)*indent+'<BroadBand bandName="%s"/>'%(CustomFilterList[cfl]),file=wfile)
                    cfl += 1

                print((N_idt+6)*indent+'</bands>',file=wfile)
                print((N_idt+5)*indent+'</ConfigurableBandWavelengthGrid>',file=wfile)
                print((N_idt+4)*indent+'</wavelengthGrid>',file=wfile)
                print((N_idt+3)*indent+'</FullInstrument>',file=wfile)

            # else:
            #     print((N_idt+3)*indent+'<FullInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s">'%(fname_ij,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,Npix_X,centre_X,fov_unit,fov_Y,fov_unit,Npix_Y,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
            #     print((N_idt+4)*indent+'<wavelengthGrid type="WavelengthGrid">',file=wfile)
            #     if inst_2d_sed_type == 'lin':
            #         print((N_idt+5)*indent+'<LinWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(inst_2d_sed_min_wv,inst_2d_sed_unit,inst_2d_sed_max_wv,inst_2d_sed_unit,inst_2d_sed_N_wv),file=wfile)
            #     elif inst_2d_sed_type == 'log':
            #         print((N_idt+5)*indent+'<LogWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(inst_2d_sed_min_wv,inst_2d_sed_unit,inst_2d_sed_max_wv,inst_2d_sed_unit,inst_2d_sed_N_wv),file=wfile)
            #     elif inst_2d_sed_type == 'nestlog':
            #         print((N_idt+5)*indent+'<NestedLogWavelengthGrid minWavelengthBaseGrid="%s %s" maxWavelengthBaseGrid="%s %s" numWavelengthsBaseGrid="%s" minWavelengthSubGrid="%s %s" maxWavelengthSubGrid="%s %s" numWavelengthsSubGrid="%s"/>'%(inst_2d_sed_min_wv,inst_2d_sed_unit,inst_2d_sed_max_wv,inst_2d_sed_unit,inst_2d_sed_N_wv,inst_2d_sed_min_wv_sub,inst_2d_sed_unit,inst_2d_sed_max_wv_sub,inst_2d_sed_unit,inst_2d_sed_N_wv_sub),file=wfile)
            #     elif inst_2d_sed_type == 'file':
            #         print((N_idt+5)*indent+'<FileWavelengthGrid filename="%s/%s" relativeHalfWidth="%s" log="true"/>'%(inst_2d_sed_repo,inst_2d_sed_fname,inst_2d_sed_relHW),file=wfile)

            #     print((N_idt+4)*indent+'</wavelengthGrid>',file=wfile)
            #     print((N_idt+3)*indent+'</FullInstrument>',file=wfile)
            if inst_2d_sed_on == True or inst_2d_sed_on == 'true':
                print((N_idt+3)*indent+'<FullInstrument instrumentName="%s_inst_2d" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" fieldOfViewX="%s %s" numPixelsX="%s" centerX="%s %s" fieldOfViewY="%s %s" numPixelsY="%s" centerY="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s">'%(fname_ij,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,fov_X,fov_unit,Npix_X,centre_X,fov_unit,fov_Y,fov_unit,Npix_Y,centre_Y,fov_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                print((N_idt+4)*indent+'<wavelengthGrid type="WavelengthGrid">',file=wfile)
                if inst_2d_sed_type == 'lin':
                    print((N_idt+5)*indent+'<LinWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(inst_2d_sed_min_wv,inst_2d_sed_unit,inst_2d_sed_max_wv,inst_2d_sed_unit,inst_2d_sed_N_wv),file=wfile)
                elif inst_2d_sed_type == 'log':
                    print((N_idt+5)*indent+'<LogWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(inst_2d_sed_min_wv,inst_2d_sed_unit,inst_2d_sed_max_wv,inst_2d_sed_unit,inst_2d_sed_N_wv),file=wfile)
                elif inst_2d_sed_type == 'nestlog':
                    print((N_idt+5)*indent+'<NestedLogWavelengthGrid minWavelengthBaseGrid="%s %s" maxWavelengthBaseGrid="%s %s" numWavelengthsBaseGrid="%s" minWavelengthSubGrid="%s %s" maxWavelengthSubGrid="%s %s" numWavelengthsSubGrid="%s"/>'%(inst_2d_sed_min_wv,inst_2d_sed_unit,inst_2d_sed_max_wv,inst_2d_sed_unit,inst_2d_sed_N_wv,inst_2d_sed_min_wv_sub,inst_2d_sed_unit,inst_2d_sed_max_wv_sub,inst_2d_sed_unit,inst_2d_sed_N_wv_sub),file=wfile)
                elif inst_2d_sed_type == 'file':
                    print((N_idt+5)*indent+'<FileWavelengthGrid filename="%s/%s" relativeHalfWidth="%s" log="true"/>'%(inst_2d_sed_repo,inst_2d_sed_fname,inst_2d_sed_relHW),file=wfile)

                print((N_idt+4)*indent+'</wavelengthGrid>',file=wfile)
                print((N_idt+3)*indent+'</FullInstrument>',file=wfile)


        if save_1d_sed == True:
            k = 0
            while k < len(aptr_space):
                aptr_k = aptr_space[k]
                if aptr_k//10 == 0:
                    fname_ijk = fname_ij + '_0%s'%(aptr_k)
                else:
                    fname_ijk = fname_ij + '_%s'%(aptr_k)

                print((N_idt+3)*indent+'<SEDInstrument instrumentName="%s" distance="%s %s" inclination="%s deg" azimuth="%s deg" roll="%s deg" radius="%s %s" recordComponents="%s" numScatteringLevels="%s" recordPolarization="%s" recordStatistics="%s">'%(fname_ijk,inst_dist,inst_dist_unit,inc_i,azm_j,roll_default,aptr_k,aperture_unit,recordComponents,numScatteringLevels,recordPolarization,recordStatistics),file=wfile)
                print((N_idt+4)*indent+'<wavelengthGrid type="WavelengthGrid">',file=wfile)

                if inst_sed_grid_type == 'lin':
                    print((N_idt+5)*indent+'<LinWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(inst_sed_min_wv,inst_sed_grid_unit,inst_sed_max_wv,inst_sed_grid_unit,inst_sed_N_wv),file=wfile)
                elif inst_sed_grid_type == 'log':
                    print((N_idt+5)*indent+'<LogWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(inst_sed_min_wv,inst_sed_grid_unit,inst_sed_max_wv,inst_sed_grid_unit,inst_sed_N_wv),file=wfile)
                elif inst_sed_grid_type == 'nestlog':
                    print((N_idt+5)*indent+'<NestedLogWavelengthGrid minWavelengthBaseGrid="%s %s" maxWavelengthBaseGrid="%s %s" numWavelengthsBaseGrid="%s" minWavelengthSubGrid="%s %s" maxWavelengthSubGrid="%s %s" numWavelengthsSubGrid="%s"/>'%(inst_sed_min_wv,inst_sed_grid_unit,inst_sed_max_wv,inst_sed_grid_unit,inst_sed_N_wv,inst_sed_min_wv_sub,inst_sed_grid_unit,inst_sed_max_wv_sub,inst_sed_grid_unit,inst_sed_N_wv_sub),file=wfile)

                print((N_idt+4)*indent+'</wavelengthGrid>',file=wfile)
                print((N_idt+3)*indent+'</SEDInstrument>',file=wfile)

                k += 1

    print((N_idt+2)*indent+'</instruments>',file=wfile)
    print((N_idt+1)*indent+'</InstrumentSystem>',file=wfile)
    print((N_idt)*indent+'</instrumentSystem>',file=wfile)

    return N_idt










