import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar

# ==========================================
# 1. CONFIGURATION
# ==========================================
D = 200.0         # Horizontal span (m)
H_tower = 50.0    # Vertical height difference (m)
lam = 5.0         # Rope linear density (kg/m)
# Note: Gondola mass is omitted here because the continuous 
# "rigid rail" trajectory equation depends only on M_cw and lambda.

# --- 2. SOLVE THE TRANSCENDENTAL EQUATION ---
# Equation: H = a * [cosh(D/a) - 1]
def find_a(a):
    if a <= 0: return 1e9
    return a * (np.cosh(D/a) - 1) - H_tower

# Numerically find the catenary constant 'a'
sol_a = root_scalar(find_a, bracket=[10, 5000], method='brentq')
a = sol_a.root

# Calculate the required Counterweight Mass
M_cw = a * lam

# --- 3. GENERATE TRAJECTORY DATA ---
x_vals = np.linspace(0, D, 200)
# Final Equation: y(x) = (M_cw / lam) * [cosh((x * lam) / M_cw) - 1]
y_vals = (M_cw / lam) * (np.cosh((x_vals * lam) / M_cw) - 1)

# --- 4. PLOTTING ---
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the continuous trajectory
ax.plot(x_vals, y_vals, 'r-', linewidth=3, label='Theoretical Gondola Trajectory')

# Plot the anchor stations
ax.plot([0, D], [0, H_tower], 'ks', markersize=10, label='Anchor Stations')

# --- ADD PARAMETER TEXT BOX ---
text_str = '\n'.join((
    r'$\mathbf{System\ Parameters:}$',
    f'$D = {D:.1f}$ m (Span)',
    f'$H = {H_tower:.1f}$ m (Tower Height)',
    f'$\lambda = {lam:.1f}$ kg/m (Rope Density)',
    r'$\mathbf{Calculated\ Constraint:}$',
    f'$M_{{cw}} = {M_cw:.1f}$ kg (Counterweight)'
))
props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)

# Graph formatting
ax.set_title("Gondola Trajectory: Continuous Catenary Model", fontsize=14)
ax.set_xlabel("Horizontal Distance $x$ (m)", fontsize=12)
ax.set_ylabel("Vertical Height $y$ (m)", fontsize=12)
ax.axhline(0, color='black', linewidth=1, alpha=0.5) # Ground line
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='lower right')

# Keep the aspect ratio visually accurate to real life
ax.set_aspect('equal') 

# Adjust layout and display
plt.tight_layout()

# Optional: Uncomment the line below to save the image directly to your folder
# plt.savefig('final_trajectory.png', dpi=300, bbox_inches='tight')

plt.show()