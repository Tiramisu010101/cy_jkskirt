import numpy as np
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def Probe_System(
                wfile,
                indent,
                indent_base
                ):
    
    #!!! Probe system will be updated soon
    
    N_idt = indent_base
    
    print((N_idt)*indent+'<probeSystem type="ProbeSystem">',file=wfile)
    print((N_idt+1)*indent+'<ProbeSystem>',file=wfile)
    print((N_idt+2)*indent+'<probes type="Probe">',file=wfile)
    # print((N_idt+3)*indent+'<ConvergenceCutsProbe probeName="dns" probeAfter="Setup"/>',file=wfile)
    # print((N_idt+3)*indent+'<DensityProbe probeName="intsdens" aggregation="Type" probeAfter="Setup">',file=wfile)
    # print((N_idt+4)*indent+'<form type="Form">',file=wfile)
    # print((N_idt+5)*indent+'<PlanarCutsForm  minX="-1e4 pc" maxX="1e4 pc" minY="-1e4 pc" maxY="1e4 pc" minZ="-1e4 pc" maxZ="1e4 pc" positionX="0 pc" positionY="0 pc" positionZ="0 pc" numPixelsX="500" numPixelsY="500" numPixelsZ="500"/>',file=wfile)
    # print((N_idt+4)*indent+'</form>',file=wfile)
    # print((N_idt+3)*indent+'</DensityProbe>',file=wfile)
    # print((N_idt+3)*indent+'<ImportedMediumDensityProbe probeName="dustdns">',file=wfile)
    # print((N_idt+4)*indent+'<form type="GenericForm">',file=wfile)
    # print((N_idt+5)*indent+'<PlanarCutsForm minX="-2e4 pc" maxX="2e4 pc" minY="-2e4 pc" maxY="2e4 pc" minZ="-2e4 pc" maxZ="2e4 pc" positionX="0 pc" positionY="0 pc" positionZ="0 pc" numPixelsX="50" numPixelsY="50" numPixelsZ="50"/>', file= wfile)
    # print((N_idt+4)*indent+'</form>', file=wfile)
    # print((N_idt+3)*indent+'</ImportedMediumDensityProbe>',file=wfile)
    # print((N_idt+3)*indent+'<TemperatureProbe probeName="tmp" aggregation="Type" probeAfter="Run">',file=wfile)
    # print((N_idt+4)*indent+'<form type="Form">',file=wfile)
    # print((N_idt+5)*indent+'<DefaultCutsForm/>',file=wfile)
    # print((N_idt+4)*indent+'</form>',file=wfile)
    # print((N_idt+3)*indent+'</TemperatureProbe>',file=wfile)
    print((N_idt+2)*indent+'</probes>',file=wfile)
    print((N_idt+1)*indent+'</ProbeSystem>',file=wfile)
    print((N_idt)*indent+'</probeSystem>',file=wfile)
    
    return N_idt
    
    
