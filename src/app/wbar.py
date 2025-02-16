import plotly.graph_objs as go
from flask import jsonify, request, session, render_template
import numpy as np

from app import app

def w_bar_calc(w11, w12, w22, p):
    q = 1 - p
    return p**2 * w11 + 2 * p * q * w12 + q**2 * w22

def create_w_plot(w_bars_list=None):
    fig = go.Figure()
    
    if w_bars_list:
        for w_bars in w_bars_list:
            x_vals = list(range(0,101))  # x-axis is generation numbers
            fig.add_trace(go.Scatter(x=x_vals, y=w_bars, mode='lines'))

    fig.update_layout(
        title={
            'text': 'W Bar Value over Allele Frequency',
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            range=[0, 100],
            showline=True,      # Show the y-axis line
            showgrid=False,     # Hide the grid lines
            linecolor='black'   # Set the color of the y-axis line (optional)
        ),  # Adapt the range dynamically
        yaxis=dict(
            range=[0, 1],
            showline=True,      # Show the y-axis line
            showgrid=False,     # Hide the grid lines
            linecolor='black'   # Set the color of the y-axis line (optional)
        ),
        yaxis_title='W Bar',
        xaxis_title='Allele Frequency as a Percentage',
        showlegend=False  # Turn off the legend if desired
    )
    
    return fig

@app.route('/w_plot', methods=['POST'])
def w_plot():
    w_bars = request.get_json().get('w_bars', [])
    w_bars_list = session.get('w_bars_list', [])
    w_bars_list.append(w_bars)
    session['w_bars_list'] = w_bars_list
    fig = create_w_plot(w_bars_list)
    plot_data = fig.to_dict()
    return jsonify(plot_data)

@app.route('/w_reset', methods=['POST'])
def w_reset():
    data = request.get_json()
    session['w_bar_state'] = {
        'w11': float(data.get('w11')),
        'w12': float(data.get('w12')),
        'w22': float(data.get('w22')),
        'w_bars': []
    }
    return jsonify(session['w_bar_state'])  # Send the data as JSON

@app.route('/w_next', methods=['POST'])
def w_next():
    state = session['w_bar_state']
    
    proportions = np.linspace(0.01, 1.0, 100)
    new_freqs = w_bar_calc(state['w11'], state['w12'], state['w22'], proportions)
    state['w_bars'].extend(new_freqs.tolist())
    session['w_bar_state'] = state
    
    return jsonify(state)  # Send the updated state as JSON


@app.route('/w_clear', methods=['POST'])
def clear_w_plot():
    session['w_bars_list'] = []  # Reset frequency data to an empty list
    # Create an empty plot
    fig = create_w_plot()  # Use your existing function to create an empty plot
    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    return jsonify(plot_data)

w_plot_html = create_w_plot()

@app.route('/w_bar')
def w_bar():
    clear_w_plot()
    global w_plot_html
    return render_template('w_bar.html', title='W Bar', plot=w_plot_html)