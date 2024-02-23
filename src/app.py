from flask import Flask, render_template
from blueprint import bp
import base64
from io import BytesIO
from flask import Flask
from matplotlib.figure import Figure
from get_tickers.portfolioMCSimulation import main


app = Flask(__name__)
#app.register_blueprint(bp, url_prefix="/")

@app.route("/")
def home():
    # Generate the figure **without using pyplot**.
    simulatedPortfolio = main(['GME', 'SU'])
    meanReturns = simulatedPortfolio.simulatedReturns.tolist()
    fig = Figure()
    ax = fig.subplots()
    ax.plot(meanReturns)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"