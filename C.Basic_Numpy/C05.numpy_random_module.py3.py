"""
Random sampling
(Numpy.random module)
https://numpy.org/doc/stable/reference/random/index.html
https://numpy.org/doc/stable/reference/random/generator.html

Below is based on the version of Numpy, 1.17 or later.

By Daeho Jin
"""

import numpy as np
import sys

###--- Start
print('\nBefore start, check the version of numpy')
print('ver= np.__version__  # Check if Numpy version is 1.17 or later')
# Check if Numpy version is 1.17 or later
ver= np.__version__
print('version= ',ver)
if int(ver.split('.')[1])<17:

    sys.exit('Numpy version should be 1.17 or later')

print('\n* Start by initializing')
print('rg = np.random.default_rng()  # Initialize "Random Generator" object')
rg = np.random.default_rng()  # Initialize "Random Generator" object

print('\n* Get integer random numbers in [0,100]')
print('print(rg.integers(0, 100, size=5, endpoint=True))  # endpoint=True so include 100')
print(rg.integers(0, 100, size=5, endpoint=True))  # endpoint=True so include 100
print('* One more time')
print('print(rg.integers(0, 100, size=5, endpoint=True))')
print(rg.integers(0, 100, size=5, endpoint=True))

print('\n* Get float random numbers in [0.,1.)')
print('print(rg.random(size=5))  # between [0.0, 1.0)')
print(rg.random(size=5))  # between [0.0, 1.0)
print('* One more time with specific dtype')
print('print(rg.random(size=5, dtype=np.float32))')
print(rg.random(size=5, dtype=np.float32))  # between [0.0, 1.0)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print('* Sub-sampling and shuffle from given array')
print('arr1d= np.arange(100)  # Define sample array')
arr1d= np.arange(100)

print('\n* Randomly select 10 samples from arr1d')
print('''chosen= rg.choice(arr1d, size=10)  # "shuffle=False" can speed up for large size
print(chosen)''')
chosen= rg.choice(arr1d, size=10)  # "shuffle=False" can speed up for large size
print(chosen)

print('\n* Shuffle in-place (while "permutation" returns copy)')
print('''rg.shuffle(chosen)
print(chosen)''')
rg.shuffle(chosen)
print(chosen)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print('* Set seed in order to repeat results')
print('''rg2 = np.random.default_rng(123)  # Initialize with seed
print(rg2.random(size=5))  # between [0.0, 1.0)''')
rg2 = np.random.default_rng(123)  # Initialize with seed
print(rg2.random(size=5))  # between [0.0, 1.0)

print('''
rg3 = np.random.default_rng(123)  # Anothoer initialization with the same seed
print(rg3.random(size=5))  # between [0.0, 1.0)''')
rg3 = np.random.default_rng(123)  # Anothoer initialization with same seed
print(rg3.random(size=5))  # between [0.0, 1.0)

input("\nPress Enter to continue...\n")
print("----------------------------------------\n")

print('* Get random numbers under specific distribution')
print('''import matplotlib.pyplot as plt
xx= rg.standard_normal(size=1000)  # normal distribution with mean=0, std=1
yy= rg.uniform(size=1000)  # uniform distribution
plt.scatter(xx,yy)  # draw sactter plot with xx and yy
plt.show()
''')
import matplotlib.pyplot as plt
xx= rg.standard_normal(size=500)
yy= rg.uniform(size=500)
plt.scatter(xx,yy)
plt.show()

print('''\n# Various distributions are available at
https://numpy.org/doc/stable/reference/random/generator.html''')

print("\nTHE END: Random numbers in Numpy\n")
