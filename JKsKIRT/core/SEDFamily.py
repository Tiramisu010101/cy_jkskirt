import numpy as np
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# SED Family
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def BlackBody(wfile,
              indent,
              indent_base
              ):
    
    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<BlackBodySEDFamily/>',file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def CastelliKrucz(wfile,
                  indent,
                  indent_base
                  ):

    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<CastelliKuruczSEDFamily/>',file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def Maraston(wfile,
             imf,
             indent,
             indent_base
             ):

    N_idt = indent_base
    
    if imf == 'kroupa':
        imf = 'Kroupa'
    elif imf == 'salpeter':
        imf = 'Salpeter'

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<MarastonSEDFamily imf="%s"/>'%(imf),file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def BC03(wfile,
         imf,
         resolution,
         indent,
         indent_base
         ):
    
    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<BruzualCharlotSEDFamily imf="%s" resolution="%s"/>'%(imf,resolution),file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def Starburst99(wfile,
                indent,
                indent_base
                ):
    
    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<Starburst99SEDFamily/>',file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def FSPS(wfile,
         imf,
         indent,
         indent_base
         ):

    N_idt = indent_base
    
    if imf == 'kroupa':
        imf = 'Kroupa'
    elif imf == 'salpeter':
        imf = 'Salpeter'
    elif imf == 'chabrier':
        imf = 'Chabrier'

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<FSPSSEDFamily imf="%s"/>'%(imf),file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def Bpass(wfile,
          imf,
          resolution,
          indent,
          indent_base
          ):
    
    N_idt = indent_base
    if imf == 'Chabrier':
        imf = 'Chabrier300'
    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<BpassSEDFamily imf="%s" resolution="%s"/>'%(imf,resolution),file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def MappingsIII(wfile,
                indent,
                indent_base
                ):
    
    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<MappingsSEDFamily/>',file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def LyaGaussian(wfile,
                  indent,
                  indent_base
                  ):

    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<LyaGaussianSEDFamily/>',file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt


def LyaDoublePeak(wfile,
                  indent,
                  indent_base
                  ):

    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<LyaDoublePeakedSEDFamily/>',file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    
    return N_idt

def Toddlers(wfile,
             indent,
             indent_base,
             stellartemplate,
             includedust,
             resolution,
             sfrperiod,
             todsedMode='SFRNormalized'
             ):
    
    # if pahfraction == 'high':
    #     pahfraction = 'High'
    # if pahfraction == 'low':
    #     pahfraction = 'Low'
    # if resolution == 'high':
    #     resolution = 'High'
    # if resolution == 'low':
    #     resolution = 'Low'

    N_idt = indent_base

    print((N_idt)*indent+'<sedFamily type="SEDFamily">',file=wfile)
    print((N_idt+1)*indent+'<ToddlersSEDFamily sedMode="%s" stellarTemplate="%s" includeDust="%s" resolution="%s" sfrPeriod="%s"/>'%(todsedMode,stellartemplate,includedust,resolution,sfrperiod),file=wfile)
    print((N_idt)*indent+'</sedFamily>',file=wfile)
    return N_idt





def ToddlersCustomCloud(wfile, indent, indent_base, includedust='true',
                       resolution='Low', table_directory=None):
    """Select one custom cloud table; write the filename-based C++ reader."""
    from pathlib import PurePosixPath
    from xml.sax.saxutils import quoteattr
    if table_directory is None:
        table_directory = '/home/yuchang/SKIRT/resources/SKIRT9_Resources_TODDLERS_VariableDust/SED_TODDLERS_Custom'
    dust = str(includedust).lower()
    resolutions = {'low': 'lr', 'high': 'hr', 'lr': 'lr', 'hr': 'hr'}
    if dust not in ('true', 'false'):
        raise ValueError('tod_includedust must be true or false')
    if str(resolution).lower() not in resolutions:
        raise ValueError('Custom cloud resolution must be Low/High or lr/hr')
    name = 'ToddlersCloudCustom_BPASS_chab100_bin_{}_{}.stab'.format(
        'Dust' if dust == 'true' else 'noDust', resolutions[str(resolution).lower()])
    filename = str(PurePosixPath(table_directory) / name)
    print(indent_base * indent + '<sedFamily type="SEDFamily">', file=wfile)
    print((indent_base + 1) * indent + '<ToddlersCustomCloudSEDFamily filename=' +
          quoteattr(filename) + '/>', file=wfile)
    print(indent_base * indent + '</sedFamily>', file=wfile)
    return indent_base
