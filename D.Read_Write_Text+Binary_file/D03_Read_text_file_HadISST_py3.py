'''
Read text file (with Hadley Ice-SST data)

1. Reading manually
# Numpy.genfromtxt() or loadtxt() is not working since number of columns is varying (due to daily header)

Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

All values are integers
Temperatures are stored as degrees C * 100
100% sea-ice-covered gridboxes are flagged as -1000 (actually -10.0)
Land squares are set to -32768
Fixed digit; for the land area, no gap between two '-32768's

The day, month and year are stored at the start of each month. The day simply tells
you on which day the month starts.

Data Array (360x180)
Item (  1,  1) stores the value for the 1-deg-area centred at 179.5W and 89.5N
Item (360,180) stores the value for the 1-deg-area centred at 179.5E and 89.5S

          ----- ----- -----
         |     |     |     |
         | DAY | MON | YR  |
         |_____|_____|_____|____________________________
     90N |(1,1)                                         |
         |                                              |
         |                                              |
         |                                              |
         |                                              |
         |(1,90)                                        |
     Equ |                                              |
         |(1,91)                                        |
         |                                              |
         |                                              |
         |                                              |
         |                                              |
     90S |(1,180)______________________________(360,180)|
          180W                 0                    180E

----

First line of data:
     1     1  2019   180 rows    360 columns

By Daeho Jin
'''

import sys
import os.path
import numpy as np

def main():
    indir= '../Data/'
    yrs= [2015,2020]  # Starting year and ending year
    for yr in range(yrs[0],yrs[1]+1,1):
        #HadISST1_SST_YYYY.txt
        infn= indir+'HadISST1_SST_{}.txt'.format(yr)

        time_info,sst1= read_hadisst_manually(infn)
        if yr==yrs[0]:
            times= np.copy(time_info)
            sst= np.copy(sst1)
        else:
            times= np.concatenate((times,time_info), axis=0)
            sst= np.concatenate((sst,sst1),axis=0)

    print(times.shape,sst.shape)

    ### Transform values to degreeC by dividing it by 100
    sst= sst/100.

    ### Now latitude starting 90N to 90S, so should be flipped.
    sst= sst[:,::-1,:]

    ### Change values represengint both ice-cover(-1000) and land area(-32768) to NaN
    miss_idx= sst<-9.9
    sst[miss_idx]= np.nan

    ### Calculate all-time mean
    sst_mean= sst.mean(axis=0)  # During all-time, if one nan is available, return nan

    ### Check data using simple plot
    check_data_imshow(sst_mean, origin='lower')
    return

def read_hadisst_manually(fname):
    """
    Read Hadley SST Text file
    fname: include directory
    """
    if not os.path.isfile(fname):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist: "+fname)

    time_info, vals = [], []
    width= 6  # Values are of fixed width in the text file
    with open(fname,'r') as f:
        for i,line in enumerate(f):
            if len(line)<50:  # Distinguish monthly header from sst data
                ww=line.strip().split()
                time_info.append([int(item) for item in ww[:3]])
                dims= [int(ww[3]),int(ww[5])]
                nct=0
                temp_array= []  # Initialize storage to save monthly sst data
            else:
                ww= [line[i:i+width] for i in range(0,len(line.strip()),width)]
                temp_array.append(ww)
                nct+=1
                if nct==dims[0]:  # If one month map is completed
                    vals.append(np.array(temp_array,dtype=np.int32))

    return np.asarray(time_info), np.asarray(vals)

def check_data_imshow(arr2d, origin='lower'):
    import matplotlib.pyplot as plt
    plt.imshow(arr2d, origin=origin)
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    main()
