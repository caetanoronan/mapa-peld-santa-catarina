import markdown
import pdfkit
from datetime import datetime

# Ler o arquivo markdown
with open('RELATORIO_AVALIACAO_VIABILIDADE_REMOTA_M2.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Converter para HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# Template HTML completo
html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Avaliação de Viabilidade Remota - Módulo 2</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }}

        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            text-align: center;
            font-size: 24px;
        }}

        h2 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 10px;
            margin-top: 30px;
            font-size: 20px;
        }}

        h3 {{
            color: #34495e;
            font-size: 16px;
            margin-top: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 12px;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}

        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        .resumo-executivo {{
            background-color: #ecf0f1;
            padding: 20px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
        }}

        .dificuldade-facil {{
            background-color: #d4edda;
            color: #155724;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}

        .dificuldade-medio {{
            background-color: #fff3cd;
            color: #856404;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}

        .dificuldade-dificil {{
            background-color: #f8d7da;
            color: #721c24;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
        }}

        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #3498db;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}

        .data-geracao {{
            text-align: right;
            font-size: 11px;
            color: #666;
            margin-bottom: 20px;
        }}

        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 11px;
        }}

        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <div class="data-geracao">
        Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>

    {html_content}

    <div class="footer">
        <p><strong>Programa PELD-BISC</strong> | Universidade Federal de Santa Catarina</p>
        <p>Relatório de Avaliação de Viabilidade Remota - Análise baseada em dados geoespaciais públicos</p>
        <p>Contato: caetanoronan@gmail.com | Site: https://peldbisc.ufsc.br</p>
    </div>
</body>
</html>
"""

# Salvar HTML temporário
with open('RELATORIO_AVALIACAO_VIABILIDADE_REMOTA_M2.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ HTML gerado com sucesso: RELATORIO_AVALIACAO_VIABILIDADE_REMOTA_M2.html")

# Nota: Para gerar PDF, instale wkhtmltopdf de https://wkhtmltopdf.org/downloads.html
# Depois descomente o código abaixo:

# # Configurações do PDF
# options = {
#     'page-size': 'A4',
#     'margin-top': '1.5in',
#     'margin-right': '1in',
#     'margin-bottom': '1.5in',
#     'margin-left': '1in',
#     'encoding': 'UTF-8',
#     'no-outline': None,
#     'enable-local-file-access': None
# }

# # Converter para PDF
# try:
#     pdfkit.from_file('relatorio_temp.html', 'RELATORIO_AVALIACAO_VIABILIDADE_REMOTA_M2.pdf', options=options)
#     print("✅ PDF gerado com sucesso: RELATORIO_AVALIACAO_VIABILIDADE_REMOTA_M2.pdf")
# except Exception as e:
#     print(f"❌ Erro ao gerar PDF: {e}")
#     print("Instale o wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")