"""
Print header information of HDF5 file

Daeho Jin

---
Data: IMERG V06 Final (http://dx.doi.org/10.5067/GPM/IMERG/3B-HH/05)

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

def main():
    ##-- Parameters
    indir= '../Data/'
    fname= indir+'3B-HHR.MS.MRG.3IMERG.20180218-S000000-E002959.0000.V06B.HDF5'

    hdf_f = open_hdf5(fname)

    h5keys=[]
    hdf_f.visit(h5keys.append)  # Visit every key and save in list
    for i,key_name in enumerate(h5keys):
        print("{}: {}".format(i,key_name))

    ##-- Select a variable to see the details
    while True:
        answer= input("\nIf want to attribute details, type the number of variable.\n")
        if answer.isnumeric() and (int(answer)>0 and int(answer)<=len(h5keys)):
            hdf_key_details(hdf_f, h5keys[int(answer)])
        else:
            break

    hdf_f.close()
    return

import h5py
def open_hdf5(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid = h5py.File(fname,'r')
    print("Open:",fname)
    return hid

def hdf_key_details(hdf_fid, key_name):
    print("\n{}".format(key_name))
    dset=hdf_fid[key_name]
    for (name, val) in dset.attrs.items():
        print("Name: {}".format(name))
        print("   Values: {}".format(val))
    return

if __name__ == "__main__":
    main()
