from numba import jit

def adsr_slope(attack_t, decay_t, sustain_level, release_t, RATE):
    attack_slope = 1.0 / (attack_t * RATE)
    decay_slope = (1.0 - sustain_level) / (decay_t * RATE)
    release_slope = sustain_level / (release_t * RATE)
    return attack_slope, decay_slope, release_slope

@jit(nopython=True)
def adsr_main(ISPRESS, G, decay_phase, attack_s, decay_s, sustain_level, release_s):

    for i in range(0, 12):
        if ISPRESS[i] == 1:
            if G[i] >= 1:
                decay_phase[i] = 1
            if decay_phase[i] == 1:
                G[i] = (G[i] - decay_s) if (G[i] > sustain_level + decay_s) else sustain_level
            else:
                G[i] = 1 if (attack_s > 1) else (G[i] + attack_s)

        elif ISPRESS[i] == 0:
            if G[i] <= sustain_level:
                G[i] = (G[i] - release_s) if (G[i] >= release_s) else 0
                if G[i] == 0:
                    decay_phase[i] = 0
            else:
                G[i] = G[i] - decay_s

    return G, decay_phase