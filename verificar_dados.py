import json

# Verificar coordenadas
with open('coordenadas_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    coords = json.loads(content[start:end])
    print(f'Coordenadas carregadas: {len(coords)}')
    print('Primeiras 3 coordenadas:')
    for i, coord in enumerate(coords[:3]):
        print(f'  {i+1}. {coord["name"]} - Módulo: {coord["module"]} - Lat: {coord["lat"]}, Lon: {coord["long"]}')

# Verificar dados ecológicos
with open('dados_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    data = json.loads(content[start:end])
    print(f'\nDados ecológicos carregados: {len(data)}')
    print('Primeiros 3 registros:')
    for i, item in enumerate(data[:3]):
        antigo = item.get('Antigo', 'N/A')
        plot = item.get('Plot', 'N/A')
        mod = item.get('Mod', 'N/A')
        tipo_veg = item.get('tipo.veg', 'N/A')
        print(f'  {i+1}. Antigo: {antigo}, Plot: {plot}, Mod: {mod}, Vegetação: {tipo_veg}')

# Verificar correspondência
print('\nVerificando correspondência entre coordenadas e dados ecológicos:')
matches = 0
for coord in coords[:10]:  # Verificar primeiras 10
    ecological = None
    for item in data:
        if item.get('Antigo') == coord['name'] or item.get('Plot') == coord['name']:
            ecological = item
            break
    if ecological:
        matches += 1
        print(f'  ✓ {coord["name"]} -> Encontrado (Vegetação: {ecological.get("tipo.veg", "N/A")})')
    else:
        print(f'  ✗ {coord["name"]} -> Não encontrado')

print(f'\nCorrespondências encontradas (primeiras 10): {matches}/10')