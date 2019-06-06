'''
Difference between masked_array and other indexing method
+
Applying backgroudn image (Need to check directory for BGimg folder)
Ref: http://earthpy.org/cartopy_backgroung.html
'''

import sys
import numpy as np
import os.path
from subprocess import call

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

def map_common(ax1,gl_loc=[True,True,False,True],gl_dlon=60,gl_dlat=30):
    ax1.set_title(subtit,x=0.,ha='left',fontsize=13,stretch='semi-condensed')
    ax1.coastlines(color='silver',linewidth=1.)

    gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                       linewidth=0.6, color='gray', alpha=0.5, linestyle='--')

    gl.ylabels_left = gl_loc[0]
    gl.ylabels_right = gl_loc[1]
    gl.xlabels_top = gl_loc[2]
    gl.xlabels_bottom = gl_loc[3]

    gl.xlocator = FixedLocator(range(-180+gl_dlon,361,gl_dlon)) #[0,60,180,240,360]) #np.arange(-180,181,60))
    gl.ylocator = MultipleLocator(gl_dlat)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 11, 'color': 'k'}
    gl.ylabel_style = {'size': 11, 'color': 'k'}

def add_colorbar(cb_ax,cblab,horizontal=True):

    global clmin, clmax
    tt=np.arange(clmin,clmax+1,4)
    #tt2=[str(x)+'%' for x in tt]
    if horizontal:
        cb = fig.colorbar(cs,cax=cb_ax,orientation='horizontal',ticks=tt,extend='both')
        cb.ax.set_xticklabels(tt,size=11)
        cb.ax.set_xlabel(cblab)
    else:
        cb = fig.colorbar(cs,cax=cb_ax,orientation='vertical',ticks=tt,extend='both')
        cb.ax.set_yticklabels(tt,size=11)
        cb.ax.set_ylabel(cblab)

###---- Main

##-- Parameters
indir='./data/'
fname=indir+'HadISST1.sample.348x180x360.f32dat'

nt=348 ### Monthly for 29 years
nlon=360; lon0=0.5; dlon=1.
nlat=180; lat0=-89.5; dlat=1.

undef= -9999.

##-- Read binary file
#sst=bin_file_read2mtx(fname)  ### "dtype=np.float32" is omitted.
#sst=sst.reshape([nt,nlat,nlon])
# If using mmap:
sst=np.memmap(fname,dtype=np.float32,mode='r',shape=(nt,nlat,nlon))
sst=np.array(sst)
print(sst.shape)

###--------

##-- Identify missings
msidx= sst<-100
msidx=msidx.sum(axis=0).astype(bool) ### For identify gridcells having any missings for all time
print(msidx.shape,msidx.sum())

sstmean= sst.mean(axis=0)
sstmean[msidx]=undef
sm_max,sm_min=sstmean[~msidx].max(), sstmean[~msidx].min()
print("Min and Max of Mean SST=",sm_min, sm_max)
##-- Sampling for limited regiosn
lon_deg_range=[-60,30]
lat_deg_range=[40,75]

lon_idx=[lon_deg2x(x,lon0,dlon) for x in lon_deg_range]; nlon2=lon_idx[1]-lon_idx[0]
lat_idx=[lat_deg2y(y,lat0,dlat) for y in lat_deg_range]; nlat2=lat_idx[1]-lat_idx[0]
print(lon_idx, lat_idx)
### In the case of trouble of lon_idx
### lon_idx[1] < lon_idx[0]
### Now need to make lon-list

lon_list=list(range(lon_idx[0],nlon,1))+list(range(lon_idx[1]))
sstmean2=sstmean[lat_idx[0]:lat_idx[1],lon_list]
print(sstmean2.shape)

### The other maskig method
sst_rg=sst[:,lat_idx[0]:lat_idx[1],lon_list]
sst_rg=np.ma.masked_less(sst_rg,-100)
print(type(sst_rg))
sstmean_ma=sst_rg.mean(axis=0)



###--- Map Plot
import matplotlib            ### Discover only
matplotlib.use('TkAgg')      ### Discover only
import matplotlib.colors as cls
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FixedLocator, MultipleLocator

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.feature import LAND

fig=plt.figure()
fig.set_size_inches(8.5,8)  ## (xsize,ysize)
suptit="SST Map"
fig.suptitle(suptit,fontsize=17,y=0.98,stretch='semi-condensed') ## x=0., ha='left'

left,right,top,bottom=0.05,0.95,0.925,0.05
iix=left; gapx=0.02; npnx=2
lx=(right-iix-gapx*(npnx-1))/float(npnx)
iiy=top; gapy=0.12; npny=2
ly=(iiy-bottom-gapy*(npny-1))/float(npny)

lx0=lx*npnx+gapx*(npnx-1)
ix=iix; iy=iiy-ly

cm = plt.cm.get_cmap('nipy_spectral')
cm.set_bad('0.4')
cm.set_under('0.8')

lons_data=np.arange(lon0,360.1,dlon)
lats_data=np.arange(lat0,90.1,dlat)

clmin,clmax= int(sm_min)+1,int(sm_max)+1
clevels= np.linspace(clmin,clmax,51)

##-- Top Panel
ax1=fig.add_axes([ix,iy,lx0,ly],projection=ccrs.PlateCarree(central_longitude=180))  ### Now it's GeoAxes, not just Axes

### Import background image for land area
#ax1.add_feature(LAND)
os.environ["CARTOPY_USER_BACKGROUNDS"] = "/home/djin1/Zbegins_Python/Py3_lecture_2019/BGimg/"
ax1.background_img(name='BM',resolution='high') # BM or Topo available now.

subtit='(a) Global Mean'

props = dict(vmin=clmin,vmax=clmax,cmap=cm,alpha=0.9,transform=ccrs.PlateCarree())
cs=ax1.contourf(lons_data,lats_data,sstmean, clevels,**props)
#cs=ax1.pcolormesh(lons_data,lats_data,sstmean, **props)

map_common(ax1)

ax1.set_aspect('auto')

### Add colorbar
#- Get position from previous subplot
pos1 = ax1.get_position().bounds  ##<= (left,bottom,width,height)
cb_ax = fig.add_axes([pos1[0],pos1[1]-pos1[3]/6.,pos1[2],pos1[3]/15.])  ##<= (left,bottom,width,height)
cblab = "Temperature (\u00B0C)"
add_colorbar(cb_ax,cblab,horizontal=True)



##-- Bottom Panels

lons_data2=np.arange(lon_deg_range[0]+0.5,lon_deg_range[1],dlon)
lats_data2=np.arange(lat_deg_range[0]+0.5,lat_deg_range[1],dlat)

iy=iy-gapy-ly
ax2=fig.add_axes([ix,iy,lx,ly],
                 projection=ccrs.PlateCarree(central_longitude=-15))  ### Now it's GeoAxes, not just Axes
ax2.set_extent([lon_deg_range[0]-10,lon_deg_range[1]+10,lat_deg_range[0]-5,lat_deg_range[1]+5],ccrs.PlateCarree())

ax2.background_img(name='Topo',resolution='high') # BM or Topo available now.

subtit='(b) Masking All missings'

props = dict(vmin=clmin,vmax=clmax,cmap=cm,alpha=0.9,transform=ccrs.PlateCarree())
cs=ax2.pcolormesh(lons_data2,lats_data2,sstmean2, **props)

map_common(ax2,gl_loc=[True,False,False,True],gl_dlon=15,gl_dlat=10)

ax2.set_aspect('auto')

##-- Bottom Right
ix=ix+lx+gapx
ax3=fig.add_axes([ix,iy,lx,ly],
                 projection=ccrs.PlateCarree(central_longitude=-15))  ### Now it's GeoAxes, not just Axes
ax3.set_extent([lon_deg_range[0]-10,lon_deg_range[1]+10,lat_deg_range[0]-5,lat_deg_range[1]+5],ccrs.PlateCarree())

ax3.background_img(name='Topo',resolution='high') # BM or Topo available now.

subtit='(c) Using masked array'

props = dict(vmin=clmin,vmax=clmax,cmap=cm,alpha=0.9,transform=ccrs.PlateCarree())
cs=ax3.pcolormesh(lons_data2,lats_data2,sstmean_ma, **props)

map_common(ax3,gl_loc=[False,True,False,True],gl_dlon=15,gl_dlat=10)

#ax3.set_aspect('auto')

###--- Save Fig
outdir = "/discover/nobackup/djin1/Scratch/Py3_lecture_2019_Pics/"
fnout = "sst_map_ex1.png"

### Show or Save
plt.show()
#plt.savefig(outdir+fnout,bbox_inches='tight',dpi=175)
#plt.savefig(outdir+fnout,dpi=160)

if os.path.isfile(outdir+fnout) and not os.path.isfile('./Pics/'+fnout):
    call(["ln","-s",outdir+fnout,"./Pics/"])
