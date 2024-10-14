from flask import jsonify, request, session
import numpy as np

from app import app

def next_gen(p, w11, w12, w22, pop_size):
    q = 1 - p
    w_bar = p**2 * w11 + 2 * p * q * w12 + q**2 * w22
    selec = (p**2 * w11 + p * q * w12) / w_bar

    random_values = np.random.rand(2 * pop_size)
    j = np.sum(random_values < selec)
    
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
    current_freq = np.array(state['freqs'][-1])
    
    while state['gen'] < state['gens']:
        next_freq = next_gen(current_freq, state['w11'], state['w12'], state['w22'], state['pop'])
        state['freqs'].append(next_freq)
        current_freq = next_freq
        state['gen'] += 1

    session['selec_d_state'] = state
    
    return jsonify(state)  # Send the updated state as JSON
