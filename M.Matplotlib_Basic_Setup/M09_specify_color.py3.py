'''
Matplotlib Basic(9)
: Introduce various methods to specify color

by Daeho Jin

---
Reference:
https://matplotlib.org/stable/tutorials/colors/colors.html
'''

import numpy as np
import matplotlib.pyplot as plt


###--- Synthesizing data to be plotted ---###
x = np.arange(10)

###---

abc='abcdefghijklmn'
###--- Plotting Start ---###

##-- Page Setup --##
fig = plt.figure()
fig.set_size_inches(8.5,6)    # Physical page size in inches, (lx,ly)

fig.subplots_adjust(left=0.05,right=0.95,top=0.92,bottom=0.05,
                    hspace=0.3,wspace=0.2)  ### Margins, etc.

##-- Title for the page --##
suptit = "Various methods to specify colors"
fig.suptitle(suptit,fontsize=15,va='bottom',y=0.975)  #,ha='left',x=0.,stretch='semi-condensed')

color0= ['b','g','r','c','m','y','k'] #,'w'
color1= ['{:.01f}'.format(val) for val in np.arange(0.,1.,0.15)]
color2= ['C{:d}'.format(val) for val in range(10)]
color3= ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
        'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
color4= ['xkcd:{}'.format(cn) for cn in ['navy','peach','lime','hot pink',
            'lavender','maroon','pale pink','grey blue','sage','baby green' ]]  # https://xkcd.com/color/rgb/
color5= [(0, 191/255, 1), '#00ff00','crimson','aquamarine','mediumseagreen']
#<--- (r,g,b), hex code, or any HTML color names (X11/CSS4 colors)

nrow, ncol= 2,3
for i,colors in enumerate([color0,color1,color3,color4,color5,color2]):
    ##-- Set up an axis --##
    ax1 = fig.add_subplot(nrow,ncol,i+1)   # (# of rows, # of columns, indicater from 1)

    ax1.set_prop_cycle(color=colors)  # Given colors will be repeated; a cycle is defined

    ##-- Plot on an axis --##
    for b in range(-5,6,1):
        ax1.plot(x,x+b,lw=5,alpha=0.9)
        ax1.plot(x,b-x+5,lw=5,alpha=0.9)

    ax1.set_title('({}) Panel#{:d}'.format(abc[i],i+1))
    ax1.set_xlim([-0.1,5])
    ax1.set_ylim([-0.1,5])

##-- Seeing or Saving Pic --##

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"M09_specify_color.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

#- If want to see on screen -#
plt.show()
