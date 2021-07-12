'''
Matplotlib Application(11)
Applying background image (Need to check directory for BGimg folder)
Ref: http://earthpy.org/cartopy_backgroung.html

By Daeho Jin
'''

import sys
import numpy as np
import os

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import cartopy.crs as ccrs
from cartopy.feature import LAND, OCEAN

### Coastlines with No data
def main():

    ### Prepare for plotting
    suptit= "Background Image Examples"
    var_names= ['Using np.nan','Using masked_array']

    outdir= '../Pics/'
    out_fig_nm= outdir+'O11.Background_image_ex.png'

    ###--- Plot
    fig=plt.figure()
    fig.set_size_inches(10,6)  ## (xsize,ysize)
    fig.suptitle(suptit,fontsize=18,y=0.97,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    abc= 'abcdefghijklmn'
    nrow,ncol= 2,2
    fig.subplots_adjust(left=0.06,right=0.94,top=0.94,bottom=0.1,wspace=0.25,hspace=0.25) ### Margins, etc.

    mproj = ccrs.PlateCarree()
    data_crs= ccrs.PlateCarree()
    os.environ["CARTOPY_USER_BACKGROUNDS"] = "./BGimg/"

    ##-- Subplot1
    ax1= fig.add_subplot(nrow,ncol,1, projection=mproj)
    subtit= '({}) Default'.format(abc[0])
    map_common(ax1,subtit,data_crs,yloc=30,xloc=60)

    ##-- Subplot2
    ax2= fig.add_subplot(nrow,ncol,2, projection=mproj)
    ax2.add_feature(LAND)
    ax2.add_feature(OCEAN)
    subtit= '({}) Cartopy Features'.format(abc[1])
    map_common(ax2,subtit,data_crs,yloc=30,xloc=60)

    ##-- Subplot3
    ax3= fig.add_subplot(nrow,ncol,3, projection=mproj)
    ax3.background_img(name='Topo',resolution='low')  # BM or Topo available now.
    subtit= '({}) Topographic map (low resol)'.format(abc[2])
    map_common(ax3,subtit,data_crs,yloc=30,xloc=60)

    ##-- Subplot4
    ax4= fig.add_subplot(nrow,ncol,4, projection=mproj)
    ax4.background_img(name='BM',resolution='high')  # BM or Topo available now.
    subtit= '({}) Blue Marble (high resol)'.format(abc[3])
    map_common(ax4,subtit,data_crs,yloc=30,xloc=60)

    ### Show or Save
    outfnm= out_fig_nm
    print(outfnm)
    plt.savefig(outfnm,bbox_inches='tight',dpi=150)
    plt.show()
    return

def map_common(ax,subtit,proj,yloc=10,xloc=30):
    """ Decorating Cartopy Map
    """
    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)
    ### Coast Lines
    ax.coastlines(color='silver',linewidth=0.8,resolution='50m')
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
