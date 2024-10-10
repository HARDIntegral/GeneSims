from flask import jsonify

def next_gen(p, w11, w12, w22):
    q = 1 - p
    w_bar = p**2 * w11 + 2 * p * q * w12 + q**2 * w22
    return (p**2 * w11 + p * q * w12) / w_bar

def next(): 
    global state

    if state['gen'] >= state['gens']:
        return jsonify(state)
    
    p = state['p']
    w11 = state['w11']
    w12 = state['w12']
    w22 = state['w22']

    next_freq = next_gen(p, w11, w12, w22)
    state['freqs'].append(next_freq)
    state['gen'] += 1
