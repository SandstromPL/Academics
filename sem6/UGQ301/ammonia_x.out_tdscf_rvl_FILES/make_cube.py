import numpy as np
from scipy.interpolate import griddata

# 1. Load the original atomic and grid coordinates
atoms = []
grid_pts = []
with open('test.xyz', 'r') as f:
    mode = None
    for line in f:
        if '[Atoms]' in line: mode = 'atoms'; continue
        if '[Grid]' in line: mode = 'grid'; continue
        
        parts = line.split()
        if not parts: continue
        
        if mode == 'atoms':
            # Element Index, Atomic Number, X, Y, Z
            atoms.append((int(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])))
        elif mode == 'grid':
            # Grid Index, X, Y, Z
            grid_pts.append([float(parts[1]), float(parts[2]), float(parts[3])])

grid_pts = np.array(grid_pts)

# 2. Load the density values for the first frame
rho_vals = []
with open('rvlab.tdscf.rho.01900', 'r') as f:
    for line in f:
        parts = line.split()
        if parts: rho_vals.append(float(parts[1]))
rho_vals = np.array(rho_vals)

# Ensure data arrays match in length
min_len = min(len(grid_pts), len(rho_vals))
grid_pts = grid_pts[:min_len]
rho_vals = rho_vals[:min_len]

# 3. Create a uniform 50x50x50 Cartesian Box over the molecule
N = 50
padding = 3.0  # Add some Bohr padding around the molecule
min_bounds = grid_pts.min(axis=0) - padding
max_bounds = grid_pts.max(axis=0) + padding

x = np.linspace(min_bounds[0], max_bounds[0], N)
y = np.linspace(min_bounds[1], max_bounds[1], N)
z = np.linspace(min_bounds[2], max_bounds[2], N)
grid_x, grid_y, grid_z = np.meshgrid(x, y, z, indexing='ij')

# 4. Interpolate the scattered data into the uniform box
print("Interpolating points to a 3D grid... this will just take a second.")
grid_density = griddata(grid_pts, rho_vals, (grid_x, grid_y, grid_z), method='linear', fill_value=0.0)

# 5. Write out the standard .cube format
print("Writing ammonia.cube...")
with open('ammonia01900.cube', 'w') as f:
    f.write("Generated from unstructured rvlab data\n")
    f.write("Electron Density\n")
    f.write(f"{len(atoms)} {min_bounds[0]:.6f} {min_bounds[1]:.6f} {min_bounds[2]:.6f}\n")
    
    dx, dy, dz = x[1]-x[0], y[1]-y[0], z[1]-z[0]
    f.write(f"{N} {dx:.6f} 0.000000 0.000000\n")
    f.write(f"{N} 0.000000 {dy:.6f} 0.000000\n")
    f.write(f"{N} 0.000000 0.000000 {dz:.6f}\n")
    
    for atom in atoms:
        # Atomic number, charge (same as number), X, Y, Z
        f.write(f"{atom[0]} {float(atom[0]):.6f} {atom[1]:.6f} {atom[2]:.6f} {atom[3]:.6f}\n")
    
    # Write density array (Gaussian format requires 6 values per line, Z loops fastest)
    count = 0
    for ix in range(N):
        for iy in range(N):
            for iz in range(N):
                f.write(f"{grid_density[ix,iy,iz]:.5E} ")
                count += 1
                if count % 6 == 0: f.write("\n")
            if count % 6 != 0: 
                f.write("\n")
                count = 0

print("Done! Load ammonia.cube in Avogadro.")
