'''
Matplotlib Basic(1)
: Make sure the concept of "figure," "axes," and "axis."
: Define and Set up a figure
: Define an axes in a figure
: Draw a simple line plot
: Save the plot with some options

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/tutorials/introductory/usage.html
'''

import numpy as np
import matplotlib.pyplot as plt

###--- Synthesizing data to be plotted ---###
x = np.arange(5)
y = x**2

#for x1,y1 in zip(x,y):
#    print(x1,y1)
###---


###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()  # https://matplotlib.org/stable/api/figure_api.html
fig.set_size_inches(4.5,6)    # Physical page size in inches, (lx,ly)

##-- Title for the page --##
suptit="Single Panel Setting"
fig.suptitle(suptit,fontsize=15)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

##-- Set up axis1 --##
ax1 = fig.add_subplot(1,1,1)   # (# of rows, # of columns, indicater from 1)
### These are also working:
#ax1 = fig.add_subplot()
#ax1 = fig.add_subplot(111)

##-- Plot on an axis --##
ax1.plot(x,y)

##-- Seeing or Saving Pic --##
#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"M01_single_panel1.png"
print(outfnm)
fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
#fig.savefig(outfnm,dpi=100,facecolor='0.8')
#fig.savefig(outfnm,dpi=100,facecolor='0.8',transparent=True)
#fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
