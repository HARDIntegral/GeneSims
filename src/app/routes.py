import plotly.graph_objs as go
from flask import jsonify, render_template, make_response, request, session

from app import app
from app.selection import next_gen

@app.route('/favicon.ico')
def favicon():
    return make_response("", 204)

def create_plot(freqs=None):
    fig = go.Figure()

    if freqs:
        x_vals = list(range(len(freqs)))  # x-axis is generation numbers
        fig.add_trace(go.Scatter(x=x_vals, y=freqs, mode='lines', name='Allele Frequency'))

    fig.update_layout(
        title='Allele Frequency over Evolutionary Time',
        xaxis=dict(range=[0, len(freqs) if freqs else 100]),
        yaxis=dict(range=[0, 1]),
        yaxis_title='Allele Frequency',
        xaxis_title='Generations'
    )
    
    return fig

plot_html = create_plot()

@app.route('/')
def selection():
    global plot_html
    return render_template('selection.html', title='Selection', plot=plot_html)

@app.route('/plot')
def plot():
    state = session.get('selec_state', None)  # Get the current session state
    freqs = state.get('freqs', []) if state else None  # Extract frequencies if available
    fig = create_plot(freqs)  # Pass frequencies or None for an empty plot

    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    return jsonify(plot_data)

@app.route('/reset', methods=['POST'])
def reset():
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

@app.route('/next', methods=['POST'])
def next():
    state = session['selec_state']

    # Check if the generation limit is reached
    if state['gen'] >= state['gens']:
        return jsonify(state)
    
    # Calculate the next frequency and update the state
    next_freq = next_gen(state['freqs'][-1], state['w11'], state['w12'], state['w22'])
    state['freqs'].append(next_freq)  # Append to the freqs list directly
    state['gen'] += 1  # Increment the generation
    
    # Update session with the modified state
    session['selec_state'] = state
    
    return jsonify(state)  # Send the updated state as JSON
        