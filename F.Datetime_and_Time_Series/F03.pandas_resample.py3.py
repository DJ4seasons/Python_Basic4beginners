



data1 = bin_file_read2mtx(fnm).reshape([ndy,nvars])
#data.append(data1[itidx:itidx+ndays,:])
#df1= pd.DataFrame(data1,index=pd.period_range(tgt_dates[0],freq='D',periods=ndy))
df1= pd.DataFrame(data1,index=pd.date_range(*date_range,freq='D'))
df1= df1.resample('M').mean()
data1= df1.to_numpy().reshape([-1,12,nvars])
ano1= data1-data1.mean(axis=0).reshape([1,12,nvars])
data.append(ano1.reshape([-1,nvars]))
times= df1.index.values #.to_timestamp()
