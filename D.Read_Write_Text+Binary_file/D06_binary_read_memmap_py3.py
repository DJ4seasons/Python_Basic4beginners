'''
Read binary file

Read binary file using Numpy.memmap()
Numpy.memmap() is good for huge binary file,
since it reads memory layout, not the data itself,
so we can handle large data even when the data is larger than memory size

Xie, P., A. Yatagai, M. Chen, T. Hayasaka, Y. Fukushima, C. Liu, and S. Yang (2007), A gauge-based analysis of daily precipitation over East Asia, J. Hydrometeorol., 8, 607. 626
Chen, M., W. Shi, P. Xie, V. B. S. Silva, V E. Kousky, R. Wayne Higgins, and J. E. Janowiak (2008), Assessing objective techniques for gauge-based analyses of global daily precipitation, J. Geophys. Res., 113, D04110
Mingyue Chen, Wei Shi, Pingping Xie, Viviane B. S. Silva, Vernon E. Kousky, R. Wayne Higgins, John E. Janowiak. (2008) Assessing objective techniques for gauge-based analyses of global daily precipitation. Journal of Geophysical Research 113:D4
---
National Center for Atmospheric Research Staff (Eds). Last modified 21 Jul 2018.
"The Climate Data Guide: CPC Unified Gauge-Based Analysis of Global Daily Precipitation."
Retrieved from https://climatedataguide.ucar.edu/climate-data/cpc-unified-gauge-based-analysis-global-daily-precipitation.

By Daeho Jin
'''

import sys
import os.path
import numpy as np
from datetime import date

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

def bin_file_read_memmap(fname, dtype=np.float32, shape=None, offset=0):
    """ Open a binary file and read data using np.memmap()
        fname : file name with directory path
        dtype : data type; np.float32 or np.float64, etc.
        shape : dimension of array to be loaded
        offset: offset value which is the starting point to read """

    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    try:
        bin_mat= np.memmap(fname, dtype=dtype, mode='r', shape=shape, offset=offset)
    except Exception as e:
        print("Error on np.memmap()")
        sys.exit(e)
    else:
        return bin_mat

def data_transform(arr_memmap, undef=np.nan):
    ### Change type to np.array()
    arr= np.array(arr_memmap)  # Be sure using np.array(), not np.asarray()

    ### Change missing value to NaN
    if not np.isnan(undef):
        miss_idx= arr==undef
        arr[miss_idx]= np.nan

    ### Basic unit is 0.1 mm/day, and change to mm/hr
    arr/=240
    return arr

def check_data_imshow(arr2d, origin='lower'):
    import matplotlib.pyplot as plt
    plt.imshow(arr2d, origin=origin)
    plt.colorbar()
    plt.show()

def main():
    ###--- Parameters
    indir= '../Data/'
    #PRCP_CU_GAUGE_V1.0GLB_0.50deg.lnx.20200701.RT
    tgt_date= date(2020,7,1)
    tgt_date_name= tgt_date.strftime('%Y%m%d')
    nlat, nlon= 360, 720
    nvars= 2  # 'rain' and 'gnum'
    undef= -999.
    ### The order of grads readable file: x -> y -> z -> var -> t
    ### In python, dimension order is reversed
    data_dim= (nvars, nlat, nlon)  # Make sure it's tuple

    infn= indir+"PRCP_CU_GAUGE_V1.0GLB_0.50deg.lnx.{}.RT".format(tgt_date_name)
    ### Actually, this sample file is not big enough to avoid np.fromfile()
    ### However, this code intend to show exmaple of np.memmap()
    prcp= bin_file_read_memmap(infn, dtype=np.float32, shape=data_dim)
    print(type(prcp), prcp.shape)

    prcp= prcp[0,60:300,:]  # Slicing for rain, 60S-60N
    print("After slicing")
    print(type(prcp), prcp.shape)

    ### Data specific treatment
    prcp= data_transform(prcp, undef=undef)

    ### Check data using simple plot
    check_data_imshow(prcp)

    ###-----------------
    ### Test np.memmap() with offset
    ### The purpose of setting 'offset' option is to read specific part, not read as a whole
    ### Remind that current data shape= (nvars, nlat, nlon)
    ### Assume that we want to read the first variable and from 60S-60N only.
    nbyte= 4  # float32(bit) = 4 Byte
    latidx2read= [60,300]
    offset= nbyte*nlon*latidx2read[0]  # Passing this amount of data by assuming 1-d array
    data_dim2read= (latidx2read[1]-latidx2read[0], nlon)  # Make sure it's tuple

    prcp2= bin_file_read_memmap(infn, dtype=np.float32, shape=data_dim2read, offset=offset)
    print('Using offset option')
    print(type(prcp2), prcp2.shape)

    prcp2= data_transform(prcp2, undef=undef)

    ### Test if two precip arrays are same
    print(np.nanmax(np.absolute(prcp-prcp2)),np.allclose(prcp, prcp2,equal_nan=True))
    return


if __name__ == "__main__":
    main()
