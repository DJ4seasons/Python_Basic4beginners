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

from math import ceil
def lon_deg2x(lon,lon0,dlon):
    x=ceil((lon-lon0)/dlon)
    if lon0<0 and lon>180:
        x-= int(360/dlon)
    if lon0>0 and lon<0:
        x+= int(360/dlon)

    return x
lat_deg2y = lambda lat,lat0,dlat: ceil((lat-lat0)/dlat)

###---- Main

##-- Parameters
indir='./data/'
fname=indir+'HadISST1.sample.348x180x360.f32dat'

nt=348 ### Monthly for 29 years
nlon=360; lon0=0.5; dlon=1.
nlat=180; lat0=-89.5; dlat=1.

undef= -9999.

##-- Read binary file
sst=bin_file_read2mtx(fname)  ### "dtype=np.float32" is omitted. 
sst=sst.reshape([nt,nlat,nlon])
print(sst.shape)

###--------

##-- Sampling for limited regiosn (60E-160E,25S-25N)
lon_deg_range=[60,160]
lat_deg_range=[-25,25]

lon_idx=[lon_deg2x(x,lon0,dlon) for x in lon_deg_range]; nlon2=lon_idx[1]-lon_idx[0]
lat_idx=[lat_deg2y(y,lat0,dlat) for y in lat_deg_range]; nlat2=lat_idx[1]-lat_idx[0]
print(lon_idx, lat_idx)
sst=sst[:,lat_idx[0]:lat_idx[1],lon_idx[0]:lon_idx[1]]
print(sst.shape)

##-- Identify missings
msidx= sst<-100
msidx=msidx.sum(axis=0).astype(bool) ### For identify gridcells having any missings for all time
print(msidx.shape,msidx.sum())

##-- Remove annual cycle
#- 1. Calc annual cycle
anncyl= sst.reshape([-1,12,nlat2,nlon2]).mean(axis=0)
print(anncyl.shape)

#- 2. Calc anomalies
sstano= sst.reshape([-1,12,nlat2,nlon2])-anncyl[None,:,:,:]
sstano= sstano.reshape([nt,nlat2,nlon2])

##-- Calc Root-Mean-Squared-Sum of anomalies
rms= np.sqrt(np.mean(sstano*sstano,axis=0))
print(rms[~msidx].max(), rms[~msidx].min())

##-- Restore missings
rms[msidx]=undef

###----------

##-- Write to binary file
outdir=indir
outfn=outdir+'HadSST_rms.{}x{}.f32dat'.format(nlat2,nlon2)

##-- Protect existing file
if os.path.isfile(outfn):
    sys.exit("Already Exist: "+outfn)
else: 
    with open(outfn, 'wb') as f:
        rms.astype(np.float32).tofile(f)
