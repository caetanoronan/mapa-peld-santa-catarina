import json
import csv
from statistics import mean, median
import math

def compute_stdev(values):
    if not values or len(values) < 2:
        return 0
    m = mean(values)
    var = sum((x-m)**2 for x in values) / (len(values) - 1)
    return math.sqrt(var)
from collections import defaultdict, Counter

# Thresholds (can be tuned)
ALTITUDE_RANGE_THRESHOLD = 30  # meters (if altitude range per plot bigger than this -> alert)
HMAX_OUTLIER_Z = 3  # z-score for hmax outliers
DODGEL_OUTLIER_Z = 3  # z-score for dossel

# Read coordinates
with open('coordenadas_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    coords = json.loads(content[start:end])

# Read ecological data
with open('dados_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    start = content.find('[')
    end = content.rfind(']') + 1
    data = json.loads(content[start:end])

# Helper: compute biom total per record
def biom_total(row):
    vals = []
    for k in ['Biom1', 'Biom2', 'Biom3', 'Biom4']:
        v = row.get(k)
        if isinstance(v, (int, float)):
            vals.append(v)
    return sum(vals) if vals else None

# Group data by Plot
by_plot = defaultdict(list)
for row in data:
    plot = row.get('Plot')
    if plot:
        by_plot[plot].append(row)

# Compute per-plot aggregates (consolidated)
consolidated = []
for coord in coords:
    plot = coord['name']
    rows = by_plot.get(plot, [])
    n = len(rows)

    # numeric fields
    alt_vals = [r.get('Altitude') for r in rows if isinstance(r.get('Altitude'), (int, float))]
    hmax_vals = [r.get('hmax') for r in rows if isinstance(r.get('hmax'), (int, float))]
    dossel_vals = [r.get('dossel') for r in rows if isinstance(r.get('dossel'), (int, float))]
    biom_vals = [v for v in (biom_total(r) for r in rows) if isinstance(v, (int, float))]

    # vegetation type majority
    veg_counts = Counter([r.get('tipo.veg') for r in rows if r.get('tipo.veg')])
    veg_major = veg_counts.most_common(1)[0][0] if veg_counts else ''

    # build row
    row = {
        'Plot': plot,
        'Matches': n,
        'Veg_major': veg_major,
        'Altitude_mean': mean(alt_vals) if alt_vals else '',
        'Altitude_median': median(alt_vals) if alt_vals else '',
        'Altitude_min': min(alt_vals) if alt_vals else '',
        'Altitude_max': max(alt_vals) if alt_vals else '',
        'Altitude_range': (max(alt_vals)-min(alt_vals)) if alt_vals and len(alt_vals)>1 else '',
        'hmax_mean': mean(hmax_vals) if hmax_vals else '',
        'hmax_median': median(hmax_vals) if hmax_vals else '',
        'hmax_n': len(hmax_vals),
        'dossel_mean': mean(dossel_vals) if dossel_vals else '',
        'dossel_median': median(dossel_vals) if dossel_vals else '',
        'dossel_n': len(dossel_vals),
        'biom_total_mean': mean(biom_vals) if biom_vals else '',
        'biom_total_median': median(biom_vals) if biom_vals else '',
    }
    consolidated.append(row)

# Write consolidated CSV
with open('relatorio_consolidado_parcela.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(consolidated[0].keys()))
    writer.writeheader()
    for r in consolidated:
        writer.writerow(r)

# Build anomaly checks
alerts = []
# Altitude range too large
for r in consolidated:
    plot = r['Plot']
    if r['Altitude_range'] != '' and isinstance(r['Altitude_range'], (int, float)):
        if r['Altitude_range'] > ALTITUDE_RANGE_THRESHOLD:
            alerts.append({'Plot': plot, 'Type': 'ALTITUDE_RANGE', 'Value': r['Altitude_range'], 'Msg': f"Range greater than {ALTITUDE_RANGE_THRESHOLD} m"})

# Missing plot data (0 matches)
for coord in coords:
    plot = coord['name']
    if plot not in by_plot or len(by_plot[plot]) == 0:
        alerts.append({'Plot': plot, 'Type': 'NO_DATA', 'Value': 0, 'Msg': 'No rows for this plot'})

# Duplicate Antigo values per Plot (conflict)
for plot, rows in by_plot.items():
    antigos = [r.get('Antigo') for r in rows if r.get('Antigo')]
    if len(set(antigos)) > 1:
        alerts.append({'Plot': plot, 'Type': 'MULTI_ANTIGO', 'Value': len(set(antigos)), 'Msg': 'Multiple Antigo values mapped to same Plot'})

# Duplicate UniqueID across different plots
uid_to_plot = defaultdict(set)
for r in data:
    uid = r.get('UniqueID')
    if uid:
        uid_to_plot[uid].add(r.get('Plot'))
for uid, plots in uid_to_plot.items():
    if len(plots) > 1:
        alerts.append({'Plot': ';'.join(sorted(plots)), 'Type': 'UNIQUEID_DUP', 'Value': len(plots), 'Msg': f'UniqueID {uid} appears in multiple plots'})

# Outlier detection for hmax/dossel using simple z-score across all plots
import math

def z_scores(values):
    if not values:
        return []
    m = mean(values)
    if len(values) < 2:
        return [(v, 0) for v in values]
    s = compute_stdev(values)
    if s == 0:
        return [(v, 0) for v in values]
    return [(v, (v-m)/s) for v in values]

# hmax
all_hmax = [r.get('hmax') for r in data if isinstance(r.get('hmax'), (int, float))]
for plot, rows in by_plot.items():
    h_vals = [r.get('hmax') for r in rows if isinstance(r.get('hmax'), (int, float))]
    if not h_vals:
        continue
    # compute z-scores w.r.t all_hmax
    zs = []
    m = mean(all_hmax)
    s = compute_stdev(all_hmax) if len(all_hmax) > 1 else 0
    for v in h_vals:
        z = (v-m)/s if s>0 else 0
        if abs(z) >= HMAX_OUTLIER_Z:
            alerts.append({'Plot': plot, 'Type': 'HMAX_OUTLIER', 'Value': v, 'Msg': f'hmax z={z:.2f} exceeds {HMAX_OUTLIER_Z}'})

# dossel
all_dossel = [r.get('dossel') for r in data if isinstance(r.get('dossel'), (int, float))]
for plot, rows in by_plot.items():
    d_vals = [r.get('dossel') for r in rows if isinstance(r.get('dossel'), (int, float))]
    if not d_vals:
        continue
    m = mean(all_dossel)
    s = compute_stdev(all_dossel) if len(all_dossel) > 1 else 0
    for v in d_vals:
        z = (v-m)/s if s>0 else 0
        if abs(z) >= DODGEL_OUTLIER_Z:
            alerts.append({'Plot': plot, 'Type': 'DOSSEL_OUTLIER', 'Value': v, 'Msg': f'dossel z={z:.2f} exceeds {DODGEL_OUTLIER_Z}'})

# Write alerts CSV
if alerts:
    with open('alertas_dados.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Plot','Type','Value','Msg'])
        writer.writeheader()
        for a in alerts:
            writer.writerow(a)
else:
    print('Nenhum alerta encontrado')

print('Advanced reports generated: relatorio_consolidado_parcela.csv, alertas_dados.csv (if any)')
