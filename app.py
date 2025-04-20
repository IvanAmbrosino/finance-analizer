from flask import Flask, render_template_string
import yfinance as yf
import plotly.express as px
from dash import Dash, html
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    # Obtener datos de la acción
    ticker = yf.Ticker("MSFT")
    hist = ticker.history(period='1y', interval='1d')
    hist.index = pd.to_datetime(hist.index)
    df = hist.reset_index()

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

    # Crear gráfico interactivo con Plotly
    fig = px.line(df, x='Date', y='Close', title='MSFT - Precio de Cierre (último mes)')
    graph_html = fig.to_html(full_html=False)

    # Renderizar HTML con Jinja2 correctamente
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gráfico de MSFT</title>
    </head>
    <body>
        <h1>Fluctuación del precio de MSFT</h1>
        {{ graph_html | safe }}
    </body>
    </html>
    """
    return render_template_string(html_template, graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)

