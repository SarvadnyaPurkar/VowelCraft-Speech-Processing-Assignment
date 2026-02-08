import parselmouth
import numpy as np
import matplotlib.pyplot as plt

# Load sound
snd = parselmouth.Sound("audioA1.wav")

# Extract pitch (filtered autocorrelation)
pitch = snd.to_pitch()

# Get pitch values (Hz)
f0_values = pitch.selected_array['frequency']
f0_values = f0_values[f0_values > 0]  # remove unvoiced frames

# Average F0
avg_f0 = np.mean(f0_values)
print("Average F0:", avg_f0)

# Histogram
plt.hist(f0_values, bins=50, color="skyblue", edgecolor="black")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Count")
plt.title("Histogram of F0")
plt.show()
