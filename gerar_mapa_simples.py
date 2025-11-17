import pandas as pd
import folium

# Leitura do CSV com ponto e vírgula e encoding latin1
csv_path = 'amb_csv/ppbio_sc-coordenadas_parcelas.csv'
try:
    df = pd.read_csv(csv_path, encoding='latin1', sep=';')
except Exception as e:
    raise SystemExit(f"Erro ao ler CSV '{csv_path}': {e}")

# Normalizar coluna 'type' (corrigir problemas de encoding)
if 'type' in df.columns:
    df['type_clean'] = df['type'].astype(str).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('ascii')
    # Mapear termos em português sem acento
    df['type_clean'] = df['type_clean'].str.replace('Riparia', 'Riparia', regex=False)
    df['type_clean'] = df['type_clean'].str.replace('Terrestre', 'Terrestre', regex=False)
else:
    df['type_clean'] = 'Unknown'

# Coordenadas
if 'lat' not in df.columns or 'long' not in df.columns:
    raise SystemExit("CSV não contém colunas 'lat' e 'long'.")

# Converter para numérico
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['long'] = pd.to_numeric(df['long'], errors='coerce')

# Remover linhas sem coordenadas
df = df.dropna(subset=['lat', 'long'])

# Criar mapa
m = folium.Map(location=[df['lat'].mean(), df['long'].mean()], zoom_start=11, min_zoom=6, max_zoom=18)

# Compatibilizar com versões antigas do Folium — garante min/max zoom nas options
m.options.setdefault('minZoom', 6)
m.options.setdefault('maxZoom', 18)

# Grupos de camadas
fg_terrestre = folium.FeatureGroup('Parcelas Terrestres', show=True)
fg_riparia = folium.FeatureGroup('Parcelas Ripárias', show=True)

for _, row in df.iterrows():
    popup = folium.Popup(f"<b>Módulo:</b> {row.get('module','')}<br>"
                         f"<b>Nome:</b> {row.get('name','')}<br>"
                         f"<b>Tipo:</b> {row.get('type','')}<br>"
                         f"<b>Lat:</b> {row['lat']}<br>"
                         f"<b>Long:</b> {row['long']}", max_width=300)
    icon_color = 'blue' if str(row.get('type','')).lower().startswith('ter') else 'green'
    marker = folium.Marker(location=[row['lat'], row['long']], popup=popup, icon=folium.Icon(color=icon_color))
    if str(row.get('type_clean','')).lower().startswith('ter'):
        marker.add_to(fg_terrestre)
    else:
        marker.add_to(fg_riparia)

fg_terrestre.add_to(m)
fg_riparia.add_to(m)
folium.LayerControl().add_to(m)

out = 'mapa_interativo_simples.html'
# Inject fallback JS to apply zoom limits safely before saving
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
# Avoid injecting the same fallback multiple times across runs
fallback_marker = '<!-- zoom-limits-applied -->'
root_str = str(m.get_root())
if fallback_marker not in root_str:
    m.get_root().html.add_child(folium.Element(fallback_marker + fallback_js))
# Avoid injecting the same fallback multiple times across runs

m.save(out)
print(f"Mapa simples criado: {out}")
