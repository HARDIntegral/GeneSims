import plotly.graph_objs as go
from flask import jsonify, request, render_template, make_response, session

from app import app
from app.selection import s_reset, s_next
from app.selection_drift import sd_reset, sd_next

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
def index():
    return render_template('index.html', title='Home', plot=plot_html)

@app.route('/selection')
def selection():
    global plot_html
    return render_template('selection.html', title='Selection', plot=plot_html)

@app.route('/selection_drift')
def selection_drift():
    global plot_html
    return render_template('selection_drift.html', title='Selection with Drift', plot=plot_html)

@app.route('/plot', methods=['POST'])
def plot():
    freqs = request.get_json().get('freqs', [])
    fig = create_plot(freqs)  # Pass frequencies or None for an empty plot

    # Convert the figure to JSON format for Plotly.js
    plot_data = fig.to_dict()
    return jsonify(plot_data)