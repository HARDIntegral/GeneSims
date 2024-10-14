from flask import jsonify, request, session
import numpy as np

from app import app

def next_gen(p, w11, w12, w22):
    q = 1 - p
    w_bar = p**2 * w11 + 2 * p * q * w12 + q**2 * w22
    return (p**2 * w11 + p * q * w12) / w_bar

@app.route('/s_reset', methods=['POST'])
def s_reset():
    data = request.get_json()
    session['selec_state'] = {
        'gen': 0,
        'gens': int(data.get('gens')),
        'p': float(data.get('p')),
        'w11': float(data.get('w11')),
        'w12': float(data.get('w12')),
        'w22': float(data.get('w22')),
        'freqs': [float(data.get('p'))]
    }
    return jsonify(session['selec_state']) # Send the data as JSON

@app.route('/s_next', methods=['POST'])
def s_next():
    state = session['selec_state']
    current_gen = state['gen']
    total_gens = state['gens']
    freqs = np.array(state['freqs'])
    remaining_gens = total_gens - current_gen

    new_freqs = np.empty(remaining_gens)
    current_freq = freqs[-1]
    for gen in range(remaining_gens):
        next_freq = next_gen(current_freq, state['w11'], state['w12'], state['w22'])
        new_freqs[gen] = next_freq
        current_freq = next_freq

    # Convert the NumPy array of new frequencies back to a list and extend the state
    state['freqs'].extend(new_freqs.tolist())
    state['gen'] = total_gens

    # Update the session with the modified state
    session['selec_state'] = state
    
    return jsonify(state)  # Send the updated state as JSON