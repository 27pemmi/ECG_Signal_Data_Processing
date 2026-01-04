# used libraries
import wfdb
from wfdb import processing
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# bandpass filter for noise
def bandpass_filter(signal, fs, lowcut=5, hicut=15, order=4):
    nyquist = 0.5 * fs
    b, a = butter(order, [lowcut / nyquist, hicut / nyquist], btype='band')
    return filtfilt(b, a, signal)

# R-peak labeling
def snap_to_extreme(r_peak, raw_ecg, fs, search_window=40):
    snapped = []
    window = int((search_window / 1000) * fs)
    for p in r_peak:
        segment_start = max(p - window, 0)
        segment_end = min(p + window, len(raw_ecg))
        segment = raw_ecg[segment_start:segment_end]
        max_index = np.argmax(segment)
        min_index = np.argmin(segment)
        if abs(segment[max_index]) > abs(segment[min_index]):
            snapped.append(segment_start + max_index)
        else:
            snapped.append(segment_start + min_index)
    return np.array(snapped)

# HR and other metric computation
def compute_metrics(r_peak, fs):
    if len(r_peak) < 2:
        return 0, 0, np.array([])
    rr_int = np.diff(r_peak) / fs
    HR = 60 / np.mean(rr_int)
    sdnn = np.std(rr_int)
    return HR, sdnn, rr_int

# general ecg segment plot code
def plot_ecg_segment(raw_ecg, time, r_peak, fs, title="ECG Segment"):
    if len(r_peak) > 0:
        first_peak_idx = r_peak[0]
        plot_start = max(first_peak_idx - int(0.5 * fs), 0)
        plot_end = plot_start + int(10 * fs)
    else:
        plot_start, plot_end = 0, int(10 * fs)

    plt.figure(figsize=(10, 4))
    plt.plot(time[plot_start:plot_end], raw_ecg[plot_start:plot_end], label='Raw ECG')
    plot_peak = r_peak[(r_peak >= plot_start) & (r_peak < plot_end)]
    plt.plot(time[plot_peak], raw_ecg[plot_peak], 'ro', label='R-peaks')
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('ECG (mV)')
    plt.legend()
    plt.show()

# resting ecg graph mode
rest = wfdb.rdrecord('16265', pn_dir='nsrdb')
rest_ecg = rest.p_signal[:, 0]
fs_rest = rest.fs
time_rest = np.arange(len(rest_ecg)) / fs_rest

rest_filtered = bandpass_filter(rest_ecg, fs_rest)
rest_peaks = processing.gqrs_detect(sig=rest_filtered, fs=fs_rest)
rest_peaks = snap_to_extreme(rest_peaks, rest_ecg, fs_rest)

# Remove first 1750 beats for sample error/match other sample
rest_peaks = rest_peaks[1750:]

# label and plot rest
plot_ecg_segment(rest_ecg, time_rest, rest_peaks, fs_rest, "Resting ECG Segment")

# compute rest metrics
rest_hr, rest_sdnn, rest_rr = compute_metrics(rest_peaks, fs_rest)

# Total resting beats for reference: 98743

# print important data
print(f"Resting ECG: HR={rest_hr:.1f} BPM, HRV(SDNN)={rest_sdnn:.3f} s")

# stress ecg graph mode
stress = wfdb.rdrecord('323', pn_dir='stdb')
stress_ecg = stress.p_signal[:, 0]
fs_stress = stress.fs
time_stress = np.arange(len(stress_ecg)) / fs_stress

stress_filtered = bandpass_filter(stress_ecg, fs_stress)
stress_peaks = processing.gqrs_detect(sig=stress_filtered, fs=fs_stress)
stress_peaks = snap_to_extreme(stress_peaks, stress_ecg, fs_stress)

# Remove first 1750 beats for sample error/match other sample
stress_peaks = stress_peaks[1750:]

# label and plot rest
plot_ecg_segment(stress_ecg, time_stress, stress_peaks, fs_stress, "Stressed ECG Segment")

# compute stress metrics
stress_hr, stress_sdnn, stress_rr = compute_metrics(stress_peaks, fs_stress)

# Total stress beats for reference: 3542

# print important data
print(f"Stress ECG: HR={stress_hr:.1f} BPM, HRV(SDNN)={stress_sdnn:.3f} s")

# plot both graphs and comparison
min_len = min(len(rest_rr), len(stress_rr))
rest_rr = rest_rr[:min_len]
stress_rr = stress_rr[:min_len]

plt.figure(figsize=(10, 4))
plt.plot(rest_rr, label='Resting RR')
plt.plot(stress_rr, label='Stress RR')
plt.xlabel('Beat Number')
plt.ylabel('RR Interval (s)')
plt.title('RR Interval Comparison')
plt.legend()
plt.show()

# histogram
plt.figure(figsize=(8, 4))
plt.hist(rest_rr, bins=40, alpha=0.6, label='Resting')
plt.hist(stress_rr, bins=40, alpha=0.6, label='Stress')
plt.xlabel('RR Interval (s)')
plt.ylabel('Count')
plt.title('RR Interval Distribution')
plt.legend()
plt.show()