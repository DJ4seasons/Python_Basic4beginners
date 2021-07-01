'''
Matplotlib Basic_Lv2: 8. Normalizing for colormap
: Various normalizing method to match between data and colormap

by Daeho Jin

---
Reference:
### Color Map Normalization
https://matplotlib.org/stable/tutorials/colors/colormapnorms.html

### Color Map Guide
https://matplotlib.org/users/colormaps.html#choosing-colormaps

### Caution:
"CenteredNorm" is a new feature on matplotlib version 3.4
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cls
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, ScalarFormatter

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
x = np.linspace(-3,4,141)
y = np.linspace(-2,3,101)
X,Y = np.meshgrid(x,y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - 0.4*Z2)
print(Z.min(), Z.max())

###--- Plotting Start ---###
##-- Page Setup --##
fig = plt.figure()            # Define "figure" instance
fig.set_size_inches(8.5,6)    # Physical page size in inches, (lx,ly)
suptit="Color Map Example"
fig.suptitle(suptit,fontsize=15,y=0.98,va='bottom')  # Title for the page
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.93,wspace=0.2,hspace=0.25)

abc='abcdefghijklmn'
##---
panel_names= ['Default','Normalize', 'LogNorm', 'BoundaryNorm',
            'CenteredNorm', 'TwoSlopeNorm']

props_base= dict(extent=[-3,4,-2,3],origin='lower',interpolation='bilinear')

props0= dict(cmap='plasma',**props_base)  # The addition of vmin and vmax is same to "Normalize()"
props1= dict(norm=cls.Normalize(vmin=-0.3,vmax=0.9),cmap='plasma',**props_base)
props2= dict(norm=cls.LogNorm(vmin=0.01,vmax=1),cmap='plasma',**props_base)

bounds= np.arange(-0.2,0.81,0.2)
props3= dict(norm=cls.BoundaryNorm(boundaries=bounds,ncolors=256,extend='both'),cmap='RdYlBu_r',**props_base)
#<--- Colormaps are composed of total 256 colors usually; contourf() is based on BoundaryNorm 
props4= dict(norm=cls.CenteredNorm(vcenter=0),cmap='RdYlBu_r',**props_base)
props5= dict(norm=cls.TwoSlopeNorm(vmin=-0.3,vcenter=0,vmax=0.9),cmap='RdYlBu_r',**props_base)

nrow, ncol= 2,3
for i,(tit,props) in enumerate(zip(panel_names,[eval('props'+str(num)) for num in range(6)])):
    ax1 = fig.add_subplot(nrow,ncol,i+1)   # subplot(# of rows, # of columns, indicater)
    pic1= ax1.imshow(Z,**props)
    subtit='({}) {}'.format(abc[i],panel_names[i])
    ax1.set_title(subtit,fontsize=12)
    ax1.tick_params(axis='both',which='major',labelsize=10)

    cb= draw_colorbar(ax1,pic1,type='horizontal',size='panel',extend='both',gap=0.07)
    if 'Log' in tit:
        cb.ax.xaxis.set_major_formatter(ScalarFormatter())
    elif 'Default' in tit or 'Normalize' in tit:
        cb.ax.xaxis.set_major_locator(MultipleLocator(0.3))
        cb.ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    elif 'Center' in tit:
        tlabs= cb.ax.get_xticklabels()
        cb.ax.set_xticklabels(tlabs,ha='right',rotation=35)

#- If want to save to file
outdir = "../Pics/"
outfnm = outdir+"N08_Colormap_Normalization.png"
print(outfnm)
#fig.savefig(outfnm,dpi=100)   # dpi: pixels per inch
fig.savefig(outfnm,dpi=100,bbox_inches='tight')   # dpi: pixels per inch
# Defalut: facecolor='w', edgecolor='w', transparent=False

##-- Seeing or Saving Pic --##
plt.show()
