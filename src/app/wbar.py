import plotly.graph_objs as go
from flask import jsonify, request, session, render_template

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
        title='W Bar Value over Allele Frequency',
        xaxis=dict(range=[0, 100]),  # Adapt the range dynamically
        yaxis=dict(range=[0, 1]),
        yaxis_title='W Bar',
        xaxis_title='Allele Frequency as a Percentage',
        showlegend=False  # Turn off the legend if desired
    )
    
    return fig
@app.route('/w_plot', methods=['POST'])
def w_plot():
    w_bars = request.get_json().get('w_bars', [])
    # Get existing frequency lists from session, or initialize if not present
    w_bars_list = session.get('w_bars_list', [])
    # Append the new frequencies as a new trace
    w_bars_list.append(w_bars)
    # Update the session with the new list of frequency lists
    session['w_bars_list'] = w_bars_list
    # Create a new plot with the list of lists of frequencies
    fig = create_w_plot(w_bars_list)  # Pass the list of lists
    # Convert the figure to JSON format for Plotly.js
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
    for i in range(1, 101):
        next_freq = w_bar_calc(state['w11'], state['w12'], state['w22'], i/100)
        state['w_bars'].append(next_freq)
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