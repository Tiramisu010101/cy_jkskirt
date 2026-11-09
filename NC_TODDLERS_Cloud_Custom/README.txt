TODDLERS custom age-dependent Cloud tables

BPASS chab100 binary; fixed n_cl=300 H/cm3, M_cl=10^6.5 Msun, SFE=0.045, q_PAH=0.
Each table contains 1,440 spectra: 20 ages x 6 Z x 4 f_dust x 3 r_sl.
StoredTable<5> axes: lambda(m),time(Myr),Z(1),f_dust(1),r_sl(1)
Quantity: Llambda(W/m). The source is an individual cloud, with no SFR averaging.
Use ages from 0.1 to 10 Myr. No physical extrapolation is supplied.

The four files are valid SKIRT StoredTables. The stock ToddlersSEDFamily Cloud reader
expects six other axes and cannot load these five-axis files directly.
See manifest.json for grid values, units, checksums, and the stellar input interpolation.
