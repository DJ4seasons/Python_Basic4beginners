'''
Matplotlib Basic_Lv2(5)
:

by Daeho Jin

---
Reference:
### Color Map Reference
https://matplotlib.org/stable/gallery/color/colormap_reference.html

### Color Map Guide
https://matplotlib.org/stable/tutorials/colors/colormaps.html

### Other references
Stauffer, R., G. J. Mayr, M. Dabernig, and A. Zeileis, 2015: Somewhere Over the Rainbow: How to Make Effective Use of Colors in Meteorological Visualizations. Bull. Amer. Meteor. Soc., 96, 203–216, https://doi.org/10.1175/BAMS-D-13-00155.1.
Tips for designing scientific figures for color blind readers[https://www.somersault1824.com/tips-for-designing-scientific-figures-for-color-blind-readers/]
http://hclwizard.org/hclwizard/


default,  norm, lognorm, boundary, centered, twoslope

'''

import numpy as np
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
x = y = np.linspace(-0.1,1.1,13)  # For 12x12 array
X,Y = np.meshgrid(x,y)
Z = np.cos(np.pi/2*X)-np.sin(np.pi/2*Y)
print(Z.min(), Z.max())

###--- Plotting Start ---###
##-- Page Setup --##
fig = plt.figure()            # Define "figure" instance
fig.set_size_inches(8.5,6)    # Physical page size in inches, (lx,ly)
suptit="Color Map Example"
fig.suptitle(suptit,fontsize=15,y=0.97,va='bottom')   # Title for the page
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.92,wspace=0.15,hspace=0.3)

abc='abcdefghijklmn'
##---
panel_names= ['cmap="magma"','set_under/over', 'cmap_r', 'Cut a cmap',
            'Combine two cmaps', 'Add white at the end']

cmap1= plt.cm.get_cmap('magma')
cmap2= plt.cm.get_cmap('magma')
cmap2.set_under='0.3'; cmap2.set_over='0.7'

cmap3= plt.cm.get_cmap('magma_r')
cmap4= plt.cm.get_cmap('RdYlBu_r')
cmap4= cmap4(np.arange(30)); print(type(cmap4),cmap4.shape)  # Converted to ndarray
cmap4= cls.LinearSegmentedColormap.from_list("newCM",cmap4[10:,:])

cmap5a= plt.cm.get_cmap('plasma')(np.arange(100))  # Converted to ndarray
cmap5b= plt.cm.get_cmap('viridis_r')(np.arange(100))  # Convert to ndarray
cmap5= np.concatenate((cmap5a,cmap5b),axis=0)
cmap5= cls.LinearSegmentedColormap.from_list("newCM",cmap5)

cmap6= plt.cm.get_cmap('magma_r')(np.arange(50))   # Converted to ndarray
cmap6= np.concatenate((np.array([1,1,1,1]).reshape([1,-1]),cmap6[:-1,:]))
cmap6= cls.LinearSegmentedColormap.from_list("newCMR",cmap6)

##---
nrow, ncol= 2,3
for i,(tit,cm) in enumerate(zip(panel_names,[eval('cmap'+str(num+1)) for num in range(6)])):
    ax1 = fig.add_subplot(nrow,ncol,i+1)   # subplot(# of rows, # of columns, indicater)

    props= dict(cmap=cm,vmin=-1,vmax=1,extent=[-0.1,1.1,-0.1,1.1],
                origin='lower',interpolation='bilinear')
    pic1= ax1.imshow(Z,**props)

    subtit='({}) {}'.format(abc[i],panel_names[i])
    ax1.set_title(subtit,fontsize=12)

    #            cb=draw_colorbar(ax,pic1,type='horizontal',size='page')
    #    cb= draw_colorbar(ax,pic1,type='vertical',size='panel',extend='both',gap=0.02)
    #    cb_yt= np.arange(0.1,1.,0.2)
    #    cb_ytl=["a{:.1f}".format(x) for x in cb_yt]
    #    cb.set_ticks(cb_yt)
    #    cb.ax.set_yticklabels(cb_ytl,size=12,color='b',stretch='semi-condensed')

    #ax.set_xticks(np.linspace(0,len(xlin)-1,4))
    #ax.set_xticklabels([-2,0,2,4])
    #ax.set_yticks(np.linspace(0,len(ylin)-1,5))
    #ax.set_yticklabels([-3,-1,1,3,5])
    #ax.tick_params(axis='both',which='major',labelsize=10)


#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N07_colormap+colorbar.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

##-- Seeing or Saving Pic --##
plt.show()
