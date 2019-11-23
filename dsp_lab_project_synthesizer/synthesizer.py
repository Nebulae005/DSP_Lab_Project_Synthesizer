from player import Player
from oscillator import wave_gen
from filter import digital_filter

import numpy as np  
import matplotlib.pyplot as plt

player = Player()
player.open_stream()


# 1) Generate fundamental signal waves

# wave_type = 'sine'
wave_type = 'square'
# wave_type = 'sawtooth'
# wave_type = 'triangle'
frequency = 1320.0
time_length = 1.0
volume = 1.0
RATE = 44100

wave = wave_gen(wave_type, frequency, time_length, volume, RATE)


# 2) Apply a filter

filter_type = 'lowpass'
# filter_type = 'highpass'
filter_ratio = 4.0          # must greater or equal than 1 
cutoff_freq = frequency * filter_ratio

filtered_wave = digital_filter(filter_type, cutoff_freq, wave, RATE)

# 3) Apply an amplifier (ADSR)
# TODO 





## test output

LEN = (int)(frequency * 5)
X_in = np.fft.fft(wave[10000:10000+LEN])
X_out = np.fft.fft(filtered_wave[10000:10000+LEN])

# Frequency domain
plt.figure(1)
f = RATE/LEN * np.arange(0, LEN)
# plt.plot(f, 20 * np.log10(np.abs(X_in)))  # dB scale
# plt.plot(f, 20 * np.log10(np.abs(X_out)))
plt.plot(f, abs(X_in) + 1500)       # linear scale
plt.plot(f, abs(X_out) - 1500)
plt.xlim(0, 0.5*RATE)
# plt.ylim(0, 150)      # set for dB scale
plt.xlabel('Frequency (Hz)')
plt.legend(['original signal','filtered signal'])
plt.show()

# Time domain
plt.figure(2)
plt.plot(wave[10000:10200])
plt.plot(filtered_wave[10000:10200])
plt.legend(['original signal','filtered signal'])
plt.show()


# player.play_wave(wave)
player.play_wave(filtered_wave)