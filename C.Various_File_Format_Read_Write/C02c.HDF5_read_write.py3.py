"""
Read HDF5 file and write a few variables to a new hdf5 file

"""


import sys
import numpy as np
import os.path


import h5py

def open_hdf5(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=h5py.File(fname,'r')
    print("Open:",fname)
    return hid


def hdf_key_test(f,key1):
    if key1 not in list(f.keys()):
        print(list(f.keys()))
        sys.exit('Key name is not matched: {}'.format(key1))
    else:
        print('key is available')


##-- Parameters
indir='./data/'
#fname=indir+'3B-HHR.MS.MRG.3IMERG.20180218-S000000-E002959.0000.V06A.HDF5'
fname=indir+'AERDB_L2_VIIRS_SNPP.A2014067.1936.001.2019056041229.nc'

h5keys=['Longitude','Latitude','Aerosol_Optical_Thickness_550_Land_Ocean','Spectral_Aerosol_Optical_Thickness_Land']

undef = -999.

## Open file and test keys
hdf_f = open_hdf5(fname)
for key in h5keys:
    hdf_key_test(hdf_f,key)

## Read data
lons=hdf_f[h5keys[0]]  ## h5py data array
lats=hdf_f[h5keys[1]][:]  ## Now numpy array
aot550lo=hdf_f[h5keys[2]][:]
saotl=hdf_f[h5keys[3]][:]

print(type(lons),type(lats))
print(lons.shape,lats.shape,aot550lo.shape,saotl.shape)

lons=lons[:]
hdf_f.close()

udidx= aot550lo==undef
print("Missing rate of {} = {:.2f}%".format(h5keys[2],udidx.sum()/aot550lo.reshape(-1).shape[0]*100.))

for k in range(saotl.shape[0]):
    idx= saotl[k,:,:]==undef
    
    iidx= np.logical_and(idx,udidx)
    print(idx.sum(),udidx.sum(),iidx.sum())

    saotl[k,~iidx]=undef

### Write
outdir = indir
outfn = outdir+'AERDB_temp.hdf5'
with h5py.File(outfn, 'w') as f:
    dset1 = f.create_dataset("lon",data=lons)
    dset2 = f.create_dataset("lat",data=lats)
    dset3 = f.create_dataset("Screened_"+h5keys[3], data=saotl, dtype='f4')

    f["lon"].dims[0].label='lon'
    f["lon"].dims[1].label='lat'

    f["lat"].dims[0].label='lon'
    f["lat"].dims[1].label='lat'

    f["Screened_"+h5keys[3]].dims[0].label='bands(412, 488, 670)'
    f["Screened_"+h5keys[3]].dims[1].label='lon'
#    f["Screened_"+h5keys[3]].dims[2].label='lat'
    dset3.dims[2].label='lat'
    dset3.attrs['_FillValue']=undef

