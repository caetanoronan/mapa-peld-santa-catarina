import pdfplumber
import pandas as pd
import folium
from folium.plugins import MarkerCluster, FeatureGroupSubGroup
from branca.element import Template, MacroElement
import json

pdf_path = 'Parcelas PPBio Atualizadas.pdf'
coords_csv = 'amb_csv/ppbio_sc-coordenadas_parcelas.csv'

# --- Extrair tabela de renomeação do PDF ---
with pdfplumber.open(pdf_path) as pdf:
    tables = []
    for page in pdf.pages:
        for table in page.extract_tables():
            tables.append(table)

if not tables:
    raise SystemExit('Nenhuma tabela encontrada no PDF')

first = tables[0]
df_pdf = pd.DataFrame(first)
# Promover header se necessário
header = df_pdf.iloc[0].tolist()
if 'Antigo' in header and 'Novo' in header:
    df_pdf.columns = header
    df_pdf = df_pdf[1:].reset_index(drop=True)
else:
    df_pdf.columns = ['Antigo', 'Novo', 'Existência']

df_pdf['Antigo'] = df_pdf['Antigo'].astype(str).str.strip()
df_pdf['Novo'] = df_pdf['Novo'].astype(str).str.strip()
df_pdf['Existência'] = df_pdf['Existência'].astype(str).str.strip()

# Salvar mapeamento (opcional)
map_csv = 'amb_csv/parcelas_renomeadas_from_pdf.csv'
df_pdf.to_csv(map_csv, index=False, encoding='utf-8')
print(f'Mapeamento salvo em: {map_csv}')

# --- Carregar coordenadas ---
df_coords = pd.read_csv(coords_csv, encoding='latin1', sep=';')
df_coords['name_norm'] = df_coords['name'].astype(str).str.strip()
df_pdf['Antigo_norm'] = df_pdf['Antigo'].astype(str).str.strip()

# Merge
df_merged = pd.merge(df_coords, df_pdf[['Antigo_norm', 'Novo', 'Existência']], left_on='name_norm', right_on='Antigo_norm', how='left')
df_merged['nome_final'] = df_merged['Novo'].fillna(df_merged['name'])

merged_csv = 'amb_csv/parcelas_coords_com_nome_novo.csv'
df_merged.to_csv(merged_csv, index=False, encoding='utf-8')
print(f'CSV de coordenadas com novo nome salvo em: {merged_csv}')

# --- Preparar mapa com camadas por módulo e tipos, clusters e legenda ---
df_merged['lat'] = pd.to_numeric(df_merged['lat'], errors='coerce')
df_merged['long'] = pd.to_numeric(df_merged['long'], errors='coerce')
df_merged = df_merged.dropna(subset=['lat', 'long'])

center = [df_merged['lat'].mean(), df_merged['long'].mean()]
# Criar mapa sem camada base padrão e adicionar múltiplas camadas base (Satellite, Terrain, OpenStreetMap)
m = folium.Map(location=center, zoom_start=11, tiles=None)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap', control=True).add_to(m)
folium.TileLayer('Stamen Terrain', name='Terrain', control=True,
                 attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
# ESRI World Imagery (satellite)
folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                 attr='Esri', name='Satellite', overlay=False, control=True).add_to(m)

# Cores por tipo
type_color = {
    'Terrestre': 'blue',
    'Riparia': 'green'
}

# Cor para existência
exist_color = {
    'SIM': 'darkblue',
    'NÃO': 'lightgray',
    'NAO': 'lightgray',
    '': 'lightgray'
}

# Criar grupos por módulo e tipo (sem subgrupos, FeatureGroups separadas para aparecer no LayerControl)
modules = sorted(df_merged['module'].dropna().unique())
subgroup_map = {}  # (module, type) -> MarkerCluster
for mod in modules:
    for t in ['Terrestre', 'Riparia']:
        fg_name = f'Módulo {mod} - {t}'
        fg = folium.FeatureGroup(name=fg_name, show=True)
        m.add_child(fg)
        mc = MarkerCluster().add_to(fg)
        subgroup_map[(mod, t)] = mc

# Grupo para parcelas sem módulo ou tipo outros
no_mod_fg = folium.FeatureGroup(name='Sem Módulo', show=False)
no_mod_cluster = MarkerCluster().add_to(no_mod_fg)
m.add_child(no_mod_fg)

# Contadores para debug
counters = {key: 0 for key in subgroup_map.keys()}
counters['no_mod'] = 0

# Construir GeoJSON
features = []

# Adicionar marcadores
for _, r in df_merged.iterrows():
    mod = r.get('module') if pd.notna(r.get('module')) else None
    tipo = str(r.get('type', '')).strip()
    tipo_clean = 'Terrestre' if tipo.lower().startswith('ter') else ('Riparia' if tipo.lower().startswith('rip') else 'Outros')
    existencia = str(r.get('Existência', '')).upper().strip()
    nome_antigo = r.get('name', '')
    nome_novo = r.get('nome_final', nome_antigo)
    lat = r['lat']
    lon = r['long']
    popup_html = (f"<b>Nome antigo:</b> {nome_antigo}<br>"
                  f"<b>Nome novo:</b> {nome_novo}<br>"
                  f"<b>Módulo:</b> {mod}<br>"
                  f"<b>Tipo:</b> {tipo}<br>"
                  f"<b>Existência:</b> {existencia}")
    popup = folium.Popup(popup_html, max_width=350)

    # cor base por tipo
    base_color = type_color.get(tipo_clean, 'gray')
    draw_color = exist_color.get(existencia, base_color)

    # Criar marcador com forma distinta
    if tipo_clean == 'Terrestre':
        marker = folium.CircleMarker(location=[lat, lon], radius=6, color=draw_color, fill=True, fill_color=draw_color, popup=popup)
    elif tipo_clean == 'Riparia':
        marker = folium.RegularPolygonMarker(location=[lat, lon], number_of_sides=3, radius=8, color=draw_color, fill_color=draw_color, popup=popup)
    else:
        marker = folium.Marker(location=[lat, lon], popup=popup)

    # Adicionar em subgrupo apropriado
    if mod in modules and tipo_clean in ['Terrestre', 'Riparia']:
        mc = subgroup_map.get((mod, tipo_clean))
        if mc is not None:
            mc.add_child(marker)
            counters[(mod, tipo_clean)] += 1
        else:
            no_mod_cluster.add_child(marker)
            counters['no_mod'] += 1
    else:
        no_mod_cluster.add_child(marker)
        counters['no_mod'] += 1

    # Adicionar feature para GeoJSON
    feat = {
        'type': 'Feature',
        'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
        'properties': {
            'nome_antigo': nome_antigo,
            'nome_novo': nome_novo,
            'module': mod,
            'type': tipo,
            'existencia': existence if False else existencia
        }
    }
    features.append(feat)

# Salvar GeoJSON
geo = {'type': 'FeatureCollection', 'features': features}
geo_path = 'amb_csv/parcelas_geo.json'
with open(geo_path, 'w', encoding='utf-8') as f:
    json.dump(geo, f, ensure_ascii=False, indent=2)
print(f'GeoJSON salvo em: {geo_path}')

# Incluir camada GeoJSON
folium.GeoJson(geo_path, name='Parcelas (GeoJSON)', tooltip=folium.GeoJsonTooltip(fields=['nome_novo', 'module', 'type', 'existencia'], aliases=['Nome','Módulo','Tipo','Existência'])).add_to(m)

# Adicionar controle de camadas
folium.LayerControl(collapsed=False).add_to(m)

# Adicionar título
title_html = '''
<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 1000; background-color: white; padding: 10px; border: 2px solid black; font-size: 16px;">
<h3 style="margin: 0;"><b>Mapa Interativo das Parcelas PELD - Santa Catarina</b></h3>
<p style="margin: 5px 0 0 0;">Use o controle de camadas (canto superior direito) para ligar/desligar módulos e tipos.</p>
</div>
'''
title_element = folium.Html(title_html, script=True)
m.get_root().add_child(title_element)

# Legenda (HTML simples)
legend_html = '''
{% macro html(this, kwargs) %}
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 260px; height: 160px; 
     z-index:9999; font-size:14px; background-color: white; padding: 10px; border:2px solid gray;">
<b>Legenda</b><br>
&nbsp;<svg height="12" width="12"><circle cx="6" cy="6" r="5" fill="darkblue"/></svg>&nbsp;Terrestre (instalada)<br>
&nbsp;<svg height="12" width="12"><polygon points="6,1 11,11 1,11" fill="green"/></svg>&nbsp;Ripária (instalada)<br>
&nbsp;<svg height="12" width="12"><circle cx="6" cy="6" r="5" fill="lightgray"/></svg>&nbsp;Não instalada / Não consta<br>
<hr style="margin:6px 0">
<b>Camadas:</b><br>
&nbsp;Cada módulo tem subcamadas por tipo (toggle por módulo > tipo)
</div>
{% endmacro %}
'''
template = Template(legend_html)
macro = MacroElement()
macro._template = template
m.get_root().add_child(macro)

out_html = 'mapa_interativo_from_pdf.html'
m.save(out_html)
print(f'Mapa gerado: {out_html}')
print("Contadores de marcadores por grupo:")
for key, count in counters.items():
    print(f"{key}: {count}")
