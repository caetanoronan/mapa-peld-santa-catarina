import csv
from pathlib import Path

BOOTSTRAP_CDN = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"
DATATABLES_CSS = "https://cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css"
JQUERY = "https://code.jquery.com/jquery-3.7.1.min.js"
DATATABLES_JS = "https://cdn.datatables.net/1.13.5/js/jquery.dataTables.min.js"

# Files to present
files = {
    'Correspondências e Duplicatas': 'relatorio_correspondencias_duplicatas.csv',
    'Resumo por Parcela': 'resumo_por_parcela.csv',
    'Consolidado por Parcela': 'relatorio_consolidado_parcela.csv',
    'Alertas de Dados': 'alertas_dados.csv',
}

out = Path('relatorios_dashboard.html')

html = []
html.append(f"<!doctype html><html lang=\"pt-br\"><head><meta charset=\"utf-8\"/>")
html.append(f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>")
html.append(f"<link rel=\"stylesheet\" href=\"{BOOTSTRAP_CDN}\">")
html.append(f"<link rel=\"stylesheet\" href=\"{DATATABLES_CSS}\">")
html.append("<title>Relatórios PELD - Dashboard</title>")
html.append("</head><body>")
html.append('<div class="container my-4">')
html.append('<h2>Relatórios PELD - Conferência</h2>')
html.append('<p class="text-muted">Tabela interativa — ordene, filtre e exporte direto do navegador.</p>')
# Nav tabs
html.append('<ul class="nav nav-tabs" id="relTabs" role="tablist">')
first=True
for idx,title in enumerate(files.keys()):
    active = 'active' if first else ''
    aria = 'true' if first else 'false'
    html.append(f'<li class="nav-item" role="presentation">')
    html.append(f'<button class="nav-link {active}" id="tab{idx}-tab" data-bs-toggle="tab" data-bs-target="#tab{idx}" type="button" role="tab" aria-controls="tab{idx}" aria-selected="{aria}">{title}</button>')
    html.append('</li>')
    first=False
html.append('</ul>')

# Tab content
html.append('<div class="tab-content mt-3" id="relTabsContent">')
first=True
for idx,(title,filename) in enumerate(files.items()):
    active = 'show active' if idx==0 else ''
    html.append(f'<div class="tab-pane fade {active}" id="tab{idx}" role="tabpanel" aria-labelledby="tab{idx}-tab">')
    if Path(filename).exists():
        # read CSV
        rows = []
        with open(filename, encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for r in reader:
                rows.append(r)
        # table
        html.append('<div class="table-responsive">')
        html.append(f'<table id="table{idx}" class="display table table-striped" style="width:100%">')
        html.append('<thead><tr>')
        for h in headers:
            html.append(f'<th>{h}</th>')
        html.append('</tr></thead>')
        html.append('<tbody>')
        for r in rows:
            html.append('<tr>')
            for cell in r:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')
        html.append('</table></div>')
        html.append(f'<p>Arquivo: <code>{filename}</code> — <a href="{filename}" download>Baixar CSV</a></p>')
    else:
        html.append(f'<div class="alert alert-warning">Arquivo <code>{filename}</code> não encontrado.</div>')
    html.append('</div>')
html.append('</div>')

# Scripts
html.append(f'<script src="{JQUERY}"></script>')
html.append(f'<script src="{DATATABLES_JS}"></script>')
html.append('<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>')
html.append('<script>')
# Initialize tables
for idx in range(len(files)):
    html.append(f'$(document).ready(function(){{ $("#table{idx}").DataTable({{"pageLength": 25}}); }});')
html.append('</script>')

html.append('</div></body></html>')

out.write_text('\n'.join(html), encoding='utf-8')
print('relatorios_dashboard.html gerado!')
