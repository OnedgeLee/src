#%%
from sympy import *
import numpy as np

POS = False
if POS :
    c64 = 2.8151
    c63 = -20.106
    c62 = 32.553
    c61 = 2.1583
    c60 = 0
    shift_6 = 3.4  # shift 3.4 V
    c24 = 1.7366
    c23 = -12.352
    c22 = 23.031
    c21 = 1.973
    c20 = 0
    shift_2 = 3.2  # start 3.2 V
    c104 = -4.1484
    c103 = 7.0742
    c102 = 2.8924
    c101 = 6.9909
    shift_10 = 3.3  # start at 3.3 V
    c100 = 0
else :
    c64 = -383.24
    c63 = 398.52
    c62 = -146.72
    c61 = 64.452
    c60 = -22.5
    shift_6 = 3.2 # shift 3.35 V
    c24 = 77.486
    c23 = -291.77
    c22 = 205.23
    c21 = 9.3263
    c20 = -26.5
    shift_2 = 3.2 # start 3.2 V end 3.8
    c104 = 179.89
    c103 = -310.34
    c102 = 168.42
    c101 = 5.0462
    shift_10 = 3.25 # start at 3.25 (0)
    c100 = -23

# pressure range - 20 ~ + 20
p = 0 # kPa

x1 = symbols('x1')
x2 = symbols('x2')
x3 = symbols('x3')

f1 = c64*x1**4 + c63*x1**3 + c62*x1**2 + c61*x1 + c60 - p
f2 = c24*x2**4 + c23*x2**3 + c22*x2**2 + c21*x2 + c20 - p
f3 = c104*x3**4 + c103*x3**3 + c102*x3**2 + c101*x3 + c100 - p

# f_d = f.diff(x)
f1_d = f1.diff(x1)
# f2_d = f2.diff(x2)
f3_d = f3.diff(x3)

x1n = 0.25
# x2n = 0.2
# x3n = 0.2
for i in range(20):
    x1n = x1n - np.float(f1.evalf(subs= {x1:x1n})) / np.float(f1_d.evalf(subs= {x1:x1n}))
    print(f'The {i+1} iteration xn is {x1n:.4} and f(xn) is {np.float(f1.evalf(subs= {x1:x1n})):.3}')

"""
for i in range(10):
    x2n = x2n - np.float(f2.evalf(subs= {x2:x2n})) / np.float(f2_d.evalf(subs= {x2:x2n}))
    print(f'The {i+1} iteration xn is {x2n:.4} and f(xn) is {np.float(f2.evalf(subs= {x2:x2n})):.3}')

for i in range(10):
    x3n = x3n - np.float(f3.evalf(subs= {x3:x3n})) / np.float(f3_d.evalf(subs= {x3:x3n}))
    print(f'The {i+1} iteration xn is {x3n:.4} and f(xn) is {np.float(f3.evalf(subs= {x3:x3n})):.3}')
"""
sol1 = x1n + shift_6
print(sol1)
# sol2 = x2n + shift_2
# sol3 = x3n + shift_10
# print(sol1, sol2, sol3)