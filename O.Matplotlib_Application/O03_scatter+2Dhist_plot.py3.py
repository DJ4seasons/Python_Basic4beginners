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
    uwnd= uwnd.compressed()
    vwnd= vwnd.compressed()
    if uwnd.shape != vwnd.shape:  # Now the shape should be identical
        print("Shapes are not same:", uwnd.shape, vwnd.shape)
        sys.exit()

    outdir= '../Pics/'
    outfn= outdir+'O03_CCMP_Wind_daily_u_vs_v.{}.box+violin.png'.format(date_txt)

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
    fig.set_size_inches(6,8.5)    # Physical page size in inches, (lx,ly)
    fig.subplots_adjust(left=0.06,right=0.94,top=0.92,bottom=0.05,hspace=0.25) #,wspace=0.15)  ### Margins, etc.

    ##-- Title for the page --##
    suptit="CCMP Surface Wind distribution on 2019.01.01"
    fig.suptitle(suptit,fontsize=17,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

    nbins=len(plot_data['data'])
    xind=np.arange(nbins)
    cc=['steelblue','#f07575']

    ##-- Set up an axis --##
    ax1 = fig.add_subplot(2,1,1)   # (# of rows, # of columns, indicater from 1)

    flierprops = dict(marker='.',markerfacecolor='gray',markeredgecolor='none',markersize=3,linestyle='none')
    medianprops = dict(color='k',linewidth=1.5)
    meanprops = dict(marker='x',markeredgecolor='k',markerfacecolor='k',markersize=10,markeredgewidth=2)
    capprops = dict(linewidth=1.5,color='k')
    whiskerprops= dict(linewidth=1.5,linestyle='-')


    boxes=[]
    for i in range(nbins):
        boxprops= dict(facecolor=cc[i],linewidth=1.5)
        box1=ax1.boxplot(plot_data['data'][i],positions=[xind[i],],
                    whis=[5,95],widths=0.6,patch_artist=True,showmeans=True,
                    boxprops=boxprops,flierprops=flierprops,
                    medianprops=medianprops,meanprops=meanprops,
                    capprops=capprops,whiskerprops=whiskerprops)
        boxes.append(box1)

    ax1.legend([box["boxes"][0] for box in boxes], plot_data['var_names'],
                loc='upper right', bbox_to_anchor=[0.99,0.98],
                fontsize=12,framealpha=0.6,borderaxespad=0.)

    subtit='(a) Filled Box Plot'
    data_range= [[wnd.min(),wnd.max()] for wnd in plot_data['data']]
    data_max= np.absolute(np.asarray(data_range)).max()+1
    y_range=[-data_max, data_max]
    plot_common(ax1,subtit,xind,plot_data['var_names'],y_range)

    ##-- Set another axis --##
    ax2 = fig.add_subplot(2,1,2)   # (# of rows, # of columns, indicater from 1)

    violins=[]
    for i in range(nbins):
        vio1=ax2.violinplot(plot_data['data'][i],positions=[xind[i],],
                        points=100, widths=0.6,
                        vert=True, showextrema=True)
        violins.append(vio1)

    markerprops= dict(marker='x',c='k',s=100,linewidth=2,zorder=3)  # 'linewidth', not 'linewidths'
    ax2.scatter(xind,[data.mean() for data in plot_data['data']], **markerprops)

    for b1,b2 in zip(*[vio1['bodies'] for vio1 in violins]):
        b1.set_color(cc[0]); b1.set_alpha(0.9)
        b2.set_color(cc[1]); b2.set_alpha(0.9)

    patches= [mpatches.Patch(color=col) for col in cc]
    ax2.legend(patches, plot_data['var_names'],
                loc='upper right', bbox_to_anchor=[0.99,0.98],
                fontsize=12,framealpha=0.6,borderaxespad=0.)

    subtit='(b) Violin Plot'
    plot_common(ax2,subtit,xind,plot_data['var_names'],y_range)

    ##-- Seeing or Saving Pic --##
    #- If want to see on screen -#
    #plt.show()

    #- If want to save to file
    outfnm= plot_data['outfn']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
    return

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
