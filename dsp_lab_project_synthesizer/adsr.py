def adsr_slope(attack_t, decay_t, sustain_level, release_t, RATE):
    attack_slope = 1.0 / (attack_t * RATE)
    decay_slope = (1.0 - sustain_level) / (decay_t * RATE)
    release_slope = sustain_level / (release_t * RATE)
    return attack_slope, decay_slope, release_slope

def adsr_main(ISPRESS, G, decay_phase, attack_s, decay_s, sustain_level, release_s):
    if ISPRESS == 1:
        if G >= 1:
            decay_phase = True
        if decay_phase:
            G = (G - decay_s) if (G > sustain_level + decay_s) else sustain_level
        else:
            G = 1 if (attack_s > 1) else (G + attack_s)

    elif ISPRESS == 0:
        if G <= sustain_level:
            G = (G - release_s) if (G >= release_s) else 0
            if G == 0:
                decay_phase = False
        else:
            G = G - decay_s

    return G, decay_phase