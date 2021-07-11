'''
Matplotlib Application(7)
Apply various map projections of Cartopy

Part1: Global maps (continue)
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
    print(xlon[0], xlon[-1], ylat[0], ylat[-1])
    X,Y= np.meshgrid(xlon,ylat)  # For pcolormesh(shading='nearest')

    ###------
    ### Plot
    ###------
    fig=plt.figure()
    fig.set_size_inches(7.5,9)  ## (xsize,ysize)
    suptit= 'Cartopy Projection Example2 - Semi-Global'
    fig.suptitle(suptit,fontsize=17,y=0.98,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    abc= 'abcdefghijklmn'
    nrow,ncol = 4,2

    left,right,top,bottom=0.05,0.95,0.92,0.1
    npnx, gapx= ncol, 0.12
    npny, gapy= nrow, 0.08
    lx=(right-left-gapx*(npnx-1))/float(npnx)
    ly=(top-bottom-gapy*(npny-1))/float(npny)
    ix, iy= left, top

    ###--- Some parameters
    centers= [0,180]  # Central longitude of a map
    proj_nms= ['Orthographic(ctr_lat=30)','NearsidePerspective(ctr_lat=30)',
                'NorthPolarStereo','SouthPolarStereo']
    data_crs= ccrs.PlateCarree()

    cm = plt.cm.get_cmap('jet').copy()
    cm.set_under('0.8')
    clevels= np.linspace(0,32,65)
    props_contour= dict(cmap=cm,alpha=0.9,extend='both',transform=data_crs)
    props_pcm= dict(cmap=cm,alpha=0.9,shading='nearest',
                    vmin=0,vmax=32,transform=data_crs)

    for i, center in enumerate(centers):
        projs = [ccrs.Orthographic(central_longitude=center,central_latitude=30),
                ccrs.NearsidePerspective(central_longitude=center,central_latitude=30),
                ccrs.NorthPolarStereo(central_longitude=center),
                ccrs.SouthPolarStereo(central_longitude=center)]

        for j, (proj_name, map_proj) in enumerate(zip(proj_nms, projs)):
            ax1=fig.add_axes([ix,iy-ly,lx,ly],projection=map_proj)  ### Now it's GeoAxes, not just Axes
            #pic1= ax1.contourf(xlon,ylat,sstmean1,clevels,**props_contour)  # Error with Orthographic
            pic1= ax1.pcolormesh(X,Y,sstmean1,**props_pcm)

            if proj_name=='NorthPolarStereo':
                ax1.set_extent([-180,179.9,0,90],crs=data_crs)
            elif proj_name=='SouthPolarStereo':
                ax1.set_extent([-180,179.9,-90,0],crs=data_crs)

            subtit= '({}) {}'.format(abc[j*2+i],proj_name)
            if center != 0: subtit+= '(ctr_lon={})'.format(center)
            ax1.set_title(subtit,fontsize=13,stretch='condensed')
            
            ax1.add_feature(LAND)
            ax1.coastlines(resolution='110m',color='0.25',linewidth=1.)
            prop_gl= dict(linewidth=0.8, color='gray', alpha=0.7, linestyle='--')
            if cartopy_version < 0.18:
                ax1.gridlines(crs=data_crs, **prop_gl)
            else:
                gl=ax1.gridlines(crs=data_crs,draw_labels=True,**prop_gl)
                gl.top_labels= False

            gl.xlocator = MultipleLocator(60)
            gl.ylocator = MultipleLocator(30)

            iy=iy-ly-gapy

        ix= ix+lx+gapx
        iy= top

    cb= fns.draw_colorbar(fig,ax1,pic1,size='page',type='horizontal',extend='both',width=0.02,gap=0.07)
    cb.set_ticks(MultipleLocator(5))
    cb.ax.set_xlabel('Temperature (\u00B0C)',fontsize=11)
    cb.ax.tick_params(labelsize=9)

    ### Show or Save
    outdir= '../Pics/'
    outfnm= outdir+'O07.cartopy_global_projections_part2.png'
    print(outfnm)
    plt.savefig(outfnm,bbox_inches='tight',dpi=150)
    #plt.savefig(outfnm,dpi=100)
    plt.show()
    return

if __name__ == "__main__":
    main()
