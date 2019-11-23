import numpy as np  
import scipy.signal

def digital_filter(filter_type, cutoff_freq, wave, RATE):
    ORDER = 7
    Nyq_freq = RATE/2
    states = np.zeros(ORDER)

    b, a = scipy.signal.butter(ORDER, cutoff_freq/Nyq_freq, filter_type, analog = False)
    [filtered_wave, states] = scipy.signal.lfilter(b, a, wave, zi = states)
    
    return filtered_wave