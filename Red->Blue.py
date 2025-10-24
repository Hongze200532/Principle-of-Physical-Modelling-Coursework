import pandas as pd
import numpy as np

# Read CSV Data
df_blue = pd.read_csv("mass_point_blue_coords.csv")
df_red = pd.read_csv("mass_point_red_coords.csv")

df_blue.columns = ["Frame", "Xb", "Yb"]
df_red.columns = ["Frame", "Xr", "Yr"]

# Combine Two data
df = pd.merge(df_blue, df_red, on="Frame", how="outer").sort_values("Frame")

# Calculate the center of the circle 
valid = df.dropna(subset=["Xb", "Yb", "Xr", "Yr"])
if len(valid) < 3:
    raise ValueError("Error")

def fit_circle(x, y):
    A = np.c_[2*x, 2*y, np.ones(len(x))]
    b = x**2 + y**2
    sol, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    a, b, c = sol
    r = np.sqrt(c + a**2 + b**2)
    return a, b, r

a, b, r = fit_circle(valid["Xb"], valid["Yb"])
print(f"Circle Center: ({a:.2f}, {b:.2f}), Blue Mass Center R {r:.2f}")

ratio = 3 / 2  # Blue : Red

for i in range(len(df)):
    if pd.isna(df.loc[i, "Xb"]) or pd.isna(df.loc[i, "Yb"]):
        xr, yr = df.loc[i, "Xr"], df.loc[i, "Yr"]
        if not (np.isnan(xr) or np.isnan(yr)):
            xb = a - ratio * (xr - a)
            yb = b - ratio * (yr - b)
            df.loc[i, "Xb"] = xb
            df.loc[i, "Yb"] = yb

# Renew CSV File
df.to_csv("blue_ball_filled.csv", index=False, float_format="%.3f")
print(" NewFile ->: blue_ball_filled.csv")
