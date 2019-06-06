'''
Interpolation into grid
'''

import numpy as np
import sys
import os.path
from subprocess import call
from datetime import timedelta, date, datetime
from netCDF4 import Dataset, date2num


import matplotlib   ### Discover Only
matplotlib.use('TkAgg')   ### Discover Only

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FixedLocator, MultipleLocator

def open_netcdf(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    fid=Dataset(fname,'r')
    print("Open:",fname)
    return fid

def daterange(start_date, end_date):
    ### Including end date
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def read_nc_variable(fid,var_name):
    vdata=fid.variables[var_name][:]
    if vdata.shape[0]==1:
        vdata=vdata.reshape(vdata.shape[1:])
    return vdata


###--- Prepare Data ---###
var= 'slp'
dim_names = ['XLAT','XLONG']
indir = '/home/djin1/Zbegins_Python/Py3_lecture_2019/data/'

tgt_date = date(2018,2,18)  ### Target Date

dd=tgt_date.strftime('%Y-%m-%d')
infn=indir+'{}_wrfout_d01_{}_12-00-00.nc'.format(var,dd)
fid=open_netcdf(infn)

lats=read_nc_variable(fid,'XLAT')[::5,::5].reshape(-1)
lons=read_nc_variable(fid,'XLONG')[::5,::5].reshape(-1)
data=read_nc_variable(fid,var.upper())[::5,::5].reshape(-1)

from math import floor, ceil
lat_range=[ceil(lats.min()),floor(lats.max())]
lon_range=[ceil(lons.min()),floor(lons.max())]
print(lat_range,lon_range)

##-- Interpolate to 2D grid --##
from scipy.interpolate import griddata

grid_x= np.arange(lon_range[0],lon_range[1]+0.01,0.1) # 0.1deg
grid_y= np.arange(lat_range[0],lat_range[1]+0.01,0.1)
grid_x,grid_y=np.meshgrid(grid_x,grid_y)
grid_z= griddata((lons,lats),data,(grid_x,grid_y),method='cubic',fill_value=-999.)
print(grid_x.shape,grid_y.shape,grid_z.shape) #;sys.exit()


###--- Plotting Start ---###

def draw_colorbar(ax,pic1,type='vertical',size='panel',gap=0.06,width=0.02,extend='neither'):
    '''
    Type: 'horizontal' or 'vertical'
    Size: 'page' or 'panel'
    Gap: gap between panel(axis) and colorbar
    Extend: 'both', 'min', 'max', 'neither'
    '''
    pos1=ax.get_position().bounds  ##<= (left,bottom,width,height)
    if type.lower()=='vertical' and size.lower()=='page':
        cb_ax =fig.add_axes([pos1[0]+pos1[2]+gap,0.1,width,0.8])  ##<= (left,bottom,width,height)
    elif type.lower()=='vertical' and size.lower()=='panel':
        cb_ax =fig.add_axes([pos1[0]+pos1[2]+gap,pos1[1],width,pos1[3]])  ##<= (left,bottom,width,height)
    elif type.lower()=='horizontal' and size.lower()=='page':
        cb_ax =fig.add_axes([0.1,pos1[1]-gap,0.8,width])  ##<= (left,bottom,width,height)
    elif type.lower()=='horizontal' and size.lower()=='panel':
        cb_ax =fig.add_axes([pos1[0],pos1[1]-gap,pos1[2],width])  ##<= (left,bottom,width,height)
    else:
        print('Error: Options are incorrect:',type,size)
        return

    cbar=fig.colorbar(pic1,cax=cb_ax,extend=extend,orientation=type)  #,ticks=[0.01,0.1,1],format='%.2f')
    cbar.ax.tick_params(labelsize=10)
    return cbar


##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(7.2,6)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.06,hspace=0.3,wspace=0.1)  ### Margins, etc.

##-- Title for the page --##
suptit="SLP Bar Plot"
fig.suptitle(suptit,fontsize=15,y=1.0)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

abc='abcdefghijklmn'
cm = plt.cm.get_cmap('CMRmap')

##-- Set up an axis --##
ax1 = fig.add_subplot(2,2,1)   # (# of rows, # of columns, indicater from 1)

pic1 = ax1.scatter(lons,lats,c=data,s=3,marker='o',alpha=0.9,cmap=cm)

subtit='(a) SLP scatter'
ax1.set_title(subtit,fontsize=12,x=0.,ha='left')
ax1.set_xlim(lon_range)
ax1.set_ylim(lat_range)

##-- Set up an axis --##
ax2 = fig.add_subplot(2,2,2)   # (# of rows, # of columns, indicater from 1)

X,Y=np.meshgrid(np.arange(lon_range[0]-0.05,lon_range[1]+0.06,0.1),np.arange(lat_range[0]-0.05,lat_range[1]+0.06,0.1))
props = dict(edgecolor='none',alpha=0.8,vmin=975,vmax=1010,cmap=cm)
pic2 = ax2.pcolormesh(X,Y,grid_z,**props)

subtit='(b) SLP gridded'
ax2.set_title(subtit,fontsize=12,x=0.,ha='left')
ax2.set_xlim(lon_range)
ax2.set_ylim(lat_range)
ax2.yaxis.tick_right()

###--- On Map ---###
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def map_common(ax1,gl_loc=[True,True,False,True],gl_dlon=60,gl_dlat=30):
    #ax1.set_title(subtit,x=0.,ha='left',fontsize=13,stretch='semi-condensed')
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

##-- Set up an axis --##
ax3 = fig.add_subplot(2,2,3,projection=ccrs.PlateCarree())   # (# of rows, # of columns, indicater from 1)

pic3 = ax3.scatter(lons,lats,c=data,s=3,marker='o',alpha=0.9,cmap=cm)

subtit='(c) SLP scatter on Map'
ax3.set_title(subtit,fontsize=12,x=0.,ha='left')
#ax3.set_xlim(lon_range)
#ax3.set_ylim(lat_range)
map_common(ax3,gl_dlon=4,gl_dlat=4,gl_loc=[True,False,False,True])
cb=draw_colorbar(ax3,pic3,type='horizontal',size='page')


##-- Set up an axis --##
ax4 = fig.add_subplot(2,2,4,projection=ccrs.PlateCarree())   # (# of rows, # of columns, indicater from 1)

X,Y=np.meshgrid(np.arange(lon_range[0]-0.05,lon_range[1]+0.06,0.1),np.arange(lat_range[0]-0.05,lat_range[1]+0.06,0.1))
props = dict(edgecolor='none',alpha=0.8,vmin=975,vmax=1010,cmap=cm)
pic4 = ax4.pcolormesh(X,Y,grid_z,**props)

subtit='(b) SLP gridded'
ax4.set_title(subtit,fontsize=12,x=0.,ha='left')
#ax4.set_xlim(lon_range)
#ax4.set_ylim(lat_range)

map_common(ax4,gl_dlon=4,gl_dlat=4,gl_loc=[False,True,False,True])
ax4.set_aspect('auto')
##-- Seeing or Saving Pic --##

#- If want to see on screen -#
plt.show()

#- If want to save to file
outdir = "/home/djin1/Zbegins_Python/Py3_lecture_2019/data/Pics/"
outfnm = outdir+"SLP_Scatter+pcolormesh.png"
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
