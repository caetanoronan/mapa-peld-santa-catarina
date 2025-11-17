import json
import pdfplumber

# Extrair o mapeamento completo do PDF
pdf_path = 'Parcelas PPBio Atualizadas.pdf'
mapeadas = set()

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table[1:]:  # Pular cabeçalho
                antigo, novo, existencia = row
                if existencia == 'SIM':
                    mapeadas.add(novo)

print(f'Parcelas mapeadas no PDF: {len(mapeadas)}')
print('Nomes mapeados:', sorted(mapeadas))

# Ler o arquivo atual
with open('coordenadas_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('window.ppbioCoordenadas = [')
end = content.find('];', start) + 2
json_str = content[start:end].replace('window.ppbioCoordenadas = ', '').rstrip(';')
data = json.loads(json_str)

print(f'\nParcelas no arquivo: {len(data)}')

# Filtrar apenas as parcelas que estão mapeadas no PDF
parcelas_filtradas = []
removidas = []

for item in data:
    name = item['name']
    if name in mapeadas:
        parcelas_filtradas.append(item)
        print(f'MANTIDA: {name}')
    else:
        removidas.append(item)
        print(f'REMOVIDA: {name} - {item["module"]} - {item["type"]}')

print(f'\nMantidas: {len(parcelas_filtradas)}')
print(f'Removidas: {len(removidas)}')

# Salvar o arquivo filtrado
updated_json = json.dumps(parcelas_filtradas, indent=2, ensure_ascii=False)
updated_content = content.replace(json_str, updated_json)

with open('coordenadas_ppBio.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print('\nArquivo coordenadas_ppBio.js atualizado! Agora contém apenas as parcelas que existem segundo o PDF.')