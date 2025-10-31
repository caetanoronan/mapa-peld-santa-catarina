import geopandas as gpd
import folium
import pandas as pd
from folium.plugins import MarkerCluster

# Carregar os dados do CSV
df = pd.read_csv('amb_csv/ppbio_sc-coordenadas_parcelas.csv', encoding='latin1', sep=';')

# Converter shapefiles para GeoJSON
try:
    gdf_parque_nacional = gpd.read_file('PROJETO_PELDSC/PARNA_SAO_JOAQUIM_SHP/PARNA SAO JOAQUIM SHP/PARNASJlimites.shp')
    gdf_parque_nacional = gdf_parque_nacional.to_crs(epsg=4326)  # Garantir WGS84
    parque_nacional_geojson = 'parque_nacional_sj.geojson'
    gdf_parque_nacional.to_file(parque_nacional_geojson, driver='GeoJSON')
    print("Shapefile do Parque Nacional de São Joaquim convertido para GeoJSON")
except Exception as e:
    print(f"Erro ao converter shapefile do Parque Nacional: {e}")
    parque_nacional_geojson = None

try:
    gdf_parque_estadual = gpd.read_file('Projeto_PARNA_PESF/PARQUE_PESF_1_temp.shp')
    gdf_parque_estadual = gdf_parque_estadual.to_crs(epsg=4326)  # Garantir WGS84
    parque_estadual_geojson = 'parque_estadual_serra_furada.geojson'
    gdf_parque_estadual.to_file(parque_estadual_geojson, driver='GeoJSON')
    print("Shapefile do Parque Estadual da Serra Furada convertido para GeoJSON")
except Exception as e:
    print(f"Erro ao converter shapefile do Parque Estadual: {e}")
    parque_estadual_geojson = None

try:
    gdf_cidades = gpd.read_file('Projeto_PARNA_PESF/Cidades_parna_sj_temp.shp')
    gdf_cidades = gdf_cidades.to_crs(epsg=4326)  # Garantir WGS84
    cidades_geojson = 'cidades_afetadas.geojson'
    gdf_cidades.to_file(cidades_geojson, driver='GeoJSON')
    print("Shapefile das cidades convertido para GeoJSON")
except Exception as e:
    print(f"Erro ao converter shapefile das cidades: {e}")
    cidades_geojson = None

try:
    gdf_estado = gpd.read_file('Organizacao Territorio/SC_UF_2024/SC_UF_2024.shp')
    gdf_estado = gdf_estado.to_crs(epsg=4326)  # Garantir WGS84
    estado_geojson = 'limite_santa_catarina.geojson'
    gdf_estado.to_file(estado_geojson, driver='GeoJSON')
    print("Shapefile do limite estadual de Santa Catarina convertido para GeoJSON")
except Exception as e:
    print(f"Erro ao converter shapefile do limite estadual: {e}")
    estado_geojson = None

# Criar mapa centrado na média das coordenadas
mapa = folium.Map(location=[df['lat'].mean(), df['long'].mean()], zoom_start=10, min_zoom=8, max_zoom=18)

# Adicionar camada do parque nacional se disponível
if parque_nacional_geojson:
    folium.GeoJson(parque_nacional_geojson, name='Parque Nacional de São Joaquim', 
                   style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'weight': 3, 'fillOpacity': 0.1}).add_to(mapa)

# Adicionar camada do parque estadual se disponível
if parque_estadual_geojson:
    folium.GeoJson(parque_estadual_geojson, name='Parque Estadual da Serra Furada', 
                   style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'weight': 2, 'fillOpacity': 0.1}).add_to(mapa)

# Adicionar camada das cidades afetadas se disponível
if cidades_geojson:
    folium.GeoJson(cidades_geojson, name='Cidades Afetadas pelo PARNA',
                   style_function=lambda x: {'fillColor': 'orange', 'color': 'red', 'weight': 1, 'fillOpacity': 0.3},
                   tooltip=folium.GeoJsonTooltip(fields=['NM_MUN', 'AREA_KM2'], aliases=['Cidade:', 'Área (km²):'])).add_to(mapa)

# Adicionar camada do limite estadual se disponível
if estado_geojson:
    folium.GeoJson(estado_geojson, name='Limite Estadual de Santa Catarina',
                   style_function=lambda x: {'fillColor': 'none', 'color': 'black', 'weight': 4, 'fillOpacity': 0}).add_to(mapa)

# Criar grupos de marcadores
terrestre_group = folium.FeatureGroup(name='Parcelas Terrestres', show=True)
riparia_group = folium.FeatureGroup(name='Parcelas Ripárias', show=True)

# Adicionar marcadores agrupados
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

# Adicionar grupos ao mapa
terrestre_group.add_to(mapa)
riparia_group.add_to(mapa)

# Adicionar controle de camadas
folium.LayerControl().add_to(mapa)

# Título será adicionado manualmente no HTML após geração

# Salvar o mapa
mapa.save('mapa_interativo_peld.html')
print("Mapa PELD criado: mapa_interativo_peld.html")