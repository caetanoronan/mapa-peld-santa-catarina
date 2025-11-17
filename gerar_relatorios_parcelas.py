import json
import csv
from statistics import mean, median
from collections import Counter, defaultdict

# Load coordinates
with open('coordenadas_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    coords = json.loads(content[start:end])

# Load ecological data
with open('dados_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    data = json.loads(content[start:end])

# Map data by Plot
by_plot = defaultdict(list)
for item in data:
    plot = item.get('Plot')
    if plot:
        by_plot[plot].append(item)

# 1) Create correspondences/duplicates CSV
with open('relatorio_correspondencias_duplicatas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Plot', 'Matches', 'UniqueIDs', 'Sample_Antigo', 'Sample_UniqueIDs'])
    for coord in coords:
        plot = coord['name']
        rows = by_plot.get(plot, [])
        matches = len(rows)
        uniqueids = len({r.get('UniqueID') for r in rows if r.get('UniqueID')})
        sample_antigo = ','.join({r.get('Antigo') or '' for r in rows}) if rows else ''
        sample_uids = ','.join(sorted({r.get('UniqueID') or '' for r in rows})[:5])
        writer.writerow([plot, matches, uniqueids, sample_antigo, sample_uids])

# 2) Create summary per parcela CSV
numeric_fields = ['Altitude', 'hmax', 'dossel']
# Create derived 'Biom_total'
def compute_biom_total(row):
    vals = []
    for k in ['Biom1', 'Biom2', 'Biom3', 'Biom4']:
        v = row.get(k)
        if isinstance(v, (int, float)):
            vals.append(v)
    return sum(vals) if vals else None

with open('resumo_por_parcela.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['Plot', 'Matches', 'TipoVeg_Majoritario'] + [f'{field}_mean' for field in numeric_fields] + [f'{field}_median' for field in numeric_fields] + ['Biom_total_mean','Biom_total_median','Altitude_count']
    writer.writerow(header)

    for coord in coords:
        plot = coord['name']
        rows = by_plot.get(plot, [])
        matches = len(rows)
        tipo_counts = Counter([r.get('tipo.veg') for r in rows if r.get('tipo.veg')])
        tipo_major = tipo_counts.most_common(1)[0][0] if tipo_counts else ''

        numeric_means = []
        numeric_meds = []
        for field in numeric_fields:
            vals = [r.get(field) for r in rows if isinstance(r.get(field), (int, float))]
            numeric_means.append(mean(vals) if vals else '')
            numeric_meds.append(median(vals) if vals else '')

        biom_vals = [compute_biom_total(r) for r in rows if compute_biom_total(r) is not None]
        biom_mean = mean(biom_vals) if biom_vals else ''
        biom_med = median(biom_vals) if biom_vals else ''

        alt_count = len([r for r in rows if isinstance(r.get('Altitude'), (int, float))])

        writer.writerow([plot, matches, tipo_major] + numeric_means + numeric_meds + [biom_mean, biom_med, alt_count])

print('Relatórios gerados: relatorio_correspondencias_duplicatas.csv, resumo_por_parcela.csv')
