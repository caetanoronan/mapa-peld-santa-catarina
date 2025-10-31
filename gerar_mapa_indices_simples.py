import geopandas as gpd
import folium
import pandas as pd
import rasterio
import numpy as np
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Carregar dados básicos
df = pd.read_csv('amb_csv/ppbio_sc-coordenadas_parcelas.csv', encoding='latin1', sep=';')

# Converter shapefiles
try:
    gdf_parque_nacional = gpd.read_file('PROJETO_PELDSC/PARNA_SAO_JOAQUIM_SHP/PARNA SAO JOAQUIM SHP/PARNASJlimites.shp')
    gdf_parque_nacional = gdf_parque_nacional.to_crs(epsg=4326)
    parque_nacional_geojson = 'parque_nacional_sj.geojson'
    gdf_parque_nacional.to_file(parque_nacional_geojson, driver='GeoJSON')
except:
    parque_nacional_geojson = None

try:
    gdf_parque_estadual = gpd.read_file('Projeto_PARNA_PESF/PARQUE_PESF_1_temp.shp')
    gdf_parque_estadual = gdf_parque_estadual.to_crs(epsg=4326)
    parque_estadual_geojson = 'parque_estadual_serra_furada.geojson'
    gdf_parque_estadual.to_file(parque_estadual_geojson, driver='GeoJSON')
except:
    parque_estadual_geojson = None

try:
    gdf_cidades = gpd.read_file('Projeto_PARNA_PESF/Cidades_parna_sj_temp.shp')
    gdf_cidades = gdf_cidades.to_crs(epsg=4326)
    cidades_geojson = 'cidades_afetadas.geojson'
    gdf_cidades.to_file(cidades_geojson, driver='GeoJSON')
except:
    cidades_geojson = None

try:
    gdf_estado = gpd.read_file('Organizacao Territorio/SC_UF_2024/SC_UF_2024.shp')
    gdf_estado = gdf_estado.to_crs(epsg=4326)
    estado_geojson = 'limite_santa_catarina.geojson'
    gdf_estado.to_file(estado_geojson, driver='GeoJSON')
except:
    estado_geojson = None

# Criar mapa base
mapa = folium.Map(location=[df['lat'].mean(), df['long'].mean()], zoom_start=10, min_zoom=8, max_zoom=18)

# Adicionar camada de relevo
folium.TileLayer(
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attr='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    name='Relevo (OpenTopoMap)',
    overlay=False
).add_to(mapa)

# Função para criar visualização simplificada de índice
def criar_visualizacao_indice(file_path, titulo, colormap='RdYlGn'):
    try:
        with rasterio.open(file_path) as src:
            # Ler uma amostra dos dados (para performance)
            data = src.read(1, out_shape=(src.height // 10, src.width // 10),
                          resampling=rasterio.enums.Resampling.bilinear)

            # Filtrar valores válidos
            if 'NDVI' in file_path:
                mask = (data >= -1) & (data <= 1)
            elif 'EVI' in file_path:
                mask = (data >= -1) & (data <= 2)
            elif 'SAVI' in file_path:
                mask = (data >= -1) & (data <= 1.5)
            else:
                mask = data != src.nodata if src.nodata else np.ones_like(data, dtype=bool)

            data_masked = np.ma.masked_array(data, ~mask)

            # Criar figura matplotlib
            fig, ax = plt.subplots(figsize=(8, 6))
            im = ax.imshow(data_masked, cmap=colormap, vmin=data_masked.min(), vmax=data_masked.max())
            ax.set_title(f'{titulo}\nValores: {data_masked.min():.3f} a {data_masked.max():.3f}')
            ax.axis('off')

            # Adicionar colorbar
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.set_label('Valor do Índice')

            # Converter para base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            plt.close()

            # Calcular bounds aproximados (WGS84)
            bounds = src.bounds
            # Conversão aproximada UTM 22S -> WGS84
            left = -51.8 + (bounds.left - 400000) / 90000
            right = -51.8 + (bounds.right - 400000) / 90000
            bottom = -29.8 + (bounds.bottom - 6700000) / 90000
            top = -29.8 + (bounds.top - 6700000) / 90000

            image_bounds = [[bottom, left], [top, right]]

            return image_base64, image_bounds

    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return None, None

# Adicionar índices de vegetação como camadas
indices = [
    ('Projeto_PARNA_PESF/NDVI.tif', 'NDVI (Vegetação)', 'RdYlGn'),
    ('Projeto_PARNA_PESF/EVI_.tif', 'EVI (Cobertura Densa)', 'viridis'),
    ('Projeto_PARNA_PESF/SAVI.tif', 'SAVI (Solo Ajustado)', 'plasma'),
    ('Projeto_PARNA_PESF/ARVI_Calculado.tif', 'ARVI (Atmosfera)', 'inferno')
]

for file_path, titulo, colormap in indices:
    image_b64, bounds = criar_visualizacao_indice(file_path, titulo, colormap)
    if image_b64 and bounds:
        # Criar HTML para a imagem
        image_html = f'<img src="data:image/png;base64,{image_b64}" style="max-width:100%; max-height:400px;">'

        # Adicionar como popup em um marcador central
        center_lat = (bounds[0][0] + bounds[1][0]) / 2
        center_lon = (bounds[0][1] + bounds[1][1]) / 2

        folium.Marker(
            location=[center_lat, center_lon],
            popup=folium.Popup(image_html, max_width=600),
            tooltip=titulo,
            icon=folium.Icon(color='green', icon='leaf')
        ).add_to(mapa)

# Adicionar camadas vetoriais
if parque_nacional_geojson:
    folium.GeoJson(parque_nacional_geojson, name='Parque Nacional de São Joaquim',
                   style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'weight': 3, 'fillOpacity': 0.1}).add_to(mapa)

if parque_estadual_geojson:
    folium.GeoJson(parque_estadual_geojson, name='Parque Estadual da Serra Furada',
                   style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'weight': 2, 'fillOpacity': 0.1}).add_to(mapa)

if cidades_geojson:
    folium.GeoJson(cidades_geojson, name='Cidades Afetadas pelo PARNA',
                   style_function=lambda x: {'fillColor': 'orange', 'color': 'red', 'weight': 1, 'fillOpacity': 0.3},
                   tooltip=folium.GeoJsonTooltip(fields=['NM_MUN', 'AREA_KM2'], aliases=['Cidade:', 'Área (km²):'])).add_to(mapa)

if estado_geojson:
    folium.GeoJson(estado_geojson, name='Limite Estadual de Santa Catarina',
                   style_function=lambda x: {'fillColor': 'none', 'color': 'black', 'weight': 4, 'fillOpacity': 0}).add_to(mapa)

# Adicionar marcadores das parcelas
terrestre_group = folium.FeatureGroup(name='Parcelas Terrestres', show=True)
riparia_group = folium.FeatureGroup(name='Parcelas Ripárias', show=True)

for idx, row in df.iterrows():
    popup_text = f"""
    <b>Módulo:</b> {row['module']}<br>
    <b>Nome:</b> {row['name']}<br>
    <b>Tipo:</b> {row['type']}<br>
    <b>Latitude:</b> {row['lat']}<br>
    <b>Longitude:</b> {row['long']}
    """
    marker = folium.Marker(
        location=[row['lat'], row['long']],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color='blue' if row['type'] == 'Terrestre' else 'green')
    )
    if row['type'] == 'Terrestre':
        marker.add_to(terrestre_group)
    else:
        marker.add_to(riparia_group)

terrestre_group.add_to(mapa)
riparia_group.add_to(mapa)

# Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

# Adicionar título
title_html = '''
<div style="position: fixed; top: 10px; left: 50px; z-index: 1000; background: rgba(255,255,255,0.8); padding: 10px; border-radius: 5px; font-family: Arial;">
    <h3 style="margin: 0; color: #2c3e50;">📊 Mapa PELD - Índices de Vegetação</h3>
    <p style="margin: 5px 0 0 0; font-size: 12px; color: #7f8c8d;">Clique nos marcadores verdes para ver os índices</p>
</div>
'''
mapa.get_root().html.add_child(folium.Element(title_html))

mapa.save('mapa_indices_vegetacao.html')
print("Mapa com índices de vegetação criado: mapa_indices_vegetacao.html")
print("Clique nos marcadores verdes para visualizar os índices NDVI, EVI, SAVI e ARVI")