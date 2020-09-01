'''
Matplotlib Application(9)

Remove gap on the dateline

By Daeho Jin
'''

import sys
import numpy as np
import os.path

import O00_Functions as fns

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import cartopy.crs as ccrs
from cartopy.feature import LAND

def main():
    ### Read HadISST
    yrs=[2015,2019]
    sst,lats,lons= fns.read_sst_from_HadISST(yrs)
    print(sst.shape)
    print(np.isnan(sst).sum()/sst.shape[0])

    ##-- Mean for all time
    sstmean1= np.nanmean(sst,axis=0)
    xlon= np.arange(lons['nlon'])*lons['dlon']+lons['lon0']
    ylat= np.arange(lats['nlat'])*lats['dlat']+lats['lat0']
    ##-- Grid boundaries for pcolormesh
    xlonb= np.insert(xlon,0,xlon[0]-lons['dlon'])+lons['dlon']/2
    ylatb= np.insert(ylat,0,ylat[0]-lats['dlat'])+lats['dlat']/2

    ###------
    ### Plot
    ###------
    fig=plt.figure()
    fig.set_size_inches(8.5,6)  ## (xsize,ysize)
    suptit= 'Cartopy Projection Example4 - Regional'
    fig.suptitle(suptit,fontsize=17,y=0.98,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    abc= 'abcdefg'
    left,right,top,bottom=0.05,0.93,0.925,0.12
    iix=left; gapx=0.02; npnx=2
    lx=(right-iix-gapx*(npnx-1))/float(npnx)
    iiy=top; gapy=0.09; npny=2
    ly=(iiy-bottom-gapy*(npny-1))/float(npny)

    ix=iix; iy=iiy-ly

    cm = plt.cm.get_cmap('jet')
    #cm.set_bad('w') #0.4')
    cm.set_under('0.8')
    clevels= np.linspace(0,30,91)

    ###--- Map Projection
    map_bound= [140,200,25,65]
    center= [(map_bound[0]+map_bound[1])/2,(map_bound[2]+map_bound[3])/2]
    mproj = ccrs.PlateCarree(central_longitude= center[0])
    data_crs= ccrs.PlateCarree()

    props_contour= dict(cmap=cm,alpha=0.9,transform=data_crs,extend='both')
    props_pcmesh= dict(cmap=cm,alpha=0.9,transform=data_crs)

    ##-- Top Panels for raw data
    ax1=fig.add_axes([ix,iy,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax1.set_extent(map_bound,crs=data_crs)
    pic1= ax1.contourf(xlon,ylat,sstmean1,clevels,**props_contour)
    subtit= '(a) Contourf(raw)'
    #ax1.set_title(subtit,fontsize=13,ha='left',x=0.0)
    fns.map_common(ax1,subtit,data_crs,gl_lab_locator=[False,True,True,False],xloc=15,lon_range=map_bound[:2])

    ix=ix+lx+gapx
    ax2= fig.add_axes([ix,iy,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax2.set_extent(map_bound,crs=data_crs)
    pic2= ax2.pcolormesh(xlonb,ylatb,sstmean1,**props_pcmesh)
    subtit= '(b) Pcolormesh(raw)'
    fns.map_common(ax2,subtit,data_crs,gl_lab_locator=[False,True,False,True],xloc=15,lon_range=map_bound[:2])

    iy=iy-ly-gapy; ix=left

    ##-- Add pad
    xlon2= np.concatenate((xlon,[xlon[-1]*2-xlon[-2],]))
    sstmean2= np.pad(sstmean1,pad_width=((0,0),(0,1)),mode='wrap')

    ax3=fig.add_axes([ix,iy,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax3.set_extent(map_bound,crs=data_crs)
    pic3= ax3.contourf(xlon2,ylat,sstmean2,clevels,**props_contour)
    subtit= '(c) Contourf(pad added)'
    fns.map_common(ax3,subtit,data_crs,gl_lab_locator=[False,True,True,False],xloc=15,lon_range=map_bound[:2])

    ix=ix+lx+gapx

    ##-- Swap Eastern and Western part (convert [-180,180] to [0,360])
    nn=xlon.shape[0]
    xidx= np.arange(nn,dtype=int)
    new_xidx= np.concatenate((xidx[nn//2:],xidx[:nn//2]))
    xlon3= xlon[new_xidx]; xlon3[xlon3<0]+=360
    sstmean3= sstmean1[:,new_xidx]

    ax4=fig.add_axes([ix,iy,lx,ly],projection=mproj)  ### Now it's GeoAxes, not just Axes
    ax4.set_extent(map_bound,crs=data_crs)
    pic4= ax4.contourf(xlon3,ylat,sstmean3,clevels,**props_contour)
    subtit= '(d) Contourf(swap half and half)'
    fns.map_common(ax4,subtit,data_crs,gl_lab_locator=[False,True,False,True],xloc=15,lon_range=map_bound[:2])


    ##-- Colorbar
    cb= fns.draw_colorbar(fig,ax4,pic1,size='page',type='horizontal',width=0.025,gap=0.07)
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
    ax1.add_feature(LAND)
    ax1.coastlines(resolution='50m',color='0.25',linewidth=1.)
    gl= ax1.gridlines(crs=data_crs, linewidth=0.8, color='gray', alpha=0.5, linestyle='--')
    gl.xlocator = MultipleLocator(15)
    gl.ylocator = MultipleLocator(10)



if __name__ == "__main__":
    main()
