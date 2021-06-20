'''
Python Basic Part4
: IF, FOR, and WHILE

By Daeho Jin
'''


### IF
print("\n*** IF ***")
print("\n1. IF basic form")
print("""
if condition:
    statement1  # Keep 'consistent' spacing
elif condition: # Optional
    statement2  # Keep 'consistent' spacing
else:           # Optional
    statement3  # Keep 'consistent' spacing
""")

print('''Example:
if True:
   print("Print this because condition is True")
elif False:
   print("Not printing this")
else:
   print("Not printing this")
''')
print("Result:")
if True:
   print("Print this because condition is True")
elif False:
   print("Not printing this")
else:
   print("Not printing this")

print("\nPress Enter to continue... (1)\n")
input("----------------------------------------\n")

print("\n2. IF one-line")
print("\nif condition: statement \n")

print("a = 3")
a = 3
print("TEST1: if a>0: print('this')")
if a>0: print('this')
print("TEST2: if a>0: print('this'); print('that')")
if a>0: print('this'); print('that')
print("TEST3: if a<0: print('this'); print('that')")
if a<0: print('this'); print('that')
print("\n---> Multi-statements are possible!")

print("\nPress Enter to continue... (2)\n")
input("----------------------------------------\n")

print("\n3. IF ELSE one-line")
print("\nstatement1 if condition else statement2 \n")

print("a = {}".format(a))
print("TEST1: b = 1 if a>0 else -1")
b = 1 if a>0 else -1
print("b = {} \n".format(b))
print("TEST2: c = 1 if b<0 else -1")
c = 1 if b<0 else -1
print("c = {} \n".format(c))

print("---> It only works for one variable!")
print("---> It doesn't work: c = 1 if b<0 else d = 1")

print("\nPress Enter to continue... (3)\n")
input("----------------------------------------\n")

### FOR
print("\n*** FOR Loop ***")
print("\n1. FOR basic form")
print("""
for x in iterable:
    statement(s)  # Keep 'consistent spacing'
""")

print("""Example:
list1, list2 = [], []
for i in range(10):  # range(10) = range(0,10) = range(0,10,1)
    if i%2==0:
        list1.append(i)
    else:
        list2.append(i)
""")
print("Result:")
list1, list2 = [], []
for i in range(10):  # range(10) = range(0,10) = range(0,10,1)
    if i%2==0:
        list1.append(i)
    else:
        list2.append(i)
print("list1 = {}".format(list1))
print("list2 = {}".format(list2))

print("\nPress Enter to continue... (1)\n")
input("----------------------------------------\n")

print("\n2. FOR one-line")
print("* Useful when building a list!")
print("Example1: a = [ x*x for x in range(5)]")
a = [ x*x for x in range(5)]
print("a = {}\n".format(a))

print("* It is also possible to combine FOR and IF")
print("Example2: b = [ x*x for x in range(5) if x%2==0]")
b = [ x*x for x in range(5) if x%2==0]
print("b = {}\n".format(b))

print("* An example combining FOR and IF Else; Caution for order of FOR and IF")
print("Example3: c = [ x*x if x%2==0 else -x for x in range(5)]")
c = [ x*x if x%2==0 else -x for x in range(5)]
print("c = {}\n".format(c))

print("\nPress Enter to continue... (2)\n")
input("----------------------------------------\n")

### For + zip, enumerate
print("\n3. FOR + enumerate, zip")
print("""Example of enumerate:
for i,val in enumerate(c):
    print("{}: x={}".format(i,val))
""")
print("Result:")
for i,val in enumerate(c):
    print("{}: x = {:3d}".format(i,val))

print("""\nExample of zip:
list3=[]
for x,y in zip(list1,list2):
   list3.append(",".join([str(x),str(y)]))  # join: built-in function of string
""")
print("Result:")
list3=[]
for x,y in zip(list1,list2):
   list3.append(",".join([str(x),str(y)]))
print("list3 = {}".format(list3))

print("\n* FYI: ','.join(map(str,list1)) ---> {}".format(','.join(map(str,list1))))

input("\nPress Enter to continue... (3-1)\n")

print("""
Example of zip+enumerate:
for i,(val1,val2) in enumerate(zip(list1,list2)):
   print('{}: {},{}'.format(i,val1,val2))
""")
print("Result:")
for i,(val1,val2) in enumerate(zip(list1,list2)):
   print('{}: {},{}'.format(i,val1,val2))

print("\nPress Enter to continue... (3-2)\n")
input("----------------------------------------\n")


### While
print("\n*** WHILE Loop ***")
print("\n1. WHILE basic form")
print("while condition:")
print("    statement(s)  # Keep 'consistent spacing'\n")
print("""\nExample of WHILE:
i=0
while i<3:
    print(i)
    i+=1  # Same as i=i+1
""")
print("Result:")
i=0
while i<3:
    print(i)
    i+=1

print("\nPress Enter to continue... (1)\n")
input("----------------------------------------\n")

print("\n2. Pass, Continue, and Break test in while loop")
print("""\nExample code:
i=0
while True:
    i+=1
    print(i)
    if i==1:
        print("continue"); continue
    elif i==2:
        print("pass"); pass
    elif i==3:
        print("break"); break
    print("End of while block")
print("Out of while block")
""")
print("Result:")
i=0
while True:
    i+=1
    print(i)
    if i==1:
        print("continue"); continue
    elif i==2:
        print("pass"); pass
    elif i==3:
        print("break"); break
    print("End of while block")
print("Out of while block \n")

print("---> 'continue': Go to next round of loop")
print("---> 'pass': Keep going (No effect on loop)")

print("\nPress Enter to continue... (2)\n")
input("----------------------------------------\n")

print("\n3. Break out of multiple loops")
print("""\nExample code of break:
for i in range(3):
    j=0
    while j<3:
        print(i,j)
        if i==1:
            print('break'); break
        j+=1
""")
print("Result:")
for i in range(3):
    j=0
    while j<3:
        print(i,j)
        if i==1:
            print('break'); break
        j+=1

input("\nPress Enter to continue... (3-1)\n")

print("""\nExample code of StopIteration:
try:
    for i in range(3):
        j=0
        while j<3:
            print(i,j)
            if i==1:
                print('StopIteration'); raise StopIteration
            j+=1
except StopIteration:
    print("It's working")  # Or simply 'pass' for doing nothing.
print("Out of loops")
""")
print("Result:")
try:
    for i in range(3):
        j=0
        while j<3:
            print(i,j)
            if i==1:
                print('StopIteration'); raise StopIteration
            j+=1
except StopIteration:
    print("It's working")
print("Out of loops")

print("\nPress Enter to continue... (3-2)\n")
input("----------------------------------------\n")

print("THE END: Python Basic Part4 - IF, FOR, and WHILE\n")
