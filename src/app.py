from flask import Flask, render_template, request
import base64
from io import BytesIO
from flask import Flask
from matplotlib.figure import Figure
from get_tickers.portfolioMCSimulation import main

"""
Leverage w/ flask fun app.py in the src dir
"""


app = Flask(__name__)
#app.register_blueprint(bp, url_prefix="/")
@app.route("/")
def home():
    return("THIS IS THE HOME PAGE")

@app.route("/MC_Simulation")
def MC_simulation():
    simulatedPortfolio = main(['GME', 'SU'])
    meanReturns = simulatedPortfolio.simulatedReturns.tolist()
    fig = Figure()
    ax = fig.subplots()
    ax.plot(meanReturns)

    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@app.route("/input_stocks")
def get_stock_input():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    num_inputs = int(request.form['num_inputs'])
    inputs = [request.form[f'input_{i}'] for i in range(1, num_inputs+1)]
    # Process the inputs here
    print(inputs)
    return "Inputs received successfully!"