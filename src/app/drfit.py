from flask import jsonify, request, session
from random import random as rand
import numpy as np

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
    current_gen = state['gen']
    total_gens = state['gens']
    pop = state['pop']

    freqs = np.array(state['freqs'])
    remaining_gens = total_gens - current_gen
    random_values = np.random.rand(2 * pop, remaining_gens)
    new_freqs = np.empty(remaining_gens)
    current_freq = freqs[-1]

    for gen in range(remaining_gens):
        success_count = np.sum(random_values[:, gen] < current_freq)
        new_freqs[gen] = success_count / (2 * pop)
        current_freq = new_freqs[gen]

    state['freqs'].extend(new_freqs.tolist())
    state['gen'] = total_gens
    session['drift_state'] = state

    return jsonify(state)