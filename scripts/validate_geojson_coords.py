#!/usr/bin/env python3
"""
Validator for GeoJSON layers and coordinate list used by the dashboard.

- Verifica existência de arquivos .geojson no diretório do projeto
- Tenta analisar cada arquivo .geojson com json.load
- Analisa `coordenadas_ppBio.js` procurando por `window.ppbioCoordenadas = [...]`
- Verifica campos obrigatórios: `lat`, `long`, `name`, `module`
- Valida ranges de latitude/longitude
- Pode sugerir normalizações (ex: `M1` -> `M01`) — apenas relatório por padrão

Uso:
    python scripts/validate_geojson_coords.py
    python scripts/validate_geojson_coords.py --fix  # write coordenadas_ppBio_fixed.js with module normalized

"""

import json
import os
import re
import sys
from glob import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOJSON_GLOB = os.path.join(ROOT, '*.geojson')
COORD_FILE = os.path.join(ROOT, 'coordenadas_ppBio.js')


def check_geojson_files():
    files = glob(GEOJSON_GLOB)
    print(f"Encontrados {len(files)} arquivos .geojson no diretório: {ROOT}")

    problems = []
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            if not isinstance(data, dict) or 'features' not in data:
                problems.append((f, 'Arquivo JSON sem chave "features"'))
        except Exception as e:
            problems.append((f, f'Erro ao ler/parsear: {e}'))

    if problems:
        print('\n== Problemas nos GeoJSONs ==')
        for p in problems:
            print(p[0], ':', p[1])
    else:
        print('\nTodos os GeoJSONs lidos corretamente (ou pelo menos parsearam).')

    return files, problems


def extract_coords_array(js_path):
    if not os.path.exists(js_path):
        print(f'Arquivo de coordenadas não encontrado: {js_path}')
        return None

    with open(js_path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    m = re.search(r"window\.ppbioCoordenadas\s*=\s*(\[.*?\]);", content, re.S)
    if not m:
        print('Não foi possível localizar `window.ppbioCoordenadas = [...]` em', js_path)
        return None

    arr_text = m.group(1)

    # Ajustes: remover comentários e finalizações traiçoeiras (se existirem)
    # O arquivo aparentemente usa JSON padrão — tentamos carregar diretamente
    try:
        coords = json.loads(arr_text)
    except Exception as e:
        # Tentar correções simples: substituir NaN por null, converter aspas simples
        fixed_text = re.sub(r'\bNaN\b', 'null', arr_text)
        try:
            coords = json.loads(fixed_text)
        except Exception as e2:
            print('Falha ao parsear array de coordenadas (tentativa com NaN->null falhou):', e2)
            return None

    return coords


def validate_coords(coords):
    issues = []
    for i, c in enumerate(coords):
        name = c.get('name')
        module = c.get('module')
        lat = c.get('lat')
        long = c.get('long')

        if name is None:
            issues.append((i, 'Falta campo name'))
        if module is None:
            issues.append((i, 'Falta campo module'))
        if lat is None or long is None:
            issues.append((i, 'Falta lat/long'))
            continue

        try:
            latf = float(lat)
            longf = float(long)
        except Exception:
            issues.append((i, f'lat/long não-numéricos: lat={lat!r}, long={long!r}'))
            continue

        if not (-90 <= latf <= 90):
            issues.append((i, f'Latitude fora de intervalo [-90,90]: {latf}'))
        if not (-180 <= longf <= 180):
            issues.append((i, f'Longitude fora de intervalo [-180,180]: {longf}'))

        # Check M vs M0 normalization
        if isinstance(module, str):
            if re.match(r'^M\d$', module):
                issues.append((i, f"Módulo com formato curto: {module} (sugestão: M0{module[1]})"))

    return issues


def write_fixed(coords, output_path):
    # Normalize module to M0X if given as Mx
    for c in coords:
        if 'module' in c and isinstance(c['module'], str):
            m = c['module'].strip()
            if re.match(r'^M\d$', m):
                c['module'] = f'M0{m[1]}'

    # Build JS array string
    js_array = json.dumps(coords, ensure_ascii=False, indent=2)
    with open(output_path, 'w', encoding='utf-8') as fh:
        fh.write('window.ppbioCoordenadas = ' + js_array + ';\n')

    print('Arquivo corrigido escrito em', output_path)


if __name__ == '__main__':
    files, geo_issues = check_geojson_files()

    coords = extract_coords_array(COORD_FILE)
    if coords is None:
        print('Não há dados de coordenadas válidos para checar.')
        sys.exit(1)

    print('\nTotal de coordenadas:', len(coords))
    coord_issues = validate_coords(coords)

    if coord_issues:
        print('\n== Problemas nas coordenadas encontrados:')
        for idx, msg in coord_issues:
            record = coords[idx]
            print(f'#{idx}: parcela={record.get("name")} module={record.get("module")} lat={record.get("lat")} long={record.get("long")}: {msg}')
    else:
        print('\nNenhum problema detectado nas coordenadas.')

    # Se passado --fix, criar `coordenadas_ppBio_fixed.js` no diretório raiz
    if '--fix' in sys.argv:
        out = os.path.join(ROOT, 'coordenadas_ppBio_fixed.js')
        write_fixed(coords, out)
        print('Use esse arquivo para revisar as correções; eu não alterei o arquivo original.')

    # Saída de resumo
    print('\nResumo:')
    print(f'  GeoJSONs com problemas: {len(geo_issues)}')
    print(f'  Coordenadas com problemas: {len(coord_issues)}')

    if len(coord_issues) == 0 and len(geo_issues) == 0:
        print('\nTudo parece OK. Tente abrir o dashboard via servidor local e verifique novamente o mapa.')
    else:
        print('\nRevise os itens acima antes de abrir o dashboard novamente.')
