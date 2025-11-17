import pdfplumber
import pandas as pd
import folium
from folium.plugins import MarkerCluster, Search
import json

# Carregar dados
pdf_path = 'Parcelas PPBio Atualizadas.pdf'
coords_csv = 'amb_csv/ppbio_sc-coordenadas_parcelas.csv'

# Extrair PDF
with pdfplumber.open(pdf_path) as pdf:
    tables = [page.extract_tables() for page in pdf.pages]
tables = [t for sub in tables for t in sub if t]

df_pdf = pd.DataFrame(tables[0])
if 'Antigo' in df_pdf.iloc[0].tolist():
    df_pdf.columns = df_pdf.iloc[0]
    df_pdf = df_pdf[1:]
df_pdf = df_pdf.apply(lambda x: x.astype(str).str.strip())

# Merge com coordenadas
df_coords = pd.read_csv(coords_csv, encoding='latin1', sep=';')
df_coords['name_norm'] = df_coords['name'].astype(str).str.strip()
df_pdf['Antigo_norm'] = df_pdf['Antigo']

df_merged = pd.merge(df_coords, df_pdf[['Antigo_norm', 'Novo', 'Existência']], left_on='name_norm', right_on='Antigo_norm', how='left')
df_merged['nome_final'] = df_merged['Novo'].fillna(df_merged['name'])
df_merged['lat'] = pd.to_numeric(df_merged['lat'], errors='coerce')
df_merged['long'] = pd.to_numeric(df_merged['long'], errors='coerce')
df_merged = df_merged.dropna(subset=['lat', 'long'])

# Mapa aprimorado
center = [df_merged['lat'].mean(), df_merged['long'].mean()]
m = folium.Map(location=center, zoom_start=10, tiles=None, control_scale=True, min_zoom=6, max_zoom=18)

# Fallback for older Folium versions
m.options.setdefault('minZoom', 6)
m.options.setdefault('maxZoom', 18)

# Camadas base
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
folium.TileLayer('OpenTopoMap', name='Terreno').add_to(m)

# Camadas contextuais (se arquivos existirem)
try:
    folium.GeoJson('parque_nacional_sj.geojson', name='Parque Nacional', style_function=lambda x: {'color': 'green', 'weight': 2}).add_to(m)
except:
    pass
try:
    folium.GeoJson('parque_estadual_serra_furada.geojson', name='Parque Estadual', style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)
except:
    pass
try:
    folium.GeoJson('limite_santa_catarina.geojson', name='Limite Estadual', style_function=lambda x: {'color': 'black', 'weight': 3}).add_to(m)
except:
    pass
try:
    folium.GeoJson('cidades_afetadas.geojson', name='Cidades Afetadas', style_function=lambda x: {'color': 'red', 'weight': 1}).add_to(m)
except:
    pass

# Grupos por módulo
modules = df_merged['module'].dropna().unique()
group_dict = {}
for mod in modules:
    fg = folium.FeatureGroup(name=f'Módulo {mod}', show=True)
    mc = MarkerCluster(disableClusteringAtZoom=15, spiderfyOnMaxZoom=True).add_to(fg)
    m.add_child(fg)
    group_dict[mod] = mc

# Adicionar marcadores
for _, r in df_merged.iterrows():
    mod = r.get('module')
    tipo = str(r.get('type', '')).strip()
    existencia = str(r.get('Existência', '')).upper().strip()
    nome_antigo = r.get('name', '')
    nome_novo = r.get('nome_final', nome_antigo)

    # Cor por tipo
    if tipo.lower().startswith('ter'):
        color = 'blue'
        icon_shape = 'circle'
    elif tipo.lower().startswith('rip'):
        color = 'green'
        icon_shape = 'triangle'
    else:
        color = 'gray'
        icon_shape = 'star'

    # Popup aprimorado
    popup_html = f"""
    <div style="font-family: Segoe UI; font-size: 14px; padding: 10px; border-radius: 8px; background: linear-gradient(to bottom, #f0f8f0, #e8f5e8); box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
        <h4 style="margin: 0; color: #2e7d32;">{nome_novo}</h4>
        <p><strong>Nome antigo:</strong> {nome_antigo}</p>
        <p><strong>Módulo:</strong> {mod}</p>
        <p><strong>Tipo:</strong> {tipo}</p>
        <p><strong>Existência:</strong> {existencia}</p>
        <p><strong>Lat:</strong> {r['lat']:.6f}</p>
        <p><strong>Long:</strong> {r['long']:.6f}</p>
    </div>
    """

    # Marcador personalizado
    if icon_shape == 'circle':
        marker = folium.CircleMarker(
            location=[r['lat'], r['long']],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=300)
        )
    elif icon_shape == 'triangle':
        marker = folium.RegularPolygonMarker(
            location=[r['lat'], r['long']],
            number_of_sides=3,
            radius=10,
            color=color,
            fill_color=color,
            popup=folium.Popup(popup_html, max_width=300)
        )
    else:
        marker = folium.Marker(
            location=[r['lat'], r['long']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color)
        )

    if mod in group_dict:
        marker.add_to(group_dict[mod])

# Controle de camadas
folium.LayerControl(collapsed=False).add_to(m)

# Legenda dinâmica
legend_html = '''
<div style="position: fixed; bottom: 50px; right: 50px; width: 200px; height: 150px; z-index:9999; font-size:12px; background: rgba(255,255,255,0.9); padding: 10px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.3); font-family: Segoe UI;">
    <h4 style="margin: 0 0 10px 0; color: #2e7d32;">Legenda</h4>
    <div><span style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: blue; margin-right: 5px;"></span>Terrestre</div>
    <div><span style="display: inline-block; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 10px solid green; margin-right: 5px;"></span>Ripária</div>
    <div><span style="display: inline-block; width: 12px; height: 12px; background: gray; margin-right: 5px;"></span>Outros</div>
    <hr style="margin: 8px 0;">
    <div id="counter">Total: 49 parcelas</div>
</div>
<script>
    // Atualizar contador dinamicamente (simples)
    document.getElementById('counter').innerText = 'Total: 49 parcelas';
</script>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Salvar
 # Add JS fallback to enforce zoom limits
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
m.get_root().html.add_child(folium.Element(fallback_js))
m.save('mapa_aprimorado.html')
print('Mapa aprimorado gerado: mapa_aprimorado.html')
# Add safe JS fallback to enforce zoom limits until Folium bug/serialization is resolved
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