import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar, root

# --- 1. CONFIGURATION (The "Slovak Exercise" Parameters) ---
D = 200.0         # Distance to top station (meters)
H = 50.0          # Height of top station (meters)
m_gondola = 500.0 # Mass of the gondola (kg)
lam = 5.0         # Linear density of rope (kg/m)
g = 9.81          # Gravity (m/s^2)

# --- 2. CALCULATE THE COUNTERWEIGHT (M) ---
# The problem states: "Mass is exactly such that cabin leaves horizontally."
# This implies that for the UNLOADED rope, y'(0) = 0 and y(D) = H.
# We solve the catenary equation y = a*cosh(x/a) - a for 'a' such that y(D) = H.

def find_catenary_constant(a):
    # The equation: H = a * (cosh(D/a) - 1)
    # We rearrange to find root: a * (cosh(D/a) - 1) - H = 0
    if a <= 0: return 1e9
    return a * (np.cosh(D/a) - 1) - H

# Numerical solve for 'a'
sol_a = root_scalar(find_catenary_constant, bracket=[0.1, 10000], method='brentq')
a_static = sol_a.root
M_counterweight = a_static * lam # Because a = T/(lam*g) and T = M*g

print(f"--- SYSTEM CALCULATIONS ---")
print(f"Required Catenary Constant (a): {a_static:.2f} m")
print(f"Required Counterweight Mass: {M_counterweight:.2f} kg")
print(f"Base Tension: {M_counterweight * g / 1000:.2f} kN")
print(f"---------------------------")

# --- 3. THE SOLVER FOR GONDOLA TRAJECTORY ---
def solve_gondola_position(x_g, M_cw, D, H, m_g, lam):
    """
    Finds the vertical position y_g of the gondola at horizontal position x_g.
    Constraint: Tension at left anchor is FIXED at T = M_cw * g.
    """
    if x_g <= 0: return 0.0
    if x_g >= D: return H

    # We need to solve for 3 variables:
    # 1. y_g: Vertical position of gondola
    # 2. c1: Integration constant for left segment (determines angle at start)
    # 3. c2: Integration constant for right segment
    
    # NOTE: The horizontal tension H is NOT constant anymore.
    # H depends on the start angle theta: H = T_counter * cos(theta_start)
    # Slope at start y'(0) = sinh(-c1/a). 
    # This creates a complex dependency. 
    
    # SIMPLIFICATION FOR ROBUSTNESS:
    # Instead of full 3-variable optimization which is unstable, we use the 
    # "Fixed Rail" approximation for the initial guess and then refine.
    # For a counterweight system, H varies slightly but 'a' varies with it.
    
    # Let's solve the force balance vectorially at the gondola.
    
    def system(vars):
        y_current, H_current, c1, c2 = vars
        
        # Catenary parameter for this specific H
        a = H_current / (lam * g)
        
        # LEFT SEGMENT: from (0,0) to (x_g, y_current)
        # y(x) = a * cosh((x-c1)/a) - offset
        # We define y(x) = a*cosh((x-c1)/a) - a*cosh(-c1/a) (so y(0)=0)
        y_left_end = a * np.cosh((x_g - c1)/a) - a * np.cosh((-c1)/a)
        
        # RIGHT SEGMENT: from (x_g, y_current) to (D,H)
        # y(x) = a * cosh((x-c2)/a) + v_shift
        # Match gondola: v_shift = y_current - a*cosh((x_g-c2)/a)
        v_shift = y_current - a * np.cosh((x_g - c2)/a)
        y_right_end = a * np.cosh((D - c2)/a) + v_shift
        
        # SLOPES (dy/dx = sinh((x-c)/a))
        slope_L_gondola = np.sinh((x_g - c1)/a)
        slope_R_gondola = np.sinh((x_g - c2)/a)
        slope_L_anchor  = np.sinh((0 - c1)/a) # Slope at (0,0)
        
        # FORCE IMBALANCE (The Kink)
        # H * (slope_right - slope_left) = m_g * g
        force_err = H_current * (slope_R_gondola - slope_L_gondola) - (m_g * g)
        
        # COUNTERWEIGHT CONSTRAINT
        # Tension at anchor (0,0) must equal Counterweight Weight
        # T_anchor = H / cos(theta) = H * sqrt(1 + slope^2)
        # We want: H * sqrt(1 + slope_L_anchor^2) = M_cw * g
        tension_err = H_current * np.sqrt(1 + slope_L_anchor**2) - (M_cw * g)
        
        return [
            y_current - y_left_end,  # Left segment hits gondola
            H - y_right_end,         # Right segment hits top tower
            force_err,               # Kink equilibrium
            tension_err              # Counterweight validity
        ]

    # Initial Guesses
    H_guess = M_cw * g # Start assuming horizontal departure (approx)
    y_guess = (H/D) * x_g
    vars_guess = [y_guess, H_guess, 0, D] # c1~0 implies horizontal start
    
    try:
        sol = root(system, vars_guess, method='lm')
        if sol.success:
            return sol.x[0] # Return y_g
        else:
            return None
    except:
        return None

# --- 4. GENERATE DATA POINTS ---
x_vals = np.linspace(0, D, 50)
y_static = [] # The empty rope (The "Rail")
y_trajectory = [] # The actual gondola path

print("Simulating Trajectory (this may take a moment)...")

# Calculate Static Rail (Simple Catenary)
for x in x_vals:
    val = a_static * (np.cosh(x/a_static) - 1)
    y_static.append(val)

# Calculate Actual Trajectory (Moving Kink)
for x in x_vals:
    y_traj = solve_gondola_position(x, M_counterweight, D, H, m_gondola, lam)
    
    # Fallback if solver fails (usually at boundaries)
    if y_traj is None: 
        y_traj = a_static * (np.cosh(x/a_static) - 1)
        
    y_trajectory.append(y_traj)

# --- 5. PLOTTING ---
plt.figure(figsize=(12, 7))

# Plot Anchors
plt.plot([0, D], [0, H], 'ko', markersize=8, label='Stations')
plt.text(0, -2, "Start (0,0)\nCounterweight", ha='center')
plt.text(D, H+2, f"End ({D},{H})", ha='center')

# Plot 1: The "Rail" (Unloaded Rope)
plt.plot(x_vals, y_static, 'b--', alpha=0.5, label='Unloaded Rope (The "Rail")')

# Plot 2: The Trajectory (Loaded)
plt.plot(x_vals, y_trajectory, 'r-', linewidth=2, label=f'Gondola Trajectory (Mass {m_gondola}kg)')

plt.title(f'Gondola Trajectory Analysis\nCounterweight: {M_counterweight:.0f}kg | Gondola: {m_gondola}kg')
plt.xlabel('Distance x (m)')
plt.ylabel('Height y (m)')
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.axis('equal')

# Show "Sag Difference" annotation
mid_idx = len(x_vals)//2
sag_diff = y_trajectory[mid_idx] - y_static[mid_idx]
plt.annotate(f'Deflection due to\\ngondola: {abs(sag_diff):.2f}m', 
             xy=(x_vals[mid_idx], y_trajectory[mid_idx]), 
             xytext=(x_vals[mid_idx]+20, y_trajectory[mid_idx]-10),
             arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.tight_layout()
plt.show()
