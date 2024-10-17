# genetics_helpers.py
import numpy as np
import plotly.graph_objs as go

def create_plot(freqs_list=None, title='Allele Frequency Distribution'):
    """Creates a histogram plot for the allele frequency distribution."""
    fig = go.Figure(data=[
        go.Histogram(
            x=freqs_list,
            xbins=dict(start=0, end=1.1, size=0.1),
            marker_color='blue',
            opacity=0.75
        )
    ])
    
    # Update layout
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Allele Frequency',
        yaxis_title='Number of Populations',
        xaxis=dict(dtick=0.1, range=[0, 1.1]),
        yaxis=dict(title='Count', autorange=True, range=[0, 10]),
        bargap=0.2
    )
    
    return fig

def calculate_frequencies(pop_freqs, calc_func, state):
    """Calculates frequencies based on a given calculation function."""
    return [calc_func(freq, state) for freq in pop_freqs]

def run_simulation(report_interval, migrate_func, calc_freq, state):
    for _ in range(report_interval):
        if migrate_func:
            migrate_func()  # Call migrate if not None
        
        pop_freqs = np.array(state.get('pop_freqs'))
        # Pass both freq and state to calc_freq
        pop_freqs = np.array([calc_freq(freq, state) for freq in pop_freqs])
        state['pop_freqs'] = pop_freqs.tolist()


