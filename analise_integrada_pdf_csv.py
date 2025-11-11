import pandas as pd

# Carregar a tabela do PDF (extraída como CSV para facilitar)
pdf_data = {
    'Antigo': ['TN0500', 'TN1500', 'TN2500', 'TN3500', 'TN4500', 'TS0500', 'TS1500', 'TS2500', 'TS3500', 'TS4500',
               'TN1300', 'TN4000', 'TS0150', 'TS1845', 'TL0900', 'TW0500', 'TW1500', 'TW2500', 'TW3500', 'TW4500',
               'TL400_PSA4', 'TL1500', 'TL2500', 'TL3500', 'TL4500', 'TW065_RIP5_PSA9', 'NÃO CONSTA', 'NÃO CONSTA',
               'NÃO CONSTA', 'NÃO CONSTA', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10',
               'R1', 'R2', 'R3', 'NÃO CONSTA', 'NÃO CONSTA'],
    'Novo': ['M01T01', 'M01T02', 'M01T03', 'M01T04', 'M01T05', 'M01T06', 'M01T07', 'M01T08', 'M01T09', 'M01T10',
             'M01R01', 'M01R02', 'M01R03', 'M01R04', 'M01R05', 'M02T01', 'M02T02', 'M02T03', 'M02T04', 'M02T05',
             'M02T06', 'M02T07', 'M02T08', 'M02T09', 'M02T10', 'M02R01', 'M02R02', 'M02R03', 'M02R04', 'M02R05',
             'M03T01', 'M03T02', 'M03T03', 'M03T04', 'M03T05', 'M03T06', 'M03T07', 'M03T08', 'M03T09', 'M03T10',
             'M03R01', 'M03R02', 'M03R03', 'M03R04', 'M03R05'],
    'Existência': ['SIM']*15 + ['NÃO', 'SIM', 'NÃO', 'SIM', 'SIM', 'SIM', 'NÃO', 'NÃO', 'NÃO', 'NÃO', 'SIM'] + ['NÃO']*4 + ['SIM']*10 + ['SIM']*3 + ['NÃO']*2
}

df_pdf = pd.DataFrame(pdf_data)

# Carregar CSV
df_csv = pd.read_csv('amb_csv/amb.csv', encoding='latin-1')

print("Análise Integrada: PDF vs CSV")
print("="*50)

# Estatísticas básicas
print(f"Parcelas no PDF: {len(df_pdf)}")
print(f"Registros no CSV: {len(df_csv)}")
print(f"Parcelas únicas no CSV: {df_csv['Plot'].nunique()}")

# Merge baseado no código novo
df_merged = pd.merge(df_pdf, df_csv, left_on='Novo', right_on='Plot', how='left')

print(f"\nApós merge: {len(df_merged)} registros")

# Verificar quais parcelas do PDF têm dados no CSV
parcels_with_data = df_merged.dropna(subset=['Plot']).groupby('Novo').size()
print(f"Parcelas do PDF com dados no CSV: {len(parcels_with_data)}")

parcels_without_data = df_merged[df_merged['Plot'].isna()]['Novo'].unique()
print(f"Parcelas do PDF SEM dados no CSV: {list(parcels_without_data)}")

# Análise por existência
existing_parcels = df_pdf[df_pdf['Existência'] == 'SIM']['Novo']
non_existing_parcels = df_pdf[df_pdf['Existência'] == 'NÃO']['Novo']

existing_with_data = len([p for p in existing_parcels if p in parcels_with_data.index])
non_existing_with_data = len([p for p in non_existing_parcels if p in parcels_with_data.index])

print(f"\nParcelas existentes (SIM) com dados: {existing_with_data}/{len(existing_parcels)}")
print(f"Parcelas não existentes (NÃO) com dados: {non_existing_with_data}/{len(non_existing_parcels)}")

# Estatísticas dos dados disponíveis
if not df_merged.empty:
    print("\nEstatísticas dos dados CSV para parcelas do PDF:")
    print(f"Altitude média: {df_merged['Altitude'].mean():.1f} m")
    print(f"Altitude mínima: {df_merged['Altitude'].min()} m")
    print(f"Altitude máxima: {df_merged['Altitude'].max()} m")
    
    # Tipos de vegetação
    veg_types = df_merged['tipo.veg'].value_counts()
    print(f"\nTipos de vegetação mais comuns:")
    print(veg_types.head(5))

# Salvar análise
df_merged.to_csv('analise_integrada_pdf_csv.csv', index=False)
print("\nAnálise salva em 'analise_integrada_pdf_csv.csv'")