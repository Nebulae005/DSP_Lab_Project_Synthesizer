import tkinter as Tk

from math import cos, pi 
import pyaudio, struct   
import numpy as np 
from matplotlib import pyplot
from PIL import Image, ImageTk

from filter import digital_filter
from adsr import adsr_slope, adsr_main
from oscillator import sinwave_gen, sawtooth_gen, square_gen, triangle_gen

Fs = 8000           # rate (samples/second)
f1 = 440            # f1 : frequency of sinusoid (Hz)
r = 2 ** (1.0/12.0)

def fun_wave():
    global wave_type
    if wave_v.get() == 0:
        wave_type = 'sine'
    elif wave_v.get() == 1:
        wave_type = 'sawtooth'
    elif wave_v.get() == 2:
        wave_type = 'square'
    elif wave_v.get() == 3:
        wave_type = 'triangle'
    print('The wave type you selected is ' + wave_type)

def fun_fil():
    global set_filter
    global filter_type
    if filter_v.get() == 0:
        set_filter = False
    elif filter_v.get() == 1:
        set_filter = True
        filter_type = 'lowpass'
    elif filter_v.get() == 2:
        set_filter = True
        filter_type = 'highpass'
    print('The filter type is:' + filter_type)
    # return filter_type

def fun_freq(v):
    global cutoff_freq
    cutoff_freq = f1 * freq_v.get()
    if cutoff_freq > Fs * 0.45:
        cutoff_freq = Fs * 0.45
    L_freq.config(text = 'Cut-off frequency: ' + str(cutoff_freq))

def getvalue_fun(event):
    global attack_s
    global decay_s
    global sustain_level
    global release_s
    sustain_level = S.get()
    attack_s, decay_s, release_s = adsr_slope(A.get(), D.get(), S.get(), R.get(), Fs)

def on_press(event):
    global CONTINUE
    global ISPRESS
    global f1
    global r
    global notes
    f1 = 440.0

    index = 0
    if event.char == 'q':
        CONTINUE = False
    elif event.char == '0':
        index = 9
        ISPRESS = 1
    elif event.char == '-':
        index = 10
        ISPRESS = 1
    elif event.char == '=':
        index = 11
        ISPRESS = 1
    elif '1' <= event.char <= '9':
        index = ord(event.char) - ord('1')
        ISPRESS = 1
    else:
        ISPRESS = 0
    f1 *= r ** index
    notes.set(index)

def on_release(event):
    global ISPRESS
    global notes
    ISPRESS = 0
    notes.set(-1j)

def quit_fun():
    global CONTINUE
    CONTINUE = False

root = Tk.Tk()
root.title('keyboard synthesizer')

root.bind("<KeyPress>", on_press)
root.bind("<KeyRelease>", on_release)

# Title
label = Tk.Label(root, text = 'Keyboard Synthesizer', font=('', 16)).grid(row=0, column=1, rowspan=1, columnspan=5, pady = 10, padx = 10)

# Select wave form
wave_v = Tk.IntVar()
wave = Tk.LabelFrame(root, text = ' Select wave type ', width=250, height=200).grid(row = 1, column = 1, pady = 10, padx = 10)
RB_sin = Tk.Radiobutton(wave, text = 'SINE', value = 0, variable = wave_v, command = fun_wave, font = ('', 12)).place(x = 70, y = 90)
RB_sawtooth = Tk.Radiobutton(wave, text = 'SAWTOOTH', value = 1, variable = wave_v, command = fun_wave, font = ('', 12)).place(x = 70, y = 130)
RB_square = Tk.Radiobutton(wave, text = 'SQUARE', value = 2, variable = wave_v, command = fun_wave, font = ('', 12)).place(x = 70, y = 170)
RB_triangle = Tk.Radiobutton(wave, text = 'TRIANGLE', value = 3, variable = wave_v, command = fun_wave, font = ('', 12)).place(x = 70, y = 210)

# Select filter type
filter_v = Tk.IntVar()
filter = Tk.LabelFrame(root, text = ' Filter type ', width = 250, height=200).grid(row = 1, column = 2, pady = 10, padx = 10)
RB_no_fil = Tk.Radiobutton(filter, text = 'No filter', value = 0, variable = filter_v, command = fun_fil, font = ('', 14)).place(x = 350, y = 100)
RB_lp_fil = Tk.Radiobutton(filter, text = 'Low pass filter', value = 1, variable = filter_v, command = fun_fil, font = ('', 14)).place(x = 350, y = 140)
RB_hp_fil = Tk.Radiobutton(filter, text = 'High pass filter', value = 2, variable = filter_v, command = fun_fil, font = ('', 14)).place(x = 350, y = 180)

# Select cut-off frequency
freq_v = Tk.DoubleVar()
freq = Tk.LabelFrame(root, text = ' Cut-off frequency ', width = 250, height=200).grid(row = 1, column = 3, pady = 10, padx = 10)
L_ratio = Tk.Label(freq, text = 'Ratio', font = ('', 14)).place(x = 600, y = 115)
L_freq = Tk.Label(freq, text = 'Cut-off frequency: ' + str(freq_v.get()), font = ('', 14))
L_freq.place(x = 600, y = 180)
S_ratio = Tk.Scale(freq, variable = freq_v, from_ = 0.7, to = 10, resolution = 0.1, orient = Tk.HORIZONTAL, command = fun_freq).place(x = 650, y = 100)

# Select parameters of ADSR
A = Tk.DoubleVar()
A.set(0.05)
D = Tk.DoubleVar()
D.set(0.2)
S = Tk.DoubleVar()
S.set(0.6)
R = Tk.DoubleVar()
R.set(0.3)

adsr = Tk.LabelFrame(root, text = 'Select parameters of ADSR ', width=800, height=200, container = True).grid(row = 2, column = 1,columnspan=3, pady = 10, padx = 10)

L_A = Tk.Label(adsr, text = 'Attack time').place(x = 100, y = 310)
S_A = Tk.Scale(adsr, variable = A, from_ = 0.001, to = 0.1, resolution = 0.001, command = getvalue_fun).place(x = 100, y = 340)
L_D = Tk.Label(adsr, text = 'Decay time').place(x = 250, y = 310)
S_D = Tk.Scale(adsr, variable = D, from_ = 0.001, to = 1.0, resolution = 0.001, command = getvalue_fun).place(x = 250, y = 340)
L_S = Tk.Label(adsr, text = 'Sustain_level').place(x = 400, y = 310)
S_S = Tk.Scale(adsr, variable = S, from_ = 0.0, to = 0.999, resolution = 0.001, command = getvalue_fun).place(x = 400, y = 340)
L_R = Tk.Label(adsr, text = 'Release_time').place(x = 550, y = 310)
S_R = Tk.Scale(adsr, variable = R, from_ = 0.001, to = 1.0, resolution = 0.001, command = getvalue_fun).place(x = 550, y = 340)



# Piano keyboard
# TODO: 1. radiobutton  2. 每次release修改变量为-1     3. bind key & button    4.
# Image
img = Image.open('piano.jpg')
pic = ImageTk.PhotoImage(img.resize((750, 200)))
L_pic = Tk.Label(root, image = pic).grid(row = 3, column = 1, columnspan=3, pady = 10, padx = 10)
# Radiobutton
notes = Tk.IntVar()
notes.set(-1)
# R_A = Tk.Radiobutton(root, )
for i in range(12):
    # TODO: define command
    Tk.Radiobutton(root, value = i, variable = notes).place(x = 145 + i * 39.5, y = 490)



# Quit
B_esc = Tk.Button(root, text = 'QUIT', command = quit_fun).grid(row = 5, column = 1,rowspan=1, columnspan=5, padx = 10, pady = 10)







# ADSR parameters
G = 0
decay_phase = False
attack_s = 0.0
decay_s = 0.0
sustain_level = 0.5
release_s = 0.0

# waveform parameter
theta = 0.0
sawtooth_data = 0.0
triangle_data = 0.0
idx = 0
positive_side = True
increase_slope = True
wave_type = 'sine'

# filter parameters
set_filter = False
filter_type = 'lowpass'
cutoff_freq = 0.0
ORDER = 7
states = np.zeros(ORDER)


# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,  
    channels = 1, 
    rate = Fs,
    input = False, 
    output = True,
    frames_per_buffer = 128)            
    # specify low frames_per_buffer to reduce latency

MAXVALUE = 32767
MINVALUE = -32768
BLOCKLEN = 512
output_block = [0] * BLOCKLEN
CONTINUE = True
ISPRESS = 0

# plot dynamic waveform
t = [1000.*i/Fs for i in range(BLOCKLEN)]

pyplot.ion()           # Turn on interactive mode so plot gets updated

my_fig = pyplot.figure(1)
my_plot = my_fig.add_subplot(1, 1, 1)
[my_line] = my_plot.plot(t, output_block)
my_plot.set_ylim(-32000, 32000)
my_plot.set_xlim(0, BLOCKLEN*1000.0/Fs)   # Time axis in milliseconds 
my_plot.set_xlabel('Time (milliseconds)')

# root.mainloop()

while CONTINUE:
    root.update()

    for i in range(0, BLOCKLEN):

        G, decay_phase = adsr_main(ISPRESS, G, decay_phase, attack_s, decay_s, sustain_level, release_s)

        if wave_type == 'sine':
            output_block[i], theta = sinwave_gen(f1, Fs, theta, G)
        elif wave_type == 'sawtooth':
            output_block[i], sawtooth_data = sawtooth_gen(f1, Fs, sawtooth_data, G)
        elif wave_type == 'square':
            output_block[i], idx, positive_side = square_gen(f1, Fs, idx, positive_side, G)
        elif wave_type == 'triangle':
            output_block[i], triangle_data, increase_slope = triangle_gen(f1, Fs, triangle_data, increase_slope, G)

    # Apply a filter
    if set_filter:
        output_block_filtered, states = digital_filter(filter_type, cutoff_freq, output_block, Fs, ORDER, states)
        output_block_filtered = np.clip(output_block_filtered, MINVALUE, MAXVALUE)
        output_block_filtered = output_block_filtered.astype(int)
        my_line.set_ydata(output_block_filtered)
        binary_data = struct.pack('h' * BLOCKLEN, *output_block_filtered)
    else:
        my_line.set_ydata(output_block)
        binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    my_plot.set_title('Frequency = %.2f' % f1)
    stream.write(binary_data)

print('* Finished')

pyplot.ioff()
        