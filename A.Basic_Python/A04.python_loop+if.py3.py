'''
Python Basic(4)
: IF, FOR, and WHILE

By Daeho Jin
'''


### IF
print("\n*** IF ***")
print("\n1. IF basic")
print("if condition:")
print("    statement1  # Keep 'consistent' spacing")
print("elif condition: #optional")
print("    statement2  # Keep 'consistent' spacing")
print("else:           #optional")
print("    statement3  # Keep 'consistent' spacing\n")

print('''Example:
if True:
   print("Print this because condition is True")
elif False:
   print("Not printing this")
else:
   print("Not printing this")\n''')
if True:
   print("Print this because condition is True")
elif False:
   print("Not printing this")
else:
   print("Not printing this")

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2. IF one-line")
print("if condition: statement")
print("a = 3")
a = 3
print("TEST1: if a>0: print('this')")
if a>0: print('this')
print("TEST2: if a>0: print('this'); print('that')")
if a>0: print('this'); print('that')
print("TEST3: if a<0: print('this'); print('that')")
if a<0: print('this'); print('that')
print("\n---> Multi-statements are possible!")
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n3. IF ELSE one-line")
print("statement1 if condition else statement2")
print("a = 3")
a = 3
print("b = 1 if a>0 else -1")
b = 1 if a>0 else -1
print("b = {}".format(b))
print("\nc = 1 if b<0 else -1")
c = 1 if b<0 else -1
print("c = {}".format(c))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

### FOR
print("\n*** FOR Loop ***")
print("\n1. FOR basic")
print("for x in iterable:")
print("    statement(s)  # Keep 'consistent spacing'\n")

print("""Example:
list1, list2 = [], []
for i in range(10):  # range(10) = range(0,10) = range(0,10,1)
    if i%2==0:
        list1.append(i)
    else:
        list2.append(i)\n""")
list1, list2 = [], []
for i in range(10):  # range(10) = range(0,10) = range(0,10,1)
    if i%2==0:
        list1.append(i)
    else:
        list2.append(i)
print("list1 = {}".format(list1))
print("list2 = {}".format(list2))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2. FOR one-line")
print("* Useful when building a list!")
print("Example1: a = [ x*x for x in range(5)]")
a = [ x*x for x in range(5)]
print("a = {}\n".format(a))

print("* It is also possible to combine FOR and IF")
print("Example2: b = [ x*x for x in range(5) if x%2==0]")
b = [ x*x for x in range(5) if x%2==0]
print("b = {}\n".format(b))

print("Example3: c = [ x*x if x%2==0 else -x for x in range(5)]")
c = [ x*x if x%2==0 else -x for x in range(5)]
print("c = {}\n".format(c))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

### For + zip, enumerate
print("\n3. FOR + enumerate, zip")
print("""Example of enumerate:
for i,x in enumerate(c):
    print("{}: x={}".format(i,x))""")
for i,x in enumerate(c):
    print("{}: x={}".format(i,x))

print("""\nExample of zip:
list3=[]
for x,y in zip(list1,list2):
   list3.append(",".join([str(x),str(y)]))""")
list3=[]
for x,y in zip(list1,list2):
   list3.append(",".join([str(x),str(y)]))
print("list3 = {}".format(list3))

print("""\nExample of zip+enumerate:
for i,(x,y) in enumerate(zip(list1,list2)):
   print('{}: {},{}'.format(i,x,y))""")
for i,(x,y) in enumerate(zip(list1,list2)):
   print('{}: {},{}'.format(i,x,y))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")


### While
print("\n*** WHILE Loop ***")
print("\n1. WHILE basic")
print("while condition:")
print("    statement(s)  # Keep 'consistent spacing'\n")
print("""\nExample of WHILE:
i=0
while i<3:
    print(i)
    i+=1""")
i=0
while i<3:
    print(i)
    i+=1

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

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
    print("Return")""")
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
    print("Return")
print("---> Note that 'continue' and 'pass' are different!")
input("\nPress Enter to continue...\n")
print("THE END: Python Basic(4) - IF, FOR, and WHILE\n")
