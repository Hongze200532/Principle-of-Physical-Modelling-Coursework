'''
In this initial_model file, we assume there is no friction in the system
'''
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import sympy as sp

# Symbol Definition
t = sp.Symbol('t', real=True)
theta = sp.Function('theta')(t)
# Data Setting
mA = 0.0287
mB = 0.058
mD = 0.1288
rA = 0.12
rB = -0.08
rD = 0.04
G = 9.81

I = mA*rA**2 + mB*rB**2 + mD*rD**2 # Inertia

# ODE Equation Expression
alpha = sp.diff(theta, t, 2) # 2nd derivative of theta about time t
eq = sp.Eq(I*alpha + G*(-mA*rA*sp.sin(theta) + mB*rB*sp.sin(theta) - mD*rD*sp.sin(theta)), 0)

# Numerical Part:
k_expr = (G*(mA*rA - mB*rB + mD*rD))/I
k_val = float(k_expr)
print(f"\ Numerical_Cons:  k = {k_val:.6f} s^-2")

# Define 1st ODE system
def rhs(t, y):
    theta, omega = y
    return [omega, k_val * np.sin(theta)]

# Initial Condition
y0 = [0.1, 0.0]   # 初始角度 0.1 rad, 初始角速度 0
t_span = (0, 5.0)
t_eval = np.linspace(t_span[0], t_span[1], 1000)

# Numerical Solution
sol = solve_ivp(rhs, t_span, y0, t_eval=t_eval, rtol=1e-9, atol=1e-12)

# Visualisation
plt.figure(figsize=(7,4))
plt.plot(sol.t, sol.y[0], label='θ(t)')
plt.plot(sol.t, sol.y[1], label='θ\'(t)', linestyle='--')
plt.xlabel('Time t (s)')
plt.ylabel('Angle θ (rad)')
plt.title('ODE Numerical Solution: θ(t) & θ\'(t)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
