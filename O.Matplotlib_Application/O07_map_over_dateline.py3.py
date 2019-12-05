import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.ticker import AutoMinorLocator, FixedLocator, MultipleLocator

def map_common(ax1,gl_loc=[True,True,False,True],gl_lon_info=range(-180,180,60),gl_dlat=30):

    ax1.coastlines(color='silver',linewidth=1.)

    gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                       linewidth=0.6, color='gray', alpha=0.5, linestyle='--')

    gl.ylabels_left = gl_loc[0]
    gl.ylabels_right = gl_loc[1]
    gl.xlabels_top = gl_loc[2]
    gl.xlabels_bottom = gl_loc[3]

    gl.xlocator = FixedLocator(gl_lon_info)
    gl.ylocator = MultipleLocator(gl_dlat)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 11, 'color': 'k'}
    gl.ylabel_style = {'size': 11, 'color': 'k'}


lon_boundary=np.arange(-240,-60,1.)
lat_boundary=np.arange(15,75,1.)
data=np.ones([lat_boundary.shape[0]-1,lon_boundary.shape[0]-1]) ## Data dimension is 1 less than boundaries
data=data*lat_boundary[:-1,None]

lon_offset=-150  ##
x,y=np.meshgrid(lon_boundary-lon_offset,lat_boundary)

fig=plt.figure()
fig.set_size_inches(7.5,5) ## (xsize, ysize)
ax1=fig.add_subplot(111,projection=ccrs.PlateCarree(central_longitude=lon_offset))
ax1.set_extent([-250,-50,10,80],crs=ccrs.PlateCarree())

props=dict(vmin=0,vmax=90,cmap=plt.cm.get_cmap('bone'),alpha=0.8)
cs=ax1.pcolormesh(x,y,data,**props)
ax1.set_title('Lon_Offset={}'.format(lon_offset))
map_common(ax1,gl_lon_info=[-180,-120,-60,120,],gl_dlat=15)

fnout='./O07_map_over_dateline.png'
#plt.show()
plt.savefig(fnout,bbox_inches='tight',dpi=150)
