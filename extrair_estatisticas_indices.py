"""
Script simplificado para extrair estatísticas dos índices de vegetação
e criar visualizações temporais com dados reais dos parques
"""

import rasterio
import numpy as np
from rasterio.mask import mask
import geopandas as gpd
import json
import os

print("\n" + "="*70)
print("   EXTRAÇÃO DE ESTATÍSTICAS TEMPORAIS - PELD SC")
print("="*70)

# Caminhos
pasta_indices = r"Indice_vegetacao"
parque_nacional = r"PROJETO_PELDSC\PARNA_SAO_JOAQUIM_SHP\PARNA SAO JOAQUIM SHP\PARNASJlimites.shp"
parque_estadual = r"Projeto_PARNA_PESF\PARQUE_PESF_1_temp.shp"

# Verificar arquivos
print("\n📂 Verificando arquivos...")

indices_disponiveis = {}
for arquivo in ["NDVI_Landsat8_2025.tif", "EVI_2025_06_25.tif"]:
    caminho = os.path.join(pasta_indices, arquivo)
    if os.path.exists(caminho):
        nome = arquivo.split('_')[0]
        indices_disponiveis[nome] = caminho
        print(f"   ✅ {nome} encontrado")

if not indices_disponiveis:
    print("   ❌ Nenhum índice encontrado!")
    exit(1)

# Carregar shapefiles dos parques
print("\n🏞️  Carregando limites dos parques...")

try:
    gdf_pn = gpd.read_file(parque_nacional)
    gdf_pn = gdf_pn.to_crs("EPSG:32622")  # Converter para mesma projeção das imagens
    print(f"   ✅ Parque Nacional São Joaquim carregado")
except Exception as e:
    print(f"   ❌ Erro ao carregar PNSJ: {e}")
    gdf_pn = None

try:
    gdf_pe = gpd.read_file(parque_estadual)
    gdf_pe = gdf_pe.to_crs("EPSG:32622")
    print(f"   ✅ Parque Estadual Serra Furada carregado")
except Exception as e:
    print(f"   ❌ Erro ao carregar PESF: {e}")
    gdf_pe = None

def extrair_estatisticas_parque(raster_path, geometria, nome_parque):
    """
    Extrai estatísticas de um índice para uma área específica
    """
    try:
        with rasterio.open(raster_path) as src:
            # Recortar raster pela geometria do parque
            out_image, out_transform = mask(src, [geometria], crop=True, nodata=np.nan)
            data = out_image[0]
            
            # Remover valores inválidos
            data_valido = data[(data != src.nodata) & (~np.isnan(data))]
            
            if len(data_valido) == 0:
                return None
            
            # Calcular estatísticas
            estatisticas = {
                'parque': nome_parque,
                'media': float(np.mean(data_valido)),
                'mediana': float(np.median(data_valido)),
                'desvio_padrao': float(np.std(data_valido)),
                'minimo': float(np.min(data_valido)),
                'maximo': float(np.max(data_valido)),
                'pixels': len(data_valido)
            }
            
            return estatisticas
    except Exception as e:
        print(f"      ⚠️  Erro ao processar {nome_parque}: {e}")
        return None

# Processar cada índice
resultados = {}

for indice_nome, indice_path in indices_disponiveis.items():
    print(f"\n{'─'*70}")
    print(f"📊 Processando {indice_nome}")
    print(f"{'─'*70}")
    
    resultados[indice_nome] = {}
    
    # Processar Parque Nacional
    if gdf_pn is not None:
        print(f"\n   Analisando Parque Nacional São Joaquim...")
        geom_pn = gdf_pn.geometry.iloc[0]
        stats_pn = extrair_estatisticas_parque(indice_path, geom_pn, "PNSJ")
        
        if stats_pn:
            resultados[indice_nome]['PNSJ'] = stats_pn
            print(f"      ✅ Média: {stats_pn['media']:.3f}")
            print(f"      📊 Min: {stats_pn['minimo']:.3f}, Max: {stats_pn['maximo']:.3f}")
            print(f"      📏 Pixels analisados: {stats_pn['pixels']:,}")
    
    # Processar Parque Estadual
    if gdf_pe is not None:
        print(f"\n   Analisando Parque Estadual Serra Furada...")
        geom_pe = gdf_pe.unary_union  # Unir todas as zonas
        stats_pe = extrair_estatisticas_parque(indice_path, geom_pe, "PESF")
        
        if stats_pe:
            resultados[indice_nome]['PESF'] = stats_pe
            print(f"      ✅ Média: {stats_pe['media']:.3f}")
            print(f"      📊 Min: {stats_pe['minimo']:.3f}, Max: {stats_pe['maximo']:.3f}")
            print(f"      📏 Pixels analisados: {stats_pe['pixels']:,}")

# Salvar resultados
print(f"\n{'='*70}")
print("   💾 SALVANDO RESULTADOS")
print(f"{'='*70}")

output_file = "estatisticas_indices_2025.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print(f"\n✅ Estatísticas salvas em: {output_file}")

# Exibir resumo
print(f"\n{'='*70}")
print("   📊 RESUMO GERAL")
print(f"{'='*70}")

for indice, parques in resultados.items():
    print(f"\n🌿 {indice}:")
    for parque, stats in parques.items():
        interpretacao = ""
        if indice == "NDVI":
            if stats['media'] > 0.7:
                interpretacao = "🟢 Vegetação densa e saudável"
            elif stats['media'] > 0.4:
                interpretacao = "🟡 Vegetação moderada"
            else:
                interpretacao = "🔴 Vegetação esparsa/estresse"
        elif indice == "EVI":
            if stats['media'] > 0.5:
                interpretacao = "🟢 Cobertura vegetal excelente"
            elif stats['media'] > 0.3:
                interpretacao = "🟡 Cobertura vegetal boa"
            else:
                interpretacao = "🔴 Cobertura vegetal baixa"
        
        print(f"   • {parque}: {stats['media']:.3f} ± {stats['desvio_padrao']:.3f} {interpretacao}")

print(f"\n{'='*70}")
print("✅ Processamento concluído com sucesso!")
print(f"{'='*70}")

print("\n💡 Próximos passos:")
print("   1. Use estes dados para criar série temporal simulada")
print("   2. Execute gerar_visualizacoes_temporais.py para mapas interativos")
print("   3. Publique no GitHub Pages")
