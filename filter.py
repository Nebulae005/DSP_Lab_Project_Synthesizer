import scipy.signal

def digital_filter(filter_type, cutoff_freq, wave, RATE, ORDER, states):
    Nyq_freq = RATE/2
    if cutoff_freq > 0.9 * Nyq_freq:
    	cutoff_freq = 0.9 * Nyq_freq
    b, a = scipy.signal.butter(ORDER, cutoff_freq/Nyq_freq, filter_type, analog = False)
    [filtered_wave, states_out] = scipy.signal.lfilter(b, a, wave, zi = states)
    
    return filtered_wave, states_out