"""
Script para adicionar rodapé com créditos em todos os mapas HTML
"""

import os
import glob

# Rodapé HTML padrão com créditos
rodape_creditos = """
<div style="position: fixed; bottom: 0; left: 0; right: 0; 
            background: rgba(255, 255, 255, 0.95); 
            border-top: 2px solid #ddd; 
            padding: 10px; 
            z-index: 9999; 
            font-size: 11px;
            text-align: center;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);">
    <strong>👨‍💻 Desenvolvido por:</strong> Ronan Armando Caetano (UFSC) — Graduando em Ciências Biológicas; Técnico em Geoprocessamento (IFSC); Técnico em Saneamento (IFSC) | 
    <strong>🤖 Com assistência de:</strong> GitHub Copilot — Raptor mini (Preview) | 
    <strong>🏛️</strong> PELD-BISC 2025 | 
    <strong>🛰️</strong> Dados: Landsat 8/9, ICMBio, PELD | 
    <a href="dashboard_peld.html" style="color: #3498db; text-decoration: none; font-weight: bold;">📊 Dashboard</a> | 
    <a href="CREDITOS.md" target="_blank" style="color: #3498db; text-decoration: none; font-weight: bold;">📚 Créditos Completos</a>
</div>
"""

print("\n" + "="*70)
print("   ADICIONANDO CRÉDITOS AOS MAPAS HTML")
print("="*70)

# Lista de arquivos HTML (mapas)
mapas_html = [
    'mapa_interativo_peld.html',
    'mapa_indices_parques.html',
    'mapa_slider_temporal.html',
    'mapa_comparacao_lado_a_lado.html',
    'mapa_serie_temporal.html',
    'mapa_analise_ndvi_vs_evi.html'
]

for mapa in mapas_html:
    if os.path.exists(mapa):
        print(f"\n📄 Processando: {mapa}")
        
        # Ler conteúdo do arquivo
        with open(mapa, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar se já tem créditos
        if 'Ronan Armando Caetano' in conteudo:
            print(f"   ✅ Já contém créditos")
            continue
        
        # Adicionar rodapé antes do </body>
        if '</body>' in conteudo:
            conteudo = conteudo.replace('</body>', rodape_creditos + '\n</body>')
            
            # Salvar arquivo atualizado
            with open(mapa, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            print(f"   ✅ Créditos adicionados com sucesso!")
        else:
            print(f"   ⚠️  Tag </body> não encontrada")
    else:
        print(f"\n❌ Arquivo não encontrado: {mapa}")

print("\n" + "="*70)
print("   ✅ PROCESSO CONCLUÍDO!")
print("="*70)
print("\n💡 Todos os mapas agora incluem créditos no rodapé")
print("📄 Créditos completos disponíveis em: CREDITOS.md")
