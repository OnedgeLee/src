#%%
from sympy import *
import numpy as np
from math import pi

P1 = -16000
P2 = 0
P3 = 0

l0 = 171.5
# PI()*((19.25+6.75)/2)^2/1000000
A_avg = 0.00054558

cp2 = 0.0168/3
cp1 = 0.7759/3

cn2 = 0.0046/3
cn1 = 0.6986/3

l1 = symbols('l1')
l2 = symbols('l2')
l3 = symbols('l3')

F1 = P1 * A_avg
F2 = P2 * A_avg
F3 = P3 * A_avg

print(F1)

if P1 > 0 :
    f1 = cp2*l1**2 + cp1*l1 - F1
else :
    f1 = cn2*l1**2 + cn1*l1 - F1

if P2 > 0 :
    f2 = cp2*l2**2 + cp1*l2 - F2
else :
    f2 = cn2*l2**2 + cn1*l2 - F2

if P3 > 0 :
    f3 = cp2*l3**2 + cp1*l3 - F3
else :
    f3 = cn2*l3**2 + cn1*l3 - F3

f1_d = f1.diff(l1)
f2_d = f2.diff(l2)
f3_d = f3.diff(l3)

l1n = 30
l2n = 30
l3n = 30

for i in range(20):
    l1n = l1n - np.float(f1.evalf(subs= {l1:l1n})) / np.float(f1_d.evalf(subs= {l1:l1n}))
    print(f'The {i+1} iteration ln is {l1n:.4} and f(xln) is {np.float(f1.evalf(subs= {l1:l1n})):.3}')

l_1 = l1n + l0
print(l_1)

"""
for i in range(10):
    x2n = x2n - np.float(f2.evalf(subs= {x2:x2n})) / np.float(f2_d.evalf(subs= {x2:x2n}))
    print(f'The {i+1} iteration xn is {x2n:.4} and f(xn) is {np.float(f2.evalf(subs= {x2:x2n})):.3}')

for i in range(10):
    x3n = x3n - np.float(f3.evalf(subs= {x3:x3n})) / np.float(f3_d.evalf(subs= {x3:x3n}))
    print(f'The {i+1} iteration xn is {x3n:.4} and f(xn) is {np.float(f3.evalf(subs= {x3:x3n})):.3}')
"""