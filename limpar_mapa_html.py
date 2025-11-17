import re

# Parcelas que foram removidas e precisam ser eliminadas do HTML
parcelas_removidas = [
    'TL054_RIP8', 'TL077_RIP7', 'TL3500_PSA2', 'RIP_PSA3', 'TL4200_RIP',
    'TL4500_PSA1', 'RIP_PSA8', 'TN066_RIP9', 'TW144_RIP1', 'TW125_RIP2_PSA7',
    'TW105_RIP3', 'TW4600'
]

# Ler o arquivo HTML
with open('mapa_simples_completo_atualizado.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Arquivo HTML original: {len(content)} caracteres')

# Para cada parcela removida, encontrar e remover o bloco de código correspondente
removidas_count = 0
for parcela in parcelas_removidas:
    # Padrão para encontrar o bloco var marker_... = L.marker(...).addTo(layer_group_...)
    # Seguido pelo bloco var html_... = $(`<div... até o marker.bindPopup(html_...)
    pattern = rf'var marker_[a-f0-9_]{{32}} = L\.marker\(\[.*?\]\).*?\.addTo\(layer_group_[a-f0-9_]{{32}}\);\s*var html_[a-f0-9_]{{32}} = \$\(`<div.*?{re.escape(parcela)}.*?</div>`\)\[0\];\s*marker_[a-f0-9_]{{32}}\.bindPopup\(html_[a-f0-9_]{{32}}\);'

    # Usar uma abordagem mais simples: procurar por blocos que contenham o nome da parcela
    # e remover desde "var marker_" até o "bindPopup" correspondente

    # Primeiro, encontrar todas as ocorrências do nome da parcela
    occurrences = []
    start_pos = 0
    while True:
        pos = content.find(parcela, start_pos)
        if pos == -1:
            break
        occurrences.append(pos)
        start_pos = pos + 1

    print(f'{parcela}: {len(occurrences)} ocorrências encontradas')

    # Para cada ocorrência, encontrar o bloco completo do marker
    for pos in reversed(occurrences):  # Do fim para o início para não afetar posições
        # Encontrar o início do bloco (var marker_)
        marker_start = content.rfind('var marker_', 0, pos)
        if marker_start == -1:
            continue

        # Encontrar o fim do bloco (ponto e vírgula após bindPopup)
        bind_popup_end = content.find(';', pos)
        if bind_popup_end == -1:
            continue

        # Encontrar o próximo ponto e vírgula após bindPopup para garantir que pegamos o bloco completo
        next_semicolon = content.find(';', bind_popup_end + 1)
        if next_semicolon == -1:
            next_semicolon = bind_popup_end + 1

        # Extrair o bloco
        block = content[marker_start:next_semicolon + 1]

        # Verificar se o bloco contém o nome da parcela
        if parcela in block:
            print(f'  Removendo bloco de {len(block)} caracteres')
            content = content[:marker_start] + content[next_semicolon + 1:]
            removidas_count += 1

print(f'\\nTotal de blocos removidos: {removidas_count}')

# Salvar o arquivo limpo
with open('mapa_simples_completo_atualizado.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Arquivo HTML limpo: {len(content)} caracteres')
print('Arquivo mapa_simples_completo_atualizado.html atualizado!')