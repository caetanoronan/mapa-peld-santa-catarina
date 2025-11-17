import json

# Carrega coordenadas
with open('coordenadas_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    coords = json.loads(content[start:end])

# Carrega dados ecológicos
with open('dados_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    data = json.loads(content[start:end])

# Mapear por 'Antigo' e 'Plot'
map_antigo = {}
map_plot = {}
for item in data:
    antigo = item.get('Antigo')
    plot = item.get('Plot')
    if antigo:
        map_antigo.setdefault(antigo, []).append(item)
    if plot:
        map_plot.setdefault(plot, []).append(item)

# Verificar correspondência para todas as coordenadas
not_found = []
duplicate_matches = []
exact_matches = 0
for coord in coords:
    name = coord['name']
    antiga = map_antigo.get(name, [])
    byplot = map_plot.get(name, [])
    matches = len(antiga) + len(byplot)
    if matches == 0:
        not_found.append(name)
    elif matches > 1:
        duplicate_matches.append((name, matches))
    else:
        exact_matches += 1

print(f'Total coordenadas: {len(coords)}')
print(f'Encontradas com correspondência exata: {exact_matches}')
print(f'Com correspondência duplicada: {len(duplicate_matches)} -> {duplicate_matches[:10]}')
print(f'Não encontradas: {len(not_found)} -> {not_found[:20]}')

# Checar se há entradas sem 'Plot' ou sem 'Antigo'
no_plot = [d for d in data if not d.get('Plot')]
no_antigo = [d for d in data if not d.get('Antigo')]
print(f'Entradas sem Plot: {len(no_plot)}')
print(f'Entradas sem Antigo: {len(no_antigo)}')

# Duplicatas no conjunto de dados
from collections import Counter
plots = [d.get('Plot') for d in data if d.get('Plot')]
antigos = [d.get('Antigo') for d in data if d.get('Antigo')]
plot_counts = {k: v for k, v in Counter(plots).items() if v > 1}
antigo_counts = {k: v for k, v in Counter(antigos).items() if v > 1}
print(f'Duplicatas por Plot: {len(plot_counts)}')
print(f'Duplicatas por Antigo: {len(antigo_counts)}')

# Tip: listar os nomes que aparecem no mapa simples completo (arquivo gerado) e compará-los com coords
try:
    with open('mapa_simples_completo.html', 'r', encoding='utf-8') as f:
        content = f.read()
        # quick search for M0xTxx pattern occurrences
        import re
        names = set(re.findall(r"M\d\dT\d\d|M\d\dR\d\d", content))
        # Ajuste: regex deve capturar M01T05 etc.
        # Mais permissivo:
        names2 = set(re.findall(r"M\d{2}[TR]\d{2}", content))
        print(f'Mapa Simples Completo nomes encontrados (amostra 20): {list(names2)[:20]}')
except FileNotFoundError:
    pass
