'''
Matplotlib Application(5)
Lat/Lon formatter without Cartopy (i.e., no coastlines)
+
Shared x and y example

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
    lon_deg_range=[150,220]
    lat_deg_range=[-30,30]

    latlons= dict(latinfo=(lats['lat0'],lats['dlat'],lats['nlat']),
                    loninfo=(lons['lon0'],lons['dlon'],lons['nlon']))
    lat_idx, lon_ids = fns.get_tgt_latlon_idx(latlons, lat_deg_range, lon_deg_range)

    sst= sst[:,lat_idx[0]:lat_idx[1],lon_ids]
    print(sst.shape)
    print(np.isnan(sst).sum()/sst.shape[0])
    if np.isnan(sst).sum()>0:
        sst= np.ma.masked_invalid(sst)

    ##-- Mean for all time
    sst_mean= sst.mean(axis=0)

    ##-- Domain info for display
    data_lats= np.arange(lat_idx[0],lat_idx[1],1)*lats['dlat']+lats['lat0']
    data_lons= np.asarray(lon_ids)*lons['dlon']+lons['lon0']
    if data_lons[0]>data_lons[-1]:
        data_lons[data_lons<data_lons[0]]+=360

    dlon, dlat = lons['dlon'], lats['dlat']
    # Exact range of data for imshow()
    img_bound= [data_lons[0]-dlon/2, data_lons[-1]+dlon/2,
                data_lats[0]-dlat/2, data_lats[-1]+dlat/2]
    print(img_bound)

    ### Prepare for plotting
    suptit="Mean of HadISST [{}-{}]".format(*yrs)

    outdir= '../Pics/'
    out_fig_nm= outdir+'O05.LatLon_Formatter+Shared_XY.png'
    plot_data= dict(data=sst_mean, img_bound=img_bound, lats=data_lats, lons=data_lons,
                    out_fnm=out_fig_nm, suptit=suptit)
    plot_map(plot_data)
    return

###--- Map Plot
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
def plot_map(pdata):
    fig=plt.figure()
    fig.set_size_inches(7,6)  ## (xsize,ysize)
    suptit=pdata['suptit']
    fig.suptitle(suptit,fontsize=17,y=0.97,va='bottom') #stretch='semi-condensed') ## x=0., ha='left'

    left,right,top,bottom=0.06,0.94,0.93,0.05
    gapx, gapy = 0.01, 0.012
    lx, ly= right-left-gapx, top-bottom-gapy
    lx1= lx*0.75; lx2= lx-lx1  # 3 to 1 ratio
    ly1= ly*0.75; ly2= ly-ly1
    ix, iy = left, top

    cm = plt.cm.get_cmap('jet').copy()
    cm.set_bad('0.7')

    data= pdata['data']
    img_bound= pdata['img_bound']
    lats, lons= pdata['lats'], pdata['lons']

    val_min, val_max= np.floor(data.min()), np.ceil(data.max())
    props_imshow= dict(vmin=val_min, vmax=val_max, origin='lower',
                        extent=img_bound, cmap=cm, aspect='auto')
    props_line= dict(alpha=0.8,lw=2.5)

    ###--- Main panel
    ax1= fig.add_axes([ix,iy-ly1,lx1,ly1])
    pic1= ax1.imshow(data, **props_imshow)
    ##-- X-axis
    ax1.tick_params(axis='x', labelbottom=False)
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ##-- Y-axis
    ax1.yaxis.set_major_formatter(FuncFormatter(fns.lat_formatter))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_ticks_position('both')
    ##-- Both
    ax1.tick_params(axis='both',labelsize=10)
    ax1.grid(color='0.4',lw=0.8,ls=':')

    ###--- Bottom panel
    iy= iy-ly1-gapy
    ax1b= fig.add_axes([ix,iy-ly2,lx1,ly2],sharex=ax1)
    pic1b= ax1b.plot(lons, data.mean(axis=0), **props_line)
    ##-- X-axis
    ax1b.xaxis.set_major_formatter(FuncFormatter(fns.lon_formatter))
    ax1b.xaxis.set_minor_locator(AutoMinorLocator(2))
    ##-- Y-axis
    ax1b.set_ylim([25.75,28.75])
    ax1b.yaxis.set_major_locator(MultipleLocator(1))
    ax1b.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1b.yaxis.set_ticks_position('both')
    ax1b.set_ylabel('degC',fontsize=10)
    ##-- Both
    ax1b.tick_params(axis='both',labelsize=10)
    ax1b.grid(color='0.4',lw=0.8,ls=':')
    ax1b.text(0.98,0.95,'Meridional Mean',ha='right',va='top',fontsize=11,transform=ax1b.transAxes)

    ###--- Right panel
    ix= ix+lx1+gapx
    iy= top
    ax1r= fig.add_axes([ix,iy-ly1,lx2,ly1],sharey=ax1)
    pic1r= ax1r.plot(data.mean(axis=1),lats, **props_line)
    ##-- X-axis
    ax1r.set_xlim([21,31])
    ax1r.xaxis.set_major_locator(MultipleLocator(4))
    ax1r.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1r.set_xlabel('degC',fontsize=10)
    ##-- Y-axis
    ax1r.yaxis.set_major_formatter(FuncFormatter(fns.lat_formatter))
    ax1r.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1r.yaxis.tick_right()
    ##-- Both
    ax1r.tick_params(axis='both',labelsize=10)
    ax1r.grid(color='0.4',lw=0.8,ls=':')
    ax1r.text(0.05,0.98,'Zonal Mean',ha='left',va='top',fontsize=11,transform=ax1r.transAxes)

    ###--- Color Bar
    cb1= fns.draw_colorbar(fig,ax1b,pic1,type='horizontal',extend='both',gap=0.08)
    cb1.ax.xaxis.set_minor_locator(AutoMinorLocator(2))

    ### Show or Save
    outfnm= pdata['out_fnm']
    print(outfnm)
    plt.savefig(outfnm,bbox_inches='tight',dpi=150)
    #plt.savefig(outfnm,dpi=100)
    plt.show()
    return

if __name__ == "__main__":
    main()
