from math import cos, pi
import pyaudio, struct
import tkinter as Tk
import numpy as np
from matplotlib import pyplot

from filter import digital_filter
from adsr import adsr_envolope, adsr
from oscillator import sinwave_gen, sawtooth_gen, square_gen, triangle_gen


#Fs = 8000           # rate (samples/second)
#f1 = 440            # f1 : frequency of sinusoid (Hz)


def on_press(event):
    global CONTINUE
    global ISPRESS

    if event.char == 'q':
      CONTINUE = False

    ISPRESS = 1

def on_release(event):
    global ISPRESS

    ISPRESS = 0

def wave(attack_t, decay_t, sustain_level, release_t, wave_type, filter_type, f1, Fs = 8000):
    global ISPRESS
    global CONTINUE

    BLOCKLEN = 512
    output_block = [0] * BLOCKLEN
    CONTINUE = True
    G = 0
    ISPRESS = 0

    # Define Tkinter root
    root = Tk.Tk()
    root.bind("<KeyPress>", on_press)
    root.bind("<KeyRelease>", on_release)

    L1 = Tk.Label(root, text='demo_02.py')
    L1.pack()

    # Create Pyaudio object
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=Fs,
        input=False,
        output=True,
        frames_per_buffer=128)
    # specify low frames_per_buffer to reduce latency

    # ADSR parameters
    #attack_t = 0.05
    #decay_t = 0.2
    #sustain_level = 0.5
    #release_t = 0.3
    decay_phase = False

    attack_s, decay_s, release_s = adsr_envolope(attack_t, decay_t, sustain_level, release_t, Fs)

    # waveform parameter
    theta = 0.0
    sawtooth_data = 0.0
    triangle_data = 0.0
    idx = 0
    positive_side = True
    increase_slope = True
    #wave_type = 'square'

    # filter parameters
    #filter_type = 'lowpass'
    filter_ratio = 2.3  # must greater or equal than 1
    cutoff_freq = f1 * filter_ratio
    ORDER = 7
    states = np.zeros(ORDER)

    t = [1000. * i / Fs for i in range(BLOCKLEN)]

    pyplot.ion()  # Turn on interactive mode so plot gets updated

    my_fig = pyplot.figure(1)
    my_plot = my_fig.add_subplot(1, 1, 1)
    [my_line] = my_plot.plot(t, output_block)
    my_plot.set_ylim(-32000, 32000)
    my_plot.set_xlim(0, BLOCKLEN * 1000.0 / Fs)  # Time axis in milliseconds
    my_plot.set_xlabel('Time (milliseconds)')

    while CONTINUE:
        root.update()

        for i in range(0, BLOCKLEN):

            G, decay_phase = adsr(ISPRESS, G, decay_phase, attack_s, decay_s, sustain_level, release_s)

            if wave_type == 'sine':
                output_block[i], theta = sinwave_gen(f1, Fs, theta, G)
            elif wave_type == 'sawtooth':
                output_block[i], sawtooth_data = sawtooth_gen(f1, Fs, sawtooth_data, G)
            elif wave_type == 'square':
                output_block[i], idx, positive_side = square_gen(f1, Fs, idx, positive_side, G)
            elif wave_type == 'triangle':
                output_block[i], triangle_data, increase_slope = triangle_gen(f1, Fs, triangle_data, increase_slope, G)

        # Apply a filter
        output_block_filtered, states = digital_filter(filter_type, cutoff_freq, output_block, Fs, ORDER, states)
        output_block_filtered = output_block_filtered.astype(int)

        my_line.set_ydata(output_block)
        # my_line.set_ydata(output_block_filtered)
        my_plot.set_title('Frequency = %.2f' % f1)

        binary_data = struct.pack('h' * BLOCKLEN, *output_block)
        # binary_data = sqtruct.pack('h' * BLOCKLEN, *output_block_filtered)   # 'h' for 16 bits
        stream.write(binary_data)

    print('* Finished')

    pyplot.ioff()

wave(attack_t = 0.05, decay_t = 0.2, sustain_level = 0.5, release_t = 0.3, f1 = 440, wave_type = 'sine', filter_type = 'lowpass')