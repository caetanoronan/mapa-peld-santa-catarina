import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Carregar dados
df = pd.read_csv('analise_integrada_pdf_csv.csv')

# Função para criar gráfico interativo de distribuição de altitude
def create_altitude_distribution():
    fig = px.histogram(df, x='Altitude',
                      title='Distribuição de Altitude das Parcelas PPBio',
                      labels={'Altitude': 'Altitude (m)', 'count': 'Frequência'},
                      color_discrete_sequence=['#2E8B57'])

    fig.update_layout(
        xaxis_title="Altitude (m)",
        yaxis_title="Número de Parcelas",
        showlegend=False,
        height=400
    )

    return fig

# Função para criar boxplot de altitude por módulo
def create_altitude_by_module():
    fig = px.box(df, x='Mod', y='Altitude',
                title='Altitude por Módulo PPBio',
                labels={'Mod': 'Módulo', 'Altitude': 'Altitude (m)'},
                color='Mod',
                color_discrete_sequence=['#2E8B57', '#3CB371', '#90EE90'])

    fig.update_layout(height=400)
    return fig

# Função para criar gráfico de tipos de vegetação
def create_vegetation_types():
    veg_counts = df['tipo.veg'].value_counts().reset_index()
    veg_counts.columns = ['Tipo de Vegetação', 'Contagem']

    fig = px.bar(veg_counts, x='Tipo de Vegetação', y='Contagem',
                title='Distribuição dos Tipos de Vegetação',
                color='Tipo de Vegetação',
                color_discrete_sequence=['#2E8B57', '#3CB371', '#90EE90', '#98FB98'])

    fig.update_layout(height=400)
    return fig

# Função para criar stripplot de altitude por vegetação
def create_altitude_by_vegetation():
    fig = px.strip(df, x='tipo.veg', y='Altitude',
                  title='Altitude por Tipo de Vegetação',
                  labels={'tipo.veg': 'Tipo de Vegetação', 'Altitude': 'Altitude (m)'},
                  color='tipo.veg',
                  color_discrete_sequence=['#2E8B57', '#3CB371', '#90EE90', '#98FB98'])

    fig.update_layout(height=400)
    return fig

# Função para criar scatter plot altitude vs biomassa
def create_altitude_vs_biomass():
    # Calcular biomassa média por parcela
    biomass_cols = ['Biom1', 'Biom2', 'Biom3', 'Biom4']
    df['Biomassa_Media'] = df[biomass_cols].mean(axis=1)

    fig = px.scatter(df, x='Altitude', y='Biomassa_Media',
                    title='Altitude vs Biomassa do Estrato Superior',
                    labels={'Altitude': 'Altitude (m)', 'Biomassa_Media': 'Biomassa (%)'},
                    trendline="ols",
                    color_discrete_sequence=['#2E8B57'])

    fig.update_layout(height=400)
    return fig

# Função para criar boxplot de biomassa por estrato
def create_biomass_by_stratum():
    biomass_cols = ['Biom1', 'Biom2', 'Biom3', 'Biom4']
    biomass_names = ['Superior', 'Médio-Alto', 'Médio', 'Inferior']

    biomass_data = []
    for i, col in enumerate(biomass_cols):
        temp_df = df[['Mod', col]].copy()
        temp_df['Estrato'] = biomass_names[i]
        temp_df['Biomassa'] = temp_df[col]
        biomass_data.append(temp_df[['Mod', 'Estrato', 'Biomassa']])

    biomass_df = pd.concat(biomass_data)

    fig = px.box(biomass_df, x='Estrato', y='Biomassa',
                title='Biomassa por Estrato Vegetal',
                labels={'Estrato': 'Estrato Vegetal', 'Biomassa': 'Biomassa (%)'},
                color='Estrato',
                color_discrete_sequence=['#2E8B57', '#3CB371', '#90EE90', '#98FB98'])

    fig.update_layout(height=400)
    return fig

# Função para criar heatmap de correlação
def create_correlation_heatmap():
    # Selecionar colunas numéricas relevantes
    numeric_cols = ['Altitude', 'Biom1', 'Biom2', 'Biom3', 'Biom4',
                   'dossel', 'hmax', 'Prof1', 'Prof2', 'Prof3', 'Prof4']

    corr_matrix = df[numeric_cols].corr()

    fig = px.imshow(corr_matrix,
                   title='Matriz de Correlação Ecológica',
                   color_continuous_scale='RdBu_r',
                   aspect='auto')

    fig.update_layout(height=500)
    return fig

# Função para criar gráfico de profundidade do solo
def create_soil_depth():
    soil_cols = ['Prof1', 'Prof2', 'Prof3', 'Prof4']
    soil_names = ['Q1', 'Q2', 'Q3', 'Q4']

    soil_data = []
    for i, col in enumerate(soil_cols):
        temp_df = df[['Mod', col]].copy()
        temp_df['Quadrante'] = soil_names[i]
        temp_df['Profundidade'] = temp_df[col]
        soil_data.append(temp_df[['Mod', 'Quadrante', 'Profundidade']])

    soil_df = pd.concat(soil_data)

    fig = px.bar(soil_df.groupby('Quadrante')['Profundidade'].mean().reset_index(),
                x='Quadrante', y='Profundidade',
                title='Profundidade Média do Solo por Quadrante',
                labels={'Quadrante': 'Quadrante', 'Profundidade': 'Profundidade (cm)'},
                color_discrete_sequence=['#2E8B57'])

    fig.update_layout(height=400)
    return fig

# Gerar todos os gráficos e salvar como HTML
def generate_interactive_charts():
    charts = {
        'altitude_distribution': create_altitude_distribution(),
        'altitude_by_module': create_altitude_by_module(),
        'vegetation_types': create_vegetation_types(),
        'altitude_by_vegetation': create_altitude_by_vegetation(),
        'altitude_vs_biomass': create_altitude_vs_biomass(),
        'biomass_by_stratum': create_biomass_by_stratum(),
        'correlation_heatmap': create_correlation_heatmap(),
        'soil_depth': create_soil_depth()
    }

    # Salvar cada gráfico como HTML separado
    for chart_name, fig in charts.items():
        fig.write_html(f'{chart_name}_interactive.html')
        print(f'Gráfico {chart_name} salvo como {chart_name}_interactive.html')

    print("Todos os gráficos interativos foram gerados!")

if __name__ == "__main__":
    generate_interactive_charts()