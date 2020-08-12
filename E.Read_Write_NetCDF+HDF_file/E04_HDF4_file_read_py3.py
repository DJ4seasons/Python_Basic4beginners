"""
Open HDF4 file and draw a map of data

---
MYD04_L2 (Aqua Level2 Aerosol data)
DOI: Levy, R., Hsu, C., et al., 2015. MODIS Atmosphere L2 Aerosol Product. NASA MODIS Adaptive Processing System, Goddard Space Flight Center, USA:
http://dx.doi.org/10.5067/MODIS/MYD04_L2.006 (Aqua)

MODIS Aerosol Data Products can be found at the LAADS Web website.

Daeho Jin
"""

import sys
import os.path
import numpy as np

#from pyhdf.SD import SD, SDC
'''
def open_hdf4(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=SD(fname, SDC.READ)
    print("Open:",fname)
    return hid
'''

from E03_HDF4_file_header_info_py3 import open_hdf4

def main():
    ##-- Parameters
    indir='../Data/'
    #fname=indir+'3B42.20180218.00.7.HDF'
    fname= indir+'MYD04_L2.A2019001.0420.061.2019001165304.hdf'

    var_names= ['Latitude','Longitude', 'Optical_Depth_Land_And_Ocean']

    ##-- Open hdf4 file
    hdf_f = open_hdf4(fname)

    ##-- Read data
    data= [hdf_f.select(vn).get() for vn in var_names]
    attr= [hdf_f.select(vn).attributes() for vn in var_names]

    hdf_f.end()  # Close hdf4 file
    print(type(data[0]), data[0].shape)
    print(data[2].min(),data[2].max())
    for i,(d,a) in enumerate(zip(data,attr)):
        ms_idx= d==a['_FillValue']
        d= d.astype(float)
        d[ms_idx]= np.nan
        d= (d-a['add_offset'])*a['scale_factor']
        data[i]=d
        print(var_names[i],np.nanmin(d),np.nanmax(d),ms_idx.sum())

    outdir= '../Pics'
    out_fig_nm= outdir+'E04_MYD04_L2.A2019001.0420.{}.png'.format(var_names[2])
    plot_data= dict(data=data, var_names=var_names, out_fnm=out_fig_nm)
    plot_map(plot_data)

    return

###---
### Show MYD04_L2 data on map
###---
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def plot_map(plot_data):

    fig=plt.figure()
    fig.set_size_inches(7,6)  ## (xsize,ysize)

    ###--- Map Projection
    #proj = ccrs.PlateCarree()


    ###--- Check range of map
    lat_min, lat_max= np.nanmin(plot_data['data'][0]),np.nanmax(plot_data['data'][0])
    lon_min, lon_max= np.nanmin(plot_data['data'][1]),np.nanmax(plot_data['data'][1])
    proj= ccrs.Orthographic(central_longitude=(lon_min+lon_max)/2, central_latitude=(lat_min+lat_max)/2)

    #val_min, val_max= np.nanmin(plot_data['data'][2]),np.nanmax(plot_data['data'][2])
    val_min, val_max= np.nanpercentile(plot_data['data'][2],[5,95])

    lat_space, lon_space= (lat_max-lat_min)*0.05, (lon_max-lon_min)*0.05  # 5% extention of map area
    extent_range= [lon_min-lon_space, lon_max+lon_space, lat_min-lat_space, lat_max+lat_space]

    ###--- Color map
    cm = plt.cm.get_cmap('magma_r')
    cm.set_bad('0.85')  # <-- Not working in scatter plot

    ax1= fig.add_subplot(111,projection=proj)
    ax1.set_extent(extent_range)
    props= dict(vmin=val_min, vmax=val_max, marker='s',s=1,
                alpha=0.7,cmap=cm,transform=ccrs.PlateCarree())
    map1= ax1.scatter(plot_data['data'][1],plot_data['data'][0],c=plot_data['data'][2],**props)

    ### If want to add missing points
    ms_idx= np.isnan(plot_data['data'][2])
    map2= ax1.scatter(plot_data['data'][1][ms_idx],plot_data['data'][0][ms_idx],c='0.85',**props)

    subtit= plot_data['var_names'][2]
    map_common(ax1,subtit,ccrs.PlateCarree(),xloc=5,yloc=5)
    draw_colorbar(fig,ax1,map1,type='horizontal',size='panel',gap=0.08,width=0.03,extend='both')

    ##-- Seeing or Saving Pic --##
    plt.show()

    #- If want to save to file
    outfnm = plot_data['out_fnm']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    #fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

    # Defalut: facecolor='w', edgecolor='w', transparent=False
    return

def map_common(ax,subtit,proj,gl_lab_locator=[False,True,True,False],yloc=10,xloc=30):
    """ Decorating Cartopy Map
    """
    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)
    ### Coast Lines
    ax.coastlines(color='silver',linewidth=1.,resolution='50m')
    ### Grid Lines
    gl= ax.gridlines(crs=proj, draw_labels=False,
                    linewidth=0.6, color='gray', alpha=0.5, linestyle='--')

    ### x and y-axis tick labels
    #gl.xlabels_top,gl.xlabels_bottom,gl.ylabels_left,gl.ylabels_right = gl_lab_locator
    #gl.xlocator = MultipleLocator(xloc)
    #gl.ylocator = MultipleLocator(yloc)
    #gl.xformatter = LONGITUDE_FORMATTER
    #gl.yformatter = LATITUDE_FORMATTER
    #gl.xlabel_style = {'size': 10, 'color': 'k'}
    #gl.ylabel_style = {'size': 10, 'color': 'k'}
    ### Aspect ratio of map
    #ax.set_aspect('auto') ### 'auto' allows the map to be distorted and fill the defined axes
    return

def draw_colorbar(fig,ax,pic1,type='vertical',size='panel',gap=0.06,width=0.02,extend='neither'):
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

if __name__ == "__main__":
    main()
