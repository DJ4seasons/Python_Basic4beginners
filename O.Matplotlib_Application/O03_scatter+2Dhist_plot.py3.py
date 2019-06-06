import numpy as np
import sys
import os.path
from subprocess import call
from datetime import timedelta, date, datetime
from netCDF4 import Dataset, date2num


import matplotlib   ### Discover Only
matplotlib.use('TkAgg')   ### Discover Only

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

def open_netcdf(fname):
    if not os.path.isfile(fname):
        print("File does not exist:"+fname)
        sys.exit()

    fid=Dataset(fname,'r')
    print("Open:",fname)
    return fid

def daterange(start_date, end_date):
    ### Including end date
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def read_nc_variable(fid,var_name):
    vdata=fid.variables[var_name][:]
    if vdata.shape[0]==1:
        vdata=vdata.reshape(vdata.shape[1:])
    return vdata

def draw_colorbar(ax,pic1,type='vertical',size='panel',gap=0.06,width=0.02,extend='neither'):
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


###--- Prepare Data ---###
var= 'slp'
dim_names = ['XLAT','XLONG']
indir = '/home/djin1/Zbegins_Python/Py3_lecture_2019/data/'

start_date = date(2018,2,17)  ### Start Date
end_date = date(2018,2,19)   ### Including this End Date

abc='abcdefghijklmn'

bins=np.arange(970,1021,5)
xlabs=['{}-\n{}'.format(bins[i],bins[i+1]) for i in range(len(bins)-1)]
print(xlabs)

data=[]; days=[]
for oneday in daterange(start_date,end_date):
    dd=oneday.strftime('%Y-%m-%d')
    days.append(dd)

    infn=indir+'{}_wrfout_d01_{}_12-00-00.nc'.format(var,dd)
    fid=open_netcdf(infn)
    #if oneday==start_date:
    #    lats=read_nc_variable(fid,'XLAT')
    #    lons=read_nc_variable(fid,'XLONG')

    data1=read_nc_variable(fid,var.upper())
    data.append(data1.reshape(-1))



x=data[1]
xidx= x<990
x=x[xidx]
y=data[0][xidx]
cc=data[2][xidx]

###--- Linear Regression
from sklearn import linear_model

## For linear-regression
regr=linear_model.LinearRegression()   ### Initiate Regression Object

xdata=x.reshape([-1,1])  ## wind speed
ydata=y.reshape([-1,1])  ## surface pressure

regr.fit(xdata,ydata)
r2score=regr.score(xdata,ydata)
print(u"Coeff.={:.2f}, Intercept={:.2f}, R\u00B2 Score={:.3f}".format(regr.coef_[0][0], regr.intercept_[0],r2score))

xcoord=np.linspace(x.min(),x.max(),100).reshape([-1,1])
y_pred=regr.predict(xcoord)
#regr.__init__()     ### Re-initiate in order to use next time with different data

### Calculate density of data
from scipy.stats import kde

k=kde.gaussian_kde([x,y])
xi,yi=np.mgrid[x.min():x.max():100j,y.min():y.max():100j]
zi=k(np.vstack([xi.flatten(),yi.flatten()]))



###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(10,5)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.05,hspace=0.35,wspace=0.15)  ### Margins, etc.

##-- Title for the page --##
suptit="SLP(t+0) vs. SLP(t-1) Plot"
fig.suptitle(suptit,fontsize=15,y=1.)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

##-- Color Map
cm=plt.cm.get_cmap('viridis'); cm.set_under(color='0.8')

##-- Set up an axis --##
ax1 = fig.add_subplot(1,3,1)   # (# of rows, # of columns, indicater from 1)

pic1 = ax1.scatter(x,y,c=cc,s=5,marker='o',alpha=0.8,cmap=cm)

rline = ax1.plot(xcoord,y_pred,color='k',ls='--',linewidth=2.)
anntxt=r'$R^2={:.3f}$'.format(r2score)
anntxt2='Coef.={:.2f}'.format(regr.coef_[0][0])
ax1.annotate(anntxt,xy=(0.02,0.92),xycoords='axes fraction',ha='left',fontsize=12,stretch='semi-condensed')
ax1.annotate(anntxt2,xy=(0.02,0.85),xycoords='axes fraction',ha='left',fontsize=12,stretch='semi-condensed')

cb=draw_colorbar(ax1,pic1,type='horizontal',size='panel',gap=0.08,width=0.03)

subtit='(a) Scatter+Regression'
ax1.set_title(subtit,fontsize=12,x=0.,ha='left')
ax1.set_xlim(970,992)
ax1.set_ylim(999,1004)
#ax1.set_xticks(xind)
#ax1.set_xticklabels(xlabs[:-4])
#yt_form=FuncFormatter(lambda x, pos: "{:0.0f}%".format(x))
#ax1.yaxis.set_major_formatter(yt_form)

##-- Set up an axis --##
ax2 = fig.add_subplot(1,3,2)   # (# of rows, # of columns, indicater from 1)

pic1 = ax2.scatter(x,y,c=cc,s=5,marker='o',alpha=0.8,cmap=cm)
den1 = ax2.contour(xi,yi,zi.reshape(xi.shape),6,colors='k',linewidths=1.5)



subtit='(b) Scatter+Density'
ax2.set_title(subtit,fontsize=12,x=0.,ha='left')
ax2.set_xlim(970,992)
ax2.set_ylim(999,1004)
ax2.set_yticklabels('')
#ax1.set_xticks(xind)
#ax1.set_xticklabels(xlabs[:-4])
#yt_form=FuncFormatter(lambda x, pos: "{:0.0f}%".format(x))
#ax1.yaxis.set_major_formatter(yt_form)

##-- Set up an axis --##
ax3 = fig.add_subplot(1,3,3)   # (# of rows, # of columns, indicater from 1)

H, xedges, yedges= np.histogram2d(x,y,bins=10)
H=(H/H.sum()*100.).T; print(H.max(),H.mean())
X,Y=np.meshgrid(xedges,yedges)
props = dict(edgecolor='none',alpha=0.8,vmin=0.1,vmax=6,cmap=cm)

pic1 = ax3.pcolormesh(X,Y,H,**props)

cb=draw_colorbar(ax3,pic1,type='horizontal',size='panel',extend='both',gap=0.08,width=0.03)

subtit='(c) 2D Histogram'
ax3.set_title(subtit,fontsize=12,x=0.,ha='left')
ax3.yaxis.tick_right()
#ax3.set_xlim(970,992)
#ax3.set_ylim(999,1004)


ny,nx=H.shape #; maxlocs.append([])
for n in range(ny):
    for m in range(nx):
        if H[n,m]>3.:
            xloc=(xedges[m]+xedges[m+1])/2.
            yloc=(yedges[n]+yedges[n+1])/2.
            ax3.annotate("{:.1f}".format(H[n,m]),xy=(xloc,yloc),ha='center',va='center',stretch='semi-condensed',fontsize=12)



##-- Seeing or Saving Pic --##

#- If want to see on screen -#
plt.show()

#- If want to save to file
outdir = "/home/djin1/Zbegins_Python/Py3_lecture_2019/data/Pics/"
outfnm = outdir+"Scatter+2Dhist1.png"
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
sys.exit()
