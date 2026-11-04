## new version JKskirt

import os
import sys
from pathlib import Path
from importlib import reload

import numpy as np
import pandas as pd


def fibonacci_los(n_los):
    """Return unit directions and (inclination, azimuth) pairs in degrees."""
    if isinstance(n_los, bool) or not isinstance(n_los, (int, np.integer)) or n_los < 1:
        raise ValueError('n_los must be a positive integer')
    i = np.arange(n_los)
    z = 1 - 2 * (i + 0.5) / n_los
    phi = (i * np.pi * (3 - np.sqrt(5))) % (2 * np.pi)
    r = np.sqrt(1 - z**2)
    directions = np.column_stack((r * np.cos(phi), r * np.sin(phi), z))
    angles = np.column_stack((np.degrees(np.arccos(z)), np.degrees(phi)))
    return directions, angles


def choose_start_index(targets, output_base):
    """Select a start position in the ordered (nout, id, R90) target list."""
    if not targets:
        print('No galaxies to process.')
        return None

    has_sed = []
    print('\nOrder  Snapshot  Galaxy ID  Existing output (file presence is not completion)')
    for order, (nout, galaxy_id, _) in enumerate(targets, start=1):
        folder = Path(output_base) / f'gal_{nout:04d}' / f'{galaxy_id:04d}'
        sed_files = [p for p in folder.glob('*_sed.dat')
                     if p.is_file() and p.stat().st_size > 0]
        has_sed.append(bool(sed_files))
        status = (f'{len(sed_files)} nonempty SED file(s)' if sed_files else
                  'folder exists, no nonempty SED file' if folder.is_dir() else
                  'no output folder')
        print(f'{order:5d}  {nout:8d}  {galaxy_id:9d}  {status}')

    prefix = 0
    for exists in has_sed:
        if not exists:
            break
        prefix += 1
    print(f'\nSED files exist consecutively for the first {prefix} galaxies.')
    if prefix < len(targets):
        print(f'First order without an SED file: {prefix + 1} (nout {targets[prefix][0]}, ID {targets[prefix][1]})')
    else:
        print('All listed galaxies have SED files. Select an order only to rerun.')

    while True:
        answer = input(f'Start from which order [1-{len(targets)}]? (q/Enter: cancel): ').strip()
        if not answer or answer.lower() == 'q':
            return None
        try:
            order = int(answer)
        except ValueError:
            print('Enter an order number, not a galaxy ID.')
            continue
        if not 1 <= order <= len(targets):
            print('Order is outside the listed range.')
            continue
        start = order - 1
        print(f'Will run {len(targets) - start} galaxies, starting at order {order}, nout {targets[start][0]}, ID {targets[start][1]}.')
        if any(has_sed[start:]):
            print('This selection includes existing SED outputs; matching output files may be overwritten.')
        if input('Run this sequence? [y/N]: ').strip().lower() == 'y':
            return start
        return None


if __name__=="__main__":
    
    GFE_DIR = '/home/yuchang/JKsKIRT/'
    sys.path.append(GFE_DIR)
    import JKsKIRT as gskirt

    from rur import uri, uhmi

    SioverSil = 0.163 
    boxrad = 10
    n_los = 20  # Number of Fibonacci-sphere sightlines; shared by all galaxies.
    los_vectors, los_angles = fibonacci_los(n_los)

    # Resolve the CSV before SKIRT changes the working directory.
    csv_path = Path('/home/yuchang/Attenuation/galaxy_properties_15.csv')
    df = pd.read_csv(csv_path, index_col=['nout', 'id'])

    nout_arr = [78, 50, 36]

    if not df.index.is_unique:
        raise ValueError('CSV contains duplicate (nout, id) pairs')
    
    targets = []
    for nout in nout_arr:
        for galaxy_id, row in df.loc[nout].iterrows():
            r90 = float(row['R90'])
            targets.append((int(nout), int(galaxy_id), r90))

    repo = '/storage8/NCdustfix/NCdustfix2/'
    path_in_repo = 'snapshots'
    mode = 'nc'

    
    output_base = Path('/storage1/yuchang/Attenuation15')
    start_index = choose_start_index(targets, output_base)
    if start_index is None:
        print('Cancelled; no SKIRT runs started.')
        sys.exit(0)

    loaded_nout = None
    galaxy_by_id = {}
    for order in range(start_index, len(targets)):
        nout, id, R90 = targets[order]
        if nout != loaded_nout:
            catalogue_snap = uri.RamsesSnapshot(
                repo=repo, path_in_repo=path_in_repo, iout=nout,
                mode=mode, longint=False)
            try:
                gals_tot, pid = uhmi.HaloMaker.load(
                    catalogue_snap, galaxy=True, load_parts=True,
                    double_precision=True, extend=True)
                galaxy_by_id = {int(gal['id']): gal.copy() for gal in gals_tot}
            finally:
                catalogue_snap.clear()
            missing_ids = [galaxy_id for target_nout, galaxy_id, _ in targets[order:]
                           if target_nout == nout and galaxy_id not in galaxy_by_id]
            if missing_ids:
                raise ValueError(f'Snapshot {nout}: galaxy IDs missing from catalogue: {missing_ids}')
            loaded_nout = nout

        gal = galaxy_by_id[id]
        output_root = str(output_base / f'gal_{nout:04d}') + '/'
        print(f'Processing [{order + 1}/{len(targets)}] (nout={nout}, id={id}), R90={R90} kpc', end='\n\n')
        snap = uri.RamsesSnapshot(
            repo=repo, path_in_repo=path_in_repo, iout=nout,
            mode=mode, longint=False)

        boxtokpc = 1/snap.unit['kpc']
        snap.set_box_halo(gal, 
                        use_halo_radius=False, 
                        radius=max(boxrad, 1.5 * R90)/boxtokpc)

        star = snap.get_part(pname='star')
        cell = snap.get_cell()
        snap.clear()

        center = np.array([
            gal['x'],
            gal['y'],
            gal['z']
        ])

        pos = np.column_stack([star['x'], star['y'], star['z']])
        pos_cell = np.column_stack([cell['x'], cell['y'], cell['z']])
        
        dpos = (pos - center) * boxtokpc
        r = np.sqrt(np.sum(dpos**2, axis=1))
        pos_mask = r <= R90 * 1.5

        dpos_cell = (pos_cell - center) * boxtokpc
        r_cell = np.sqrt(np.sum(dpos_cell**2, axis=1))
        pos_mask_cell = r_cell <= R90 * 1.5

        star = star[pos_mask]
        cell = cell[pos_mask_cell]

        
        p_mC_small = cell['d1']*cell['m','Msun']
        p_mC_large = cell['d2']*cell['m','Msun']
        p_mSil_small = cell['d3']*cell['m','Msun']/SioverSil
        p_mSil_large = cell['d4']*cell['m','Msun']/SioverSil

        p_m_H = cell['m','Msun']
        sfe_s = np.full_like(star['m','Msun'], 0.025) # Follwing SKIRT-COLIBRE pipeline
        cnd_s = np.full_like(star['m','Msun'], 320) # Follwing SKIRT-COLIBRE pipeline

        repo_par = '/home/yuchang/JKsKIRT/JKsKIRT/example/'
        fname_par = 'Attenuation_parameter'

        if repo_par not in sys.path:
            sys.path.append(repo_par)
        if fname_par in sys.modules:
            par = reload(sys.modules[fname_par])
        else:
            par = __import__(fname_par)

        par.repo = output_root
        par.repo_output = f'{id:04d}/'
        par.z_red = float(df.loc[(nout, id), 'z'])
        if par.z_red > 0:
            par.inst_dist = 0
        par.los_angles = los_angles
        par.inst_1d_sed_only = True
        par.save_1d_sed = True
        los_dir = Path(par.repo) / par.repo_output
        los_dir.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({
            'los_id': np.arange(n_los),
            'instrument_prefix': [f'los_{i:03d}' for i in range(n_los)],
            'inclination_deg': los_angles[:, 0],
            'azimuth_deg': los_angles[:, 1],
            'roll_deg': np.full(n_los, par.roll_default),
            'x': los_vectors[:, 0], 'y': los_vectors[:, 1], 'z': los_vectors[:, 2],
        }).to_csv(los_dir / 'fibonacci_los.csv', index=False)
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
