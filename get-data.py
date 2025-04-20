import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Descargar datos de MSFT del último mes
dat = yf.Ticker("MSFT")
hist = dat.history(period='1y', interval='1d')

# Asegurarse de que el índice es datetime
hist.index = pd.to_datetime(hist.index)

# Graficar el precio de cierre
plt.figure(figsize=(12, 6))
plt.plot(hist.index, hist['Close'], label='Precio de Cierre', color='blue', linewidth=2)

plt.title('Fluctuación del precio de cierre de MSFT - Último mes')
plt.xlabel('Fecha')
plt.ylabel('Precio de Cierre (USD)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("grafico_msft.png")
print("Gráfico guardado como grafico_msft.png")
