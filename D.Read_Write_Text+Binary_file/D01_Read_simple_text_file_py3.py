'''
Read text file (simple methods)

1. Using readlines(): All the lines at once
2. Using Numpy.loadtxt(): Convert text to numpy array (without missings)

Reference:
https://docs.python.org/3.8/library/stdtypes.html?highlight=strip#string-methods
https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects
https://numpy.org/devdocs/reference/generated/numpy.loadtxt.html

Data file:  Data/MERRA2_model_levels.txt
1	0.01	13	0.6168	25	9.2929	37	78.5123	49	450	61	820
2	0.02	14	0.7951	26	11.2769	38	92.3657	50	487.5	62	835
3	0.0327	15	1.0194	27	13.6434	39	108.663	51	525	63	850
4	0.0476	16	1.3005	28	16.4571	40	127.837	52	562.5	64	865
5	0.066	17	1.6508	29	19.7916	41	150.393	53	600	65	880
6	0.0893	18	2.085	30	23.7304	42	176.93	54	637.5	66	895
7	0.1197	19	2.6202	31	28.3678	43	208.152	55	675	67	910
8	0.1595	20	3.2764	32	33.81	44	244.875	56	700	68	925
9	0.2113	21	4.0766	33	40.1754	45	288.083	57	725	69	940
10	0.2785	22	5.0468	34	47.6439	46	337.5	58	750	70	955
11	0.365	23	6.2168	35	56.3879	47	375	59	775	71	970
12	0.4758	24	7.6198	36	66.6034	48	412.5	60	800	72	985

Source: https://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf

By Daeho Jin
'''

import sys
import os.path
import numpy as np

def main():
    ### File Info
    indir= '../Data/'
    infn= indir+'MERRA2_model_levels.txt'

    ### Check if file exists
    if not os.path.isfile(infn):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist: "+fname)

    ### Basic method to open a file
    f= open(infn,'r')  # 'r', 'w', 'a'
    f.close()

    ### Recommended method to open a file
    with open(infn,'r') as f:  # file will be closed by itself at the end of block
        lines = f.readlines()
        ## Or test "lines = list(f)"

    print("# of lines = ",len(lines))
    print(lines[0])
    print("Starting and ending letters = '{}', '{}'".format(lines[0][0], lines[0][-1]))

    ### Convert from line to words
    all_words=[]
    for l in lines:
        if len(l)>0:  # Exclude empty line(s)
            ww= l.strip().split()  # See reference: string methods
            all_words.append([float(w) for w in ww])

    arr1 = np.asarray(all_words)
    print("Method 1: ",arr1.shape)

    ###----
    ### Use np.loadtxt()
    arr2 = np.loadtxt(infn)
    #with open(infn,'r') as f:  # It also works
    #    arr2 = np.loadtxt(f)
    print("Method 2: ",arr2.shape)

    ### Test if they are identical
    print("Are they identical?",np.array_equal(arr1,arr2))

    ###----
    ### Transform array to usuable form
    #nrow,ncol= arr1.shape
    arr1= arr1[:,1::2].T.reshape(-1)
    print("Model Levels: \n", arr1)

    ###----
    ### All at once
    arr3 = np.loadtxt(infn, usecols=[1,3,5,7,9,11]).T.reshape(-1)
    print("Are they identical?",np.array_equal(arr1,arr3))

    return

if __name__ == "__main__":
    main()
