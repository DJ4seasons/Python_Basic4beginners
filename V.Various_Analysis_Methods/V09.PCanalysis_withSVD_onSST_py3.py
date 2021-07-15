"""
Principal Component Analysis (or Empirical Orthogonal Function[EOF] analysis)
https://climatedataguide.ucar.edu/climate-data-tools-and-analysis/empirical-orthogonal-function-eof-analysis-and-rotated-eof-analysis

Basic idea
1. Calculate co-variance matrix of a variable, [2-D domain as 1-D, time]
2. From co-variance matrix (size= 2-D_domain_size**2), calculate eigenvalue and orthogonal patterns
3. Project the orthogonal patterns to the original variable matrix, and get principal components(PCs)
4. Normalize orthogonal patterns and PCs

Improved method using Singular Value Decomposition(SVD)
1. Apply SVD to a variable matrix, [2-D domain as 1-D, time], and get orthogonal patterns and PCs
2. Normalize orthogonal patterns and PCs

---
Binary data file(HadISST) was produced by D04 code

Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

Daeho Jin

---
https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.svd.html
"""

import sys
import os.path
import numpy as np
from datetime import date, timedelta

import V00_Functions as vf

def main():
    ### Years to read data
    yrs= [2015,2020]  # Starting year and ending year

    ### Get SST anomaly
    area_range= [-180,180,-60,60]  # [lon_range, lat_range]
    sstano, lat_info, lon_info= vf.get_sst_ano_from_HadISST(area_range,yrs,remove_AC=True)
    lat0, dlat, nlat= lat_info.values()
    lon0, dlon, nlon= lon_info.values()

    ### Weight by latitude
    lat_deg= np.arange(nlat)*dlat+lat0
    lat_wt= np.sqrt(np.cos(lat_deg/180*np.pi))  # Or use np.deg2rad()
    sstano= sstano*lat_wt[None,:,None]

    ### This is only for reducing computing time!!!
    ### Degrading data resolution (for convenience)
    scaler=2
    nlat2, nlon2= nlat//scaler, nlon//scaler
    sstano= sstano.reshape([-1,nlat2,scaler,nlon2,scaler]).mean(axis=(2,4))

    ### Find location of missing values
    ms_idx= np.isnan(sstano.mean(axis=0))  # one missing becomes missing
    print("Missing ratio= {:.2f}%".format(ms_idx.sum()/ms_idx.reshape(-1).shape[0]*100))

    ### Get PCs and Eigenvectors
    maxnum=10
    pc, evec, eval= PC_analysis(sstano[:,~ms_idx],maxnum=maxnum)

    '''### Check if it works
    n1= sstano[:,~ms_idx][:,3600]
    n2= np.dot(pc,evec)[:,3600]
    plt.plot(n1); plt.plot(n2)
    plt.show() ; sys.exit()'''

    ### Restore to lat-lon format
    ev_map= np.full([maxnum,*ms_idx.shape],np.nan)
    ev_map[:,~ms_idx]= evec
    img_bound= [lon0-dlon/2,lon0+dlon*(nlon+0.5),lat0-dlat/2,lat0+dlat*(nlat+0.5)]  # Exact range of data, necessary for imshow()
    ##-- Above bound is based on previous resolution, but it's ok since no change on area_boundary

    ### Prepare for plotting
    suptit= 'PC and EOF of Global SST [HadISST, 2015-20]'
    tgt_nums= [1,2,3]
    mon_list= vf.get_monthly_dates(date(yrs[0],1,1),date(yrs[1],12,31),day=15,include_date2=True)

    outdir= '../Pics/'
    out_fig_nm= outdir+'V09.EOF_example_HadISST.png'
    plot_data= dict(ev_map=ev_map, pc=pc, suptit= suptit, out_fnm=out_fig_nm,
                    img_bound=img_bound,mon_list=mon_list,tgt_nums=tgt_nums)
    plot_map(plot_data)

    return

def PC_analysis(arr2d, maxnum=10):
    '''
    # Principle Component using SVD
    # Require "scipy.linalg.svd"
    # Assume that the input data, "arr2d" has no missing values, and
    #    shape of [time, other dimensions as 1d]
    # "maxnum" controls the number of PCs and Eigenvectors to return
    #
    # Output
    # pc: principal components, [time, maxnum]
    # evec: eigenvectors, [maxnum, other dimensions as 1d]
    # eval: eigenvalues, [min(time, other dimensions as 1d)]
    '''
    from scipy.linalg import svd

    if len(arr2d.shape)>2:
        arr2d= arr2d.reshape([arr2d.shape[0],-1])
    nt,nn= arr2d.shape

    ### Perform SVD
    pc, s, evec = svd(arr2d,full_matrices=False)
    print(pc.shape, s.shape, evec.shape)

    ### Eigen values
    eval= s**2/(nt-1)
    trace= np.sum(eval)
    print("\nTrace Sum= {:.3f}".format(trace))

    for i in range(maxnum):
        eval_info='''
    Eigenvalue #{num} = {ev:10.3f}; {ev_pct:6.1f}% of total variance.'''.format(
            num=i+1, ev=eval[i], ev_pct=eval[i]/trace*100)
        print(eval_info)

    ### Normalizing Eigenvectors
    evec= evec[:maxnum,:]*np.sqrt(eval[:maxnum])[:,None]
    flip_idx= evec.min(axis=1)*-1 > evec.max(axis=1)
    evec[flip_idx,:]*=-1  # Set bigger value becomes positive

    ### Normalizing PC
    pc= pc[:,:maxnum]*np.sqrt(nt-1)
    pc[:,flip_idx]*=-1  # Same flipping as eigenvectors

    return pc, evec, eval

###---
### Draw (semi) global map
###---
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.dates import DateFormatter
import cartopy.crs as ccrs

def plot_map(pdata):
    '''
    Draw PC time series on the top, and
       draw global map where dateline is on the center
    '''

    ###--- Create a figure
    fig=plt.figure()
    fig.set_size_inches(6,10)  ## (xsize,ysize)

    ###--- Suptitle
    fig.suptitle(pdata['suptit'],fontsize=16,y=0.97,va='bottom',stretch='semi-condensed')

    ###--- Axes setting
    nk= len(pdata['tgt_nums'])  # Number of data to show
    left,right,top,bottom= 0.07, 0.93, 0.925, 0.1
    npnx,gapx,npny,gapy= 1, 0.05, nk+1, 0.064
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    ###--- Top panel: PC time series
    ax1= fig.add_axes([ix,iy-ly,lx,ly])
    colors= plt.cm.tab10(np.linspace(0.05,0.95,10))
    for i,k in enumerate(pdata['tgt_nums']):
        ax1.plot_date(pdata['mon_list'],pdata['pc'][:,k],fmt='-',c=colors[i],
                lw=2.5,alpha=0.85,label='PC{}'.format(k))
    iy=iy-ly-gapy
    subtit= '(a) '
    ax1.set_title(subtit,fontsize=12,ha='left',x=0.0)
    ax1.legend(bbox_to_anchor=(0.08, 1.02, .92, .10), loc='lower left',
           ncol=nk, mode="expand", borderaxespad=0.,fontsize=10)
    ax1.axhline(y=0.,c='k',lw=0.8,ls='--')
    ax1.grid(ls=':')
    ax1.xaxis.set_major_formatter(DateFormatter('%b%Y'))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_ticks_position('both')
    ax1.tick_params(axis='both',labelsize=10)

    ###--- Next, draw global maps
    ###--- Map Projection
    center= 180  # Want to draw a map where dateline is on the center
    proj = ccrs.PlateCarree(central_longitude=center)
    data_crs= ccrs.PlateCarree()

    map_extent= [0.,359.9,-61,61]  # Range to be shown
    img_range= pdata['img_bound']

    val_max= max(np.nanmin(pdata['ev_map'])*-1,np.nanmax(pdata['ev_map']))
    val_min, val_max= val_max*-0.9, val_max*0.9
    abc='abcdefgh'

    ###--- Color map
    cm = plt.cm.get_cmap('RdBu_r').copy()
    cm.set_bad('0.9')  # For the gridcell of NaN

    props= dict(vmin=val_min, vmax=val_max, origin='lower',
                extent=img_range,cmap=cm,transform=data_crs)

    for i, (data,k) in enumerate(zip(pdata['ev_map'],pdata['tgt_nums'])):
        ax2= fig.add_axes([ix,iy-ly,lx,ly],projection=proj)
        ax2.set_extent(map_extent,crs=data_crs)
        map1= ax2.imshow(data,**props)

        subtit= '({}) EOF{}'.format(abc[i+1],k)
        vf.map_common(ax2,subtit,data_crs,xloc=60,yloc=20,gl_lab_locator=[True,True,False,True])

        iy=iy-ly-gapy
    vf.draw_colorbar(fig,ax2,map1,type='horizontal',size='panel',gap=0.06,extend='both',width=0.02)

    ##-- Seeing or Saving Pic --##
    outfnm = pdata['out_fnm']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(outfnm,dpi=150,bbox_inches='tight')   # dpi: pixels per inch
    # Defalut: facecolor='w', edgecolor='w', transparent=False
    plt.show()
    return

if __name__ == "__main__":
    main()
