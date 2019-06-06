"""
Print header information of NetCDF file

Both NetCDF3 and NetCDF4 formats are supported.

"""


import sys
import numpy as np
import os.path

from subprocess import call
from netCDF4 import Dataset

def open_netcdf(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    fid=Dataset(fname,'r')
    print("Open:",fname)
    return fid



##-- Parameters
#indir='./data/'
#fname=indir+'AERDB_L2_VIIRS_SNPP.A2014067.1936.001.2019056041229.nc'
#fname=indir+'slp_wrfout_d01_2018-02-20_00:00:00.nc'

### Get file name from argument
if len(sys.argv)<2:
    sys.exit("Please provide NC file name as an argument!")
else:
    fname= str(sys.argv[1])   ## [1]: the first argument


nc_f= open_netcdf(fname)
print("\n*** NC Format=",nc_f.data_model)


###--- Attributes
print("\n*** Global Attributes ***")
nc_attrs= nc_f.ncattrs()
for nc_attr in nc_attrs:
    print('   {}: {}'.format(nc_attr,nc_f.getncattr(nc_attr)))

print("\n*** Dimensions ***")
for nc_dim in nc_f.dimensions:
#    print('   Name: {}'.format(nc_dim))
    print('   {}'.format(str(nc_f.dimensions[nc_dim]).split(':')[1]))
    
print("\n*** Variables ***")
for var in nc_f.variables:
    print(nc_f.variables[var])
          
nc_f.close()
