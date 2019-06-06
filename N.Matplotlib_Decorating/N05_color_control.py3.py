import sys
import numpy as np

import matplotlib   ### Discover Only
matplotlib.use('TkAgg')   ### Discover Only

import matplotlib.pyplot as plt
import matplotlib.colors as cls
#from matplotlib.ticker import AutoMinorLocator, MultipleLocator

def draw_colorbar(ax,pic1,type='vertical',size='panel',gap=0.06,width=0.02,extend='neither'):
    '''
    Type: 'horizontal' or 'vertical'
    Size: 'page' or 'panel'
    Gap: gap between panel(axis) and colorbar
    Extend: 'both', 'min', 'max', 'neither'
    '''
    pos1=ax.get_position().bounds  ##<= (left,bottom,width,height)
    if type.lower()=='vertical' and size.lower()=='page':
        cb_ax =fig.add_axes([pos1[0]+pos1[2]+gap,0.1,width,0.8])  ##<= (left,bottom,width,height)
    elif type.lower()=='vertical' and size.lower()=='panel':
        cb_ax =fig.add_axes([pos1[0]+pos1[2]+gap,pos1[1],width,pos1[3]])  ##<= (left,bottom,width,height)
    elif type.lower()=='horizontal' and size.lower()=='page':
        cb_ax =fig.add_axes([0.1,pos1[1]-gap,0.8,width])  ##<= (left,bottom,width,height)
    elif type.lower()=='horizontal' and size.lower()=='panel':
        cb_ax =fig.add_axes([pos1[0],pos1[1]-gap,pos1[2],width])  ##<= (left,bottom,width,height)
    else:
        print('Error: Options are incorrect:',type,size)
        return
    
    cbar=fig.colorbar(pic1,cax=cb_ax,extend=extend,orientation=type)  #,ticks=[0.01,0.1,1],format='%.2f')
    cbar.ax.tick_params(labelsize=10)
    return cbar



###--- Synthesizing data to be plotted ---###
xlin = np.linspace(-2,4,121)
ylin = np.linspace(-3,5,161)    
X,Y = np.meshgrid(xlin,ylin)
Z = 1./(np.exp((X/3.)**2+(Y/5.)**2))

cmap_names=['viridis','plasma','inferno','magma','magma_r','YlOrBr', 'RdPu', 'YlGnBu', 'bone', 'spring', 'cool', 'hot', 'PuOr', 'seismic', 'terrain', 'CMRmap', 'rainbow', 'nipy_spectral', 'jet']



###--- Plotting Start ---###
##-- Page Setup --##
fig = plt.figure()            # Define "figure" instance
fig.set_size_inches(10,11)    # Physical page size in inches, (lx,ly)
suptit="Color Map Example"
fig.suptitle(suptit,fontsize=18)   # Title for the page
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.92,wspace=-0.1,hspace=0.25)

##-- Plotting for axis1 --##
for i in range(20):
    ax = fig.add_subplot(4,5,i+1)   # subplot(# of rows, # of columns, indicater)

    if i<19:
        subtit='({}) {}'.format(i+1,cmap_names[i])
        pic1 = ax.imshow(Z,origin='lower',cmap=cmap_names[i],interpolation='nearest')     
        if i==18:
            cb=draw_colorbar(ax,pic1,type='horizontal',size='page')
 
    else:
        subtit='({}) part of jet'.format(i+1)
        cm = plt.cm.get_cmap('jet',100)
        cmnew = cm(np.arange(100))[25:75,:]
        newcm = cls.LinearSegmentedColormap.from_list("middle_jet",cmnew)
        newcm.set_under("1.");newcm.set_over("0.")

        props = dict(vmin=0.1,vmax=.9,cmap=newcm,alpha=0.9,interpolation='nearest')
        pic1 = ax.imshow(Z,origin='lower',**props)   

        cb=draw_colorbar(ax,pic1,type='vertical',size='panel',extend='both',gap=0.02)
        cb_yt=np.arange(0.1,1.,0.2); cb_ytl=["a{:.1f}".format(x) for x in cb_yt]
        cb.set_ticks(cb_yt)
        cb.ax.set_yticklabels(cb_ytl,size=12,color='b',stretch='semi-condensed')
    
    ax.set_title(subtit,fontsize=12,x=0.,ha='left')
    ax.set_xticks(np.linspace(0,len(xlin)-1,4))
    ax.set_xticklabels([-2,0,2,4])
    ax.set_yticks(np.linspace(0,len(ylin)-1,5))
    ax.set_yticklabels([-3,-1,1,3,5])
    ax.tick_params(axis='both',which='major',labelsize=10)



##-- Seeing or Saving Pic --##
plt.show()

#- If want to save to file
outdir = "/home/djin1/Zbegins_Python/Py3_lecture_2019/data/Pics/"
outfnm = outdir+"color_control.png"
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch

# Defalut: facecolor='w', edgecolor='w', transparent=False
sys.exit()


### Color Map Reference
## https://matplotlib.org/examples/color/colormaps_reference.html

### Color Map Guide
## https://matplotlib.org/users/colormaps.html#choosing-colormaps
