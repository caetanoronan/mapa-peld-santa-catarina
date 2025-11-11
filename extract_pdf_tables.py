import pdfplumber
import pandas as pd

pdf_path = 'Parcelas PPBio Atualizadas.pdf'

print("Extraindo tabelas do PDF...")

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\nPágina {i+1}:")
        tables = page.extract_tables()
        if tables:
            for j, table in enumerate(tables):
                print(f"Tabela {j+1}:")
                df = pd.DataFrame(table)
                print(df)
                print("\n" + "="*50)
        else:
            print("Nenhuma tabela encontrada nesta página.")

# Também extrair texto completo para contexto
text = ""
for page in pdf.pages:
    text += page.extract_text() + "\n"

print("\nTexto completo extraído:")
print(text)