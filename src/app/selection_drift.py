from flask import jsonify, request, session
from random import random as rand

from app import app

def next_gen(p, w11, w12, w22, pop_size):
    q = 1 - p
    w_bar = p**2 * w11 + 2 * p * q * w12 + q**2 * w22
    selec = (p**2 * w11 + p * q * w12) / w_bar

    j = 0
    for i in range(2 * pop_size):
        if (rand() < selec):
            j += 1
    
    return j / (2 * pop_size)

@app.route('/sd_reset', methods=['POST'])
def sd_reset():
    data = request.get_json()
    session['selec_d_state'] = {
        'gen': 0,
        'gens': int(data.get('gens')),
        'p': float(data.get('p')),
        'w11': float(data.get('w11')),
        'w12': float(data.get('w12')),
        'w22': float(data.get('w22')),
        'pop': int(data.get('pop')),
        'freqs': [float(data.get('p'))]
    }
    return jsonify(session['selec_d_state']) # Send the data as JSON

@app.route('/sd_next', methods=['POST'])
def sd_next():
    state = session['selec_d_state']

    while state['gen'] < state['gens']:
        next_freq = next_gen(state['freqs'][-1], state['w11'], state['w12'], state['w22'], state['pop'])
        state['freqs'].append(next_freq)
        state['gen'] += 1

    # Update session with the modified state
    session['selec_d_state'] = state
    
    return jsonify(state)  # Send the updated state as JSON