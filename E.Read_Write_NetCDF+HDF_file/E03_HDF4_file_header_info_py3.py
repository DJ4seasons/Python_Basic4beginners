"""
Print header information of HDF4 file

---
TMPA (3B42) data (10.5067/TRMM/TMPA/DAY/7)
Reference:
Huffman, G.J., R.F. Adler, D.T. Bolvin, E.J. Nelkin (2010), The TRMM Multi-satellite Precipitation Analysis (TMPA). Chapter 1 in Satellite Rainfall Applications for Surface Hydrology, doi:10.1007/978-90-481-2915-7

Daeho Jin
"""

import sys
import os.path
import numpy as np

from pyhdf.SD import SD, SDC

def open_hdf4(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=SD(fname, SDC.READ)
    print("Open:",fname)
    return hid


##-- Parameters
indir='../data/'
fname=indir+'3B42.20180218.00.7.HDF'

hdf_f = open_hdf4(fname)

dinfo= hdf_f.datasets()
#print(hdf_f.datasets())
for dd in dinfo:
    print("Name: {}".format(dd))
    print("   Values: {}".format(dinfo[dd]))
