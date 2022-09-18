"""
Read HDF5 file and write a few variables to a new hdf5 file

Daeho Jin

---
Data: IMERG V06B Final (http://dx.doi.org/10.5067/GPM/IMERG/3B-HH/05)

Reference:
Huffman, G. J., & Coauthors. (2018). GPM Integrated Multi‐Satellite Retrievals for GPM (IMERG) Algorithm Theoretical
Basis Document (ATBD) v5.2. NASA. Retrieved from https://gpm.nasa.gov/resources/documents/gpm-integrated-multi-
satellite-retrievals-gpm-imerg-algorithm-theoretical-basis

Source:
https://gpm.nasa.gov/data-access/downloads/gpm

"""

import sys
import os.path
import numpy as np

import h5py
import E05_HDF5_file_header_info_py3 as hdf5_fns
from datetime import datetime

def main():
    ##-- Parameters
    indir='../Data/'
    fname=indir+'3B-HHR.MS.MRG.3IMERG.20180218-S000000-E002959.0000.V06B.HDF5'

    var_names= ['time','lon', 'lat', 'precipitationCal']
    h5keys=['Grid/'+var for var in var_names]

    ## Open file and test keys
    hdf_f = hdf5_fns.open_hdf5(fname)
    for key in h5keys:
        hdf_key_test(hdf_f, key)

    ## Read data
    times= hdf_f[h5keys[0]][:]  # datetime.utcfromtimestamp(times[0])
    lons= hdf_f[h5keys[1]][:]
    lats= hdf_f[h5keys[2]][:]  # Now numpy array, same as netCDF, but not MaskedArray
    prcp= hdf_f[h5keys[3]]  # h5py data array
    print(type(lats), type(prcp))
    print(lons.shape, lats.shape, prcp.shape)

    attrs= list(prcp.attrs.items())  # Save for using it at writing stage
    prcp= prcp[:]  # Now numpy array
    hdf_f.close()
    print(type(prcp), prcp.dtype)

    ## Are there missings?
    fill_value= search_fill_value(attrs)
    ms_idx= prcp==fill_value
    print("# of missing grid cells=",ms_idx.sum())
    print()

    ### Create a hdf file
    outdir= indir
    outfn= outdir+'3B-HHR.MS.MRG.3IMERG.20180218-S000000-E002959.0000.V06B.simple.HDF5'
    with h5py.File(outfn, 'w') as f:
        dset0 = f.create_dataset("time", data=times)
        dset1 = f.create_dataset("lon", data=lons)
        dset2 = f.create_dataset("lat", data=lats)
        dset3 = f.create_dataset(var_names[3], data=prcp, dtype='f4')  # dtype is forced
        ## For compression,
        ## compression= "gzip", compression_opts=N  # N= 0 to 9
        ## Other compression methods: "lzf", "szip" Or, scaleoffset=N
        ## https://docs.h5py.org/en/stable/high/dataset.html#lossless-compression-filters
        ## For fill value,
        ## Note on attribute! (since it is based on ndarray, not masked array)

        f["lon"].dims[0].label='lon'  # Or dset1.dims[0].label
        f["lat"].dims[0].label='lat'

        dset3.dims[0].label='time'  # Or f[varname[3]].dims[0].label
        dset3.dims[1].label='lat'
        dset3.dims[2].label='lon'
        for (name, val) in attrs:
            dset3.attrs[name]=val

    print(outfn+" is written\n")

    ## Test the written netcdf file
    test= True
    if test:
        hdf_f2= hdf5_fns.open_hdf5(outfn)
        hdf5_fns.hdf_key_details(hdf_f2, var_names[3])

    return

def hdf_key_test(f, key1):
    print(key1)
    keys= key1.strip().split('/')

    if keys[0] not in list(f.keys()):
        print(list(f.keys()))
        sys.exit('Key name is not matched: {}'.format(keys[0]))
    else:
        if len(keys)>1:
            if keys[1] not in list(f[keys[0]].keys()):
                sys.exit('Key name is not matched: {}'.format(keys[1]))
        print('key is available')
    return

def search_fill_value(attrs_list):
    for name, val in attrs_list:
        if name=='_FillValue':
            return val
    print("_FillValue is not found")
    return -999

if __name__ == "__main__":
    main()
