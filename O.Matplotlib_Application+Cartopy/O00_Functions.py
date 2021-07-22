import sys
import os.path
import numpy as np
from datetime import date
from netCDF4 import Dataset

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

def get_tgt_latlon_idx(latlons, tgt_lats, tgt_lons):
    lon0,dlon,nlon= latlons['loninfo']
    lat0,dlat,nlat= latlons['latinfo']
    ##-- Regional index
    if isinstance(tgt_lons,(list,tuple,np.ndarray)):
        lon_idx= [lon_deg2x(ll,lon0,dlon) for ll in tgt_lons]
        if lon_idx[0]==lon_idx[1]:
            if tgt_lons[0]!=tgt_lons[1]:
                lon_ids= np.arange(nlon)+lon_idx[0]
                lon_ids[lon_ids>=nlon] -= nlon
            else:
                lon_ids= np.array([lon_idx,])
        elif lon_idx[1]<lon_idx[0]:
            lon_ids= np.arange(lon_idx[0]-nlon,lon_idx[1],1)
        else:
            lon_ids= np.arange(lon_idx[0], lon_idx[1], 1)
    else:
        lon_ids= np.arange(nlon,dtype=int)
    lat_idx= [lat_deg2y(ll,lat0,dlat) for ll in tgt_lats]
    return lat_idx, lon_ids

def lon_formatter(x,pos):
    if x<=-180: x+=360
    elif x>=360: x-=360

    if x>0 and x<180:
        return "{:.0f}\u00B0E".format(x)
    elif x>180 and x<360:
        return "{:.0f}\u00B0W".format(360-x)
    elif x>-180 and x<0:
        return "{:.0f}\u00B0W".format(-x)
    else:
        return "{:.0f}\u00B0".format(x)

def lat_formatter(x,pos):
    if x>0:
        return "{:.0f}\u00B0N".format(x)
    elif x<0:
        return "{:.0f}\u00B0S".format(-x)
    else:
        return "{:.0f}\u00B0".format(x)

def open_netcdf(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    fid=Dataset(fname,'r')
    print("Open:",fname)
    return fid


def read_nc_variable(fid,var_name):
    vdata=fid.variables[var_name][:]
    if vdata.shape[0]==1:  # Same to Numpy.squeeze()
        vdata=vdata.reshape(vdata.shape[1:])
    return vdata

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

def read_sst_from_HadISST(yrs=[2015,2020],include_ice=False):
    ###--- Parameters
    indir= '../Data/'
    yrs0= [2015,2020]
    lon0,dlon,nlon= -179.5,1.,360
    lat0,dlat,nlat=  -89.5,1.,180
    mon_per_yr= 12
    nt= (yrs0[1]-yrs0[0]+1)*mon_per_yr

    infn= indir+"HadISST1.sample.{}-{}.{}x{}x{}.f32dat".format(*yrs0,nt,nlat,nlon)
    sst= bin_file_read2mtx(infn)  # 'dtype' option is omitted because 'f32' is basic dtype
    sst= sst.reshape([nt,nlat,nlon]).astype(float)  # Improve precision of calculation

    it= (yrs[0]-yrs0[0])*mon_per_yr
    nmons= (yrs[1]-yrs[0]+1)*mon_per_yr
    if (it != 0) or (nmons != nt):
        sst= sst[it:it+nmons,:,:]
    print(sst.shape)

    ### We already know that missings are -999.9, and ice-cover value is -10.00.
    if include_ice:
        miss_idx= sst<-11
    else:
        miss_idx= sst<-9.9
    sst[miss_idx]= np.nan

    lat_info= dict(lat0=lat0,dlat=dlat,nlat=nlat)
    lon_info= dict(lon0=lon0,dlon=dlon,nlon=nlon)
    return sst, lat_info,lon_info


def bar_x_locator(width,data_dim=[1,10]):
    """
    Depending on width and number of bars,
    return bar location on x axis
    Input width: (0,1) range
    Input data_dim: [# of vars, # of bins]
    Output locs: list of 1-D array(s)
    """
    xx=np.arange(data_dim[1])
    shifter= -width/2*(data_dim[0]-1)
    locs=[]
    for x1 in range(data_dim[0]):
        locs.append(xx+(shifter+width*x1))
    return locs

def write_val(ax,values,xloc,yloc,crt=0,ha='center',va='center'):
    """
    Show values on designated location if val>crt.
    Input values, xloc, and yloc should be of same dimension
    """
    ### Show data values
    for val,xl,yl in zip(values,xloc,yloc):
        if val>crt: # Write large enough numbers only
            pctxt='{:.0f}%'.format(val)
            ax.text(xl,yl,pctxt,ha=ha,va=va,stretch='semi-condensed',fontsize=10)
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
