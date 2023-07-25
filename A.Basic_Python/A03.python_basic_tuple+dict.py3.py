'''
Python Basic Part3
: Tuple and Dictionary

By Daeho Jin
'''

###--- Tuple
print("\n*** Tuple ***")
print("\n1. Define a tuple with ()")
print(">> a = (1,2,3)  # Define a tuple" )
a = (1,2,3)
print("a = {};\ttype = {}".format(a,type(a)))

print("\n2. Tuple operation")
print("a+a = {}".format(a+a))
print("a*3 = {}".format(a*3))
print("\nPress Enter to continue... (1,2)\n")
input("----------------------------------------\n")

print("\n3. What makes tuple distinguished from list")
try:
    print("try a[0]=0  # Try to change value of tuple item")
    a[0]=0
except Exception as err:
    print("Error message\n:",err)

print("\nHence, tuple is usually used for parameters.")
print("\nPress Enter to continue... (3)\n")
input("----------------------------------------\n")

###--- Dictionary
print("\n*** Dictionary ***")
print("\n1. Define a dictionry with {}")
print("ex) a_dict = {key:value}\n")
print('>> d = {"brand": "Ford", "model": "Mustang", "year": [2015, 2019] }')
d = {"brand": "Ford", "model": "Mustang", "year": [2015, 2019] }
print("d = {}; type = {}\n".format(d,type(d)))
print(">> print(d['model']) # Access value by key")
print(d['model'])

print("\n2. Define a dictionry with dict()")
print(">> e = dict(brand='Ford', model='Mustang', year=[2015, 2019])")
print(">> print(e)")
e = dict(brand='Ford', model='Mustang', year=[2015, 2019])
print(e)

print("\n>> f = dict([('brand','Ford'), ('model','Mustang'), ('year',[2015, 2019])])")
print(">> print(f)")
f = dict([('brand','Ford'), ('model','Mustang'), ('year',[2015, 2019])])
print(f)

print("\nPress Enter to continue... (1,2)\n")
input("----------------------------------------\n")

print("\n3. Add, change, remove, and update item(s)")
print(">> g = {}  # Empty dictionry")
g = {}
print(">> g['brand']='Kia'")
g['brand']='kia'
print(">> g['model']='optima'")
g['model']='optima'
print(">> print(g)")
print(g)

print("\n>> g.pop('brand')  # dict.pop() is different from list.pop()")
g.pop('brand')
print(">> print(g)")
print(g)

print("\n>> h = g  # Copy or not copy?")
h = g
print(">> h['model']='Sonata' \n")
h['model']='Sonata'
print(">> print(g)")
print(g)
print("---> Use dict.copy()")

print("\n>> g.update(dict(brand='Hyundai'))  # Update g by merging new dictionry into g")
g.update(dict(brand='Hyundai'))
print(">> print(g)")
print(g)

print("\nPress Enter to continue... (3)\n")
input("----------------------------------------\n")


print("\n4. Membership test")
print("For a dictionry, g = {} \n".format(g))
print(">> 'Sonata' in g ?")
print('Sonata' in g)
print("\n>> 'model' in g ?")
print('model' in g)
print("\n>> 'model' in g.keys() ?")
print('model' in g.keys())
print("\n>> 'Sonata' in g.values() ?")
print('Sonata' in g.values())

print("\nPress Enter to continue... (4)\n")
input("----------------------------------------\n")

print("\n5. Visit all items")
print("For a dictionry, f = {}".format(f))
print("\n5-1. Method1")
print('''>> for key in f:  # or f.keys()
>>     print("{}: {}".format(key, f[key]))
''')
for key in f:
    print("{}: {}".format(key, f[key]))

print("\n5-2. Method2")
print('''>> for key, val in f.items():
>>     print("{}: {}".format(key, val))
''')
for key, val in f.items():
    print("{}: {}".format(key, val))

print("\nPress Enter to continue... (5)\n")
input("----------------------------------------\n")

print("\n6. Miscellaneous")
print("Two stars(**) with Dictionary: An example from A01:")
multi_lines='''
Hello, I like to buy a {brand} {model}.
Do you have model year(s) {year}?
'''
print(">> print(multi_lines)")
print(multi_lines)
print(">> print(multi_lines).foramt(**f)")
print(multi_lines.format(**f))  # two stars: distribute items of "key:value"

print("\nPress Enter to continue... (6)\n")
input("----------------------------------------\n")

print("THE END: Python Basic Part3 - Tuple and Dictionary\n")
