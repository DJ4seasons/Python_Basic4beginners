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

from scipy import stats

import V00_Functions as vf

def main():
    ### Get Nino3.4 Index
    yrs= [2015,2019]  # Starting year and ending year
    #Nino4 (5N-5S, 160E-150W) [160,210,-5,5]
    #Nino3.4 (5N-5S, 170W-120W) [-170,-120,-5,5]
    nn34= vf.get_sst_areamean_from_HadISST([-170,-120,-5,5],yrs,remove_AC=True)
    ### And other region
    tio= vf.get_sst_areamean_from_HadISST([240,280,-10,0],yrs,remove_AC=True)
    spo= vf.get_sst_areamean_from_HadISST([-170,-120,-40,-30],yrs,remove_AC=True)

    data= [nn34, tio, spo]
    var_names= ['Ni{}o3.4'.format('\u00F1'), 'Trop_IO', 'S_Pacific']

    dof_coef1= [get_dof_coef_log_r1(ts) for ts in data]
    dof_coef2= [get_dof_coef_e_folding(ts) for ts in data]

    get_stat= lambda ts, dof_coef: [ts.mean(), ts.std(ddof=1), len(ts)*dof_coef]

    print("\n{} vs. {}".format(var_names[0], var_names[1]))
    t1,p1= stats.ttest_ind_from_stats(*get_stat(data[0],dof_coef1[0]), *get_stat(data[1],dof_coef1[1]), equal_var=False)
    t2,p2= stats.ttest_ind_from_stats(*get_stat(data[0],dof_coef2[0]), *get_stat(data[1],dof_coef2[1]), equal_var=False)
    print("DoF1= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(len(data[0])*dof_coef1[0], len(data[1])*dof_coef1[1], t1, p1))
    print("DoF2= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(len(data[0])*dof_coef2[0], len(data[1])*dof_coef2[1], t2, p2))

    print("\n{} vs. {}".format(var_names[0], var_names[2]))
    t1,p1= stats.ttest_ind_from_stats(*get_stat(data[0],dof_coef1[0]), *get_stat(data[2],dof_coef1[2]), equal_var=False)
    t2,p2= stats.ttest_ind_from_stats(*get_stat(data[0],dof_coef2[0]), *get_stat(data[2],dof_coef2[2]), equal_var=False)
    print("DoF1= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(len(data[0])*dof_coef1[0], len(data[2])*dof_coef1[2], t1, p1))
    print("DoF2= {:.2f}, {:.2f}: t={:.2f}, p={:.3f}".format(len(data[0])*dof_coef2[0], len(data[2])*dof_coef2[2], t2, p2))

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
