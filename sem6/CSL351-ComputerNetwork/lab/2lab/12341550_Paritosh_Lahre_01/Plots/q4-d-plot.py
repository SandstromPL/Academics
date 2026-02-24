import matplotlib.pyplot as plt
import numpy as np

# Data extracted from your screenshots
# We use 'None' to represent hops where packets timed out (* * *)

# ----------------- Google.com Data -----------------
# Hops: 1-15
google_hops = list(range(1, 16))
google_rtts = [
    65.62,  # Hop 1 (Avg of 65.683, 65.603, 65.579)
    65.53,  # Hop 2
    69.83,  # Hop 3
    69.74,  # Hop 4
    None,   # Hop 5 (* * *)
    None,   # Hop 6 (* * *)
    None,   # Hop 7 (* * *)
    75.37,  # Hop 8
    77.82,  # Hop 9
    None,   # Hop 10 (* * *)
    83.97,  # Hop 11
    92.14,  # Hop 12
    91.55,  # Hop 13
    97.77,  # Hop 14
    76.87   # Hop 15
]

# ----------------- Youtube.com Data -----------------
# Hops: 1-13
youtube_hops = list(range(1, 14))
youtube_rtts = [
    32.84,  # Hop 1
    33.02,  # Hop 2
    34.00,  # Hop 3
    34.54,  # Hop 4
    None,   # Hop 5 (* * *)
    None,   # Hop 6 (* * *)
    None,   # Hop 7 (* * *)
    47.63,  # Hop 8
    49.54,  # Hop 9
    None,   # Hop 10 (* * *)
    62.64,  # Hop 11
    48.73,  # Hop 12
    94.63   # Hop 13
]

# ----------------- Instagram.com Data -----------------
# Hops: 1-12 (Timeouts after hop 12)
instagram_hops = list(range(1, 13))
instagram_rtts = [
    56.66,  # Hop 1
    56.52,  # Hop 2
    56.78,  # Hop 3
    58.51,  # Hop 4
    None,   # Hop 5 (* * *)
    None,   # Hop 6 (* * *)
    None,   # Hop 7 (* * *)
    75.00,  # Hop 8
    85.30,  # Hop 9
    75.00,  # Hop 10 (Avg of non-star values)
    76.80,  # Hop 11
    82.68   # Hop 12
]

# ----------------- Plotting -----------------
plt.figure(figsize=(12, 6))

# Plot Google
plt.plot(google_hops, google_rtts, marker='o', label='google.com', color='blue', linestyle='-')

# Plot Youtube
plt.plot(youtube_hops, youtube_rtts, marker='s', label='youtube.com', color='red', linestyle='-')

# Plot Instagram
plt.plot(instagram_hops, instagram_rtts, marker='^', label='instagram.com', color='purple', linestyle='-')

# Graph formatting
plt.title('Traceroute RTT Analysis (Hop vs Latency)')
plt.xlabel('Hop Number')
plt.ylabel('Round Trip Time (ms)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.xticks(np.arange(1, 16, 1))  # Ensure all hop numbers are shown on x-axis

# Show the plot
plt.tight_layout()
plt.show()
