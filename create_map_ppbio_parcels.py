import pandas as pd
import folium
from folium.plugins import MarkerCluster
import re

# Ler coordenadas das parcelas
coords_df = pd.read_csv('amb_csv/ppbio_sc-coordenadas_parcelas.csv', sep=';', encoding='latin-1')
print("Coordenadas carregadas:")
print(coords_df.head())
print(f"Total de parcelas com coordenadas: {len(coords_df)}")

# Ler texto do PDF para extrair mapeamento
with open('pdf_extracted_text.txt', 'r', encoding='utf-8') as f:
    pdf_text = f.read()

# Extrair linhas da tabela (cada linha tem formato: ANTIGO NOVO SIM/NÃO)
lines = pdf_text.split('\n')
mapping = {}

for line in lines:
    # Procurar por linhas que contenham códigos e SIM
    if 'SIM' in line and len(line.split()) >= 3:
        parts = line.split()
        if len(parts) >= 3:
            antigo = parts[0]
            novo = parts[1]
            existencia = parts[2]
            if existencia == 'SIM':
                mapping[antigo] = novo

print(f"\nMapeamento extraído do PDF: {len(mapping)} parcelas existentes")
for antigo, novo in mapping.items():
    print(f"{antigo} -> {novo}")

# Criar dicionário reverso (antigo -> novo) para facilitar busca
reverse_mapping = mapping  # mapping já é {antigo: novo}

# Filtrar coordenadas apenas para parcelas que existem
existing_parcels = []
for _, row in coords_df.iterrows():
    name = row['name']
    # Verificar se o nome está no mapeamento reverso
    if name in reverse_mapping:
        existing_parcels.append({
            'name': name,
            'novo_codigo': reverse_mapping[name],
            'lat': row['lat'],
            'long': row['long'],
            'type': row['type'],
            'module': row['module']
        })

print(f"\nParcelas existentes com coordenadas encontradas: {len(existing_parcels)}")

# Criar mapa centrado em Santa Catarina
center_lat = coords_df['lat'].mean()
center_long = coords_df['long'].mean()

m = folium.Map(location=[center_lat, center_long], zoom_start=10,
               tiles='OpenStreetMap')

# Apply fallback for min/max zoom to ensure Leaflet limits even if Folium serializes oddly
m.options.setdefault('minZoom', 6)
m.options.setdefault('maxZoom', 18)

minz = m.options.get('minZoom', 6)
maxz = m.options.get('maxZoom', 18)
fallback_js = f"""
<script>
document.addEventListener('DOMContentLoaded', function () {{
    function applyLimits(attemptsLeft) {{
        let applied = false;
        for (const k in window) {{
            if (k.startsWith('map_') && window[k] && typeof window[k].setMinZoom === 'function') {{
                try {{
                    window[k].setMinZoom({minz});
                    window[k].setMaxZoom({maxz});
                    applied = true;
                }} catch (e) {{ console.warn('Failed to apply zoom', e); }}
            }}
        }}
        if (!applied && attemptsLeft > 0) setTimeout(function(){{applyLimits(attemptsLeft - 1);}}, 100);
    }}
    applyLimits(10);
}});
</script>
"""
fallback_marker = '<!-- zoom-limits-applied -->'
root_str = str(m.get_root())
if fallback_marker not in root_str:
    m.get_root().html.add_child(folium.Element(fallback_marker + fallback_js))

# Adicionar marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Cores por módulo
module_colors = {
    'M1': 'red',
    'M2': 'blue',
    'M3': 'green'
}

# Adicionar marcadores para cada parcela existente
for parcel in existing_parcels:
    color = module_colors.get(parcel['module'], 'gray')

    # Criar popup com informações
    popup_text = f"""
    <b>Parcela: {parcel['name']}</b><br>
    <b>Código Novo: {parcel['novo_codigo']}</b><br>
    Tipo: {parcel['type']}<br>
    Módulo: {parcel['module']}<br>
    Coordenadas: {parcel['lat']:.6f}, {parcel['long']:.6f}
    """

    folium.CircleMarker(
        location=[parcel['lat'], parcel['long']],
        radius=8,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(marker_cluster)

# Adicionar legenda
legend_html = '''
<div style="position: fixed;
     bottom: 50px; left: 50px; width: 180px; height: 120px;
     background-color: white; border:2px solid grey; z-index:9999;
     font-size:14px; padding: 10px">
<p><b>Legenda - Parcelas PPBio</b></p>
<p><span style="color:red;">●</span> Módulo 1 (M01)</p>
<p><span style="color:blue;">●</span> Módulo 2 (M02)</p>
<p><span style="color:green;">●</span> Módulo 3 (M03)</p>
<p><b>Total: {}</b> parcelas</p>
</div>
'''.format(len(existing_parcels))

m.get_root().html.add_child(folium.Element(legend_html))

# Adicionar título
title_html = '''
<h3 align="center" style="font-size:20px"><b>Mapa das Parcelas PPBio Existentes - Santa Catarina</b></h3>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Salvar mapa
m.save('mapa_parcelas_ppbio_existentes.html')
print("\nMapa salvo como 'mapa_parcelas_ppbio_existentes.html'")

# Estatísticas
print("\nEstatísticas do mapa:")
print(f"Total de parcelas existentes: {len(existing_parcels)}")

modules_count = {}
for parcel in existing_parcels:
    mod = parcel['module']
    modules_count[mod] = modules_count.get(mod, 0) + 1

print("Parcelas por módulo:")
for mod, count in modules_count.items():
    print(f"  {mod}: {count} parcelas")

types_count = {}
for parcel in existing_parcels:
    typ = parcel['type']
    types_count[typ] = types_count.get(typ, 0) + 1

print("Parcelas por tipo:")
for typ, count in types_count.items():
    print(f"  {typ}: {count} parcelas")