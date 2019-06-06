import glob
from subprocess import call

indir='./data/'
fnames=glob.glob(indir+'*.*')

for fn in fnames:
    if ":" in fn:
        print(fn)
        fn2=fn.replace(":","-")
            
        print("Changed: "+fn2)
        call(["mv",fn,fn2])
