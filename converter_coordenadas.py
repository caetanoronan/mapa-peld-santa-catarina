import csv
import json

# Carregar dados do CSV de coordenadas com tratamento de erros
coordenadas = []
try:
    with open('amb_csv/ppbio_sc-coordenadas_parcelas.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            coordenadas.append({
                'module': row['module'],
                'name': row['name'],
                'long': float(row['long']),
                'lat': float(row['lat']),
                'type': row['type']
            })
except UnicodeDecodeError:
    print("Tentando com codificação latin-1...")
    with open('amb_csv/ppbio_sc-coordenadas_parcelas.csv', 'r', encoding='latin-1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            coordenadas.append({
                'module': row['module'],
                'name': row['name'],
                'long': float(row['long']),
                'lat': float(row['lat']),
                'type': row['type']
            })

# Criar arquivo JavaScript com os dados
js_content = f"""
// Coordenadas PPBio carregadas do CSV
window.ppbioCoordenadas = {json.dumps(coordenadas, indent=2)};

console.log('Coordenadas PPBio carregadas:', window.ppbioCoordenadas.length, 'parcelas');
"""

with open('coordenadas_ppBio.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Arquivo coordenadas_ppBio.js criado com {len(coordenadas)} coordenadas!")