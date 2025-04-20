from dash import Dash, html, dash_table, dcc
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import datetime
from dash import Dash, html
from collections import defaultdict

app = Dash()

#https://docs.google.com/spreadsheets/d/1zCBy4cAL6hT-33Qz1jbJ_JNqvDrxJ6ca_TXij5cvfTA/edit?usp=sharing
# Conexion con el google sheet
# Reemplaza con el ID de tu hoja de cálculo
sheet_id = "1zCBy4cAL6hT-33Qz1jbJ_JNqvDrxJ6ca_TXij5cvfTA"
sheet_gid = "0"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_gid}"
df_csv = pd.read_csv(url)
data=df_csv.to_dict('records')

#agrupamos todas las compras por ticker
# Agrupar dinámicamente por TICKER
agrupadas = defaultdict(list)
for compra in data:
    ticker = compra["TICKER"]
    agrupadas[ticker].append(compra)

totales = {}
for grupo in agrupadas.values():
    total_invertido = sum(int(c['CANTIDAD']) * float(c['PRECIO_COMPRA']) for c in grupo)
    total_acciones = sum(int(c['CANTIDAD']) for c in grupo)
    precio_promedio = total_invertido / total_acciones
    min_fecha = min(c['FECHA_COMPRA'] for c in grupo)
    totales[grupo[0]['TICKER']] = {
        'TICKER': grupo[0]['TICKER'],
        'TOTAL_INVERTIDO': total_invertido,
        'TOTAL_ACCIONES': total_acciones,
        'PRECIO_PROMEDIO': precio_promedio,
        'MIN_FECHA': min_fecha
    }

graficos = []
for dato in totales.values():
# Obtener datos de la acción
    ticker = yf.Ticker(dato['TICKER'])
    #hist = ticker.history(period='1y', interval='1d')
    start_date = dato['MIN_FECHA']
    end_date = datetime.datetime.today().strftime('%Y-%m-%d')
    hist = ticker.history(start=start_date, end=end_date, interval='1d')
    hist.index = pd.to_datetime(hist.index)
    df = hist.reset_index()
    # Crear gráfico interactivo con Plotly
    fig = px.line(df, x='Date', y='Close', title=f'{dato["TICKER"]} - Precio de Cierre (último mes)')
    fig = go.Figure()

    # Precio promedio
    precio_promedio = dato['TOTAL_INVERTIDO'] / dato['TOTAL_ACCIONES']

    # Ganancia o pérdida
    ganancia_por_accion = df.iloc[-1]['Close'] - precio_promedio
    ganancia_total = ganancia_por_accion * dato['TOTAL_ACCIONES']
    porcentaje = (ganancia_total / precio_promedio) * 100

    calculos = {
        'Precio promedio': precio_promedio,
        'Total invertido': dato['TOTAL_INVERTIDO'],
        'Total acciones': dato['TOTAL_ACCIONES'],
        'Ganancia por acción': ganancia_por_accion,
        'Ganancia total': ganancia_total,
        'Porcentaje': porcentaje
    }
    calculos_vertical = [{"Campo": k, "Valor": v} for k, v in calculos.items()]

    # Definir colores según resultado
    color_texto = "green" if ganancia_total >= 0 else "red"
    color_linea = "green" if ganancia_total >= 0 else "red"
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        line=dict(color=color_linea),
        name='Precio Close'
    ))
    fig.update_layout(title="Evolución del precio para el ticker: " + dato['TICKER'])
    # Agregar trazas al gráfico
    # Dividir eventos en compras y ventas
    compras = [e for e in agrupadas[dato['TICKER']] if e["OPERACION"] == "compra"]
    ventas = [e for e in agrupadas[dato['TICKER']] if e["OPERACION"] == "venta"]
    fig.add_trace(go.Scatter(
        x=[e["FECHA_COMPRA"] for e in compras],
        y=[e["PRECIO_COMPRA"] for e in compras],
        mode='markers',
        marker=dict(color='green', size=10, symbol='triangle-up'),
        name='Compra'
    ))
    #fig.add_trace(go.Scatter(
    #    x=[e["FECHA_VENTA"] for e in ventas],
    #    y=[e["PRECIO_VENTA"] for e in ventas],
    #    mode='markers',
    #    marker=dict(color='red', size=10, symbol='triangle-down'),
    #    name='Venta'
    #))
    graficos.append(
        html.Div([
            html.Div([
                html.P("Ganancia total:"),
                html.H3(f"${ganancia_total:.2f}", style={'color': color_texto}),
                html.P("Variación porcentual:"),
                html.H3(f"{porcentaje:.2f}%", style={'color': color_texto}),
                dash_table.DataTable(
                    data = calculos_vertical,
                    page_size=10)
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
            html.Div([
                dcc.Graph(figure=fig)
            ], style={'width': '75%', 'display': 'inline-block'})
        ])
    )


app.layout = [
    html.Div(children='ACCIONES'),
    dash_table.DataTable(
        data=df_csv.to_dict('records'),
        page_size=10),
    html.Div(graficos)
    ]

if __name__ == '__main__':
    app.run(port=8000, debug=True)
