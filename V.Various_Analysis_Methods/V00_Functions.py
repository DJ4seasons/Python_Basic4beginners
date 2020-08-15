"""
Various functions commonly used in codes in this directory

Daeho Jin
"""

import sys
import os.path
import numpy as np
from datetime import date

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

def read_sst_from_HadISST(yrs=[2015,2019]):
    ###--- Parameters
    indir= '../Data/'
    yrs0= [2015,2019]
    lon0,dlon,nlon= -179.5,1.,360
    lat0,dlat,nlat=  -89.5,1.,180
    mon_per_yr= 12
    nt= (yrs0[1]-yrs0[0]+1)*mon_per_yr

    infn= indir+"HadISST1.sample.{}-{}.{}x{}x{}.f32dat".format(*yrs,nt,nlat,nlon)
    sst= bin_file_read2mtx(infn)  # 'dtype' option is omitted because 'f32' is basic dtype
    sst= sst.reshape([nt,nlat,nlon]).astype(float)  # Improve precision of calculation

    it= (yrs[0]-yrs0[0])*mon_per_yr
    nmons= (yrs[1]-yrs[0]+1)*mon_per_yr
    sst= sst[it:it+nmons,:,:]
    print(sst.shape)

    ### We already know that missings are -999.9, and ice-cover value is -10.00.
    miss_idx= sst<-9.9
    sst[miss_idx]= np.nan

    lats= dict(lat0=lat0,dlat=dlat,nlat=nlat)
    lons= dict(lon0=lon0,dlon=dlon,nlon=nlon)
    return sst, lats,lons

def get_sst_ano_from_HadISST(area_bound,yrs=[2015,2019],remove_AC=True):
    '''
    area_bound= [west,east,south,north] in degrees
    '''

    ### Read SST
    sst, lats, lons= read_sst_from_HadISST(yrs=yrs)

    ### Cut by given area_bound
    if area_bound[2]<lats['lat0'] or area_bound[3]>lats['lat0']+lats['dlat']*lats['nlat']:
        print("area_bound is out of limit", area_bound, lats)
        sys.exit()

    lon_idx= [lon_deg2x(lon,lons['lon0'],lons['dlon']) for lon in area_bound[:2]]
    lat_idx= [lat_deg2y(lat,lats['lat0'],lats['dlat']) for lat in area_bound[2:]]
    print(lon_idx,lat_idx)
    if lon_idx[0]>=lon_idx[1]:
        tmpidx= list(range(lon_idx[0],lons['nlon']))+list(range(0,lon_idx[1]))
        sst= sst[:,lat_idx[0]:lat_idx[1],tmpidx]
    else:
        sst= sst[:,lat_idx[0]:lat_idx[1],lon_idx[0]:lon_idx[1]]

    ##- Update parameters
    nt,nlat,nlon= sst.shape
    lons['lon0']= lons['lon0']+lons['dlon']*lon_idx[0]
    lons['nlon']= nlon
    lats['lat0']= lats['lat0']+lats['dlat']*lat_idx[0]
    lats['nlat']= nlat


    ### Remove annual mean
    sstm= sst.mean(axis=0)
    sstano= sst-sstm[None,:,:]  # This is for masking grid cells having any NaN
    sst=1  # Flush sst array data from memory because it's unnecessary hereinafter

    if remove_AC:
        ### Remove seasonal cycle
        mon_per_yr=12
        ssn_mean= sstano.reshape([-1,mon_per_yr,nlat,nlon]).mean(axis=0)
        sstano= (sstano.reshape([-1,mon_per_yr,nlat,nlon])-ssn_mean[None,:,:,:]).reshape([nt,nlat,nlon])

    return sstano, lats, lons

def get_sst_areamean_from_HadISST(area_bound,yrs= [2015,2019]):
    '''
    area_bound= [west,east,south,north] in degrees
    '''
    ### Read SST
    sst, lats, lons= read_sst_from_HadISST(yrs=yrs)

    ### Calculate area mean
    lon_idx= [lon_deg2x(lon,lons['lon0'],lons['dlon']) for lon in area_bound[:2]]
    lat_idx= [lat_deg2y(lat,lats['lat0'],lats['dlat']) for lat in area_bound[2:]]

    if lon_idx[0]>lon_idx[1]:
        tmpidx= list(range(lon_idx[0],lons['nlon']))+list(range(0,lon_idx[1]))
        am= np.nanmean(sst[:,lat_idx[0]:lat_idx[1],tmpidx],axis=(1,2))
    else:
        am= np.nanmean(sst[:,lat_idx[0]:lat_idx[1],lon_idx[0]:lon_idx[1]],axis=(1,2))
    print(lon_idx+lat_idx,am.shape, am.min(), am.max())  # Check if NaN exists here

    ### Remove seasonal cycle
    mon_per_yr=12
    am_mean= am.reshape([-1,mon_per_yr]).mean(axis=0)
    am= (am.reshape([-1,mon_per_yr])-am_mean[None,:]).reshape(-1)
    return am

def read_rmm_text(date_range=[]):
    """
    Read RMM Index Text file
    fname: include directory
    date_range: start and end dates, including both end dates, optional
    """
    indir= '../Data/'
    fname= indir+'rmm.74toRealtime.txt'

    if not os.path.isfile(fname):
        #print( "File does not exist:"+fname); sys.exit()
        sys.exit("File does not exist: "+fname)

    if len(date_range)!=0 and len(date_range)!=2:
        print("date_range should be [] or [ini_date,end_date]")
        sys.exit()

    time_info=[]; pcs=[]; phs=[]
    with open(fname,'r') as f:
        for i,line in enumerate(f):
            if i>=2:  ### Skip header (2 lines)
                ww=line.strip().split() #
                onedate=date(*map(int,ww[0:3])) ### "map()": Apply "int()" function to each member of ww[0:3]
                if len(date_range)==0 or (len(date_range)==2 and onedate>=date_range[0] and onedate<=date_range[1]):
                    pcs.append([float(ww[3]),float(ww[4])]) ### RMM PC1 and PC2
                    phs.append(int(ww[5]))  ### MJO Phase
                    time_info.append(onedate)  ### Save month only

    print("Total RMM data record=",len(phs))
    time_info, pcs, phs= np.asarray(time_info),np.asarray(pcs),np.asarray(phs) ### Return as Numpy array
    strs= np.sqrt((pcs**2).sum(axis=1))  # Euclidean distance

    ### Check missing
    miss_idx= phs==999
    if miss_idx.sum()>0:
        print("There are {} missing(s)".format(miss_idx.sum()))
    else:
        print("No missings")

    return time_info, pcs, phs, strs, miss_idx

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
