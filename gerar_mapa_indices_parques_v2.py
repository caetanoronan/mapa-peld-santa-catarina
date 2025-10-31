import geopandas as gpd
import folium
import pandas as pd

# Carregar dados
df = pd.read_csv('amb_csv/ppbio_sc-coordenadas_parcelas.csv', encoding='latin1', sep=';')

# Carregar parques
parque_nacional = gpd.read_file('PROJETO_PELDSC/PARNA_SAO_JOAQUIM_SHP/PARNA SAO JOAQUIM SHP/PARNASJlimites.shp')
parque_nacional = parque_nacional.to_crs(epsg=4326)

parque_estadual = gpd.read_file('Projeto_PARNA_PESF/PARQUE_PESF_1_temp.shp')
parque_estadual = parque_estadual.to_crs(epsg=4326)

# Calcular centroids (usando bounds como alternativa mais simples)
pn_bounds = parque_nacional.total_bounds
pn_center_lat = (pn_bounds[1] + pn_bounds[3]) / 2
pn_center_lon = (pn_bounds[0] + pn_bounds[2]) / 2

pe_bounds = parque_estadual.total_bounds
pe_center_lat = (pe_bounds[1] + pe_bounds[3]) / 2
pe_center_lon = (pe_bounds[0] + pe_bounds[2]) / 2

# Criar mapa focado nos parques
mapa = folium.Map(location=[(pn_center_lat + pe_center_lat)/2, (pn_center_lon + pe_center_lon)/2],
                  zoom_start=11, min_zoom=8, max_zoom=18)

# Adicionar camada de relevo
folium.TileLayer(
    tiles='https://{s}.tile.opentomap.org/{z}/{x}/{y}.png',
    attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    name='Relevo (OpenTopoMap)',
    overlay=False
).add_to(mapa)

# Adicionar parques
folium.GeoJson(
    parque_nacional.__geo_interface__,
    name='Parque Nacional de São Joaquim',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'weight': 3, 'fillOpacity': 0.2}
).add_to(mapa)

folium.GeoJson(
    parque_estadual.__geo_interface__,
    name='Parque Estadual da Serra Furada',
    style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'weight': 2, 'fillOpacity': 0.2}
).add_to(mapa)

# Informações dos índices (textuais por enquanto)
ndvi_info = """
<h4>🌱 NDVI - Normalized Difference Vegetation Index</h4>
<p><b>Parque Nacional de São Joaquim</b></p>
<ul>
<li><b>Range:</b> -0.746 a 0.996</li>
<li><b>Média:</b> 0.771</li>
<li><b>Interpretação:</b> Alta saúde da vegetação (valores > 0.6)</li>
<li><b>Área saudável:</b> ~85% da cobertura vegetal</li>
</ul>
<img src="ndvi_overlay.png" style="max-width:100%; max-height:200px; border:1px solid #ddd;">
"""

evi_info = """
<h4>🌿 EVI - Enhanced Vegetation Index</h4>
<p><b>Parque Nacional de São Joaquim</b></p>
<ul>
<li><b>Range:</b> -1.000 a 2.000</li>
<li><b>Média:</b> 1.181</li>
<li><b>Interpretação:</b> Cobertura densa de vegetação</li>
<li><b>Vantagem:</b> Melhor para áreas com alta biomassa</li>
</ul>
<img src="evi_overlay.png" style="max-width:100%; max-height:200px; border:1px solid #ddd;">
"""

savi_info = """
<h4>🌾 SAVI - Soil Adjusted Vegetation Index</h4>
<p><b>Parque Estadual da Serra Furada</b></p>
<ul>
<li><b>Range:</b> -1.000 a 1.500</li>
<li><b>Média:</b> 1.115</li>
<li><b>Interpretação:</b> Vegetação ajustada à influência do solo</li>
<li><b>Aplicação:</b> Áreas com solo exposto ou ralo</li>
</ul>
"""

arvi_info = """
<h4>☁️ ARVI - Atmospherically Resistant Vegetation Index</h4>
<p><b>Parque Estadual da Serra Furada</b></p>
<ul>
<li><b>Range:</b> 0.488 a 2.000</li>
<li><b>Média:</b> 1.443</li>
<li><b>Interpretação:</b> Resistente a interferências atmosféricas</li>
<li><b>Vantagem:</b> Melhor para imagens com aerosóis</li>
</ul>
"""

# Adicionar marcadores com informações dos índices
folium.Marker(
    location=[pn_center_lat, pn_center_lon],
    popup=folium.Popup(ndvi_info, max_width=400),
    tooltip='NDVI - Parque Nacional',
    icon=folium.Icon(color='green', icon='leaf', prefix='fa')
).add_to(mapa)

folium.Marker(
    location=[pn_center_lat + 0.005, pn_center_lon + 0.005],
    popup=folium.Popup(evi_info, max_width=400),
    tooltip='EVI - Parque Nacional',
    icon=folium.Icon(color='green', icon='tree', prefix='fa')
).add_to(mapa)

folium.Marker(
    location=[pe_center_lat, pe_center_lon],
    popup=folium.Popup(savi_info, max_width=400),
    tooltip='SAVI - Parque Estadual',
    icon=folium.Icon(color='blue', icon='pagelines', prefix='fa')
).add_to(mapa)

folium.Marker(
    location=[pe_center_lat + 0.005, pe_center_lon + 0.005],
    popup=folium.Popup(arvi_info, max_width=400),
    tooltip='ARVI - Parque Estadual',
    icon=folium.Icon(color='blue', icon='cloud', prefix='fa')
).add_to(mapa)

# Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

# Adicionar título
title_html = '''
<div style="position: fixed; top: 10px; left: 50px; z-index: 1000; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 8px; font-family: Arial; box-shadow: 0 2px 8px rgba(0,0,0,0.2); max-width: 300px;">
    <h3 style="margin: 0 0 8px 0; color: #2c3e50; font-size: 16px;">🌿 Índices de Vegetação</h3>
    <p style="margin: 0; font-size: 12px; color: #7f8c8d; line-height: 1.4;">
        <b>🟢 Verde:</b> Parque Nacional<br>
        <b>🔵 Azul:</b> Parque Estadual<br>
        <i>Clique nos marcadores para ver os índices</i>
    </p>
</div>
'''
mapa.get_root().html.add_child(folium.Element(title_html))

mapa.save('mapa_indices_parques.html')
print("Mapa focado nos parques criado: mapa_indices_parques.html")
print("Agora os índices estão localizados corretamente nos parques!")