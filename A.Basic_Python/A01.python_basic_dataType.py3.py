'''
Python Basic Part1
: Data Types

By Daeho Jin
'''

### Part0: Assignment
print("\n*** Before Start ***\n")
print("Assignment: left = right")
print("It means value 'right' is assigned to variable 'left'")
print("\nFor example, ")
print("a = 1")
print("a, b, c = 1,2,3")
a,b,c= 1,2,3; print(a,b,c)
print("a = b = 1")
a=b=1; print(a,b)
input("\nPress Enter to continue... (0)\n")
print("----------------------------------------\n")

### Part1: Data Types
print("\n*** Data Types ***")
print("!!! Data Type is defined when a value is assigned !!!")
### Integer and float numbers
print("\n1. Integer and float numbers\n")
a=17
b=7
print("a = {}:\ttype = {}".format(a,type(a)))
print("b = {}:\ttype = {} \n".format(b,type(b)))
print("c = a+b")
c=a+b
print("c = {}:\ttype = {} \n".format(c,type(c)))
print("c = a/b")
c=a/b
print("c = {}:\ttype = {}".format(c,type(c)))
print("---> Division by integer results in float type\n")
print("d = a//b")
d=a//b
print("d = {}:\ttype = {}".format(d,type(d)))
input("\nPress Enter to continue... (1)\n")
print("----------------------------------------\n")

### Print format
print("\n2. Print format examples")
print("cf. https://pyformat.info/ \n")
format_test = '{},\t{:d},\t{:02d},\t{:03d},\t{:.2f},\t{:.3f}'
print(format_test)
print(format_test.format(a,a,a,a,a,c))

print("\nIn case of printing {}, {}, {}".format(a,b,c))
format_test2 = '{1:d},\t{2:.2f},\t{0:.1f}'
print('\n'+format_test2)
print(format_test2.format(a,b,c))
format_test3 = '{0:d},\t{1:.2f},\t{other:.1f}'
print('\n'+format_test3)
print(format_test3.format(a,b,other=c))
print("\nHow about multi-lines? Use tripple quote mark!")
multi_lines='''
Hello, my name is {name}.
I am {age:d} years old.
My favorite food is {food}
'''
keywords={"name":"Bob", "age":35, "food":"chococake"}  # This is dictionry!
print(multi_lines.format(**keywords))  # two stars: distribute items of "key:value"
input("\nPress Enter to continue... (2)\n")
print("----------------------------------------\n")

### String
print("\n3. String examples\n")
print("d = str(c) # Change type from float to string ")
d=str(c)
print("d = {}:\ttype = {}\n".format(d,type(d)))
print("len(d), d[0:4], d[-3:]")  # Python index starts at 0
print("{}, {}, {}\n".format(len(d),d[0:4],d[-3:]))
print("c+c vs. d+d[:5] vs. d*2")
print("{} vs. {} vs. {}\n".format(c+c,d+d[:5],d*2))
print("len(d*2)")
print(len(d*2))
input("\nPress Enter to continue... (3)\n")
print("----------------------------------------\n")

### Printing unicode
print("\n4. Unicode example\n")
print("El Ni\u00F1o and La Ni\u00F1a \n")
print("Delta: {}, epsilon: {}, degree: {} \n".format('\u0394','\u03B5','\u00B0'))
print("Subscript: x{}, x{}, x{} \n".format('\u2081','\u2082','\u2090'))
print("Superscript: x{}, x{}, x{} \n".format('\u2071','\u00B2','\u0363'))
input("\nPress Enter to continue... (4)\n")
print("----------------------------------------\n")

### Boolean
print("\n5. Boolean type\n")
print("boo1, boo2 = True, False")
boo1, boo2 = True, False
print("boo1 = {}:\ttype = {} \n".format(boo1,type(boo1)))
print("Value of {} and {}:".format(boo1,boo2))
print(int(boo1),int(boo2),'\n')
print("{}+{} = {}".format(boo1,boo2,boo1+boo2))
print("{}+{} = {}".format(boo1,boo1,boo1+boo1))
print("{}+{} = {} \n".format(boo2,boo2,boo2+boo2))
print("{} 'and' {} = {}".format(boo1,boo2,boo1 and boo2))
print("{} 'or' {} = {}".format(boo1,boo2,boo1 or boo2))
print("'not' {} = {} \n".format(boo1, not boo1))

print("bool(-1) = {}, bool(0) = {}, bool(1) = {}, bool(2) = {}".format(bool(-1),bool(0),bool(1),bool(2)))
print("bool(-0.1) = {}, bool(0.) = {}, bool(0.1) = {}".format(bool(-0.1),bool(0.),bool(0.1)))
print("---> Value zero(0) is False, and all others are True")
input("\nPress Enter to continue... (5)\n")

print("THE END: Python Basic Part1 - Data Types\n")
