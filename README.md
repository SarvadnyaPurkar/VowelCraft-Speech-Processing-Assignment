# VowelCraft: Speech Processing Assignment

This repository contains the implementation and results of **Assignment 1** for Speech Processing. It documents the workflow from recording speech samples to analyzing acoustic features and synthesizing vowels using digital signal processing techniques.

---

## Project Overview

The assignment is divided into three main parts:

### 1. Speech Recording and Transcription
- Recorded five sentences from the Harvard Sentences collection in a quiet environment.
- Achieved a signal-to-noise ratio (SNR) of over 70 dB, ensuring high-quality recordings.
- Created both **word-level** and **phoneme-level** transcriptions using Praat TextGrid.

### 2. Acoustic Analysis
- Extracted **pitch contour (F0)** using Praat.  
  - Average F0: ~133 Hz.  
  - Histogram showed most values between 100–180 Hz, consistent with typical male speech.
- Computed **formant trajectories (F1, F2, F3)** for vowels /a/, /e/, /i/, /o/, /u/.
- Plotted the **F1–F2 vowel triangle**, clearly showing separation of vowel qualities.

### 3. Vowel Synthesis
- Constructed a **three-formant vocal tract transfer function** using cascaded second-order filters.
- Excitation sources:
  - **Impulse train** with period matching average F0.
  - **Half-wave rectified cosine** (bonus experiment).
- Generated synthetic vowels /i/, /a/, /u/ as WAV files.
- Observed that synthesized vowels captured identity but lacked natural timbre due to omission of higher formants and simplified source modeling.

---

## Key Results

- **Formant Values (Hz):**
  - /i/: F1 = 291, F2 = 2246, F3 = 3012  
  - /u/: F1 = 336, F2 = 842, F3 = 2215  
  - /a/: F1 = 714, F2 = 1089, F3 = 2510  

- **Observations:**
  - Synthesized vowels resembled target vowels but sounded artificial.
  - Naturalness requires inclusion of higher formants (F4, F5), realistic bandwidths, and a glottal source model.

---

## Repository Structure

- `audio/` → Original recordings (Harvard sentences).  
- `textgrid/` → Word and phoneme transcriptions.  
- `plots/` → Pitch contour, formant trajectories, vowel triangle.  
- `synthesis/` → Python code for vowel generation.  
- `wav_output/` → Synthesized vowel audio files.  

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/VowelCraft.git
   cd VowelCraft
