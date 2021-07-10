'''
Matplotlib Application(5)
Difference between masked_array and other indexing method
+
Applying background image (Need to check directory for BGimg folder)
Ref: http://earthpy.org/cartopy_backgroung.html

By Daeho Jin
'''

import sys
import numpy as np
import os.path

import O00_Functions as fns

def main():
    ### Read HadISST
    yrs=[2015,2020]
    sst,lats,lons= fns.read_sst_from_HadISST(yrs)

    ##-- Sampling for limited regiosn
    lon_deg_range=[-60,30]
    lat_deg_range=[45,80]

    latlons= dict(latinfo=(lats['lat0'],lats['dlat'],lats['nlat']),
                    loninfo=(lons['lon0'],lons['dlon'],lons['nlon']))
    lat_idx, lon_ids = fns.get_tgt_latlon_idx(latlons, lat_deg_range, lon_deg_range)

    sst= sst[:,lat_idx[0]:lat_idx[1],lon_ids]
    print(sst.shape)
    print(np.isnan(sst).sum()/sst.shape[0])

    ##-- Masked array counterpart
    sst_masked= np.ma.masked_invalid(sst)

    ##-- Mean for all time
    sstmean1= sst.mean(axis=0)
    sstmean2= sst_masked.mean(axis=0)

    ##-- Map info for displaying
    lon0, dlon= lons['lon0'], lons['dlon']
    lat0, dlat= lats['lat0'], lats['dlat']
    lat_bound= [lat_idx[0]*dlat+lat0-dlat/2,lat_idx[1]*dlat+lat0-dlat/2]
    if lon_idx[0]<lon_idx[1]:
        img_bound= [lon_idx[0]*dlon+lon0-dlon/2,lon_idx[1]*dlon+lon0-dlon/2]+lat_bound  # Exact range of data, necessary for imshow()
    else:
        img_bound= [lon_idx[0]*dlon+lon0-dlon/2,lon_idx[1]*dlon+lon0-dlon/2+360]+lat_bound  # Exact range of data, necessary for imshow()

    ### Prepare for plotting
    suptit="HadISST Mean [{}-{}]".format(*yrs)
    var_names= ['Using np.nan','Using masked_array']

    outdir= '../Pics/'
    out_fig_nm= outdir+'O05.masked_SST+background_img.png'
    plot_data= dict(data=[sstmean1,sstmean2], var_names=var_names, out_fnm=out_fig_nm,
                    img_bound=img_bound,suptit=suptit)
    plot_map(plot_data)
    return

###--- Map Plot
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import LAND
def plot_map(pdata):
    fig=plt.figure()
    fig.set_size_inches(8.5,6)  ## (xsize,ysize)
    suptit=pdata['suptit']
    fig.suptitle(suptit,fontsize=17,y=0.98,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    left,right,top,bottom=0.05,0.93,0.925,0.05
    iix=left; gapx=0.02; npnx=2
    lx=(right-iix-gapx*(npnx-1))/float(npnx)
    iiy=top; gapy=0.09; npny=2
    ly=(iiy-bottom-gapy*(npny-1))/float(npny)

    ix=iix; iy=iiy-ly

    cm = plt.cm.get_cmap('jet')
    #cm.set_bad('w') #0.4')
    cm.set_under('0.8')

    nlat,nlon= pdata['data'][0].shape
    img_bound= pdata['img_bound']
    dlat,dlon= (img_bound[1]-img_bound[0])/nlon, (img_bound[3]-img_bound[2])/nlat
    lons_data=np.arange(img_bound[0]+dlon/2,img_bound[1],dlon)
    lats_data=np.arange(img_bound[2]+dlat/2,img_bound[3],dlat)
    print(dlat,dlon,lons_data.shape,lats_data.shape,pdata['data'][0].shape)
    val_min, val_max= 0, int(pdata['data'][1].max())

    ###--- Map Projection
    center= (img_bound[0]+img_bound[1])/2  # Want to draw a map where dateline is on the center
    proj = ccrs.PlateCarree(central_longitude=center)
    data_crs= ccrs.PlateCarree()

    props_imshow= dict(vmin=val_min, vmax=val_max, origin='lower',
                    extent=img_bound,cmap=cm,transform=data_crs)
    props_contour= dict(cmap=cm,
                    alpha=0.9,transform=data_crs,extend='both') #vmin=val_min,vmax=val_max,

    ##-- Top Panel
    ax11=fig.add_axes([ix,iy,lx,ly],projection=proj)  ### Now it's GeoAxes, not just Axes

    ### Import background image for land area
    os.environ["CARTOPY_USER_BACKGROUNDS"] = "./BGimg/"
    ax11.background_img(name='Topo',resolution='high') # BM or Topo available now.

    pic11= ax11.imshow(pdata['data'][0],**props_imshow)
    ax11.set_extent(img_bound,crs=data_crs)
    subtit='(a) {} + Imshow(intpl=None)'.format(pdata['var_names'][0])
    fns.map_common(ax11,subtit,data_crs,xloc=15)
    print(img_bound)
    ix=ix+lx+gapx
    ax12= fig.add_axes([ix,iy,lx,ly],projection=proj)
    ax12.add_feature(LAND)
    clevels= np.linspace(val_min,val_max,31)
    pic12=ax12.contourf(lons_data,lats_data,pdata['data'][0],clevels,**props_contour)
    subtit='(b) {} + Contourf(31 levels)'.format(pdata['var_names'][0])
    gl_lab_locator=[False,True,False,True]
    fns.map_common(ax12,subtit,data_crs,xloc=15,gl_lab_locator=gl_lab_locator)

    ##-- Bottom Panels
    iy=iy-gapy-ly; ix=iix
    ax21=fig.add_axes([ix,iy,lx,ly],projection=proj)  ### Now it's GeoAxes, not just Axes
    pic21= ax21.imshow(pdata['data'][1],interpolation='gaussian',**props_imshow)
    ax21.set_extent(img_bound,crs=data_crs)
    ax21.add_feature(LAND)
    subtit='(c) {} + Imshow'.format(pdata['var_names'][1])
    fns.map_common(ax21,subtit,data_crs,xloc=15)
    cb1= fns.draw_colorbar(fig,ax21,pic21,type='horizontal',extend='both')

    ix=ix+lx+gapx
    ax22= fig.add_axes([ix,iy,lx,ly],projection=proj)
    ax22.background_img(name='BM',resolution='high') # BM or Topo available now.
    clevels= np.linspace(val_min,val_max,101)
    pic22=ax22.contourf(lons_data,lats_data,pdata['data'][1],clevels,**props_contour)
    subtit='(d) {} + Contourf'.format(pdata['var_names'][1])
    gl_lab_locator=[False,True,False,True]
    fns.map_common(ax22,subtit,data_crs,xloc=15,gl_lab_locator=gl_lab_locator)
    cb1= fns.draw_colorbar(fig,ax22,pic22,type='horizontal')

    ### Show or Save
    plt.show()
    outfnm= pdata['out_fnm']
    print(outfnm)
    #plt.savefig(outfnm,bbox_inches='tight',dpi=150)
    #plt.savefig(outfnm,dpi=100)

    return

if __name__ == "__main__":
    main()
