"""
Print header information of HDF4 file


"""


import sys
import numpy as np
import os.path

from subprocess import call
from pyhdf.SD import SD, SDC

def open_hdf4(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=SD(fname,SDC.READ)
    print("Open:",fname)
    return hid


##-- Parameters
indir='./data/'
fname=indir+'3B42.20180218.00.7.HDF'

hdf_f = open_hdf4(fname)

dinfo= hdf_f.datasets()
#print(hdf_f.datasets())
for dd in dinfo:
    print("Name: {}".format(dd))
    print("   Values: {}".format(dinfo[dd]))


'''
h5keys=[]
hdf_f.visit(h5keys.append)


it=13
print("\n{}".format(h5keys[it]))
dset=hdf_f[h5keys[it]]
for (name, val) in dset.attrs.items():
    print("Name: {}".format(name))
    print("   Values: {}".format(val))

'''
