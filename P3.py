import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf

# Parameters
Fs = 8000  # Sampling rate
Q = np.random.uniform(5, 10)  # Random Q value between 5-10

# Using measured formant frequencies from Praat
formant_data = {
    'i': {'F1': 291.55, 'F2': 2245.8, 'F3': 3012.03},
    'u': {'F1': 335.67, 'F2': 842.33, 'F3': 2215.12},
    'a': {'F1': 714.32, 'F2': 1089.15, 'F3': 2510.44}
}


F0 = 133.17 

print(f"Q = {Q:.2f}")
print(f"F0 (pitch) = {F0} Hz\n")

# Calculate r_i and theta_i for each formant
def calculate_params(Fi, Bi, Fs):
    theta_i = 2 * np.pi * Fi / Fs
    r_i = np.exp(-2 * np.pi * Bi / Fs)
    return r_i, theta_i

# Create second-order systems
def create_formant_filter(r, theta):
    b = [1]
    a = [1, -2*r*np.cos(theta), r**2]
    return b, a

# Process each vowel
for vowel_name, formants in formant_data.items():
    F1 = formants['F1']
    F2 = formants['F2']
    F3 = formants['F3']
    
    # Bandwidths
    B1 = F1 / Q
    B2 = F2 / Q
    B3 = F3 / Q
    
    print(f"=== Vowel /{vowel_name}/ ===")
    print(f"F1 = {F1:.2f} Hz, B1 = {B1:.2f} Hz")
    print(f"F2 = {F2:.2f} Hz, B2 = {B2:.2f} Hz")
    print(f"F3 = {F3:.2f} Hz, B3 = {B3:.2f} Hz")
    
    # Calculate parameters
    r1, theta1 = calculate_params(F1, B1, Fs)
    r2, theta2 = calculate_params(F2, B2, Fs)
    r3, theta3 = calculate_params(F3, B3, Fs)
    
    print(f"r1 = {r1:.4f}, theta1 = {theta1:.4f}")
    print(f"r2 = {r2:.4f}, theta2 = {theta2:.4f}")
    print(f"r3 = {r3:.4f}, theta3 = {theta3:.4f}\n")
    
    # Create filters
    b1, a1 = create_formant_filter(r1, theta1)
    b2, a2 = create_formant_filter(r2, theta2)
    b3, a3 = create_formant_filter(r3, theta3)
    
    # Calculate frequency response with more points for better resolution
    frequencies = np.logspace(np.log10(10), np.log10(Fs/2), 2000)
    w_digital = 2 * np.pi * frequencies / Fs
    
    # Get individual frequency responses
    _, H1 = signal.freqz(b1, a1, worN=w_digital)
    _, H2 = signal.freqz(b2, a2, worN=w_digital)
    _, H3 = signal.freqz(b3, a3, worN=w_digital)
    
    # Combined frequency response
    H_combined = H1 * H2 * H3
    
    # Create figure with subplots to show individual and combined responses
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Individual formants
    axes[0, 0].semilogx(frequencies, 20*np.log10(np.abs(H1)))
    axes[0, 0].axvline(F1, color='r', linestyle='--', alpha=0.7, label=f'F1={F1:.1f} Hz')
    axes[0, 0].grid(True, which='both', alpha=0.3)
    axes[0, 0].set_xlabel('Frequency (Hz)')
    axes[0, 0].set_ylabel('|H1(ω)| (dB)')
    axes[0, 0].set_title('First Formant')
    axes[0, 0].legend()
    axes[0, 0].set_xlim([10, Fs/2])
    
    axes[0, 1].semilogx(frequencies, 20*np.log10(np.abs(H2)))
    axes[0, 1].axvline(F2, color='r', linestyle='--', alpha=0.7, label=f'F2={F2:.1f} Hz')
    axes[0, 1].grid(True, which='both', alpha=0.3)
    axes[0, 1].set_xlabel('Frequency (Hz)')
    axes[0, 1].set_ylabel('|H2(ω)| (dB)')
    axes[0, 1].set_title('Second Formant')
    axes[0, 1].legend()
    axes[0, 1].set_xlim([10, Fs/2])
    
    axes[1, 0].semilogx(frequencies, 20*np.log10(np.abs(H3)))
    axes[1, 0].axvline(F3, color='r', linestyle='--', alpha=0.7, label=f'F3={F3:.1f} Hz')
    axes[1, 0].grid(True, which='both', alpha=0.3)
    axes[1, 0].set_xlabel('Frequency (Hz)')
    axes[1, 0].set_ylabel('|H3(ω)| (dB)')
    axes[1, 0].set_title('Third Formant')
    axes[1, 0].legend()
    axes[1, 0].set_xlim([10, Fs/2])
    
    # Combined response with formant markers
    axes[1, 1].semilogx(frequencies, 20*np.log10(np.abs(H_combined)), 'b-', linewidth=2)
    axes[1, 1].axvline(F1, color='r', linestyle='--', alpha=0.5, label=f'F1={F1:.1f}')
    axes[1, 1].axvline(F2, color='g', linestyle='--', alpha=0.5, label=f'F2={F2:.1f}')
    axes[1, 1].axvline(F3, color='orange', linestyle='--', alpha=0.5, label=f'F3={F3:.1f}')
    axes[1, 1].grid(True, which='both', alpha=0.3)
    axes[1, 1].set_xlabel('Frequency (Hz)')
    axes[1, 1].set_ylabel('|H(ω)| (dB)')
    axes[1, 1].set_title(f'Combined Response: Vowel /{vowel_name}/')
    axes[1, 1].legend()
    axes[1, 1].set_xlim([10, Fs/2])
    
    plt.suptitle(f'Vowel /{vowel_name}/ - Formant Analysis (Q={Q:.2f})', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'vowel_{vowel_name}_detailed_response.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Also create the standard plot with |H(ω)|² 
    plt.figure(figsize=(12, 6))
    plt.semilogx(frequencies, 10*np.log10(np.abs(H_combined)**2), 'b-', linewidth=2)
    plt.axvline(F1, color='r', linestyle='--', alpha=0.5, label=f'F1={F1:.1f} Hz')
    plt.axvline(F2, color='g', linestyle='--', alpha=0.5, label=f'F2={F2:.1f} Hz')
    plt.axvline(F3, color='orange', linestyle='--', alpha=0.5, label=f'F3={F3:.1f} Hz')
    plt.grid(True, which='both', alpha=0.3)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('|H(ω)|² (dB)')
    plt.title(f"Vowel /{vowel_name}/ Frequency Response\n(F1={F1:.1f}, F2={F2:.1f}, F3={F3:.1f}, Q={Q:.2f})")
    plt.xlim([10, Fs/2])
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'vowel_{vowel_name}_frequency_response.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Generate audio signals
    duration = 1.0
    t = np.arange(0, duration, 1/Fs)
    period_samples = int(Fs / F0)
    
    # Part (a,b): Impulse train excitation
    impulse_train = np.zeros(len(t))
    impulse_train[::period_samples] = 1
    
    output_impulse = signal.lfilter(b1, a1, impulse_train)
    output_impulse = signal.lfilter(b2, a2, output_impulse)
    output_impulse = signal.lfilter(b3, a3, output_impulse)
    output_impulse = output_impulse / np.max(np.abs(output_impulse)) * 0.9
    
    sf.write(f'vowel_{vowel_name}_impulse.wav', output_impulse, Fs)
    
    # Part (c): Half-wave rectified cosine excitation
    cosine_signal = np.cos(2 * np.pi * F0 * t)
    half_wave_rectified = np.maximum(cosine_signal, 0)
    
    output_cosine = signal.lfilter(b1, a1, half_wave_rectified)
    output_cosine = signal.lfilter(b2, a2, output_cosine)
    output_cosine = signal.lfilter(b3, a3, output_cosine)
    output_cosine = output_cosine / np.max(np.abs(output_cosine)) * 0.9
    
    sf.write(f'vowel_{vowel_name}_cosine.wav', output_cosine, Fs)
    
    print(f"Generated audio files for /{vowel_name}/\n")

print("=== All files generated successfully! ===")
print(f"\nNote: Using F0 = {F0} Hz for pitch")