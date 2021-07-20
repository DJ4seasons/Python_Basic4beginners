"""
Print header information of NetCDF file (i.e., ncdump -h)

Both NetCDF3 and NetCDF4 formats are supported by 'netCDF4' module

Daeho Jin
"""

import sys
import os.path
import numpy as np

from netCDF4 import Dataset

def main():
    ###--- Parameters
    indir= '../Data/'

    ### netCDF3 example:
    #fname= indir+'AMO_HADLEY.1870-2010.CLM_1901-1970.nc'

    ### netCDF4 example:
    fname= indir+'CCMP_Wind_Analysis_20190101_V02.0_L3.0_RSS.nc'

    ### Open netcdf file
    nc_f= open_netcdf(fname)

    ### Print details of netCDF file
    print_netcdf_details(nc_f)

    nc_f.close()
    return

def open_netcdf(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    fid=Dataset(fname,'r')
    print("Open:",fname)
    return fid

def print_netcdf_details(nc_fid):

    ###--- NetCDF version info
    print("\n*** NC Format=",nc_fid.data_model)

    ###--- Dimensions
    print("\n*** Dimensions ***")
    for nc_dim in nc_fid.dimensions:
        print('   {}'.format(str(nc_fid.dimensions[nc_dim]).split(':')[1]))

    ###--- Variables
    print("\n*** Variables ***")
    print(type(nc_fid.variables))
    var_names= list(nc_fid.variables.keys())
    for i, vn in enumerate(var_names):
        print("{:3d}: {}".format(i+1,vn))

    ##-- Select a variable to see the details
    while True:
        answer= input("\nIf want to attribute details, type the number of variable.\n")
        if answer.isnumeric() and (int(answer)>0 and int(answer)<=len(var_names)):
            vnm= var_names[int(answer)-1]
            print(nc_fid.variables[vnm])
        else:
            break

    ###--- Attributes
    print("\n*** Global Attributes ***")
    nc_attrs= nc_fid.ncattrs()
    for nc_attr in nc_attrs:
        print('   {}: {}'.format(nc_attr,nc_fid.getncattr(nc_attr)))
    return

if __name__ == "__main__":
    main()
