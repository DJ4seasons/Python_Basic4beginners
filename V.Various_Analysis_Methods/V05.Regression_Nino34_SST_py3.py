"""
Calculate regression slopes between Nino3.4 and global SST

---
Binary data file(HadISST) was produced by D04 code

Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Source: https://www.metoffice.gov.uk/hadobs/hadisst/data/download.html
Referece: Rayner, N. A.; Parker, D. E.; Horton, E. B.; Folland, C. K.; Alexander, L. V.;
 Rowell, D. P.; Kent, E. C.; Kaplan, A. (2003) Global analyses of sea surface temperature,
 sea ice, and night marine air temperature since the late nineteenth century
 J. Geophys. Res.Vol. 108, No. D14, 4407, doi:10.1029/2002JD002670 

Daeho Jin
"""

import sys
import os.path
import numpy as np

import V00_Functions as vf

def main():
    ### Years to read data
    yrs= [2015,2019]  # Starting year and ending year

    ### Get Nino3.4 Index
    #Nino3.4 (5N-5S, 170W-120W) [-170,-120,-5,5]
    nn34= vf.get_sst_areamean_from_HadISST([-170,-120,-5,5],yrs,remove_AC=True)

    ### Get SST anomaly
    area_range= [-180,180,-60,60]  # [lon_range, lat_range]
    #area_range= [0,360,-60,60]  # [lon_range, lat_range]
    sstano, lat_info, lon_info= vf.get_sst_ano_from_HadISST(area_range,yrs,remove_AC=True)

    print(nn34.shape, nn34.min(), nn34.max())  # Check if NaN exists here
    print(sstano.shape, np.nanmin(sstano), np.nanmax(sstano))  # Check data

    ms_idx= np.isnan(sstano[0,:,:])

    ### Calculate a map of regression slopes
    regr_map= np.full(sstano.shape[1:],np.nan)

    regr_coef1= regr_manual_1d_vs_2d(nn34, sstano[:,~ms_idx])  # Calculate if not NaN
    print('Method1',regr_coef1.shape, np.nanmin(regr_coef1), np.nanmax(regr_coef1), np.isnan(regr_coef1).sum())
    regr_map[~ms_idx]= regr_coef1  # Back to the map shape
    regr_coef1= np.copy(regr_map)

    regr_coef2= regr_linregress_1d_vs_2d(nn34, sstano[:,~ms_idx])  # Calculate if not NaN
    print('Method2',regr_coef2.shape, np.nanmin(regr_coef2), np.nanmax(regr_coef2), np.isnan(regr_coef2).sum())
    regr_map[~ms_idx]= regr_coef2  # Back to the map shape
    regr_coef2= np.copy(regr_map)

    regr_coef3= regr_sklearn_1d_vs_2d(nn34, sstano[:,~ms_idx])  # Calculate if not NaN
    print('Method3',regr_coef3.shape, np.nanmin(regr_coef3), np.nanmax(regr_coef3), np.isnan(regr_coef3).sum())
    regr_map[~ms_idx]= regr_coef3  # Back to the map shape
    regr_coef3= np.copy(regr_map)

    ### Prepare for plotting
    suptit="Regr. coef. of SST against Ni{}o3.4 [HadISST,2015-19]".format('\u00F1')
    data= [regr_coef1, regr_coef2, regr_coef3]
    var_names= ['Calc_manually','Using linregress()','Using sklearn.linear_model']

    outdir= '../Pics/'
    out_fig_nm= outdir+'V05.regression_2D_example.png'
    plot_data= dict(data=data, var_names=var_names, out_fnm=out_fig_nm,
                    suptit=suptit,lat_info=lat_info, lon_info=lon_info)
    plot_map(plot_data)

    return

def regr_manual_1d_vs_2d(arr1d, arr2d):
    """
    Calculate regression slopes based on equation

    Input
    arr1d: 1-d array of shape [m,]
    arr2d: 2-d array of shape [m,n]
    Assumed that there is no missings in input data
    ---
    Output
    regr: coefficients, 1-d array of shape [n]
    Abnormal values are filled with NaN
    """
    var1= np.var(arr1d)
    regr= np.mean(arr2d*arr1d[:,None],axis=0)/var1
    return regr

def regr_linregress_1d_vs_2d(arr1d, arr2d):
    """
    Calculate regression slopes
    based on scipy.stats.linregress()
    Because 'linregress' only get 1-d array, need to use 'np.apply_along_axis'
    'linregress' returns 5 variables, and slope is the first.

    Input
    arr1d: 1-d array of shape [m,]
    arr2d: 2-d array of shape [m,n]
    Assumed that there is no missings in input data
    ---
    Output
    regr: coefficients, 1-d array of shape [n]
    """
    from scipy.stats import linregress
    regr= np.apply_along_axis(lambda y,x: linregress(x,y)[0],0,arr2d,x=arr1d)
    return regr

def regr_sklearn_1d_vs_2d(arr1d, arr2d):
    """
    Calculate regression slopes
    based on scikitj-learn(sklearn).linear_model.LinearRegression()
    LinearRegression() creates a class object,
    and slopes are returned as attribute 'coef_'

    Input
    arr1d: 1-d array of shape [m,]
    arr2d: 2-d array of shape [m,n]
    Assumed that there is no missings in input data
    ---
    Output
    regr: coefficients, 1-d array of shape [n]
    """
    from sklearn.linear_model import LinearRegression as LR
    regr=LR()   ### Initiate Regression Object

    xdata= arr1d.reshape([-1,1])  ## Need shape of ([n_samples, n_features])
    ydata= arr2d  ## Already satisfy required shape, ([n_samples, n_targets])

    regr.fit(xdata,ydata)  ## Fit the linear model
    coef= np.squeeze(regr.coef_)
    return coef


###---
### Draw (semi) global map
###---
import matplotlib.pyplot as plt
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
    suptit= pdata['suptit']
    fig.suptitle(suptit,fontsize=16,y=0.97,va='bottom',stretch='semi-condensed')

    ###--- Map Projection
    center= 180  # Want to draw a map where dateline is on the center
    proj = ccrs.PlateCarree(central_longitude=center)
    data_crs= ccrs.PlateCarree()

    lon0,dlon,nlon= [val for val in pdata['lon_info'].values()]
    lat0,dlat,nlat= [val for val in pdata['lat_info'].values()]

    map_extent= [0.,359.9,-60.1,60.1]  # Range to be shown
    img_range= [lon0-dlon/2,lon0+dlon*(nlon+0.5),lat0-dlat/2,lat0+dlat*(nlat+0.5)]  # Exact range of data, necessary for imshow()
    #xm,ym= np.meshgrid(np.arange(nlon+1)*dlon+lon0-dlon/2, np.arange(nlat+1)*dlat+lat0-dlat/2)  # For pcolormesh()

    ###--- Set range of values to be shown
    vmax= max(abs(np.nanmin(pdata['data'][0])),np.nanmax(pdata['data'][0]))
    vmax= np.floor(vmax*5)/5   # You can change as you want
    val_min, val_max= -vmax, vmax

    ###--- Color map
    cm = plt.cm.get_cmap('plasma') #'RdYlBu_r')
    cm.set_bad('0.9')  # For the gridcell of NaN

    left,right,top,bottom= 0.07, 0.97, 0.93, 0.12
    npnx,gapx,npny,gapy= 1, 0.05, len(pdata['data']), 0.06
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    props_imshow= dict(vmin=val_min, vmax=val_max, origin='lower',
                    extent=img_range,cmap=cm,transform=data_crs)
    #props_pcolormesh= dict(vmin=val_min, vmax=val_max,cmap=cm,transform=data_crs)

    for i, (data,vnm) in enumerate(zip(pdata['data'],pdata['var_names'])):
        ax1= fig.add_axes([ix,iy-ly,lx,ly],projection=proj)
        ax1.set_extent(map_extent,crs=data_crs)
        map1= ax1.imshow(data,**props_imshow)
        #map1= ax1.pcolormesh(xm,ym,data,**props_pcolormesh)

        subtit= '({}) {}'.format(abc[i],vnm)
        vf.map_common(ax1,subtit,data_crs,xloc=60,yloc=20)

        iy=iy-ly-gapy
    cb= vf.draw_colorbar(fig,ax1,map1,type='horizontal',size='panel',gap=0.06,extend='both')
    cb.set_label('{}C per unit change of Ni{}o3.4'.format('\u00B0','\u00F1'),fontsize=11)
    cb.ax.tick_params(labelsize=10)

    ##-- Seeing or Saving Pic --##
    plt.show()

    #- If want to save to file
    outfnm = pdata['out_fnm']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    #fig.savefig(outfnm,dpi=150,bbox_inches='tight')   # dpi: pixels per inch

    return


if __name__ == "__main__":
    main()
