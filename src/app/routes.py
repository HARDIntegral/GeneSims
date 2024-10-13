import plotly.graph_objs as go
from flask import jsonify, request, render_template, make_response, session

from app import app

# Makes these routes visible
from app.wbar import w_bar, w_reset, w_next, clear_w_plot
from app.selection import s_reset, s_next
from app.drfit import d_reset, d_next
from app.selection_drift import sd_reset, sd_next

@app.route('/favicon.ico')
def favicon():
    return make_response("", 204)

def create_plot(freqs_list=None):
    fig = go.Figure()
    
    if freqs_list:
        for i, freqs in enumerate(freqs_list):
            x_vals = list(range(len(freqs)))  # x-axis is generation numbers
            fig.add_trace(go.Scatter(x=x_vals, y=freqs, mode='lines', name=f'Allele Frequency {i + 1}'))

    fig.update_layout(
        title='Allele Frequency over Evolutionary Time',
        xaxis=dict(range=[0, max(len(freq) for freq in freqs_list) if freqs_list else 100]),  # Adapt the range dynamically
        yaxis=dict(range=[0, 1]),
        yaxis_title='Allele Frequency',
        xaxis_title='Generations',
        showlegend=False  # Turn off the legend if desired
    )
    
    return fig

plot_html = create_plot()

@app.route('/')
def index():
    return render_template('index.html', title='Home', plot=plot_html)

@app.route('/selection')
def selection():
    clear_graph()
    global plot_html
    return render_template('selection.html', title='Selection', plot=plot_html)

@app.route('/selection_drift')
def selection_drift():
    clear_graph()
    global plot_html
    return render_template('selection_drift.html', title='Selection with Drift', plot=plot_html)

@app.route('/drift')
def drift():
    clear_graph()
    global plot_html
    return render_template('drift.html', title='Basic Drift', plot=plot_html)

@app.route('/plot', methods=['POST'])
def plot():
    freqs = request.get_json().get('freqs', [])
    # Get existing frequency lists from session, or initialize if not present
    freqs_list = session.get('freqs_list', [])
    # Append the new frequencies as a new trace
    freqs_list.append(freqs)
    # Update the session with the new list of frequency lists
    session['freqs_list'] = freqs_list
    # Create a new plot with the list of lists of frequencies
    fig = create_plot(freqs_list)  # Pass the list of lists
    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    return jsonify(plot_data)

@app.route('/clear', methods=['POST'])
def clear_graph():
    session['freqs_list'] = []  # Reset frequency data to an empty list
    # Create an empty plot
    fig = create_plot()  # Use your existing function to create an empty plot
    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    return jsonify(plot_data)