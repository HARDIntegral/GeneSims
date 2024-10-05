from flask import jsonify, request
from flask_socketio import SocketIO
import numpy as np
from src import app

socket = SocketIO(app)

def next_gen(p, w11, w12, w22):
    q = 1 - p
    w_bar = p**2 * w11 + 2 * p * q * w12 + q**2 * w22
    return (p**2 * w11 + p * q * w12) / w_bar

def parse_state(state_data):
    gen = int(state_data.get('gen', 0))
    gens = int(state_data.get('gens', 100))
    p = float(state_data.get('p', 0.1))
    w11 = float(state_data.get('w11', 1.2))
    w12 = float(state_data.get('w12', 1.0))
    w22 = float(state_data.get('w22', 0.8))
    freqs = list(state_data.get('freqs', []))

    return {
        'gen': gen,
        'gens': gens,
        'p': p,
        'w11': w11,
        'w12': w12,
        'w22': w22,
        'freqs': freqs
    }

@socket.on('reset', namespace='/selection')
def reset(data):
    socket.emit('state updated', parse_state(data), namespace='/selection');

@socket.on('next', namespace='/selection')
def next(): 
    global state

    if state['gen'] >= state['gens']:
        return jsonify(state)
    
    p = state['p']
    w11 = state['w11']
    w12 = state['w12']
    w22 = state['w22']

    next_freq = next_gen(p, w11, w12, w22)
    state['freqs'].append(next_freq)
    state['gen'] += 1

    socket.emit('state updated', {'state': state}, namespace='/selection');