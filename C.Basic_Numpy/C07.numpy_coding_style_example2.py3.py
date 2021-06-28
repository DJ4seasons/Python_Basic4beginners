"""
Numpy coding style example (2)

Let's assume that we need to solve a linear equation, y= Ax.
Then,
x= A^-1 * y

Below, time consumtion of two methods are compared:
1. Step-by-step: making inverse of A, then multiply with y
2. Use dedicated function: np.linalg.solve()

By Daeho Jin
"""

import numpy as np
from time import time

def build_array(arr_size):
    rg= np.random.default_rng()
    A= np.eye(arr_size) + rg.random((arr_size,arr_size))
    x= rg.random(arr_size)*2-1
    y= np.dot(A,x)
    return A, x, y

def solving_lin_eq_manual(A,y):
    return np.dot(np.linalg.inv(A),y)

def check_time_lin_eq(func, A,y,x, n_trial=1):
    time0= time()
    for i in range(n_trial):
        x_calc= func(A,y)
    time1= time()

    equal_test= np.array_equal(x,x_calc)
    print("Trial#{} x == x_calc ? {}".format(i+1, equal_test))
    if not equal_test:
        print("Trial#{} x ~= x_calc ? {}".format(i+1, np.allclose(x,x_calc)))
        # np.allclose(): Element-wise comparison with tolerance
        print("Max. Diff = {}".format(np.absolute(x-x_calc).max()))

    return time1-time0

def main():
    n_trial= 3
    arr_size= 2500

    A,x,y= build_array(arr_size)

    # Style 1
    print("Style1: Step-by-step")
    time_consumed= check_time_lin_eq(solving_lin_eq_manual,A,y,x,n_trial)
    print("Run time of Style1 = {:.3f}".format(time_consumed))

    # Style 2
    print("\nStyle2: Use dedicated function")
    time_consumed= check_time_lin_eq(np.linalg.solve,A,y,x,n_trial)
    print("Run time of Style2 = {:.3f} \n".format(time_consumed))

    return

if __name__ == "__main__":
    main()
