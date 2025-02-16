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
    # Check if state is already initialized to avoid resetting it every time
    if 'mig_state' not in session:
        data = request.get_json()
        session['mig_state'] = {
            'pop': int(data.get('pop')),
            'mig': float(data.get('mig')),
            'pop_freqs': [0.5] * 32  # Reset frequencies to 0.5 for each population
        }
        print(f"Session state after reset: {session['mig_state']}")  # Debugging line
    else:
        print("Session already initialized, skipping reset.")  # Debugging line
    
    return jsonify(session['mig_state'])

def migrate():
    state = session['mig_state']
    pop_freqs = np.array(state.get('pop_freqs'))  # Current population frequencies
    num_pops = len(pop_freqs)
    mig = state.get('mig')

    # Create a new array for updated frequencies
    new_freqs = np.zeros(num_pops)

    # Loop over each population to apply migration
    for n in range(num_pops):
        new_freqs[n] = (1 - mig) * pop_freqs[n]  # Self contribution
        for j in range(num_pops):
            if j != n:
                new_freqs[n] += mig * pop_freqs[j] / (num_pops - 1)  # Contribution from others

    state['pop_freqs'] = new_freqs.tolist()  # Update state with new frequencies

def calc_freq(freq, state):
    n = state.get('pop')
    random_values = np.random.rand(2 * n)  # Random values to simulate genetic drift
    num_freq_occ = np.sum(random_values < freq)  # Count how many times the allele occurs
    return num_freq_occ / (2 * n)

@app.route('/mig_next', methods=['POST'])
def mig_next():
    state = session.get('mig_state')
    run_simulation(10, migrate, calc_freq, state)  # Run the simulation for 10 iterations
    session['mig_state'] = state  # Update the session state
    return jsonify(state)

@app.route('/mig_plot', methods=['POST'])
def mig_plot():
    allele_frequencies = request.json.get('allele_frequencies', [])
    session['freqs_list'] = allele_frequencies  # Store allele frequencies in the session
    fig = create_plot(allele_frequencies)  # Create a new plot based on the frequencies
    plot_data = fig.to_dict()  # Convert plot to dictionary format
    return jsonify(plot_data)

@app.route('/mig_clear', methods=['POST'])
def clear_mig_plot():
    session['freqs_list'] = []  # Clear allele frequencies
    fig = create_plot()  # Create an empty plot
    plot_data = fig.to_dict()  # Convert to dictionary format for the response
    return jsonify(plot_data)
