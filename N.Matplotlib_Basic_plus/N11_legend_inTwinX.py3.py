'''
Matplotlib Basic_Lv2: 11. Legend in twinx setting
: Draw legend in the case of twinx()

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/axes_api.html#twinning-and-sharing
https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html
https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.legend
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter


###--- Synthesizing data to be plotted ---###
x = np.arange(1,5,0.5)
y1 = 1/x
y2 = x**2

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(6,9)    # Physical page size in inches, (lx,ly)

##-- Title for the page --##
suptit="Legend example in twinx() condition"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

fig.subplots_adjust(left=0.1,right=0.95,top=0.94,bottom=0.07,hspace=0.3)

nrow, ncol= 3,1

###--- Panel1: Two lines in one axes
ax1 = fig.add_subplot(nrow,ncol,1)
line1=ax1.plot(x,y1,marker='^',label='1/x')  # plotting line graph1
line2=ax1.plot(x,y2,marker='o',label='x^2')  # plotting line graph2
subtit= '(a) Two lines in one axes'
ax1.set_title(subtit,fontsize=13,x=0,ha='left')
ax1.legend(loc='best')

###--- Panel2: Applying twinx()
ax2 = fig.add_subplot(nrow,ncol,2)
ax2b = ax2.twinx()  # New axes shares the x-axis of ax1

line1=ax2.plot(x,y1,marker='^',label='1/x')  # plotting line graph1
line2=ax2b.plot(x,y2,marker='o',label='x^2')  # plotting line graph2
subtit= '(b) Two lines in x-shared axes'
ax2.set_title(subtit,fontsize=13,x=0,ha='left')
ax2.legend(loc='best')
ax2b.legend(loc='best')

###--- Panel3: Same twinx() but with legend handler
ax3 = fig.add_subplot(nrow,ncol,3)
ax3b = ax3.twinx()  # New axes shares the x-axis of ax1

line1=ax3.plot(x,y1,marker='^',label='1/x')  # plotting line graph1
line2=ax3b.plot(x,y2,marker='o',label='x^2')  # plotting line graph2
subtit= '(c) Two lines in x-shared axes'
ax3.set_title(subtit,fontsize=13,x=0,ha='left')

## Combine two legend boxes
lines, labels = ax3.get_legend_handles_labels()
lines2, labels2 = ax3b.get_legend_handles_labels()
ax3.legend(lines + lines2, labels + labels2, loc='upper center', ncol=2)

###--- Legend for whole figure
fig.legend(bbox_to_anchor=(0.5, 0.03), loc='upper center',fontsize=11,
           ncol=3, borderaxespad=0.)


##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N11_legend_inTwinX_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
