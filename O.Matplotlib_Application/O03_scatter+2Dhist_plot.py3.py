'''
Matplotlib Application(3)
: Display scatter and 2D histogram plot to show relationship of two variables

Data
: CCMP_Wind_Analysis_20190101_V02.0_L3.0_RSS.daily.nc (obtained from E02)

by Daeho Jin
'''

import sys
import os.path
import numpy as np
from datetime import date
from netCDF4 import Dataset

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

def main():
    ###--- Read CCMP wind data
    tgt_date= date(2019,1,1)
    date_txt= tgt_date.strftime('%Y%m%d')

    indir= '../Data/'
    infn= indir+'CCMP_Wind_Analysis_{}_V02.0_L3.0_RSS.daily.nc'.format(date_txt)

    fid= open_netcdf(infn)

    var_names= ['uwnd', 'vwnd']
    uwnd= read_nc_variable(fid,var_names[0])
    vwnd= read_nc_variable(fid,var_names[1])

    ###--- Check missings and select commonly non-missing data
    missings= np.logical_or(uwnd.mask, vwnd.mask)
    uwnd.mask, vwnd.mask= missings, missings
    uwnd= uwnd.compressed()[::3]  # Reduce data size to 1/3 for convenience
    vwnd= vwnd.compressed()[::3]
    if uwnd.shape != vwnd.shape:  # Now the shape should be identical
        print("Shapes are not same:", uwnd.shape, vwnd.shape)
        sys.exit()

    outdir= '../Pics/'
    outfn= outdir+'O03_CCMP_Wind_daily_u_vs_v.{}.Scatter+2Dhist.png'.format(date_txt)

    plot_data= dict(data=[uwnd,vwnd],var_names=var_names,outfn=outfn)
    plot_main(plot_data)


###---
### Box and Viloin Plot
###---
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter
import matplotlib.patches as mpatches

def plot_main(plot_data):
    ###--- Plotting Start ---###
    abc='abcdefghijklmn'
    ##-- Page Setup --##
    fig = plt.figure()
    fig.set_size_inches(10,5)    # Physical page size in inches, (lx,ly)
    fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.1,wspace=0.15)  ### Margins, etc. ,hspace=0.35

    ##-- Title for the page --##
    suptit="CCMP Surface Wind distribution on 2019.01.01"
    fig.suptitle(suptit,fontsize=16,va='bottom',y=0.98)  #,ha='left',x=0.,stretch='semi-condensed')

    cm=plt.cm.get_cmap('plasma')
    x, y= plot_data['data']
    spd= np.sqrt(x**2+y**2)  # Wind speed; set for color scale of scatter plot

    ##-- Set up an axis --##
    ax1 = fig.add_subplot(1,2,1)   # (# of rows, # of columns, indicater from 1)
    props= dict(s=5,marker='o',alpha=0.8,cmap=cm,vmin=0.,vmax=20)
    pic1 = ax1.scatter(x,y,c=spd,**props)

    subtit='(a) Scatter Plot'
    ax1.set_title(subtit,fontsize=12,x=0.,ha='left')
    plot_common(ax1,subtit=subtit)
    ax1.set_xlabel(plot_data['var_names'][0].upper(),fontsize=12)
    ax1.set_ylabel(plot_data['var_names'][1].upper(),fontsize=12)

    cb1=draw_colorbar(fig,ax1,pic1,type='horizontal',size='panel',extend='max',gap=0.15,width=0.03)
    cb1.set_ticks(range(0,21,5))
    cb1.set_label('Wind Speed(m/s)',fontsize=11)
    ##-- Set up an axis --##
    ax2 = fig.add_subplot(1,2,2)   # (# of rows, # of columns, indicater from 1)

    cm=plt.cm.get_cmap('viridis'); cm.set_under(color='0.8')
    H, xedges, yedges= np.histogram2d(x,y,bins=(9,8))
    H=(H/H.sum()*100.).T; print(H.max(),H.mean())
    X,Y=np.meshgrid(xedges,yedges)
    props = dict(edgecolor='none',alpha=0.8,vmin=0.1,vmax=10,cmap=cm)

    pic2 = ax2.pcolormesh(X,Y,H,**props)

    subtit='(c) 2D Histogram'
    ax2.set_title(subtit,fontsize=12,x=0.,ha='left')
    plot_common(ax2,subtit=subtit,ytright=True)
    ax2.set_xlabel(plot_data['var_names'][0].upper(),fontsize=12)
    ax2.set_ylabel(plot_data['var_names'][1].upper(),fontsize=12,rotation=-90)
    ax2.yaxis.set_label_position("right")

    cb2=draw_colorbar(fig,ax2,pic2,type='horizontal',size='panel',extend='both',gap=0.15,width=0.03)
    xt= cb2.get_ticks()
    xt= [0.1,]+list(xt)
    cb2.set_ticks(xt)
    cb2.ax.set_xticklabels(['{:.1f}%'.format(x) for x in xt],size=10)

    ny,nx=H.shape
    xlocs=(xedges[1:]+xedges[:-1])/2
    ylocs=(yedges[1:]+yedges[:-1])/2
    xl,yl= np.meshgrid(xlocs,ylocs)
    write_val(ax2,H.reshape(-1),xl.reshape(-1),yl.reshape(-1),crt=4.95)

    ##-- Seeing or Saving Pic --##
    #- If want to see on screen -#
    #plt.show()

    #- If want to save to file
    outfnm= plot_data['outfn']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
    return

def write_val(ax,values,xloc,yloc,crt=0,ha='center',va='center'):
    """
    Show values on designated location if val>crt.
    Input values, xloc, and yloc should be of same dimension
    """
    ### Show data values
    for val,xl,yl in zip(values,xloc,yloc):
        if val>crt: # Write only for large numbers
            pctxt='{:.1f}%'.format(val)
            ax.text(xl,yl,pctxt,ha=ha,va=va,stretch='semi-condensed',fontsize=10)
    return

def plot_common(ax,subtit='',ytlab=True,ytright=False):
    ax.set_title(subtit,fontsize=14,x=0.,ha='left') #,y=0.9

    ax.set_xlim(-20,20)
    ax.xaxis.set_major_locator(MultipleLocator(10))   # For Major Ticks
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks

    ax.set_ylim(-20,20)
    ax.set_yticks(range(-20,21,10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))

    if not ytlab:
        ax.set_yticklabels('')

    if ytright:
        ax.yaxis.tick_right()

    ax.yaxis.set_ticks_position('both')
    ax.tick_params(axis='both',labelsize=10)

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
