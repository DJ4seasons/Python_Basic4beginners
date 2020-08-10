'''
Matplotlib Basic(3)
: Produce multi-panels using fig.add_subplot()

by Daeho Jin

---
Reference:
https://matplotlib.org/3.3.0/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.add_subplot
https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html
'''

import numpy as np
import matplotlib.pyplot as plt


###--- Synthesizing data to be plotted ---###
x = np.arange(5)
y = x**2

#for x1,y1 in zip(x,y):
#    print(x1,y1)
###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(8.5,6)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.05,hspace=0.3,wspace=0.2)  ### Margins, etc.

##-- Title for the page --##
suptit="Multi-Panel Setting"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

axes=[]
axes.append(fig.add_subplot(2,2,1))
axes.append(fig.add_subplot(2,4,3))
axes.append(fig.add_subplot(4,4,4))
axes.append(fig.add_subplot(4,4,8))
axes.append(fig.add_subplot(4,1,3))

##-- Plot on an axis --##
for i,ax1 in enumerate(axes):
    ax1.plot(x,y,color='{:.1f}'.format(i/5))
    ax1.set_title('({}) Panel#{:d}'.format(abc[i],i+1))


##-- Seeing or Saving Pic --##

#- If want to see on screen -#
plt.show()

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"M03c_multi_panel1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
