import tkinter as Tk

def adsr_envolope(attack_t, decay_t, sustain_level, release_t, RATE = 44100):
    attack_slope = 1.0 / (attack_t * RATE)
    decay_slope = (1.0 - sustain_level) / (decay_t * RATE)
    release_slope = sustain_level / (release_t * RATE)
    return attack_slope, decay_slope, release_slope


def key_function(event):
    global CONTINUE
    global KEYPRESS

    print('your press:' + event.char)
    if event.char == 'a':
        KEYPRESS = True
    else:
        KEYPRESS = False


CONTINUE = True
KEYPRESS = False

root = Tk.Tk()
root.bind("<Key>", key_function)

volume = 1.0
RATE = 44100
attack_t = 0.2
decay_t = 0.2
sustain_level = 0.5
release_t = 0.3
n = 0

attack_s, decay_s, release_s = adsr_envolope(attack_t, decay_t, sustain_level, release_t)

while CONTINUE:
    root.update()

    if KEYPRESS and CONTINUE:
        if n <= (attack_t * RATE):
            volume = volume * (attack_s * n)
            n = n + 1
        elif n <= ((attack_t + decay_t) * RATE):
            volume = volume * (1.0 - decay_s * (n - attack_t * RATE))
            n = n + 1
        else:
            volume = volume
            n = n + 1
    elif KEYPRESS == False:
        i = 0
        volume = volume * (1.0 - release_s * i)
        n = n + i
        i = i + 1