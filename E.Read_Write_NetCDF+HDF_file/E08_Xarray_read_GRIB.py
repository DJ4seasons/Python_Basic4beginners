"""
Read Grib file with Xarray
By Daeho Jin

Before start, please check if 'cfgrib' module is installed.
This module is necessary for reading grib files.
https://anaconda.org/conda-forge/cfgrib

---
Input file:
data/ocnf01.gdas.200101.grb2
(NCEP Climate Forecast System Reanalysis, Monthly product, WMO GRIB2)

Reference:
Saha, Suranjana, et. al., 2010: The NCEP Climate Forecast System Reanalysis.
    Bull. Amer. Meteor. Soc., 91(8), 1015-1057 (DOI: 10.1175/2010BAMS3001.1)

How to cite this data:
Saha, S., et al. 2010. NCEP Climate Forecast System Reanalysis (CFSR) Monthly Products,
    January 1979 to December 2010. Research Data Archive at the National Center for
    Atmospheric Research, Computational and Information Systems Laboratory.
    https://doi.org/10.5065/D6DN438J.

Download site:
https://rda.ucar.edu/datasets/ds093.2/
"""


import sys
import os.path
import numpy as np
from datetime import datetime
import xarray as xr

def main():
    ###--- Parameters
    tgt_date= datetime(2001,1,1)
    date_str= tgt_date.strftime('%Y%m')
    #date_str= '{}{:02d}{:02d}'.format(2019,1,1)

    indir = '../Data/'
    #ocnf01.gdas.200101.grb2
    infn= indir+'ocnf01.gdas.{}.grb2'.format(date_str)

    # Open as Xarray Dataset including several DataArrays
    # Due to the characteristics of this file, we have to select one of these options.
    # filter_by_keys={'typeOfLevel': 'depthBelowSea'}, {'typeOfLevel': 'surface'}, {'typeOfLevel': 'unknown'}, {'typeOfLevel': 'oceanIsotherm'}
    ds = xr.open_dataset(infn,engine='cfgrib',filter_by_keys={'typeOfLevel': 'surface'})
    print(ds)
    # Then, we can see these variable names:
    # uflx, vflx, sshg, siconc, unknown, sde, t, emnp, thflx

    keys0= ['longitude','latitude','sshg']
    print('\n** Read data "sshg"**')
    data=[]
    for k in keys0:
        data1= ds[k]  #.to_numpy()  # If you want to change to Numpy array, try this function.
        print(k,type(data1),data1.shape)  # Note that the type is 'xarray.core.dataarray.DataArray'
        data.append(data1)
    # Test if the data is read well
    import matplotlib.pyplot as plt
    plt.pcolormesh(*data,shading='nearest')
    plt.colorbar() # Draw colorbar
    plt.show()

    return

if __name__ == "__main__":
    main()
