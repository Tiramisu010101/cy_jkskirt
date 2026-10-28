import numpy as np

from ..core import Base
from ..core import Source
from ..core import Medium
from ..core import Instrument
from ..core import Probe

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def writing_ski(
               #!!! Sim Mode
               mode='extinction', # 'transparent', 'extinction', 're-rad'
               #!!! Basic Settings
               N_phot=5e7,
               rnd_seed=12345,
               
               wavelengthOutputStyle='Wavelength',
               fluxOutputStyle='Wavelength',
               
               #!!! Cosmology
               z_red=0,
               H_0=0.675,
               Om_m=0.31,
               
               #!!! Source System
               #@@@ general setting 
               source_unit='micron',
               wv_source_min=0.0091, # micron
               wv_source_max=1000, # micron
               wv_source_del=0.01, # micron
               source_bias=0.5, 
               
               bias_type='log',
               bias_unit='micron',
               wv_bias_min=0.0091,
               wv_bias_max=1000,

               import_velocity='true',
               import_dispersion='false',
               source_weight=1,
               bias_deg=0.5,
               
               #@@@ old particles
               smoothing_kernel_o='cubic',
               SED_type_o='BC03',
               SED_IMF_o='Chabrier',
               SED_res_o='High',
               SED_type_original_o='BPASS',
               f_conv_o=0.68,
               lya_disp_o=50,
               lya_shape_o='gaussian',
               
               #@@@ young particles
               add_young=False,
               smoothing_kernel_y='cubic',
               SED_type_y='BC03',
               SED_IMF_y='Chabrier',
               SED_res_y='High',
               SED_type_original_y='BPASS',
               f_conv_y=0.68,
               lya_disp_y=50,
               lya_shape_y='gaussian',
               tod_sedtemplate='BPASSChab300Bin',
               tod_includedust='true',
               tod_sfrperiod='Period10Myr',
               
               #!!! Medium System
               forceScattering='true',
               minWeightReduction=1e4,
               minScattEvents=0,
               pathLengthBias=0.5,
    
               explicitAbsorption='false',
               lyaAccelerationScheme='Variable',
               lyaAccelerationStrength=1,
               includeHubbleFlow='false',
               maxTemperature_lya=2e4,
               defaultTemperature=1e4,
               includePolarization='false',
               dustEmissionOptions='false',
               dustemtype='Equilibrium',
               
               storeRadiationField='true',
               radfield_type='log',
               radfield_unit='micron',
               radfield_min_wv=0.1, # micron
               radfield_max_wv=1000, # micron
               radfield_N_wv=50001, # micron
               
               med_type='particle',
               med_Mfrac=0.4, #directly related to Dust-to-Metal ratio
               importMetallicity='true',
               importTemperature='true',
               maxTemperature=30000, #[K]
               importVelocity_med='false',
               importMagneticField='false',
               importVariableMixParams='false',
               
               smoothing_kernel_med='cubic', 
               
               Dust_Type='themis',
               Dust_Env='MW',
               N_Si=8,
               N_C=8,
               N_PAH=8,
               add_pah=False,
               on_the_fly_dust=False,
               minSize=1e-7, #[cm]
               maxSize=1e-4,
               centroid_small=5e-7,
               centroid_large=1e-5,
               width_small=7.5e-1,
               width_large=7.5e-1,
    
               #!!! Sampling options
               numDensitySamples=100,
               numPropertySamples=1,
               aggregateVelocity='Average',
               
               #!!! Griding Strategy
               grid_unit='kpc',
               grid_minX=-30,
               grid_maxX=+30,
               grid_minY=-30,
               grid_maxY=+30,
               grid_minZ=-30,
               grid_maxZ=+30,
               
               Tree_Type='oct',
               Tree_Policy='density',
               
               minLevel=3,
               maxLevel=12,
               numExtraLevels=0,
               maxDustFraction=1e-6,
               maxDustOpticalDepth=0,
               grid_wv_test_unit='micron',
               grid_wv_test=0.55,
               maxDustDensityDispersion=0,
               maxElectronFraction=1e-6,
               maxGasFraction=1e-6,
               
               #!!! Instruments
               #@@@ default wvlength grid
               def_wv_grid='pre-defined',
               includeGALEX='true',
               includejohnson='true',
               includespitzer='true',
               includeSDSS='true',
               include2MASS='true',
               includeWISE='false',
               includeHERSCHEL='false',
               CustomFilterList=[],

               #@@@ instrument sys
               #@@@!!! general setting
               inst_dist_unit='Mpc',
               inst_dist=1000,
                
               inc_default=0,
               azm_default=0,
               roll_default=0,

               inc_min=0,
               inc_max=90,
               inc_del=10,
               
               azm_min=0,
               azm_max=0,
               azm_del=30,
               
               recordComponents='true',
               recordPolarization='false',
               recordStatistics='false',
               numScatteringLevels=0,
               
               #@@@!!! fullInstrument
               fov_unit='kpc',
               fov_X=60,
               fov_Y=60,
               
               pscale_X=0.05, #kpc
               pscale_Y=0.05,
               
               centre_X=0,
               centre_Y=0,

               #@@@!!! SEDInstrument
               inst_1d_sed_only=False,
               save_1d_sed=True,
               aperture_unit='kpc', 
               aperture_min=5, 
               aperture_max=20,
               aper_del=5,
               
               inst_sed_grid_type='log',
               inst_sed_grid_unit='micron',
               inst_sed_min_wv=0.1,
               inst_sed_max_wv=1000,
               inst_sed_N_wv=5000,
               inst_sed_grid_add_band=False,
               
               ### only activated when you choose nestedlog for the inst_sed_grid_type
               inst_sed_min_wv_sub = 0.4,
               inst_sed_max_wv_sub = 0.7,
               inst_sed_N_wv_sub = 3001,
    
               # If you want to save 2d array with a given wavelength grid, not with a pre-defined band-pass filter,
               # Turn 'inst_2d_sed_on' to True.
               inst_2d_sed_on=False,
               inst_2d_sed_unit='micron',
               inst_2d_sed_type = 'log',
               inst_2d_sed_min_wv = 0.09,
               inst_2d_sed_max_wv = 1000,
               inst_2d_sed_N_wv = 100,
    
               ### only activated when you choose 'nestedlog' for inst_2d_sed_type
               inst_2d_sed_min_wv_sub = 0.4,
               inst_2d_sed_max_wv_sub = 0.7,
               inst_2d_sed_N_wv_sub = 200,

               ### only activated when you choose 'file' for inst_2d_sed_type
               inst_2d_sed_repo='./',
               inst_2d_sed_fname='inst_2d_sed.txt',
               inst_2d_sed_relHW=0,
               visual = False,

               #!!! Basic Info
               repo='/home/jangjk/',
               opart_name='part_old.txt',
               ypart_name='part_young.txt',
               gas_name='gas_cell.txt',
               ski_name='nh_ext.ski',

                indent='    ',
                todsedMode='SFRNormalized',
                # Dust emission nested logarithmic wavelength grid
                dustem_grid_unit='micron',
                dustem_min_wv=1,
                dustem_max_wv=10000,
                dustem_N_wv=100,
                dustem_min_wv_sub=2,
                dustem_max_wv_sub=25,
                dustem_N_wv_sub=400,
                includeHeatingByCMB='true',
                maxFractionOfPrimary=0.01,
                maxFractionOfPrevious=0.03
                ):
    
    
    if add_young and SED_type_y.lower() == 'toddlers' and todsedMode == 'SFRNormalizedVariableDust':
        if tod_sedtemplate != 'BPASSChab100Bin':
            raise ValueError("SFRNormalizedVariableDust requires tod_sedtemplate='BPASSChab100Bin'")

    wfile = open(repo+ski_name,'w')

    N_idt = Base.Start(wfile=wfile,
                      N_phot=N_phot,
                      rnd_seed=rnd_seed,
                      wavelengthOutputStyle=wavelengthOutputStyle,
                      fluxOutputStyle=fluxOutputStyle,
                      z_red=z_red,
                      H_0=H_0,
                      Om_m=Om_m,
                      indent=indent,
                      indent_base=0,
                      mode=mode
                      )
    
    
    N_idt = Source.Source_System(wfile=wfile,
                                  source_unit=source_unit,
                                  wv_source_min=wv_source_min,
                                  wv_source_max=wv_source_max,
                                  wv_source_del=wv_source_del,
                                  source_bias=source_bias,
                                  bias_type=bias_type,
                                  bias_unit=bias_unit,
                                  wv_bias_min=wv_bias_min,
                                  wv_bias_max=wv_bias_max,
                                  import_velocity=import_velocity,
                                  import_dispersion=import_dispersion,
                                  source_weight=source_weight,
                                  bias_deg=bias_deg,
                                  old_fbase=repo,
                                  old_fname=opart_name,
                                  kernel_old=smoothing_kernel_o,
                                  sed_type_old=SED_type_o,
                                  sed_imf_old=SED_IMF_o,
                                  sed_res_old=SED_res_o,
                                  young_fbase=repo,
                                  young_fname=ypart_name,
                                  add_young=add_young,
                                  kernel_young=smoothing_kernel_y,
                                  sed_type_young=SED_type_y,
                                  sed_imf_young=SED_IMF_y,
                                  sed_res_young=SED_res_y,
                                  tod_sedtemplate=tod_sedtemplate,
                                  tod_includedust=tod_includedust,
                                  tod_sfrperiod=tod_sfrperiod,
                                  todsedMode=todsedMode,
                                  indent=indent,
                                  indent_base=N_idt
                                  )
    
    
    if mode in ['transparent','trans','nomedium','noext','no extinction','without extinction']:
        pass

    else:
        N_idt = Medium.Medium_System(wfile=wfile,
                                    forceScattering=forceScattering,
                                    minWeightReduction=minWeightReduction,
                                    minScattEvents=minScattEvents,
                                    pathLengthBias=pathLengthBias,
                                    dustEmissionOptions=dustEmissionOptions,
                                    dustemtype=dustemtype,
                                    includeHeatingByCMB=includeHeatingByCMB,
                                    maxFractionOfPrimary=maxFractionOfPrimary,
                                    maxFractionOfPrevious=maxFractionOfPrevious,
                                    dustem_grid_unit=dustem_grid_unit,
                                    dustem_min_wv=dustem_min_wv,
                                    dustem_max_wv=dustem_max_wv,
                                    dustem_N_wv=dustem_N_wv,
                                    dustem_min_wv_sub=dustem_min_wv_sub,
                                    dustem_max_wv_sub=dustem_max_wv_sub,
                                    dustem_N_wv_sub=dustem_N_wv_sub,
                                    storeRadiationField=storeRadiationField,
                                    radfield_type=radfield_type,
                                    radfield_unit=radfield_unit,
                                    radfield_min_wv=radfield_min_wv,
                                    radfield_max_wv=radfield_max_wv,
                                    radfield_N_wv=radfield_N_wv,
                                    gas_fbase=repo,
                                    gas_fname=gas_name,
                                    med_type=med_type,
                                    med_Mfrac=med_Mfrac,
                                    importMetallicity=importMetallicity,
                                    importTemperature=importTemperature,
                                    maxTemperature=maxTemperature,
                                    importVelocity=importVelocity_med,
                                    importMagneticField=importMagneticField,
                                    importVariableMixParams=importVariableMixParams,
                                    smoothing_kernel=smoothing_kernel_med,
                                    Dust_Type=Dust_Type,
                                    Dust_Env=Dust_Env,
                                    N_Si=N_Si,
                                    N_C=N_C,
                                    N_PAH=N_PAH,
                                    
                                    add_pah=add_pah,
                                    
                                    on_the_fly_dust=on_the_fly_dust,
                                    minSize=minSize,
                                    maxSize=maxSize,
                                    centroid_small=centroid_small,
                                    width_small=width_small,
                                    centroid_large=centroid_large,
                                    width_large=width_large,

                                    numDensitySamples=numDensitySamples,
                                    numPropertySamples=numPropertySamples,
                                    aggregateVelocity=aggregateVelocity,
                                    grid_unit=grid_unit,
                                    grid_minX=grid_minX,
                                    grid_maxX=grid_maxX,
                                    grid_minY=grid_minY,
                                    grid_maxY=grid_maxY,
                                    grid_minZ=grid_minZ,
                                    grid_maxZ=grid_maxZ,
                                    Tree_Type=Tree_Type,
                                    Tree_Policy=Tree_Policy,
                                    minLevel=minLevel,
                                    maxLevel=maxLevel,
                                    numExtraLevels=numExtraLevels,
                                    maxDustFraction=maxDustFraction,
                                    maxDustOpticalDepth=maxDustOpticalDepth,
                                    grid_wv_test_unit=grid_wv_test_unit,
                                    grid_wv_test=grid_wv_test,
                                    maxDustDensityDispersion=maxDustDensityDispersion,
                                    maxElectronFraction=maxElectronFraction,
                                    maxGasFraction=maxGasFraction,
                                    indent=indent,
                                    indent_base=N_idt
                                    )
               

    N_idt = Instrument.Inst_System(
                                   wfile=wfile,
                                   def_wv_grid=def_wv_grid,
                                   includeGALEX=includeGALEX,
                                   includejohnson=includejohnson,
                                   includespitzer=includespitzer,
                                   includeSDSS=includeSDSS,
                                   include2MASS=include2MASS,
                                   includeWISE=includeWISE,
                                   includeHERSCHEL=includeHERSCHEL,
                                   CustomFilterList=CustomFilterList,
                                   inst_dist_unit=inst_dist_unit,
                                   inst_dist=inst_dist,
                                   inc_default=inc_default,
                                   azm_default=azm_default,
                                   roll_default=roll_default,
                                   inc_min=inc_min,
                                   inc_max=inc_max,
                                   inc_del=inc_del,
                                   azm_min=azm_min,
                                   azm_max=azm_max,
                                   azm_del=azm_del,
                                   recordComponents=recordComponents,
                                   recordPolarization=recordPolarization,
                                   recordStatistics=recordStatistics,
                                   numScatteringLevels=numScatteringLevels,
                                   fov_unit=fov_unit,
                                   fov_X=fov_X,
                                   fov_Y=fov_Y,
                                   pscale_X=pscale_X, 
                                   pscale_Y=pscale_Y,
                                   centre_X=centre_X,
                                   centre_Y=centre_Y,
                                   save_1d_sed=save_1d_sed,
                                   aperture_unit=aperture_unit, 
                                   aperture_min=aperture_min, 
                                   aperture_max=aperture_max,
                                   aper_del=aper_del,
                                   inst_sed_grid_type=inst_sed_grid_type,
                                   inst_sed_grid_unit=inst_sed_grid_unit,
                                   inst_sed_min_wv=inst_sed_min_wv,
                                   inst_sed_max_wv=inst_sed_max_wv,
                                   inst_sed_N_wv=inst_sed_N_wv,
                                   inst_sed_min_wv_sub = inst_sed_min_wv_sub,
                                   inst_sed_max_wv_sub = inst_sed_max_wv_sub,
                                   inst_sed_N_wv_sub = inst_sed_N_wv_sub,

                                   inst_2d_sed_on=inst_2d_sed_on,
                                   inst_2d_sed_unit=inst_2d_sed_unit,
                                   inst_2d_sed_type = inst_2d_sed_type,
                                   inst_2d_sed_min_wv = inst_2d_sed_min_wv,
                                   inst_2d_sed_max_wv = inst_2d_sed_max_wv,
                                   inst_2d_sed_N_wv = inst_2d_sed_N_wv,
                                   inst_2d_sed_min_wv_sub = inst_2d_sed_min_wv_sub,
                                   inst_2d_sed_max_wv_sub = inst_2d_sed_max_wv_sub,
                                   inst_2d_sed_N_wv_sub = inst_2d_sed_N_wv_sub,
                                   inst_2d_sed_repo=inst_2d_sed_repo,
                                   inst_2d_sed_fname=inst_2d_sed_fname,
                                   inst_2d_sed_relHW=inst_2d_sed_relHW,
                                   visual = visual,
                                   indent=indent,
                                   indent_base=N_idt
                                    )


    N_idt = Probe.Probe_System(
                                wfile=wfile,
                               indent=indent,
                               indent_base=N_idt
                              )

    Base.End(
             wfile=wfile,
             indent=indent,
             indent_base=N_idt
             )
    
    
    wfile.close()
    return

#writing_ski()















































