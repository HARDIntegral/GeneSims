# migration.py
from flask import jsonify, request, render_template, session
from app import app
from app.drift_helper import create_plot, run_simulation
import numpy as np

@app.route('/drift_migration')
def dmig():
    global mig_plot_html
    fig = create_plot()
    mig_plot_html = fig.to_html()
    return render_template('drift_migration.html', title='Drift with Migration', plot=mig_plot_html)

@app.route('/mig_reset', methods=['POST'])
def mig_reset():
    data = request.get_json()
    session['mig_state'] = {
        'pop': int(data.get('pop')),
        'mig': float(data.get('mig')),
        'pop_freqs': [0.5] * 32
    }
    return jsonify(session['mig_state'])

def migrate():
    state = session['mig_state']
    pop_freqs = np.array(state.get('pop_freqs'))
    num_pops = len(pop_freqs)
    mig = state.get('mig')
    temp_freqs = np.zeros(num_pops)

    for n in range(num_pops):
        temp_freqs[n] = pop_freqs[n] * (1 - mig)
        temp_freqs += mig * pop_freqs / (num_pops - 1)
    
    state['pop_freqs'] = temp_freqs.tolist()

def calc_freq(freq, state):
    n = state.get('pop')
    random_values = np.random.rand(2 * n)
    num_freq_occ = np.sum(random_values < freq)
    return num_freq_occ / (2 * n)

@app.route('/mig_next', methods=['POST'])
def mig_next():
    state = session.get('mig_state')
    run_simulation(10, migrate, calc_freq, state)
    session['mig_state'] = state
    return jsonify(state)

@app.route('/mig_plot', methods=['POST'])
def mig_plot():
    allele_frequencies = request.json.get('allele_frequencies', [])
    session['freqs_list'] = allele_frequencies
    fig = create_plot(allele_frequencies)
    plot_data = fig.to_dict()
    return jsonify(plot_data)

@app.route('/mig_clear', methods=['POST'])
def clear_mig_plot():
    session['freqs_list'] = []
    fig = create_plot()
    plot_data = fig.to_dict()
    return jsonify(plot_data)
