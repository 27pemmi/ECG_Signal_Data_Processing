== ECG Signal Data Processing: Resting vs Exercising 
This independent project analyzes authentic ECG (electrocardiogram) data to compare heart activity during rest to heart activity during exercise using biomedical signal processing ideas.

= Databases (Physionet):
  - Resting ECG Data: MIT-BIH Normal Sinus Rhythm Database (record 16265)
    https://physionet.org/content/nsrdb/1.0.0/ 
  - Exercise ECG Data: MIT-BIH ST Change Database (record 323)
  	https://physionet.org/content/stdb/1.0.0/ 

= Applied ideas:
  - Bandpass filtering (5-15 Hz)
  	  Bandpass filtering removes noise from the data, which can come from breathing, moving during data collection, and machine interference at higher frequencies. By limiting the          sample to 5-15 Hz, the QRS complex is much more clear and easier to process. 
  - Use of WFDB for QRS detection
  	  The WFDB (Waveform Database) is a well-known tool able to detect QRS peaks in real-world ECGs. 
  - Positive and negative R-peak localization
  	  R-peaks (the top of the heartbeat) can be recorded as spiking up (positive) or as spiking down (negative). My R-peak localization can detect a peak in either direction based on       magnitude.
  - Heart rate + variability calculated with SDNN
  	  The heart rate is calculated through RR peaks (time between R-peaks). The variability of the heart rates is calculated using SDNN (Standard Deviation of Normal-Normal                 intervals), which I use to show how much the heart rates vary over time. 
	
= Final Results:
  - The Exercise ECG shows a much higher overall heart rate compared to the heart rate at rest. 
  - Heart rate variability is decreased during exercise/stress (More consistent RR intervals - more sympathetic influence)
  - RR interval plots and histograms display these findings, with the stressed ECG showing shorter and more concentrated RR intervals than resting. 

= Tools used:
  - Python (PyCharm)
  - NumPy
  - SciPy
  - Matplotlib
  - WFDB
