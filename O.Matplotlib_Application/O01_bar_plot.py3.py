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

histdata=[]; days=[]
for oneday in daterange(start_date,end_date):
    dd=oneday.strftime('%Y-%m-%d')
    days.append(dd)

    infn=indir+'{}_wrfout_d01_{}_12-00-00.nc'.format(var,dd)
    fid=open_netcdf(infn)
    #if oneday==start_date:
    #    lats=read_nc_variable(fid,'XLAT')
    #    lons=read_nc_variable(fid,'XLONG')

    data=read_nc_variable(fid,var.upper())
    hist,b=np.histogram(data,bins=bins)
    hist=hist/hist.sum()*100.
    histdata.append(hist[:-4])




###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(8.5,6)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.05,hspace=0.35,wspace=0.15)  ### Margins, etc.

##-- Title for the page --##
suptit="SLP Bar Plot"
fig.suptitle(suptit,fontsize=15)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

nbins=len(bins)-1
xind=np.arange(nbins)[:-4]
width=0.28
cc=['deeppink','skyblue','gold','0.7']

##-- Set up an axis --##
ax1 = fig.add_subplot(2,1,1)   # (# of rows, # of columns, indicater from 1)

pp=[]
for i,hh in enumerate(histdata):
    ##-- Plot on an axis --##
    pic1=ax1.bar(xind+width*i,histdata[i],width,color=cc[i])
    pp.append(pic1[0])

subtit='(a) Starndard Bar'
ax1.set_title(subtit,fontsize=12,x=0.,ha='left')
ax1.set_xticks(xind)
ax1.set_xticklabels(xlabs[:-4])
yt_form=FuncFormatter(lambda x, pos: "{:0.0f}%".format(x))
ax1.yaxis.set_major_formatter(yt_form)

ax1.legend(pp,days,bbox_to_anchor=(0.02,0.98),loc=2,borderaxespad=0.,fontsize=10)

##-- Set up another axis --##
ax2 = fig.add_subplot(2,1,2)   # (# of rows, # of columns, indicater from 1)

pp=[]; bottom=np.zeros_like(histdata[0])
for i,hh in enumerate(histdata):
    ##-- Plot on an axis --##
    pic1=ax2.bar(xind,histdata[i],width,bottom=bottom,color=cc[i])
    bottom+=histdata[i]
    pp.append(pic1[0])

subtit='(b) Stacked Bar'
ax2.set_title(subtit,fontsize=12,x=0.,ha='left')
ax2.set_xticks(xind)
ax2.set_xticklabels(xlabs)
yt_form=FuncFormatter(lambda x, pos: "{:0.0f}%".format(x))
ax2.yaxis.set_major_formatter(yt_form)

ax2.legend(pp,days,bbox_to_anchor=(0.02,0.98),loc=2,borderaxespad=0.,fontsize=10)


##-- Seeing or Saving Pic --##

#- If want to see on screen -#
plt.show()

#- If want to save to file
outdir = "/home/djin1/Zbegins_Python/Py3_lecture_2019/data/Pics/"
outfnm = outdir+"Bar_ex1.png"
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
sys.exit()
