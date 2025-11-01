"""
Script para baixar imagens Landsat de múltiplas datas usando Earth Engine Data Catalog
Focado na região dos Parques Nacional São Joaquim e Estadual Serra Furada
"""

import ee
import os
from datetime import datetime, timedelta

# Inicializar Earth Engine (requer autenticação)
try:
    ee.Initialize()
except:
    print("Tentando autenticar no Google Earth Engine...")
    ee.Authenticate()
    ee.Initialize()

# Definir área de interesse (bounding box dos parques)
# Coordenadas aproximadas da região dos parques em SC
aoi = ee.Geometry.Rectangle([
    -49.7, -28.3,  # [lon_min, lat_min]
    -49.3, -28.0   # [lon_max, lat_max]
])

# Definir períodos para download (últimos 5 anos, uma imagem por ano)
periodos = [
    ('2020-06-01', '2020-08-31', '2020'),  # Verão austral
    ('2021-06-01', '2021-08-31', '2021'),
    ('2022-06-01', '2022-08-31', '2022'),
    ('2023-06-01', '2023-08-31', '2023'),
    ('2024-06-01', '2024-08-31', '2024'),
]

def baixar_imagem_landsat(inicio, fim, ano):
    """
    Baixa a melhor imagem Landsat 8/9 do período especificado
    """
    print(f"\n{'='*60}")
    print(f"Buscando imagens para o período: {ano} ({inicio} a {fim})")
    print(f"{'='*60}")
    
    # Buscar coleção Landsat 8/9 (Surface Reflectance)
    colecao = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterBounds(aoi) \
        .filterDate(inicio, fim) \
        .filter(ee.Filter.lt('CLOUD_COVER', 20))  # Menos de 20% de nuvens
    
    # Verificar se há imagens disponíveis
    count = colecao.size().getInfo()
    print(f"Imagens encontradas: {count}")
    
    if count == 0:
        print(f"❌ Nenhuma imagem encontrada para {ano}")
        return None
    
    # Selecionar a imagem com menor cobertura de nuvens
    imagem = colecao.sort('CLOUD_COVER').first()
    
    # Obter informações da imagem
    info = imagem.getInfo()
    cloud_cover = info['properties']['CLOUD_COVER']
    date = info['properties']['DATE_ACQUIRED']
    scene_id = info['properties']['LANDSAT_SCENE_ID']
    
    print(f"\n✅ Melhor imagem selecionada:")
    print(f"   Data: {date}")
    print(f"   Cobertura de nuvens: {cloud_cover:.2f}%")
    print(f"   Scene ID: {scene_id}")
    
    # Selecionar bandas necessárias (Red, NIR, Blue, SWIR)
    # Landsat 8/9 Surface Reflectance bands:
    # SR_B2 = Blue, SR_B3 = Green, SR_B4 = Red, SR_B5 = NIR, SR_B6 = SWIR1
    bandas = ['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6']
    imagem_bandas = imagem.select(bandas)
    
    # Aplicar escala (Landsat Collection 2 Surface Reflectance)
    def aplicar_escala(img):
        optical = img.select('SR_B.*').multiply(0.0000275).add(-0.2)
        return img.addBands(optical, None, True)
    
    imagem_scaled = aplicar_escala(imagem_bandas)
    
    # Calcular índices de vegetação
    ndvi = imagem_scaled.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    
    # EVI = 2.5 * ((NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1))
    evi = imagem_scaled.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
        {
            'NIR': imagem_scaled.select('SR_B5'),
            'RED': imagem_scaled.select('SR_B4'),
            'BLUE': imagem_scaled.select('SR_B2')
        }
    ).rename('EVI')
    
    # SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L), onde L = 0.5
    savi = imagem_scaled.expression(
        '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
        {
            'NIR': imagem_scaled.select('SR_B5'),
            'RED': imagem_scaled.select('SR_B4')
        }
    ).rename('SAVI')
    
    # ARVI = (NIR - (2*Red - Blue)) / (NIR + (2*Red - Blue))
    arvi = imagem_scaled.expression(
        '(NIR - (2 * RED - BLUE)) / (NIR + (2 * RED - BLUE))',
        {
            'NIR': imagem_scaled.select('SR_B5'),
            'RED': imagem_scaled.select('SR_B4'),
            'BLUE': imagem_scaled.select('SR_B2')
        }
    ).rename('ARVI')
    
    # Combinar todos os índices
    indices = ndvi.addBands([evi, savi, arvi])
    
    return {
        'imagem': indices,
        'data': date,
        'ano': ano,
        'cloud_cover': cloud_cover
    }

def exportar_para_drive(resultado):
    """
    Exporta a imagem para o Google Drive
    """
    if resultado is None:
        return
    
    ano = resultado['ano']
    data = resultado['data']
    imagem = resultado['imagem']
    
    # Exportar cada índice separadamente
    indices_nomes = ['NDVI', 'EVI', 'SAVI', 'ARVI']
    
    for indice in indices_nomes:
        task = ee.batch.Export.image.toDrive(
            image=imagem.select(indice),
            description=f'{indice}_{ano}',
            folder='PELD_Landsat_Temporal',
            fileNamePrefix=f'{indice}_{data}',
            region=aoi,
            scale=30,  # Resolução de 30m
            crs='EPSG:4326',
            maxPixels=1e9
        )
        
        task.start()
        print(f"📤 Exportando {indice} para Google Drive...")
        print(f"   Nome do arquivo: {indice}_{data}.tif")

def main():
    """
    Função principal
    """
    print("\n" + "="*60)
    print("   DOWNLOAD DE IMAGENS LANDSAT - ANÁLISE TEMPORAL PELD")
    print("="*60)
    print("\n📍 Área de interesse: Parques de Santa Catarina")
    print("🛰️  Satélite: Landsat 8/9 (Surface Reflectance)")
    print("📊 Índices: NDVI, EVI, SAVI, ARVI")
    print("⏰ Período: 2020-2024\n")
    
    resultados = []
    
    # Processar cada período
    for inicio, fim, ano in periodos:
        resultado = baixar_imagem_landsat(inicio, fim, ano)
        if resultado:
            resultados.append(resultado)
            exportar_para_drive(resultado)
    
    print(f"\n{'='*60}")
    print(f"✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"{'='*60}")
    print(f"\nTotal de imagens processadas: {len(resultados)}")
    print("\n📂 As imagens estão sendo exportadas para o Google Drive")
    print("   Pasta: PELD_Landsat_Temporal")
    print("\n⚠️  IMPORTANTE: Acesse https://code.earthengine.google.com/tasks")
    print("   para monitorar o progresso das exportações.")
    
    # Resumo
    print("\n📋 RESUMO:")
    for r in resultados:
        print(f"   {r['ano']}: {r['data']} (nuvens: {r['cloud_cover']:.1f}%)")

if __name__ == "__main__":
    main()
