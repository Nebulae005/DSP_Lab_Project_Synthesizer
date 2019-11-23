import numpy as np
import scipy.signal


def wave_gen(wave_type, frequency, time_length, volume, RATE):

    wave = np.ones(int(RATE * float(time_length)))
    t = np.linspace(0, time_length, RATE * time_length, endpoint=False)

    if wave_type =='sine':
        phases = np.cumsum(2.0 * np.pi * frequency / RATE * wave)
        return volume * np.sin(phases)
    elif wave_type == 'sawtooth':
        return volume * scipy.signal.sawtooth(2*np.pi*frequency*t, 1)
    elif wave_type == 'square':
        return volume * scipy.signal.square(2*np.pi*frequency*t)
    elif wave_type == 'triangle':
        return volume * scipy.signal.sawtooth(2*np.pi*frequency*t, 0.5)