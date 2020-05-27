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

def memmap_range(nt,nt_chunk):
    #!!! Provide starting and ending point
    for n in range(nt//nt_chunk+1):
        n_ini= n*nt_chunk
        n_end= min((n+1)*nt_chunk,nt)
        yield n_ini,n_end

###---- Main

##-- Parameters
nn=1000
kk=500

data_dir= './data/'

##-- Build and write a dataset for test
arr=np.arange(nn*kk).reshape(nn,kk)
fnout = data_dir+'temp_bin.f32dat'

if not os.path.isfile(fnout):
    with open(fnout,'wb') as f:
        arr.astype(np.float32).tofile(f)

##-- Read binary file with np.memmap
arr2=np.memmap(fnout,dtype=np.float32,mode='r',shape=(nn,kk))

print(arr[10:20,99])
print(arr2[10:20,99])

del arr2

##-- Read part of data with 'offset'
nchunk=120
nbyte=4 #<-- float32 = 4byte
offset_unit=kk*nbyte
offset=0 #<-- Starting Point

for nni,nne in memmap_range(nn,nchunk):
    nsize= nne-nni
    small_arr=np.memmap(fnout,dtype=np.float32,mode='r',shape=(nsize,kk),offset=offset)
    small_arr=np.array(small_arr)
    print('i={}, size={}, error={}'.format(nne,nsize,(arr[nni:nne,:]-small_arr).mean()))

    offset+=nsize*offset_unit
