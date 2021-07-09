"""
Open HDF4 file and draw a map of data

---
MYD04_L2 (Aqua Level2 Aerosol data)
DOI: Levy, R., Hsu, C., et al., 2015. MODIS Atmosphere L2 Aerosol Product. NASA MODIS Adaptive Processing System, Goddard Space Flight Center, USA:
http://dx.doi.org/10.5067/MODIS/MYD04_L2.006 (Aqua)

MODIS Aerosol Data Products can be found at the LAADS Web website.

Daeho Jin
"""

import sys
import os.path
import numpy as np

#from pyhdf.SD import SD, SDC
'''
def open_hdf4(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=SD(fname, SDC.READ)
    print("Open:",fname)
    return hid
'''

from E03_HDF4_file_header_info_py3 import open_hdf4
from E02_NetCDF_read_write_py3 import check_data_imshow

def main():
    ##-- Parameters
    indir='../Data/'
    #fname=indir+'3B42.20180218.00.7.HDF'
    fname= indir+'MYD04_L2.A2019001.0420.061.2019001165304.hdf'

    var_names= ['Latitude','Longitude', 'Optical_Depth_Land_And_Ocean']

    ##-- Open hdf4 file
    hdf_f = open_hdf4(fname)

    ##-- Read data
    data= [hdf_f.select(vn).get() for vn in var_names]
    attr= [hdf_f.select(vn).attributes() for vn in var_names]

    hdf_f.end()  # Close hdf4 file
    print(type(data[0]), data[0].shape)
    print(data[2].min(),data[2].max())
    print()

    for i,(d,a) in enumerate(zip(data,attr)):
        ms_idx= d==a['_FillValue']
        d= d.astype(float)
        d[ms_idx]= np.nan
        d= (d-a['add_offset'])*a['scale_factor']
        data[i]=d
        print(var_names[i],np.nanmin(d),np.nanmax(d),ms_idx.sum())

    check_data_imshow(data[2])

    return


if __name__ == "__main__":
    main()
