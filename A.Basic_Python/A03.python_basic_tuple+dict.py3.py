'''
Python Basic(3)
: Tuple and Dictionary

By Daeho Jin
'''

###--- Tuple
print("\n*** Tuple ***")
print("\n1. Define a tuple with ()")
print("a = (1,2,3)  # Define a tuple" )
a = (1,2,3)
print("a = {}:\ttype = {}".format(a,type(a)))

print("\n2. Tuple operation")
print("a+a = {}".format(a+a))
print("a*3 = {}".format(a*3))
input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n3. What makes tuple distinguished from list")
try:
    print("try a[0]=0  # Try to change value of tuple item")
    a[0]=0
except Exception as err:
    print("Error message\n:",err)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

###--- Dictionary
print("\n*** Dictionary ***")
print("\n1. Define a dictionry with {}")
print("ex) a_dict = {key:value}\n")
print('d = {"brand": "Ford", "model": "Mustang", "year": 2019 }')
d = {"brand": "Ford", "model": "Mustang", "year": 2019 }
print("d = {}:\ttype = {}\n".format(d,type(d)))
print('d["year"] = {}  # Access value by key'.format(d['year']))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n2. Add, change, and remove item")
print("e = {}  # Empty dictionry")
e = {}
print("e['brand']='kia'")
e['brand']='kia'
print("e['model']='optima'")
e['model']='optima'
print("e = {}\n".format(e))

print("e.pop('brand')")
e.pop('brand')
print("e = {}\n".format(e))

print("e['model']='Sonata'")
e['model']='Sonata'
print("e = {}\n".format(e))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n3. Define a dictionry with dict()")
print("f = dict(brand='Ford', model='Mustang', year=2019)")
f = dict(brand='Ford', model='Mustang', year=2019)
print("f = {}\n".format(f))

print("g = dict([('brand','Ford'), ('model','Mustang'), ('year',2019)])")
g = dict([('brand','Ford'), ('model','Mustang'), ('year',2019)])
print("g = {}".format(g))

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n4. Membership test")
print("'Mustang' in g ?")
print('Mustang' in g)
print("\n'model' in g ?")
print('model' in g)
print("\n'model' in g.keys() ?")
print('model' in g.keys())
print("\n'Mustang' in g.values() ?")
print('Mustang' in g.values())

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print("\n5. Visit all items")
print("\n5-1. Method1")
print('''for key in g:
    print("{}: {}".format(key, g[key]))
''')
for key in g: # or g.keys()
    print("{}: {}".format(key, g[key]))

print("\n5-2. Method2")
print('''for key, val in g.items():
    print("{}: {}".format(key, val))
''')
for key, val in g.items():
    print("{}: {}".format(key, val))

print("THE END: Python Basic(3) - Tuple and Dictionary\n")
