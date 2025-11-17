import pdfplumber
import pandas as pd
import folium

coords_csv = 'coordenadas_ppBio_corrigidas.csv'

df_coords = pd.read_csv(coords_csv, encoding='utf-8')
df_coords['name_norm'] = df_coords['name'].astype(str).str.strip()

# Como já temos os dados corrigidos, não precisamos do merge com PDF
df_merged = df_coords.copy()
df_merged['nome_final'] = df_merged['name']
df_merged['Existência'] = 'SIM'  # Todas são existentes

# Limpar dados
df_merged['lat'] = pd.to_numeric(df_merged['lat'], errors='coerce')
df_merged['long'] = pd.to_numeric(df_merged['long'], errors='coerce')
df_merged = df_merged.dropna(subset=['lat', 'long'])

# Mapa aprimorado
center = [df_merged['lat'].mean(), df_merged['long'].mean()]
m = folium.Map(
    location=center,
    zoom_start=10,
    tiles=None,
    control_scale=True,
    min_zoom=6,
    max_zoom=18
)

# Fallback: ensure min/max zoom are present in map options for older folium versions
# Use 'minZoom'/'maxZoom' keys which appear in the Leaflet initialization
m.options.setdefault('minZoom', 6)
m.options.setdefault('maxZoom', 18)
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri', name='Satélite').add_to(m)
folium.TileLayer('OpenTopoMap', name='Terreno').add_to(m)

# Camadas contextuais
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

# Criar grupos por módulo
modules = df_merged['module'].dropna().unique()
group_dict = {}
for mod in modules:
    fg = folium.FeatureGroup(name=f'Módulo {mod}', show=True)
    m.add_child(fg)
    group_dict[mod] = fg

# Adicionar controle de camadas
folium.LayerControl(collapsed=False).add_to(m)


# Adicionar marcadores
for _, r in df_merged.iterrows():
    mod = r.get('module', '')
    tipo = str(r.get('type', '')).strip()
    existencia = str(r.get('Existência', '')).upper().strip()
    nome_antigo = r.get('name', '')
    nome_novo = r.get('nome_final', nome_antigo)
    lat, lon = r['lat'], r['long']
    
    # Popup informativo
    popup_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 200px;">
        <h4 style="margin: 0; color: #2E8B57;">{nome_novo}</h4>
        <p style="margin: 5px 0;"><strong>Nome antigo:</strong> {nome_antigo}</p>
        <p style="margin: 5px 0;"><strong>Módulo:</strong> {mod}</p>
        <p style="margin: 5px 0;"><strong>Tipo:</strong> {tipo}</p>
        <p style="margin: 5px 0;"><strong>Existência:</strong> {existencia}</p>
        <p style="margin: 5px 0;"><strong>Coordenadas:</strong> {lat:.6f}, {lon:.6f}</p>
    </div>
    """
    
    if tipo.lower().startswith('ter'):
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            color='blue',
            fill=True,
            fill_color='lightblue',
            fill_opacity=0.7,
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=nome_novo
        ).add_to(group_dict.get(mod, m))
    elif tipo.lower().startswith('rip'):
        folium.RegularPolygonMarker(
            location=[lat, lon],
            number_of_sides=3,
            radius=10,
            color='green',
            fill=True,
            fill_color='lightgreen',
            fill_opacity=0.7,
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=nome_novo
        ).add_to(group_dict.get(mod, m))
    else:
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=nome_novo
        ).add_to(group_dict.get(mod, m))

# Legenda dinâmica
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 120px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
     border-radius:6px; padding: 10px">
<p><strong>Legenda</strong></p>
<p><i class="fa fa-circle" style="color:blue"></i> Terrestre</p>
<p><i class="fa fa-play" style="color:green; transform: rotate(90deg);"></i> Ripária</p>
<p><i class="fa fa-map-marker" style="color:gray"></i> Outro</p>
</div>
'''
m.get_root().add_child(folium.Element(legend_html))

# Non-breaking JS fallback to enforce min/max zoom after map is created.
# This avoids changing the Leaflet initializer object and thus prevents
# parsing issues in environments where Folium emits a spread-like token.
fallback_js = """
<script>
document.addEventListener('DOMContentLoaded', function () {
    // Try to set zoom limits on any global map_* object. Retry a few times
    // to account for execution order differences in generated HTML.
    function applyLimits(attemptsLeft) {
        let appliedAny = false;
        for (const k in window) {
            if (k.startsWith('map_') && window[k] && typeof window[k].setMinZoom === 'function') {
                try {
                    window[k].setMinZoom(6);
                    window[k].setMaxZoom(18);
                    console.log('Zoom limits applied to', k);
                    appliedAny = true;
                } catch (e) {
                    console.warn('Failed to apply zoom limits', e);
                }
            }
        }
        if (!appliedAny && attemptsLeft > 0) {
            setTimeout(function(){ applyLimits(attemptsLeft - 1); }, 100);
        }
    }
    // initial attempt with 10 retries
    applyLimits(10);
});
</script>
"""
fallback_marker = '<!-- zoom-limits-applied -->'
root_str = str(m.get_root())
if fallback_marker not in root_str:
    m.get_root().html.add_child(folium.Element(fallback_marker + fallback_js))

# Salvar
m.save('mapa_simples_completo.html')
# Folium sometimes serializes JS with an object spread token "...{" that breaks
# in-browser initialization on some environments. Post-process the HTML:
# Remove post-processing because it caused an invalid JS token in the generated HTML and
# left the map blank for some users. For now, rely on folium's map options only and avoid
# injecting/editing the rendered HTML at the end of the generation flow.
print(f'Mapa simples gerado: mapa_simples_completo.html')
print(f'Total de parcelas: {len(df_merged)}')