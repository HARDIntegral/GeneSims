import plotly.graph_objs as go
from flask import jsonify, request, render_template, session
from random import random as rand

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
    num_pops = len(state.get('pop_freqs'))
    temp_freqs = [0.0] * num_pops
    mig = state.get('mig')

    for n in range(num_pops):
        temp_freqs[n] = state.get('pop_freqs')[n] * (1 - mig)
        for j in range(n):
            temp_freqs[j] += mig * state.get('pop_freqs')[j] / (num_pops - 1)
        for j in range(n + 1, num_pops):
            temp_freqs[j] += mig * state.get('pop_freqs')[j] / (num_pops - 1)
    
    state['pop_freqs'] = temp_freqs

def calc_freq(freq):
    mig = session.get('mig_state').get('mig')
    n = session.get('mig_state').get('pop')
    num_freq_occ = 0

    for _ in range(0, 2*n):
        random = rand()
        if random < freq:
            num_freq_occ += 1

    return num_freq_occ/(2 * n)

@app.route('/mig_next', methods=['POST'])
def mig_next():
    state = session.get('mig_state')
    report_interval = 10
    num_pops = len(state.get('pop_freqs'))

    for i in range(0, report_interval):
        if i < report_interval:
            migrate()  # Call the migration function
            for j in range(0, num_pops):
                state.get('pop_freqs')[j] = calc_freq(state.get('pop_freqs')[j]) 
    
    session['mig_state'] = state
    return jsonify(state)  # Send the updated state data back to the client

@app.route('/mig_plot', methods=['POST'])
def mig_plot():
    # Check if the request contains allele frequency data
    allele_frequencies = request.json.get('allele_frequencies', [])
    # Update the session with new frequency data
    session['freqs_list'] = allele_frequencies  # Update session data
    # Create a new plot with the updated data
    fig = create_mig_plot(allele_frequencies)  # Call the function to create the updated plot
    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    
    return jsonify(plot_data)  # Send the updated plot data back to the client

@app.route('/mig_clear', methods=['POST'])
def clear_mig_plot():
    session['freqs_list'] = []  # Reset frequency data to an empty list
    # Create an empty plot
    fig = create_mig_plot()  # Use your existing function to create an empty plot
    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    return jsonify(plot_data)
