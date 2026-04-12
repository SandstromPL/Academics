import numpy as np
import matplotlib.pyplot as plt

# 1. Parse the output file
times = []
mu_x = []

print("Parsing rvlab.tdscf.out...")
with open('rvlab.tdscf.out', 'r') as f:
    for line in f:
        # We only care about the lines reporting the time steps
        if "Step EAS:" in line:
            parts = line.split()
            # Ensure the line has all the columns we need
            if len(parts) >= 8:
                try:
                    t = float(parts[3])
                    dipole_x = float(parts[5])
                    times.append(t)
                    mu_x.append(dipole_x)
                except ValueError:
                    continue

times = np.array(times)
mu_x = np.array(mu_x)

print(f"Successfully extracted {len(times)} time steps.")

# 2. Process the signal
dt = times[1] - times[0]  # Time step duration (should be 0.2 a.u.)
delta_mu = mu_x - mu_x[0] # Subtract the initial resting state so it oscillates around 0

# Apply a damping function (Exponential) 
# This simulates natural line broadening and prevents weird visual artifacts
# from the simulation ending abruptly at 2000 steps.
gamma = 0.005 
damped_signal = delta_mu * np.exp(-gamma * times)

# 3. Perform the Fast Fourier Transform (FFT)
N = len(times)

# Calculate frequencies in atomic units, then convert to eV (1 a.u. = 27.2114 eV)
freq_au = np.fft.fftfreq(N, d=dt) * (2.0 * np.pi)
energy_ev = freq_au * 27.2114

# Calculate the actual spectrum intensity
spectrum_complex = np.fft.fft(damped_signal) * dt
intensity = energy_ev * np.abs(np.imag(spectrum_complex))

# We only care about positive energies, usually up to ~25 eV for UV-Vis absorption
valid_indices = (energy_ev > 0) & (energy_ev < 25)
plot_energy = energy_ev[valid_indices]
plot_intensity = intensity[valid_indices]

# 4. Plot the results side-by-side
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Top Plot: The raw time-domain oscillation (The "Sloshing")
ax1.plot(times, delta_mu, color='#1f77b4', label='Raw Dipole Response')
ax1.plot(times, damped_signal, color='#d62728', alpha=0.7, label='Damped Signal (Used for FFT)')
ax1.set_title('Time-Dependent Dipole Moment (X-axis)')
ax1.set_xlabel('Time (Atomic Units)')
ax1.set_ylabel('Dipole Moment (a.u.)')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)

# Bottom Plot: The resulting Absorption Spectrum (The "Colors")
ax2.plot(plot_energy, plot_intensity, color='#9467bd', linewidth=2)
ax2.fill_between(plot_energy, plot_intensity, color='#9467bd', alpha=0.2)
ax2.set_title('Calculated Absorption Spectrum of Ammonia')
ax2.set_xlabel('Energy (eV)')
ax2.set_ylabel('Intensity (arb. units)')
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
