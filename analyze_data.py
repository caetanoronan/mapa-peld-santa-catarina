import json

# Load the data
with open('dados_ppBio.js', 'r', encoding='utf-8') as f:
    content = f.read()
    # Remove the JavaScript wrapper
    data_str = content.replace('// Dados PPBio carregados do CSV\nwindow.ppbioData = ', '').replace(';', '')
    data = json.loads(data_str)

print(f'Total de registros: {len(data)}')
if data:
    print('Primeiro registro:')
    for key, value in data[0].items():
        print(f'  {key}: {value} (type: {type(value).__name__})')

    # Check for null/NaN values in key fields
    print('\nVerificando campos importantes:')
    fields_to_check = ['Altitude', 'Biom1', 'Biom2', 'Biom3', 'Biom4', 'tipo.veg', 'Mod']
    for field in fields_to_check:
        values = [d.get(field) for d in data if field in d]
        null_count = sum(1 for v in values if v is None or (isinstance(v, float) and str(v).lower() == 'nan'))
        print(f'  {field}: {len(values)} valores, {null_count} nulos/NaN')