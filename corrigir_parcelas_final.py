import argparse
import csv
import json
from datetime import datetime
from pathlib import Path


# Parcelas que não existem (nomes antigos)
nao_existem_antigos = [
    'TW0500', 'TW2500', 'TL1500', 'TL2500', 'TL3500', 'TL4500'
]


def extract_json_block(content: str, varname: str = 'window.ppbioCoordenadas') -> tuple[str, int, int]:
    """Extract JSON array assigned to a JS variable and return substring + start+end indices."""
    start_marker = f'{varname} = '
    start = content.find(start_marker)
    if start == -1:
        raise ValueError(f'Variável JS {varname} não encontrada.')
    # find the opening [ after the assignment
    arr_start = content.find('[', start)
    # find matching closing '];' after arr_start
    arr_end = content.find('];', arr_start)
    if arr_start == -1 or arr_end == -1:
        raise ValueError('Bloco JSON não encontrado ou malformed JS.')
    json_str = content[arr_start:arr_end + 1]
    return json_str, arr_start, arr_end + 1


parser = argparse.ArgumentParser(description='Corrigir nomes de parcelas em coordenadas_ppBio.js')
parser.add_argument('--apply', action='store_true', help='Escreve o arquivo atualizado (caso contrário, dry-run)')
parser.add_argument('--backup', action='store_true', help='Cria um backup do arquivo original antes de sobrescrever')
parser.add_argument('--resolve-duplicates', action='store_true', help='Tenta resolver colisões de nomes ao finalizando o mapeamento')
args = parser.parse_args()


# Ler o arquivo JavaScript
js_path = Path('coordenadas_ppBio.js')
content = js_path.read_text(encoding='utf-8')

# Encontrar a parte JSON
json_str, sidx, eidx = extract_json_block(content, 'window.ppbioCoordenadas')

# Carregar como JSON
data = json.loads(json_str)

print('Removendo parcelas que não existem...')
parcelas_filtradas = []
removidas = 0
removed_log = []

for item in data:
    name = item.get('name')
    if name in nao_existem_antigos:
        module = item.get('module', '')
        tipo = item.get('type', '')
        print(f'REMOVIDA: {name} - {module} - {tipo}')
        removed_log.append({'old': name, 'module': module, 'type': tipo})
        removidas += 1
    else:
        parcelas_filtradas.append(item)

print(f'\nRemovidas: {removidas} parcelas')
print(f'Restantes: {len(parcelas_filtradas)} parcelas')

# Agora aplicar o mapeamento dos nomes
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

print('\nAtualizando nomes das parcelas restantes...')
atualizadas = 0
map_log = []
for item in parcelas_filtradas:
    old_name = item['name']
    if old_name in mapping:
        item['name'] = mapping[old_name]
        print(f'{old_name} -> {item["name"]}')
        atualizadas += 1
        map_log.append({'old': old_name, 'new': item['name'], 'action': 'MAPPED'})
    else:
        map_log.append({'old': old_name, 'new': old_name, 'action': 'UNCHANGED'})

print(f'\nAtualizadas: {atualizadas} parcelas')
print(f'Total final: {len(parcelas_filtradas)} parcelas')

# Verifica colisões de nomes (duplicates)
from collections import Counter, defaultdict
name_counts = Counter([p.get('name') for p in parcelas_filtradas])
duplicates = [name for name, cnt in name_counts.items() if cnt > 1]
if duplicates:
    print('\nAtenção: colisões encontradas para os seguintes nomes (aparências):')
    for d in duplicates:
        print(f'  {d}: {name_counts[d]} ocorrências')
    if args.resolve_duplicates:
        print('\nTentando resolver colisões automaticamente...')
        dupe_map = defaultdict(int)
        for item in parcelas_filtradas:
            nm = item.get('name')
            if nm in duplicates:
                dupe_map[nm] += 1
                suffix = f'_dup{dupe_map[nm]}'
                item['name'] = f'{nm}{suffix}'
                print(f'  Ajustado {nm} -> {item["name"]}')
                map_log.append({'old': nm, 'new': item['name'], 'action': 'DUP_RESOLVED'})
else:
    print('\nNenhuma colisão de nomes encontrada.')
# Salvar o arquivo atualizado
updated_json = json.dumps(parcelas_filtradas, indent=2, ensure_ascii=False)
updated_content = content.replace(json_str, updated_json)
# Build CSV report
report_rows = []
for m in map_log:
    report_rows.append({'old_name': m['old'], 'new_name': m['new'], 'action': m.get('action', '')})
for r in removed_log:
    report_rows.append({'old_name': r['old'], 'new_name': '', 'action': 'REMOVED'})

report_file = 'corrigir_parcelas_report.csv'
with open(report_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['old_name', 'new_name', 'action'])
    writer.writeheader()
    for row in report_rows:
        writer.writerow(row)

print(f'\nRelatório gerado: {report_file}')

if args.apply:
    if args.backup:
        backup_name = f'coordenadas_ppBio.js.bak.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        print(f'Criando backup: {backup_name}')
        Path(backup_name).write_text(content, encoding='utf-8')
    # Write updated file
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print('\nArquivo coordenadas_ppBio.js atualizado com sucesso!')
else:
    print('\nDry-run: o arquivo não foi escrito. Re-execute com --apply para gravar as mudanças.')