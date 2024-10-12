from flask import jsonify, request, session
from random import random as rand

from app import app

def next_gen(freq, pop):
    ct = 0
    for i in range(2 * pop):
        if rand() < freq:
            ct += 1
    return ct / (2 * pop)


@app.route('/d_reset', methods=['POST'])
def d_reset():
    data = request.get_json()
    session['drift_state'] = {
        'gen': 0,
        'gens': int(data.get('gens')),
        'freqs': [float(data.get('init_freq'))],
        'pop': int(data.get('pop'))
    }

    return jsonify(session['drift_state'])


@app.route('/d_next', methods=['POST'])
def d_next():
    state = session['drift_state']

    while state['gen'] < state['gens']:
        next_freq = next_gen(state['freqs'][-1], state['pop'])
        state['freqs'].append(next_freq)
        state['gen'] += 1

    session['drift_state'] = state

    return jsonify(state)