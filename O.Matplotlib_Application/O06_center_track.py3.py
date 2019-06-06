import numpy as np
import sys
import os.path
from subprocess import call
from datetime import timedelta, date, datetime
from netCDF4 import Dataset, date2num


import matplotlib   ### Discover Only
matplotlib.use('TkAgg')   ### Discover Only

import matplotlib.pyplot as plt
import matplotlib.colors as cls
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FixedLocator

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.feature as cfeature
import shapely.geometry as sgeom

from scipy.interpolate import griddata

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


###--- Prepare Data ---###
var= 'slp'
dim_names = ['XLAT','XLONG']
indir = '/home/djin1/Zbegins_Python/Py3_lecture_2019/data/'

start_date = date(2018,2,17)  ### Start Date
end_date = date(2018,2,19)   ### Including this End Date

centers=[]; cdata=[]
for oneday in daterange(start_date,end_date):
    dd=oneday.strftime('%Y-%m-%d')

    for hh in range(0,24,6):
        infn=indir+'{}_wrfout_d01_{}_{:02d}-00-00.nc'.format(var,dd,hh)
        fid=open_netcdf(infn)
        if oneday==start_date and hh==0:
            lats=read_nc_variable(fid,'XLAT').reshape(-1)
            lons=read_nc_variable(fid,'XLONG').reshape(-1)

            from math import floor, ceil
            lat_range=[ceil(lats.min()),floor(lats.max())]
            lon_range=[ceil(lons.min()),floor(lons.max())]
            print(lat_range,lon_range)

#        fids.append(fid)
        data=read_nc_variable(fid,var.upper()).reshape(-1)
        #print(type(data),data.shape,data.argmin())
        k=data.argmin()
        centers.append([lons[k],lats[k],data[k]])

        ##-- Interpolate to 2D grid --##
        grid_x= np.arange(lon_range[0],lon_range[1]+0.01,0.1) # 0.1deg
        grid_y= np.arange(lat_range[0],lat_range[1]+0.01,0.1)
        grid_x,grid_y=np.meshgrid(grid_x,grid_y)
        grid_z= griddata((lons[::17],lats[::17]),data[::17],(grid_x,grid_y),method='cubic',fill_value=-999.)
        cdata.append(grid_z)

        fid.close()

centers=np.asarray(centers).T
print(centers.shape)


###--- Plotting Start ---###

abc='abcdefghijklmn'

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(6,6)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.07,right=0.93,top=0.92,bottom=0.1,hspace=0.35,wspace=0.15)  ### Margins, etc.

##-- Title for the page --##
suptit="Center Track from SLP"
fig.suptitle(suptit,fontsize=15)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')


##-- Set up an axis --##
ax1 = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())   # (# of rows, # of columns, indicater from 1)
ax1.set_extent(lon_range+lat_range)

### Backgroud Image
#ax1.stock_img()
os.environ["CARTOPY_USER_BACKGROUNDS"] = "/home/djin1/Zbegins_Python/Py3_lecture_2019/BGimg/"
ax1.background_img(name='Topo',resolution='high') # BM or Topo available now.

### State line?
# Create a feature for States/Admin 1 regions at 1:110m from Natural Earth
#states_provinces = cfeature.NaturalEarthFeature(
#    category='cultural',
#    name='admin_1_states_provinces_lines',
#    scale='110m',
#    facecolor='none')

ax1.add_feature(cfeature.LAND)
ax1.add_feature(cfeature.COASTLINE)
#ax1.add_feature(states_provinces, edgecolor='gray')


cm=plt.cm.get_cmap('jet_r')
props=dict(marker='x',s=50,cmap=cm,alpha=0.9,norm=cls.Normalize(vmin=965,vmax=990))
X,Y,CC= centers[0,:],centers[1,:],centers[2,:]
for ln,lt,val in zip(X,Y,CC):
    print(ln,lt,val)

pic1=ax1.scatter(X,Y,c=CC,**props)
cb=draw_colorbar(ax1,pic1,type='horizontal',size='panel',extend='both',width=0.03,gap=0.07)
cb.ax.set_xlabel('Pressure (hPa)',size=11)

# turn the lons and lats into a shapely LineString
#track = sgeom.LineString(zip(X, Y))
#ax1.add_geometries([track], ccrs.PlateCarree(),facecolor='none',lw=2.,color='k')

cm=plt.cm.get_cmap('jet_r',250)
cm=cm(np.arange(250))
for i,data in enumerate(cdata):
    cidx= int((CC[i]-965)*10)
    pic2=ax1.contour(grid_x,grid_y,data,[990,],colors=[tuple(cm[cidx,:-1]),],linewidths=1.5)

#subtit='(a) Starndard Bar'
#ax1.set_title(subtit,fontsize=12,x=0.,ha='left')

map_common(ax1,gl_dlon=4,gl_dlat=4) #,gl_loc=[False,True,False,True])
ax1.set_aspect('auto')

##-- Seeing or Saving Pic --##

#- If want to see on screen -#
plt.show()

#- If want to save to file
outdir = "/home/djin1/Zbegins_Python/Py3_lecture_2019/data/Pics/"
outfnm = outdir+"Center_track1.png"
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
sys.exit()
