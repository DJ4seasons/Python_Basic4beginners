"""
Matplotlib Application(10)
Draw maps of satellite Level2 data

PlateCarree
Orthographic

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
import O00_Functions as fns

from pyhdf.SD import SD, SDC
def open_hdf4(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    hid=SD(fname, SDC.READ)
    print("Open:",fname)
    return hid

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
        print(var_names[i],d.shape,np.nanmin(d),np.nanmax(d),ms_idx.sum())

    ##-- Info for a plot
    suptit= 'MODIS Level-2 {}'.format(var_names[2])
    outdir= '../Pics/'
    out_fig_nm= outdir+'O10_MYD04_L2.A2019001.0420.{}_onMap.png'.format(var_names[2])
    plot_data= dict(latlon= data[:2], data=data[2], var_name=var_names[2],
                    suptit= suptit, out_fnm=out_fig_nm)
    plot_map(plot_data)

    return

###---
### Show MYD04_L2 data on map
###---
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import cartopy.crs as ccrs

def plot_map(pdata):

    fig=plt.figure()
    fig.set_size_inches(8.5,4.5)  ## (xsize,ysize)
    fig.suptitle(pdata['suptit'],fontsize=17,y=0.97,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    abc= 'abcdefghijklmn'
    nrow,ncol= 1,2
    fig.subplots_adjust(left=0.06,right=0.94,top=0.95,bottom=0.1,wspace=0.25) #,hspace=0.3 ### Margins, etc.

    data_crs= ccrs.PlateCarree()
    cm = mpl.colormaps['magma_r']

    ###--- Check range of map
    lats,lons= pdata['latlon']
    lat_min, lat_max= np.nanmin(lats),np.nanmax(lats)
    lon_min, lon_max= np.nanmin(lons),np.nanmax(lons)
    center= [(lat_min+lat_max)/2, (lon_min+lon_max)/2]

    lat_space, lon_space= (lat_max-lat_min)*0.05, (lon_max-lon_min)*0.05  # 5% extention of map area
    extent_range= [lon_min-lon_space, lon_max+lon_space, lat_min-lat_space, lat_max+lat_space]

    #val_min, val_max= np.nanmin(plot_data['data'][2]),np.nanmax(plot_data['data'][2])
    val_min, val_max= np.nanpercentile(pdata['data'][2],[5,95])

    ###--- Map Projection
    proj_nms= ['PlateCarree','Orthographic',]
    mprojs = [ccrs.PlateCarree(central_longitude= center[1]),
            ccrs.Orthographic(central_longitude= center[1],central_latitude= center[0]),
            ]

    sct_props0= dict( marker='s',s=1,alpha=0.7,transform=data_crs)
    sct_props1= sct_props0.copy()
    sct_props1.update(dict(vmin=val_min, vmax=val_max,cmap=cm))

    ###--- Plot
    for i,(proj,proj_name) in enumerate(zip(mprojs,proj_nms)):
        ax1= fig.add_subplot(nrow,ncol,i+1,projection=proj)

        ax1.set_extent(extent_range,crs=data_crs)
        map1= ax1.scatter(lons,lats,c=pdata['data'],**sct_props1)

        ### If want to add missing points
        ms_idx= np.isnan(pdata['data'])
        map2= ax1.scatter(lons[ms_idx],lats[ms_idx],c='0.85',**sct_props0)

        subtit= '({}) {}'.format(abc[i],proj_name)
        map_common(ax1,subtit,data_crs,xloc=5,yloc=5)

    cb= fns.draw_colorbar(fig,ax1,map1,type='horizontal',size='page',gap=0.12,width=0.03,extend='both')

    #- If want to save to file
    outfnm = pdata['out_fnm']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
    # Defalut: facecolor='w', edgecolor='w', transparent=False

    ##-- Seeing or Saving Pic --##
    plt.show()

    return

def map_common(ax,subtit,proj,yloc=10,xloc=30):
    """ Decorating Cartopy Map
    """
    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)
    ### Coast Lines
    ax.coastlines(color='silver',linewidth=1.,resolution='50m')
    ### Grid Lines
    gl= ax.gridlines(crs=proj, draw_labels=True,
                    linewidth=0.6, color='gray', alpha=0.5, linestyle='--')

    ### x and y-axis tick labels
    gl.top_labels= False
    gl.xlocator = MultipleLocator(xloc)
    gl.ylocator = MultipleLocator(yloc)
    gl.xlabel_style = {'size': 10, 'color': 'k'}
    gl.ylabel_style = {'size': 10, 'color': 'k'}
    ### Aspect ratio of map
    #ax.set_aspect('auto') ### 'auto' allows the map to be distorted and fill the defined axes
    return

if __name__ == "__main__":
    main()
