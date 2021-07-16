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
xx = yy = np.arange(4)+0.5
xx = np.tile(xx,4)
yy = np.repeat(yy,4)

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

color0= []  # Defalut is from tab10, or accesses by 'C0', 'C1', ..., 'C9' (CN colors)
color1= ['b','g','r','c','m','y','k'] #,'w'
color2= ['{:.01f}'.format(val) for val in np.arange(0.,1.,0.15)]
color3= ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']  # From colormap "tab10"
color3+= ['xkcd:{}'.format(cn) for cn in ['maroon','pale pink','grey blue','sage','baby green' ]]
# https://xkcd.com/color/rgb/
color4= [(0, 191/255, 1), (1,0.5,0.1),'#00ff00','#c5b0d5','crimson','aquamarine','mediumseagreen']
#<--- (r,g,b), hex code, or any HTML color names (X11/CSS4 colors)

### Pick colors from pre-defined colormap
### https://matplotlib.org/stable/tutorials/colors/colormaps.html
cmap= plt.cm.get_cmap('magma',10)  # Default: 256 RGBA list
cmap= cmap(np.arange(10))  # Results in np.ndarray, [10,4]
color5= list(cmap)

panel_names= ['Default (=tab10)','Simple Alphabet', 'Gray Scale', 'Tab and xkcd colors',
            'RGB, Hex, or C-names', 'From Colormap (magma)']
nrow, ncol= 2,3
for i,(tit,colors) in enumerate(zip(panel_names,[eval('color'+str(num)) for num in range(6)])):
    ##-- Set up an axes --##
    ax1 = fig.add_subplot(nrow,ncol,i+1)   # (# of rows, # of columns, indicater from 1)

    if len(colors)!=0:
        ax1.set_prop_cycle(color=colors)  # Given colors will be repeated; a cycle is defined

    ##-- Plot on an axes --##
    for x1,y1 in zip(xx,yy):
        ax1.plot(x1,y1,marker='s',markersize=30)


    ax1.set_title('({}) {}'.format(abc[i],tit),ha='left',x=0.,fontsize=12)
    ax1.set_xlim([0,4])
    ax1.set_ylim([0,4])

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
