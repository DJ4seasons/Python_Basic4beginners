"""
#
# Search multiple files using glob
# and change file name
#
# By Daeho Jin
#
"""

import glob
from subprocess import run

indir='./Text_Box/'
fnames=glob.glob(indir+'Statement*.txt')  # Get file names using star mark.
### Be cautious that result of glob is basically not sorted but random order.

for fn in fnames:
    print(fn)
    words = fn.strip().split('/')  # Seperate directory name and file name
    fn0 = words[-1]  # File name is the last one

    if "_" in fn0:  # Check if the fine name contains "_"
        fn0 = fn0.replace("_","+")  # Replace "_" with "+" in the file name
        words[-1] = fn0  # Replace the file name with new one
        fn2 = '/'.join(words)  # Reconstruct a string containing directory name and file name
        print(fn+" ==> "+fn2)
        run("mv {} {}".format(fn,fn2), shell=True)  # Execute shell command 'mv'
