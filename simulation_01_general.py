import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import root_scalar, root

# --- 1. PHYSICS CONFIGURATION ---
D = 200.0         # Horizontal span (m)
Tower_H = 50.0    # Height of top station (m)
m_g = 500.0       # Mass of the gondola (kg)
lam = 5.0         # Linear density of rope (kg/m)
g = 9.81          # Gravity (m/s^2)
FRAMES = 100      # Number of frames in the video

# --- 2. CALCULATE UNLOADED RAIL (Counterweight tension) ---
def find_a(a):
    if a <= 0: return 1e9
    return a * (np.cosh(D/a) - 1) - Tower_H

a_static = root_scalar(find_a, bracket=[10, 5000], method='brentq').root
M_cw = a_static * lam # Required counterweight mass

# --- 3. THE PHYSICS SOLVER ---
def solve_state(x_g):
    """Solves the piecewise catenary equations for a specific gondola position"""
    def system(vars):
        y_g, H, c1, c2 = vars
        a = H / (lam * g)
        
        y_L_xg = a * np.cosh((x_g - c1)/a) - a * np.cosh(-c1/a)
        v_shift = y_g - a * np.cosh((x_g - c2)/a)
        y_R_D = a * np.cosh((D - c2)/a) + v_shift
        
        slope_L_xg = np.sinh((x_g - c1)/a)
        slope_R_xg = np.sinh((x_g - c2)/a)
        slope_start = np.sinh(-c1/a)
        
        force_err = H * (slope_R_xg - slope_L_xg) - (m_g * g)
        tension_err = H * np.sqrt(1 + slope_start**2) - (M_cw * g)
        
        return [y_g - y_L_xg, Tower_H - y_R_D, force_err, tension_err]

    # Guess based on the static unloaded rope
    guess = [(Tower_H/D)*x_g - 5, M_cw*g, 0, D]
    sol = root(system, guess, method='lm')
    return sol.x if sol.success else guess

# --- 4. PRE-COMPUTE ANIMATION DATA ---
print("Pre-calculating physics frames to ensure smooth video playback...")
x_gondola_vals = np.linspace(2, D-2, FRAMES) # Avoid exact 0 and D for solver stability
frame_data = []

for x_g in x_gondola_vals:
    y_g, H, c1, c2 = solve_state(x_g)
    a = H / (lam * g)
    
    # Left rope segment
    x_left = np.linspace(0, x_g, 20)
    y_left = a * np.cosh((x_left - c1)/a) - a * np.cosh(-c1/a)
    
    # Right rope segment
    x_right = np.linspace(x_g, D, 20)
    v_shift = y_g - a * np.cosh((x_g - c2)/a)
    y_right = a * np.cosh((x_right - c2)/a) + v_shift
    
    # Combine into one rope array
    rope_x = np.concatenate((x_left, x_right))
    rope_y = np.concatenate((y_left, y_right))
    
    frame_data.append((x_g, y_g, rope_x, rope_y))

# Extract trajectory points
traj_x = [data[0] for data in frame_data]
traj_y = [data[1] for data in frame_data]
min_y = min(traj_y)

print("Calculations complete! Launching animation...")

# --- 5. MATPLOTLIB ANIMATION SETUP ---
fig, ax = plt.subplots(figsize=(12, 7))

# Set fixed axes limits so the screen doesn't jump around
ax.set_xlim(-10, D + 10)
ax.set_ylim(min_y - 10, Tower_H + 10)
ax.set_aspect('equal') # True physical proportions
ax.grid(True, linestyle='--', alpha=0.6)

# Static Elements
ax.plot([0, D], [0, Tower_H], 'ks', markersize=10, label='Stations') # Anchors
unloaded_x = np.linspace(0, D, 100)
unloaded_y = a_static * (np.cosh(unloaded_x/a_static) - 1)
ax.plot(unloaded_x, unloaded_y, 'k--', alpha=0.3, label='Unloaded Rope') # Static rail

# Dynamic Elements (Initialized empty)
rope_line, = ax.plot([], [], 'b-', linewidth=1.5, label='Dynamic Piecewise Rope')
trajectory_line, = ax.plot([], [], 'r-', linewidth=3, alpha=0.7, label='Gondola Trajectory')
gondola_dot, = ax.plot([], [], 'ro', markersize=10, markeredgecolor='black')

# Text labels
ax.set_title("Simulation of Gondola Trajectory (Trajectory vs. Rope Shape)", fontsize=14)
ax.set_xlabel("Horizontal Distance (m)")
ax.set_ylabel("Vertical Height (m)")
ax.legend(loc='upper left')

# Initialization function for the animation
def init():
    rope_line.set_data([], [])
    trajectory_line.set_data([], [])
    gondola_dot.set_data([], [])
    return rope_line, trajectory_line, gondola_dot

# Update function called for each frame
def update(frame):
    x_g, y_g, rope_x, rope_y = frame_data[frame]
    
    # 1. Update the V-shaped piecewise rope
    rope_line.set_data(rope_x, rope_y)
    
    # 2. Update the Gondola position
    gondola_dot.set_data([x_g], [y_g])
    
    # 3. Update the trailing trajectory line (all points up to current frame)
    trajectory_line.set_data(traj_x[:frame+1], traj_y[:frame+1])
    
    return rope_line, trajectory_line, gondola_dot

# Create the animation object
ani = animation.FuncAnimation(
    fig, update, frames=FRAMES, init_func=init,
    interval=50,       # Delay between frames in milliseconds (50ms = 20 FPS)
    blit=True,         # Optimizes drawing by only updating changing parts
    repeat=True        # Loop the animation
)

# --- 6. DISPLAY / SAVE ---
# To save as a GIF or MP4 (requires ffmpeg or imagemagick installed):
# ani.save('gondola_simulation.gif', writer='pillow', fps=20)
# ani.save('gondola_simulation.mp4', writer='ffmpeg', fps=20)

plt.tight_layout()
plt.show()