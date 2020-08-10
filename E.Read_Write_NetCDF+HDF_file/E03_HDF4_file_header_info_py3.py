"""
Print header information of HDF4 file

---
TMPA (3B42) data (10.5067/TRMM/TMPA/DAY/7)
Reference:
Huffman, G.J., R.F. Adler, D.T. Bolvin, E.J. Nelkin (2010), The TRMM Multi-satellite Precipitation Analysis (TMPA). Chapter 1 in Satellite Rainfall Applications for Surface Hydrology, doi:10.1007/978-90-481-2915-7

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

from pyhdf.SD import SD, SDC

def open_hdf4(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=SD(fname, SDC.READ)
    print("Open:",fname)
    return hid

def print_hdf4_details(hdf_fid):
    dsets= hdf_fid.datasets()
    vnames=[]
    for i,dd in enumerate(dsets.keys()):
        print("{:3d} Name: {}".format(i+1,dd))
        print("   Values: {}".format(dsets[dd]))
        vnames.append(dd)
    return vnames

def main():
    ##-- Parameters
    indir='../Data/'
    #fname=indir+'3B42.20180218.00.7.HDF'
    fname= indir+'MYD04_L2.A2019001.0420.061.2019001165304.hdf'

    ##-- Open hdf4 file
    hdf_f = open_hdf4(fname)

    ##-- Print variable names
    var_names= print_hdf4_details(hdf_f)

    ##-- Select a variable to see the details
    while True:
        answer= input("\nIf want to attribute details, type the number of variable.\n")
        if answer.isnumeric() and (int(answer)>0 and int(answer)<=len(var_names)):
            vnm= var_names[int(answer)-1]
            print('\nAttributes of {}'.format(vnm))
            attr= hdf_f.select(vnm).attributes()
            for item in attr.keys():
                print('{}: {}'.format(item,attr[item]))
        else:
            break
    hdf_f.end()  # Close hdf4 file
    return

if __name__ == "__main__":
    main()
