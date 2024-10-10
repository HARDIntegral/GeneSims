from flask import jsonify, request, session

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

    while state['gen'] < state['gens']:
        next_freq = next_gen(state['freqs'][-1], state['w11'], state['w12'], state['w22'])
        state['freqs'].append(next_freq)
        state['gen'] += 1

    # Update session with the modified state
    session['selec_state'] = state
    
    return jsonify(state)  # Send the updated state as JSON