'''
Read text file

1. Reading manually
2. Using Numpy.genfromtxt()

Data file:  Real-Time Multivariate MJO(RMM) Index
Source: http://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt
Referece: Wheeler, M. C., and H. H. Hendon, 2004: An all-season real-time multivariate MJO index: Development of
an index for monitoring and prediction. Mon. Wea. Rev., 132, 1917-1932. doi:10.1175/1520-0493(2004)132<1917:AARMMI>2.0.CO;2

By Daeho Jin
'''

import sys
import os.path
import numpy as np

def read_rmm_manual(fname):
    """
    Read RMM Index Text file
    fname: include directory

    Assume that we already know the structure of text file.
    There are 2 lines header.
    var_names= year, month, day, RMM1, RMM2, phase, amplitude.  Missing Value= 1.E36 or 999
    """

    if not os.path.isfile(fname):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist: "+fname)

    time_info, pcs, phs, amps= [], [], [], []
    with open(fname,'r') as f:
        for i,line in enumerate(f):
            if i>=2:  # Skip header (2 lines)
                ww=line.strip().split()
                time_info.append([int(item) for item in ww[:3]])  # Yr,Mo,Dy
                pcs.append([float(ww[3]),float(ww[4])]) # RMM PC1 and PC2
                phs.append(int(ww[5]))  # MJO Phase
                amps.append(float(ww[6]))  # MJO Strength

    print("Total RMM data record=",len(phs))
    #return time_info,pcs,phs,amps  # This is also possible
    return np.asarray(time_info),np.asarray(pcs),np.asarray(phs),np.asarray(amps) ### Return as Numpy array

def read_rmm_genfromtxt(fname):
    """
    Read RMM Index Text file
    fname: include directory

    Assume that we already know the structure of text file.
    There are 2 lines header.
    var_names= year, month, day, RMM1, RMM2, phase, amplitude.  Missing Value= 1.E36 or 999
    """

    if not os.path.isfile(fname):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist: "+fname)

    dtypes= dict(names=('yr','mon','day','pc1','pc2','phs','amp'),
                formats=(int,int,int,float,float,int,float))

    data= np.genfromtxt(fname, dtype=dtypes, skip_header=2, usecols=range(len(dtypes['names'])))
    print("Total RMM data record=",len(data))
    print(type(data),data.dtype,data.shape)
    ### Note that now the "data" is structured array
    ### https://numpy.org/doc/stable/user/basics.rec.html
    ### Hence, transforming process is added in order to match output format

    int_part_idx= [dtypes['names'].index(item) for item in ['yr','mon','day','phs']]
    int_part= data.view(int).reshape(data.shape+(-1,))[:,int_part_idx]

    float_part_idx= [dtypes['names'].index(item) for item in ['pc1','pc2','amp']]
    float_part= data.view(float).reshape(data.shape+(-1,))[:,float_part_idx]

    time_info= int_part[:,:3]
    pcs= float_part[:,:2]
    phs= int_part[:,-1]
    amps= float_part[:,-1]
    return time_info,pcs,phs,amps

def main():
    indir= '../Data/'
    infn= indir+'rmm.74toRealtime.txt'

    rmm_data= read_rmm_manual(infn)
    test_idx= 1000
    for arr in rmm_data:
        print(arr.shape, arr[test_idx])

    rmm_data2= read_rmm_genfromtxt(infn)
    test_idx= 1000
    for arr in rmm_data2:
        print(arr.shape, arr[test_idx])
    return

if __name__ == "__main__":
    main()
