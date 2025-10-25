import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read CSV
df_coords = pd.read_csv("blue_ball_filled.csv")
df_theta = pd.read_csv("mass_point_theta.csv")

# Clean Data
df_coords = df_coords.dropna(subset=["Xb", "Yb"])
X_pixels = df_coords["Xb"].to_numpy()
Y_pixels = df_coords["Yb"].to_numpy()

# Blue Ball R = 0.5 cm
def fit_circle(x, y):
    A = np.c_[2*x, 2*y, np.ones(len(x))]
    b = x**2 + y**2
    sol, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    a, b, c = sol
    r = np.sqrt(c + a**2 + b**2)
    return a, b, r

a_px, b_px, r_px = fit_circle(X_pixels, Y_pixels)
print(f"Center of Circle (Pixel): ({a_px:.2f}, {b_px:.2f}), R: {r_px:.2f} px")

# Pixel -> cm
scale = r_px / 0.5
print(f"Pixel/cm Ratio: 1 cm = {scale:.2f} px")

X = X_pixels / scale
Y = Y_pixels / scale
a = a_px / scale
b = b_px / scale
r = r_px / scale

# Plotting
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# ---------- Left ----------
ax[0].plot(X, Y, 'b.', label="Blue Mass Point Curve")
ax[0].plot(a, b, 'ro', label="Center of the circle")

theta = np.linspace(0, 2*np.pi, 200)
circle_x = a + r * np.cos(theta)
circle_y = b + r * np.sin(theta)
ax[0].plot(circle_x, circle_y, 'g--', label="Circle")

ax[0].set_aspect('equal', adjustable='box')
ax[0].set_xlabel("X (cm)")
ax[0].set_ylabel("Y (cm)")
ax[0].invert_yaxis()
ax[0].set_title("Blue Mass Point Movement (in cm)")
ax[0].legend()

# ---------- Right ----------
data = pd.read_csv('blue_ball_filled_clean.csv')
frame = data['Frame']
Xb = data['Xb']
Yb = data['Yb']

# Center of Circle
x_center = np.mean(Xb)
y_center = np.mean(Yb)

# === Calculate θ(t) (Unit:rad) ===
theta_rad = np.arctan2(-(Yb - y_center), Xb - x_center)
theta_unwrapped = np.unwrap(theta_rad)  # keep in Rad

fps = 30
t = frame / fps

ax[1].plot(t, theta_unwrapped, color='magenta')
ax[1].set_xlabel("Time t (s)")
ax[1].set_ylabel("Angle θ (rad)")
ax[1].set_title("Angle Change with Time θ(t)")
ax[1].grid(True)

plt.tight_layout()
plt.show()
