import numpy as np

from . import Base
from . import MaterialMix
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Medium System
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def Medium_System(wfile,
                  
                  forceScattering,
                  minWeightReduction,
                  minScattEvents,
                  pathLengthBias,
                  
                  storeRadiationField,
                  radfield_type,
                  radfield_unit,
                  radfield_min_wv,
                  radfield_max_wv,
                  radfield_N_wv,
                  
                  dustEmissionOptions,
                  dustemtype,
                  gas_fbase,
                  gas_fname,
                  
                  med_type,
                  med_Mfrac,
                  importMetallicity,
                  importTemperature,
                  maxTemperature,
                  importVelocity,
                  importMagneticField,
                  importVariableMixParams,
                  smoothing_kernel,
                  
                  Dust_Type,
                  Dust_Env,
                  N_Si,
                  N_C,
                  N_PAH,
                  add_pah,
                  
                  on_the_fly_dust,
                  minSize,
                  maxSize,
                  centroid_small,
                  width_small,
                  centroid_large,
                  width_large,
                  
                  numDensitySamples,
                  numPropertySamples,
                  aggregateVelocity,

                  grid_unit,
                  grid_minX,
                  grid_maxX,
                  grid_minY,
                  grid_maxY,
                  grid_minZ,
                  grid_maxZ,
               
                  Tree_Type,
                  Tree_Policy,
                  minLevel,
                  maxLevel,
                  numExtraLevels,
                  maxDustFraction,
                  maxDustOpticalDepth,
                  grid_wv_test_unit,
                  grid_wv_test,
                  maxDustDensityDispersion,
                  maxElectronFraction,
                  maxGasFraction,

                  indent,
                  indent_base
                  ):
    
    N_idt = indent_base
    
    print((N_idt)*indent+'<mediumSystem type="MediumSystem">',file=wfile)
    print((N_idt+1)*indent+'<MediumSystem>',file=wfile)
    print((N_idt+2)*indent+'<photonPacketOptions type="PhotonPacketOptions">',file=wfile)
    print((N_idt+3)*indent+'<PhotonPacketOptions forceScattering="%s" minWeightReduction="%s" minScattEvents="%s" pathLengthBias="%s"/>'%(forceScattering,minWeightReduction,minScattEvents,pathLengthBias),file=wfile)
    print((N_idt+2)*indent+'</photonPacketOptions>',file=wfile)
    print((N_idt+2)*indent+'<radiationFieldOptions type="RadiationFieldOptions">',file=wfile)
    print((N_idt+3)*indent+'<RadiationFieldOptions storeRadiationField="%s">'%(storeRadiationField),file=wfile)
    
    if storeRadiationField == 'true':
        print((N_idt+4)*indent+'<radiationFieldWLG type="DisjointWavelengthGrid">',file=wfile)
        
        if radfield_type =='log':
            print((N_idt+5)*indent+'<LogWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(radfield_min_wv,radfield_unit,radfield_max_wv,radfield_unit,radfield_N_wv),file=wfile)
        elif radfield_type =='lin':
            print((N_idt+5)*indent+'<LinWavelengthGrid minWavelength="%s %s" maxWavelength="%s %s" numWavelengths="%s"/>'%(radfield_min_wv,radfield_unit,radfield_max_wv,radfield_unit,radfield_N_wv),file=wfile)
        
        print((N_idt+4)*indent+'</radiationFieldWLG>',file=wfile)


    print((N_idt+3)*indent+'</RadiationFieldOptions>',file=wfile)
    print((N_idt+2)*indent+'</radiationFieldOptions>',file=wfile)    
    
    if dustEmissionOptions == 'true':
        print((N_idt+2)*indent+'<secondaryEmissionOptions type="SecondaryEmissionOptions">',file=wfile)
        print((N_idt+3)*indent+'<SecondaryEmissionOptions storeEmissionRadiationField="false" secondaryPacketsMultiplier="1" spatialBias="0.5" sourceBias="0.5"/>',file=wfile)
        print((N_idt+2)*indent+'</secondaryEmissionOptions>',file=wfile)
        print((N_idt+2)*indent+'<dustEmissionOptions type="DustEmissionOptions">',file=wfile)
        print((N_idt+3)*indent+'<DustEmissionOptions dustEmissionType="%s" includeHeatingByCMB="true" maxFractionOfPrimary="0.01" maxFractionOfPrevious="0.03" sourceWeight="1" wavelengthBias="0.5">'%(dustemtype),file=wfile)
        print((N_idt+4)*indent+'<cellLibrary type="SpatialCellLibrary">',file=wfile)
        print((N_idt+5)*indent+'<AllCellsLibrary/>',file=wfile)
        print((N_idt+4)*indent+'</cellLibrary>',file=wfile)
        print((N_idt+4)*indent+'<dustEmissionWLG type="DisjointWavelengthGrid">',file=wfile)
        # print((N_idt+5)*indent+'<LogWavelengthGrid minWavelength="1 micron" maxWavelength="2000 micron" numWavelengths="1000"/>',file=wfile)
        print((N_idt+5)*indent+'<NestedLogWavelengthGrid minWavelengthBaseGrid="1 micron" maxWavelengthBaseGrid="2000 micron" numWavelengthsBaseGrid="100" minWavelengthSubGrid="2 micron" maxWavelengthSubGrid="25 micron" numWavelengthsSubGrid="400"/>',file=wfile)
        print((N_idt+4)*indent+'</dustEmissionWLG>',file=wfile)
        print((N_idt+4)*indent+'<wavelengthBiasDistribution type="WavelengthDistribution">',file=wfile)
        print((N_idt+5)*indent+'<DefaultWavelengthDistribution/>',file=wfile)
        print((N_idt+4)*indent+'</wavelengthBiasDistribution>',file=wfile)
        print((N_idt+3)*indent+'</DustEmissionOptions>',file=wfile)
        print((N_idt+2)*indent+'</dustEmissionOptions>',file=wfile)

    print((N_idt+2)*indent+'<media type="Medium">',file=wfile)

    if med_type == 'particle':
        print((N_idt+3)*indent+'<ParticleMedium filename="%s/%s" massFraction="%s" importMetallicity="%s" importTemperature="%s" maxTemperature="%s K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="">'%(gas_fbase,gas_fname,med_Mfrac,importMetallicity,importTemperature,maxTemperature,importVelocity,importMagneticField,importVariableMixParams),file=wfile)
        
        dummy = Base.Smoothing_Kernel(wfile=wfile,
                                  smoothing_type=smoothing_kernel,
                                  indent=indent,
                                  indent_base=N_idt+4)
    
        dummy = MaterialMix.MatMix(wfile=wfile,
                               Dust_Type=Dust_Type,
                               Dust_Env=Dust_Env,
                               N_Si=N_Si,
                               N_C=N_C,
                               N_PAH=N_PAH,
                               indent=indent,
                               indent_base=N_idt+4)

        print((N_idt+3)*indent+'</ParticleMedium>',file=wfile)

    elif med_type == 'cell':
        if on_the_fly_dust in [False,'false']:
            print((N_idt+3)*indent+'<CellMedium filename="%s/%s" massFraction="%s" importMetallicity="%s" importTemperature="%s" maxTemperature="%s K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="x-min,y-min,z-min,x-max,y-max,z-max,mass volume density,metallicity,temperature">'%(gas_fbase,gas_fname,med_Mfrac,importMetallicity,importTemperature,maxTemperature,importVelocity,importMagneticField,importVariableMixParams),file=wfile)

            dummy = MaterialMix.MatMix(wfile=wfile,
                                   Dust_Type=Dust_Type,
                                   Dust_Env=Dust_Env,
                                   N_Si=N_Si,
                                   N_C=N_C,
                                   N_PAH=N_PAH,
                                   indent=indent,
                                   indent_base=N_idt+4)

            print((N_idt+3)*indent+'</CellMedium>',file=wfile)
        else:
            print((N_idt+3)*indent+'<CellMedium filename="%s/%s" massType="MassDensity" massFraction="1" importMetallicity="false" importTemperature="false" maxTemperature="0 K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="x-min,y-min,z-min,x-max,y-max,z-max,small carbonaceous density">'%(gas_fbase,gas_fname,importVelocity,importMagneticField,importVariableMixParams),file=wfile)
            print((N_idt+4)*indent+'<materialMix type="MaterialMix">',file=wfile)
            print((N_idt+5)*indent+'<ConfigurableDustMix scatteringType="HenyeyGreenstein">',file=wfile)
            print((N_idt+6)*indent+'<populations type="GrainPopulation">',file=wfile)
            print((N_idt+7)*indent+'<GrainPopulation numSizes="%s" normalizationType="FactorOnSizeDistribution" factorOnSizeDistribution="1">'%(N_C),file=wfile)
            print((N_idt+8)*indent+'<composition type="GrainComposition">',file=wfile)
            print((N_idt+9)*indent+'<DraineGraphiteGrainComposition/>',file=wfile)
            print((N_idt+8)*indent+'</composition>',file=wfile)
            print((N_idt+8)*indent+'<sizeDistribution type="GrainSizeDistribution">',file=wfile)
            print((N_idt+9)*indent+'<LogNormalGrainSizeDistribution minSize="%s cm" maxSize="%s cm" centroid="%s cm" width="%s"/>'%(minSize,maxSize,centroid_small,width_small),file=wfile)
            print((N_idt+8)*indent+'</sizeDistribution>',file=wfile)
            print((N_idt+7)*indent+'</GrainPopulation>',file=wfile)
            print((N_idt+6)*indent+'</populations>',file=wfile)
            print((N_idt+5)*indent+'</ConfigurableDustMix>',file=wfile)
            print((N_idt+4)*indent+'</materialMix>',file=wfile) 
            print((N_idt+3)*indent+'</CellMedium>',file=wfile)
        
            print((N_idt+3)*indent+'<CellMedium filename="%s/%s" massType="MassDensity" massFraction="1" importMetallicity="false" importTemperature="false" maxTemperature="0 K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="x-min,y-min,z-min,x-max,y-max,z-max,large carbonaceous density">'%(gas_fbase,gas_fname,importVelocity,importMagneticField,importVariableMixParams),file=wfile)
            print((N_idt+4)*indent+'<materialMix type="MaterialMix">',file=wfile)
            print((N_idt+5)*indent+'<ConfigurableDustMix scatteringType="HenyeyGreenstein">',file=wfile)
            print((N_idt+6)*indent+'<populations type="GrainPopulation">',file=wfile)
            print((N_idt+7)*indent+'<GrainPopulation numSizes="%s" normalizationType="FactorOnSizeDistribution" factorOnSizeDistribution="1">'%(N_C),file=wfile)
            print((N_idt+8)*indent+'<composition type="GrainComposition">',file=wfile)
            print((N_idt+9)*indent+'<DraineGraphiteGrainComposition/>',file=wfile)
            print((N_idt+8)*indent+'</composition>',file=wfile)
            print((N_idt+8)*indent+'<sizeDistribution type="GrainSizeDistribution">',file=wfile)
            print((N_idt+9)*indent+'<LogNormalGrainSizeDistribution minSize="%s cm" maxSize="%s cm" centroid="%s cm" width="%s"/>'%(minSize,maxSize,centroid_large,width_large),file=wfile)
            print((N_idt+8)*indent+'</sizeDistribution>',file=wfile)
            print((N_idt+7)*indent+'</GrainPopulation>',file=wfile)
            print((N_idt+6)*indent+'</populations>',file=wfile)
            print((N_idt+5)*indent+'</ConfigurableDustMix>',file=wfile)
            print((N_idt+4)*indent+'</materialMix>',file=wfile) 
            print((N_idt+3)*indent+'</CellMedium>',file=wfile)
            
            print((N_idt+3)*indent+'<CellMedium filename="%s/%s" massType="MassDensity" massFraction="1" importMetallicity="false" importTemperature="false" maxTemperature="0 K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="x-min,y-min,z-min,x-max,y-max,z-max,small silicates density">'%(gas_fbase,gas_fname,importVelocity,importMagneticField,importVariableMixParams),file=wfile)
            print((N_idt+4)*indent+'<materialMix type="MaterialMix">',file=wfile)
            print((N_idt+5)*indent+'<ConfigurableDustMix scatteringType="HenyeyGreenstein">',file=wfile)
            print((N_idt+6)*indent+'<populations type="GrainPopulation">',file=wfile)
            print((N_idt+7)*indent+'<GrainPopulation numSizes="%s" normalizationType="FactorOnSizeDistribution" factorOnSizeDistribution="1">'%(N_C),file=wfile)
            print((N_idt+8)*indent+'<composition type="GrainComposition">',file=wfile)
            print((N_idt+9)*indent+'<DraineSilicateGrainComposition/>',file=wfile)
            print((N_idt+8)*indent+'</composition>',file=wfile)
            print((N_idt+8)*indent+'<sizeDistribution type="GrainSizeDistribution">',file=wfile)
            print((N_idt+9)*indent+'<LogNormalGrainSizeDistribution minSize="%s cm" maxSize="%s cm" centroid="%s cm" width="%s"/>'%(minSize,maxSize,centroid_small,width_small),file=wfile)
            print((N_idt+8)*indent+'</sizeDistribution>',file=wfile)
            print((N_idt+7)*indent+'</GrainPopulation>',file=wfile)
            print((N_idt+6)*indent+'</populations>',file=wfile)
            print((N_idt+5)*indent+'</ConfigurableDustMix>',file=wfile)
            print((N_idt+4)*indent+'</materialMix>',file=wfile) 
            print((N_idt+3)*indent+'</CellMedium>',file=wfile)
        
            print((N_idt+3)*indent+'<CellMedium filename="%s/%s" massType="MassDensity" massFraction="1" importMetallicity="false" importTemperature="false" maxTemperature="0 K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="x-min,y-min,z-min,x-max,y-max,z-max,large silicates density">'%(gas_fbase,gas_fname,importVelocity,importMagneticField,importVariableMixParams),file=wfile)
            print((N_idt+4)*indent+'<materialMix type="MaterialMix">',file=wfile)
            print((N_idt+5)*indent+'<ConfigurableDustMix scatteringType="HenyeyGreenstein">',file=wfile)
            print((N_idt+6)*indent+'<populations type="GrainPopulation">',file=wfile)
            print((N_idt+7)*indent+'<GrainPopulation numSizes="%s" normalizationType="FactorOnSizeDistribution" factorOnSizeDistribution="1">'%(N_C),file=wfile)
            print((N_idt+8)*indent+'<composition type="GrainComposition">',file=wfile)
            print((N_idt+9)*indent+'<DraineSilicateGrainComposition/>',file=wfile)
            print((N_idt+8)*indent+'</composition>',file=wfile)
            print((N_idt+8)*indent+'<sizeDistribution type="GrainSizeDistribution">',file=wfile)
            print((N_idt+9)*indent+'<LogNormalGrainSizeDistribution minSize="%s cm" maxSize="%s cm" centroid="%s cm" width="%s"/>'%(minSize,maxSize,centroid_large,width_large),file=wfile)
            print((N_idt+8)*indent+'</sizeDistribution>',file=wfile)
            print((N_idt+7)*indent+'</GrainPopulation>',file=wfile)
            print((N_idt+6)*indent+'</populations>',file=wfile)
            print((N_idt+5)*indent+'</ConfigurableDustMix>',file=wfile)
            print((N_idt+4)*indent+'</materialMix>',file=wfile) 
            print((N_idt+3)*indent+'</CellMedium>',file=wfile)
            
            if add_pah == True:
                print((N_idt+3)*indent+'<CellMedium filename="%s/%s" massType="MassDensity" massFraction="1" importMetallicity="false" importTemperature="false" maxTemperature="0 K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="x-min,y-min,z-min,x-max,y-max,z-max,pah neutral density">'%(gas_fbase,gas_fname,importVelocity,importMagneticField,importVariableMixParams),file=wfile)
                print((N_idt+4)*indent+'<materialMix type="MaterialMix">',file=wfile)
                print((N_idt+5)*indent+'<ConfigurableDustMix scatteringType="HenyeyGreenstein">',file=wfile)
                print((N_idt+6)*indent+'<populations type="GrainPopulation">',file=wfile)
                print((N_idt+7)*indent+'<GrainPopulation numSizes="%s" normalizationType="FactorOnSizeDistribution" factorOnSizeDistribution="1">'%(N_PAH),file=wfile)
                print((N_idt+8)*indent+'<composition type="GrainComposition">',file=wfile)
                print((N_idt+9)*indent+'<DraineNeutralPAHGrainComposition/>',file=wfile)
                print((N_idt+8)*indent+'</composition>',file=wfile)
                print((N_idt+8)*indent+'<sizeDistribution type="GrainSizeDistribution">',file=wfile)
                print((N_idt+9)*indent+'<ZubkoPAHGrainSizeDistribution/>',file=wfile)
                print((N_idt+8)*indent+'</sizeDistribution>',file=wfile)
                print((N_idt+7)*indent+'</GrainPopulation>',file=wfile)
                print((N_idt+6)*indent+'</populations>',file=wfile)
                print((N_idt+5)*indent+'</ConfigurableDustMix>',file=wfile)
                print((N_idt+4)*indent+'</materialMix>',file=wfile) 
                print((N_idt+3)*indent+'</CellMedium>',file=wfile)

                print((N_idt+3)*indent+'<CellMedium filename="%s/%s" massType="MassDensity" massFraction="1" importMetallicity="false" importTemperature="false" maxTemperature="0 K" importVelocity="%s" importMagneticField="%s" importVariableMixParams="%s" useColumns="x-min,y-min,z-min,x-max,y-max,z-max,pah ionized density">'%(gas_fbase,gas_fname,importVelocity,importMagneticField,importVariableMixParams),file=wfile)
                print((N_idt+4)*indent+'<materialMix type="MaterialMix">',file=wfile)
                print((N_idt+5)*indent+'<ConfigurableDustMix scatteringType="HenyeyGreenstein">',file=wfile)
                print((N_idt+6)*indent+'<populations type="GrainPopulation">',file=wfile)
                print((N_idt+7)*indent+'<GrainPopulation numSizes="%s" normalizationType="FactorOnSizeDistribution" factorOnSizeDistribution="1">'%(N_PAH),file=wfile)
                print((N_idt+8)*indent+'<composition type="GrainComposition">',file=wfile)
                print((N_idt+9)*indent+'<DraineIonizedPAHGrainComposition/>',file=wfile)
                print((N_idt+8)*indent+'</composition>',file=wfile)
                print((N_idt+8)*indent+'<sizeDistribution type="GrainSizeDistribution">',file=wfile)
                print((N_idt+9)*indent+'<ZubkoPAHGrainSizeDistribution/>',file=wfile)
                print((N_idt+8)*indent+'</sizeDistribution>',file=wfile)
                print((N_idt+7)*indent+'</GrainPopulation>',file=wfile)
                print((N_idt+6)*indent+'</populations>',file=wfile)
                print((N_idt+5)*indent+'</ConfigurableDustMix>',file=wfile)
                print((N_idt+4)*indent+'</materialMix>',file=wfile) 
                print((N_idt+3)*indent+'</CellMedium>',file=wfile)




                  
    print((N_idt+2)*indent+'</media>',file=wfile)

    if med_type in ['particle','cell']:
        print((N_idt+2)*indent+'<samplingOptions type="SamplingOptions">',file=wfile)
        print((N_idt+3)*indent+'<SamplingOptions numDensitySamples="%s" numPropertySamples="%s" aggregateVelocity="%s"/>'%(numDensitySamples,numPropertySamples,aggregateVelocity),file=wfile)
        print((N_idt+2)*indent+'</samplingOptions>',file=wfile)
        
        print((N_idt+2)*indent+'<grid type="SpatialGrid">',file=wfile)
        if Tree_Type == 'oct':
            print((N_idt+3)*indent+'<PolicyTreeSpatialGrid minX="%s %s" maxX="%s %s" minY="%s %s" maxY="%s %s" minZ="%s %s" maxZ="%s %s" treeType="OctTree">'%(grid_minX, grid_unit, grid_maxX, grid_unit, grid_minY, grid_unit, grid_maxY, grid_unit, grid_minZ, grid_unit, grid_maxZ, grid_unit),file=wfile)

            print((N_idt+4)*indent+'<policy type="TreePolicy">',file=wfile)
            if Tree_Policy == 'density':
                print((N_idt+5)*indent+'<DensityTreePolicy minLevel="%s" maxLevel="%s" maxDustFraction="%s" maxDustOpticalDepth="%s" wavelength="%s %s" maxDustDensityDispersion="%s" maxElectronFraction="%s" maxGasFraction="%s"/>'%(minLevel,maxLevel,maxDustFraction,maxDustOpticalDepth,grid_wv_test,grid_wv_test_unit,maxDustDensityDispersion,maxElectronFraction,maxGasFraction),file=wfile)
            elif Tree_Policy == 'site':
                print((N_idt+5)*indent+'<SiteListTreePolicy minLevel="%s" maxLevel="%s" numExtraLevels="%s"/>'%(minLevel,maxLevel,numExtraLevels),file=wfile)
            print((N_idt+4)*indent+'</policy>',file=wfile)
            print((N_idt+3)*indent+'</PolicyTreeSpatialGrid>',file=wfile)
            
            
        print((N_idt+2)*indent+'</grid>',file=wfile)
        
        
    print((N_idt+1)*indent+'</MediumSystem>',file=wfile)
    print((N_idt)*indent+'</mediumSystem>',file=wfile)   
    
    return N_idt
        
        
        
        
        
