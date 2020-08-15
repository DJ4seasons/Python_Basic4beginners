"""
Calculate correlation coefficients between Nino3.4 and global SST

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

def bin_file_read2mtx(fname, dtype=np.float32):
    """ Open a binary file, and read data
        fname : file name with directory path
        dtype   : data type; np.float32 or np.float64, etc. """

    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    with open(fname,'rb') as fd:
        bin_mat = np.fromfile(file=fd, dtype=dtype)

    return bin_mat

from math import ceil
def lon_deg2x(lon,lon0,dlon):
    '''
    For given longitude information, return index of given specific longitude
    lon: target longitude to be transformed to index
    lon0: the first (smallest) value of longitude grid
    dlon: the increment of longitude grid
    return: integer index
    '''
    x = ceil((lon-lon0)/dlon)
    nx = int(360/dlon)
    if x<0:
        while(x<0):
            x+= nx
    if x>=nx: x=x%nx
    return x
lat_deg2y = lambda lat,lat0,dlat: ceil((lat-lat0)/dlat)

def main():
    ###--- Parameters
    indir= '../Data/'
    #HadISST1.sample.2017-2019.36x180x360.f32dat
    yrs= [2015,2019]  # Starting year and ending year
    mon_per_yr= 12
    nt= (yrs[1]-yrs[0]+1)*mon_per_yr
    lon0,dlon,nlon= -179.5,1.,360
    lat0,dlat,nlat=  -89.5,1.,180

    infn= indir+"HadISST1.sample.{}-{}.{}x{}x{}.f32dat".format(*yrs,nt,nlat,nlon)
    sst= bin_file_read2mtx(infn)  # 'dtype' option is omitted because 'f32' is basic dtype
    sst= sst.reshape([nt,nlat,nlon]).astype(float)  # Improve precision of calculation
    print(sst.shape)

    ### We already know that missings are -999.9, and ice-cover value is -10.00.
    miss_idx= sst<-9.9
    sst[miss_idx]= np.nan
    print(miss_idx.sum())

    ### Cut SST only for 60S to 60N for convenience
    lat_idx= [lat_deg2y(lat,lat0,dlat) for lat in [-60,60]]
    sst= sst[:,lat_idx[0]:lat_idx[1],:]
    ##- Update parameters
    lat0= lat0+ (lat_idx[0]*dlat)
    nlat= lat_idx[1]-lat_idx[0]

    ### Degrading data resolution (for convenience)
    sst= sst.reshape([nt,nlat//2,2,nlon//2,2]).swapaxes(2,3).\
            reshape([nt,nlat//2,nlon//2,4]).mean(axis=-1)
    ##- Update parameters
    lat0,dlat,nlat= lat0+dlat, dlat*2, nlat//2
    lon0,dlon,nlon= lon0+dlon, dlon*2, nlon//2
    print(sst.shape)

    ### Remove annual mean
    sstm= sst.mean(axis=0)
    sstano= sst-sstm[None,:,:]  # This is for masking grid cells with any NaN
    sst=1  # Flush sst array data from memory because it's unnecessary hereinafter
    ms_idx= np.isnan(sstm)  # They will not be used for calculation
    print(ms_idx.sum(), '{:.2f}%'.format(ms_idx.sum()/nlat/nlon*100))

    ### Remove seasonal cycle
    ssn_mean= sstano.reshape([-1,mon_per_yr,nlat,nlon]).mean(axis=0)
    sstano= (sstano.reshape([-1,mon_per_yr,nlat,nlon])-ssn_mean[None,:,:,:]).reshape([nt,nlat,nlon])

    ### Principle Component using SVD
    from scipy.linalg import svd
    pc, s, evec = svd(sstano[:,~ms_idx])
    print(evec.shape, s.shape, pc.shape)

    ### Eigen values
    eval= s**2/nt
    print(eval[:3],eval[-3:],eval.max())
    trace= np.sum(eval)
    print("Trace = {:.3f}".format(trace))

    for i in range(10):
        eval_info='''
    Eigenvalue #{num} = {ev:7.3f}
    This explains {ev_pct:.1f}% of total variance.'''.format(
            num=i, ev=eval[i], ev_pct=eval[i]/trace*100)
        print(eval_info)

    ### Normalizing EOF
    evec= evec[:nt,:]*np.sqrt(eval)[:,None]
    flip_idx= evec.min(axis=1)*-1 > evec.max(axis=1)  # set bigger value becomes positive
    evec[flip_idx,:]*=-1

    ### Normalizing PC
    pc= pc*np.sqrt(nt) #[:,None]
    pc[:,flip_idx]*=-1

    import matplotlib.pyplot as plt
    amap= np.full([nlat,nlon],np.nan)
    amap[~ms_idx]= evec[0,:]
    #plt.imshow(amap,origin='lower')
    plt.plot(pc[:,0],color='k')
    plt.plot(pc[:,1],color='r')
    #plt.colorbar()
    plt.show()
    sys.exit()

    ### Prepare for plotting
    data= [corr_coef1, corr_coef2, corr_coef3]
    var_names= ['Calc_manually','Using pearsonr()','Using corrcoef()']
    lat_info= dict(lat0=lat0,dlat=dlat,nlat=nlat)
    lon_info= dict(lon0=lon0,dlon=dlon,nlon=nlon)

    outdir= '../Pics/'
    out_fig_nm= outdir+'X0x.correlation_example.png'.format(var_names[2])
    plot_data= dict(data=data, var_names=var_names, out_fnm=out_fig_nm,
                    lat_info=lat_info, lon_info=lon_info)
    plot_map(plot_data)

    return

def corr_manual_1d_vs_2d(arr1d, arr2d):
    """
    Calculate Pearson correlation coefficients

    Input
    arr1d: 1-d array of shape [m,]
    arr2d: 2-d array of shape [m,n]
    Assumed that there is no missings in input data
    ---
    Output
    corr: coefficients, 1-d array of shape [n]
    Abnormal values are filled with NaN
    """
    std1= np.std(arr1d)
    std2= np.std(arr2d,axis=0)
    ### Avoid division by zero
    nonzero_idx= std2!=0

    corr= np.full([arr2d.shape[1],],np.nan)
    corr[nonzero_idx]= np.mean(arr2d*arr1d[:,None],axis=0)[nonzero_idx]/std1/std2[nonzero_idx]
    return corr

def corr_pearsonr_1d_vs_2d(arr1d, arr2d):
    """
    Calculate Pearson correlation coefficients
    based on scipy.stats.pearsonr()
    Because 'pearsonr' only get 1-d array, need to use 'np.apply_along_axis'
    'pearsonr' returns two variables, coefficient and p-value.

    Input
    arr1d: 1-d array of shape [m,]
    arr2d: 2-d array of shape [m,n]
    Assumed that there is no missings in input data
    ---
    Output
    corr: coefficients, 1-d array of shape [n]
    Abnormal values are filled with NaN
    """
    from scipy.stats import pearsonr
    corr= np.apply_along_axis(lambda x,y: pearsonr(x,y)[0],0,arr2d,y=arr1d)
    return corr

def corr_corrcoef_1d_vs_2d(arr1d, arr2d):
    """
    Calculate Pearson correlation coefficients
    based on numpy.corrcoef()
    Because 'corrcoef' only get 1-d array, need to use 'np.apply_along_axis'
    'corrcoef' returns a array, and coefficient is [0,1] or [1,0]

    Input
    arr1d: 1-d array of shape [m,]
    arr2d: 2-d array of shape [m,n]
    Assumed that there is no missings in input data
    ---
    Output
    corr: coefficients, 1-d array of shape [n]
    Abnormal values are filled with NaN
    """
    corr= np.apply_along_axis(lambda x,y: np.corrcoef(x,y)[0,1],0,arr2d,y=arr1d)
    return corr


###---
### Draw (semi) global map
###---
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FixedLocator

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def plot_map(pdata):
    ###--- Create a figure
    fig=plt.figure()
    fig.set_size_inches(7,8.5)  ## (xsize,ysize)

    ###--- Suptitle
    suptit="Corr. coef. between SST and Ni{}o3.4 [HadISST,2015-19]".format('\u00F1')
    fig.suptitle(suptit,fontsize=16,y=0.97,va='bottom',stretch='semi-condensed')

    ###--- Map Projection
    center= 180  # Want to draw a map where dateline is on the center
    proj = ccrs.PlateCarree(central_longitude=center)
    proj0= ccrs.PlateCarree()

    ###--- We already know the range of values
    map_extent= [0.,359.9,-60.1,60.1]  # Range to be shown
    img_range= [-179.5,179.5,-59.5,59.5]  # Exact range of data
    val_min, val_max= -1,1  # Because it's correlation coefficient
    abc='abcdefgh'

    ###--- Color map
    cm = plt.cm.get_cmap('Spectral_r')
    cm.set_bad('0.9')  # For the gridcell of NaN

    left,right,top,bottom= 0.07, 0.97, 0.925, 0.1
    npnx,gapx,npny,gapy= 1, 0.05, len(pdata['data']), 0.07
    lx= (right-left-gapx*(npnx-1))/npnx
    ly= (top-bottom-gapy*(npny-1))/npny
    ix,iy= left, top

    props= dict(vmin=val_min, vmax=val_max, origin='lower',
                extent=img_range,cmap=cm,transform=proj0)

    for i, (data,vnm) in enumerate(zip(pdata['data'],pdata['var_names'])):
        ax1= fig.add_axes([ix,iy-ly,lx,ly],projection=proj)
        ax1.set_extent(map_extent,crs=proj0)
        map1= ax1.imshow(data,**props)

        subtit= '({}) {}'.format(abc[i],vnm)
        map_common(ax1,subtit,proj0,xloc=60,yloc=20)

        iy=iy-ly-gapy
    draw_colorbar(fig,ax1,map1,type='horizontal',size='panel',gap=0.06)

    ##-- Seeing or Saving Pic --##
    plt.show()

    #- If want to save to file
    outfnm = pdata['out_fnm']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    #fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

    # Defalut: facecolor='w', edgecolor='w', transparent=False
    return

def map_common(ax,subtit,proj,gl_lab_locator=[False,True,True,False],yloc=10,xloc=30):
    """ Decorating Cartopy Map
    """
    ### Title
    ax.set_title(subtit,fontsize=13,ha='left',x=0.0)
    ### Coast Lines
    ax.coastlines(color='silver',linewidth=1.)
    ### Grid Lines
    '''# Trick to draw grid lines over dateline; not necessary in Cartopy 0.18.0 or later
    gl= ax.gridlines(crs=proj, draw_labels=False,
                    linewidth=0.6, color='gray', alpha=0.5, linestyle='--')
    gl.xlocator = MultipleLocator(xloc)
    gl.ylocator = MultipleLocator(yloc)'''

    gl= ax.gridlines(crs=proj, draw_labels=True,
                    linewidth=0.6, color='gray', alpha=0.5, linestyle='--')

    ### x and y-axis tick labels
    gl.xlabels_top,gl.xlabels_bottom,gl.ylabels_left,gl.ylabels_right = gl_lab_locator
    gl.xlocator = FixedLocator(range(-180,180,xloc))
    #gl.xlocator = MultipleLocator(xloc)
    gl.ylocator = MultipleLocator(yloc)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 10, 'color': 'k'}
    gl.ylabel_style = {'size': 10, 'color': 'k'}
    ### Aspect ratio of map
    ax.set_aspect('auto') ### 'auto' allows the map to be distorted and fill the defined axes
    return

def draw_colorbar(fig,ax,pic1,type='vertical',size='panel',gap=0.06,width=0.02,extend='neither'):
    '''
    Type: 'horizontal' or 'vertical'
    Size: 'page' or 'panel'
    Gap: gap between panel(axis) and colorbar
    Extend: 'both', 'min', 'max', 'neither'
    '''
    pos1=ax.get_position().bounds  ##<= (left,bottom,width,height)
    if type.lower()=='vertical' and size.lower()=='page':
        cb_ax =fig.add_axes([pos1[0]+pos1[2]+gap,0.1,width,0.8])  ##<= (left,bottom,width,height)
    elif type.lower()=='vertical' and size.lower()=='panel':
        cb_ax =fig.add_axes([pos1[0]+pos1[2]+gap,pos1[1],width,pos1[3]])  ##<= (left,bottom,width,height)
    elif type.lower()=='horizontal' and size.lower()=='page':
        cb_ax =fig.add_axes([0.1,pos1[1]-gap,0.8,width])  ##<= (left,bottom,width,height)
    elif type.lower()=='horizontal' and size.lower()=='panel':
        cb_ax =fig.add_axes([pos1[0],pos1[1]-gap,pos1[2],width])  ##<= (left,bottom,width,height)
    else:
        print('Error: Options are incorrect:',type,size)
        return

    cbar=fig.colorbar(pic1,cax=cb_ax,extend=extend,orientation=type)  #,ticks=[0.01,0.1,1],format='%.2f')
    cbar.ax.tick_params(labelsize=10)
    return cbar

if __name__ == "__main__":
    main()
