from flask import render_template
from src import app

@app.route('/selection')
def selection():
    return render_template('selection.html', title='Selection')

@app.route('/drift')
def drift():
    return render_template('drift.html')

@app.route('/selection_drift')
def selection_drift():
    return render_template('selection_drift.html')

@app.route('/drift_mutation')
def drift_mutation():
    return render_template('drift_mutation.html')

@app.route('/drift_migration')
def drift_migration():
    return render_template('drift_migration.html')

@app.route('/w_bar')
def w_bar():
    return render_template('w_bar.html')