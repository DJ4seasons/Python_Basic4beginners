"""
#
# Write a fortran code, compile it, and run in python code
#
# By Daeho Jin
#
"""

import sys
import os
from subprocess import run, CalledProcessError

fn0 = "estimate_pi"
fn_x = "{}.x".format(fn0)
fn_f90 = "./{}.f90".format(fn0)

f_program = """
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

keywords = dict(prog_name=fn0, n_trial=3, dot_count=1000)
print(keywords)

if os.path.isfile(fn_f90):
    os.remove(fn_f90)

print(f_program.format(**keywords),file=open(fn_f90,'w'))
try:
    run("gfortran -o {} {}".format(fn_x,fn_f90), shell=True, check=True)
    run("./{}".format(fn_x), shell=True, check=True)
except CalledProcessError:  # If problem(s) occur
    sys.exit()  # End this python program

run("rm {}*".format(fn0), shell=True)  # Be cautious not to delete other files
