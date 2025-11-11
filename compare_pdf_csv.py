import pdfplumber
import pandas as pd
import re

# Extrair texto do PDF
pdf_path = 'Parcelas PPBio Atualizadas.pdf'

print("Extraindo texto do PDF...")

with pdfplumber.open(pdf_path) as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

print("Texto extraído do PDF:")
print("=" * 50)
print(text[:2000])  # Mostrar primeiras 2000 caracteres
print("=" * 50)

# Carregar dados do CSV
csv_path = 'amb_csv/amb.csv'
df_csv = pd.read_csv(csv_path, encoding='latin-1')

print(f"\nDados do CSV ({len(df_csv)} registros):")
print("=" * 50)
print(df_csv.head(10))
print("=" * 50)

# Tentar extrair informações específicas do PDF
# Procurar por padrões como códigos de parcela, altitudes, etc.

# Procurar por códigos de parcela no PDF (padrão como M01T01, etc.)
parcel_codes_pdf = re.findall(r'M\d{2}[TR]\d{2}', text)
print(f"\nCódigos de parcela encontrados no PDF: {len(set(parcel_codes_pdf))} únicos")
print(set(parcel_codes_pdf))

# Verificar códigos únicos no CSV
parcel_codes_csv = df_csv['Plot'].unique()
print(f"Códigos de parcela no CSV: {len(parcel_codes_csv)} únicos")
print(parcel_codes_csv)

# Comparar altitudes
altitudes_pdf = re.findall(r'\b\d{3,4}\b', text)  # Procurar números de 3-4 dígitos (altitudes)
altitudes_pdf = [int(x) for x in altitudes_pdf if 400 <= int(x) <= 1700]  # Filtrar altitudes plausíveis

print(f"\nAltitudes encontradas no PDF: {len(altitudes_pdf)} valores")
print(sorted(set(altitudes_pdf)))

altitudes_csv = df_csv['Altitude'].dropna().unique()
print(f"Altitudes no CSV: {len(altitudes_csv)} valores únicos")
print(sorted(altitudes_csv.astype(int)))

# Verificar se os dados estão consistentes
print("\n" + "=" * 50)
print("VERIFICAÇÃO DE CONSISTÊNCIA")
print("=" * 50)

# Verificar se todas as parcelas do CSV estão mencionadas no PDF
missing_in_pdf = []
for code in parcel_codes_csv:
    if code not in parcel_codes_pdf:
        missing_in_pdf.append(code)

if missing_in_pdf:
    print(f"Parcelas do CSV NÃO encontradas no PDF: {missing_in_pdf}")
else:
    print("✅ Todas as parcelas do CSV foram encontradas no PDF")

# Verificar altitudes
csv_altitudes_set = set(altitudes_csv.astype(int))
pdf_altitudes_set = set(altitudes_pdf)

common_altitudes = csv_altitudes_set.intersection(pdf_altitudes_set)
missing_altitudes = csv_altitudes_set - pdf_altitudes_set

print(f"Altitudes comuns: {len(common_altitudes)}")
if missing_altitudes:
    print(f"Altitudes do CSV não encontradas no PDF: {sorted(missing_altitudes)}")

# Salvar texto extraído para análise posterior
with open('pdf_extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("\nTexto completo do PDF salvo em 'pdf_extracted_text.txt'")