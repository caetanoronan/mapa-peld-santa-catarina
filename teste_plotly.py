import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv('analise_integrada_pdf_csv.csv')

# Criar um gráfico simples
fig = px.histogram(df, x='Altitude', title='Teste')

# Salvar
fig.write_html('teste_interactive.html')
print("Gráfico de teste criado!")