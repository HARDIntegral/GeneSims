# mutation.py
from flask import jsonify, request, render_template, session
from app import app
from app.drift_helper  import create_plot, run_simulation
import numpy as np

@app.route('/drift_mutation')
def dm():
    global mut_plot_html
    fig = create_plot()
    mut_plot_html = fig.to_html()
    return render_template('drift_mutation.html', title='Drift with Mutation', plot=mut_plot_html)

@app.route('/mut_reset', methods=['POST'])
def mut_reset():
    data = request.get_json()
    session['mut_state'] = {
        'pop': int(data.get('pop')),
        'mu': float(data.get('mu')),
        'pop_freqs': [0.5] * 32
    }
    return jsonify(session['mut_state'])

def calc_freq(freq, state):
    mu = state.get('mu')
    n = state.get('pop')
    random_values = np.random.rand(2 * n)
    freq_occurrences = (random_values < freq * (1.0 - mu)) | (random_values > 1.0 - mu + freq * mu)
    return np.sum(freq_occurrences) / (2 * n)

@app.route('/mut_next', methods=['POST'])
def mut_next():
    state = session.get('mut_state')
    run_simulation(10, None, calc_freq, state)  # No migration for mutation
    session['mut_state'] = state
    return jsonify(state)

@app.route('/mut_plot', methods=['POST'])
def mut_plot():
    allele_frequencies = request.json.get('allele_frequencies', [])
    session['freqs_list'] = allele_frequencies
    fig = create_plot(allele_frequencies)
    plot_data = fig.to_dict()
    return jsonify(plot_data)

@app.route('/mut_clear', methods=['POST'])
def clear_mut_plot():
    session['freqs_list'] = []
    fig = create_plot()
    plot_data = fig.to_dict()
    return jsonify(plot_data)
