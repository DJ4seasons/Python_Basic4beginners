'''
Write binary file (with HadISST data)

1. After reading HadISST text file (same as D03),
2. write SST values to binary file


Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

By Daeho Jin

---

https://numpy.org/doc/stable/reference/generated/numpy.ndarray.tofile.html
'''

import sys
import os.path
import numpy as np

### Import function from other program file (in the same directory)
from D03_Read_text_file_HadISST_py3 import read_hadisst_manually
# Or, import D03_Read_text_file_HadISST_py3 as fns  # then, call the function: fns.read_hadisst_manually

def main():
    indir= '../Data/'
    yrs= [2014,2021]  # Starting year and ending year
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
    ###---- Same as D03 so far

    ### Next, change land area values to -999.9 while keep ice-cover value(-10.00)
    new_undef= -999.9
    miss_idx= sst<-99.
    sst[miss_idx]= new_undef

    outdir= indir
    outfn= outdir+'HadISST1.sample.{}-{}.{}x{}x{}.f32dat'.format(*yrs,*sst.shape)  # File info on file name
    write_binary_data(outfn, sst)  # 'dtype=np.float32' option is omitted.
    return

def write_binary_data(filename, data, dtype=np.float32):
    ### First, check the file if already exist
    if os.path.isfile(filename):
        print("\n{} already exist".format(filename))
        answer= input("If want to overwrite, type 'y'; If want to append, type 'a'\n")
        if answer[0].lower()=='y':
            mode= 'wb'  # 'wb' not just 'w'
        elif answer[0].lower()=='a':
            mode= 'ab'  # 'append' 'binary'
        else:
            sys.exit("Your input '{}' is not supported.".format(answer))
    else:
        mode='wb'

    ### Wirte a ndarray to a binary file
    with open(filename, mode) as f:
        data.astype(dtype).tofile(f)

    print("{} is written.".format(filename))
    return

if __name__ == "__main__":
    main()
