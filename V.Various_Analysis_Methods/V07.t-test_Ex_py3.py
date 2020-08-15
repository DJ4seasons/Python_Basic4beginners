"""
t-test example

Note: Welch's t-test
Welch's t-test is to test if two populations have equal means.
Welch's t-test is more reliable when the two samples have unequal variance and/or unequal sample size.
https://en.wikipedia.org/wiki/Welch%27s_t-test

---
Data file:  Hadley Centre Sea Ice and Sea Surface Temperature data set (HadISST)
Binary data file(HadISST) was produced by D04 code
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
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from scipy.stats import norm

import V00_Functions as vf

def main():
    ### Get Nino3.4 Index
    yrs= [2015,2019]  # Starting year and ending year
    #Nino3.4 (5N-5S, 170W-120W) [-170,-120,-5,5]
    nn34= vf.get_sst_areamean_from_HadISST([-170,-120,-5,5],yrs)
    ### And other region
    tio= vf.get_sst_areamean_from_HadISST([240,280,-10,0],yrs)
    spo= vf.get_sst_areamean_from_HadISST([-170,-120,-40,-30],yrs)

    nn34= tio
    spo= tio
    r1= np.corrcoef(spo[1:],spo[:-1])[0,1]
    print(-np.log(r1)) # Decorrelation time; vonStorch and Zwiers (1999)
    dof_coef= -np.log(r1)

    # DOF= n*(dt/2/Te), Te= e-folding time; Panofsky and Brier, 1958)
    ac=[]
    test=True
    dt=0
    while test:
        dt+=1
        ac.append(np.corrcoef(spo[dt:],spo[:-dt])[0,1])
        if ac[-1]< 1/np.exp(1):  # e-folding time
            break
    Te= (dt*(ac[dt-2]-1/np.exp(1))+(dt-1)*(1/np.exp(1)-ac[dt-1]))/(ac[dt-2]-ac[dt-1])
    print(Te,1/(2*Te),ac)
    dof_coef= 1/2/Te

    nt= nn34.shape[0]
    nn34_prv, nn34_post= nn34[:24], nn34[24:]
    from scipy import stats
    stat_prv= [nn34_prv.mean(), nn34_prv.std(ddof=1), 24*dof_coef]
    stat_post= [nn34_post.mean(), nn34_post.std(ddof=1), (nt-24)*dof_coef]
    print(stats.ttest_ind_from_stats(*stat_prv, *stat_post, equal_var=False))

    return

def get_dof_coef_log_r1(ts1d):
    '''
    Estimating decorrelating time using auto-correlation, r1
    dof_coef= -np.log(r1)  # vonStorch and Zwiers (1999)
    '''
    r1= np.corrcoef(ts1d[1:],ts1d[:-1])[0,1]
    return -np.log(r1)

def get_dof_coef_e_folding(ts1d):
    '''
    DOF= n*(dt/2/Te), Te= e-folding time; Panofsky and Brier, 1958)
    '''
    ac=[]
    test=True
    it=0
    while test:
        it+=1
        ac.append(np.corrcoef(ts1d[it:],ts1d[:-it])[0,1])
        if ac[-1]< 1/np.exp(1):  # e-folding time
            break
    ### Linearly interpolating
    Te= (it*(ac[it-2]-1/np.exp(1))+(it-1)*(1/np.exp(1)-ac[it-1]))/(ac[it-2]-ac[it-1])
    return 1/2/Te

if __name__ == "__main__":
    main()
