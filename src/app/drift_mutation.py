from flask import jsonify, request, render_template, session
from app import app
from app.drift_helper import create_plot, run_simulation
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
    # Initialize the session with population size, mutation rate, and frequencies
    session['mut_state'] = {
        'pop': int(data.get('pop')),
        'mu': float(data.get('mu')),
        'pop_freqs': [0.5] * 32  # Start with equal frequencies
    }
    print(f"Session after reset: {session['mut_state']}")  # Debug: Verify initial state
    return jsonify(session['mut_state'])

def do_generation(pop_freqs, mu, n):
    new_freqs = np.zeros_like(pop_freqs)
    
    for i in range(len(pop_freqs)):
        random_vals = np.random.rand(2 * n)
        occurrences = np.sum((random_vals < pop_freqs[i] * (1 - mu)) | (random_vals > 1 - mu + pop_freqs[i] * mu))
        new_freqs[i] = occurrences / (2 * n)
    
    return new_freqs

@app.route('/mut_next', methods=['POST'])
def mut_next():
    state = session.get('mut_state')
    
    if state is None:
        return jsonify({'error': 'Simulation not initialized. Please reset.'}), 400  # Ensure session is initialized

    pop_freqs = np.array(state['pop_freqs'])
    mu = state['mu']
    n = state['pop']
    
    # Debug: Print session before mutation
    print(f"State before mutation: {state}")
    
    # Perform a single iteration of mutation and genetic drift
    new_freqs = do_generation(pop_freqs, mu, n)
    
    # Update the session with new frequencies
    state['pop_freqs'] = new_freqs.tolist()
    session['mut_state'] = state
    
    # Debug: Print updated session state
    print(f"State after mutation: {session['mut_state']}")

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
    # Reset the session data to initial state
    session['mut_state'] = {
        'pop': 25,  # Default population size
        'mu': 0.0,  # Default mutation rate
        'pop_freqs': [0.5] * 32  # Default frequencies
    }
    print(f"Session after clear: {session['mut_state']}")  # Debug: Verify reset state
    fig = create_plot()  # Create an empty plot
    plot_data = fig.to_dict()
    return jsonify(plot_data)
