"""
Script para criar 3 visualizações de comparação temporal de índices de vegetação
Opção 1: Slider Temporal
Opção 2: Animação Automática  
Opção 3: Comparação Lado a Lado

Para demonstração, vamos simular dados de múltiplos períodos baseados na imagem atual
"""

import folium
from folium import plugins
import pandas as pd
import json
import base64
from datetime import datetime, timedelta

# Coordenadas dos parques
pn_coords = {'lat': -28.167, 'lon': -49.583}  # Parque Nacional São Joaquim
pe_coords = {'lat': -28.083, 'lon': -49.483}  # Parque Estadual Serra Furada

# Simular dados de 5 períodos (2020-2024)
periodos = [
    {'ano': 2020, 'data': '2020-07-15', 'estacao': 'Inverno'},
    {'ano': 2021, 'data': '2021-07-15', 'estacao': 'Inverno'},
    {'ano': 2022, 'data': '2022-07-15', 'estacao': 'Inverno'},
    {'ano': 2023, 'data': '2023-07-15', 'estacao': 'Inverno'},
    {'ano': 2024, 'data': '2024-07-15', 'estacao': 'Inverno'},
]

# Simular tendência de mudança nos índices (variação natural + tendência)
def gerar_indices_simulados(ano_base, parque):
    """
    Gera valores simulados de índices com variação temporal realista
    """
    # Valores base (2020)
    if parque == 'PNSJ':
        base_ndvi = 0.72
        base_evi = 0.58
        base_savi = 0.65
        base_arvi = 0.68
    else:  # PESF
        base_ndvi = 0.68
        base_evi = 0.54
        base_savi = 0.61
        base_arvi = 0.64
    
    # Calcular anos desde 2020
    anos_passados = ano_base - 2020
    
    # Simular tendência decrescente leve (degradação) + variação natural
    import random
    random.seed(ano_base * 100 + (1 if parque == 'PNSJ' else 2))
    
    variacao_natural = random.uniform(-0.03, 0.03)
    tendencia = -0.01 * anos_passados  # Leve degradação ao longo do tempo
    
    return {
        'NDVI': round(base_ndvi + tendencia + variacao_natural, 3),
        'EVI': round(base_evi + tendencia + variacao_natural, 3),
        'SAVI': round(base_savi + tendencia + variacao_natural, 3),
        'ARVI': round(base_arvi + tendencia + variacao_natural, 3),
    }

# Gerar dados para todos os períodos
dados_temporais = []
for periodo in periodos:
    dados_temporais.append({
        'ano': periodo['ano'],
        'data': periodo['data'],
        'estacao': periodo['estacao'],
        'PNSJ': gerar_indices_simulados(periodo['ano'], 'PNSJ'),
        'PESF': gerar_indices_simulados(periodo['ano'], 'PESF'),
    })

print("\n" + "="*70)
print("   GERADOR DE VISUALIZAÇÕES TEMPORAIS - PELD SC")
print("="*70)
print("\n📊 Dados simulados para 5 períodos (2020-2024)")
print("🏞️  Parques: PNSJ e PESF")
print("📈 Índices: NDVI, EVI, SAVI, ARVI\n")

# ============================================================================
# OPÇÃO 1: SLIDER TEMPORAL
# ============================================================================

def criar_mapa_slider_temporal():
    """
    Cria mapa interativo com controle de slider temporal
    """
    print("\n" + "─"*70)
    print("📍 OPÇÃO 1: Criando Mapa com Slider Temporal...")
    print("─"*70)
    
    # Criar mapa base
    m = folium.Map(
        location=[-28.125, -49.533],
        zoom_start=11,
        min_zoom=8,
        max_zoom=18,
        tiles='OpenStreetMap'
    )
    
    # Adicionar camada de topografia
    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='OpenTopoMap',
        name='Relevo',
        overlay=True,
        control=True,
        opacity=0.6
    ).add_to(m)
    
    # Criar grupos de features para cada período
    feature_groups = {}
    
    for dados in dados_temporais:
        ano = dados['ano']
        data = dados['data']
        
        # Criar grupo para este período
        fg = folium.FeatureGroup(name=f"{ano}", show=False)
        
        # Adicionar marcadores para PNSJ
        pnsj_indices = dados['PNSJ']
        popup_pnsj = f"""
        <div style="font-family: Arial; width: 280px;">
            <h4 style="color: #2c5f2d; margin-bottom: 10px;">
                🏔️ Parque Nacional São Joaquim
            </h4>
            <p style="font-size: 11px; color: #666; margin: 5px 0;">
                📅 Data: <strong>{data}</strong>
            </p>
            <hr style="margin: 10px 0;">
            <table style="width: 100%; font-size: 12px;">
                <tr style="background: #e8f5e9;">
                    <td style="padding: 5px;"><strong>NDVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pnsj_indices['NDVI']}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><strong>EVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pnsj_indices['EVI']}</td>
                </tr>
                <tr style="background: #e8f5e9;">
                    <td style="padding: 5px;"><strong>SAVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pnsj_indices['SAVI']}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><strong>ARVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pnsj_indices['ARVI']}</td>
                </tr>
            </table>
            <p style="font-size: 10px; color: #888; margin-top: 10px;">
                🌱 Saúde da vegetação: {'Excelente' if pnsj_indices['NDVI'] > 0.7 else 'Boa'}
            </p>
        </div>
        """
        
        folium.Marker(
            location=[pn_coords['lat'], pn_coords['lon']],
            popup=folium.Popup(popup_pnsj, max_width=300),
            icon=folium.Icon(color='green', icon='tree', prefix='fa'),
            tooltip=f"PNSJ - {ano}"
        ).add_to(fg)
        
        # Adicionar marcadores para PESF
        pesf_indices = dados['PESF']
        popup_pesf = f"""
        <div style="font-family: Arial; width: 280px;">
            <h4 style="color: #1565c0; margin-bottom: 10px;">
                🏞️ Parque Estadual Serra Furada
            </h4>
            <p style="font-size: 11px; color: #666; margin: 5px 0;">
                📅 Data: <strong>{data}</strong>
            </p>
            <hr style="margin: 10px 0;">
            <table style="width: 100%; font-size: 12px;">
                <tr style="background: #e3f2fd;">
                    <td style="padding: 5px;"><strong>NDVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pesf_indices['NDVI']}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><strong>EVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pesf_indices['EVI']}</td>
                </tr>
                <tr style="background: #e3f2fd;">
                    <td style="padding: 5px;"><strong>SAVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pesf_indices['SAVI']}</td>
                </tr>
                <tr>
                    <td style="padding: 5px;"><strong>ARVI</strong></td>
                    <td style="padding: 5px; text-align: right;">{pesf_indices['ARVI']}</td>
                </tr>
            </table>
            <p style="font-size: 10px; color: #888; margin-top: 10px;">
                🌱 Saúde da vegetação: {'Excelente' if pesf_indices['NDVI'] > 0.7 else 'Boa'}
            </p>
        </div>
        """
        
        folium.Marker(
            location=[pe_coords['lat'], pe_coords['lon']],
            popup=folium.Popup(popup_pesf, max_width=300),
            icon=folium.Icon(color='blue', icon='tree', prefix='fa'),
            tooltip=f"PESF - {ano}"
        ).add_to(fg)
        
        feature_groups[ano] = fg
        fg.add_to(m)
    
    # Adicionar controle de slider temporal
    # Usando TimestampedGeoJson para controle temporal
    features = []
    for dados in dados_temporais:
        ano = dados['ano']
        
        # PNSJ
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [pn_coords['lon'], pn_coords['lat']],
            },
            'properties': {
                'time': dados['data'],
                'popup': f"PNSJ - {ano}",
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': 'green',
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 8
                }
            }
        })
        
        # PESF
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [pe_coords['lon'], pe_coords['lat']],
            },
            'properties': {
                'time': dados['data'],
                'popup': f"PESF - {ano}",
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': 'blue',
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 8
                }
            }
        })
    
    # Adicionar TimestampedGeoJson
    plugins.TimestampedGeoJson(
        {'type': 'FeatureCollection', 'features': features},
        period='P1Y',  # Período de 1 ano
        duration='P1Y',
        add_last_point=True,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY',
        time_slider_drag_update=True
    ).add_to(m)
    
    # Adicionar título
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 500px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; opacity: 0.9;">
        <h4 style="margin: 0; color: #2c5f2d;">📊 Análise Temporal de Índices de Vegetação</h4>
        <p style="margin: 5px 0; font-size: 12px;">
            Parques de Santa Catarina (2020-2024)<br>
            <strong>Use o controle de tempo abaixo para navegar entre os anos</strong>
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Salvar
    m.save('mapa_slider_temporal.html')
    print("✅ Mapa com slider temporal criado: mapa_slider_temporal.html")
    print("   Use o controle temporal na parte inferior para navegar entre os anos")

# ============================================================================
# OPÇÃO 2: COMPARAÇÃO LADO A LADO
# ============================================================================

def criar_mapa_comparacao_lado_a_lado():
    """
    Cria interface com dois mapas lado a lado para comparação
    """
    print("\n" + "─"*70)
    print("📍 OPÇÃO 2: Criando Mapa de Comparação Lado a Lado...")
    print("─"*70)
    
    # Dados de 2020 e 2024
    dados_2020 = dados_temporais[0]
    dados_2024 = dados_temporais[-1]
    
    # Criar HTML customizado com dois mapas lado a lado
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comparação Temporal 2020 vs 2024</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
            #header {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: white;
                border-bottom: 2px solid #333;
                padding: 15px;
                text-align: center;
                z-index: 1000;
            }
            #maps-container {
                display: flex;
                height: 100vh;
                padding-top: 80px;
            }
            #map2020, #map2024 {
                flex: 1;
                height: calc(100vh - 80px);
            }
            .map-label {
                position: absolute;
                top: 90px;
                padding: 10px 20px;
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid #333;
                font-weight: bold;
                z-index: 999;
                font-size: 16px;
            }
            #label2020 { left: 10px; color: #1565c0; }
            #label2024 { right: 10px; color: #2c5f2d; }
        </style>
    </head>
    <body>
        <div id="header">
            <h2 style="margin: 0; color: #2c5f2d;">📊 Comparação Temporal de Índices de Vegetação</h2>
            <p style="margin: 5px 0; font-size: 14px;">
                Parques de Santa Catarina: <strong style="color: #1565c0;">2020</strong> vs <strong style="color: #2c5f2d;">2024</strong>
            </p>
        </div>
        <div class="map-label" id="label2020">📅 2020</div>
        <div class="map-label" id="label2024">📅 2024</div>
        <div id="maps-container">
            <div id="map2020"></div>
            <div id="map2024"></div>
        </div>
        
        <script>
            // Criar mapa 2020
            var map2020 = L.map('map2020').setView([-28.125, -49.533], 11);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                minZoom: 8,
                maxZoom: 18
            }).addTo(map2020);
            
            // Criar mapa 2024
            var map2024 = L.map('map2024').setView([-28.125, -49.533], 11);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                minZoom: 8,
                maxZoom: 18
            }).addTo(map2024);
            
            // Sincronizar mapas
            map2020.on('moveend', function() {
                map2024.setView(map2020.getCenter(), map2020.getZoom(), {animate: false});
            });
            map2024.on('moveend', function() {
                map2020.setView(map2024.getCenter(), map2024.getZoom(), {animate: false});
            });
            
            // Dados 2020
            """
    
    # Adicionar marcadores 2020
    for parque, coords, cor, nome in [
        ('PNSJ', pn_coords, 'green', 'Parque Nacional São Joaquim'),
        ('PESF', pe_coords, 'blue', 'Parque Estadual Serra Furada')
    ]:
        indices = dados_2020[parque]
        html_content += f"""
            L.marker([{coords['lat']}, {coords['lon']}], {{
                icon: L.icon({{
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-{cor}.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                }})
            }}).addTo(map2020)
            .bindPopup(`
                <div style="font-family: Arial; width: 220px;">
                    <h4 style="color: {'#2c5f2d' if cor == 'green' else '#1565c0'};">{nome}</h4>
                    <p><strong>📅 Ano: 2020</strong></p>
                    <hr>
                    <table style="width: 100%; font-size: 12px;">
                        <tr><td><strong>NDVI</strong></td><td>{indices['NDVI']}</td></tr>
                        <tr><td><strong>EVI</strong></td><td>{indices['EVI']}</td></tr>
                        <tr><td><strong>SAVI</strong></td><td>{indices['SAVI']}</td></tr>
                        <tr><td><strong>ARVI</strong></td><td>{indices['ARVI']}</td></tr>
                    </table>
                </div>
            `);
        """
    
    # Adicionar marcadores 2024
    html_content += "\n            // Dados 2024\n"
    for parque, coords, cor, nome in [
        ('PNSJ', pn_coords, 'green', 'Parque Nacional São Joaquim'),
        ('PESF', pe_coords, 'blue', 'Parque Estadual Serra Furada')
    ]:
        indices = dados_2024[parque]
        indices_2020 = dados_2020[parque]
        delta_ndvi = indices['NDVI'] - indices_2020['NDVI']
        delta_evi = indices['EVI'] - indices_2020['EVI']
        
        html_content += f"""
            L.marker([{coords['lat']}, {coords['lon']}], {{
                icon: L.icon({{
                    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-{cor}.png',
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                }})
            }}).addTo(map2024)
            .bindPopup(`
                <div style="font-family: Arial; width: 220px;">
                    <h4 style="color: {'#2c5f2d' if cor == 'green' else '#1565c0'};">{nome}</h4>
                    <p><strong>📅 Ano: 2024</strong></p>
                    <hr>
                    <table style="width: 100%; font-size: 12px;">
                        <tr><td><strong>NDVI</strong></td><td>{indices['NDVI']}</td><td style="color: {'red' if delta_ndvi < 0 else 'green'};">({delta_ndvi:+.3f})</td></tr>
                        <tr><td><strong>EVI</strong></td><td>{indices['EVI']}</td><td style="color: {'red' if delta_evi < 0 else 'green'};">({delta_evi:+.3f})</td></tr>
                        <tr><td><strong>SAVI</strong></td><td>{indices['SAVI']}</td></tr>
                        <tr><td><strong>ARVI</strong></td><td>{indices['ARVI']}</td></tr>
                    </table>
                    <p style="font-size: 10px; margin-top: 10px;">📊 Mudança desde 2020</p>
                </div>
            `);
        """
    
    html_content += """
        </script>
    </body>
    </html>
    """
    
    # Salvar arquivo
    with open('mapa_comparacao_lado_a_lado.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Mapa de comparação criado: mapa_comparacao_lado_a_lado.html")
    print("   Mapas sincronizados: 2020 (esquerda) vs 2024 (direita)")

# ============================================================================
# OPÇÃO 3: GRÁFICOS DE SÉRIE TEMPORAL
# ============================================================================

def criar_graficos_serie_temporal():
    """
    Cria mapa com gráficos de evolução temporal
    """
    print("\n" + "─"*70)
    print("📍 OPÇÃO 3: Criando Mapa com Gráficos de Série Temporal...")
    print("─"*70)
    
    # Criar mapa base
    m = folium.Map(
        location=[-28.125, -49.533],
        zoom_start=11,
        min_zoom=8,
        max_zoom=18,
        tiles='OpenStreetMap'
    )
    
    # Preparar dados para gráficos
    anos = [d['ano'] for d in dados_temporais]
    
    # Dados PNSJ
    pnsj_ndvi = [d['PNSJ']['NDVI'] for d in dados_temporais]
    pnsj_evi = [d['PNSJ']['EVI'] for d in dados_temporais]
    
    # Dados PESF
    pesf_ndvi = [d['PESF']['NDVI'] for d in dados_temporais]
    pesf_evi = [d['PESF']['EVI'] for d in dados_temporais]
    
    # Criar gráfico PNSJ usando Vega-Lite (embutido no popup)
    popup_pnsj = f"""
    <div style="font-family: Arial; width: 450px;">
        <h4 style="color: #2c5f2d; text-align: center;">
            🏔️ Parque Nacional São Joaquim
        </h4>
        <h5 style="text-align: center; color: #666;">Evolução Temporal (2020-2024)</h5>
        <hr>
        
        <div style="margin: 10px 0;">
            <strong>📈 NDVI ao longo do tempo:</strong>
            <div style="font-family: monospace; font-size: 11px; background: #f5f5f5; padding: 10px; margin-top: 5px;">
                {'<br>'.join([f'{ano}: {"▓" * int(ndvi * 50)} {ndvi:.3f}' for ano, ndvi in zip(anos, pnsj_ndvi)])}
            </div>
        </div>
        
        <div style="margin: 10px 0;">
            <strong>📈 EVI ao longo do tempo:</strong>
            <div style="font-family: monospace; font-size: 11px; background: #f5f5f5; padding: 10px; margin-top: 5px;">
                {'<br>'.join([f'{ano}: {"▓" * int(evi * 50)} {evi:.3f}' for ano, evi in zip(anos, pnsj_evi)])}
            </div>
        </div>
        
        <div style="margin-top: 15px; padding: 10px; background: #e8f5e9; border-radius: 5px;">
            <strong>📊 Análise:</strong>
            <p style="font-size: 11px; margin: 5px 0;">
                • Mudança NDVI: {pnsj_ndvi[-1] - pnsj_ndvi[0]:+.3f} ({((pnsj_ndvi[-1] - pnsj_ndvi[0])/pnsj_ndvi[0]*100):+.1f}%)<br>
                • Mudança EVI: {pnsj_evi[-1] - pnsj_evi[0]:+.3f} ({((pnsj_evi[-1] - pnsj_evi[0])/pnsj_evi[0]*100):+.1f}%)<br>
                • Tendência: {'Crescimento' if pnsj_ndvi[-1] > pnsj_ndvi[0] else 'Declínio'}
            </p>
        </div>
    </div>
    """
    
    folium.Marker(
        location=[pn_coords['lat'], pn_coords['lon']],
        popup=folium.Popup(popup_pnsj, max_width=470),
        icon=folium.Icon(color='green', icon='chart-line', prefix='fa'),
        tooltip="📊 Clique para ver evolução temporal - PNSJ"
    ).add_to(m)
    
    # Criar gráfico PESF
    popup_pesf = f"""
    <div style="font-family: Arial; width: 450px;">
        <h4 style="color: #1565c0; text-align: center;">
            🏞️ Parque Estadual Serra Furada
        </h4>
        <h5 style="text-align: center; color: #666;">Evolução Temporal (2020-2024)</h5>
        <hr>
        
        <div style="margin: 10px 0;">
            <strong>📈 NDVI ao longo do tempo:</strong>
            <div style="font-family: monospace; font-size: 11px; background: #f5f5f5; padding: 10px; margin-top: 5px;">
                {'<br>'.join([f'{ano}: {"▓" * int(ndvi * 50)} {ndvi:.3f}' for ano, ndvi in zip(anos, pesf_ndvi)])}
            </div>
        </div>
        
        <div style="margin: 10px 0;">
            <strong>📈 EVI ao longo do tempo:</strong>
            <div style="font-family: monospace; font-size: 11px; background: #f5f5f5; padding: 10px; margin-top: 5px;">
                {'<br>'.join([f'{ano}: {"▓" * int(evi * 50)} {evi:.3f}' for ano, evi in zip(anos, pesf_evi)])}
            </div>
        </div>
        
        <div style="margin-top: 15px; padding: 10px; background: #e3f2fd; border-radius: 5px;">
            <strong>📊 Análise:</strong>
            <p style="font-size: 11px; margin: 5px 0;">
                • Mudança NDVI: {pesf_ndvi[-1] - pesf_ndvi[0]:+.3f} ({((pesf_ndvi[-1] - pesf_ndvi[0])/pesf_ndvi[0]*100):+.1f}%)<br>
                • Mudança EVI: {pesf_evi[-1] - pesf_evi[0]:+.3f} ({((pesf_evi[-1] - pesf_evi[0])/pesf_evi[0]*100):+.1f}%)<br>
                • Tendência: {'Crescimento' if pesf_ndvi[-1] > pesf_ndvi[0] else 'Declínio'}
            </p>
        </div>
    </div>
    """
    
    folium.Marker(
        location=[pe_coords['lat'], pe_coords['lon']],
        popup=folium.Popup(popup_pesf, max_width=470),
        icon=folium.Icon(color='blue', icon='chart-line', prefix='fa'),
        tooltip="📊 Clique para ver evolução temporal - PESF"
    ).add_to(m)
    
    # Adicionar título
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 500px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; opacity: 0.9;">
        <h4 style="margin: 0; color: #2c5f2d;">📊 Análise de Série Temporal</h4>
        <p style="margin: 5px 0; font-size: 12px;">
            Evolução dos Índices de Vegetação (2020-2024)<br>
            <strong>Clique nos marcadores para ver os gráficos de tendência</strong>
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Adicionar legenda
    legenda_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 10px; width: 200px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:11px; padding: 10px; opacity: 0.9;">
        <h5 style="margin: 0 0 10px 0;">📊 Análise de Tendências</h5>
        <p style="margin: 5px 0;">
            <strong>NDVI/EVI:</strong><br>
            • > 0.7: Vegetação densa<br>
            • 0.4-0.7: Vegetação moderada<br>
            • < 0.4: Solo exposto<br><br>
            <strong>Tendência:</strong><br>
            • Valores crescentes: Recuperação<br>
            • Valores decrescentes: Degradação
        </p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legenda_html))
    
    # Salvar
    m.save('mapa_serie_temporal.html')
    print("✅ Mapa com gráficos temporais criado: mapa_serie_temporal.html")
    print("   Clique nos marcadores para ver a evolução dos índices")

# ============================================================================
# EXECUTAR TODAS AS VISUALIZAÇÕES
# ============================================================================

def main():
    """
    Função principal - gera todas as 3 visualizações
    """
    print("\n" + "="*70)
    print("   INICIANDO GERAÇÃO DAS 3 VISUALIZAÇÕES TEMPORAIS")
    print("="*70)
    
    # Opção 1
    criar_mapa_slider_temporal()
    
    # Opção 2
    criar_mapa_comparacao_lado_a_lado()
    
    # Opção 3
    criar_graficos_serie_temporal()
    
    print("\n" + "="*70)
    print("   ✅ TODAS AS VISUALIZAÇÕES FORAM CRIADAS COM SUCESSO!")
    print("="*70)
    print("\n📂 Arquivos gerados:")
    print("   1. mapa_slider_temporal.html - Navegação temporal com slider")
    print("   2. mapa_comparacao_lado_a_lado.html - Comparação 2020 vs 2024")
    print("   3. mapa_serie_temporal.html - Gráficos de evolução temporal")
    print("\n💡 Dica: Abra cada arquivo no navegador para explorar!")
    print("\n⚠️  NOTA: Dados são simulados para demonstração.")
    print("   Para dados reais, use o script 'baixar_landsat_temporal.py'")

if __name__ == "__main__":
    main()
