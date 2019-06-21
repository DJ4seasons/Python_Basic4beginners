import sys
import numpy as np
import os.path

def bin_file_read2mtx(fname,dtype=np.float32):
    """ Open a binary file, and read data
        fname : file name
        dtype   : data type; np.float32 or np.float64, etc. """

    if not os.path.isfile(fname):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist:"+fname)

    #fd=open(fname,'rb')
    with open(fname,'rb') as f:
        bin_mat = np.fromfile(file=f,dtype=dtype)
    #fd.close() ### Not needed with "with"

    return bin_mat


###---- Main

##-- Parameters
nn=1000

data_dir= './data/'

##-- Build and write a dataset for test
arr=np.arange(nn)
fnout = data_dir+'temp_bin.f32dat'

if not os.path.isfile(fnout):
    with open(fnout,'wb') as f:
        arr.astype(np.float32).tofile(f)

##-- Read binary file with np.memmap
arr2=np.memmap(fnout,dtype=np.float32,mode='r',shape=(nn,))

print(arr[10:20],arr2[10:20])

del arr2

##-- Read part of data with 'offset'
nchunk=100
nbyte=4 #<-- float32 = 4byte

for i in range(int(nn/nchunk)):
    small_arr=np.memmap(fnout,dtype=np.float32,mode='r',shape=(nchunk,),offset=nchunk*nbyte*i)
    small_arr=np.array(small_arr)
    print('i={}, error={}'.format(i,(arr[nchunk*i:nchunk*(i+1)]-small_arr).mean()))
