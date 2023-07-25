'''
Matplotlib Application(9)
Cartopy - Remove gap on the dateline (with data from -180 to 180 in longitude)

By Daeho Jin
'''

import sys
import numpy as np
import os.path

import O00_Functions as fns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import cartopy.crs as ccrs
from cartopy.feature import LAND

import cartopy
cartopy_version= float(cartopy.__version__[:4])
print("Cartopy Version= {}".format(cartopy_version))
if cartopy_version < 0.18:
    print("Caution: This code is optimized for Cartopy version 0.18+")

def main():
    ### Read HadISST
    yrs=[2015,2020]
    sst,lats,lons= fns.read_sst_from_HadISST(yrs)

    ##-- Mean for all time
    sstmean1= np.nanmean(sst,axis=0)

    ##-- Lons and Lats of SST map (for contourf())
    xlon= np.arange(lons['nlon'])*lons['dlon']+lons['lon0']
    ylat= np.arange(lats['nlat'])*lats['dlat']+lats['lat0']
    ##-- Grid boundaries for pcolormesh
    xlonb= np.insert(xlon,0,xlon[0]-lons['dlon']) +lons['dlon']/2
    ylatb= np.insert(ylat,0,ylat[0]-lats['dlat']) +lats['dlat']/2

    ###------
    ### Plot
    ###------
    fig=plt.figure()
    fig.set_size_inches(8.5,6)  ## (xsize,ysize)
    suptit= 'Cartopy Projection Example4 - Regional, Removing gap'
    fig.suptitle(suptit,fontsize=17,y=0.98,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    abc= 'abcdefghijklmn'
    nrow,ncol = 2,2

    left,right,top,bottom=0.05,0.93,0.93,0.1
    npnx, gapx= ncol, 0.07
    npny, gapy= nrow, 0.09
    lx=(right-left-gapx*(npnx-1))/float(npnx)
    ly=(top-bottom-gapy*(npny-1))/float(npny)
    ix, iy= left, top

    ###--- Some parameters
    data_crs= ccrs.PlateCarree()

    cm = mpl.colormaps['jet']
    cm.set_under('0.8')
    clevels= np.linspace(0,30,91)
    props_contour= dict(cmap=cm,alpha=0.9,extend='both',transform=data_crs)
    props_pcmesh= dict(cmap=cm,alpha=0.9,transform=data_crs)

    ###--- Map Projection
    map_bound= [140,200,25,65]
    center= [(map_bound[0]+map_bound[1])/2,(map_bound[2]+map_bound[3])/2]
    mproj = ccrs.PlateCarree(central_longitude= center[0])


    ##-- Top Panels for raw data
    ax1=fig.add_axes([ix,iy-ly,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax1.set_extent(map_bound,crs=data_crs)
    pic1= ax1.contourf(xlon,ylat,sstmean1,clevels,**props_contour)
    subtit= '(a) Contourf(raw)'
    map_common(ax1,subtit,data_crs)

    ix=ix+lx+gapx
    ax2= fig.add_axes([ix,iy-ly,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax2.set_extent(map_bound,crs=data_crs)
    pic2= ax2.pcolormesh(xlonb,ylatb,sstmean1,**props_pcmesh)
    subtit= '(b) Pcolormesh(raw)'
    map_common(ax2,subtit,data_crs)

    iy=iy-ly-gapy; ix=left

    ##-- Add pad
    xlon2= np.append(xlon, xlon[-1]*2-xlon[-2])
    sstmean2= np.pad(sstmean1,pad_width=((0,0),(0,1)),mode='wrap')

    ax3=fig.add_axes([ix,iy-ly,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax3.set_extent(map_bound,crs=data_crs)
    pic3= ax3.contourf(xlon2,ylat,sstmean2,clevels,**props_contour)
    subtit= '(c) Contourf(padded)'
    map_common(ax3,subtit,data_crs)

    ix=ix+lx+gapx

    ##-- Swap Eastern and Western part (convert [-180,180] to [0,360])
    neg_lon_idx= xlon<0
    xidx= np.arange(xlon.shape[0],dtype=int)
    new_xidx= np.concatenate((xidx[~neg_lon_idx],xidx[neg_lon_idx]))
    xlon3= xlon[new_xidx]; xlon3[xlon3<0]+=360
    sstmean3= sstmean1[:,new_xidx]

    ax4=fig.add_axes([ix,iy-ly,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax4.set_extent(map_bound,crs=data_crs)
    pic4= ax4.contourf(xlon3,ylat,sstmean3,clevels,**props_contour)
    subtit= '(d) Contourf(swap half and half)'
    map_common(ax4,subtit,data_crs)
    ###--- Add right side y_tick_labes manually
    xloc= map_bound[1]+(map_bound[1]-map_bound[0])*0.02 - center[0]
    if xloc>180: xloc-=360
    ylocs= [30,40,50,60]
    font_kw= dict(fontsize=10,color='k')
    custom_lat_label_right(ax4,xloc,ylocs,**font_kw)

    ##-- Colorbar
    cb= fns.draw_colorbar(fig,ax4,pic1,size='page',type='horizontal',width=0.025,gap=0.08)
    cb.set_ticks(MultipleLocator(5))
    cb.ax.set_xlabel('Temperature (\u00B0C)',fontsize=11)
    cb.ax.tick_params(labelsize=9)

    ### Show or Save
    outdir= '../Pics/'
    outfnm= outdir+'O09.cartopy_projections_regional_ex2.png'
    print(outfnm)
    plt.savefig(outfnm,bbox_inches='tight',dpi=150)
    #plt.savefig(outfnm,dpi=100)
    plt.show()
    return

def map_common(ax1,subtit,data_crs):
    ### Title
    ax1.set_title(subtit,fontsize=13,ha='left',x=0.0)

    ### Fill Land Area
    ax1.add_feature(LAND)

    ### Coast Lines
    ax1.coastlines(resolution='50m',color='0.25',linewidth=1.)

    ### Grid Lines
    prop_gl= dict(linewidth=0.8, color='gray', alpha=0.7, linestyle='--')
    if cartopy_version < 0.18:
        ax1.gridlines(crs=data_crs, **prop_gl)
    else:
        gl=ax1.gridlines(crs=data_crs,draw_labels=True,**prop_gl)
        gl.top_labels= False

    gl.xlabel_style = {'size': 10}
    gl.ylabel_style = {'size': 10}
    gl.xlocator = MultipleLocator(15)
    gl.ylocator = MultipleLocator(10)

    ### Aspect ratio of map
    ax1.set_aspect('auto') ### 'auto' allows the map to be distorted and fill the defined axes
    return

def custom_lat_label_right(ax,xloc,ylocs,**font_kw):
    if isinstance(ylocs,(int,float)):
        ylocs= [ylocs,]
    for yloc in ylocs:
        ax.text(xloc,yloc,fns.lat_formatter(yloc,0),ha='left',va='center',**font_kw)

if __name__ == "__main__":
    main()
