'''
Read binary file

Read binary file using Numpy.fromfile()
Binary data file(HadISST) was produced by D04 code


Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

By Daeho Jin
'''

import sys
import os.path
import numpy as np

def bin_file_read2mtx(fname, dtype=np.float32):
    """ Open a binary file, and read data
        fname : file name with directory path
        dtype   : data type; np.float32 or np.float64, etc. """

    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    with open(fname,'rb') as fd:
        bin_mat = np.fromfile(file=fd, dtype=dtype)

    return bin_mat

def check_data_plot(arr1d):
    import matplotlib.pyplot as plt
    plt.plot(arr1d)
    plt.show()

def main():
    ###--- Parameters
    indir= '../data/'
    #HadISST1.sample.2017-2019.36x180x360.f32dat
    yrs= [2017,2019]  # Starting year and ending year
    mon_per_yr= 12
    nt= (yrs[1]-yrs[0]+1)*mon_per_yr
    nlat, nlon= 180, 360

    infn= indir+"HadISST1.sample.{}-{}.{}x{}x{}.f32dat".format(*yrs,nt,nlat,nlon)
    sst= bin_file_read2mtx(infn)  # 'dtype' option is omitted because 'f32' is basic dtype
    sst= sst.reshape([nt,nlat,nlon])
    print(sst.shape)

    ### We already know that missings are -999.9, and ice-cover value is -10.00.
    miss_idx= sst<-9.9
    sst[miss_idx]= np.nan

    ### Calculate meridional mean
    sst_mean= np.nanmean(sst, axis=(0,2))

    ### Check data using simple plot
    check_data_plot(sst_mean)
    return

if __name__ == "__main__":
    main()
