import plotly.graph_objs as go
from flask import jsonify, request, render_template, session
import numpy as np

from app import app

def create_mut_plot(freqs_list=None):
    # Create the histogram
    fig = go.Figure(data=[
        go.Histogram(
            x=freqs_list,  
            xbins=dict(
                start=0,  
                end=1.1,  
                size=0.1   
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
        ),  
        yaxis=dict(
            title='Count',
            autorange=True, 
            range=[0, 10] 
        ),
        bargap=0.2 
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
    
    random_values = np.random.rand(2 * n)
    freq_occurrences = (
        (random_values < freq * (1.0 - mu)) | 
        (random_values > 1.0 - mu + freq * mu)
    )

    return np.sum(freq_occurrences) / (2 * n)


@app.route('/mut_next', methods=['POST'])
def mut_next():
    state = session.get('mut_state')
    report_interval = 10
    pop_freqs = np.array(state.get('pop_freqs'))  # Convert to a NumPy array

    for _ in range(report_interval):
        pop_freqs = np.array([calc_freq(freq) for freq in pop_freqs])
    state['pop_freqs'] = pop_freqs.tolist()  

    session['mut_state'] = state
    return jsonify(state)  # Send the updated state data back to the client



@app.route('/mut_plot', methods=['POST'])
def mut_plot():
    allele_frequencies = request.json.get('allele_frequencies', [])
    session['freqs_list'] = allele_frequencies 
    fig = create_mut_plot(allele_frequencies) 
    plot_data = fig.to_dict()
    
    return jsonify(plot_data)  # Send the updated plot data back to the client

@app.route('/mut_clear', methods=['POST'])
def clear_mut_plot():
    session['freqs_list'] = [] 
    fig = create_mut_plot()
    plot_data = fig.to_dict()
    return jsonify(plot_data)
