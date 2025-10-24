import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fill the Blue Mass Point
df_coords = pd.read_csv("blue_ball_filled.csv")
df_theta = pd.read_csv("mass_point_theta.csv")

# Clean Data
df_coords = df_coords.dropna(subset=["Xb", "Yb"])
X = df_coords["Xb"].to_numpy()
Y = df_coords["Yb"].to_numpy()

# Polt the Circle (Left)
def fit_circle(x, y):
    A = np.c_[2*x, 2*y, np.ones(len(x))]
    b = x**2 + y**2
    sol, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    a, b, c = sol
    r = np.sqrt(c + a**2 + b**2)
    return a, b, r

a, b, r = fit_circle(X, Y)
print(f"Circle Center -({a:.2f}, {b:.2f}), 半径: {r:.2f}")

# Plotting the Curve + Circle
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# ========== Left Graph ==========
ax[0].plot(X, Y, 'b.', label="Blue Mass Point Curve")
ax[0].plot(a, b, 'ro', label="Center of the circle")

# Circle
theta = np.linspace(0, 2*np.pi, 200)
circle_x = a + r * np.cos(theta)
circle_y = b + r * np.sin(theta)
ax[0].plot(circle_x, circle_y, 'g--', label="Circle")

# Movement
ax[0].set_aspect('equal', adjustable='box')
ax[0].set_xlabel("X Pixel")
ax[0].set_ylabel("Y Pixel")
ax[0].invert_yaxis()
ax[0].set_title("Blue Mass Point Movement")
ax[0].legend()

# ========== Right Graph ==========
# Read Data from the clean data file
data = pd.read_csv('blue_ball_filled_clean.csv')
frame = data['Frame']
Xb = data['Xb']
Yb = data['Yb']

# Calculate the center of the circle
x_center = np.mean(Xb)
y_center = np.mean(Yb)

# Calculate θ(t)
theta = np.degrees(np.arctan2(-(Yb - y_center), Xb - x_center))

theta_unwrapped = np.unwrap(np.radians(theta))
theta_unwrapped = np.degrees(theta_unwrapped)

# Calculate time t
fps = 30
t = frame / fps
# Plotting the Function Curve
ax[1].plot(t, theta_unwrapped, color='magenta')
ax[1].set_xlabel("Time t (s)")
ax[1].set_ylabel("Angle θ (°)")
ax[1].set_title("Angle Change with Time θ(t)")
ax[1].grid(True)

# =============== Final Graph Plotting =================
plt.tight_layout()
plt.show()

