import sys
import numpy as np
import os.path



###---- Main

##-- Parameters
indir='./data/'
fname=indir+'storm_track.txt'

data=[]; time_info=[]
with open(fname,'r') as f:
    for i,line in enumerate(f):
        words=line.strip().split()
        #print(i,words)

        if i>0:  ### Exclude header
            flos=list(map(float,words[:4]))
            ints=list(map(int,words[4:]))

            data.append(flos)
            time_info.append(ints)



data=np.asarray(data)
time_info=np.asarray(time_info)

print(data.shape, time_info.shape)

###-------------

###--- Linear Regression
from sklearn import linear_model


## For linear-regression
regr=linear_model.LinearRegression()   ### Initiate Regression Object

xdata=data[:,2].reshape([-1,1])  ## wind speed
ydata=data[:,3].reshape([-1,1])  ## surface pressure

regr.fit(xdata,ydata)
r2score=regr.score(xdata,ydata)
print(u"Coeff.={:.2f}, Intercept={:.2f}, R\u00B2 Score={:.3f}".format(regr.coef_[0][0], regr.intercept_[0],r2score))

#y_pred=regr.predict(xcoord)
regr.__init__()     ### Re-initiate in order to use next time with different data

'''
rline = ax1.plot(xcoord,y_pred,color='k',ls='--',linewidth=2.)
anntxt=r'$R^2={:.3f}$'.format(r2score)
anntxt2='Coef.={:.2f}'.format(regr.coef_[0][0])
ax1.annotate(anntxt,xy=(0.02,0.92),xycoords='axes fraction',ha='left',fontsize=12,stretch='semi-condensed')
ax1.annotate(anntxt2,xy=(0.02,0.85),xycoords='axes fraction',ha='left',fontsize=12,stretch='semi-condensed')
'''

###-------------

### Calculate density of data
from scipy.stats import kde

xdata=data[:,2]  ## wind speed
ydata=data[:,3]  ## surface pressure
k=kde.gaussian_kde([xdata,ydata])
xi,yi=np.mgrid[xdata.min():xdata.max():100j,ydata.min():ydata.max():100j]
zi=k(np.vstack([xi.flatten(),yi.flatten()]))

print(zi.shape, zi.argmax())

j,i=np.unravel_index(zi.argmax(),xi.shape)
xloc= xdata.min()+(xdata.max()-xdata.min())/100*i
yloc= ydata.min()+(ydata.max()-ydata.min())/100*j
print("Max Density is {:.05f} when wind speed={:.2f} and pressure={:.2f}".format(zi.max(),xloc,yloc))

'''
den1 = ax2.contour(xi,yi,zi.reshape(xi.shape),6,colors='k',linewidths=1.5)

'''
###-------------

### Write to text file

outdir = indir
outfn = outdir+'text_write_ex1.txt'

##-- Protect existing file
if os.path.isfile(outfn):
    sys.exit("Already Exist: "+outfn)
else:
    with open(outfn,'w') as f:
        header="Longitude, Wind, Year, Month"
        f.write(header+"\n")

        for i in range(data.shape[0]):
            data_txt="{:.2f}, {:.2f}, {:d}, {:02d}".format(data[i,0],data[i,2],time_info[i,0],time_info[i,1])
            f.write(data_txt+"\n")
