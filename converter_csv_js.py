import pandas as pd
import json

# Carregar dados
df = pd.read_csv('analise_integrada_pdf_csv.csv')

# Converter para formato JavaScript
data_js = df.to_dict('records')

# Criar arquivo JavaScript com os dados
js_content = f"""
// Dados PPBio carregados do CSV
const ppbioData = {json.dumps(data_js, indent=2)};

console.log('Dados PPBio carregados:', ppbioData.length, 'registros');
"""

with open('dados_ppBio.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Arquivo dados_ppBio.js criado com {len(data_js)} registros!")