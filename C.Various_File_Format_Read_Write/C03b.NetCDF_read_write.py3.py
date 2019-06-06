"""
Read NC files of 4 variables, and write a NC file all together

Input files:
data/slp_wrfout_d01_2018-02-17_00-00-00.nc
data/hgt_1000hPa_wrfout_d01_2018-02-17_00-00-00.nc
data/hgt_500hPa_wrfout_d01_2018-02-17_00-00-00.nc
data/hgt_200hPa_wrfout_d01_2018-02-17_00-00-00.nc

Every 6 hours for 3 days

"""


import sys
import numpy as np
import os.path
from subprocess import call
from datetime import timedelta, date, datetime
from netCDF4 import Dataset, date2num

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

###--- Parameters
start_date = date(2018,2,17)  ### Start Date
end_date = date(2018,2,20)   ### Including this End Date

vars = ['slp','hgt_1000hPa','hgt_500hPa','hgt_200hPa']
dim_names = ['XLAT','XLONG']
indir = './data/'
outdir = indir

for oneday in daterange(start_date,end_date):
    dd=oneday.strftime('%Y-%m-%d')

    file_test=False
    f_ids=[]
    for tt in range(0,24,6):
        f_ids.append([])
        for vv in vars:
            infn=indir+'{}_wrfout_d01_{}_{:02d}-00-00.nc'.format(vv,dd,tt)
            #nc_f=open_netcdf(infn)
            if not os.path.isfile(infn):
                print(infn+" not available")
                file_test=True
                break
            else:
                fid=Dataset(infn,'r')
                f_ids[-1].append(fid)


    if file_test:
        sys.exit("Files are incomplete on {}".format(dd))
    else:
        f_id_tmp= f_ids[0][0]
        dims = f_id_tmp.variables[vars[0].upper()].dimensions
        lats = f_id_tmp.variables['XLAT'][:]
        if lats.shape[0]==1:
            lats=lats.reshape(lats.shape[1:])
        lons = f_id_tmp.variables['XLONG'][:]
        if lons.shape[0]==1:
            lons=lons.reshape(lons.shape[1:])
        print(dims,type(lons),lons.shape)


        times = [datetime(oneday.year,oneday.month,oneday.day)+n*timedelta(hours=6) for n in range(len(f_ids))]
        print(times)

        data=[]
        for fids in f_ids:
            for i,fid in enumerate(fids):
                vname=vars[i].split('_')[0].upper()
                if i==0:
                    temp=fid.variables[vname][:]
                else:
                    temp=np.concatenate((temp,fid.variables[vname][:]))

            print(vars[i],temp.shape)
            data.append(temp)

        data=np.asarray(data).astype(np.float32)
        print(data.shape)



        ### Ready to Create a daily NC file
        outfn=outdir+'wrfout_d01_{}.nc'.format(dd)
        ncfw= Dataset(outfn, "w", format="NETCDF4")

        ## Dimensions
        ln=ncfw.createDimension('lon',lons.shape[0])
        lt=ncfw.createDimension('lat',lats.shape[1])
        lv=ncfw.createDimension('lev',3)
        tm=ncfw.createDimension('time',len(times))

        lonsnc = ncfw.createVariable('lon','f4',('lon','lat',))
        latsnc = ncfw.createVariable('lat','f4',('lat','lat',))
        levsnc = ncfw.createVariable('lev','f4',('lev',))
        timenc = ncfw.createVariable('time','f8',('time',))

        lonsnc[:]=lons; latsnc[:]=lats
        lonsnc.units = 'degrees_east'; latsnc.units = 'degrees_north'
        levsnc[:]=[1000,500,200]
        levsnc.units = 'hPa'

        timenc.units = 'hours since 0001-01-01 00:00:00.0'
        timenc.calendar = 'gregorian'
        timenc[:] = date2num(times, timenc.units, calendar=timenc.calendar)

        ## Data variables
        slpnc = ncfw.createVariable('SLP','f4',('time','lat','lon'))
        slpnc[:] = data[:,0,:,:]
        hgtnc = ncfw.createVariable('HGT','f4',('time','lev','lat','lon'))
        hgtnc[:] = data[:,1:,:,:]

        ## Attributions
        ncfw.description = 'Model output on {}'.format(dd)

        ## Close file
        print("{} is written.".format(outfn))
        ncfw.close()
