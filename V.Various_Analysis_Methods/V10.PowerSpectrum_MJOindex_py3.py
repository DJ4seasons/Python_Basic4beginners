"""
Calculate power spectrum to show doninant periodicity

---
Data file:  Real-Time Multivariate MJO(RMM) Index
Source: http://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt
Referece: Wheeler, M. C., and H. H. Hendon, 2004: An all-season real-time multivariate MJO index: Development of
an index for monitoring and prediction. Mon. Wea. Rev., 132, 1917-1932. doi:10.1175/1520-0493(2004)132<1917:AARMMI>2.0.CO;2

Daeho Jin
"""

import sys
import os.path
import numpy as np
from datetime import date

import V00_Functions as vf

def main():
    ### Get RMM index
    tgt_dates=(date(2015,1,1),date(2019,12,31))  # Recent 5 years
    time_info, pcs, phs, strs, miss_idx= vf.read_rmm_text(tgt_dates)

    ### Assume that there is no missings

    ###--- Parameters
    tgt_dates=(date(2010,1,1),date(2019,12,31))  # Recent 10 years

    ### Read RMM data
    times,pcs,phs=read_rmm_text(infn,tgt_dates)
    print(pcs.shape) ### Check the dimension

    ### Check missing
    miss_idx= phs==999
    if miss_idx.sum()>0:
        print("There are missings:", miss_idx.sum())
        sys.exit()
    else:
        print("No missings")

    ### Calculate strength from PCs
    strs= np.sqrt((pcs**2).sum(axis=1))  # Euclidean distance
    print(strs.min(),strs.max()) ### Check the range of strength

    ### Data collected
    data= [pcs[:,0], pcs[:,1], strs]
    var_names= ['RMM1','RMM2','Amp']

    outdir= '../Pics/'
    out_fig_nm= outdir+'X0x.power_spectrum_RMM.png'
    plot_data= dict(data=data, var_names=var_names, out_fnm=out_fig_nm)
    plot_PS(plot_data)

    return


###---
### Calculate power spectrum and plot it
###---
from scipy.signal import welch  # For power spectrum
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FixedLocator

def plot_PS(pdata):
    ###--- Create a figure
    fig=plt.figure()
    fig.set_size_inches(5,4)  ## (xsize,ysize)

    ###--- Suptitle
    suptit="Power Spectral Density of MJO Index [2010-19]"
    fig.suptitle(suptit,fontsize=14,y=0.95,va='bottom',stretch='semi-condensed')

    c= ['b','r','g']

    ax1= fig.add_subplot(111)

    for i, (data,vnm) in enumerate(zip(pdata['data'],pdata['var_names'])):
        freqs, psd = welch(data)
        ax1.semilogx(freqs, psd,color=c[i],label=vnm)

    ax1.set_xlabel('Frequency',fontsize=11)
    ax1.set_ylabel('Power',fontsize=11)
    ax1.tick_params(axis='both',labelsize=10)
    ax1.legend(loc='upper right',fontsize=10)
    ax1.axvline(x=1/40,ls='--',lw=0.6,c='k')
    ax1.axvline(x=1/60,ls='--',lw=0.6,c='k')

    ### x-axis: period instead of frequency
    #xtloc= [0.005,0.01,0.02,0.05,0.1,0.2]  # in freq
    #xtlab= [int(np.rint(1/x)) for x in xtloc]
    #ax1.set_xticks(xtloc)
    #ax1.set_xticklabels(xtlab)
    #ax1.set_xlabel('Period in days',fontsize=11)

    ##-- Seeing or Saving Pic --##
    plt.show()

    #- If want to save to file
    outfnm = pdata['out_fnm']
    print(outfnm)
    #fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
    #fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

    # Defalut: facecolor='w', edgecolor='w', transparent=False
    return


if __name__ == "__main__":
    main()
