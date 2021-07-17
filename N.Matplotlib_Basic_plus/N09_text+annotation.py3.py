'''
Matplotlib Basic_Lv2: 9. Text and Annotation on plot
: Write/Draw text
: Advanced annotation

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.text.html
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.figtext.html
https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.annotate.html
- For mathematical expressions:
https://matplotlib.org/stable/tutorials/text/mathtext.html
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FuncFormatter

###--- Synthesizing data to be plotted ---###
x = np.arange(5)
y = x**2

###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(6,4.5)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.1,right=0.95,top=0.9,bottom=0.1) #,hspace=0.2,wspace=0.15)  ### Margins, etc.

##-- Title for the page --##
suptit="Text and Annotation"
fig.suptitle(suptit,fontsize=15)  #,ha='left',x=0.,y=0.98,stretch='semi-condensed')

##-- Set up axes1 --##
ax1 = fig.add_subplot(1,1,1)   # (# of rows, # of columns, indicater from 1)

##-- Plot on an axes --##
ax1.plot(x,y)

##-- Various Settings for axes --##
subtit='Panel#1'
ax1.set_title(subtit,fontsize=12,x=0.,ha='left') #,y=0.9

ax1.set_xlim(-0.5,4.5)
ax1.xaxis.set_major_locator(MultipleLocator(1))   # For Major Ticks
ax1.xaxis.set_minor_locator(AutoMinorLocator(2))   # For minor Ticks
ax1.set_xlabel('X-axis Label',fontsize=12)

ax1.set_ylim(-1,17)
ax1.set_ylabel('Y-axis Label',fontsize=12,rotation=90,labelpad=0)
ax1.set_yticks(range(0,17,4))
ax1.yaxis.set_minor_locator(AutoMinorLocator(2))

ax1.tick_params(axis='both',labelsize=11)
ax1.axhline(y=0.,color='k',linestyle=':')
ax1.axvline(x=0.,color='k',ls=':',lw=0.5)

##-- Text and Annotation --##
ax1.text(0.,16.,'Normal Text',ha='left',va='center',color='r',fontsize=12)
#<-- Data Coordinate by default. For "axes fraction," set "transform=ax.transAxes"
ax1.annotate('Normal Text by annotate()',xy=(0.1,0.84),xycoords='axes fraction',
            ha='left',va='center',color='b',fontsize=12)

pos1=ax1.get_position().bounds  ##<= (left,bottom,width,height); Fraction in figure
plt.figtext(pos1[0]+pos1[2]*0.15,pos1[1]+pos1[3]*0.7,'Figtext: Text in Pink Box',
            backgroundcolor='pink',color='k',fontsize=12,
            ha='left',va='bottom')   # Figure Coordinate by default

ax1.annotate(r'$y=x^2$', xy=(3., 9.),  xycoords='data',
             xytext=(3.5,4.), textcoords='data', fontsize=12,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.5"))
## Coords: 'figure fraction', 'axes fraction', 'data', etc.
## For numerical expression in Matplotlib, see https://matplotlib.org/stable/tutorials/text/mathtext.html


##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N09_text+annotation_ex1.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
