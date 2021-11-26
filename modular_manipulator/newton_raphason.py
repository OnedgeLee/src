#%%
from sympy import *
import numpy as np

v_shift = 3.333 # in Volt

p = 50 # kPa
P = 50/1000

a4 = 0.0423
a3 = -0.1335
a2 = 0.0951
a1 = 0.0548
a0 = 0

x = symbols('x')
f = a4*x**4 + a3*x**3 + a2*x**2 + a1*x + a0-P

f_d = f.diff(x)

xn = 1
for i in range(10):
    xn = xn - np.float(f.evalf(subs= {x:xn})) / np.float(f_d.evalf(subs= {x:xn}))
    print(f'The {i+1} iteration xn is {xn:.4} and f(xn) is {np.float(f.evalf(subs= {x:xn})):.3}')

sol = xn + v_shift
print(sol)