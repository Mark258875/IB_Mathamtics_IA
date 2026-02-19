# GitHub Copilot Instructions for IB Mathematics IA Project

## Project Context
This repository contains code for an International Baccalaureate (IB) Mathematics Analysis and Approaches HL Internal Assessment (IA).
The project investigates the trajectory of a gondola on a rope, comparing two mathematical models:
1. **Idealized Model**: Treats the rope as massless. The trajectory is an ellipse where the sum of distances to the anchors is constant ($L$).
2. **Realistic Model**: Treats the rope as having mass (linear density $\lambda$). The trajectory is defined by the equilibrium position of a catenary with a concentrated load (the gondola).

## Mathematical Models
When discussing or implementing code, adhere to these definitions:
- **Catenary Equation**: $y = a \cosh(x/a) + C$
- **Force Balance at Kink**: The difference in vertical tension components at the gondola must equal the gondola's weight ($W$).
- **Geometric Constraints**: The total length of the rope segments must equal the fixed rope length $L$.

## Code Style & Conventions
- **Language**: Python 3.12+
- **Key Libraries**: `numpy`, `scipy` (for optimization/root-finding), `matplotlib` (for visualization).
- **Dependency Management**: Use `uv` for managing dependencies. Run scripts with `uv run <script.py>`.
- **Plotting**:
  - Use clear, academic-style plots.
  - Always label axes with units (e.g., "Distance (m)", "Height (m)").
  - Use legends to distinguish between models (e.g., "Idealized", "Realistic", "Unloaded Rope").

## Tone and Approach
- Maintain an academic and rigorous tone suitable for a mathematics paper.
- Prioritize mathematical accuracy over code complexity.
- When explaining concepts, link the code implementation back to the physical principles (Lagrangian mechanics, potential energy minimization, force vectors).
