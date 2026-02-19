import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
D = 200.0         # Distance (m)
H = 50.0          # Height (m)
m_gondola = 500.0 # Mass (kg)
M_counter = 5000.0 # Mass of counterweight (kg)
lam = 5.0         # Rope density (kg/m)
g = 9.81

# Parameter 'a' from the counterweight
a = M_counter / lam

# Generate positions
x_vals = np.linspace(0, D, 100)

# --- CALCULATE FORCES ---
# 1. Slope Angle theta
# tan(theta) = sinh(x/a)
# sin(theta) = tanh(x/a)
# cos(theta) = 1 / cosh(x/a)

traction_forces = []
cable_tensions = []
angles_deg = []

for x in x_vals:
    # Calculate angle at this specific x
    # Note: This assumes the static rail shape (y = a*cosh(x/a))
    # For a moving kink, it's slightly different, but this is the standard approximation
    slope = np.sinh(x/a)
    theta_rad = np.arctan(slope)
    
    # Traction Force (The pull required to overcome gravity along slope)
    # F_pull = m * g * sin(theta)
    f_pull = m_gondola * g * np.sin(theta_rad)
    traction_forces.append(f_pull)
    
    # Cable Tension at this point
    # T(y) = T_min + lambda * g * y
    # But simpler: T(x) = H / cos(theta) = (M*g) * cosh(x/a)
    # This is the tension in the ROPE itself at point x
    t_cable = (M_counter * g) * np.cosh(x/a)
    cable_tensions.append(t_cable)
    
    angles_deg.append(np.degrees(theta_rad))

# --- PLOTTING ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Traction Force
ax1.plot(x_vals, traction_forces, 'r-', linewidth=2)
ax1.set_title("Required Traction Force (Haul Rope)")
ax1.set_xlabel("Distance x (m)")
ax1.set_ylabel("Force (Newtons)")
ax1.grid(True)
ax1.axhline(y=max(traction_forces), color='r', linestyle=':', label=f'Max: {max(traction_forces):.0f} N')
ax1.legend()

# Plot 2: Cable Tension
ax2.plot(x_vals, np.array(cable_tensions)/1000, 'b-', linewidth=2)
ax2.set_title("Main Cable Tension")
ax2.set_xlabel("Distance x (m)")
ax2.set_ylabel("Tension (kN)")
ax2.grid(True)
ax2.axhline(y=max(cable_tensions)/1000, color='b', linestyle=':', label=f'Max: {max(cable_tensions)/1000:.1f} kN')
ax2.legend()

plt.suptitle(f"Force Analysis: Gondola Mass {m_gondola}kg on Counterweight {M_counter}kg")
plt.show()