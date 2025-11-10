import pandas as pd

# Carregar dados das coordenadas
coords_df = pd.read_csv('amb_csv/ppbio_sc-coordenadas_parcelas.csv', sep=';', encoding='latin-1')

print('=== TODAS AS PARCELAS DO MÓDULO 2 ===')
m2_parcels = coords_df[coords_df['module'] == 'M2']
for _, row in m2_parcels.iterrows():
    print(f'{row["name"]} - {row["type"]} - ({row["lat"]:.6f}, {row["long"]:.6f})')

print('\n=== PARCELAS M2 EXISTENTES NO MAPA ===')
existing_m2 = ['TW1500', 'TW3500', 'TW4500', 'TL400_PSA4', 'TW065_RIP5_PSA9']
print('Existentes:', existing_m2)

print('\n=== PARCELAS M2 NÃO IMPLEMENTADAS ===')
all_m2 = m2_parcels['name'].tolist()
not_implemented = [p for p in all_m2 if p not in existing_m2]
print('Não implementadas:', not_implemented)
print(f'Total não implementadas: {len(not_implemented)}')

print('\n=== DETALHES DAS PARCELAS NÃO IMPLEMENTADAS ===')
for parcel_name in not_implemented:
    parcel_data = m2_parcels[m2_parcels['name'] == parcel_name].iloc[0]
    print(f'{parcel_name}: {parcel_data["type"]} - Coords: ({parcel_data["lat"]:.6f}, {parcel_data["long"]:.6f})')