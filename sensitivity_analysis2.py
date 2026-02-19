import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
D = 200.0         # Horizontal span (m)
lam = 5.0         # Rope linear density (kg/m)
M = 5000.0        # Counterweight mass (kg)
g = 9.81          # Gravity

# Parameter a
a = M / lam

# Generate arrays
x_vals = np.linspace(0, D, 100)
# For L, we start slightly above D to avoid division by zero (the singularity)
L_vals = np.linspace(D + 0.1, D + 5.0, 100) 

# --- 1. SLOPE DERIVATIVE (dy/dx) ---
# Formula: sinh(x/a)
dy_dx = np.sinh(x_vals / a)
# Convert to degrees for physical context
angles_deg = np.degrees(np.arctan(dy_dx))

# --- 2. MASS SENSITIVITY (dy/dM) ---
# Formula: (1/lam) * [cosh(u) - 1 - u*sinh(u)] where u = (x*lam)/M
u = (x_vals * lam) / M
dy_dM = (1 / lam) * (np.cosh(u) - 1 - u * np.sinh(u))
# Convert to mm per kg for readability (how many mm the rope drops per 1kg added)
dy_dM_mm = dy_dM * 1000 

# --- 3. LENGTH SENSITIVITY (dh/dL) ---
# Formula: 0.5 * sqrt(3D / (8*(L-D)))
dh_dL = 0.5 * np.sqrt((3 * D) / (8 * (L_vals - D)))

# --- PLOTTING ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

# Plot 1: Slope
ax1.plot(x_vals, angles_deg, 'b-', linewidth=2)
ax1.set_title("1. Trajectory Slope vs. Distance")
ax1.set_xlabel("Horizontal Distance x (m)")
ax1.set_ylabel("Angle (Degrees)")
ax1.grid(True)

# Plot 2: Mass Sensitivity
ax2.plot(x_vals, dy_dM_mm, 'r-', linewidth=2)
ax2.set_title("2. Mass Sensitivity vs. Distance\n(Change in height per 1kg added)")
ax2.set_xlabel("Horizontal Distance x (m)")
ax2.set_ylabel("Sensitivity (mm / kg)")
ax2.grid(True)

# Plot 3: Length Sensitivity
ax3.plot(L_vals - D, dh_dL, 'g-', linewidth=2)
ax3.set_title("3. Sag Sensitivity vs. Cable Slack\n(Singularity at tight cable)")
ax3.set_xlabel("Cable Slack: L - D (m)")
ax3.set_ylabel("Sensitivity dh/dL (m / m)")
ax3.grid(True)
# Add a vertical dashed line to highlight the asymptote
ax3.axvline(x=0, color='k', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()