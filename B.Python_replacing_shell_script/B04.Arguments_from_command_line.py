"""
#
# 1. Arguments when executing program (e.g., >>python3 program.py some srguments)
# 2. Input in the mid of program
#
# By Daeho Jin
#
"""

import sys

### 1. Getting arguments from program execution line
argv= sys.argv
print("Info of argv: ",type(argv), argv)

if len(argv)>1:
    num = int(sys.argv[1])
    print(list(range(num)))
else:
    ###2. Getting arguments using input() function
    input1= input("Type a number: ")
    print("Info of input1: ",type(input1),input1)
    num= int(input1)
    print(list(range(num)))
