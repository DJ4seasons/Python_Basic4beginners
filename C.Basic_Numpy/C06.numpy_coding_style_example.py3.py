"""
Numpy coding style examples

Below is a fortran program shown in 'B03.Script2run_fortran_code.py3'
Here two numpy functions to mimic blow program are given, and run times of them
are compared each other.

By Daeho Jin

---
program {prog_name}
  implicit none
  integer, parameter :: n_trial={n_trial}, dot_count={dot_count}
  real(8) :: q_pi, quarter_circle_ratio
  integer :: n,i

  do i=1,n_trial
    q_pi = quarter_circle_ratio(dot_count+i)
    print*,i,q_pi*4.
  enddo
end program {prog_name}

real(8) function quarter_circle_ratio(dot_count)
  implicit none
  integer :: dot_count, i,j
  integer(8) :: in_count
  real(8) :: dist, dt

  in_count=0
  dt = 1./dble(dot_count)
  do i = 1, dot_count
     do j = 0, dot_count-1
        dist = (i*dt)**2 + (j*dt)**2
        if (dist.le.1.) then
           in_count = in_count+1
        endif
     enddo
  enddo
  quarter_circle_ratio = in_count/dble(dot_count**2)
  return
end function quarter_circle_ratio
"""

import numpy as np
from time import time

def quarter_circle_ratio_elementwise(dot_count):
    """
    Produce a grid with resolution of 1/dot_cont
    and calculate distance from (0,0) to test if it is less than 1.

    Mimic fortran program, so element-wise calculation is performed.
    """
    in_count=0
    dt= 1/dot_count
    for j in range(0,dot_count,1):
        for i in range(1,dot_count+1,1):
            sqdist= (i*dt)**2 + (j*dt)**2
            if sqdist<=1:
                in_count+=1
    return in_count/(dot_count**2)

def quarter_circle_ratio_vectorized(dot_count):
    """
    Produce a grid with resolution of 1/dot_cont
    and calculate distance from (0,0) to test if it is less than 1.

    Mimic fortran program, but modifed to be vectorized.
    Apparently this requires more memory
    """

    ix= np.arange(1,dot_count+1,1)/dot_count
    iy= np.arange(dot_count)/dot_count
    ix,iy= np.meshgrid(ix,iy)
    in_count= (ix**2+iy**2<=1).sum()
    return in_count/(dot_count**2)

#---
n_trial, dot_count= 3, 3000

# Style 1
print("Start element-wise style")
time0= time()
for i in range(n_trial):
    q_pi= quarter_circle_ratio_elementwise(dot_count+i)
    print("Trial#{} dot_count={} pi={}".format(i+1, dot_count+i, q_pi*4.))
time1= time()-time0
print("Run time of element-wise style= {:.3f}".format(time1))

# Style 2
print("\nStart vectorized style")
time2= time()
for i in range(n_trial):
    q_pi= quarter_circle_ratio_vectorized(dot_count+i)
    print("Trial#{} dot_count={} pi={}".format(i+1, dot_count+i, q_pi*4.))
time3= time()-time2
print("Run time of element-wise style= {:.3f}".format(time3))
