def get_nn34_daily(tgt_dates):
    indir = '/Users/djin1/Documents/CLD_Work/Data_Obs/'
    infn_nn34= indir+'SST_index/nino3.4_anom.1870-2020.txt'  ### Monthly anomaly
    tdd0= tgt_dates[0]-timedelta(days=27)
    tdd1= tgt_dates[1]+timedelta(days=27)
    nn34ano= read_nn34_text(infn_nn34,(tdd0,tdd1))
    print(nn34ano.shape, nn34ano.mean())

    nn34ano_dy= Interp_mon2day(nn34ano,tgt_dates,(tdd0,tdd1))
    return nn34ano_dy

from scipy.interpolate import interp1d
def Interp_mon2day(vals,tgt_dates,val_dates):
    ### Interpolate Monthly data to Daily data
    ### vals: 1-D, including 1 month earlier and later than tdates

    xx=[]
    iyr,imon= val_dates[0].year, val_dates[0].month
    mdays=0
    for yy in range(iyr,val_dates[1].year+1,1):
        imm=imon if yy==iyr else 1
        for mm in range(imm,13,1):
            mm2=mm+1
            if mm2>12:
                mm2-=12; yy2=yy+1
            else:
                yy2=yy

            dy_per_mon=(date(yy2,mm2,1)-date(yy,mm,1)).days
            xx.append(dy_per_mon/2+0.5+mdays)
            mdays+=dy_per_mon
            if mm==val_dates[1].month and yy==val_dates[1].year: break
    xx=np.asarray(xx)
    print(vals.shape,xx.shape)

    f= interp1d(xx,vals,kind='cubic')

    itidx= (tgt_dates[0]-date(iyr,imon,1)).days
    etidx= (tgt_dates[1]-date(iyr,imon,1)).days+1
    xnew= np.arange(itidx,etidx,1)
    f2= f(xnew)
    print(f2.shape)
    return f2
