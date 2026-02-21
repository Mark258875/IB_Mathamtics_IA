import numpy as np
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION ---
D = 200.0         # Horizontal distance between anchors (m)
H = 50.0          # Vertical height difference (m)

# The rope length L MUST be greater than the straight-line distance R
R = np.sqrt(D**2 + H**2)
L = 220.0         # Total length of the massless rope (m)

if L <= R:
    raise ValueError(f"Rope length L ({L}) must be greater than distance R ({R:.2f})")

# --- 2. THE MATHEMATICAL MODEL ---
# Define the physical domain: 0 <= x <= D
x_vals = np.linspace(0, D, 200)
y_vals = []

# Using the quadratic coefficients from your derivation:
# y^2(4L^2 - 4H^2) - y(4KH) + (4L^2x^2 - K^2) = 0
A = 4 * (L**2 - H**2)

for x in x_vals:
    # K = L^2 - D^2 + 2xD - H^2
    K = L**2 - D**2 + 2*x*D - H**2
    
    B = -4 * K * H
    C = 4 * L**2 * x**2 - K**2
    
    # Discriminant
    discriminant = B**2 - 4 * A * C
    
    if discriminant < 0:
        # If this happens, the ellipse doesn't exist at this x (shouldn't happen on this domain)
        y_vals.append(np.nan)
    else:
        # We take the negative root for the lower arc of the ellipse (apple falls down)
        y = (-B - np.sqrt(discriminant)) / (2 * A)
        y_vals.append(y)

# --- 3. PLOTTING ---
plt.figure(figsize=(12, 6))

# Plot the trajectory
plt.plot(x_vals, y_vals, 'b-', linewidth=2.5, label=f'Elliptical Trajectory (L={L}m)')

# Plot the anchor points (Foci)
plt.plot([0, D], [0, H], 'ks', markersize=8, label='Anchor Stations (Foci)')

# Highlight the "Docking Paradox" 
# Show that y(0) is below 0, and y(D) is below H
plt.plot([0, 0], [0, y_vals[0]], 'r:', linewidth=2, label='Slack at start')
plt.plot([D, D], [H, y_vals[-1]], 'r:', linewidth=2)

# Graph formatting
plt.title(f"Idealized Massless Rope Model: Elliptical Trajectory of Gondola\nDomain: $x \in [0, {D}]$", fontsize=14)
plt.xlabel("Horizontal Distance x [m]", fontsize=12)
plt.ylabel("Vertical Height y [m]", fontsize=12)
plt.axhline(0, color='black', linewidth=0.8, alpha=0.5)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='lower center')
plt.axis('equal') # Important: keeps the geometry visually accurate

plt.tight_layout()
plt.show()