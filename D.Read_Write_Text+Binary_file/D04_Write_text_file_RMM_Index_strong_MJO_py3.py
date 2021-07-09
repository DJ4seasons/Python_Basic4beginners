'''
Write text file (with RMM data)

1. After reading RMM index file (same as D02),
2. filtering only for super-strong MJOs (strength>2)
3. then write results to text file

Data file:  Real-Time Multivariate MJO(RMM) Index
Source: http://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt
Referece: Wheeler, M. C., and H. H. Hendon, 2004: An all-season real-time multivariate MJO index: Development of
an index for monitoring and prediction. Mon. Wea. Rev., 132, 1917-1932. doi:10.1175/1520-0493(2004)132<1917:AARMMI>2.0.CO;2

By Daeho Jin

---

FYI, in the case of saving one numpy array to a text file, np.savetxt() can be an option.
https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
'''

import sys
import os.path
import numpy as np

def main():
    indir= '../Data/'
    infn= indir+'rmm.74toRealtime.txt'

    ### Import function from other program file (in the same directory)
    from D02_Read_text_file_RMM_Index_py3 import read_rmm_manual
    rmm_data= read_rmm_manual(infn)  # Return Time_info, PCs, Phases, Amplitude
    test_idx= 1000
    for arr in rmm_data:
        print(arr.shape, arr[test_idx])
    ###---- Same as D02 so far

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
    write_text_rmm(outfn, rmm_data, delimiter=',')
    return

def write_text_rmm(filename, rmm_data, delimiter='  '):
    ### First, check the file if already exist
    if os.path.isfile(filename):
        print("\n{} already exist".format(filename))
        answer= input("If want to overwrite, type 'y'; If want to append, type 'a'\n")
        if answer[0].lower()=='y':
            mode= 'w'  # '(w)rite'
        elif answer[0].lower()=='a':
            mode= 'a'  # '(a)ppend'
        else:
            sys.exit("Your input '{}' is not supported.".format(answer))
    else:
        mode='w'

    with open(filename, mode) as f:
        header1= "RMM Index only for strong MJOs (amplitude>2)\n"
        header2= "Year,Mon,Day,PC1,PC2,Phase,Amplitude\n"
        f.write(header1)
        print(header2[:-1], file=f)  # Print() insert '\n' automatically

        for i in range(rmm_data[-1].shape[0]):
            time_info= delimiter.join(rmm_data[0][i,:].astype(str))
            pcs= delimiter.join(rmm_data[1][i,:].astype(str))

            one_line= "{}{delimiter}{}{delimiter}{:d}{delimiter}{:.5f}\n".format(
                        time_info,pcs,rmm_data[2][i],rmm_data[3][i],
                        delimiter=delimiter)
            f.write(one_line)
    print("{} is written.".format(filename))
    return

if __name__ == "__main__":
    main()
