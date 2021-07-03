'''
Read text file

1. Reading manually
2. Using Numpy.genfromtxt() [can treat missing data; more complex than loadtxt()]

Data file:  Data/rmm.74toRealtime.txt (Real-Time Multivariate MJO(RMM) Index)
RMM values up to "real time". For the last few days, ACCESS analyses are used instead of NCEP
year, month, day, RMM1, RMM2, phase, amplitude.  Missing Value= 1.E36 or 999
      1974           6           1   1.6344700       1.2030400               5   2.0294800      Final_value:__OLR_&_NCEP_winds
      1974           6           2   1.6028900       1.0151200               5   1.8972900      Final_value:__OLR_&_NCEP_winds
      1974           6           3   1.5162500       1.0855100               5   1.8647600      Final_value:__OLR_&_NCEP_winds
...
      2021           4          28  -2.7815382      0.77270848               8   2.8868728     Prelim_value:_OLR_&_ACCESS_wind
      2021           4          29  -2.9952881      0.51753217               8   3.0396695     Prelim_value:_OLR_&_ACCESS_wind
      2021           4          30  -3.2881062      4.61135954E-02           8   3.2884295     Prelim_value:_OLR_&_ACCESS_wind


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

    Reference: https://numpy.org/doc/1.20/reference/generated/numpy.genfromtxt.html
    """

    if not os.path.isfile(fname):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist: "+fname)


    names=('yr','mon','day','pc1','pc2','phs','amp')
    dtypes=(int,int,int,float,float,int,float)

    data= np.genfromtxt(fname, names=names, dtype=dtypes, skip_header=2, usecols=range(len(names)) )
    ## missing_values=[1.e36, 999], usemask=True  # Return a masked array

    print("Total RMM data record=",len(data))
    print(type(data),data.dtype,data.shape)
    ### Note that now the "data" is structured array
    ### https://numpy.org/doc/stable/user/basics.rec.html
    ### Hence, transforming process is added in order to match output format

    time_info= data[['yr','mon','day']].view() #.astype(int)
    pcs= data[['pc1','pc2']].view()
    phs= data['phs'].view()
    amps= data['amp'].view()
    '''
    ### Another strategy: read without names
    data= np.genfromtxt(fname, skip_header=2, usecols=range(len(names)))
    print("Total RMM data record=",len(data))
    print(type(data),data.dtype,data.shape)  # Results in all floats

    time_info= data[:,:3].astype(int)
    pcs= data[:,3:5]
    phs= data[:,5].astype(int)
    amps= data[:,6]
    '''
    return time_info,pcs,phs,amps

def main():
    indir= '../Data/'
    infn= indir+'rmm.74toRealtime.txt'
    test_idx= 1000

    print("* Method1")
    rmm_data= read_rmm_manual(infn)
    for arr in rmm_data:
        print(arr.shape, arr[test_idx])

    print("\n* Method2")
    rmm_data2= read_rmm_genfromtxt(infn)
    for arr in rmm_data2:
        print(arr.shape, arr[test_idx])

    return

if __name__ == "__main__":
    main()
