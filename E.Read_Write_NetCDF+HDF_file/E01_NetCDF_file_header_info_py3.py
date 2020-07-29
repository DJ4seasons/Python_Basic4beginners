"""
Print header information of NetCDF file

Both NetCDF3 and NetCDF4 formats are supported by 'netCDF4' module

Daeho Jin
"""

import sys
import os.path
import numpy as np

from netCDF4 import Dataset

def open_netcdf(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    fid=Dataset(fname,'r')
    print("Open:",fname)
    return fid

def print_netcdf_details(nc_fid):

    ###--- Dimensions
    print("\n*** Dimensions ***")
    for nc_dim in nc_fid.dimensions:
        print('   {}'.format(str(nc_fid.dimensions[nc_dim]).split(':')[1]))

    ###--- Variables
    print("\n*** Variables ***")
    for var in nc_fid.variables:
        print(nc_fid.variables[var])
        print('')

    ###--- Attributes
    print("\n*** Global Attributes ***")
    nc_attrs= nc_fid.ncattrs()
    for nc_attr in nc_attrs:
        print('   {}: {}'.format(nc_attr,nc_fid.getncattr(nc_attr)))

def main():

    ###--- Parameters
    indir= '../data/'

    ### netCDF3 example:
    fname= indir+'AMO_HADLEY.1870-2010.CLM_1901-1970.nc'

    ### netCDF4 example:
    #fname= indir+'CCMP_Wind_Analysis_20190101_V02.0_L3.0_RSS.nc'

    ### Open netcdf file
    nc_f= open_netcdf(fname)
    print("\n*** NC Format=",nc_f.data_model)

    ### Print details of netCDF file
    if True:
        print_netcdf_details(nc_f)

    nc_f.close()
    return


if __name__ == "__main__":
    main()
