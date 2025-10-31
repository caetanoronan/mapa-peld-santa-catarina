import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import shape
import json

# Ler o MDE
with rasterio.open('Projeto_PARNA_PESF/MDE_Completo_Cidades.tif') as src:
    data = src.read(1)
    transform = src.transform
    crs = src.crs

    # Filtrar valores válidos (remover NoData)
    valid_mask = (data > -1000) & (data < 10000)  # Valores razoáveis de elevação
    valid_data = data[valid_mask]

    print('Dados válidos - Min:', valid_data.min(), 'Max:', valid_data.max())

    # Criar contornos de elevação
    levels = np.arange(800, 1800, 100)  # Contornos a cada 100m

    # Usar matplotlib para gerar contornos
    fig, ax = plt.subplots(figsize=(10, 10))
    cs = ax.contour(data, levels=levels, extent=[src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top])

    # Converter contornos para GeoJSON
    contours_geojson = {'type': 'FeatureCollection', 'features': []}

    for i, (level, collection) in enumerate(zip(levels, cs.collections)):
        print(f"Processando nível {level}m...")
        for path in collection.get_paths():
            if len(path.vertices) > 2:  # Apenas contornos com pontos suficientes
                # Converter coordenadas do raster para coordenadas geográficas
                coords = []
                for vertex in path.vertices:
                    # Transformar coordenadas do pixel para coordenadas geográficas
                    x, y = rasterio.transform.xy(transform, vertex[1], vertex[0])
                    coords.append([x, y])

                if len(coords) > 2:
                    feature = {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': coords
                        },
                        'properties': {
                            'elevation': int(level),
                            'unit': 'meters'
                        }
                    }
                    contours_geojson['features'].append(feature)

    # Salvar como GeoJSON
    with open('contornos_altimetria.geojson', 'w') as f:
        json.dump(contours_geojson, f)

    print(f'Contornos criados: {len(contours_geojson["features"])} features')
    print('GeoJSON salvo como contornos_altimetria.geojson')

    # Converter para WGS84 se necessário
    if crs != 'EPSG:4326':
        gdf_contours = gpd.GeoDataFrame.from_features(contours_geojson['features'])
        gdf_contours.crs = crs
        gdf_contours = gdf_contours.to_crs('EPSG:4326')
        contours_wgs84 = gdf_contours.__geo_interface__
        with open('contornos_altimetria_wgs84.geojson', 'w') as f:
            json.dump(contours_wgs84, f)
        print('GeoJSON convertido para WGS84 salvo como contornos_altimetria_wgs84.geojson')