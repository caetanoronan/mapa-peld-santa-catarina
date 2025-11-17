import json

# Mapeamento do PDF
mapping = {
    'TN0500': 'M01T01',
    'TN1500': 'M01T02',
    'TN2500': 'M01T03',
    'TN3500': 'M01T04',
    'TN4500': 'M01T05',
    'TS0500': 'M01T06',
    'TS1500': 'M01T07',
    'TS2500': 'M01T08',
    'TS3500': 'M01T09',
    'TS4500': 'M01T10',
    'TN1300': 'M01R01',
    'TN4000': 'M01R02',
    'TS0150': 'M01R03',
    'TS1845': 'M01R04',
    'TL0900': 'M01R05',
    'TW1500': 'M02T02',
    'TW3500': 'M02T04',
    'TW4500': 'M02T05',
    'TL400_PSA4': 'M02T06',
    'TW065_RIP5_PSA9': 'M02R01',
    'T1': 'M03T01',
    'T2': 'M03T02',
    'T3': 'M03T03',
    'T4': 'M03T04',
    'T5': 'M03T05',
    'T6': 'M03T06',
    'T7': 'M03T07',
    'T8': 'M03T08',
    'T9': 'M03T09',
    'T10': 'M03T10',
    'R1': 'M03R01',
    'R2': 'M03R02',
    'R3': 'M03R03'
}

# Ler o arquivo JavaScript
with open('coordenadas_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar a parte JSON dentro do JavaScript
start = content.find('window.ppbioCoordenadas = [')
end = content.find('];', start) + 2

json_part = content[start:end]

# Parsear como JSON (removendo a parte JavaScript)
json_str = json_part.replace('window.ppbioCoordenadas = ', '').rstrip(';')

# Carregar como JSON
data = json.loads(json_str)

# Atualizar os nomes
updated_count = 0
for item in data:
    old_name = item['name']
    if old_name in mapping:
        item['name'] = mapping[old_name]
        updated_count += 1
        print(f'Atualizado: {old_name} -> {item["name"]}')

print(f'Total de parcelas atualizadas: {updated_count}')

# Converter de volta para JSON
updated_json = json.dumps(data, indent=2, ensure_ascii=False)

# Atualizar o conteúdo do arquivo
updated_content = content.replace(json_str, updated_json)

# Salvar o arquivo atualizado
with open('coordenadas_ppBio.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print('Arquivo coordenadas_ppBio.js atualizado com sucesso!')