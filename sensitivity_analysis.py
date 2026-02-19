import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
D = 200.0
H = 50.0
lam = 5.0

# Define a baseline Mass (calculated previously to hit the target approx)
M_base = 6000.0 

# Create variations
masses = [M_base * 0.8, M_base * 0.9, M_base, M_base * 1.1, M_base * 1.2]
colors = ['red', 'orange', 'green', 'blue', 'purple']
labels = ['-20%', '-10%', 'Baseline', '+10%', '+20%']

x_vals = np.linspace(0, D, 100)

plt.figure(figsize=(10, 6))

for M, col, lab in zip(masses, colors, labels):
    # Calculate parameter a = M / lambda
    a = M / lam
    
    # Calculate Trajectory
    # Note: With different M, it won't hit (D,H) exactly if fixed at (0,0).
    # This simulates "What happens to the rope sag"
    y_vals = a * (np.cosh(x_vals/a) - 1)
    
    plt.plot(x_vals, y_vals, color=col, label=f'Mass {M:.0f}kg ({lab})')

# Plot Anchors (Target)
plt.plot(D, H, 'ko', markersize=8, label='Target Tower')
plt.plot(0, 0, 'ko')

plt.title("Sensitivity Analysis: Trajectory vs. Counterweight Mass")
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.legend()
plt.grid(True)
plt.show()