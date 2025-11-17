import json

# Parcelas que não existem (usando os novos nomes após atualização)
nao_existem_novos = [
    'M02T01', 'M02T03', 'M02T07', 'M02T08', 'M02T09', 'M02T10',
    'M02R02', 'M02R03', 'M02R04', 'M02R05', 'M03R04', 'M03R05'
]

# Ler o arquivo JavaScript
with open('coordenadas_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar a parte JSON
start = content.find('window.ppbioCoordenadas = [')
end = content.find('];', start) + 2
json_str = content[start:end].replace('window.ppbioCoordenadas = ', '').rstrip(';')

# Carregar como JSON
data = json.loads(json_str)

print('Parcelas atuais no arquivo:')
parcelas_para_remover = []
parcelas_filtradas = []

for item in data:
    name = item['name']
    module = item['module']
    tipo = item['type']

    # Verificar se deve ser removida
    deve_remover = False

    # Verificar se está na lista de parcelas que não existem
    if name in nao_existem_novos:
        deve_remover = True
        print(f'{name} - {module} - {tipo} -> REMOVIDA (não existe)')

    else:
        parcelas_filtradas.append(item)
        print(f'{name} - {module} - {tipo} -> MANTIDA')

if parcelas_para_remover:
    print(f'\nRemovendo {len(parcelas_para_remover)} parcelas...')

print(f'\nTotal original: {len(data)} parcelas')
print(f'Total após filtro: {len(parcelas_filtradas)} parcelas')
print(f'Removidas: {len(data) - len(parcelas_filtradas)} parcelas')

# Converter de volta para JSON
updated_json = json.dumps(parcelas_filtradas, indent=2, ensure_ascii=False)

# Atualizar o conteúdo do arquivo
updated_content = content.replace(json_str, updated_json)

# Salvar o arquivo atualizado
with open('coordenadas_ppBio.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print('\nArquivo coordenadas_ppBio.js atualizado! Parcelas inexistentes removidas.')