'''
Write text file

1. After reading RMM index file (same as D01),
2. filtering only for super-strong MJOs (strength>2)
3. then write results to text file

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

def write_text_rmm(filename, rmm_data):
    ### First, check the file if already exist
    if os.path.isfile(filename):
        print("\n{} already exist".format(filename))
        answer= input("If want to overwrite, type 'y'; If want to append, type 'a'\n")
        if answer[0].lower()=='y':
            mode= 'w'  # '(w)rite'
        elif answer[0].lower()=='a':
            mode= 'a'  # '(a)ppend'
        else:
            sys.exit("Your type {} is inappropriate.".format(answer))

    with open(filename, mode) as f:
        header1= "RMM Index only for strong MJOs (amplitude>1)\n"
        header2= "Year,Mon,Day,PC1,PC2,Phase,Amplitude\n"
        f.write(header1)
        print(header2[:-1], file=f)  # Print() insert '\n' automatically

        for i in range(rmm_data[-1].shape[0]):
            time_info= ",".join(rmm_data[0][i,:].astype(str))
            pcs= ",".join(rmm_data[1][i,:].astype(str))

            one_line= "{},{},{:d},{:.5f}\n".format(time_info,pcs,rmm_data[2][i],rmm_data[3][i])
            f.write(one_line)

def main():
    indir= '../data/'
    infn= indir+'rmm.74toRealtime.txt'

    rmm_data= read_rmm_manual(infn)
    test_idx= 1000
    for arr in rmm_data:
        print(arr.shape, arr[test_idx])

    ###---- Same as D01 so far
    ### Next, filtering for super-strong MJOs
    miss_idx= rmm_data[2]==999
    strong_idx= np.logical_and(rmm_data[-1]>2, ~miss_idx)
    rmm_data= [arr[strong_idx] for arr in rmm_data]
    print("After filtering")
    for arr in rmm_data:
        print(arr.shape, arr[test_idx])

    ### Save the results
    outdir= indir
    outfn= outdir+'rmm.74toRealtime.OnlyStrongMJOs.csv'
    write_text_rmm(outfn, rmm_data)
    return

if __name__ == "__main__":
    main()
