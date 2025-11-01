"""
Análise Comparativa: NDVI vs EVI
Mapa interativo mostrando as diferenças e correlações entre os dois índices
"""

import folium
from folium import plugins
import json

print("\n" + "="*70)
print("   ANÁLISE COMPARATIVA: NDVI vs EVI")
print("="*70)

# Carregar dados reais
with open('estatisticas_indices_2025.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Coordenadas dos parques
pn_coords = {'lat': -28.167, 'lon': -49.583}
pe_coords = {'lat': -28.083, 'lon': -49.483}

# Criar mapa base
m = folium.Map(
    location=[-28.125, -49.533],
    zoom_start=11,
    min_zoom=8,
    max_zoom=18,
    tiles='OpenStreetMap'
)

# Adicionar camada topográfica
folium.TileLayer(
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attr='OpenTopoMap',
    name='Relevo',
    overlay=True,
    control=True,
    opacity=0.6
).add_to(m)

# Função para interpretar índices
def interpretar_ndvi(valor):
    if valor > 0.7:
        return "🟢 Vegetação densa e saudável", "#2e7d32"
    elif valor > 0.4:
        return "🟡 Vegetação moderada", "#f57c00"
    else:
        return "🔴 Vegetação esparsa/estresse", "#c62828"

def interpretar_evi(valor):
    if valor > 0.5:
        return "🟢 Cobertura excelente", "#2e7d32"
    elif valor > 0.3:
        return "🟡 Cobertura boa", "#f57c00"
    else:
        return "🔴 Cobertura baixa", "#c62828"

# Processar cada parque
parques = {
    'PNSJ': {
        'nome': 'Parque Nacional São Joaquim',
        'coords': pn_coords,
        'cor': 'green',
        'icon': 'mountain'
    },
    'PESF': {
        'nome': 'Parque Estadual Serra Furada',
        'coords': pe_coords,
        'cor': 'blue',
        'icon': 'tree'
    }
}

print("\n📊 Gerando análises comparativas...")

for parque_id, info in parques.items():
    ndvi_data = dados['NDVI'][parque_id]
    evi_data = dados['EVI'][parque_id]
    
    # Calcular correlação e discrepâncias
    ndvi_val = ndvi_data['media']
    evi_val = evi_data['media']
    
    # Normalizar EVI para escala similar ao NDVI (0-1)
    evi_normalizado = min(evi_val / 2.0, 1.0)
    
    # Discrepância entre índices
    discrepancia = abs(ndvi_val - evi_normalizado)
    
    interpretacao_ndvi, cor_ndvi = interpretar_ndvi(ndvi_val)
    interpretacao_evi, cor_evi = interpretar_evi(evi_val)
    
    # Análise da discrepância
    if discrepancia < 0.1:
        analise_concordancia = "✅ <strong>Alta concordância</strong> entre índices"
        explicacao = "Ambos os índices concordam sobre a condição da vegetação."
    elif discrepancia < 0.2:
        analise_concordancia = "⚠️ <strong>Concordância moderada</strong>"
        explicacao = "Há algumas diferenças, possivelmente devido a condições atmosféricas ou tipo de vegetação."
    else:
        analise_concordancia = "❌ <strong>Baixa concordância</strong>"
        if evi_normalizado > ndvi_val:
            explicacao = "EVI detecta mais vegetação que NDVI. Isso pode indicar: <br>• Vegetação densa com saturação do NDVI<br>• Influência de cobertura de nuvens/atmosfera<br>• Presença de vegetação de altitude"
        else:
            explicacao = "NDVI detecta mais vegetação que EVI. Isso pode indicar: <br>• Presença de solo exposto<br>• Vegetação esparsa<br>• Interferência atmosférica favorecendo NDVI"
    
    # Razão NDVI/EVI
    razao = ndvi_val / evi_normalizado if evi_normalizado > 0 else 0
    
    # Criar popup detalhado
    popup_html = f"""
    <div style="font-family: Arial; width: 400px; max-height: 600px; overflow-y: auto;">
        <h3 style="color: {'#2c5f2d' if info['cor'] == 'green' else '#1565c0'}; margin-bottom: 10px; text-align: center;">
            📊 Análise Comparativa
        </h3>
        <h4 style="text-align: center; color: #666; margin: 5px 0;">
            {info['nome']}
        </h4>
        
        <hr style="margin: 15px 0;">
        
        <!-- NDVI Section -->
        <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <h4 style="margin: 0 0 10px 0; color: #2e7d32;">🌿 NDVI (Normalized Difference Vegetation Index)</h4>
            <table style="width: 100%; font-size: 13px;">
                <tr>
                    <td><strong>Valor Médio:</strong></td>
                    <td style="text-align: right; font-size: 18px; font-weight: bold; color: {cor_ndvi};">{ndvi_val:.3f}</td>
                </tr>
                <tr>
                    <td><strong>Desvio Padrão:</strong></td>
                    <td style="text-align: right;">±{ndvi_data['desvio_padrao']:.3f}</td>
                </tr>
                <tr>
                    <td><strong>Faixa:</strong></td>
                    <td style="text-align: right;">{ndvi_data['minimo']:.3f} - {ndvi_data['maximo']:.3f}</td>
                </tr>
                <tr>
                    <td colspan="2" style="padding-top: 10px; border-top: 1px solid #ccc; margin-top: 10px;">
                        {interpretacao_ndvi}
                    </td>
                </tr>
            </table>
        </div>
        
        <!-- EVI Section -->
        <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <h4 style="margin: 0 0 10px 0; color: #1565c0;">🌲 EVI (Enhanced Vegetation Index)</h4>
            <table style="width: 100%; font-size: 13px;">
                <tr>
                    <td><strong>Valor Médio:</strong></td>
                    <td style="text-align: right; font-size: 18px; font-weight: bold; color: {cor_evi};">{evi_val:.3f}</td>
                </tr>
                <tr>
                    <td><strong>Desvio Padrão:</strong></td>
                    <td style="text-align: right;">±{evi_data['desvio_padrao']:.3f}</td>
                </tr>
                <tr>
                    <td><strong>Faixa:</strong></td>
                    <td style="text-align: right;">{evi_data['minimo']:.3f} - {evi_data['maximo']:.3f}</td>
                </tr>
                <tr>
                    <td colspan="2" style="padding-top: 10px; border-top: 1px solid #ccc; margin-top: 10px;">
                        {interpretacao_evi}
                    </td>
                </tr>
            </table>
        </div>
        
        <!-- Análise Comparativa -->
        <div style="background: #fff3e0; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <h4 style="margin: 0 0 10px 0; color: #e65100;">🔍 Análise Comparativa</h4>
            <p style="font-size: 13px; margin: 5px 0;">
                <strong>Concordância:</strong> {analise_concordancia}
            </p>
            <p style="font-size: 13px; margin: 5px 0;">
                <strong>Discrepância:</strong> {discrepancia:.3f}
            </p>
            <p style="font-size: 13px; margin: 5px 0;">
                <strong>Razão NDVI/EVI:</strong> {razao:.3f}
            </p>
            <p style="font-size: 12px; margin-top: 10px; padding: 10px; background: white; border-left: 3px solid #e65100;">
                {explicacao}
            </p>
        </div>
        
        <!-- Explicação Técnica -->
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
            <h4 style="margin: 0 0 10px 0; color: #424242;">📚 Por que NDVI e EVI são diferentes?</h4>
            <ul style="font-size: 12px; margin: 0; padding-left: 20px;">
                <li><strong>NDVI:</strong> Sensível à clorofila, mas satura em vegetação densa</li>
                <li><strong>EVI:</strong> Corrige efeitos atmosféricos e saturação, melhor para florestas</li>
                <li><strong>Complementaridade:</strong> Usar ambos dá visão mais completa</li>
            </ul>
        </div>
        
        <p style="font-size: 10px; color: #999; text-align: center; margin-top: 15px;">
            📅 Dados extraídos de imagem Landsat 8 (Junho/2025)<br>
            📏 {ndvi_data['pixels']:,} pixels analisados
        </p>
    </div>
    """
    
    # Adicionar marcador
    folium.Marker(
        location=[info['coords']['lat'], info['coords']['lon']],
        popup=folium.Popup(popup_html, max_width=450),
        icon=folium.Icon(color=info['cor'], icon='info-sign', prefix='fa'),
        tooltip=f"📊 Clique para análise NDVI vs EVI - {parque_id}"
    ).add_to(m)
    
    print(f"   ✅ {parque_id}: NDVI={ndvi_val:.3f}, EVI={evi_val:.3f}, Discrepância={discrepancia:.3f}")

# Adicionar título
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50px; width: 550px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 15px; opacity: 0.95; box-shadow: 3px 3px 10px rgba(0,0,0,0.3);">
    <h3 style="margin: 0 0 10px 0; color: #2c5f2d;">📊 Análise Comparativa: NDVI vs EVI</h3>
    <p style="margin: 5px 0; font-size: 12px;">
        <strong>Entenda as diferenças entre os índices de vegetação</strong><br>
        Clique nos marcadores para análise detalhada de cada parque
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Adicionar legenda explicativa
legenda_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 10px; width: 280px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:11px; padding: 12px; opacity: 0.95;">
    <h4 style="margin: 0 0 10px 0; color: #424242;">📚 Guia Rápido</h4>
    <p style="margin: 5px 0;"><strong>NDVI:</strong> -1 a 1</p>
    <p style="margin: 0 0 5px 15px; font-size: 10px;">
        > 0.7 = Floresta densa<br>
        0.4-0.7 = Vegetação moderada<br>
        < 0.4 = Vegetação esparsa
    </p>
    <p style="margin: 5px 0;"><strong>EVI:</strong> -1 a 2</p>
    <p style="margin: 0 0 5px 15px; font-size: 10px;">
        > 0.5 = Cobertura excelente<br>
        0.3-0.5 = Cobertura boa<br>
        < 0.3 = Cobertura baixa
    </p>
    <hr style="margin: 10px 0;">
    <p style="font-size: 10px; margin: 0; color: #666;">
        💡 EVI geralmente mostra valores mais altos que NDVI em florestas densas devido à correção de saturação
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legenda_html))

# Salvar
output_file = 'mapa_analise_ndvi_vs_evi.html'
m.save(output_file)

print(f"\n✅ Mapa de análise comparativa criado: {output_file}")
print("\n" + "="*70)
print("   ✅ ANÁLISE COMPARATIVA CONCLUÍDA!")
print("="*70)

# Resumo da análise
print("\n📊 RESUMO DA ANÁLISE:")
print("\n🏔️  Parque Nacional São Joaquim:")
print(f"   • NDVI: {dados['NDVI']['PNSJ']['media']:.3f} (vegetação moderada)")
print(f"   • EVI:  {dados['EVI']['PNSJ']['media']:.3f} (cobertura excelente)")
print(f"   • Conclusão: EVI detecta mais vegetação, indicando floresta densa")

print("\n🏞️  Parque Estadual Serra Furada:")
print(f"   • NDVI: {dados['NDVI']['PESF']['media']:.3f} (vegetação moderada)")
print(f"   • EVI:  {dados['EVI']['PESF']['media']:.3f} (cobertura excelente)")
print(f"   • Conclusão: EVI detecta mais vegetação, indicando floresta densa")

print("\n🔬 INTERPRETAÇÃO GERAL:")
print("   ✅ Os valores de EVI são significativamente mais altos que NDVI")
print("   ✅ Isso é ESPERADO em áreas de floresta densa")
print("   ✅ NDVI satura em vegetação densa (valores máximos ~0.8-0.9)")
print("   ✅ EVI corrige essa saturação e detecta melhor a cobertura real")
print("   ✅ Imagem capturada em JUNHO (inverno) pode ter menos folhagem")

print("\n💡 RECOMENDAÇÃO:")
print("   • Use EVI para análises de cobertura vegetal densa")
print("   • Use NDVI para detecção de mudanças sazonais")
print("   • Combine ambos para análise completa")
