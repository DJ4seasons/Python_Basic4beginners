"""
Print header information of HDF5 file

"""


import sys
import numpy as np
import os.path


import h5py

def open_hdf5(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=h5py.File(fname,'r')
    print("Open:",fname)
    return hid

def printname(name):
    global i
    print(i,name)
    i+=1


##-- Parameters
indir='./data/'
#fname=indir+'3B-HHR.MS.MRG.3IMERG.20180218-S000000-E002959.0000.V06A.HDF5'
fname=indir+'AERDB_L2_VIIRS_SNPP.A2014067.1936.001.2019056041229.nc'
#fname=indir+'AERDB_temp.hdf5'

hdf_f = open_hdf5(fname)

i=0
hdf_f.visit(printname)


h5keys=[]
hdf_f.visit(h5keys.append)


it=2
print("\n{}".format(h5keys[it]))
dset=hdf_f[h5keys[it]]
for (name, val) in dset.attrs.items():
    print("Name: {}".format(name))
    print("   Values: {}".format(val))

it=43
print("\n{}".format(h5keys[it]))
dset=hdf_f[h5keys[it]]
for (name, val) in dset.attrs.items():
    print("Name: {}".format(name))
    print("   Values: {}".format(val))
