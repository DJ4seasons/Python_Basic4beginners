'''
Write binary file

1. After reading HadISST text file (same as D02),
2. write SST values to binary file


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
            sys.exit("Your type {} is inappropriate.".format(answer))
    else:
        mode='wb'

    ### Wirte sst to a binary file
    with open(filename, mode) as f:
        data.astype(dtype).tofile(f)

def main():
    indir= '../Data/'
    yrs= [2017,2019]  # Starting year and ending year
    for yr in range(yrs[0],yrs[1]+1,1):
        #HadISST1_SST_2019.txt
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

    ###---- Same as D02 so far
    ### Next, change land area values to -999.9 while keep ice-cover value(-10.00)
    new_undef= -999.9
    miss_idx= sst<-99.
    sst[miss_idx]= new_undef

    outdir= indir
    outfn= outdir+'HadISST1.sample.{}-{}.{}x{}x{}.f32dat'.format(*yrs,*sst.shape)  # File info on file name
    write_binary_data(outfn, sst)  # 'dtype=np.float3' option is omitted.
    return

if __name__ == "__main__":
    main()
