import plotly.graph_objs as go
from flask import jsonify, request, render_template, session
from random import random as rand

from app import app

def create_mut_plot(freqs_list=None):
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
mut_plot_html = go.Figure().to_html()

@app.route('/drift_mutation')
def dm():
    # Call create_mut_plot within the request context
    global mut_plot_html
    fig = create_mut_plot()
    mut_plot_html = fig.to_html()
    return render_template('drift_mutation.html', title='Drift with Mutation', plot=mut_plot_html)

@app.route('/mut_reset', methods=['POST'])
def mut_reset():
    data = request.get_json()
    session['mut_state'] = {
        'pop': int(data.get('pop')),
        'mu' : float(data.get('mu')),
        'pop_freqs': [0.5] * 32
    }
    return jsonify(session['mut_state'])  # Send the updated state data back to the client

def calc_freq(freq):
    mu = session.get('mut_state').get('mu')
    n = session.get('mut_state').get('pop')
    num_freq_occ = 0

    for _ in range(0, 2*n):
        random = rand()
        if random < freq * (1.0 - mu) or random > 1.0 - mu + freq * mu:
            num_freq_occ += 1

    return num_freq_occ/(2 * n)

@app.route('/mut_next', methods=['POST'])
def mut_next():
    state = session.get('mut_state')
    report_interval = 10
    num_pops = len(state.get('pop_freqs'))

    for i in range(0, report_interval):
        if i < report_interval:
            for j in range(0, num_pops):
                state.get('pop_freqs')[j] = calc_freq(state.get('pop_freqs')[j]) 
    
    session['mut_state'] = state
    return jsonify(state)  # Send the updated state data back to the client

@app.route('/mut_plot', methods=['POST'])
def mut_plot():
    # Check if the request contains allele frequency data
    allele_frequencies = request.json.get('allele_frequencies', [])
    # Update the session with new frequency data
    session['freqs_list'] = allele_frequencies  # Update session data
    # Create a new plot with the updated data
    fig = create_mut_plot(allele_frequencies)  # Call the function to create the updated plot
    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    
    return jsonify(plot_data)  # Send the updated plot data back to the client

@app.route('/mut_clear', methods=['POST'])
def clear_mut_plot():
    session['freqs_list'] = []  # Reset frequency data to an empty list
    # Create an empty plot
    fig = create_mut_plot()  # Use your existing function to create an empty plot
    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    return jsonify(plot_data)
