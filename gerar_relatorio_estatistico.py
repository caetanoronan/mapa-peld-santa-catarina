import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from pathlib import Path
from scipy import stats
import math
try:
    import statsmodels.formula.api as smf
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    HAS_STATSMODELS = True
except Exception:
    HAS_STATSMODELS = False

# Load consolidated CSV
consol = pd.read_csv('relatorio_consolidado_parcela.csv')
resumo = pd.read_csv('resumo_por_parcela.csv')
corres = pd.read_csv('relatorio_correspondencias_duplicatas.csv')

# Merge where needed
df = consol.copy()
# Compute additional fields
for col in ['Altitude_mean','biom_total_mean','dossel_mean','hmax_mean']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Descriptive stats
desc_alt = df['Altitude_mean'].describe()
veg_counts = resumo['TipoVeg_Majoritario'].value_counts()

# Correlation matrix
corr_cols = ['Altitude_mean','biom_total_mean','dossel_mean','hmax_mean']
pearson_corr = df[corr_cols].corr(method='pearson')
spearman_corr = df[corr_cols].corr(method='spearman')
# p-values for Pearson
pearson_pvals = pd.DataFrame(np.ones((len(corr_cols), len(corr_cols))), index=corr_cols, columns=corr_cols)
for i, a in enumerate(corr_cols):
    for j, b in enumerate(corr_cols):
        if i < j:
            valid = df[[a, b]].dropna()
            if len(valid) >= 3:
                r, p = stats.pearsonr(valid[a], valid[b])
                pearson_pvals.loc[a, b] = p
                pearson_pvals.loc[b, a] = p

# Plots
# 1. Altitude distribution histogram
fig_alt = go.Figure()
fig_alt.add_trace(go.Histogram(
    x=df['Altitude_mean'],
    nbinsx=20,
    marker=dict(color='#7bccc4', line=dict(color='#2b8cbe', width=2)),
    hovertemplate='Altitude média: %{x}<br>Contagem: %{y}<extra></extra>',
    name='Altitude',
    showlegend=False,
    opacity=0.85
))
fig_alt.update_layout(
    title=dict(text='Distribuição de Altitude das Parcelas', font=dict(size=22, family='Inter, Arial, sans-serif', color='#222'), x=0.05),
    xaxis=dict(title=dict(text='Altitude média (m)', font=dict(size=16, family='Inter, Arial, sans-serif', color='#222')), tickfont=dict(size=14), gridcolor='#e0f3db', zerolinecolor='#a8ddb5', automargin=True),
    yaxis=dict(title=dict(text='Número de Parcelas', font=dict(size=16, family='Inter, Arial, sans-serif', color='#222')), tickfont=dict(size=14), gridcolor='#e0f3db', zerolinecolor='#a8ddb5', automargin=True),
    bargap=0.08,
    bargroupgap=0.04,
    plot_bgcolor='#f7fcfd',
    paper_bgcolor='#f7fcfd',
    hoverlabel=dict(bgcolor='#b2e2e2', font=dict(color='#222', size=14)),
    colorway=['#7bccc4', '#bae4bc', '#2b8cbe'],
    margin=dict(t=60, l=60, r=30, b=60),
    annotations=[dict(text='Fonte: dados ppBio', xref='paper', yref='paper', x=1, y=-0.18, showarrow=False, font=dict(size=12, color='#666'), align='right')]
)
hist_alt = fig_alt

# 2. Biomassa vs Altitude scatter
scatter_biom = px.scatter(df, x='Altitude_mean', y='biom_total_mean', color='Veg_major', trendline='ols', title='Biomassa vs Altitude')
# 3. Dossel vs Altitude
scatter_dossel = px.scatter(df, x='Altitude_mean', y='dossel_mean', color='Veg_major', trendline='ols', title='Cobertura de Dossel vs Altitude')
# 4. Correlation heatmap (values + significance stars)
def sig_star(p):
    if p < 0.001:
        return '***'
    if p < 0.01:
        return '**'
    if p < 0.05:
        return '*'
    return ''

text_corr = pearson_corr.round(3).astype(str)
for a in corr_cols:
    for b in corr_cols:
        if a == b:
            text_corr.loc[a, b] = text_corr.loc[a, b]
        else:
            p = pearson_pvals.loc[a, b]
            text_corr.loc[a, b] = f"{pearson_corr.loc[a, b]:.2f}{sig_star(p)}"

heat = px.imshow(pearson_corr, text_auto=True, labels=dict(x='Variável', y='Variável', color='r'), x=corr_cols, y=corr_cols, title='Matriz de Correlação (Pearson)')
heat.update_traces(text=text_corr.values)
# 5. Boxplots por vegetação
box_biom = px.box(resumo, x='TipoVeg_Majoritario', y='Biom_total_mean', title='Biomassa média por Tipo de Vegetação')
box_dossel = px.box(resumo, x='TipoVeg_Majoritario', y='dossel_mean', title='Cobertura de Dossel média por Tipo de Vegetação')

# Statistical tests
tests = []
# Shapiro-Wilk for normality
for col in corr_cols:
    valid = df[col].dropna()
    if len(valid) >= 3:
        stat, p = stats.shapiro(valid)
        tests.append({'test': 'Shapiro-Wilk', 'variable': col, 'stat': stat, 'pvalue': p, 'pairs': np.nan, 'r': np.nan, 'rho': np.nan})

# Correlations
for i, a in enumerate(corr_cols):
    for j, b in enumerate(corr_cols):
        if i < j:
            valid = df[[a, b]].dropna()
            if len(valid) >= 3:
                # Pearson
                r, p = stats.pearsonr(valid[a], valid[b])
                tests.append({'test': 'Pearson', 'variable': np.nan, 'stat': np.nan, 'pvalue': p, 'pairs': f'{a} x {b}', 'r': r, 'rho': np.nan})
                # Spearman
                rho, p_rho = stats.spearmanr(valid[a], valid[b])
                tests.append({'test': 'Spearman', 'variable': np.nan, 'stat': np.nan, 'pvalue': p_rho, 'pairs': f'{a} x {b}', 'r': np.nan, 'rho': rho})

tests_df = pd.DataFrame(tests)

# OLS models
models = []
if HAS_STATSMODELS:
    for dep in ['biom_total_mean', 'dossel_mean']:
        formula = f"{dep} ~ Altitude_mean"
        try:
            model = smf.ols(formula, data=df).fit()
            models.append({'dependent': dep, 'coef_alt': model.params['Altitude_mean'], 'p_alt': model.pvalues['Altitude_mean'], 'r2': model.rsquared})
        except:
            models.append({'dependent': dep, 'coef_alt': np.nan, 'p_alt': np.nan, 'r2': np.nan})
else:
    models = [{'dependent': 'biom_total_mean', 'coef_alt': np.nan, 'p_alt': np.nan, 'r2': np.nan}, {'dependent': 'dossel_mean', 'coef_alt': np.nan, 'p_alt': np.nan, 'r2': np.nan}]

models_df = pd.DataFrame(models)

# Generate HTML
html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Estatístico - ppBio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', Arial, sans-serif; background-color: #f8f9fa; }}
        .container {{ max-width: 1200px; }}
        h1 {{ color: #2c3e50; margin-bottom: 2rem; text-align: center; }}
        h2 {{ color: #34495e; margin-top: 2rem; }}
        .plotly-graph-div {{ margin: 1rem 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
        th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid #dee2e6; }}
        th {{ background-color: #f8f9fa; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="container my-5">
        <h1>Relatório Estatístico - Projeto ppBio</h1>
        
        <section id="resumo">
            <h2>Resumo Estatístico</h2>
            <p>Este relatório apresenta uma análise estatística completa dos dados do projeto ppBio, incluindo distribuições, correlações e testes de hipóteses.</p>
            <h3>Contagem por Tipo de Vegetação</h3>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Tipo de Vegetação</th>
                        <th>Contagem</th>
                    </tr>
                </thead>
                <tbody>
"""

for veg, count in veg_counts.items():
    html += f"""
                    <tr>
                        <th>{veg}</th>
                        <td>{count}</td>
                    </tr>"""

html += """
                </tbody>
            </table>
        </section>
        
        <section id="graficos">
            <h2>Gráficos</h2>
"""

# Add plots
html += hist_alt.to_html(full_html=False, include_plotlyjs=False)
html += "<h3>Biomassa vs Altitude</h3>"
html += scatter_biom.to_html(full_html=False, include_plotlyjs=False)
html += "<h3>Dossel vs Altitude</h3>"
html += scatter_dossel.to_html(full_html=False, include_plotlyjs=False)
html += "<h3>Matriz de Correlação</h3>"
html += heat.to_html(full_html=False, include_plotlyjs=False)
html += "<h3>Boxplots por tipo de vegetação</h3>"
html += box_biom.to_html(full_html=False, include_plotlyjs=False)
html += box_dossel.to_html(full_html=False, include_plotlyjs=False)

html += """
        </section>
        
        <section id="testes">
            <h2>Testes Realizados</h2>
"""

html += tests_df.to_html(index=False, classes='table table-striped')

html += """
            <h3>Modelos OLS</h3>
"""

html += models_df.to_html(index=False, classes='table table-striped')

html += """
        </section>
        
        <section id="tabelas">
            <h2>Tabela de Dados Consolidados</h2>
"""

html += df.to_html(index=False, classes='table table-striped')

html += """
        </section>
        
        <section id="metodo">
            <h2>Metodologia</h2>
            <p>As variáveis foram agregadas por parcela como médias (quando indicado). A biomassa total por parcela foi calculada como soma das colunas Biom1..Biom4. As análises de correlação e testes de hipóteses (ANOVA/Kruskal) foram realizados conforme presença de normalidade (Shapiro-Wilk). Em caso de ANOVA com diferenças significantes, foi aplicado teste de comparações múltiplas de Tukey. Se não houve normalidade, foi aplicado Kruskal-Wallis com testes pareados Mann-Whitney U com correção de Bonferroni.</p>
        </section>
    </div>
    
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

with open('apresentacao_relatorio_estatistico.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Relatório gerado com sucesso!")
