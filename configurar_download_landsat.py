"""
Script para baixar imagens Landsat de múltiplas datas usando métodos alternativos
Opções: Microsoft Planetary Computer, USGS EarthExplorer, AWS Open Data

Este script usa a biblioteca 'landsatxplore' que facilita o download do USGS
"""

import os
from datetime import datetime, timedelta

print("\n" + "="*70)
print("   DOWNLOAD DE IMAGENS LANDSAT - MÉTODOS ALTERNATIVOS")
print("="*70)

print("\n📋 OPÇÕES DISPONÍVEIS:")
print("\n1️⃣  USGS EarthExplorer (landsatxplore)")
print("   • Acesso direto ao catálogo USGS")
print("   • Requer conta gratuita no earthexplorer.usgs.gov")
print("   • Simples de usar via Python")

print("\n2️⃣  Microsoft Planetary Computer")
print("   • Acesso via API STAC")
print("   • Não requer autenticação para leitura")
print("   • Bom para análises em nuvem")

print("\n3️⃣  AWS Open Data Registry")
print("   • Landsat em buckets S3 públicos")
print("   • Download direto via boto3")
print("   • Requer conhecimento da estrutura de paths")

print("\n" + "─"*70)
print("MÉTODO RECOMENDADO: landsatxplore (USGS)")
print("─"*70)

# Verificar se landsatxplore está instalado
try:
    import landsatxplore.api
    print("\n✅ landsatxplore já está instalado")
except ImportError:
    print("\n📦 Instalando landsatxplore...")
    os.system("python -m pip install landsatxplore")
    print("✅ landsatxplore instalado com sucesso!")

print("\n" + "="*70)
print("   CONFIGURAÇÃO NECESSÁRIA")
print("="*70)

print("\n📝 Para usar o USGS EarthExplorer, você precisa:")
print("\n1. Criar conta gratuita em: https://earthexplorer.usgs.gov/register")
print("2. Anotar seu username e password")
print("3. Executar este script novamente com suas credenciais")

print("\n💡 EXEMPLO DE USO:")
print("""
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer

# Conectar à API
api = API('seu_username', 'sua_senha')

# Buscar cenas
scenes = api.search(
    dataset='landsat_ot_c2_l2',  # Landsat 8/9 Collection 2 Level 2
    latitude=-28.125,
    longitude=-49.533,
    start_date='2020-06-01',
    end_date='2024-12-31',
    max_cloud_cover=20
)

print(f"Encontradas {len(scenes)} cenas")

# Download
ee = EarthExplorer('seu_username', 'sua_senha')
for scene in scenes[:5]:  # Baixar 5 primeiras
    ee.download(scene['entity_id'], output_dir='./landsat_temporal')

ee.logout()
api.logout()
""")

# Criar script auxiliar para quando o usuário tiver credenciais
script_download = """'''
Script de Download Automático - Landsat Temporal
Execute este script após criar conta no USGS EarthExplorer
'''

from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
import os

# CONFIGURAÇÃO: Substitua com suas credenciais
USERNAME = 'seu_username_aqui'
PASSWORD = 'sua_senha_aqui'

# Área de interesse (Parques SC)
LATITUDE = -28.125
LONGITUDE = -49.533

# Períodos desejados
PERIODOS = [
    ('2020-06-01', '2020-08-31'),
    ('2021-06-01', '2021-08-31'),
    ('2022-06-01', '2022-08-31'),
    ('2023-06-01', '2023-08-31'),
    ('2024-06-01', '2024-08-31'),
]

print("\\n" + "="*70)
print("   DOWNLOAD AUTOMÁTICO DE IMAGENS LANDSAT")
print("="*70)

# Conectar à API
print("\\n🔐 Conectando ao USGS...")
try:
    api = API(USERNAME, PASSWORD)
    print("✅ Conectado com sucesso!")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
    print("\\n💡 Verifique suas credenciais e tente novamente")
    exit(1)

# Criar diretório de saída
output_dir = './landsat_temporal_download'
os.makedirs(output_dir, exist_ok=True)

todas_cenas = []

# Buscar cenas para cada período
for inicio, fim in PERIODOS:
    print(f"\\n📅 Buscando imagens: {inicio} a {fim}")
    
    try:
        scenes = api.search(
            dataset='landsat_ot_c2_l2',  # Landsat 8/9 Collection 2 Level 2
            latitude=LATITUDE,
            longitude=LONGITUDE,
            start_date=inicio,
            end_date=fim,
            max_cloud_cover=20  # Máximo 20% de nuvens
        )
        
        if scenes:
            # Pegar a cena com menor cobertura de nuvens
            melhor = min(scenes, key=lambda x: x['cloud_cover'])
            todas_cenas.append(melhor)
            print(f"   ✅ Encontrada: {melhor['display_id']}")
            print(f"      Data: {melhor['acquisition_date']}")
            print(f"      Nuvens: {melhor['cloud_cover']:.1f}%")
        else:
            print(f"   ⚠️  Nenhuma imagem encontrada para este período")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")

print(f"\\n{'='*70}")
print(f"   TOTAL: {len(todas_cenas)} imagens selecionadas")
print(f"{'='*70}")

if not todas_cenas:
    print("\\n❌ Nenhuma imagem disponível para download")
    api.logout()
    exit(0)

# Perguntar se deseja baixar
print(f"\\n📥 Deseja baixar estas {len(todas_cenas)} imagens?")
print("   (Tamanho estimado: ~1-2 GB por imagem)")
resposta = input("   Digite 'sim' para continuar: ").strip().lower()

if resposta != 'sim':
    print("\\n❌ Download cancelado")
    api.logout()
    exit(0)

# Download
print(f"\\n{'='*70}")
print("   INICIANDO DOWNLOADS")
print(f"{'='*70}")

ee = EarthExplorer(USERNAME, PASSWORD)

for i, scene in enumerate(todas_cenas, 1):
    print(f"\\n[{i}/{len(todas_cenas)}] Baixando: {scene['display_id']}")
    try:
        ee.download(scene['entity_id'], output_dir=output_dir)
        print(f"   ✅ Download concluído!")
    except Exception as e:
        print(f"   ❌ Erro no download: {e}")

ee.logout()
api.logout()

print(f"\\n{'='*70}")
print("   ✅ PROCESSO CONCLUÍDO!")
print(f"{'='*70}")
print(f"\\n📂 Imagens salvas em: {os.path.abspath(output_dir)}")
print("\\n💡 Próximo passo: Processar as imagens baixadas para extrair índices")
'''
"""

# Salvar script auxiliar
with open('baixar_landsat_usgs.py', 'w', encoding='utf-8') as f:
    f.write(script_download)

print("\n" + "="*70)
print("   ✅ SCRIPT AUXILIAR CRIADO")
print("="*70)

print(f"\n📄 Script salvo: baixar_landsat_usgs.py")
print("\n📋 PRÓXIMOS PASSOS:")
print("\n1. Crie conta em: https://earthexplorer.usgs.gov/register")
print("2. Edite 'baixar_landsat_usgs.py' e adicione suas credenciais")
print("3. Execute: python baixar_landsat_usgs.py")
print("4. Aguarde o download das imagens")
print("5. Processe as imagens com scripts de índices")

print("\n⏱️  TEMPO ESTIMADO:")
print("   • Registro: 2-5 minutos")
print("   • Download: 10-30 minutos (depende da conexão)")
print("   • Processamento: 5-15 minutos")

print("\n🎯 ALTERNATIVA RÁPIDA:")
print("   Se preferir, use os dados simulados já criados!")
print("   Os mapas temporais já estão funcionando com dados realistas.")

print("\n" + "="*70)
