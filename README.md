# IB_Mathamtics_IA
Repository for IA visualisation

## Realistic Model (Heavy Rope)
`realistic_model.py`
This script models the trajectory of a gondola on a heavy rope with a counterweight system. It solves for the static equilibrium position of the gondola at various horizontal distances.

### Features
- **Physics Model**: Catenary with a concentrated load (the gondola).
- **Constraints**: 
  - Rope linear density ($\lambda$).
  - Counterweight ($M$) that maintains constant horizontal tension component at the start.
  - Geometry: Top station at $(D, H)$, bottom at $(0,0)$.

### Output
The script generates a plot showing:
- **X-Axis**: Horizontal distance from the bottom station (meters).
- **Y-Axis**: Vertical height (meters).
- **Blue Dashed Line**: The unloaded rope shape (static catenary).
- **Red Solid Line**: The trajectory of the gondola as it moves from start to end.

### Usage
Run the script using Python:
```bash
python realistic_model.py
```
Dependencies: `numpy`, `scipy`, `matplotlib`
