# Projeto PELD - Mapa Interativo de Coordenadas

Este projeto contém dados e mapas relacionados ao Programa de Pesquisa Ecológica de Longa Duração (PELD) em Santa Catarina, Brasil.

## Mapa Interativo

O arquivo `mapa_interativo_peld.html` é um mapa interativo criado com Folium (baseado em Leaflet.js) mostrando as coordenadas das parcelas terrestres e ripárias dos módulos M1, M2 e M3.

### Características:
- **Marcadores coloridos**: Azul para parcelas terrestres, verde para ripárias
- **Popups informativos**: Módulo, nome, tipo, coordenadas
- **Controle de camadas**: Permite mostrar/ocultar tipos de parcelas, parques e cidades afetadas
- **Limite do Parque Nacional São Joaquim**: Polígono verde escuro (45.524 ha)
- **Limite do Parque Estadual da Serra Furada**: Polígono azul (zonas de uso)
- **Cidades Afetadas pelo PARNA**: Polígonos laranja/vermelho com tooltips (nome e área)
- **Limite Estadual de Santa Catarina**: Linha preta grossa (contorno do estado)
- **Interatividade**: Zoom, pan, cliques
- **Limites de zoom**: Zoom mínimo 8 (visão regional), zoom máximo 18 (detalhes locais)
- **Base OpenStreetMap**: Gratuita e atualizada

### Como visualizar:
- Abra o arquivo `mapa_interativo_peld.html` em qualquer navegador web.
- Use o controle de camadas no canto superior direito para alternar entre tipos de parcelas.

### Camadas Disponíveis:
1. **Parcelas terrestres** (marcadores azuis)
2. **Parcelas ripárias** (marcadores verdes)  
3. **Parque Nacional de São Joaquim** (polígono verde escuro - 45.524 ha)
4. **Parque Estadual da Serra Furada** (polígono azul - 1.330 ha, 6 zonas)
5. **Cidades afetadas pelo PARNA** (polígonos laranja/vermelho com tooltips)
6. **Limite Estadual de Santa Catarina** (linha preta grossa - contorno do estado)

### Dados utilizados:
- Arquivo: `amb_csv/ppbio_sc-coordenadas_parcelas.csv`
- Contém coordenadas geográficas (latitude/longitude) de parcelas de monitoramento.
- **Limite do Parque Nacional São Joaquim**: `PROJETO_PELDSC/PARNA_SAO_JOAQUIM_SHP/PARNA SAO JOAQUIM SHP/PARNASJlimites.shp`
- **Limite do Parque Estadual da Serra Furada**: `Projeto_PARNA_PESF/PARQUE_PESF_1_temp.shp` (1.330 ha, 6 zonas de uso)
- **Cidades Afetadas pelo PARNA**: `Projeto_PARNA_PESF/Cidades_parna_sj_temp.shp`
- **Limite Estadual de Santa Catarina**: `Organizacao Territorio/SC_UF_2024/SC_UF_2024.shp`

## Estrutura do Projeto

- `amb_csv/`: Dados CSV de coordenadas
- `Imagens/`: Imagens Landsat e outros dados raster
- `Indice_vegetacao/`: Dados de índices de vegetação (NDVI, EVI, SAVI)
- `Projeto_PARNA_PESF/`: Projetos QGIS e shapefiles do Parque Nacional São Joaquim
- `PROJETO_PELDSC/`: Dados geográficos adicionais
- `Relatorio/`: Relatórios e documentação

## Tecnologias Utilizadas

- **Folium**: Biblioteca Python para mapas interativos
- **Pandas**: Para processamento de dados CSV
- **Leaflet.js**: Biblioteca JavaScript subjacente
- **GeoPandas**: Para conversão de shapefiles (futuro)

## Inspiração

Adaptado do estilo de mapas interativos como o projeto de linhas de transmissão (https://caetanoronan.github.io/linhas-transmissao-foz-iguacu/), com foco em dados ecológicos e biodiversidade.

## Publicação Online

Para tornar este mapa acessível ao público:

1. **GitHub Pages**: Faça upload do repositório para GitHub e ative Pages.
2. **Netlify**: Faça deploy direto do HTML.
3. **Vercel**: Plataforma similar ao Netlify.
4. **Google Drive/Dropbox**: Compartilhe o HTML diretamente.

O mapa é totalmente autônomo (HTML + JS + CSS embutidos), não requer servidor backend.

### Acesso Online

Após publicar no GitHub Pages, o mapa estará disponível em:
`https://SEU_USERNAME.github.io/NOME_DO_REPOSITORIO/mapa_interativo_peld.html`

### Como Ativar GitHub Pages:

1. Vá para o repositório no GitHub
2. Clique em "Settings" 
3. Role para baixo até "Pages"
4. Em "Source", selecione "Deploy from a branch"
5. Em "Branch", selecione "master" ou "main" e "/ (root)"
6. Clique em "Save"
7. Aguarde alguns minutos para o deploy completar

## Contato

Projeto PELD - Biodiversidade de Santa Catarina