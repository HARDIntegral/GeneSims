import plotly.graph_objs as go
from flask import jsonify, request, render_template, session
from random import random as rand
import numpy as np

from app import app

def create_mig_plot(freqs_list=None):
    # Create the histogram
    fig = go.Figure(data=[
        go.Histogram(
            x=freqs_list,  # Use the provided data or initialize with a range
            xbins=dict(
                start=0,   # Start of the range
                end=1.1,     # End of the range
                size=0.1   # Width of each bin
            ),
            marker_color='blue',
            opacity=0.75
        )
    ])
    
    # Update layout
    fig.update_layout(
        title='Allele Frequency Distribution',
        xaxis_title='Allele Frequency',
        yaxis_title='Number of Populations',
        xaxis=dict(
            dtick=0.1, range=[0,1.1]
        ),  # Set x-axis ticks
        yaxis=dict(
            title='Count',
            autorange=True,  # Auto-adjust the y-axis based on data
            range=[0, 10]  # Set minimum y-axis value to 0),
        ),
        bargap=0.2  # Gap between bars
    )
    
    return fig

# Initialize mut_plot_html with an empty plot
mig_plot_html = go.Figure().to_html()

@app.route('/drift_migration')
def dmig():
    # Call create_mut_plot within the request context
    global mig_plot_html
    fig = create_mig_plot()
    mig_plot_html = fig.to_html()
    return render_template('drift_migration.html', title='Drift with Migration', plot=mig_plot_html)

@app.route('/mig_reset', methods=['POST'])
def mig_reset():
    data = request.get_json()
    session['mig_state'] = {
        'pop': int(data.get('pop')),
        'mig' : float(data.get('mig')),
        'pop_freqs': [0.5] * 32
    }
    return jsonify(session['mig_state'])  # Send the updated state data back to the client

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


def calc_freq(freq):
    n = session.get('mig_state').get('pop')
    random_values = np.random.rand(2 * n)
    num_freq_occ = np.sum(random_values < freq)
    return num_freq_occ / (2 * n)


@app.route('/mig_next', methods=['POST'])
def mig_next():
    state = session.get('mig_state')
    report_interval = 10

    for _ in range(report_interval):
        migrate()
        state['pop_freqs'] = [
            calc_freq(freq) for freq in state.get('pop_freqs')
        ]

    session['mig_state'] = state
    return jsonify(state)  # Send the updated state data back to the client


@app.route('/mig_plot', methods=['POST'])
def mig_plot():
    allele_frequencies = request.json.get('allele_frequencies', [])
    session['freqs_list'] = allele_frequencies 
    fig = create_mig_plot(allele_frequencies)
    plot_data = fig.to_dict()
    return jsonify(plot_data)

@app.route('/mig_clear', methods=['POST'])
def clear_mig_plot():
    session['freqs_list'] = [] 
    fig = create_mig_plot() 
    plot_data = fig.to_dict()
    return jsonify(plot_data)
