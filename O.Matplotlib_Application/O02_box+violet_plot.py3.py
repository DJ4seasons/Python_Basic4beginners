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
import matplotlib.patches as mpatches

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

def setBoxColors(bp,cn1):
    from matplotlib.pyplot import setp

    #print len(bp['caps']),len(bp['fliers'])
    k=len(bp['fliers'])
    for i in range(k):
        i2=i*2
        setp(bp['boxes'][i], color=cn1,linewidth=1.5)
        setp(bp['caps'][i2], color=cn1,linewidth=1.5)
        setp(bp['caps'][i2+1], color=cn1,linewidth=1.5)
        setp(bp['whiskers'][i2], color=cn1,linewidth=1.5)
        setp(bp['whiskers'][i2+1], color=cn1,linewidth=1.5)
        setp(bp['fliers'][i], color=cn1,marker='.',markersize=2)
        setp(bp['medians'][i], color='k',linewidth=1.5)


###--- Prepare Data ---###
var1,var2 = 'hgt_200hPa','hgt_500hPa'
dim_names = ['XLAT','XLONG']
indir = '/home/djin1/Zbegins_Python/Py3_lecture_2019/data/'

start_date = date(2018,2,17)  ### Start Date
end_date = date(2018,2,19)   ### Including this End Date

abc='abcdefghijklmn'


data1=[]; data2=[]; days=[]
for oneday in daterange(start_date,end_date):
    dd=oneday.strftime('%Y-%m-%d')
    days.append(dd)

    infn=indir+'{}_wrfout_d01_{}_12-00-00.nc'.format(var1,dd)
    fid=open_netcdf(infn)
    #if oneday==start_date:
    #    lats=read_nc_variable(fid,'XLAT')
    #    lons=read_nc_variable(fid,'XLONG')
    vname=var1.split('_')[0].upper()
    data=read_nc_variable(fid,vname)
    data1.append(data.reshape(-1)[::50])

    infn=indir+'{}_wrfout_d01_{}_12-00-00.nc'.format(var2,dd)
    fid=open_netcdf(infn)
    vname=var2.split('_')[0].upper()
    data=read_nc_variable(fid,vname)
    data2.append(data.reshape(-1)[::50])



###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(8.5,8.5)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.06,right=0.94,top=0.92,bottom=0.05,hspace=0.35,wspace=0.15)  ### Margins, etc.

##-- Title for the page --##
suptit="Box Plot + Violet Plot"
fig.suptitle(suptit,fontsize=15)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

nbins=len(data1)
xind=np.arange(nbins)
cc=['deeppink','skyblue','gold','0.7']

##-- Set up an axis --##
ax1 = fig.add_subplot(3,1,1)   # (# of rows, # of columns, indicater from 1)
ax1b= ax1.twinx()

flierprops = dict(marker='.',markerfacecolor='gray',markeredgecolor='none',markersize=3,linestyle='none')
medianprops = dict(color='k',linewidth=1.5)
meanprops = dict(marker='x',markeredgecolor='k',markerfacecolor='k',markersize=10,markeredgewidth=2)
capprops = dict(linewidth=1.5,color='k')
whiskerprops=dict(linewidth=1.5,linestyle='-')

box1=ax1.boxplot(data1,whis=[5,95],widths=0.25,positions=xind-0.15,patch_artist=True,showmeans=True,flierprops=flierprops,boxprops=dict(facecolor='lightblue',linewidth=1.5),medianprops=medianprops,meanprops=meanprops,capprops=capprops,whiskerprops=whiskerprops)
box2=ax1b.boxplot(data2,whis=[5,95],widths=0.25,positions=xind+0.15,patch_artist=True,showmeans=True,flierprops=flierprops,boxprops=dict(facecolor='pink',linewidth=1.5),medianprops=medianprops,meanprops=meanprops,capprops=capprops,whiskerprops=whiskerprops)

ax1.legend([box1["boxes"][0],box2["boxes"][0]], [var1,var2], bbox_to_anchor=(0.5,0.98,.49,.1),loc=3,ncol=2,mode='expand',fontsize=12,framealpha=0.6,borderaxespad=0.)


subtit='(a) Filled Box Plot'
ax1.set_title(subtit,fontsize=12,x=0.,ha='left')
ax1.set_xticks(xind)
ax1.set_xticklabels(days)
ax1.set_xlim(xind[0]-0.5,xind[-1]+0.5)
#yt_form=FuncFormatter(lambda x, pos: "{:0.0f}%".format(x))
#ax1.yaxis.set_major_formatter(yt_form)
ax1.set_ylim(12400,12510)
ax1b.set_ylim(5600,6000)


##-- Set another axis --##
ax2 = fig.add_subplot(3,1,2)   # (# of rows, # of columns, indicater from 1)
ax2b= ax2.twinx()

vio1=ax2.violinplot(data1,positions=xind-0.15,points=100,showextrema=True,widths=0.25)
vio2=ax2b.violinplot(data2,positions=xind+0.15,points=100,showextrema=False,widths=0.25)

for b1,b2 in zip(vio1['bodies'],vio2['bodies']):
    b1.set_color('lightblue'); b1.set_alpha(0.9)
    b2.set_color('pink'); b2.set_alpha(0.9)

patch1= mpatches.Patch(color='lightblue')
patch2= mpatches.Patch(color='pink')
ax2.legend([patch1,patch2], [var1,var2], bbox_to_anchor=(0.5,0.98,.49,.1),loc=3,ncol=2,mode='expand',fontsize=12,framealpha=0.6,borderaxespad=0.)


subtit='(b) Violin Plot'
ax2.set_title(subtit,fontsize=12,x=0.,ha='left')
ax2.set_xticks(xind)
ax2.set_xlim(xind[0]-0.5,xind[-1]+0.5)
ax2.set_xticklabels(days)
ax2.set_ylim(12400,12510)
ax2b.set_ylim(5600,6000)


##-- Set another axis --##
ax3 = fig.add_subplot(3,1,3)   # (# of rows, # of columns, indicater from 1)
ax3b= ax3.twinx()

vio1=ax3.violinplot(data1,positions=xind,points=100,showextrema=False,widths=0.5)
vio2=ax3b.violinplot(data2,positions=xind,points=100,showextrema=False,widths=0.5)

for b1,b2 in zip(vio1['bodies'],vio2['bodies']):
    b1.set_color('lightblue'); b1.set_alpha(0.9)
    m = np.mean(b1.get_paths()[0].vertices[:, 0])
    b1.get_paths()[0].vertices[:, 0] = np.clip(b1.get_paths()[0].vertices[:, 0], -np.inf, m)

    b2.set_color('pink'); b2.set_alpha(0.9)
    m = np.mean(b2.get_paths()[0].vertices[:, 0])
    b2.get_paths()[0].vertices[:, 0] = np.clip(b2.get_paths()[0].vertices[:, 0], m, np.inf)

patch1= mpatches.Patch(color='lightblue')
patch2= mpatches.Patch(color='pink')
ax3.legend([patch1,patch2], [var1,var2], bbox_to_anchor=(0.5,0.98,.49,.1),loc=3,ncol=2,mode='expand',fontsize=12,framealpha=0.6,borderaxespad=0.)

flierprops = dict(marker='.',markerfacecolor='gray',markeredgecolor='none',markersize=3,linestyle='none')
box1=ax3.boxplot(data1,whis=[5,95],widths=0.15,positions=xind-0.12,patch_artist=False,flierprops=flierprops)
box2=ax3b.boxplot(data2,whis=[5,95],widths=0.15,positions=xind+0.12,patch_artist=False,flierprops=flierprops)

#setBoxColors(box1,'lightblue')
#setBoxColors(box2,'pink')

subtit='(c) Half-Violin Plot'
ax3.set_title(subtit,fontsize=12,x=0.,ha='left')
ax3.set_xticks(xind)
ax3.set_xlim(xind[0]-0.5,xind[-1]+0.5)
ax3.set_xticklabels(days)
ax3.set_ylim(12400,12510)
ax3b.set_ylim(5600,6000)


##-- Seeing or Saving Pic --##

#- If want to see on screen -#
plt.show()

#- If want to save to file
outdir = "/home/djin1/Zbegins_Python/Py3_lecture_2019/data/Pics/"
outfnm = outdir+"Box+violet1.png"
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
sys.exit()
