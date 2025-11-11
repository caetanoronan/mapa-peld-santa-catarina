import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Carregar dados
df = pd.read_csv('analise_integrada_pdf_csv.csv', low_memory=False)
df = df.dropna(subset=['Altitude'])

print("Gerando visualizações gráficas dos dados PPBio...")

# 1. Histograma de distribuição de altitude
plt.figure(figsize=(10, 6))
plt.hist(df['Altitude'], bins=20, edgecolor='black', alpha=0.7)
plt.title('Distribuição de Altitude das Parcelas PPBio', fontsize=14, fontweight='bold')
plt.xlabel('Altitude (m)')
plt.ylabel('Frequência')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('distribuicao_altitude.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Boxplot de altitude por módulo
plt.figure(figsize=(8, 6))
modulo_order = sorted(df['Novo'].str[:3].unique())
sns.boxplot(data=df, x=df['Novo'].str[:3], y='Altitude', order=modulo_order)
plt.title('Altitude por Módulo', fontsize=14, fontweight='bold')
plt.xlabel('Módulo')
plt.ylabel('Altitude (m)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('boxplot_altitude_modulo.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Scatter plot altitude vs biomassa
plt.figure(figsize=(10, 6))
plt.scatter(df['Altitude'], df['Biom1'], alpha=0.6, s=50)
plt.title('Relação entre Altitude e Biomassa (Estrato 1)', fontsize=14, fontweight='bold')
plt.xlabel('Altitude (m)')
plt.ylabel('Biomassa (%)')
plt.grid(True, alpha=0.3)

# Adicionar linha de tendência
z = np.polyfit(df['Altitude'], df['Biom1'], 1)
p = np.poly1d(z)
plt.plot(df['Altitude'], p(df['Altitude']), "r--", alpha=0.8, linewidth=2)

plt.tight_layout()
plt.savefig('scatter_altitude_biomassa.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Gráfico de barras de tipos de vegetação
plt.figure(figsize=(10, 6))
veg_counts = df['tipo.veg'].value_counts()
veg_counts.plot(kind='bar', edgecolor='black', alpha=0.7)
plt.title('Distribuição de Tipos de Vegetação', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Vegetação')
plt.ylabel('Número de Registros')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('barras_tipos_vegetacao.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Heatmap de correlação
plt.figure(figsize=(8, 6))
numeric_cols = ['Altitude', 'Biom1', 'Biom2', 'Biom3', 'Biom4', 'dossel', 'hmax']
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f',
            square=True, linewidths=0.5)
plt.title('Matriz de Correlação', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap_correlacao.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Boxplot de biomassa por estrato
plt.figure(figsize=(10, 6))
biom_data = df[['Biom1', 'Biom2', 'Biom3', 'Biom4']].melt(var_name='Estrato', value_name='Biomassa')
sns.boxplot(data=biom_data, x='Estrato', y='Biomassa')
plt.title('Distribuição de Biomassa por Estrato Vegetal', fontsize=14, fontweight='bold')
plt.xlabel('Estrato')
plt.ylabel('Biomassa (%)')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('boxplot_biomassa_estrato.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Gráfico de dispersão altitude vs tipo de vegetação
plt.figure(figsize=(12, 6))
sns.stripplot(data=df, x='tipo.veg', y='Altitude', alpha=0.7, jitter=True)
plt.title('Altitude por Tipo de Vegetação', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Vegetação')
plt.ylabel('Altitude (m)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('stripplot_altitude_vegetacao.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Gráfico de barras de profundidade do solo
plt.figure(figsize=(8, 6))
solo_means = df[['Prof1', 'Prof2', 'Prof3', 'Prof4']].mean()
solo_means.plot(kind='bar', edgecolor='black', alpha=0.7)
plt.title('Profundidade Média do Solo por Quadrante', fontsize=14, fontweight='bold')
plt.xlabel('Quadrante')
plt.ylabel('Profundidade (cm)')
plt.xticks(rotation=0)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('barras_profundidade_solo.png', dpi=300, bbox_inches='tight')
plt.close()

print("Gráficos gerados com sucesso!")
print("Arquivos salvos:")
print("- distribuicao_altitude.png")
print("- boxplot_altitude_modulo.png")
print("- scatter_altitude_biomassa.png")
print("- barras_tipos_vegetacao.png")
print("- heatmap_correlacao.png")
print("- boxplot_biomassa_estrato.png")
print("- stripplot_altitude_vegetacao.png")
print("- barras_profundidade_solo.png")