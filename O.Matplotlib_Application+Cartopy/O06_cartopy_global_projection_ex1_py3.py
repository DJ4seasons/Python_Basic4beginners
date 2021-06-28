'''
Matplotlib Application(6)
Apply various map projection, global maps

PlateCarree
LambertCylindrical
Mollweide
Robinson
---
Orthographic
Geostationary
NorthPolarStereo
SouthPolarStereo

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

import cartopy
cartopy_version= float(cartopy.__version__[:4])
print("Cartopy Version= {}".format(cartopy_version))

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

    ###------
    ### Plot
    ###------
    fig=plt.figure()
    fig.set_size_inches(8.5,6)  ## (xsize,ysize)
    suptit= 'Cartopy Projection Example1 - Global'
    fig.suptitle(suptit,fontsize=17,y=0.98,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    abc= 'abcdefg'
    left,right,top,bottom=0.05,0.95,0.925,0.12
    iix=left; gapx=0.12; npnx=2
    lx=(right-iix-gapx*(npnx-1))/float(npnx)
    iiy=top; gapy=0.09; npny=2
    ly=(iiy-bottom-gapy*(npny-1))/float(npny)

    ix=iix; iy=iiy-ly

    cm = plt.cm.get_cmap('jet')
    #cm.set_bad('w') #0.4')
    cm.set_under('0.8')
    clevels= np.linspace(0,30,91)

    ###--- Map Projection
    center= 180  # Want to draw a map where dateline is on the center
    proj_nms= ['PlateCarree', 'LambertCylindrical', 'Mollweide', 'Robinson']
    projs = [ccrs.PlateCarree(central_longitude=center),
            ccrs.LambertCylindrical(central_longitude=center),
            ccrs.Mollweide(central_longitude=center),
            ccrs.Robinson(central_longitude=center)]
    data_crs= ccrs.PlateCarree()

    props_contour= dict(cmap=cm,alpha=0.9,transform=data_crs,extend='both')
    #if
    ##-- Top Panel
    for i in range(npnx*npny):
        ax1=fig.add_axes([ix,iy,lx,ly],projection=projs[i])  ### Now it's GeoAxes, not just Axes
        pic1= ax1.contourf(xlon,ylat,sstmean1,clevels,**props_contour)
        subtit= '({}) {}'.format(abc[i],proj_nms[i])
        ax1.set_title(subtit,fontsize=13,ha='left',x=0.0)
        ax1.add_feature(LAND)
        ax1.coastlines(resolution='110m',color='0.25',linewidth=1.)
        prop_gl= dict(linewidth=0.8, color='gray', alpha=0.7, linestyle='--')
        if cartopy_version < 0.18:
            ax1.gridlines(crs=data_crs, **prop_gl)
        else:
            gl=ax1.gridlines(crs=data_crs,draw_labels=True,**prop_gl)
            gl.top_labels, gl.right_labels= False, False

        gl.xlocator = MultipleLocator(60)
        gl.ylocator = MultipleLocator(30)
        ix=ix+lx+gapx
        if ix+lx>1:
            iy=iy-ly-gapy; ix=left

    cb= fns.draw_colorbar(fig,ax1,pic1,size='page',type='horizontal',width=0.025,gap=0.07)
    cb.set_ticks(MultipleLocator(5))
    cb.ax.set_xlabel('Temperature (\u00B0C)',fontsize=11)
    cb.ax.tick_params(labelsize=9)

    ### Show or Save
    outdir= '../Pics/'
    outfnm= outdir+'O06.cartopy_global_projections_part1.png'
    print(outfnm)
    plt.savefig(outfnm,bbox_inches='tight',dpi=150)
    #plt.savefig(outfnm,dpi=100)
    plt.show()
    return

if __name__ == "__main__":
    main()
