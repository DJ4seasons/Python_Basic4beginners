"""
t-test example
Re-arange global SST to 5deg x 5deg box, and for every box, test mean difference
between first 3 years and later 2 years.

Note: Welch's t-test
Welch's t-test is to test if two populations have equal means.
Welch's t-test is more reliable when the two samples have unequal variance and/or unequal sample size.
https://en.wikipedia.org/wiki/Welch%27s_t-test

---
Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Binary data file(HadISST) was produced by D04 code
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

Daeho Jin

---
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind_from_stats.html
"""

import sys
import os.path
import numpy as np

import V00_Functions as vf

def main():
    ### Years to read data
    yrs= [2015,2020]  # Starting year and ending year

    ### Get SST anomaly
    area_range= [-180,180,-60,60]  # [lon_range, lat_range]
    sstano, lat_info, lon_info= vf.get_sst_ano_from_HadISST(area_range,yrs,remove_AC=True)

    ### Re-arange SST by 5deg x 5deg cells
    nlat, nlon= lat_info['nlat'], lon_info['nlon']
    scaler=5
    nlat2, nlon2= nlat//scaler, nlon//scaler
    sstano= sstano.reshape([-1,nlat2,scaler,nlon2,scaler]).swapaxes(2,3)
    sstano= sstano.reshape([-1,nlat2,nlon2,scaler**2])
    ms_idx= np.isnan(sstano[0,:,:,:]).sum(axis=2)>scaler**2/2  # missing if more than half is missing

    data2test= np.nanmean(sstano[:,~ms_idx,:],axis=2)  # Mean for 5x5 cells

    ### Calculate dependency_level
    dof_coef1= np.apply_along_axis(get_dof_coef_log_r1,0,data2test)
    dof_coef2= np.apply_along_axis(get_dof_coef_e_folding,0,data2test)
    print(dof_coef1.min(),np.median(dof_coef1))
    print(dof_coef2.min(),np.median(dof_coef2))

    ### Split data for t-test
    data_prv, data_post= data2test[:36,:], data2test[36:,:]  # First 3 years and later 3 years

    ### Calculate significance level of t-test by different dof setting
    p_vals1= get_ttest_pval_2d(dof_coef1,data_prv,data_post)
    p_vals2= get_ttest_pval_2d(dof_coef2,data_prv,data_post)
    p_vals3= get_ttest_pval_2d(np.ones_like(dof_coef1),data_prv,data_post)  # Assume no dependency

    ### Construct new map of p-values
    new_map= np.full(ms_idx.shape,np.nan,dtype=float)
    data=[]
    for pp in [p_vals1, p_vals2, p_vals3]:
        new_map[~ms_idx]= pp
        data.append(np.copy(new_map))

    ### Map info for displaying
    lon0, dlon= lon_info['lon0'], lon_info['dlon']
    lat0, dlat= lat_info['lat0'], lat_info['dlat']
    img_bound= [lon0-dlon/2,lon0+dlon*(nlon+0.5),lat0-dlat/2,lat0+dlat*(nlat+0.5)]  # Exact range of data, necessary for imshow()
    ##-- Above bound is based on previous resolution, but it's ok since no change on area_boundary

    ### Prepare for plotting
    suptit="t-test for Mean Diff., 2015-17 vs. 2018-20 [HadISST]"
    var_names= ['DoF= -N*log(r1)','DoF= N/(2*Te)','DoF= N']

    outdir= '../Pics/'
    out_fig_nm= outdir+'V08.t-test_example_5deg_box.png'
    plot_data= dict(data=data, var_names=var_names, out_fnm=out_fig_nm,
                    img_bound=img_bound,suptit=suptit)
    plot_map(plot_data)

    return

from scipy import stats
def get_ttest_pval_2d(dof_coef,data1,data2):
    '''
    Calculate p-value for 2-D arrays
    '''
    nn1,nn2= data1.shape[0], data2.shape[0]

    stat1= [data1.mean(axis=0), data1.std(axis=0,ddof=1), nn1*dof_coef]
    stat2= [data2.mean(axis=0), data2.std(axis=0,ddof=1), nn2*dof_coef]
    stat1, stat2 = np.asarray(stat1),np.asarray(stat2)

    p_vals=[]
    for i in range(stat1.shape[1]):
        if stat1[2,i]>3 and stat2[2,i]>3:  # Limit by minimum dof criterion
            p_vals.append(stats.ttest_ind_from_stats(*stat1[:,i], *stat2[:,i], equal_var=False)[1])
        else:
            p_vals.append(np.nan)

    return np.asarray(p_vals)

def get_dof_coef_log_r1(ts1d):
    '''
    Estimating decorrelating time using auto-correlation, r1
    dof_coef= -np.log(r1)  # vonStorch and Zwiers (1999)
    '''
    r1= np.corrcoef(ts1d[1:],ts1d[:-1])[0,1]
    return -np.log(r1)

def get_dof_coef_e_folding(ts1d):
    '''
    DOF= n*(dt/2/Te), Te= e-folding time; Panofsky and Brier, 1958)
    '''
    ac=[]
    test=True
    it=0
    while test:
        it+=1
        ac.append(np.corrcoef(ts1d[it:],ts1d[:-it])[0,1])
        if ac[-1]< 1/np.exp(1):  # e-folding time
            break
    ### Linearly interpolating
    Te= (it*(ac[it-2]-1/np.exp(1))+(it-1)*(1/np.exp(1)-ac[it-1]))/(ac[it-2]-ac[it-1])
    return 1/2/Te

###---
### Draw (semi) global map
###---
import matplotlib.pyplot as plt
import matplotlib.colors as cls
import cartopy.crs as ccrs

def plot_map(pdata):
    '''
    Draw global map where dateline is on the center
    '''
    abc='abcdefgh'

    ###--- Create a figure
    fig=plt.figure()
    fig.set_size_inches(7,8.5)  ## (xsize,ysize)

    ###--- Suptitle
    suptit=pdata['suptit']
    fig.suptitle(suptit,fontsize=16,y=0.97,va='bottom',stretch='semi-condensed')

    ###--- Map Projection
    center= 180  # Want to draw a map where dateline is on the center
    proj = ccrs.PlateCarree(central_longitude=center)
    data_crs= ccrs.PlateCarree()

    map_extent= [0.,359.9,-60,60]  # Range to be shown
    img_range= pdata['img_bound']

    ###--- Set range of values to be shown
    #val_min, val_max= 0,0.5   <-- it is unnecessary for BoundaryNorm
    p_val_levels= [0,0.01, 0.02, 0.05, 0.1, 0.2]

    ###--- Color map
    colors= ['darkred','#FA325A','darkorange','forestgreen','#C9CD71']
    cm= cls.LinearSegmentedColormap.from_list("cm5",colors)
    cm.set_under('1.'); cm.set_over('1.')
    cm.set_bad('0.8')  # For the gridcell of NaN
    norm= cls.BoundaryNorm(p_val_levels,ncolors=cm.N,clip=False)

    left,right,top,bottom= 0.07, 0.97, 0.93, 0.12
    npnx,gapx,npny,gapy= 1, 0.05, len(pdata['data']), 0.06
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    props_imshow= dict(norm=norm, origin='lower',cmap=cm,
                extent=img_range,transform=data_crs)

    for i, (data,vnm) in enumerate(zip(pdata['data'],pdata['var_names'])):
        ax1= fig.add_axes([ix,iy-ly,lx,ly],projection=proj)
        ax1.set_extent(map_extent,crs=data_crs)
        map1= ax1.imshow(data,**props_imshow)

        subtit= '({}) {}'.format(abc[i],vnm)
        vf.map_common(ax1,subtit,data_crs,xloc=60,yloc=20)

        iy=iy-ly-gapy
    cb= vf.draw_colorbar(fig,ax1,map1,type='horizontal',size='panel',gap=0.06,extend='max')
    cb.set_label('Significance level',fontsize=11)
    cb.ax.set_xticklabels(['{:.0f}%'.format((1-val)*100) for val in p_val_levels])
    cb.ax.tick_params(labelsize=10)

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
