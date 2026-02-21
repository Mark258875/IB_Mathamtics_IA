import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import root_scalar, root

# ==========================================
# 1. CONFIGURATION
# ==========================================
D = 200.0         # Horizontal span (m)
H_tower = 300.0    # Vertical height difference (m)
m_g = 250.0       # Mass of the loaded gondola (kg)
lam = 5.0         # Rope linear density (kg/m)
g = 9.81          # Gravity (m/s^2)

# --- 2. CALCULATE TRUE COUNTERWEIGHT (Loaded Horizontal Departure) ---
def find_a(a):
    if a <= 0: return 1e9
    # alpha is the starting angle required just to support the gondola
    alpha = np.arcsinh(m_g / (a * lam)) 
    return a * (np.cosh(D/a + alpha) - np.cosh(alpha)) - H_tower

# Find the catenary constant for the loaded system
sol_a = root_scalar(find_a, bracket=[10, 8000], method='brentq')
a_loaded = sol_a.root
M_cw = a_loaded * lam # True Counterweight Mass

print("\n" + "="*40)
print(" TRUE PHYSICS CALCULATIONS")
print("="*40)
print(f"-> Gondola Mass (m_g):       {m_g} kg")
print(f"-> REQUIRED COUNTERWEIGHT:   {M_cw:.2f} kg")
print("="*40 + "\n")

# --- 3. CALCULATE UNLOADED ROPE (Gondola removed) ---
def solve_unloaded():
    def sys(vars):
        H_u, c1_u = vars
        a_u = H_u / (lam * g)
        
        y_D = a_u * np.cosh((D - c1_u)/a_u) - a_u * np.cosh(-c1_u/a_u)
        T_0 = H_u * np.cosh(-c1_u/a_u)
        
        return [y_D - H_tower, T_0 - (M_cw * g)]

    guess = [M_cw * g * 0.95, 10] 
    sol = root(sys, guess, method='lm')
    return sol.x if sol.success else guess

H_unl, c1_unl = solve_unloaded()
a_unl = H_unl / (lam * g)
unloaded_x = np.linspace(0, D, 100)
unloaded_y = a_unl * np.cosh((unloaded_x - c1_unl)/a_unl) - a_unl * np.cosh(-c1_unl/a_unl)

# --- 4. PHYSICS SOLVER FOR MOVING GONDOLA ---
def solve_state(x_g):
    def system(vars):
        y_g, H_tens, c1, c2 = vars
        a = H_tens / (lam * g)
        
        y_L_xg = a * np.cosh((x_g - c1)/a) - a * np.cosh(-c1/a)
        v_shift = y_g - a * np.cosh((x_g - c2)/a)
        y_R_D = a * np.cosh((D - c2)/a) + v_shift
        
        slope_L_xg = np.sinh((x_g - c1)/a)
        slope_R_xg = np.sinh((x_g - c2)/a)
        slope_start = np.sinh(-c1/a)
        
        err1 = y_g - y_L_xg
        err2 = H_tower - y_R_D
        err3 = H_tens * (slope_R_xg - slope_L_xg) - (m_g * g)
        err4 = H_tens * np.sqrt(1 + slope_start**2) - (M_cw * g)
        
        return [err1, err2, err3, err4]

    guess = [(H_tower/D)*x_g, M_cw*g, 0, D]
    sol = root(system, guess, method='lm')
    return sol.x if sol.success else guess

# --- 5. PRE-COMPUTE FRAMES ---
print("Simulating physics frames...")
FRAMES = 80
x_gondola_vals = np.linspace(0.1, D-0.1, FRAMES) 
frame_data = []

for x_g in x_gondola_vals:
    y_g, H_tens, c1, c2 = solve_state(x_g)
    a = H_tens / (lam * g)
    
    x_left = np.linspace(0, x_g, 25)
    y_left = a * np.cosh((x_left - c1)/a) - a * np.cosh(-c1/a)
    
    x_right = np.linspace(x_g, D, 25)
    v_shift = y_g - a * np.cosh((x_g - c2)/a)
    y_right = a * np.cosh((x_right - c2)/a) + v_shift
    
    rope_x = np.concatenate((x_left, x_right))
    rope_y = np.concatenate((y_left, y_right))
    frame_data.append((x_g, y_g, rope_x, rope_y))

traj_x = [data[0] for data in frame_data]
traj_y = [data[1] for data in frame_data]

# --- 6. MATPLOTLIB ANIMATION ---
fig, ax = plt.subplots(figsize=(12, 7))

ax.set_xlim(-10, D + 10)
ax.set_ylim(-5, H_tower + 10)
ax.set_aspect('equal') 
ax.grid(True, linestyle='--', alpha=0.6)
ax.axhline(0, color='black', linewidth=1, alpha=0.8) # The y=0 ground line

# Plot Stations
ax.plot([0, D], [0, H_tower], 'ks', markersize=10, label='Stations')

# Plot the Unloaded Rope (Dashed Line)
ax.plot(unloaded_x, unloaded_y, 'k--', linewidth=2, alpha=0.5, label='Empty Rope (Gondola at station)')

# Dynamic Elements
rope_line, = ax.plot([], [], 'b-', linewidth=2, label='Loaded Piecewise Rope')
trajectory_line, = ax.plot([], [], 'r-', linewidth=3, alpha=0.6, label='Gondola Trajectory')
gondola_dot, = ax.plot([], [], 'ro', markersize=10, markeredgecolor='black')

# --- ADD PARAMETER TEXT BOX ---
text_str = '\n'.join((
    r'$\mathbf{System\ Parameters:}$',
    f'$D = {D:.1f}$ m (Span)',
    f'$H = {H_tower:.1f}$ m (Tower Height)',
    f'$m_g = {m_g:.1f}$ kg (Gondola Mass)',
    f'$\lambda = {lam:.1f}$ kg/m (Rope Density)',
    r'$\mathbf{Calculated:}$',
    f'$M_{{cw}} = {M_cw:.1f}$ kg (Counterweight)'
))
props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)


ax.set_title("Gondola Trajectory with Horizontal Departure Constraint", fontsize=14)
ax.set_xlabel("Horizontal Distance (m)")
ax.set_ylabel("Vertical Height (m)")
ax.legend(loc='upper right') # Moved legend to avoid overlapping the text box

def init():
    rope_line.set_data([], [])
    trajectory_line.set_data([], [])
    gondola_dot.set_data([], [])
    return rope_line, trajectory_line, gondola_dot

def update(frame):
    x_g, y_g, rope_x, rope_y = frame_data[frame]
    rope_line.set_data(rope_x, rope_y)
    gondola_dot.set_data([x_g], [y_g])
    trajectory_line.set_data(traj_x[:frame+1], traj_y[:frame+1])
    return rope_line, trajectory_line, gondola_dot

ani = animation.FuncAnimation(fig, update, frames=FRAMES, init_func=init, interval=60, blit=True)
plt.tight_layout()
plt.show()