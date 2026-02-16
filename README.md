# IB_Mathamtics_IA

## Project Overview
This repository contains Python scripts to visualize and compare mathematical models for the trajectory of a gondola on a rope. It investigates the difference between an idealized model (massless rope forming an ellipse) and a realistic model (heavy rope with counterweight forming catenaries). 

This project serves as documentation for an Internal Assessment for an IB Mathematics AA HL.  

## Project Usage

### 1. Prerequisites
Ensure you have Python installed. This project uses `uv` for dependency management.
First, install `uv` globally:
```bash
pip install uv
```

### 2. Installation
Use the provided `Makefile` to install all project dependencies:
```bash
make install
```
This command runs commands to set up the virtual environment.

### 3. Running the Models

#### Realistic Model (Heavy Rope)
`realistic_model.py`
This script models the trajectory of a gondola on a heavy rope with a counterweight system. It solves for the static equilibrium position of the gondola at various horizontal distances.

To run the simulation:
```bash
uv run realistic_model.py
```

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
