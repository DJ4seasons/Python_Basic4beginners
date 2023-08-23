"""
#
# Make new directory and save multiple text files
# using text template
#
# By Daeho Jin
#
"""

import sys
import os
from subprocess import run

outdir = './Text_Box/'  # Directory name to create
if os.path.isdir(outdir):  # Check if the directory already exists
    run("rm -r {}".format(outdir), shell=True)  # Execute shell command
    print("{} is removed.".format(outdir))

os.mkdir(outdir)  # Create a directory
### cf. os.makedirs(): Create directories of multiple levels at once
print("{} is created.".format(outdir))

text_template = '''
Hello, this is {name}.
I like Python.
This is easy to learn.
I started Python {days} days ago.'''

name_days = [('Bob',7),('Emily',5),('Kim',10)]
for name, days in name_days:
    text = text_template.format(name=name, days=days)
    out_file = outdir+'Statement_{}.txt'.format(name)  # File name to save text
    with open(out_file,'w') as fid:  # Open a file to write text
        print(text,file=fid)
        print("Written to {}".format(out_file))

    if not os.path.isfile(out_file):  # Check if a file exists
        sys.exit("Error: File is not created: "+out_file)
