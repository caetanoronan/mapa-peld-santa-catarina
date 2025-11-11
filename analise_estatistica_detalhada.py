import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados integrados
df = pd.read_csv('analise_integrada_pdf_csv.csv', low_memory=False)

print("ANÁLISE ESTATÍSTICA DETALHADA DOS DADOS PPBio")
print("="*60)

# Limpar dados
df = df.dropna(subset=['Altitude'])  # Remover linhas sem altitude

# Estatísticas gerais
print("1. ESTATÍSTICAS GERAIS")
print("-"*30)
print(f"Total de registros: {len(df)}")
print(f"Total de parcelas únicas: {df['Novo'].nunique()}")
print(f"Altitude - Média: {df['Altitude'].mean():.1f} m")
print(f"Altitude - Mediana: {df['Altitude'].median():.1f} m")
print(f"Altitude - Desvio padrão: {df['Altitude'].std():.1f} m")
print(f"Altitude - Mínima: {df['Altitude'].min():.1f} m")
print(f"Altitude - Máxima: {df['Altitude'].max():.1f} m")

# Estatísticas por módulo
print("\n2. ESTATÍSTICAS POR MÓDULO")
print("-"*30)
mod_stats = df.groupby(df['Novo'].str[:3]).agg({
    'Altitude': ['count', 'mean', 'std', 'min', 'max'],
    'Biom1': ['mean', 'std'],
    'tipo.veg': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'
}).round(2)
print(mod_stats)

# Estatísticas por tipo de vegetação
print("\n3. ESTATÍSTICAS POR TIPO DE VEGETAÇÃO")
print("-"*30)
veg_stats = df.groupby('tipo.veg').agg({
    'Altitude': ['count', 'mean', 'std'],
    'Biom1': ['mean', 'std'],
    'dossel': ['mean', 'std']
}).round(2)
print(veg_stats)

# Correlações
print("\n4. CORRELAÇÕES PRINCIPAIS")
print("-"*30)
numeric_cols = ['Altitude', 'Biom1', 'Biom2', 'Biom3', 'Biom4', 'dossel', 'hmax']
corr_matrix = df[numeric_cols].corr()
print("Matriz de correlação:")
print(corr_matrix.round(3))

# Correlação altitude vs biomassa
alt_biom_corr = df[['Altitude', 'Biom1']].corr().iloc[0,1]
print(f"\nCorrelação Altitude vs Biomassa (Biom1): {alt_biom_corr:.3f}")

# Teste t entre parcelas existentes e não existentes
print("\n5. COMPARAÇÃO ENTRE PARCELAS EXISTENTES vs NÃO EXISTENTES")
print("-"*30)
existing_alt = df[df['Existência'] == 'SIM']['Altitude'].dropna()
non_existing_alt = df[df['Existência'] == 'NÃO']['Altitude'].dropna()

if len(existing_alt) > 0 and len(non_existing_alt) > 0:
    t_stat, p_value = stats.ttest_ind(existing_alt, non_existing_alt)
    print(f"Teste t para Altitude - Estatística: {t_stat:.3f}, p-valor: {p_value:.3f}")
    print(f"Média altitude existente: {existing_alt.mean():.1f} m (n={len(existing_alt)})")
    print(f"Média altitude não existente: {non_existing_alt.mean():.1f} m (n={len(non_existing_alt)})")
else:
    print("Dados insuficientes para comparação de altitude")
    print(f"Parcelas existentes com altitude: {len(existing_alt)}")
    print(f"Parcelas não existentes com altitude: {len(non_existing_alt)}")

# Distribuição por altitude
print("\n6. DISTRIBUIÇÃO POR FAIXAS DE ALTITUDE")
print("-"*30)
df['altitude_faixa'] = pd.cut(df['Altitude'], bins=[0, 1000, 1300, 1600, 2000],
                              labels=['<1000m', '1000-1300m', '1300-1600m', '>1600m'])
alt_dist = df.groupby('altitude_faixa', observed=False).agg({
    'Novo': 'nunique',
    'tipo.veg': lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'
})
print(alt_dist)

# Análise de solo
print("\n7. ANÁLISE DE PROFUNDIDADE DO SOLO")
print("-"*30)
solo_cols = ['Prof1', 'Prof2', 'Prof3', 'Prof4']
solo_stats = df[solo_cols].agg(['mean', 'std', 'min', 'max']).round(2)
print(solo_stats)

# Análise de biomassa por estrato
print("\n8. ANÁLISE DE BIOMASSA POR ESTRATO")
print("-"*30)
biom_cols = ['Biom1', 'Biom2', 'Biom3', 'Biom4']
biom_stats = df[biom_cols].agg(['mean', 'std', 'min', 'max']).round(2)
print(biom_stats)

# Espécies/observações mais frequentes
print("\n9. ANÁLISES DE ESPÉCIES E VEGETAÇÃO")
print("-"*30)
veg_freq = df['Veg'].value_counts().head(10)
print("Espécies/vegetação mais frequentes na coluna Veg:")
print(veg_freq)

obs_freq = df['obs'].dropna().value_counts().head(10)
print("\nObservações mais frequentes:")
print(obs_freq)

# Salvar análises
with open('analise_estatistica_detalhada.txt', 'w', encoding='utf-8') as f:
    f.write("ANÁLISE ESTATÍSTICA DETALHADA PPBio\n")
    f.write("="*50 + "\n")
    f.write(f"Data da análise: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n\n")
    f.write(str(mod_stats) + "\n\n")
    f.write(str(veg_stats) + "\n\n")
    f.write(str(corr_matrix) + "\n\n")

print("\nAnálise salva em 'analise_estatistica_detalhada.txt'")